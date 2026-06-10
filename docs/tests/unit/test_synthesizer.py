"""Test Synthesizer — synthesize the meeting → final decision report for the CEO."""
from unittest.mock import MagicMock

from core.meeting.synthesizer import Synthesizer
from core.meeting.debate_state import new_meeting_state


def test_synthesizer_writes_final_report():
    llm = MagicMock(complete=MagicMock(return_value=(
        "## 📌 Bottom line\nGO with revised scope.\n\n## Details\n..."
    )))
    syn = Synthesizer(llm=llm)
    state = new_meeting_state(brief="Launch", departments=["05-service-operations"])
    state["perspectives"] = {"05-service-operations": "OK"}
    state["pro_con_debate"]["history"] = ["PRO: GO", "CON: Risk"]
    state["perspective_debate"]["history"] = [
        "GROWTH: bold",
        "CAUTIOUS: hold",
        "BALANCED: pilot",
    ]

    out = syn.run(state)
    assert out["final_report"] is not None
    assert "Bottom line" in out["final_report"]
