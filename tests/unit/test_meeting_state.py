from core.meeting.debate_state import (
    new_meeting_state,
)


def test_new_state_has_defaults():
    state = new_meeting_state(
        brief="Test campaign",
        departments=["05-service-operations", "02-npi-program-management"],
        max_rounds=2,
    )
    assert state["brief"] == "Test campaign"
    assert state["departments"] == ["05-service-operations", "02-npi-program-management"]
    assert state["pro_con_debate"]["pro_history"] == []
    assert state["pro_con_debate"]["count"] == 0
    assert state["max_debate_rounds"] == 2


def test_perspective_debate_three_voices():
    state = new_meeting_state(brief="x", departments=[])
    pd = state["perspective_debate"]
    assert "growth_history" in pd
    assert "cautious_history" in pd
    assert "balanced_history" in pd
    assert pd["latest_speaker"] is None


def test_state_serializable():
    """Critical: state must serialize for SQLite checkpoint."""
    import json
    state = new_meeting_state(brief="x", departments=[])
    s = json.dumps(state, default=str)
    assert "brief" in s
