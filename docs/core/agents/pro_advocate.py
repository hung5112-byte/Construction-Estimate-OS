"""Pro Advocate — the side that pushes to act and proposes actions.

Adapted from references/tradingagents (RULE 2: neutral naming, no finance terms).
"""
from __future__ import annotations
from core.agents.base_agent import BaseAgent
from core.meeting.debate_state import MeetingState

PRO_SYSTEM_PROMPT = """You are the Pro Advocate (the side that pushes to act) in the company's executive meeting.

## Role
- Synthesize the department perspectives
- Propose concrete ACTIONS to execute
- Point out opportunities, advantages, the path to winning
- DEBATE against the Con Advocate (the challenger)

## Principles
- ALWAYS cite the Brain (strategy.md, products.md, budget.md, ...)
- Do NOT be vague — back every claim with specific numbers
- Rebut the Con Advocate's arguments in later rounds (read con_history)
- Define any jargon you use (CAC, ROAS, ...)
"""


class ProAdvocate:
    def __init__(self, llm):
        self.agent = BaseAgent(
            name_local="Pro Advocate",
            role="pro_advocate",
            system_prompt=PRO_SYSTEM_PROMPT,
            llm=llm,
            temperature=0.6,
        )

    def run(self, state: MeetingState) -> dict:
        debate = state["pro_con_debate"]
        history_text = []
        for p in debate["pro_history"]:
            history_text.append(f"[Previous Pro round]: {p}")
        for c in debate["con_history"]:
            history_text.append(f"[Con rebuttal]: {c}")

        perspectives_text = "\n".join(
            f"- {dept}: {persp[:300]}..." for dept, persp in state["perspectives"].items()
        )
        extra = f"## DEPARTMENT PERSPECTIVES (round 1)\n{perspectives_text}"

        response = self.agent.speak(
            brief=state["brief"],
            brain_context=state["brain_context"],
            history=history_text,
            extra_context=extra,
        )

        return {
            "pro_con_debate": {
                **debate,
                "pro_history": debate["pro_history"] + [response],
                "history": debate["history"] + [f"PRO: {response}"],
                "latest_speaker": "pro",
            }
        }
