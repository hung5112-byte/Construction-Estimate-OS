"""Tests for the V2 intra-department round — teams speak, the manager synthesizes."""
from __future__ import annotations

from unittest.mock import MagicMock

from core.meeting.debate_state import new_meeting_state
from core.orchestrator.perspectives_collector import PerspectivesCollector


def _write_dept(tmp_path, code="01-hardware-engineering", manager="mgr", teams=("alpha", "beta")):
    dept = tmp_path / code
    agents_dir = dept / "agents"
    agents_dir.mkdir(parents=True)
    agent_list = ", ".join([manager, *teams])
    (dept / "department.yaml").write_text(
        f"code: {code}\nname_local: Test Dept\ntier: 1\n"
        f"description: Test\nagents: [{agent_list}]\ndefault_speaker: {manager}\n",
        encoding="utf-8",
    )
    (agents_dir / f"{manager}.md").write_text(
        f"---\nid: {manager}\nname_local: Manager\ndepartment: {code}\n---\n"
        "You are the department manager.",
        encoding="utf-8",
    )
    for t in teams:
        (agents_dir / f"{t}.md").write_text(
            f"---\nid: {t}\nname_local: Team {t}\ndepartment: {code}\n---\n"
            f"You are team {t}.",
            encoding="utf-8",
        )
    return code


def _dispatch_llm(mapping, default="manager synthesis"):
    """Content-keyed mock: team takes run CONCURRENTLY (v2.1), so positional
    side_effect lists are racy — dispatch on the agent's own system prompt.
    The assertions below are unchanged: same takes, same synthesis, same
    error isolation — only the mock's keying moved from call order to agent
    identity."""
    def respond(messages, model=None):
        system = messages[0]["content"]
        for needle, response in mapping.items():
            if needle in system:
                if isinstance(response, Exception):
                    raise response
                return response
        return default

    llm = MagicMock()
    llm.complete = MagicMock(side_effect=respond)
    return llm


def test_intra_runs_teams_then_manager(tmp_path):
    code = _write_dept(tmp_path)
    llm = _dispatch_llm({"You are team alpha": "alpha take",
                         "You are team beta": "beta take"})

    collector = PerspectivesCollector(departments_root=tmp_path, llm=llm, intra_department=True)
    state = new_meeting_state(brief="test brief", departments=[code])
    out = collector.collect(state)

    # 2 team calls + 1 manager call
    assert llm.complete.call_count == 3
    # Department perspective is the manager synthesis
    assert out["perspectives"][code] == "manager synthesis"
    # Team takes recorded for traceability
    assert out["team_inputs"][code] == {"alpha": "alpha take", "beta": "beta take"}

    # Last call is the manager: synthesis stance + team inputs in the system message
    # (the manager call always comes AFTER both takes — concurrency covers only
    # the takes themselves).
    last_system = llm.complete.call_args_list[-1][0][0][0]["content"]
    assert "synthesize your department" in last_system
    assert "[[alpha]]" in last_system and "alpha take" in last_system
    # Team-take order is preserved in the manager's input regardless of
    # completion order (v2.1 invariant).
    assert last_system.index("[[alpha]]") < last_system.index("[[beta]]")
    # Team calls used the short-take stance
    first_system = llm.complete.call_args_list[0][0][0][0]["content"]
    assert "team input" in first_system


def test_intra_falls_back_when_no_teams(tmp_path):
    code = _write_dept(tmp_path, teams=())
    llm = MagicMock()
    llm.complete = MagicMock(return_value="solo perspective")

    collector = PerspectivesCollector(departments_root=tmp_path, llm=llm, intra_department=True)
    state = new_meeting_state(brief="test", departments=[code])
    out = collector.collect(state)

    assert llm.complete.call_count == 1
    assert out["perspectives"][code] == "solo perspective"
    assert out["team_inputs"] == {}


def test_intra_off_keeps_single_speaker(tmp_path):
    code = _write_dept(tmp_path)
    llm = MagicMock()
    llm.complete = MagicMock(return_value="single perspective")

    collector = PerspectivesCollector(departments_root=tmp_path, llm=llm, intra_department=False)
    state = new_meeting_state(brief="test", departments=[code])
    out = collector.collect(state)

    assert llm.complete.call_count == 1
    assert out["perspectives"][code] == "single perspective"
    assert out["team_inputs"] == {}


def test_intra_one_team_error_does_not_sink_department(tmp_path):
    code = _write_dept(tmp_path)
    llm = _dispatch_llm({"You are team alpha": RuntimeError("boom"),
                         "You are team beta": "beta take"},
                        default="synthesis")

    collector = PerspectivesCollector(departments_root=tmp_path, llm=llm, intra_department=True)
    state = new_meeting_state(brief="test", departments=[code])
    out = collector.collect(state)

    assert out["perspectives"][code] == "synthesis"
    assert out["team_inputs"][code]["alpha"].startswith("[ERROR]")
    assert out["team_inputs"][code]["beta"] == "beta take"
