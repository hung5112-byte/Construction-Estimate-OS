from datetime import datetime
from pathlib import Path

from core.orchestrator.flow_controller import FlowResult, FlowStage
from core.signals.dispatcher import build_brief, dispatch
from core.signals.schema import DispatchStatus, Event, Severity, TriageResult

EVENT = Event(source="email", external_id="1", sender="ops@factory.com",
              subject="Line down", body="SMT line 2 halted.",
              received_at=datetime(2026, 7, 1))
RESULT = TriageResult(severity=Severity.CRITICAL,
                      departments=["Quality & Reliability"],
                      summary="Production line stopped.")


class FakeFC:
    """Stops at Stop 1 — approving or executing from a machine trigger is a bug."""

    def __init__(self, run_stage, meeting_stage=FlowStage.PAUSE_DECISION_REPORT):
        self.run_stage = run_stage
        self.meeting_stage = meeting_stage
        self.meeting_called_with = None
        self.folder = Path("/tmp/task-x")

    def run(self, brief):
        self.brief = brief
        return FlowResult(stage=self.run_stage, task_folder=self.folder, message="m")

    def run_meeting(self, task_folder, departments):
        self.meeting_called_with = departments
        return FlowResult(stage=self.meeting_stage, task_folder=self.folder, message="m")

    def approve_decision(self, *a, **k):
        raise AssertionError("machine trigger must never approve (Stop 1 is human)")

    def execute(self, *a, **k):
        raise AssertionError("machine trigger must never execute (Stop 2 is human)")


def test_brief_carries_severity_departments_and_source():
    brief = build_brief(EVENT, RESULT)
    assert "CRITICAL EVENT" in brief
    assert "Quality & Reliability" in brief
    assert "ops@factory.com" in brief
    assert "untrusted" in brief.lower()


def test_happy_path_runs_meeting_and_stops_at_stop_1():
    fc = FakeFC(run_stage=FlowStage.PAUSE_DECISION_REPORT)
    r = dispatch(EVENT, RESULT, fc)
    assert r.status == DispatchStatus.MEETING_STARTED
    assert fc.meeting_called_with == ["Quality & Reliability"]
    assert "approval required" in r.message


def test_clarification_parks_without_meeting():
    fc = FakeFC(run_stage=FlowStage.PAUSE_CLARIFICATION)
    r = dispatch(EVENT, RESULT, fc)
    assert r.status == DispatchStatus.PARKED_CLARIFICATION
    assert fc.meeting_called_with is None  # never guess answers for the human


def test_run_error_is_reported():
    fc = FakeFC(run_stage=FlowStage.ERROR)
    r = dispatch(EVENT, RESULT, fc)
    assert r.status == DispatchStatus.ERROR


def test_meeting_error_is_reported():
    fc = FakeFC(run_stage=FlowStage.PAUSE_DECISION_REPORT,
                meeting_stage=FlowStage.ERROR)
    assert dispatch(EVENT, RESULT, fc).status == DispatchStatus.ERROR
