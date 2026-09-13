"""3 perspective debators: Growth / Cautious / Balanced.

Adapted from references/tradingagents/tradingagents/agents/risk_mgmt/
{aggressive,conservative,neutral}_debator.py with domain-neutral renaming:
  aggressive   -> Growth
  conservative -> Cautious
  neutral      -> Balanced (synthesizer)
"""
from __future__ import annotations

from core.agents.base_agent import BaseAgent
from core.meeting.debate_state import MeetingState


GROWTH_PROMPT = """You are the GROWTH side in the company meeting.
Task: Defend the boldest option, prioritize scaling, accept higher risk for higher upside.
Stick to the Brain numbers. Define any jargon."""

CAUTIOUS_PROMPT = """You are the CAUTIOUS side in the company meeting.
Task: Protect capital, surface bad scenarios, set concrete gates (pause/kill conditions).
Stick to the Brain numbers. Define any jargon."""

BALANCED_PROMPT = """You are the BALANCED side in the company meeting.
Task: Combine the Growth and Cautious views into a feasible middle-ground option.
Stick to the Brain numbers. Define any jargon."""


def _build_extra(state: MeetingState) -> str:
    """Compose context: the Pro/Con transcript + the history of the 3 perspective sides."""
    pc = state["pro_con_debate"]
    pd = state["perspective_debate"]
    parts = ["## TRANSCRIPT PRO/CON\n" + "\n".join(pc["history"])]
    if pd["growth_history"]:
        parts.append("## WHAT GROWTH SAID\n" + "\n".join(pd["growth_history"]))
    if pd["cautious_history"]:
        parts.append("## WHAT CAUTIOUS SAID\n" + "\n".join(pd["cautious_history"]))
    if pd["balanced_history"]:
        parts.append("## WHAT BALANCED SAID\n" + "\n".join(pd["balanced_history"]))
    return "\n\n".join(parts)


class GrowthDebator:
    def __init__(self, llm):
        self.agent = BaseAgent(
            name_local="Growth",
            role="growth",
            system_prompt=GROWTH_PROMPT,
            llm=llm,
        )

    def run(self, state: MeetingState) -> dict:
        resp = self.agent.speak(
            brief=state["brief"],
            brain_context=state["brain_context"],
            history=[],
            extra_context=_build_extra(state),
        )
        pd = state["perspective_debate"]
        return {
            "perspective_debate": {
                **pd,
                "growth_history": pd["growth_history"] + [resp],
                "history": pd["history"] + [f"GROWTH: {resp}"],
                "latest_speaker": "growth",
            }
        }


class CautiousDebator:
    def __init__(self, llm):
        self.agent = BaseAgent(
            name_local="Cautious",
            role="cautious",
            system_prompt=CAUTIOUS_PROMPT,
            llm=llm,
        )

    def run(self, state: MeetingState) -> dict:
        resp = self.agent.speak(
            brief=state["brief"],
            brain_context=state["brain_context"],
            history=[],
            extra_context=_build_extra(state),
        )
        pd = state["perspective_debate"]
        return {
            "perspective_debate": {
                **pd,
                "cautious_history": pd["cautious_history"] + [resp],
                "history": pd["history"] + [f"CAUTIOUS: {resp}"],
                "latest_speaker": "cautious",
            }
        }


class BalancedDebator:
    def __init__(self, llm):
        self.agent = BaseAgent(
            name_local="Balanced",
            role="balanced",
            system_prompt=BALANCED_PROMPT,
            llm=llm,
        )

    def run(self, state: MeetingState) -> dict:
        resp = self.agent.speak(
            brief=state["brief"],
            brain_context=state["brain_context"],
            history=[],
            extra_context=_build_extra(state),
        )
        pd = state["perspective_debate"]
        return {
            "perspective_debate": {
                **pd,
                "balanced_history": pd["balanced_history"] + [resp],
                "history": pd["history"] + [f"BALANCED: {resp}"],
                "latest_speaker": "balanced",
                # 1 round = growth + cautious + balanced (Balanced ends the round)
                "count": pd["count"] + 1,
            }
        }
