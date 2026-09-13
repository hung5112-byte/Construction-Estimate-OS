"""Accuracy harness — the number that says whether to trust the estimate.

Detailed sets (drawings + ground_truth.json with `expected_lines`): coverage = expected item codes found,
precision@tol = found lines whose quantity is within ±tol of expected, composite = coverage^0.4 × precision^0.6
(TakeoffBench-v1 convention, so results compare with the published human baseline 77.6 and Handoff-H1 81.6).
ROM sets (intake.json + actual.json per case): does the actual land inside the stated band, and the error of
the target. Every eval runs N times so run-to-run spread is reported, not hidden.
"""
from __future__ import annotations

import json
import shutil
import statistics
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class LedgerScore:
    coverage: float
    precision_at_tol: float
    composite: float
    tol: float
    expected: int
    found: int
    within_tol: int
    missing: list[str] = field(default_factory=list)
    off_tolerance: list[dict] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)


def score_ledger(ledger_items: list[dict], expected_lines: list[dict], tol: float = 0.25) -> LedgerScore:
    got: dict[str, float] = {}
    for it in ledger_items:
        got[it["item_code"]] = got.get(it["item_code"], 0.0) + float(it["qty"])
    exp = {e["item_code"]: float(e["qty"]) for e in expected_lines}
    found = [c for c in exp if c in got]
    within = []
    off = []
    for c in found:
        e = exp[c]
        err = abs(got[c] - e) / e if e else (0.0 if got[c] == 0 else 1.0)
        if err <= tol:
            within.append(c)
        else:
            off.append({"item_code": c, "expected": e, "got": round(got[c], 3), "error_pct": round(err * 100, 1)})
    coverage = len(found) / len(exp) if exp else 0.0
    precision = len(within) / len(found) if found else 0.0
    composite = (coverage ** 0.4) * (precision ** 0.6) if found else 0.0
    return LedgerScore(round(coverage, 4), round(precision, 4), round(composite, 4), tol, len(exp), len(found), len(within),
                       missing=sorted(set(exp) - set(got)), off_tolerance=off, extra=sorted(set(got) - set(exp)))


@dataclass
class RomScore:
    case: str
    actual_total: float
    low: float
    target: float
    high: float
    inside_band: bool
    target_error_pct: float
    aace_class: int
    accuracy_band: str


def score_rom(case: str, three_point: dict, actual_total: float, aace_class: int, band: str) -> RomScore:
    lo, tg, hi = three_point["low"]["total"], three_point["target"]["total"], three_point["high"]["total"]
    return RomScore(case, actual_total, lo, tg, hi, lo <= actual_total <= hi, round((tg - actual_total) / actual_total * 100, 1) if actual_total else 0.0, aace_class, band)


def eval_detailed_set(vault_root: Path, package_dir: Path, runs: int = 1, tol: float = 0.25, reader_json: Path | None = None) -> dict:
    """Run the seed takeoff (plus optional reader lines) `runs` times and score each against ground_truth.json."""
    from core.estimating import pipeline

    gt = json.loads((package_dir / "ground_truth.json").read_text(encoding="utf-8"))
    expected = gt.get("expected_lines") or []
    if not expected:
        raise ValueError("ground_truth.json has no expected_lines — regenerate the fixture or add them")
    scores = []
    for i in range(runs):
        folder = pipeline.intake(vault_root, package_dir, f"eval-{package_dir.name}-{i + 1}", gt.get("building_type", "office-warehouse"), gt.get("city", "Plano"), 2)
        pipeline.seed_takeoff(folder)
        if reader_json:
            pipeline.merge_reader_lines(folder, reader_json)
        items = json.loads((folder / "04-takeoff-ledger.json").read_text(encoding="utf-8"))
        scores.append(score_ledger(items, expected, tol))
    comp = [s.composite for s in scores]
    return {"set": package_dir.name, "kind": "detailed", "runs": runs, "tol": tol, "scores": [asdict(s) for s in scores],
            "composite_mean": round(statistics.mean(comp), 4), "composite_spread": round((max(comp) - min(comp)), 4),
            "coverage_mean": round(statistics.mean(s.coverage for s in scores), 4), "precision_mean": round(statistics.mean(s.precision_at_tol for s in scores), 4)}


