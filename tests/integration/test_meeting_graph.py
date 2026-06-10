"""Integration test: full graph end-to-end with mocked LLM."""
from unittest.mock import MagicMock
from core.meeting.meeting_graph import MeetingGraph
from core.meeting.debate_state import new_meeting_state


def test_meeting_runs_end_to_end_mocked():
    """Run full graph with mocked LLM (no API call, no checkpointer)."""

    def fake_complete(messages, model=None):
        sys = messages[0]["content"]
        if "Pro Advocate" in sys:
            return "GO. Clear opportunity."
        if "Con Advocate" in sys:
            return "Warning: risk X."
        if "GROWTH side" in sys:
            return "Execute boldly."
        if "CAUTIOUS side" in sys:
            return "Clear gates."
        if "BALANCED side" in sys:
            return "4-week pilot."
        if "decision report" in sys.lower() or "Synthesizer" in sys:
            return "## 📌 Bottom line\nGO with revisions.\n\n## Details\n..."
        return "..."

    mock_llm = MagicMock()
    mock_llm.complete.side_effect = fake_complete

    def mock_perspectives(state):
        return {"perspectives": {
            "05-service-operations": "Recommend proceeding",
            "02-npi-program-management": "Careful with the budget",
        }}

    # Pass checkpointer=False to disable persistence (faster + no temp files)
    graph = MeetingGraph(
        llm=mock_llm,
        perspectives_collector=mock_perspectives,
        checkpointer=False,
    )

    state = new_meeting_state(
        brief="Test campaign",
        departments=["05-service-operations", "02-npi-program-management"],
        max_rounds=1,
        task_id="test-001",
    )

    # When no checkpointer, no thread_id needed
    result = graph.build().invoke(state)

    assert result["perspectives"]["05-service-operations"] == "Recommend proceeding"
    assert len(result["pro_con_debate"]["pro_history"]) >= 1
    assert len(result["pro_con_debate"]["con_history"]) >= 1
    assert len(result["perspective_debate"]["growth_history"]) >= 1
    assert result["final_report"] is not None
    assert "Bottom line" in result["final_report"]
