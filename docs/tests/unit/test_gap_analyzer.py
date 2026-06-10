from unittest.mock import MagicMock
import json
from core.brain.gap_analyzer import GapAnalyzer, Severity
from core.brain.schema import BrainContext, Strategy, Product, Budget, Headcount


def _brain():
    return BrainContext(
        strategy=Strategy(vision="V", icp="SMEs with 5-50 employees (business owners)"),
        products=[
            Product(code="STR", name="Starter", price_usd=40, margin_pct=60),
            Product(code="PRE", name="Premium", price_usd=800, margin_pct=75),
        ],
        budget=Budget(total_year_usd=96_000, mkt_quarter_remaining_usd=64_000),
        headcount=Headcount(
            active_departments=["05-service-operations"],
            active_agents={"05-service-operations": ["service-ops-manager", "inventory"]},
        ),
        laws=[], decisions=[], state="growth", glossary={},
    )


def test_gap_detects_icp_mismatch():
    fake = json.dumps([
        {"field": "ICP", "severity": "CRITICAL",
         "current_value": "SMEs (business owners)",
         "brief_value": "high-income individuals",
         "reason": "Brief diverges from strategy ICP", "citation": "00-Brain/strategy.md"}
    ])
    llm = MagicMock(complete=MagicMock(return_value=fake))
    g = GapAnalyzer(llm=llm)
    gaps = g.analyze(brief="Ad campaign targeting high-income individuals", brain=_brain())
    assert len(gaps) == 1
    assert gaps[0].severity == Severity.CRITICAL
    assert "ICP" in gaps[0].field


def test_gap_empty_when_brain_sufficient():
    llm = MagicMock(complete=MagicMock(return_value="[]"))
    g = GapAnalyzer(llm=llm)
    gaps = g.analyze(brief="Draft an accountant JD", brain=_brain())
    assert gaps == []
