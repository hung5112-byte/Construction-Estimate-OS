"""Search US federal statutes/regulations + Texas state law — restrict to trusted
government sources. General legal information only, not legal advice."""
from __future__ import annotations
import os
from pathlib import Path
from core.tools.base_tool import BaseTool, ToolResult
from core.tools.tool_cache import ToolCache


TRUSTED_DOMAINS = [
    "irs.gov",                       # federal tax
    "uscode.house.gov",              # United States Code
    "ecfr.gov",                      # federal regulations
    "statutes.capitol.texas.gov",    # Texas statutes
    "comptroller.texas.gov",         # Texas taxes (franchise, sales/use)
    "sos.state.tx.us",               # Texas Secretary of State
    "sba.gov",                       # Small Business Administration
    "dol.gov",                       # US Department of Labor
    "usa.gov",                       # federal portal
]


class USLawSearch(BaseTool):
    name = "us_law_search"
    description = "Search US federal + Texas statutes, codes, and regulations."

    def __init__(self, api_key: str | None = None, cache_path: Path | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY", "")
        self.cache = ToolCache(
            cache_path or Path.home() / ".vn-business-os" / "tool_cache.db",
        )

    def is_available(self) -> bool:
        return bool(self.api_key)

    def run(self, query: str, **kwargs) -> ToolResult:
        if not self.is_available():
            return self.skipped_result(
                "Missing TAVILY_API_KEY — cannot look up statutes/regulations online"
            )

        cache_hit = self.cache.get(query, source=self.name)
        if cache_hit:
            return ToolResult(data=cache_hit, sources=cache_hit.get("urls", []),
                              cached=True, notes="cache hit")

        try:
            from tavily import TavilyClient
        except ImportError:
            return self.skipped_result("Package 'tavily-python' is not installed")

        client = TavilyClient(api_key=self.api_key)
        resp = client.search(
            query=query, max_results=8,
            include_answer=True,
            include_domains=TRUSTED_DOMAINS,
        )
        urls = [r["url"] for r in resp.get("results", [])]
        data = {
            "answer": resp.get("answer", ""),
            "results": resp.get("results", []),
            "urls": urls,
        }
        self.cache.set(query, data, source=self.name)
        return ToolResult(data=data, sources=urls)
