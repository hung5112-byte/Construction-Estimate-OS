from core.tools.supplier_risk import SupplierRisk


def test_low_risk_healthy_multisource_supplier():
    sr = SupplierRisk()
    r = sr.run("supplier Acme financial=90 single_source=no geo=10 ppm=200 otd=99 lead_time=20 capacity=60")
    assert r.data["risk_tier"] == "Low"
    assert r.data["single_source"] is False
    assert r.sources  # RULE 5


def test_single_source_drives_up_risk():
    sr = SupplierRisk()
    r = sr.run("supplier SolePart financial=60 single_source=yes geo=70 ppm=3000 otd=88 lead_time=70 capacity=95")
    assert r.data["risk_tier"] in ("High", "Critical")
    assert r.data["single_source"] is True
    # single-source should surface as a top driver and shape the action
    drivers = [d["factor"] for d in r.data["top_risk_drivers"]]
    assert "Single-source dependency" in drivers
    assert "second source" in r.data["recommended_action"].lower()


def test_score_is_deterministic():
    sr = SupplierRisk()
    q = "supplier X financial=50 single_source=yes geo=50 otd=90"
    assert sr.run(q).data["risk_score"] == sr.run(q).data["risk_score"]


def test_partial_signals_renormalize_weights():
    sr = SupplierRisk()
    # only two factors supplied — score must still be a valid 0–100 number
    r = sr.run("supplier Y financial=0 otd=0")  # worst on both → ~100
    assert r.data["factors_scored"] == 2
    assert r.data["risk_score"] == 100.0
    # financial was supplied (scored), so it must NOT be listed as missing
    assert "Supplier financial health" not in r.data["factors_missing"]
    assert "Geographic / country risk" in r.data["factors_missing"]


def test_quality_ppm_scales_against_ceiling():
    sr = SupplierRisk()
    # ppm at the default 5000 ceiling → 100 risk on the quality factor
    r = sr.run("supplier Z ppm=5000")
    assert r.data["factor_risks"]["Quality (defect PPM)"] == 100.0


def test_capacity_below_comfort_is_no_risk():
    sr = SupplierRisk()
    r = sr.run("supplier Z capacity=70")  # below 85 comfort default
    assert r.data["factor_risks"]["Capacity utilization"] == 0.0


def test_no_signals_returns_note():
    sr = SupplierRisk()
    r = sr.run("supplier NoData")
    assert r.data == {}
    assert "no supplier signals" in r.notes.lower()


def test_tier_thresholds():
    sr = SupplierRisk()
    assert sr._tier(80) == "Critical"
    assert sr._tier(60) == "High"
    assert sr._tier(30) == "Moderate"
    assert sr._tier(10) == "Low"
