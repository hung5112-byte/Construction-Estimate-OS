"""Con Advocate — the challenger that surfaces risks.

Adapted from references/tradingagents (RULE 2: neutral naming, no finance terms).
"""
from __future__ import annotations
from core.agents.base_agent import BaseAgent
from core.meeting.debate_state import MeetingState

CON_SYSTEM_PROMPT = """You are the Con Advocate (the challenger) in the company's executive meeting.

## Role
- Synthesize the department perspectives
- Point out RISKS, GAPS, bad scenarios
- Rebut the Pro Advocate's proposals
- Protect the company from reckless decisions

## Principles
- ALWAYS cite the Brain
- Specific numbers, not vague claims
- Rebut pro_history directly (read carefully what Pro said, then counter)
- Define any jargon you use
"""


class ConAdvocate:
    def __init__(self, llm):
        self.agent = BaseAgent(
            name_vn="Con Advocate",
            role="con_advocate",
            system_prompt=CON_SYSTEM_PROMPT,
            llm=llm,
            temperature=0.6,
        )

    def run(self, state: MeetingState) -> dict:
        debate = state["pro_con_debate"]
        history_text = []
        for p in debate["pro_history"]:
            history_text.append(f"[Pro argument]: {p}")
        for c in debate["con_history"]:
            history_text.append(f"[Previous Con round]: {c}")

        perspectives_text = "\n".join(
            f"- {dept}: {persp[:300]}..." for dept, persp in state["perspectives"].items()
        )
        extra = f"## DEPARTMENT PERSPECTIVES\n{perspectives_text}"

        response = self.agent.speak(
            brief=state["brief"],
            brain_context=state["brain_context"],
            history=history_text,
            extra_context=extra,
        )

        return {
            "pro_con_debate": {
                **debate,
                "con_history": debate["con_history"] + [response],
                "history": debate["history"] + [f"CON: {response}"],
                "latest_speaker": "con",
                "count": debate["count"] + 1,   # increment AFTER con (1 round = pro+con)
            }
        }
