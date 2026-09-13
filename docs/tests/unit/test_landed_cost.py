from core.tools.landed_cost import LandedCost


def test_tariff_only_isolated_share():
    lc = LandedCost()
    # ex-works $10, +25% Section 301, no fees → tariff 2.50, landed 12.50, share 20%
    r = lc.run("landed 10 units=1 tariff=25 mpf=0")
    assert r.data["tariff_unit"] == 2.5
    assert r.data["landed_unit"] == 12.5
    assert r.data["tariff_share_pct"] == 20.0
    assert r.data["biggest_add_on_driver"] == "tariff"
    assert r.sources  # RULE 5 — must cite an authority


def test_base_duty_and_tariff_stack():
    lc = LandedCost()
    # base duty 2.6% + Section 301 25% on $100 customs value → 2.60 + 25.00
    r = lc.run("landed 100 units=1 duty=2.6 tariff=25 mpf=0")
    assert r.data["base_duty_unit"] == 2.6
    assert r.data["tariff_unit"] == 25.0
    assert r.data["duty_plus_tariff_unit"] == 27.6


def test_freight_amortized_per_unit():
    lc = LandedCost()
    # $5,000 freight over 1,000 units = $5/unit
    r = lc.run("landed 20 units=1000 freight=5000 mpf=0")
    assert r.data["freight_unit"] == 5.0


def test_mpf_ad_valorem_within_min_max():
    lc = LandedCost()
    # customs value entry = 10 × 10,000 = 100,000 → MPF 0.3464% = 346.40 (between
    # min 32.71 and max 634.62) → per unit 346.40 / 10,000 = 0.03464
    r = lc.run("landed 10 units=10000 mpf=0.3464")
    assert r.data["mpf_entry"] == 346.40
    assert r.data["mpf_unit"] == 0.0346


def test_mpf_hits_per_entry_maximum():
    lc = LandedCost()
    # huge entry value → MPF capped at the 634.62 per-entry maximum
    r = lc.run("landed 1000 units=10000 mpf=0.3464")
    assert r.data["mpf_entry"] == 634.62


def test_in_transit_carrying_cost():
    lc = LandedCost()
    # $100 value × 10% annual cost of capital × 36.5/365 days = $1.00
    r = lc.run("landed 100 units=1 cost_of_capital=10 transit_days=36.5 mpf=0")
    assert r.data["in_transit_carrying_unit"] == 1.0


def test_ocean_hmf_only_when_opted_in():
    lc = LandedCost()
    r = lc.run("landed 200 units=1 hmf=0.125 mpf=0")
    assert r.data["hmf_unit"] == 0.25  # 0.125% of $200


def test_dollars_and_cents_precision_preserved():
    lc = LandedCost()
    # ex-works with cents must NOT be truncated to whole dollars
    r = lc.run("landed 42.50 units=1 mpf=0")
    assert r.data["ex_works_unit"] == 42.5
    assert r.data["landed_unit"] == 42.5


def test_carries_not_advice_disclaimer():
    lc = LandedCost()
    r = lc.run("landed 10 units=1 tariff=25")
    assert "NOT customs" in r.notes
    assert any("Section 301" in s for s in r.sources)


def test_mpf_minimum_binding_is_flagged():
    lc = LandedCost()
    # 1 unit, MPF on by default → the $32.71 floor binds and dominates
    r = lc.run("landed 10 tariff=25")
    assert r.data["mpf_at_minimum"] is True
    assert "per-entry minimum" in r.notes
    # at a realistic entry size the ad-valorem MPF clears the floor → not flagged
    r2 = lc.run("landed 10 units=5000 tariff=25")
    assert r2.data["mpf_at_minimum"] is False


def test_invalid_query_returns_note():
    lc = LandedCost()
    r = lc.run("landed")
    assert r.data == {}
    assert "invalid" in r.notes.lower()