def eval_rom_set(vault_root: Path, set_dir: Path, runs: int = 1) -> dict:
    """Each case folder holds intake.json and actual.json ({"actual_total": N})."""
    from core.estimating import pipeline

    cases = sorted(p for p in set_dir.iterdir() if p.is_dir() and (p / "intake.json").exists())
    if not cases:
        raise ValueError(f"no ROM cases under {set_dir} (need <case>/intake.json + actual.json)")
    results = []
    for case in cases:
        intake = json.loads((case / "intake.json").read_text(encoding="utf-8"))
        actual = float(json.loads((case / "actual.json").read_text(encoding="utf-8"))["actual_total"])
        for i in range(runs):
            intake_i = dict(intake) | {"name": f"eval-{case.name}-{i + 1}"}
            folder = pipeline.rom(vault_root, intake_i)
            est = json.loads((folder / "06-estimate.json").read_text(encoding="utf-8"))
            results.append(asdict(score_rom(case.name, est["meta"]["three_point"], actual, est["meta"]["aace_class"], est["meta"]["accuracy_band"])))
    inside = sum(1 for r in results if r["inside_band"])
    return {"set": set_dir.name, "kind": "rom", "runs": runs, "cases": len(cases), "results": results,
            "band_hit_rate": round(inside / len(results), 4) if results else 0.0,
            "target_error_mean_pct": round(statistics.mean(abs(r["target_error_pct"]) for r in results), 1) if results else 0.0}


def eval_markdown(res: dict) -> str:
    out = ["---", "type: eval_report", f"set: {res['set']}", f"kind: {res['kind']}", f"generated: {datetime.now().isoformat(timespec='seconds')}", "---",
           f"# Eval — {res['set']} ({res['kind']}, {res['runs']} run(s))", ""]
    if res["kind"] == "detailed":
        out += [f"**Composite {res['composite_mean']:.3f}** (spread {res['composite_spread']:.3f}) · coverage {res['coverage_mean']:.3f} · precision@{int(res['tol'] * 100)}% {res['precision_mean']:.3f}", "",
                "Reference points: human estimators 0.776, Handoff-H1 0.816, best raw frontier model ≈ 0.61 (TakeoffBench-v1, residential).", ""]
        s = res["scores"][0]
        if s["missing"]:
            out += ["## Missing item codes", *[f"- {m}" for m in s["missing"]], ""]
        if s["off_tolerance"]:
            out += ["## Off tolerance", "| Item | Expected | Got | Error % |", "|---|---|---|---|", *[f"| {o['item_code']} | {o['expected']:g} | {o['got']:g} | {o['error_pct']} |" for o in s["off_tolerance"]], ""]
        if s["extra"]:
            out += [f"Extra codes not in ground truth (not penalized): {', '.join(s['extra'][:30])}", ""]
    else:
        out += [f"**Band hit-rate {res['band_hit_rate']:.0%}** over {res['cases']} case(s) × {res['runs']} run(s) · mean |target error| {res['target_error_mean_pct']}%", "",
                "| Case | Actual | Low | Target | High | Inside | Target error % |", "|---|---|---|---|---|---|---|"]
        out += [f"| {r['case']} | ${r['actual_total']:,.0f} | ${r['low']:,.0f} | ${r['target']:,.0f} | ${r['high']:,.0f} | {'yes' if r['inside_band'] else 'NO'} | {r['target_error_pct']} |" for r in res["results"]]
        out.append("")
    return "\n".join(out)


def run_eval(vault_root: Path, set_dir: Path, runs: int = 1, tol: float = 0.25, out_dir: Path | None = None) -> tuple[dict, Path]:
    set_dir = Path(set_dir)
    scratch = Path(vault_root) / ".cache" / "evals"
    scratch.mkdir(parents=True, exist_ok=True)
    work = scratch / f"work-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    work.mkdir()
    (work / "00-Brain").symlink_to(Path(vault_root) / "00-Brain") if (Path(vault_root) / "00-Brain").exists() else None
    try:
        res = eval_detailed_set(work, set_dir, runs, tol) if (set_dir / "ground_truth.json").exists() else eval_rom_set(work, set_dir, runs)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    out_dir = out_dir or (Path(vault_root) / "03-Outputs" / "evals")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    (out_dir / f"{stamp}-{set_dir.name}.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    md = out_dir / f"{stamp}-{set_dir.name}.md"
    md.write_text(eval_markdown(res), encoding="utf-8")
    return res, md
