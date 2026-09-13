"""HTTP service over the pipeline (contract v1) — driven through Starlette's TestClient, no network."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from core.estimating.service import create_app

REPO = Path(__file__).resolve().parents[3]
FIX = REPO / "docs" / "tests" / "fixtures" / "sample-set-prairie-creek"


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    vault = tmp_path_factory.mktemp("vault")
    shutil.copytree(REPO / "00-Brain", vault / "00-Brain")
    return TestClient(create_app(vault))


def test_health_lists_playbooks_and_contract(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["contract_version"] == "1.0" and "restaurant-ti" in r.json()["playbooks"]


def test_detailed_flow_over_http(client):
    r = client.post("/estimates/intake", json={"package_dir": str(FIX), "name": "HTTP run", "building_type": "office-warehouse", "city": "Plano"})
    assert r.status_code == 200, r.text
    folder = r.json()["folder"]
    assert len(r.json()["sheet_register"]) == 9 and r.json()["profile"]["aace_class"] == 2
    r = client.post(f"/estimates/{folder}/takeoff")
    assert r.status_code == 200 and len(r.json()["ledger"]) > 50 and all(c["status"] == "match" for c in r.json()["checks"])
    r = client.post(f"/estimates/{folder}/takeoff", json={"reader_lines": [{"division": "09", "item_code": "09-paint-cmu", "description": "Paint CMU", "qty": 6000, "unit": "SF", "sheet": "A-201", "method": "vision", "discipline": "03-architectural", "confidence": 0.7}]})
    assert r.status_code == 200 and any(it["item_code"] == "09-paint-cmu" for it in r.json()["ledger"])
    r = client.post(f"/estimates/{folder}/rfi")
    assert r.status_code == 200 and r.json()["questions"]
    r = client.post(f"/estimates/{folder}/answers", json={"auto_assume": True})
    assert r.status_code == 200 and r.json()["open_critical"] == 0
    r = client.post(f"/estimates/{folder}/price")
    assert r.status_code == 200 and r.json()["markups"][-1]["name"] == "TOTAL BID" and r.json()["meta"]["three_point"]
    r = client.post(f"/estimates/{folder}/review")
    assert r.status_code == 200 and r.json()["verdict"] == "APPROVE", r.text
    r = client.post(f"/estimates/{folder}/report")
    assert r.status_code == 200 and "verdict: APPROVE" in r.json()["report_md"] and r.json()["proposal_md"].startswith("---")
    r = client.post(f"/estimates/{folder}/approve")
    assert r.status_code == 200 and any(o.endswith("estimate-workbook.xlsx") for o in r.json()["outputs"])
    r = client.get(f"/estimates/{folder}/files/06-estimate.json")
    assert r.status_code == 200 and "summary_by_division" in r.json()
    assert client.get(f"/estimates/{folder}/files/../00-Brain/strategy.md").status_code == 404
    assert client.post("/estimates/nope/price").status_code == 404


def test_rom_over_http_and_matched_answers(client):
    r = client.post("/estimates/rom", json={"project_type": "salon", "name": "HTTP salon", "gross_sf": 1800, "city": "Dallas", "fields": {"shampoo_bowls": 4}})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["aace_class"] == 5 and body["three_point"]["low"]["total"] < body["three_point"]["high"]["total"] and body["verdict"] in ("APPROVE", "REVISE")
    q = next(q for q in body["questions"] if q["severity"] == "WARN")
    r2 = client.post(f"/estimates/{body['folder']}/answers", json={"answers": [{"match": q["text"][:25], "answer": "confirmed 4 bowls"}]})
    assert r2.status_code == 200 and any(x.get("answer") == "confirmed 4 bowls" for x in r2.json()["questions"])
    assert client.post("/estimates/rom", json={"name": "no type"}).status_code == 400


def test_token_guard(monkeypatch, tmp_path):
    shutil.copytree(REPO / "00-Brain", tmp_path / "00-Brain")
    monkeypatch.setenv("CE_SERVICE_TOKEN", "s3cret")
    c = TestClient(create_app(tmp_path))
    assert c.get("/health").status_code == 200
    assert c.post("/estimates/rom", json={"project_type": "office", "gross_sf": 1000}).status_code == 401
    assert c.post("/estimates/rom", json={"project_type": "office", "gross_sf": 1000}, headers={"X-Api-Key": "s3cret"}).status_code == 200
