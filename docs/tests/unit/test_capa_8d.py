from core.tools.capa_8d import Capa8D


def test_on_track_early_discipline_within_sla():
    c = Capa8D()
    r = c.run("capa Q-101 step=3 days_open=10 severity=medium containment=yes")
    assert r.data["status"] == "On Track"
    assert r.data["completeness_pct"] == 37.5  # 3/8
    assert r.data["next_action"].startswith("D4")
    assert r.sources  # RULE 5


def test_overdue_past_sla():
    c = Capa8D()
    r = c.run("capa Q-102 step=5 days_open=80 sla_days=60 severity=high containment=yes")
    assert r.data["status"] == "Overdue"
    assert r.data["aging_ratio"] > 1.0
    assert r.data["escalate"] is True
    assert any("Overdue" in f for f in r.data["flags"])


def test_high_severity_without_containment_escalates_but_not_overdue():
    c = Capa8D()
    # D3 not reached (step<3) on a critical issue that is only 5 days old:
    # containment gap → escalate/P1/At Risk, but NOT "Overdue" (it isn't past SLA).
    r = c.run("capa Q-103 step=2 days_open=5 severity=critical")
    assert r.data["containment_in_place"] is False
    assert r.data["status"] == "At Risk"
    assert r.data["escalate"] is True
    assert any("containment" in f.lower() for f in r.data["flags"])
    assert r.data["priority"] == "P1"
    assert "containment" in r.data["recommended_action"].lower()
    assert "escalate" in r.data["recommended_action"].lower()


def test_fresh_issue_is_not_labeled_overdue():
    c = Capa8D()
    # 3 days into a 30-day (critical) SLA must never read "Overdue"
    r = c.run("capa Q-107 step=4 days_open=3 severity=critical containment=yes")
    assert r.data["status"] != "Overdue"
    assert r.data["aging_ratio"] < 1.0


def test_closed_when_all_disciplines_complete():
    c = Capa8D()
    r = c.run("capa Q-104 step=8 days_open=40 severity=medium")
    assert r.data["status"] == "Closed"
    assert r.data["completeness_pct"] == 100.0
    assert "archive" in r.data["recommended_action"].lower()


def test_recurrence_raises_flag_and_priority():
    c = Capa8D()
    r = c.run("capa Q-105 step=4 days_open=20 severity=medium containment=yes recurrence=yes")
    assert r.data["recurrence"] is True
    assert any("Recurrence" in f for f in r.data["flags"])
    assert r.data["priority"] in ("P1", "P2")


def test_sla_inferred_from_severity_when_absent():
    c = Capa8D()
    r = c.run("capa Q-106 step=4 days_open=1 severity=critical containment=yes")
    assert r.data["sla_days"] == 30  # critical default


def test_no_signals_returns_note():
    c = Capa8D()
    r = c.run("capa Q-000")
    assert r.data == {}
    assert "no capa signals" in r.notes.lower()
