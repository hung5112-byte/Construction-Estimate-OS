from unittest.mock import MagicMock
from core.agents.pro_advocate import ProAdvocate
from core.agents.con_advocate import ConAdvocate
from core.meeting.debate_state import new_meeting_state


def test_pro_advocate_pushes_for_action():
    mock_llm = MagicMock(complete=MagicMock(return_value="Recommend proceeding."))
    pro = ProAdvocate(llm=mock_llm)
    state = new_meeting_state(brief="Launch X", departments=[])
    state["perspectives"] = {"05-service-operations": "OK", "02-npi-program-management": "Risky"}

    output = pro.run(state)
    assert "proceeding" in output["pro_con_debate"]["pro_history"][-1]
    assert output["pro_con_debate"]["latest_speaker"] == "pro"


def test_con_advocate_raises_concerns():
    mock_llm = MagicMock(complete=MagicMock(return_value="Warning: risk."))
    con = ConAdvocate(llm=mock_llm)
    state = new_meeting_state(brief="Launch X", departments=[])
    state["pro_con_debate"]["pro_history"] = ["Pro said: GO"]

    output = con.run(state)
    assert "risk" in output["pro_con_debate"]["con_history"][-1].lower()
    assert output["pro_con_debate"]["count"] == 1   # round counter incremented after Con
