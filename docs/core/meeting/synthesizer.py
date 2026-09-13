"""Synthesizer — synthesize the whole meeting → a decision report for the Department Head.

Adapted from TradingAgents/agents/managers/portfolio_manager.py with:
- Domain-neutral output (no portfolio/trade leakage)
- RULE 4 enforced: TL;DR + jargon definitions
- RULE 5 enforced: cite research findings
- Critic contract enforced: the MACHINE-CHECKED OUTPUT CONTRACT below states the
  exact grammar the deterministic critic scanner accepts (live-replay lesson
  2026-07-05: soft "principles" bullets were partially ignored; the contract is
  now a named, verbatim-grammar section and the request line demands it).
"""
from __future__ import annotations

from core.agents.base_agent import BaseAgent
from core.critic.constants import ACCEPTED_GRAMMAR
from core.meeting.debate_state import MeetingState

SYNTHESIZER_PROMPT = """You synthesize the company meeting and write the decision report for the Department Head.

## REQUIRED output format:

```markdown
# Decision report: <task>

## 📌 Bottom line (30-second read)
- [3-5 plain-language lines; after reading, you know what to do]

## Recommendation
[EXACTLY ONE of: GO | GO-WITH-CONDITIONS | PROCEED-WITH-REVISIONS | NEED-MORE-INFO | NO-GO — on its own line, nothing else]

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

## Blockers (before Stop 2)
[ALWAYS present — write "None." if empty. Every blocker line: **task** (ref: Q<n> when it stems from a clarification answer). *Owner: <dept/person>. Deadline: <date/week>.*]

## KPI gates
[Specific: in week X, if Y < Z then pause]

## Decisions the Department Head must make
[A/B/C/D]
```

## MACHINE-CHECKED OUTPUT CONTRACT — a deterministic scanner rejects your draft if violated
Your draft is scored by a critic BEFORE any human sees it. Three of its checks
are deterministic scanners with zero tolerance. This is the EXACT grammar they
accept — nothing else counts, no synonyms, no alternative formats:

""" + ACCEPTED_GRAMMAR + """

Every rejected draft costs a full revision round (there are only 3).

## Principles (REQUIRED)
- 🔒 RULE 4: Define EVERY domain term the first time it appears
- 🔒 RULE 5: Cite every claim (Brain file, clarification ref, or research source URL)
- 🔒 The verdict is EXACTLY one canonical tier — "cautiously optimistic, monitor
  closely" is not a verdict. Hedged verdicts are forbidden.
- 🔒 Any clarification answer of "unknown / not previously considered / needs
  confirmation" on a regulatory, compliance, or certification question MUST
  appear as a first-class blocker with `(ref: Q<n>)`, an owner, and a deadline.
- 🔒 A claim with no source is either deleted or written as
  `ASSUMPTION: <claim> (uncitable: <reason>)` — never left uncited (max 5 per report).
- Plain English; after reading, the Department Head understands without needing to Google
- The bottom-line TL;DR must come first and be understandable in 30 seconds
"""

# The Synthesizer's own request line. BaseAgent's default REQUEST says "State
# your perspective (in plain English, citing the Brain)" — written for debate
# agents; for the Synthesizer it nudged live runs AWAY from the ALL-CAPS
# machine tokens. The Synthesizer writes a document, not a perspective.
SYNTHESIZER_REQUEST = (
    "Write the FULL decision report now, in the REQUIRED output format. "
    "Follow the MACHINE-CHECKED OUTPUT CONTRACT exactly — the verdict token, "
    "citation markers, ASSUMPTION lines, and blocker rows are machine-scanned "
    "verbatim and the draft is rejected on any violation."
)

REVISION_REQUEST_SUFFIX = """
## REQUEST
Apply the revision instruction above to your prior draft. FIX ONLY — resolve the
listed issues and nothing else; no new options, sections, recommendations, or
scope. Keep every section heading of the required format unchanged (especially
`## Recommendation`). Produce the FULL revised decision report as a new draft
(do not describe your edits)."""


class Synthesizer:
    def __init__(self, llm):
        self.agent = BaseAgent(
            name_local="Synthesizer",
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
        # ADR-004 §5: episodic memory reaches the judge ONLY, and only when
        # non-empty — an absent block beats a placeholder the model could
        # fabricate around.
        memory_block = state.get("memory_context") or ""
        if memory_block:
            extra += f"\n\n{memory_block}"

        report = self.agent.speak(
            brief=state["brief"],
            brain_context=state["brain_context"],
            history=[],
            extra_context=extra,
            request=SYNTHESIZER_REQUEST,
        )
        return {"final_report": report}

    def revise(
        self, prior_draft: str, revision_instruction: str, memory_block: str = ""
    ) -> str:
        """Critic-loop revision turn (Synthesizer-only, 2026-07-05 ruling Q3).

        The revision instruction re-enters the drafter's context verbatim —
        exactly like a human `revise(feedback)` at a tri-state gate; the critic
        is a machine user of the same contract (critic-draft §5, C1 semantics).

        memory_block: the same PAST DECISIONS block from the drafting turn —
        without it a revision round cannot see what [M<i>]-derived claims rest
        on, and ADR-004's fabrication mode reopens through the repair path.
        """
        memory_part = f"\n\n{memory_block}" if memory_block else ""
        messages = [
            {"role": "system", "content": self.agent.system_prompt},
            {"role": "user", "content": (
                f"## YOUR PRIOR DRAFT\n{prior_draft}\n\n"
                f"## REVISION INSTRUCTION FROM THE CRITIC\n{revision_instruction}"
                f"{memory_part}\n"
                f"{REVISION_REQUEST_SUFFIX}"
            )},
        ]
        return self.agent.llm.complete(messages, model=self.agent.model_override)
