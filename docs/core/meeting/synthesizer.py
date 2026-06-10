"""Synthesizer — synthesize the whole meeting → a decision report for the Department Head.

Adapted from TradingAgents/agents/managers/portfolio_manager.py with:
- Domain-neutral output (no portfolio/trade leakage)
- RULE 4 enforced: TL;DR + jargon definitions
- RULE 5 enforced: cite research findings
"""
from __future__ import annotations

from core.agents.base_agent import BaseAgent
from core.meeting.debate_state import MeetingState

SYNTHESIZER_PROMPT = """You synthesize the company meeting and write the decision report for the Department Head.

## REQUIRED output format:

```markdown
# Decision report: <task>

## 📌 Bottom line (30-second read)
- [3-5 plain-language lines; after reading, you know what to do]

## Recommendation
[GO / GO with revisions / NO-GO / NEED_MORE_INFO]

## Changes from the original brief (if any)
| Item | Original brief | Recommendation | Reason |
| ... |

## Detailed analysis

### What each department said
[Synthesis of perspectives]

### Pro vs Con debate
[Highlight key arguments]

### Three perspectives (Growth/Cautious/Balanced)
[Summary]

## To do before launch (BLOCKERS)
[Checklist]

## KPI gates
[Specific: in week X, if Y < Z then pause]

## Decisions the Department Head must make
[A/B/C/D]
```

## Principles (REQUIRED)
- 🔒 RULE 4: Define EVERY domain term the first time it appears
- 🔒 RULE 5: Cite every claim (Brain file:line, or research source URL)
- Plain English; after reading, the Department Head understands without needing to Google
- The bottom-line TL;DR must come first and be understandable in 30 seconds
"""


class Synthesizer:
    def __init__(self, llm):
        self.agent = BaseAgent(
            name_vn="Synthesizer",
            role="synthesizer",
            system_prompt=SYNTHESIZER_PROMPT,
            llm=llm,
            temperature=0.4,
        )

    def run(self, state: MeetingState) -> dict:
        perspectives_text = "\n\n".join(
            f"### {dept}\n{persp}" for dept, persp in state["perspectives"].items()
        )
        pc_text = "\n".join(state["pro_con_debate"]["history"])
        pd_text = "\n".join(state["perspective_debate"]["history"])
        research_text = ""
        if state.get("research_findings"):
            research_text = "## RESEARCH\n" + str(state["research_findings"])[:3000]

        extra = (
            f"## DEPARTMENT PERSPECTIVES\n{perspectives_text}\n\n"
            f"## PRO vs CON\n{pc_text}\n\n"
            f"## PERSPECTIVE DEBATE\n{pd_text}\n\n"
            f"{research_text}"
        )

        report = self.agent.speak(
            brief=state["brief"],
            brain_context=state["brain_context"],
            history=[],
            extra_context=extra,
        )
        return {"final_report": report}
