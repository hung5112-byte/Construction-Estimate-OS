"""ROM mode: playbooks × intake → three-point estimate with class/band, questions, gates, proposal."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.estimating import pipeline
from core.estimating.client_safe import blocking, scan
from core.estimating.playbooks import list_playbooks, quantity_for, resolve_basis, resolve_playbook

REPO = Path(__file__).resolve().parents[3]


def _j(folder: Path, name: str):
    return json.loads((folder / name).read_text(encoding="utf-8"))


def test_all_playbooks_load_validate_and_map_to_benchmarks():
    from core.estimating.cost_engine import load_benchmarks
    bands = {b["building_type"] for b in load_benchmarks()}
    books = list_playbooks()
    assert set(books) == {"restaurant-ti", "salon-beauty", "medical-dental", "retail-ti", "office-buildout", "white-box", "ground-up-retail", "industrial-warehouse"}
    for pb in books.values():
        assert pb.validate() == [], pb.project_type
        assert pb.building_type_band in bands, pb.building_type_band
        assert pb.status == "seed" and all("to load" in a.source for a in pb.assemblies)      # placeholders stay honest
        rows = pb.cost_rows()
        assert all(r.pricing_basis == "assembly" and r.uncertain and r.unit_low <= r.unit_total <= r.unit_high for r in rows.values())


def test_aliases_basis_and_quantity_rules():
    pb = resolve_playbook("Restaurant remodel")
    assert pb.project_type == "restaurant-ti"
    with pytest.raises(KeyError):
        resolve_playbook("space station")
    b = resolve_basis(pb, {"gross_sf": 3200, "fields": {"hood_lf": 14}})
    assert b.values["hood_lf"] == 14 and b.values["kitchen_sf"] == pytest.approx(960) and not b.missing
    assert any("kitchen_sf" in a for a in b.assumptions) and not any("hood_lf" in a for a in b.assumptions)
    hood = next(a for a in pb.assemblies if a.code == "23-hood-type1-per-lf")
    assert quantity_for(hood, b) == (14.0, "1 × hood_lf (14)")
    missing = resolve_basis(pb, {"fields": {}})
    assert "gross_sf" in missing.missing


@pytest.fixture(scope="module")
def rom_run(tmp_path_factory):
    vault = tmp_path_factory.mktemp("vault")
    shutil.copytree(REPO / "00-Brain", vault / "00-Brain")
    folder = pipeline.rom(vault, {"project_type": "restaurant-ti", "name": "Pho 88 — 3,200 SF restaurant TI", "gross_sf": 3200, "city": "Plano",
                                  "fields": {"hood_lf": 14, "fixture_count": 9}, "excluded_trades": ["fire-sprinkler"],
                                  "allowances": [{"name": "signage", "amount": 8000}], "notes": "cooler relocation"})
    return vault, folder


def test_rom_files_class_band_and_three_point(rom_run):
    _, folder = rom_run
    for f in ("00-intake.json", "00-playbook.json", "00-project-profile.md", "04-takeoff-ledger.md", "05-clarification.md", "06-estimate.md", "06-risks.json",
              "07-review-scorecard.md", "08-estimate-report.md", "09-proposal-draft.md", "09-client-safe-findings.md"):
        assert (folder / f).exists(), f
    prof = _j(folder, "00-project-profile.json")
    assert prof["aace_class"] == 5 and prof["accuracy_band"] == "−30% / +50%" and prof["playbook"]["project_type"] == "restaurant-ti"
    assert prof["exclusions"] == {"trade:fire-sprinkler": "excluded at intake"}
    est = _j(folder, "06-estimate.json")
    tp = est["meta"]["three_point"]
    assert tp["low"]["total"] < tp["target"]["total"] < tp["high"]["total"] and tp["spread_pct"] > 30
    assert est["meta"]["mode"] == "rom" and est["meta"]["location_factor"] == 0.88
    bases = {p["pricing_basis"] for p in est["lines"]}
    assert bases == {"assembly", "allowance"}
    assert not [p for p in est["lines"] if "UNPRICED" in p["flags"]]
    assert all("UNCERTAIN" in p["flags"] for p in est["lines"] if p["pricing_basis"] == "assembly")   # seed playbook → every assembly line flagged
    assert not any("fire-sprinkler" == (it.get("tags") or {}).get("trade") for it in _j(folder, "04-takeoff-ledger.json"))
    bench = est["meta"]["benchmark"]["checks"][0]
    assert bench["status"] == "inside" and bench["band"] == "150–400"
    report = (folder / "08-estimate-report.md").read_text(encoding="utf-8")
    assert "Three-point (class 5, −30% / +50%)" in report and "Excluded" not in report.split("## Assumptions")[0]


def test_rom_questions_carry_defaults_as_assumptions_and_high_risks_are_mitigated(rom_run):
    _, folder = rom_run
    qs = _j(folder, "05-questions.json")
    warns = [q for q in qs if q["severity"] == "WARN" and "Default used" in q["text"]]
    assert warns and all(q["assumption"] for q in warns)
    crits = [q for q in qs if q["severity"] == "CRITICAL"]
    assert crits and all(q["assumption"] for q in crits)         # every high risk in this playbook has a playbook exclusion
    risks = _j(folder, "06-risks.json")
    assert all(r["mitigation"]["type"] in ("exclusion", "rfi") for r in risks if r["severity"] == "high")
    sc = _j(folder, "07-review-scorecard.json")
    by = {g["id"]: g for g in sc["gates"]}
    assert sc["verdict"] == "APPROVE", [g for g in sc["gates"] if not g["passed"]]
    assert by["G3b"]["passed"] and by["G11"]["passed"] and by["G12"]["passed"] and by["G13"]["passed"] and by["G7"]["passed"]


def test_rom_proposal_is_client_safe_and_hides_internals(rom_run):
    vault, folder = rom_run
    text = (folder / "09-proposal-draft.md").read_text(encoding="utf-8")
    assert not blocking(scan(text))
    for token in ("[UNCERTAIN]", "seed", "markup", "unit cost", "library", "AUTO-ASSUMED"):
        assert token.lower() not in text.lower(), token
    assert "| Low | Target | High |" in text and "expected accuracy −30% / +50%" in text
    assert "signage: $8,000" in text and "fire-sprinkler" in text.lower()      # allowance shown; excluded trade listed
    outs = pipeline.approve(folder, vault)
    assert any(o.name == "proposal-draft.docx" for o in outs)


def test_rom_missing_required_fact_blocks_the_verdict(tmp_path):
    shutil.copytree(REPO / "00-Brain", tmp_path / "00-Brain")
    folder = pipeline.rom(tmp_path, {"project_type": "office", "name": "no-sf office", "city": "Dallas", "fields": {}})
    sc = _j(folder, "07-review-scorecard.json")
    assert sc["verdict"] == "REVISE" and not next(g for g in sc["gates"] if g["id"] == "G7")["passed"]
    qs = _j(folder, "05-questions.json")
    assert any(q["severity"] == "CRITICAL" and "gross_sf" in q["text"] and not q.get("assumption") for q in qs)


def test_rom_warehouse_class4_with_plans(tmp_path):
    shutil.copytree(REPO / "00-Brain", tmp_path / "00-Brain")
    folder = pipeline.rom(tmp_path, {"project_type": "warehouse", "name": "Flex 60k", "gross_sf": 60000, "city": "Fort Worth", "plans_available": True,
                                     "fields": {"dock_doors": 8, "office_sf": 4000}})
    prof = _j(folder, "00-project-profile.json")
    sc = _j(folder, "07-review-scorecard.json")
    assert prof["aace_class"] == 4 and prof["building_type"] == "tilt-wall industrial"
    assert sc["verdict"] == "APPROVE", [g for g in sc["gates"] if not g["passed"]]
    docks = next(it for it in _j(folder, "04-takeoff-ledger.json") if it["item_code"] == "08-dock-position")
    assert docks["qty"] == 8 and docks["tags"]["trade"] == "doors-hardware"
