"""Extractors against the synthetic bid package (docs/tests/fixtures/sample-set-prairie-creek).

Every expected value comes from ground_truth.json, which the generator wrote from the same numbers
it drew — so a failure here is an extractor regression, never a fixture opinion.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from core.estimating import sheet_geometry, sheet_register, sheet_tables, sheet_text, spec_index
from core.estimating.pdfio import open_pdf, parse_scale, sheet_size_name

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "sample-set-prairie-creek"
GT = json.loads((FIX / "ground_truth.json").read_text(encoding="utf-8"))
DRAWINGS = sorted(p for p in FIX.glob("*.pdf") if p.name != "Project-Manual.pdf")


@pytest.fixture(scope="module")
def register():
    return {s.sheet_id: s for s in sheet_register.build_register(DRAWINGS)}


def test_parse_scale_variants():
    s = parse_scale('SCALE: 1/8" = 1\'-0"')
    assert s and abs(s.pt_per_ft - 9.0) < 1e-6
    assert parse_scale('1/4"=1\'-0"').pt_per_ft == pytest.approx(18.0)
    assert parse_scale('3/32" = 1\'-0"').pt_per_ft == pytest.approx(6.75)
    assert parse_scale('1" = 20\'').pt_per_ft == pytest.approx(3.6)
    assert parse_scale("SCALE: NONE") is None
    assert sheet_size_name(36, 24) == "ARCH D" and sheet_size_name(30, 42) == "ARCH E1"


def test_register_covers_every_sheet_with_discipline_scale_and_revision(register):
    assert set(register) == set(GT["sheets"])
    for sid, s in register.items():
        assert s.is_vector and s.size_name == "ARCH D" and s.revision == "2" and s.date == "09/12/2026"
    assert register["A-101"].scale_label == '1/8" = 1\'-0"' and register["A-101"].sheet_type == "plans"
    assert register["A-101"].reader_department == "03-architectural"
    assert register["S-101"].reader_department == "02-civil-structural" and register["E-101"].reader_department == "04-mep"
    assert register["A-601"].scale_label is None and register["A-601"].not_to_scale
    assert register["G-001"].title.startswith("COVER SHEET")


def test_register_markdown_flags_scale_gate(register):
    md = sheet_register.register_markdown(list(register.values()))
    assert "Scale gate: 0 measured-type sheet(s)" in md
    assert "| **A-101** | FLOOR PLAN |" in md


def test_room_tags_match_ground_truth():
    with open_pdf(FIX / "A-101.pdf") as pdf:
        tags = sheet_text.room_tags(sheet_text.words(pdf.pages[0]))
    got = {t.number: (t.name, t.area_sf) for t in tags}
    for r in GT["rooms"]:
        assert got[r["number"]] == (r["name"], float(r["area_sf"])), r


def test_dimension_strings_and_notes():
    with open_pdf(FIX / "A-101.pdf") as pdf:
        ws = sheet_text.words(pdf.pages[0])
        texts = {d.text for d in sheet_text.dimension_strings(ws)}
    assert {"120'-0\"", "40'-0\"", "80'-0\""} <= texts
    with open_pdf(FIX / "S-101.pdf") as pdf:
        lines = sheet_text.text_lines(sheet_text.words(pdf.pages[0]))
        notes = sheet_text.notes_blocks(lines)
    assert len(notes["STRUCTURAL GENERAL NOTES"]) == 8
    assert notes["STRUCTURAL GENERAL NOTES"][1].startswith("CONCRETE: f'c = 4,000 PSI")


def test_door_and_window_candidates_match_ground_truth(register):
    with open_pdf(FIX / "A-101.pdf") as pdf:
        g = sheet_geometry.summarize(pdf.pages[0], register["A-101"].scale)
    assert len(g.doors) == GT["door_count"]
    assert all(d.leaf_found for d in g.doors)
    assert sorted(round(d.width_ft) for d in g.doors) == [3] * 11 + [6]
    assert len(g.windows) == GT["window_count"]
    assert g.exterior_perimeter_ft == pytest.approx(GT["exterior_wall_lf"], abs=0.5)
    assert g.footprint_sf == pytest.approx(GT["gross_sf"], abs=5)


def test_schedules_extract_with_headers_and_rows():
    with open_pdf(FIX / "A-601.pdf") as pdf:
        p = pdf.pages[0]
        ws = sheet_text.words(p)
        lines = sheet_text.text_lines(ws)
        scheds = {s.kind: s for s in sheet_tables.extract_schedules(p, ws, lines)}
    door = scheds["door"]
    assert door.headers == ["MARK", "SIZE", "TYPE", "FRAME", "RATING", "HARDWARE SET"]
    assert [r[0] for r in door.rows] == GT["door_marks"] + GT["overhead_doors"]
    assert scheds["window"].rows[0][-1] == str(GT["window_count"])
    assert len(scheds["finish"].rows) == len(GT["rooms"])
    with open_pdf(FIX / "S-101.pdf") as pdf:
        p = pdf.pages[0]
        ws = sheet_text.words(p)
        lines = sheet_text.text_lines(ws)
        foot = [s for s in sheet_tables.extract_schedules(p, ws, lines) if s.kind == "footing"][0]
    assert foot.rows[0][0] == "F1" and foot.rows[0][-1] == "9"


def test_spec_index_sections_and_division_01_items():
    idx = spec_index.index_manual(FIX / "Project-Manual.pdf")
    numbers = {s.number for s in idx.sections}
    assert {"00 21 13", "01 21 00", "01 23 00", "03 30 00", "26 51 00", "31 23 00"} <= numbers
    assert len(numbers) == 27
    texts = spec_index.page_texts(FIX / "Project-Manual.pdf")
    d01 = spec_index.division_01_summary(texts)
    assert d01["bid_due"][0]["groups"][0] == GT["spec"]["bid_due"]
    assert d01["rfi_cutoff"][0]["groups"][0] == GT["spec"]["rfi_cutoff"]
    assert d01["duration"][0]["groups"][0] == str(GT["spec"]["duration_days"])
    assert d01["bid_bond"][0]["groups"][0] == str(GT["spec"]["bid_bond_pct"])
    assert any("signage" in h["match"] for h in d01["allowances"])
    assert len(d01["alternates"]) == GT["spec"]["alternates"]
