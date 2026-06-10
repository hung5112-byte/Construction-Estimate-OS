from pathlib import Path
import pytest
from core.brain.reader import BrainReader

FIXTURE = Path(__file__).parent.parent / "fixtures" / "demo-vault"


def test_read_strategy_returns_vision():
    reader = BrainReader(FIXTURE)
    ctx = reader.load()
    assert "VoltEdge" in ctx.strategy.vision


def test_read_products_returns_three():
    reader = BrainReader(FIXTURE)
    ctx = reader.load()
    assert len(ctx.products) == 3
    assert ctx.products[2].code == "DOC"
    assert ctx.products[2].price_usd == 89


def test_missing_brain_raises():
    with pytest.raises(FileNotFoundError):
        BrainReader(Path("/nonexistent")).load()


def test_read_headcount_returns_departments():
    reader = BrainReader(FIXTURE)
    ctx = reader.load()
    assert "02-npi-program-management" in ctx.headcount.active_departments
    assert len(ctx.headcount.active_departments) == 3


def test_read_state_returns_growth():
    reader = BrainReader(FIXTURE)
    ctx = reader.load()
    assert ctx.state == "growth"


def test_read_glossary_has_rma():
    reader = BrainReader(FIXTURE)
    ctx = reader.load()
    assert "RMA" in ctx.glossary


def test_read_budget_returns_total():
    reader = BrainReader(FIXTURE)
    ctx = reader.load()
    assert ctx.budget.total_year_usd == 80_000
