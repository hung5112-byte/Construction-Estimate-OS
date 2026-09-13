from __future__ import annotations

import json
import shutil
from pathlib import Path

from core.estimating.evals import eval_rom_set, run_eval, score_ledger, score_rom

REPO = Path(__file__).resolve().parents[3]
FIX = REPO / "docs" / "tests" / "fixtures" / "sample-set-prairie-creek"


def test_score_ledger_math():
    exp = [{"item_code": "a", "qty": 10, "unit": "EA"}, {"item_code": "b", "qty": 100, "unit": "SF"}, {"item_code": "c", "qty": 5, "unit": "EA"}]
    got = [{"item_code": "a", "qty": 6}, {"item_code": "a", "qty": 4}, {"item_code": "b", "qty": 140}, {"item_code": "z", "qty": 1}]
    s = score_ledger(got, exp, tol=0.25)
    assert s.coverage == round(2 / 3, 4) and s.precision_at_tol == 0.5 and s.missing == ["c"] and s.extra == ["z"]
    assert s.off_tolerance[0]["item_code"] == "b" and s.composite == round((2 / 3) ** 0.4 * 0.5 ** 0.6, 4)


def test_seed_takeoff_scores_perfectly_on_the_synthetic_set(tmp_path):
    shutil.copytree(REPO / "00-Brain", tmp_path / "00-Brain")
    res, md = run_eval(tmp_path, FIX, runs=2, tol=0.25, out_dir=tmp_path / "evals")
    assert res["kind"] == "detailed" and res["composite_mean"] == 1.0 and res["composite_spread"] == 0.0, res["scores"][0]
    assert md.exists() and "Composite 1.000" in md.read_text(encoding="utf-8")


def test_rom_band_scoring(tmp_path):
    tp = {"low": {"total": 400_000}, "target": {"total": 550_000}, "high": {"total": 780_000}}
    assert score_rom("x", tp, 600_000, 5, "−30% / +50%").inside_band and not score_rom("y", tp, 900_000, 5, "b").inside_band
    shutil.copytree(REPO / "00-Brain", tmp_path / "00-Brain")
    case = tmp_path / "rom-set" / "pho-88"
    case.mkdir(parents=True)
    (case / "intake.json").write_text(json.dumps({"project_type": "restaurant-ti", "gross_sf": 3200, "city": "Plano", "fields": {"hood_lf": 14}}), encoding="utf-8")
    (case / "actual.json").write_text(json.dumps({"actual_total": 600_000}), encoding="utf-8")
    res = eval_rom_set(tmp_path, tmp_path / "rom-set", runs=1)
    assert res["cases"] == 1 and res["results"][0]["aace_class"] == 5 and isinstance(res["band_hit_rate"], float)
