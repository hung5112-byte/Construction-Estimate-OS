import pytest
from pathlib import Path
from core.agents.department import DepartmentLoader

REPO = Path(__file__).parent.parent.parent

# code -> (display name, tier, agent count incl. manager)
EXPECTED = {
    "01-bid-coordination": ("Bid Coordination & Document Control", 1, 5),
    "02-civil-structural": ("Civil & Structural Estimating", 1, 4),
    "03-architectural": ("Architectural Estimating", 1, 5),
    "04-mep": ("MEP Estimating", 1, 4),
    "05-cost-engineering": ("Cost Engineering & General Conditions", 1, 5),
    "06-estimate-review": ("Estimate Review", 1, 4),
}


def test_load_bid_coordination_dept():
    loader = DepartmentLoader(REPO / "departments")
    dept = loader.load("01-bid-coordination")
    assert dept.code == "01-bid-coordination"
    assert dept.name_local == "Bid Coordination & Document Control"
    assert dept.tier == 1
    assert dept.default_speaker == "bid-coordinator"


def test_load_all_returns_6_with_expected_shape():
    loader = DepartmentLoader(REPO / "departments")
    depts = loader.load_all()
    assert len(depts) == 6
    by_code = {d.code: d for d in depts}
    assert set(by_code) == set(EXPECTED)
    for code, (name, tier, n_agents) in EXPECTED.items():
        d = by_code[code]
        assert d.name_local == name, code
        assert d.tier == tier, code
        assert len(d.agents) == n_agents, code
        # the manager is the default speaker and is one of the agents
        assert d.default_speaker in d.agents, code


def test_unknown_dept_raises():
    loader = DepartmentLoader(REPO / "departments")
    with pytest.raises(FileNotFoundError):
        loader.load("99-nonexistent")
