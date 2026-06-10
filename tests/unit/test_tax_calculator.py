from core.tools.tax_calculator import TaxCalculator


def test_texas_sales_tax_default_state_rate():
    tc = TaxCalculator()
    r = tc.run("sales_tax 100000")  # default 6.25% Texas state rate
    assert r.data["tax_amount_usd"] == 6_250
    assert r.data["total_usd"] == 106_250
    assert r.sources  # must cite an authority (RULE 5)


def test_texas_sales_tax_custom_combined_rate():
    tc = TaxCalculator()
    r = tc.run("sales_tax 100000 rate=8.25")  # state + max local
    assert r.data["tax_amount_usd"] == 8_250


def test_self_employment_tax_math():
    tc = TaxCalculator()
    r = tc.run("self_employment_tax 100000")
    # 92.35% of net earnings is the taxable base
    assert r.data["taxable_base_usd"] == 92_350
    # 15.3% (12.4% SS + 2.9% Medicare) under the wage base
    assert r.data["se_tax_usd"] == 14_130


def test_federal_income_tax_is_progressive_and_flagged():
    tc = TaxCalculator()
    r = tc.run("federal_income_tax 50000")
    assert r.data["taxable_usd"] == 50_000
    assert r.data["tax_usd"] > 0
    # Must carry the not-advice disclaimer and cite the IRS authority
    assert "NOT tax advice" in r.notes
    assert any("Texas has NO state personal income tax" in s for s in r.sources)


def test_federal_corporate_tax_21_percent():
    tc = TaxCalculator()
    r = tc.run("federal_corporate_tax 100000")
    assert r.data["tax_usd"] == 21_000


def test_texas_franchise_tax_no_tax_due_below_threshold():
    tc = TaxCalculator()
    r = tc.run("franchise_tax 500000")  # below ~$2.47M placeholder threshold
    assert r.data["franchise_tax_usd"] == 0


def test_progressive_engine_exact():
    # Deterministic check of the progressive engine with a controlled bracket set,
    # independent of the unverified default federal thresholds.
    tc = TaxCalculator()
    brackets = [(10_000, 0.10), (40_000, 0.20), (float("inf"), 0.30)]
    # 50,000 taxable -> 10k@10% + 30k@20% + 10k@30% = 1,000 + 6,000 + 3,000 = 10,000
    assert tc._progressive(50_000, brackets) == 10_000
