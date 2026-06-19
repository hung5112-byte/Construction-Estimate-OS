"""Texas state agency regulations (state-level). General information only,
not legal advice. For city/county rules, consult the relevant local jurisdiction."""
from __future__ import annotations
import os
from pathlib import Path
from core.tools.base_tool import BaseTool, ToolResult
from core.tools.tool_cache import ToolCache


TRUSTED_LOCAL_DOMAINS = [
    "texas.gov",                  # Texas state portal
    "comptroller.texas.gov",      # Texas taxes & business registration
    "sos.state.tx.us",            # Texas Secretary of State
    "twc.texas.gov",              # Texas Workforce Commission (labor)
    "dshs.texas.gov",             # Texas Dept. of State Health Services (food, health)
    "tdlr.texas.gov",             # Texas Dept. of Licensing & Regulation
]


class USLocalRegulation(BaseTool):
    name = "us_local_regulation"
    description = "Texas state agency rules (Comptroller, SOS, TWC, DSHS, TDLR)."

    def __init__(self, api_key: str | None = None, cache_path: Path | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY", "")
        self.cache = ToolCache(cache_path or Path.home() / ".bd-business-os" / "tool_cache.db")

    def is_available(self) -> bool:
        return bool(self.api_key)

    def run(self, query: str, jurisdiction: str = "", **kwargs) -> ToolResult:
        if not self.is_available():
            return self.skipped_result(
                "Missing TAVILY_API_KEY — cannot look up state agency rules online"
            )

        full_q = f"{query} {jurisdiction}".strip()
        hit = self.cache.get(full_q, source=self.name)
        if hit:
            return ToolResult(data=hit, sources=hit.get("urls", []), cached=True)

        try:
            from tavily import TavilyClient
        except ImportError:
            return self.skipped_result("Package 'tavily-python' is not installed")

        client = TavilyClient(api_key=self.api_key)
        resp = client.search(
            query=full_q, max_results=6,
            include_domains=TRUSTED_LOCAL_DOMAINS, include_answer=True,
        )
        urls = [r["url"] for r in resp.get("results", [])]
        data = {"answer": resp.get("answer", ""), "results": resp.get("results", []), "urls": urls}
        self.cache.set(full_q, data, source=self.name)
        return ToolResult(data=data, sources=urls)
