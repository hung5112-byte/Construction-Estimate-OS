"""The LLM decides which tools to run for a task."""
from __future__ import annotations
import json
import re
from typing import TypedDict


class ToolCall(TypedDict):
    tool: str
    queries: list[str]


ROUTER_PROMPT_TEMPLATE = """You are the Tool Router. Decide which tools to run for this business task.

## Available tools (already filtered — only tools that have credentials)
{tools_list}

## REQUIRED JSON output
```json
{{
  "tools": [
    {{"tool": "<name>", "queries": ["<q1>", ...]}}
  ]
}}
```

## Principles
- Brief involves a legal claim / advertising → us_law_search (if available)
- Brief involves a specific Texas jurisdiction → us_local_regulation (if available, include the jurisdiction in the query)
- Brief references a competitor or needs positioning → competitor_research (if available)
- Brief involves a metric / KPI → industry_benchmark
- Brief involves money / taxes → tax_calculator
- Do NOT run any tool if the Brain already has enough information
- At most 4 tools per task
- ONLY choose tools FROM THE AVAILABLE LIST above
"""


_FULL_TOOL_DESCRIPTIONS = {
    "web_search": "general web search (needs TAVILY_API_KEY)",
    "us_law_search": "US federal + Texas statutes/regulations (needs TAVILY_API_KEY)",
    "us_local_regulation": "Texas state agency rules (needs TAVILY_API_KEY)",
    "competitor_research": "industry competitor research (needs TAVILY_API_KEY)",
    "industry_benchmark": "industry KPIs (hardware_electronics, saas_b2b, ecommerce_d2c, restaurant_casual, retail_offline)",
    "tax_calculator": "estimate US federal + Texas taxes (needs specific figures)",
}


class ToolRouter:
    def __init__(self, llm, available_tools: list[str] | None = None):
        """
        Args:
            llm: LLM provider
            available_tools: Tool names allowed for planning. If None → all 6 (legacy).
                            The caller (ResearchPhase) injects a filtered list based on
                            BaseTool.is_available() so the Router does not plan a tool that will skip.
        """
        self.llm = llm
        self.available_tools = available_tools

    def _build_prompt(self) -> str:
        names = self.available_tools or list(_FULL_TOOL_DESCRIPTIONS.keys())
        lines = []
        for n in names:
            desc = _FULL_TOOL_DESCRIPTIONS.get(n, "(no description)")
            lines.append(f"- {n}: {desc}")
        return ROUTER_PROMPT_TEMPLATE.format(tools_list="\n".join(lines))

    def plan(self, brief: str, brain_summary: str) -> list[ToolCall]:
        if self.available_tools is not None and not self.available_tools:
            # No credentialed tools — skip planning entirely.
            return []

        messages = [
            {"role": "system", "content": self._build_prompt()},
            {"role": "user", "content": (
                f"## BRIEF\n{brief}\n\n"
                f"## BRAIN SUMMARY\n{brain_summary[:2000]}\n\n"
                "Output JSON tool plan."
            )},
        ]
        raw = self.llm.complete(messages)
        # P2.2: robust JSON parse — handle code fence + balanced braces + greedy fallback
        data = self._extract_json(raw)
        if data is None:
            return []
        plan = data.get("tools", [])
        # Defensive filter: drop tools not in the available list
        if self.available_tools is not None:
            plan = [t for t in plan if t.get("tool") in self.available_tools]
        return plan

    @staticmethod
    def _extract_json(raw: str) -> dict | None:
        """Extract JSON from LLM output — same strategies as Router._parse_json."""
        text = raw.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fence:
            try:
                return json.loads(fence.group(1))
            except json.JSONDecodeError:
                pass

        start = text.find("{")
        if start >= 0:
            depth = 0
            for i in range(start, len(text)):
                ch = text[i]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(text[start:i + 1])
                        except json.JSONDecodeError:
                            break

        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
        return None
