from __future__ import annotations

from datetime import date

import pytest
from core.estimating.cost_engine import (
    SEED_LIBRARY,
    CostRow,
    MarkupPolicy,
    benchmark_check,
    general_conditions,
    load_library,
    load_location_factor,
    markup_stack,
    price_ledger,
    summary_by_division,
)
from core.estimating.review_gates import run_gates, verdict
from core.estimating.takeoff_ledger import Ledger, normalize_unit


def _ledger() -> Ledger:
    led = Ledger()
    led.add("08", "08-hm-door-single", "HM door single", 9, "EA", "A-601", "schedule", "03-architectural", revision="2")
    led.add("08", "08-hm-door-single", "HM door single", 12, "EA", "A-601", "vector", "03-architectural")
    led.add("03", "03-sog-6in", "6in slab on grade", 8000, "SF", "S-101", "derived", "02-civil-structural", waste_pct=4, confidence=0.5)
    led.add("99", "99-nothing", "Unknown thing", 1, "LS", "X-001", "manual", "01-bid-coordination")
    return led


def test_units_normalize_and_validate():
    assert normalize_unit("sq ft") == "SF" and normalize_unit("each") == "EA" and normalize_unit("lbs") == "LB"
    led = _ledger()
    problems = led.validate()
    assert any("99-nothing" not in p and "unusual" in p for p in problems) is False  # 99 has no unit table → no complaint
    led.add("03", "03-x", "bad unit", 1, "EA", "S-101", "schedule", "02-civil-structural")
    assert any("unusual for division 03" in p for p in led.validate()) is False  # EA is allowed in 03
    led.add("08", "08-y", "bad unit", 1, "CY", "A-601", "schedule", "03-architectural")
    assert any("unusual for division 08" in p for p in led.validate())


def test_reconcile_prefers_schedule_and_records_discrepancy():
    led = _ledger()
    disc = led.reconcile(tolerance_pct=10)
    kept = [i for i in led.items if i.item_code == "08-hm-door-single"]
    assert len(kept) == 1 and kept[0].method == "schedule" and kept[0].qty == 9
    assert len(disc) == 1 and disc[0].a_method == "schedule" and disc[0].b_qty == 12 and disc[0].delta_pct == pytest.approx(33.3)


def test_waste_applies_after_net_takeoff():
    led = _ledger()
    slab = [i for i in led.items if i.item_code == "03-sog-6in"][0]
    assert slab.qty_with_waste == pytest.approx(8320.0)


def test_price_ledger_marks_unpriced_uncertain_and_applies_location_factor():
    led = _ledger()
    led.reconcile()
    lib = load_library([SEED_LIBRARY])
    lines = price_ledger(led, lib, location_factor=0.88, as_of=date(2026, 9, 12))
    by = {ln.item_code: ln for ln in lines}
    assert "UNPRICED" in by["99-nothing"].flags and by["99-nothing"].total == 0
    assert "UNCERTAIN" in by["08-hm-door-single"].flags
    assert by["08-hm-door-single"].total == pytest.approx(9 * 1650.0)          # sub quotes are not location-factored
    slab = by["03-sog-6in"]
    assert slab.unit_labor == pytest.approx(2.60 * 0.88) and slab.total == pytest.approx(8320 * (2.60 + 3.75 + 0.35) * 0.88, rel=1e-6)
    assert "LOW-CONFIDENCE" in slab.flags


def test_stale_quote_flag():
    lib = {"x": CostRow("x", "thing", "EA", 0, 0, 0, 100, "quote", "2026-01-01", "2026-06-30")}
    led = Ledger()
    led.add("10", "x", "thing", 2, "EA", "A-101", "schedule", "03-architectural")
    ln = price_ledger(led, lib, as_of=date(2026, 9, 12))[0]
    assert "STALE-QUOTE" in ln.flags and ln.total == 200


def test_markup_stack_order_and_texas_tax_basis():
    pol = MarkupPolicy(contingency_pct=3, escalation_pct=2, insurance_pct=1.2, bond_pct=0.9, fee_pct=5, tax_pct=8.25, tax_basis="materials")
    ms = {m.name: m for m in markup_stack(1_000_000, 300_000, 100_000, pol)}
    assert ms["Contingency"].amount == pytest.approx(33_000)
    assert ms["Escalation"].amount == pytest.approx(1_133_000 * 0.02)
    assert ms["Sales tax on materials"].amount == pytest.approx(300_000 * 0.0825)
    total = ms["TOTAL BID"].amount
    pol2 = MarkupPolicy(3, 2, 1.2, 0.9, 5, tax_basis="none")
    assert markup_stack(1_000_000, 300_000, 100_000, pol2)[-1].amount < total


def test_general_conditions_duration_driven():
    gcs = general_conditions(8, staff=[("Superintendent", 1, 15500)], temp_items=[("Toilets", 2, "MO", 210), ("Dumpsters", 16, "EA", 650)], other=[("Survey", 9500, "LS")])
    totals = {g.name: g.total for g in gcs}
    assert totals["Superintendent"] == 124_000 and totals["Toilets"] == 3_360 and totals["Dumpsters"] == 10_400 and totals["Survey"] == 9_500


def test_summary_benchmark_and_gates_end_to_end():
    led = _ledger()
    led.reconcile()
    lib = load_library([SEED_LIBRARY])
    lines = price_ledger(led, lib, location_factor=1.0)
    summary = summary_by_division(lines, 12000, {"03": "Concrete", "08": "Openings"})
    assert sum(r["pct"] for r in summary) == pytest.approx(100.0, abs=0.2)
    bm = benchmark_check(2_400_000, 12000, "office-warehouse", 200_000, 2_000_000, 600_000)
    assert bm["per_sf"] == 200.0 and bm["checks"][0]["status"] == "inside"
    factor, src = load_location_factor("Plano")
    assert factor == 0.88 and "UNCERTAIN" in src
    register = [{"sheet_id": "A-601", "sheet_type": "schedules and diagrams", "scale_label": None},
                {"sheet_id": "S-101", "sheet_type": "plans", "scale_label": '1/8" = 1\'-0"'},
                {"sheet_id": "A-101", "sheet_type": "plans", "scale_label": '1/8" = 1\'-0"'}]
    gates = run_gates(register, [i.__dict__ for i in led.items], [ln.to_dict() for ln in lines], summary,
                      [{"division": "03"}, {"division": "08"}, {"division": "26"}], [{"text": "q", "severity": "CRITICAL"}], bm, 12000)
    by = {g.id: g for g in gates}
    assert not by["G1"].passed and "A-101" in by["G1"].evidence           # A-101 never claimed
    assert not by["G3"].passed and by["G3"].evidence == ["26"]             # spec division 26 has no lines
    assert by["G4"].passed and by["G5"].passed and not by["G7"].passed
    assert verdict(gates) == "REVISE"
