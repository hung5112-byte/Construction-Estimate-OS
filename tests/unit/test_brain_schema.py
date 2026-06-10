import pytest
from core.brain.schema import (
    Strategy, Product, Budget, Headcount, BrainContext
)

def test_strategy_minimal():
    s = Strategy(vision="US SME OS", icp="SMEs with 5-50 employees")
    assert s.vision == "US SME OS"

def test_product_with_price():
    p = Product(code="PRO", name="Premium", price_usd=800, margin_pct=70)
    assert p.price_usd == 800

def test_brain_context_assembly():
    ctx = BrainContext(
        strategy=Strategy(vision="V", icp="I"),
        products=[Product(code="A", name="X", price_usd=1000, margin_pct=50)],
        budget=Budget(total_year_usd=1_000_000, mkt_quarter_remaining_usd=800_000),
        headcount=Headcount(active_departments=["05-service-operations"]),
        laws=[],
        decisions=[],
        state="growth",
        glossary={},
    )
    assert ctx.products[0].name == "X"
    assert ctx.budget.mkt_quarter_remaining_usd == 800_000

def test_invalid_margin_rejected():
    with pytest.raises(ValueError):
        Product(code="A", name="X", price_usd=1000, margin_pct=150)

def test_budget_line_remaining():
    from core.brain.schema import BudgetLine
    line = BudgetLine(department="05-service-operations", allocated_usd=10_000, spent_usd=3_000)
    assert line.remaining_usd == 7_000
