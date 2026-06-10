import pytest
from pathlib import Path
from core.agents.department import DepartmentLoader

REPO = Path(__file__).parent.parent.parent

# code -> (display name, tier, agent count incl. manager)
EXPECTED = {
    "01-hardware-engineering": ("Hardware Engineering", 1, 5),
    "02-npi-program-management": ("NPI & Program Management", 1, 7),
    "03-quality-reliability": ("Quality & Reliability", 1, 6),
    "04-mfg-supplier-quality": ("Manufacturing & Supplier Quality", 2, 5),
    "05-service-operations": ("Service Operations", 2, 6),
}


def test_load_hardware_engineering_dept():
    loader = DepartmentLoader(REPO / "departments")
    dept = loader.load("01-hardware-engineering")
    assert dept.code == "01-hardware-engineering"
    assert dept.name_vn == "Hardware Engineering"
    assert dept.tier == 1
    assert dept.default_speaker == "hw-engineering-manager"


def test_load_all_returns_5_with_expected_shape():
    loader = DepartmentLoader(REPO / "departments")
    depts = loader.load_all()
    assert len(depts) == 5
    by_code = {d.code: d for d in depts}
    assert set(by_code) == set(EXPECTED)
    for code, (name, tier, n_agents) in EXPECTED.items():
        d = by_code[code]
        assert d.name_vn == name, code
        assert d.tier == tier, code
        assert len(d.agents) == n_agents, code
        # the manager is the default speaker and is one of the agents
        assert d.default_speaker in d.agents, code


def test_unknown_dept_raises():
    loader = DepartmentLoader(REPO / "departments")
    with pytest.raises(FileNotFoundError):
        loader.load("99-nonexistent")
