"""Classify a task: SIMPLE / COMPLEX / STRATEGIC + select participating departments."""
from __future__ import annotations
from enum import Enum
from pathlib import Path
import json
import re
import yaml
from dataclasses import dataclass
from core.brain.schema import BrainContext


class TaskClass(str, Enum):
    SIMPLE = "SIMPLE"
    COMPLEX = "COMPLEX"
    STRATEGIC = "STRATEGIC"


@dataclass
class TaskClassification:
    class_: TaskClass
    departments: list[str]
    reasoning: str
    confidence: float = 0.8


ROUTER_PROMPT = """You are the router that classifies a task for the preconstruction / estimating department of a commercial general contractor.

## Classification
- SIMPLE: 1-2 departments, no meeting needed. E.g. draft a scope letter, an RFI log, a bid/no-bid scorecard.
- COMPLEX: 3-5 departments debate. E.g. a bid strategy for a large package, a self-perform vs subcontract decision, a value-engineering plan.
- STRATEGIC: all-department debate, with the Chief Estimator's sign-off mid-way. E.g. a > $20M bid, a new building type or market, a GMP negotiation, a change to the markup policy.

## Departments (canonical codes)
01-bid-coordination (intake, sheet register, spec analysis, RFIs, final report),
02-civil-structural (sitework, concrete, masonry, structural steel takeoff),
03-architectural (envelope, interiors, openings, specialties takeoff),
04-mep (mechanical, plumbing, fire protection, electrical, low voltage takeoff),
05-cost-engineering (pricing, general conditions, risk/markups, sub-bid leveling),
06-estimate-review (chief estimator review, scope-gap audit, constructability, benchmarks)

## REQUIRED JSON output
```json
{
  "class": "SIMPLE|COMPLEX|STRATEGIC",
  "departments": ["XX-name", ...],
  "reasoning": "..."
}
```

## Principles for selecting departments
- Infer from keywords in the brief
- Reference the Brain to know which departments are active
- Be strict: only choose departments that are genuinely needed
- Cross-department issues usually need both sides of the handoff (e.g. a pricing question
  needs 05-cost-engineering AND the discipline that took off the quantity; any bid decision
  needs 06-estimate-review as the standing skeptic)
"""


class Router:
    def __init__(self, llm, rules_path: Path | None = None):
        self.llm = llm
        if rules_path:
            self.rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
        else:
            self.rules = {}

    def classify(self, brief: str, brain: BrainContext) -> TaskClassification:
        active = brain.headcount.active_departments
        rules_text = yaml.safe_dump(self.rules, allow_unicode=True)

        messages = [
            {"role": "system", "content": ROUTER_PROMPT + f"\n\n## RULES\n```yaml\n{rules_text}\n```"},
            {"role": "user", "content": (
                f"## BRIEF\n{brief}\n\n"
                f"## ACTIVE DEPARTMENTS\n{active}\n\n"
                f"Classify and select the departments to convene. Return JSON in the exact format."
            )},
        ]
        raw = self.llm.complete(messages)
        data = self._parse_json(raw)
        return TaskClassification(
            class_=TaskClass(data["class"]),
            departments=data["departments"],
            reasoning=data.get("reasoning", ""),
            confidence=float(data.get("confidence", 0.8)),
        )

    async def aclassify(self, brief: str, brain: BrainContext) -> TaskClassification:
        """Async version of classify() — used in async MCP tools."""
        active = brain.headcount.active_departments
        rules_text = yaml.safe_dump(self.rules, allow_unicode=True)
        messages = [
            {"role": "system", "content": ROUTER_PROMPT + f"\n\n## RULES\n```yaml\n{rules_text}\n```"},
            {"role": "user", "content": (
                f"## BRIEF\n{brief}\n\n"
                f"## ACTIVE DEPARTMENTS\n{active}\n\n"
                f"Classify and select the departments to convene. Return JSON in the exact format."
            )},
        ]
        raw = await self.llm.acomplete(messages)
        data = self._parse_json(raw)
        return TaskClassification(
            class_=TaskClass(data["class"]),
            departments=data["departments"],
            reasoning=data.get("reasoning", ""),
            confidence=float(data.get("confidence", 0.8)),
        )

    @staticmethod
    def _parse_json(raw: str) -> dict:
        """Parse JSON from LLM output — robust to multi-block, code fence, prose.

        P2.2: Instead of a greedy `\\{.*\\}` regex (which matches from the first `{`
        to the last `}` and can merge multiple JSON objects), try strategies in order:
        1. Direct json.loads (if the LLM JSON-mode returns clean output)
        2. Strip a ```json ... ``` code fence
        3. Find the first balanced JSON object (balance braces)
        4. Fall back to the legacy greedy regex
        """
        text = raw.strip()

        # Strategy 1: direct
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Strategy 2: code fence
        fence_match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL
        )
        if fence_match:
            try:
                return json.loads(fence_match.group(1))
            except json.JSONDecodeError:
                pass

        # Strategy 3: balanced braces — find the first `{`, count depth to the matching `}`
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
                        candidate = text[start:i + 1]
                        try:
                            return json.loads(candidate)
                        except json.JSONDecodeError:
                            break

        # Strategy 4: legacy greedy fallback
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            return json.loads(m.group(0))

        raise ValueError(f"Router output no JSON: {raw[:200]}")
