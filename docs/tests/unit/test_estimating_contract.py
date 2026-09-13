"""Contract test — the engine's real outputs validate against docs/contracts/schemas/*.schema.json."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from core.estimating import CONTRACT_VERSION, pipeline

REPO = Path(__file__).resolve().parents[3]
SCHEMAS = REPO / "docs" / "contracts" / "schemas"
FIX = REPO / "docs" / "tests" / "fixtures" / "sample-set-prairie-creek"


def _registry() -> Registry:
    reg = Registry()
    for f in SCHEMAS.glob("*.schema.json"):
        sch = json.loads(f.read_text(encoding="utf-8"))
        reg = reg.with_resource(f.name, Resource.from_contents(sch))
        reg = reg.with_resource(sch["$id"], Resource.from_contents(sch))
    return reg


def _validate(name: str, data) -> None:
    sch = json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
    v = Draft202012Validator(sch, registry=_registry())
    errs = sorted(v.iter_errors(data), key=lambda e: list(e.path))
    assert not errs, f"{name}: " + "; ".join(f"{list(e.path)}: {e.message[:90]}" for e in errs[:5])


@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    vault = tmp_path_factory.mktemp("vault")
    shutil.copytree(REPO / "00-Brain", vault / "00-Brain")
    detailed = pipeline.run_all(vault, FIX, "Prairie Creek contract run", "office-warehouse", "Plano", 2)
    rom = pipeline.rom(vault, {"project_type": "restaurant-ti", "name": "contract ROM", "gross_sf": 3000, "city": "Plano", "fields": {}})
    return vault, detailed, rom


def test_contract_version_and_schema_files_exist():
    assert CONTRACT_VERSION == "1.0"
    names = {f.name for f in SCHEMAS.glob("*.schema.json")}
    assert {"line.schema.json", "priced_line.schema.json", "question.schema.json", "gate.schema.json", "risk.schema.json", "profile.schema.json",
            "estimate.schema.json", "scorecard.schema.json", "rom_request.schema.json", "client_finding.schema.json"} <= names
    assert (REPO / "docs" / "contracts" / "estimate-service.v1.md").exists()


@pytest.mark.parametrize("which", ["detailed", "rom"])
def test_engine_outputs_validate(runs, which):
    _, detailed, rom = runs
    folder = detailed if which == "detailed" else rom
    j = lambda n: json.loads((folder / n).read_text(encoding="utf-8"))  # noqa: E731
    _validate("profile", j("00-project-profile.json"))
    for it in j("04-takeoff-ledger.json"):
        _validate("line", it)
    _validate("estimate", j("06-estimate.json"))
    _validate("scorecard", j("07-review-scorecard.json"))
    for q in j("05-questions.json"):
        _validate("question", q)
    for f in j("09-client-safe-findings.json"):
        _validate("client_finding", f)
    if which == "rom":
        _validate("rom_request", j("00-intake.json"))
        for r in j("06-risks.json"):
            _validate("risk", r)


def test_rom_request_schema_rejects_bad_input():
    sch = json.loads((SCHEMAS / "rom_request.schema.json").read_text(encoding="utf-8"))
    v = Draft202012Validator(sch, registry=_registry())
    assert list(v.iter_errors({"name": "no type"}))                       # project_type required
    assert list(v.iter_errors({"project_type": "office", "aace_class": 9}))
    assert not list(v.iter_errors({"project_type": "office", "gross_sf": 2500, "fields": {"exam_rooms": 4}}))
