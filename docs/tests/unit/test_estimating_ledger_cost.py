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


def test_pricing_basis_and_three_point_ranges(tmp_path):
    from core.estimating.cost_engine import three_point_totals

    byo = tmp_path / "buyouts.csv"
    byo.write_text(
        "item_code,description,unit,labor,material,equipment,sub,source,quote_date,valid_until,location,notes,pricing_basis,unit_low,unit_high\n"
        "08-hm-door-single,HM door (our buyouts),EA,0,0,0,1500,buyouts-2025.csv#row-41,2026-05-02,2027-05-01,Dallas,,historical,1350,1800\n"
        "23-hood-type1-per-lf,Type I hood per LF,LF,0,0,0,1800,playbook restaurant-ti v1.0,2026-09-01,,national,[UNCERTAIN],assembly,1450,2400\n",
        encoding="utf-8",
    )
    lib = load_library([byo, SEED_LIBRARY])
    assert lib["08-hm-door-single"].pricing_basis == "historical" and lib["08-hm-door-single"].source.startswith("buyouts")   # BYO wins over seed
    assert lib["03-sog-6in"].pricing_basis == "seed_placeholder" and lib["03-sog-6in"].uncertain
    led = Ledger()
    led.add("08", "08-hm-door-single", "HM door", 10, "EA", "A-601", "schedule", "03-architectural")
    led.add("23", "23-hood-type1-per-lf", "Hood", 12, "LF", "intake", "derived", "04-mep", confidence=0.5)
    led.add("10", "10-x-allowance", "Signage allowance", 1, "LS", "Project Manual", "allowance", "01-bid-coordination", pricing_basis="allowance")
    lines = {ln.item_code: ln for ln in price_ledger(led, lib, location_factor=0.88, as_of=date(2026, 9, 12))}
    door = lines["08-hm-door-single"]
    assert door.pricing_basis == "historical" and door.total == 15_000 and door.low == 13_500 and door.high == 18_000
    hood = lines["23-hood-type1-per-lf"]
    assert hood.pricing_basis == "assembly" and "UNCERTAIN" in hood.flags and hood.low == pytest.approx(12 * 1450) and hood.high == pytest.approx(12 * 2400)
    assert lines["10-x-allowance"].pricing_basis == "allowance" and "UNPRICED" in lines["10-x-allowance"].flags   # no row, no amount → honest
    tp = three_point_totals(list(lines.values()), 0, 0, MarkupPolicy(0, 0, 0, 0, 0, tax_pct=0))
    assert tp["low"]["total"] < tp["target"]["total"] < tp["high"]["total"] and tp["spread_pct"] > 0
    assert any("unknown pricing_basis" in p for p in Ledger().__class__().items) is False
    bad = Ledger()
    bad.add("08", "x", "x", 1, "EA", "A-1", "manual", "03-architectural", pricing_basis="guess")
    assert any("unknown pricing_basis" in p for p in bad.validate())


def _led():
    from core.estimating.takeoff_ledger import Ledger
    return Ledger()


def test_reconcile_identity_matches_across_tag_keys_and_sheets():
    led = _led()
    led.add("08", "08-hm-door-single", "HM door 102", 1, "EA", "A-601", "schedule", "03", tags={"mark": "102", "type": "HM"})
    led.add("08", "08-hm-door-single", "HM door 102 seen on plan", 1, "EA", "A-101", "vision", "03", tags={"mark": "102", "room": "102"}, confidence=0.8)
    led.add("23", "23-rtu-7-5-ton", "RTU-1", 1, "EA", "M-101", "schedule", "04", tags={"tag": "RTU-1"})
    led.add("23", "23-rtu-7-5-ton", "RTU-1 on roof plan", 1, "EA", "M-101 rev 2", "vision", "04", tags={"mark": "rtu-1"})
    disc = led.reconcile()
    assert disc == []
    assert [(i.item_code, i.method, i.qty) for i in led.items] == [("08-hm-door-single", "schedule", 1.0), ("23-rtu-7-5-ton", "schedule", 1.0)]
    assert "confirmed by vision" in led.items[0].notes and led.items[0].confidence > 0.8


