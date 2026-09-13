from datetime import datetime

from core.signals.prefilter import prefilter
from core.signals.rules import SignalRules
from core.signals.schema import Event

RULES = SignalRules.model_validate({
    "departments": ["Quality & Reliability"],
    "senders": {"allow": ["ops@factory.com"], "block": ["no-reply@ads.example.com"]},
    "keywords": {
        "critical": ["line down", "recall"],
        "high": ["shortage"],
        "ignore": ["newsletter", "unsubscribe"],
    },
})


def _event(sender="someone@x.com", subject="", body="") -> Event:
    return Event(source="email", external_id="1", sender=sender,
                 subject=subject, body=body, received_at=datetime(2026, 7, 1))


def test_blocked_sender_is_dropped():
    v = prefilter(_event(sender="no-reply@ads.example.com", body="line down"), RULES)
    assert not v.pass_to_triage
    assert v.reason == "sender blocked"


def test_newsletter_noise_is_dropped():
    v = prefilter(_event(subject="Weekly newsletter", body="unsubscribe here"), RULES)
    assert not v.pass_to_triage


def test_critical_keyword_beats_ignore_keyword():
    v = prefilter(_event(subject="newsletter", body="URGENT: product recall started"), RULES)
    assert v.pass_to_triage
    assert v.matched_critical == ["recall"]


def test_critical_keyword_passes():
    v = prefilter(_event(subject="Line down at CM"), RULES)
    assert v.pass_to_triage
    assert v.matched_critical == ["line down"]


def test_high_keyword_passes():
    v = prefilter(_event(body="component shortage on connector"), RULES)
    assert v.pass_to_triage
    assert v.matched_high == ["shortage"]


def test_allowlisted_sender_passes_without_keywords():
    v = prefilter(_event(sender="ops@factory.com", body="please review"), RULES)
    assert v.pass_to_triage


def test_unmatched_message_is_dropped():
    v = prefilter(_event(body="lunch on friday?"), RULES)
    assert not v.pass_to_triage
