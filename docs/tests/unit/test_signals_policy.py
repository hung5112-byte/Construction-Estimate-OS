from datetime import datetime, timedelta

from core.signals.policy import TriggerPolicy
from core.signals.rules import SignalRules
from core.signals.schema import Event, PolicyAction, Severity, TriageResult

RULES = SignalRules.model_validate({
    "policy": {"min_severity_to_trigger": "critical",
               "dedup_window_hours": 24,
               "max_auto_meetings_per_day": 2},
})
NOW = datetime(2026, 7, 1, 9, 0)


def _event(body: str) -> Event:
    return Event(source="email", external_id="1", sender="ops@factory.com",
                 subject="alert", body=body, received_at=NOW)


def _result(severity: Severity) -> TriageResult:
    return TriageResult(severity=severity, summary="s")


def test_below_threshold_is_log_only(tmp_path):
    policy = TriggerPolicy(tmp_path, RULES, now_fn=lambda: NOW)
    d = policy.decide(_event("a"), _result(Severity.HIGH))
    assert d.action == PolicyAction.LOG_ONLY
    assert "below trigger threshold" in d.reason


def test_critical_triggers(tmp_path):
    policy = TriggerPolicy(tmp_path, RULES, now_fn=lambda: NOW)
    d = policy.decide(_event("a"), _result(Severity.CRITICAL))
    assert d.action == PolicyAction.TRIGGER_MEETING


def test_duplicate_within_window_is_suppressed(tmp_path):
    policy = TriggerPolicy(tmp_path, RULES, now_fn=lambda: NOW)
    policy.decide(_event("a"), _result(Severity.CRITICAL))
    d = policy.decide(_event("a"), _result(Severity.CRITICAL))
    assert d.action == PolicyAction.LOG_ONLY
    assert "duplicate" in d.reason


def test_duplicate_after_window_triggers_again(tmp_path):
    clock = {"now": NOW}
    policy = TriggerPolicy(tmp_path, RULES, now_fn=lambda: clock["now"])
    policy.decide(_event("a"), _result(Severity.CRITICAL))
    clock["now"] = NOW + timedelta(hours=25)
    d = policy.decide(_event("a"), _result(Severity.CRITICAL))
    assert d.action == PolicyAction.TRIGGER_MEETING


def test_daily_cap(tmp_path):
    policy = TriggerPolicy(tmp_path, RULES, now_fn=lambda: NOW)
    assert policy.decide(_event("a"), _result(Severity.CRITICAL)).action \
        == PolicyAction.TRIGGER_MEETING
    assert policy.decide(_event("b"), _result(Severity.CRITICAL)).action \
        == PolicyAction.TRIGGER_MEETING
    d = policy.decide(_event("c"), _result(Severity.CRITICAL))
    assert d.action == PolicyAction.LOG_ONLY
    assert "daily cap" in d.reason


def test_state_survives_restart(tmp_path):
    TriggerPolicy(tmp_path, RULES, now_fn=lambda: NOW) \
        .decide(_event("a"), _result(Severity.CRITICAL))
    # New instance, same vault → same dedup memory (RULE 3)
    fresh = TriggerPolicy(tmp_path, RULES, now_fn=lambda: NOW)
    d = fresh.decide(_event("a"), _result(Severity.CRITICAL))
    assert d.action == PolicyAction.LOG_ONLY
    assert "duplicate" in d.reason
