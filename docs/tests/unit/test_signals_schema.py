from datetime import datetime

from core.signals.schema import Event

RECEIVED = datetime(2026, 7, 1, 9, 0)


def _event(**overrides) -> Event:
    base = dict(source="email", external_id="42", sender="ops@factory.com",
                subject="Line down at CM site", body="SMT line 2 halted.",
                received_at=RECEIVED)
    base.update(overrides)
    return Event(**base)


def test_fingerprint_is_stable():
    assert _event().fingerprint() == _event().fingerprint()


def test_fingerprint_ignores_external_id():
    # A re-fetched copy of the same mail (new uid) must not look new
    assert _event(external_id="42").fingerprint() == _event(external_id="99").fingerprint()


def test_fingerprint_changes_with_content():
    assert _event().fingerprint() != _event(body="different body").fingerprint()
    assert _event().fingerprint() != _event(sender="other@x.com").fingerprint()