def test_reconcile_untagged_totals_collapse_and_disagreements_are_logged():
    led = _led()
    led.add("03", "03-sog-4in", "4in slab on grade", 4000, "SF", "S-101", "derived", "02", confidence=0.6)
    led.add("03", "03-sog-4in", "4in SOG office bay", 4000, "SF", "S-101", "vision", "02", confidence=0.8)          # agrees → vision governs over derived
    led.add("05", "05-metal-deck", "Metal deck (from schedule)", 12000, "SF", "S-201", "schedule", "02")
    led.add("05", "05-metal-deck", "Deck — warehouse", 8000, "SF", "S-201", "vision", "02", confidence=0.8)
    led.add("05", "05-metal-deck", "Deck — office", 4000, "SF", "S-201", "vision", "02", confidence=0.8)               # 8000+4000 = 12000 agrees → schedule kept, both vision lines dropped
    led.add("09", "09-partition-p1", "Partitions from room perimeters", 4000, "SF", "A-101", "derived", "03", confidence=0.5)
    led.add("09", "09-partition-p1", "Partitions measured on tiles", 4900, "SF", "A-101", "vision", "03", confidence=0.6)  # 22% apart → vision governs, discrepancy logged
    led.add("05", "05-misc-metals", "Lintels", 1, "LS", "S-201", "vision", "02")
    led.add("05", "05-misc-metals", "Bollards", 1, "LS", "S-201", "vision", "02")                                        # same method twice: never merged
    disc = led.reconcile()
    got = {(i.item_code, i.method): i.qty for i in led.items}
    assert got[("03-sog-4in", "vision")] == 4000 and ("03-sog-4in", "derived") not in got
    assert got[("05-metal-deck", "schedule")] == 12000 and ("05-metal-deck", "vision") not in got
    assert got[("09-partition-p1", "vision")] == 4900 and ("09-partition-p1", "derived") not in got
    assert sum(1 for i in led.items if i.item_code == "05-misc-metals") == 2
    assert [(d.item_code, d.a_method, d.b_method, d.delta_pct) for d in disc] == [("09-partition-p1", "vision", "derived", 18.4)]   # delta relative to the governing quantity
    assert sum(i.qty for i in led.items if i.item_code == "05-metal-deck") == 12000      # no double count


def test_reconcile_pass_b_spans_sheets_and_identity_mismatches():
    led = _led()
    led.add("26", "26-troffer-led-2x4", "2x4 troffer type A", 40, "EA", "E-101", "schedule", "04", tags={"type": "A"})
    led.add("26", "26-troffer-led-2x4", "2x4 troffer (type A) on plan", 40, "EA", "E-101", "vision", "04", tags={"mark": "A"}, confidence=0.7)
    led.add("08", "08-hm-door-single", "HM door 102", 1, "EA", "A-601", "schedule", "03", tags={"mark": "102"})
    led.add("08", "08-hm-door-single", "HM door 103", 1, "EA", "A-601", "schedule", "03", tags={"mark": "103"})
    led.add("08", "08-hm-door-single", "HM single doors counted on the plan", 3, "EA", "A-101", "vision", "03", confidence=0.7)   # 3 vs 2 → 50% apart → logged, schedule kept
    disc = led.reconcile()
    got = [(i.item_code, i.method, i.qty) for i in led.items]
    assert got == [("26-troffer-led-2x4", "schedule", 40.0), ("08-hm-door-single", "schedule", 1.0), ("08-hm-door-single", "schedule", 1.0)]
    assert [(d.item_code, d.a_qty, d.b_qty, d.delta_pct) for d in disc] == [("08-hm-door-single", 2.0, 3.0, 50.0)]


def test_normalize_sheet_ids():
    from core.estimating.pipeline import normalize_sheet
    ids = ["E-101", "A-101", "A-601", "S-101"]
    assert normalize_sheet("E-101 rev 2", ids) == ("E-101", "2")
    assert normalize_sheet("A-101 (tile r0c1)", ids) == ("A-101", None)
    assert normalize_sheet("a-601", ids) == ("A-601", None)
    assert normalize_sheet("A-1011", ids) == ("A-1011", None)          # not a prefix match on a different sheet
    assert normalize_sheet("Project-Manual", ids) == ("Project-Manual", None)
