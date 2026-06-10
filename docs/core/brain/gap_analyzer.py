"""Compare the brief with the Brain → list gaps the Department Head must clarify.

🔒 RULE 1 enforced: every gap MUST cite a Brain file/section.
"""
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
import json
import re
from core.brain.schema import BrainContext


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    WARN = "WARN"
    INFO = "INFO"


@dataclass
class Gap:
    field: str
    severity: Severity
    current_value: str
    brief_value: str
    reason: str
    citation: str   # 00-Brain/<file>.md[:section]


GAP_PROMPT = """You are the Gap Analyzer. Compare the brief with the Brain context and find contradictions / missing information.

## REQUIRED JSON output: array of gaps
```json
[
  {
    "field": "ICP|budget|product_fit|headcount|...",
    "severity": "CRITICAL|WARN|INFO",
    "current_value": "...",
    "brief_value": "...",
    "reason": "...",
    "citation": "00-Brain/<file>.md or 00-Brain/<file>.md:<section>"
  }
]
```

## Principles
- 🔒 RULE 1: Every gap MUST cite the Brain
- CRITICAL: brief contradicts strategy/budget/laws
- WARN: brief may be OK but needs Department Head confirmation
- INFO: nice-to-know, do NOT ask the Department Head
- If the brief fully matches the Brain → return []
- Return a JSON array, with NO markdown
"""


class GapAnalyzer:
    def __init__(self, llm):
        self.llm = llm

    def analyze(self, brief: str, brain: BrainContext) -> list[Gap]:
        brain_dump = brain.model_dump_json(indent=2)
        messages = [
            {"role": "system", "content": GAP_PROMPT},
            {"role": "user", "content": (
                f"## BRIEF\n{brief}\n\n"
                f"## BRAIN\n```json\n{brain_dump}\n```\n\n"
                "Find gaps. Return a JSON array."
            )},
        ]
        raw = self.llm.complete(messages)
        data = self._parse_json_array(raw)
        return [Gap(
            field=d["field"],
            severity=Severity(d["severity"]),
            current_value=d.get("current_value", ""),
            brief_value=d.get("brief_value", ""),
            reason=d.get("reason", ""),
            citation=d["citation"],
        ) for d in data]

    async def aanalyze(self, brief: str, brain: BrainContext) -> list[Gap]:
        """Async version of analyze() — used in async MCP tools."""
        brain_dump = brain.model_dump_json(indent=2)
        messages = [
            {"role": "system", "content": GAP_PROMPT},
            {"role": "user", "content": (
                f"## BRIEF\n{brief}\n\n"
                f"## BRAIN\n```json\n{brain_dump}\n```\n\n"
                "Find gaps. Return a JSON array."
            )},
        ]
        raw = await self.llm.acomplete(messages)
        data = self._parse_json_array(raw)
        return [Gap(
            field=d["field"],
            severity=Severity(d["severity"]),
            current_value=d.get("current_value", ""),
            brief_value=d.get("brief_value", ""),
            reason=d.get("reason", ""),
            citation=d["citation"],
        ) for d in data]

    @staticmethod
    def _parse_json_array(raw: str) -> list[dict]:
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        if not m:
            return []
        return json.loads(m.group(0))
