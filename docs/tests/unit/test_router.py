from unittest.mock import MagicMock
from pathlib import Path
from core.orchestrator.router import Router, TaskClass
from core.brain.schema import (
    BrainContext, Strategy, Budget, Headcount, Product,
)

REPO = Path(__file__).parent.parent.parent


def _brain():
    return BrainContext(
        strategy=Strategy(vision="V", icp="mid-size US retailers"),
        products=[Product(code="P", name="X", price_usd=1000, margin_pct=50)],
        budget=Budget(total_year_usd=1_000_000),
        headcount=Headcount(active_departments=["05-service-operations", "02-npi-program-management"]),
        laws=[], decisions=[], state="growth", glossary={},
    )


def test_router_keyword_simple():
    llm = MagicMock(complete=MagicMock(return_value='{"class": "SIMPLE", "departments": ["05-service-operations"], "reasoning": "SOP task"}'))
    r = Router(llm=llm, rules_path=REPO / "core/orchestrator/classifier_rules.yaml")
    result = r.classify("Draft an RMA intake SOP", _brain())
    assert result.class_ == TaskClass.SIMPLE


def test_router_keyword_complex():
    llm = MagicMock(complete=MagicMock(return_value=
        '{"class": "COMPLEX", "departments": ["01-hardware-engineering", "02-npi-program-management", "03-quality-reliability", "04-mfg-supplier-quality", "05-service-operations"], "reasoning": "pilot launch needs many"}'
    ))
    r = Router(llm=llm, rules_path=REPO / "core/orchestrator/classifier_rules.yaml")
    result = r.classify("Plan the NPI pilot launch of the new terminal", _brain())
    assert result.class_ == TaskClass.COMPLEX
    assert len(result.departments) == 5


def test_router_returns_reasoning():
    llm = MagicMock(complete=MagicMock(return_value=
        '{"class": "STRATEGIC", "departments": ["01-hardware-engineering","02-npi-program-management","03-quality-reliability","04-mfg-supplier-quality","05-service-operations"], "reasoning": "Factory transfer high stakes"}'
    ))
    r = Router(llm=llm, rules_path=REPO / "core/orchestrator/classifier_rules.yaml")
    result = r.classify("Evaluate transferring PT500 production to the Mexico CM", _brain())
    assert "Factory transfer" in result.reasoning
