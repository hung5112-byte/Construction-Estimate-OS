from datetime import datetime

import yaml

from core.signals.event_log import log_event
from core.signals.schema import (DispatchResult, DispatchStatus, Event,
                                 PolicyAction, PolicyDecision, Severity,
                                 TriageResult)

EVENT = Event(source="email", external_id="1", sender="ops@factory.com",
              subject="Line down at CM", body="SMT line 2 halted.",
              received_at=datetime(2026, 7, 1, 9, 30))
RESULT = TriageResult(severity=Severity.CRITICAL,
                      departments=["Quality & Reliability"],
                      summary="Production line stopped.", rationale="Output halted.")
DECISION = PolicyDecision(action=PolicyAction.TRIGGER_MEETING, reason="passed all gates")


def _frontmatter(text: str) -> dict:
    return yaml.safe_load(text.split("---")[1])


def test_note_written_with_frontmatter(tmp_path):
    rel = log_event(tmp_path, EVENT, RESULT, DECISION)
    assert rel == "01-Inbox/Events/2026-07-01-0930-line-down-at-cm.md"
    text = (tmp_path / rel).read_text(encoding="utf-8")
    fm = _frontmatter(text)
    assert fm["type"] == "signal-event"
    assert fm["severity"] == "critical"
    assert fm["policy_action"] == "trigger-meeting"
    assert "SMT line 2 halted." in text


def test_dispatch_link_recorded(tmp_path):
    dispatch = DispatchResult(status=DispatchStatus.MEETING_STARTED,
                              task_folder="/vault/02-Tasks/2026-07-01-0931-line-down",
                              message="Stop 1 ready.")
    rel = log_event(tmp_path, EVENT, RESULT, DECISION, dispatch)
    text = (tmp_path / rel).read_text(encoding="utf-8")
    assert _frontmatter(text)["task_folder"].endswith("line-down")
    assert "[[2026-07-01-0931-line-down]]" in text
