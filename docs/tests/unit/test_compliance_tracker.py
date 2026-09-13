from core.tools.compliance_tracker import ComplianceTracker

# fixed as_of so tests are deterministic regardless of the real date
AS_OF = "as_of=2026-07-01"


def test_valid_far_from_expiry():
    ct = ComplianceTracker()
    r = ct.run(f"cert RoHS status=valid expiry=2027-01-01 required=yes {AS_OF}")
    assert r.data["status"] == "Valid"
    assert r.data["days_to_expiry"] == 184
    assert r.data["risk_tier"] == "Low"
    assert r.data["shippable"] is True
    assert r.sources  # RULE 5


def test_expiring_soon_inside_renewal_lead():
    ct = ComplianceTracker()
    r = ct.run(f"cert UL expiry=2026-08-01 required=yes lead_time_days=90 {AS_OF}")
    assert r.data["status"] == "Expiring soon"
    assert r.data["days_to_expiry"] == 31
    assert r.data["risk_tier"] == "High"
    assert r.data["shippable"] is True
    assert "renewal" in r.data["recommended_action"].lower()


def test_expired_required_blocks_shipment():
    ct = ComplianceTracker()
    r = ct.run(f"cert FCC expiry=2026-06-01 required=yes {AS_OF}")
    assert r.data["status"] == "Expired"
    assert r.data["days_to_expiry"] == -30
    assert r.data["risk_tier"] == "Critical"
    assert r.data["shippable"] is False
    assert "not shippable" in r.data["recommended_action"].lower()


def test_missing_required_is_critical():
    ct = ComplianceTracker()
    r = ct.run(f"cert CE status=missing required=yes {AS_OF}")
    assert r.data["status"] == "Missing"
    assert r.data["risk_tier"] == "Critical"
    assert r.data["shippable"] is False


def test_noncompliant_required_halts_shipment():
    ct = ComplianceTracker()
    r = ct.run(f"cert REACH status=noncompliant required=yes {AS_OF}")
    assert r.data["status"] == "Non-compliant"
    assert r.data["shippable"] is False
    assert "halt shipment" in r.data["recommended_action"].lower()


def test_optional_expired_is_downrated_and_shippable():
    ct = ComplianceTracker()
    r = ct.run(f"cert ExtraMark expiry=2026-06-01 required=no {AS_OF}")
    assert r.data["status"] == "Expired"
    assert r.data["risk_tier"] == "Moderate"   # not required → down-rated from Critical
    assert r.data["shippable"] is True


def test_days_to_expiry_input_without_date():
    ct = ComplianceTracker()
    r = ct.run(f"cert ITAR days_to_expiry=10 required=yes {AS_OF}")
    assert r.data["status"] == "Expiring soon"
    assert r.data["expiry_date"] is None


def test_pending_required_cert_is_not_shippable():
    ct = ComplianceTracker()
    # a required cert still in progress (not yet issued) must block shipment
    r = ct.run(f"cert UL status=pending required=yes {AS_OF}")
    assert r.data["status"] == "Pending"
    assert r.data["shippable"] is False


def test_pending_optional_cert_is_shippable():
    ct = ComplianceTracker()
    r = ct.run(f"cert Extra status=pending required=no {AS_OF}")
    assert r.data["status"] == "Pending"
    assert r.data["shippable"] is True


def test_no_status_or_expiry_returns_note():
    ct = ComplianceTracker()
    r = ct.run("cert Mystery")
    assert r.data == {}
    assert "no cert status or expiry" in r.notes.lower()
