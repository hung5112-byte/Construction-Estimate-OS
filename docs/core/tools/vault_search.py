"""vault_search — search the company's own vault via the local FTS5 index.

RULE 5: sources are vault-relative `path#heading` refs, resolvable by the
critic and clickable in Obsidian. RULE 3: the index is a rebuildable cache;
if it doesn't exist the tool reports itself unavailable instead of guessing.
"""
from __future__ import annotations

from pathlib import Path

from core.retrieval.indexer import index_db_path
from core.retrieval.search import VaultSearcher
from core.tools.base_tool import BaseTool, ToolResult

NO_MATCH_SENTINEL = (
    "NO MATCH FOUND in the vault index — do not invent prior context; "
    "answer from the task inputs only."
)


class VaultSearchTool(BaseTool):
    name = "vault_search"
    description = "hybrid keyword+semantic+link search over the company's own vault (Brain, task reports, SOPs) — local, instant, no API key"
    cache_ttl_seconds = 0  # local + instant; caching would only serve stale hits

    def __init__(self, cache_path: Path | None = None, vault_root: Path | None = None):
        # ResearchPhase._instantiate_tool passes cache_path=<vault>/.cache/tool_cache.db;
        # derive the vault root from it when vault_root isn't given explicitly.
        if vault_root is None and cache_path is not None:
            vault_root = Path(cache_path).resolve().parent.parent
        self.vault_root = Path(vault_root) if vault_root is not None else None

    def is_available(self) -> bool:
        return self.vault_root is not None and index_db_path(self.vault_root).exists()

    def run(self, query: str, k: int = 6, **kwargs) -> ToolResult:
        if not self.is_available():
            return self.skipped_result("vault index not built — run `bd-os index`")
        try:
            # Incremental sync so agents never search a stale index; cheap
            # (stat-compare) when nothing changed, and never fatal to the search.
            # embed=False: NEVER init the embedding model on the meeting path —
            # changed notes get keyword coverage immediately; their vectors
            # refresh on the next `bd-os index` / nightly run (doctor reports
            # the coverage gap).
            from core.retrieval.indexer import VaultIndexer
            VaultIndexer(self.vault_root, embed=False).build()
        except Exception:  # noqa: BLE001 — searching the existing index beats failing
            pass
        hits = VaultSearcher(self.vault_root).search(query, k=k)
        payload = [
            {"source": h.source, "breadcrumb": h.breadcrumb,
             "snippet": h.snippet, "score": round(h.score, 3),
             # provenance surfaced to the agent: ingested-doc content is
             # evidence from outside, not vault-native truth
             "trust": h.trust_tier}
            for h in hits
        ]
        return ToolResult(
            data={"hits": payload},
            sources=[h.source for h in hits],
            notes="" if hits else NO_MATCH_SENTINEL,
        )
