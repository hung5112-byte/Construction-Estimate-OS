"""Generate clarification questions from gaps.

🔒 RULE 1: do NOT generate questions if gaps is empty.
🔒 RULE 4: plain English, define jargon.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import json
import re
from core.brain.gap_analyzer import Gap, Severity


@dataclass
class Question:
    text: str
    citation: str
    severity: Severity
    choices: list[str] = field(default_factory=list)
    free_text: bool = False


QG_PROMPT = """You generate clarification questions for the Department Head.

## HARD principles (violation = reject output)
- 🔒 Every question MUST cite the Brain (file:section)
- 🔒 Plain English, no jargon unless defined inline
- 🔒 Provide 2-4 choices (usually), or free_text if open-ended
- 🔒 Questions are short, understandable in 30 seconds

## Output JSON: array of questions
```json
[
  {
    "text": "...",
    "citation": "00-Brain/<file>.md[:section]",
    "choices": ["A", "B", "C"],
    "severity": "CRITICAL|WARN",
    "free_text": false
  }
]
```

CRITICAL gap → the question MUST be asked.
WARN gap → the question SHOULD be asked (Department Head may skip).
INFO gap → do NOT ask.
"""


class QuestionGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate(self, gaps: list[Gap], brain: dict, brief: str) -> list[Question]:
        # 🔒 RULE 1: no gaps → no questions
        if not gaps:
            return []

        actionable = [g for g in gaps if g.severity in (Severity.CRITICAL, Severity.WARN)]
        if not actionable:
            return []

        gaps_text = "\n".join(
            f"- [{g.severity.value}] {g.field}: brief='{g.brief_value}' vs brain='{g.current_value}' "
            f"(cite: {g.citation}) — {g.reason}"
            for g in actionable
        )

        messages = [
            {"role": "system", "content": QG_PROMPT},
            {"role": "user", "content": f"## BRIEF\n{brief}\n\n## GAPS\n{gaps_text}\n\nGenerate the questions."},
        ]
        raw = self.llm.complete(messages)

        m = re.search(r"\[.*\]", raw, re.DOTALL)
        if not m:
            return []
        data = json.loads(m.group(0))

        return [Question(
            text=d["text"],
            citation=d["citation"],
            severity=Severity(d["severity"]),
            choices=d.get("choices", []),
            free_text=d.get("free_text", False),
        ) for d in data]

    async def agenerate(self, gaps: list[Gap], brain: dict, brief: str) -> list[Question]:
        """Async version of generate() — used in async MCP tools."""
        if not gaps:
            return []
        actionable = [g for g in gaps if g.severity in (Severity.CRITICAL, Severity.WARN)]
        if not actionable:
            return []
        gaps_text = "\n".join(
            f"- [{g.severity.value}] {g.field}: brief='{g.brief_value}' vs brain='{g.current_value}' "
            f"(cite: {g.citation}) — {g.reason}"
            for g in actionable
        )
        messages = [
            {"role": "system", "content": QG_PROMPT},
            {"role": "user", "content": f"## BRIEF\n{brief}\n\n## GAPS\n{gaps_text}\n\nGenerate the questions."},
        ]
        raw = await self.llm.acomplete(messages)
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        if not m:
            return []
        data = json.loads(m.group(0))
        return [Question(
            text=d["text"],
            citation=d["citation"],
            severity=Severity(d["severity"]),
            choices=d.get("choices", []),
            free_text=d.get("free_text", False),
        ) for d in data]
