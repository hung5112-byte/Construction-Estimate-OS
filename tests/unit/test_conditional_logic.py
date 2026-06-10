"""Unit tests for LangGraph conditional routing logic."""
from core.meeting.conditional_logic import (
    next_pro_con_node,
    next_perspective_node,
)
from core.meeting.debate_state import new_meeting_state


def test_pro_con_alternates():
    state = new_meeting_state(brief="x", departments=[], max_rounds=2)

    state["pro_con_debate"]["latest_speaker"] = None
    assert next_pro_con_node(state) == "pro"

    state["pro_con_debate"]["latest_speaker"] = "pro"
    assert next_pro_con_node(state) == "con"

    state["pro_con_debate"]["latest_speaker"] = "con"
    state["pro_con_debate"]["count"] = 1
    assert next_pro_con_node(state) == "pro"  # next round

    state["pro_con_debate"]["count"] = 2
    state["pro_con_debate"]["latest_speaker"] = "con"
    assert next_pro_con_node(state) == "perspective_phase"  # done


def test_perspective_cycles_growth_cautious_balanced():
    state = new_meeting_state(brief="x", departments=[])

    state["perspective_debate"]["latest_speaker"] = None
    assert next_perspective_node(state) == "growth"

    state["perspective_debate"]["latest_speaker"] = "growth"
    assert next_perspective_node(state) == "cautious"

    state["perspective_debate"]["latest_speaker"] = "cautious"
    assert next_perspective_node(state) == "balanced"

    state["perspective_debate"]["latest_speaker"] = "balanced"
    state["perspective_debate"]["count"] = 1
    state["max_perspective_debate_rounds"] = 1
    assert next_perspective_node(state) == "synthesizer"  # done
