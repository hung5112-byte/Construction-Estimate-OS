"""Curated US industry benchmarks."""
from __future__ import annotations
from pathlib import Path
import yaml
from core.tools.base_tool import BaseTool, ToolResult


DATA_PATH = Path(__file__).parent / "data" / "benchmarks-us.yaml"


class IndustryBenchmark(BaseTool):
    name = "industry_benchmark"
    description = "Look up curated US industry KPI benchmarks."

    def __init__(self, data_path: Path | None = None):
        self.data = yaml.safe_load(
            (data_path or DATA_PATH).read_text(encoding="utf-8")
        )

    def run(self, query: str, **kwargs) -> ToolResult:
        """query format: '<industry> <metric>' (e.g. 'hardware_electronics field_return_rate')"""
        parts = query.lower().split()
        if len(parts) < 2:
            return ToolResult(data={"not_found": True}, notes="invalid query format")

        industry = parts[0]
        metric_query = "_".join(parts[1:])

        ind_data = self.data.get(industry, {})
        for key, val in ind_data.items():
            if metric_query in key.lower() or key.lower() in metric_query:
                return ToolResult(
                    data=val,
                    sources=[f"benchmarks-us.yaml::{industry}::{key}"],
                    notes="Curated benchmark",
                )
        return ToolResult(data={"not_found": True})
