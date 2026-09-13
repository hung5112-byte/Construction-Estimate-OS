from core.tools.bom_health import BomHealth


def test_active_multisource_part_is_low_risk():
    bh = BomHealth()
    r = bh.run("bom R1234 lifecycle=active sources=3 lead_time=8 coverage=16 compliance=ok")
    assert r.data["risk_tier"] == "Low"
    assert r.data["single_source"] is False
    assert "monitor" in r.data["disposition"].lower()
    assert r.sources  # RULE 5


def test_obsolete_part_forces_redesign_out():
    bh = BomHealth()
    r = bh.run("bom U77 lifecycle=obsolete sources=1")
    assert r.data["lifecycle"] == "Obsolete"
    assert "redesign-out" in r.data["disposition"].lower()
    assert r.data["risk_tier"] in ("High", "Critical")


def test_eol_part_recommends_last_time_buy():
    bh = BomHealth()
    r = bh.run("bom IC9 lifecycle=eol sources=1 lead_time=30 coverage=4 ltb_days=45")
    assert r.data["lifecycle"] == "EOL"
    assert "last-time-buy" in r.data["disposition"].lower()
    # LTB urgency should be scored for an EOL part with a deadline
    assert "Last-time-buy urgency" in r.data["factor_risks"]


def test_active_single_source_recommends_second_source():
    bh = BomHealth()
    r = bh.run("bom C55 lifecycle=active sources=1 lead_time=10 coverage=14")
    assert r.data["single_source"] is True
    assert "second source" in r.data["disposition"].lower()


def test_ltb_urgency_ignored_when_not_eol():
    bh = BomHealth()
    # ltb_days on an active part is not meaningful → not scored
    r = bh.run("bom C55 lifecycle=active sources=2 ltb_days=30")
    assert "Last-time-buy urgency" not in r.data["factor_risks"]


def test_coverage_below_target_scores_risk():
    bh = BomHealth()
    # 3 weeks coverage vs 12-week default target → high coverage risk
    r = bh.run("bom X1 coverage=3")
    assert r.data["factor_risks"]["Inventory coverage"] == 75.0


def test_score_is_deterministic():
    bh = BomHealth()
    q = "bom D1 lifecycle=nrnd sources=1 lead_time=40 coverage=6"
    assert bh.run(q).data["risk_score"] == bh.run(q).data["risk_score"]


def test_no_signals_returns_note():
    bh = BomHealth()
    r = bh.run("bom EmptyPart")
    assert r.data == {}
    assert "no bom part signals" in r.notes.lower()
