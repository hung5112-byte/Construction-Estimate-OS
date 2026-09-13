"""Run tools in parallel after clarification, before the meeting."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from core.llm.activity_log import agent_span, log_activity
from core.tools.tool_router import ToolRouter, ToolCall
from core.tools.web_search import WebSearch
from core.tools.us_law_search import USLawSearch
from core.tools.us_local_regulation import USLocalRegulation
from core.tools.competitor_research import CompetitorResearch
from core.tools.industry_benchmark import IndustryBenchmark
from core.tools.tax_calculator import TaxCalculator
from core.tools.landed_cost import LandedCost
from core.tools.supplier_risk import SupplierRisk
from core.tools.bom_health import BomHealth
from core.tools.capa_8d import Capa8D
from core.tools.compliance_tracker import ComplianceTracker
from core.tools.vault_search import VaultSearchTool


from core.tools.estimating_tools import ESTIMATING_TOOLS

TOOL_REGISTRY = {
    "vault_search": VaultSearchTool,
    "web_search": WebSearch,
    "us_law_search": USLawSearch,
    "us_local_regulation": USLocalRegulation,
    "competitor_research": CompetitorResearch,
    "industry_benchmark": IndustryBenchmark,
    "tax_calculator": TaxCalculator,
    "landed_cost": LandedCost,
    "supplier_risk": SupplierRisk,
    "bom_health": BomHealth,
    "capa_8d": Capa8D,
    "compliance_tracker": ComplianceTracker,
    **ESTIMATING_TOOLS,
}


def list_available_tools(vault_root: Path | None = None) -> list[str]:
    """Returns tool names có credentials/dependencies. Safe to call anywhere.

    vault_root is forwarded to tools that accept it (vault_search needs it to
    find the per-vault index); tools that don't accept it are constructed bare.
    """
    available: list[str] = []
    for name, cls in TOOL_REGISTRY.items():
        try:
            instance = _construct_tool(cls, vault_root=vault_root)
            if instance.is_available():
                available.append(name)
        except Exception:  # noqa: BLE001
            pass
    return available


def _construct_tool(tool_cls, cache_path: Path | None = None, vault_root: Path | None = None):
    """Instantiate a tool with whichever of (cache_path, vault_root) it accepts.

    Signature-inspected rather than try/except-TypeError, so a genuine
    TypeError raised INSIDE a tool's __init__ propagates instead of being
    silently retried with fewer kwargs.
    """
    import inspect

    provided = {"cache_path": cache_path, "vault_root": vault_root}
    try:
        params = inspect.signature(tool_cls.__init__).parameters
        accepts_kwargs = any(
            p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()
        )
    except (TypeError, ValueError):
        params, accepts_kwargs = {}, False
    kwargs = {
        k: v for k, v in provided.items()
        if v is not None and (accepts_kwargs or k in params)
    }
    return tool_cls(**kwargs)


def list_skipped_tools(vault_root: Path | None = None) -> list[dict]:
    """Returns list of {name, reason} for tools missing credentials."""
    skipped: list[dict] = []
    for name, cls in TOOL_REGISTRY.items():
        try:
            instance = _construct_tool(cls, vault_root=vault_root)
            if not instance.is_available():
                if name == "vault_search":
                    reason = "vault index not built — run `bd-os index`"
                elif "search" in name or "research" in name or "regulation" in name:
                    reason = "Missing TAVILY_API_KEY"
                else:
                    reason = "Unavailable"
                skipped.append({"name": name, "reason": reason})
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
        self.vault_root = Path(vault_root) if vault_root else None
        # Filter ToolRouter to only credentialed tools (RULE 5 — no silent fail)
        self.tool_router = ToolRouter(
            llm, available_tools=list_available_tools(vault_root=self.vault_root)
        )

    def _cache_path(self) -> Path | None:
        """Return the per-vault cache path if vault_root is set, else None (tool uses default)."""
        if self.vault_root is None:
            return None
        cache_dir = self.vault_root / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / "tool_cache.db"

    def _instantiate_tool(self, tool_cls):
        """Init the tool with per-vault cache_path/vault_root if it accepts them."""
        return _construct_tool(
            tool_cls, cache_path=self._cache_path(), vault_root=self.vault_root
        )

    def run(self, brief: str, brain_summary: str, task_folder: Path) -> dict:
        with agent_span("researcher", stage="research", task=task_folder.name):
            results = self._run(brief, brain_summary, task_folder)
        summary = ("Research findings ready — tools: " + ", ".join(results)
                   if results else "No live research tools ran for this brief")
        log_activity("researcher", "say", stage="research",
                     task=task_folder.name, text=summary)
        return results

    def _run(self, brief: str, brain_summary: str, task_folder: Path) -> dict:
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
                    entry = {
                        "query": q, "data": r.data,
                        "sources": r.sources, "retrieved_at": r.retrieved_at,
                    }
                    if r.notes:  # e.g. vault_search's NO-MATCH anti-fabrication sentinel
                        entry["notes"] = r.notes
                    results.setdefault(tool_name, []).append(entry)
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
                    if c.get("notes"):
                        parts.append(f"**Note:** {c['notes']}")
        (folder / "03b-research-findings.md").write_text(
            "\n".join(parts), encoding="utf-8"
        )
