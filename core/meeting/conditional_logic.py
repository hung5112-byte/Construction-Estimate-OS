"""LangGraph routing logic - quyet dinh node ke tiep dua state.

Adapted from TradingAgents/graph/conditional_logic.py voi neutral naming.
"""
from __future__ import annotations
from core.meeting.debate_state import MeetingState


def next_pro_con_node(state: MeetingState) -> str:
    """Sau Pro hoac Con node, decide node ke tiep.

    Returns:
        "pro"               - pro speaker turn
        "con"               - con speaker turn
        "perspective_phase" - debate done, advance to perspective phase
    """
    debate = state["pro_con_debate"]
    max_rounds = state["max_debate_rounds"]

    if debate["count"] >= max_rounds:
        return "perspective_phase"

    speaker = debate["latest_speaker"]
    if speaker is None or speaker == "con":
        return "pro"
    return "con"


def next_perspective_node(state: MeetingState) -> str:
    """Cycle growth -> cautious -> balanced. Sau N round -> synthesizer."""
    pd = state["perspective_debate"]
    max_rounds = state["max_perspective_debate_rounds"]

    if pd["count"] >= max_rounds:
        return "synthesizer"

    speaker = pd["latest_speaker"]
    if speaker is None:
        return "growth"
    if speaker == "growth":
        return "cautious"
    if speaker == "cautious":
        return "balanced"
    # speaker == "balanced" -> next round starts with growth
    return "growth"
