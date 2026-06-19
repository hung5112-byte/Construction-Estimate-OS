"""Run tools in parallel after clarification, before the meeting."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from core.tools.tool_router import ToolRouter, ToolCall
from core.tools.web_search import WebSearch
from core.tools.us_law_search import USLawSearch
from core.tools.us_local_regulation import USLocalRegulation
from core.tools.competitor_research import CompetitorResearch
from core.tools.industry_benchmark import IndustryBenchmark
from core.tools.tax_calculator import TaxCalculator


TOOL_REGISTRY = {
    "web_search": WebSearch,
    "us_law_search": USLawSearch,
    "us_local_regulation": USLocalRegulation,
    "competitor_research": CompetitorResearch,
    "industry_benchmark": IndustryBenchmark,
    "tax_calculator": TaxCalculator,
}


def list_available_tools() -> list[str]:
    """Returns tool names có credentials/dependencies. Safe to call anywhere."""
    available: list[str] = []
    for name, cls in TOOL_REGISTRY.items():
        try:
            instance = cls()
            if instance.is_available():
                available.append(name)
        except Exception:  # noqa: BLE001
            pass
    return available


def list_skipped_tools() -> list[dict]:
    """Returns list of {name, reason} for tools missing credentials."""
    skipped: list[dict] = []
    for name, cls in TOOL_REGISTRY.items():
        try:
            instance = cls()
            if not instance.is_available():
                skipped.append({
                    "name": name,
                    "reason": "Missing TAVILY_API_KEY"
                            if "search" in name or "research" in name or "regulation" in name
                            else "Unavailable",
                })
        except Exception as e:  # noqa: BLE001
            skipped.append({"name": name, "reason": str(e)})
    return skipped


class ResearchPhase:
    def __init__(self, llm, vault_root: Path | None = None):
        """
        Args:
            llm: LLM provider
            vault_root: P2.3 — if provided, the tool cache is stored in
                <vault>/.cache/tool_cache.db instead of the global
                ~/.bd-business-os/. A per-vault cache prevents cross-company
                cache poisoning.
        """
        # Filter ToolRouter to only credentialed tools (RULE 5 — no silent fail)
        self.tool_router = ToolRouter(llm, available_tools=list_available_tools())
        self.vault_root = Path(vault_root) if vault_root else None

    def _cache_path(self) -> Path | None:
        """Return the per-vault cache path if vault_root is set, else None (tool uses default)."""
        if self.vault_root is None:
            return None
        cache_dir = self.vault_root / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / "tool_cache.db"

    def _instantiate_tool(self, tool_cls):
        """Init the tool with a per-vault cache_path if it accepts that kwarg."""
        cache_path = self._cache_path()
        if cache_path is None:
            return tool_cls()
        try:
            return tool_cls(cache_path=cache_path)
        except TypeError:
            # Tool does not accept cache_path (e.g. tax_calculator is pure compute)
            return tool_cls()

    def run(self, brief: str, brain_summary: str, task_folder: Path) -> dict:
        plan = self.tool_router.plan(brief, brain_summary)
        results: dict[str, list] = {}

        with ThreadPoolExecutor(max_workers=4) as ex:
            futures = {}
            for call in plan:
                tool_name = call["tool"]
                tool_cls = TOOL_REGISTRY.get(tool_name)
                if not tool_cls:
                    continue
                tool = self._instantiate_tool(tool_cls)
                for q in call.get("queries", []):
                    futures[ex.submit(tool.run, q)] = (tool_name, q)

            for fut, (tool_name, q) in futures.items():
                try:
                    r = fut.result()
                    results.setdefault(tool_name, []).append({
                        "query": q, "data": r.data,
                        "sources": r.sources, "retrieved_at": r.retrieved_at,
                    })
                except Exception as e:
                    results.setdefault(tool_name, []).append({
                        "query": q, "error": str(e),
                    })

        self._write_findings(task_folder, plan, results)
        return results

    def _write_findings(self, folder: Path, plan: list[ToolCall], results: dict):
        parts = ["---", "type: research_findings", "---", "", "# Research findings", ""]
        for tool_name, calls in results.items():
            parts.append(f"## {tool_name}")
            for c in calls:
                parts.append(f"\n### Query: `{c['query']}`")
                if "error" in c:
                    parts.append(f"Error: {c['error']}")
                else:
                    parts.append(f"**Data:**\n```yaml\n{c['data']}\n```")
                    parts.append(f"**Sources:** {', '.join(c.get('sources', []))}")
                    parts.append(f"**Retrieved:** {c.get('retrieved_at', '?')}")
        (folder / "03b-research-findings.md").write_text(
            "\n".join(parts), encoding="utf-8"
        )
