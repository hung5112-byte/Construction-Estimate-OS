"""TypedDict states for the LangGraph meeting orchestrator.

RULE 2: Domain-neutral — no trade/finance vocabulary.
Adapted from TradingAgents/agents/utils/agent_states.py with neutral renames.
"""
from __future__ import annotations
from typing import TypedDict, Optional


class ProConDebateState(TypedDict):
    """Pro/Con debate state — the advocating side vs. the challenging side."""
    pro_history: list[str]
    con_history: list[str]
    history: list[str]
    latest_speaker: Optional[str]
    count: int
    judge_decision: Optional[str]


class PerspectiveDebateState(TypedDict):
    """3 perspective debators: growth / cautious / balanced.

    growth   = prioritizes scale, accepts bigger risk for higher upside
    cautious = protects capital, stresses bad scenarios, demands concrete gates
    balanced = synthesizes both sides into a middle-path plan
    """
    growth_history: list[str]
    cautious_history: list[str]
    balanced_history: list[str]
    history: list[str]
    latest_speaker: Optional[str]
    count: int
    judge_decision: Optional[str]


class MeetingState(TypedDict):
    """Root state for the LangGraph meeting graph."""
    # Inputs
    brief: str
    departments: list[str]
    brain_context: dict
    research_findings: dict

    # Per-department perspectives (round 1)
    perspectives: dict[str, str]
    # Intra-department team inputs (round 1, when intra_department_round is on):
    # dept_code -> {team_agent_id -> short take}. The manager synthesizes these
    # into the department perspective above.
    team_inputs: dict[str, dict[str, str]]

    # Debates
    pro_con_debate: ProConDebateState
    perspective_debate: PerspectiveDebateState

    # Limits
    max_perspective_rounds: int
    max_debate_rounds: int
    max_perspective_debate_rounds: int

    # Output
    final_report: Optional[str]

    # Metadata
    task_id: str
    timestamp: str


def new_meeting_state(
    brief: str,
    departments: list[str],
    brain_context: dict | None = None,
    max_rounds: int = 2,
    task_id: str = "",
) -> MeetingState:
    from datetime import datetime
    return MeetingState(
        brief=brief,
        departments=departments,
        brain_context=brain_context or {},
        research_findings={},
        perspectives={},
        team_inputs={},
        pro_con_debate=ProConDebateState(
            pro_history=[], con_history=[], history=[],
            latest_speaker=None, count=0, judge_decision=None,
        ),
        perspective_debate=PerspectiveDebateState(
            growth_history=[], cautious_history=[], balanced_history=[],
            history=[], latest_speaker=None, count=0, judge_decision=None,
        ),
        max_perspective_rounds=1,
        max_debate_rounds=max_rounds,
        max_perspective_debate_rounds=1,
        final_report=None,
        task_id=task_id,
        timestamp=datetime.now().isoformat(),
    )
