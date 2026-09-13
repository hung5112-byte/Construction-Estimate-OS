"""The estimating pipeline — stages, folders, files.

02-Estimates/<timestamp>-<slug>/
  package/            copied PDFs (drawings + specifications)
  00-project-profile.md/.json
  01-sheet-register.md/.json
  02-spec-index.md/.json        + 02-division-01.json
  cards/<sheet>.md              shadow card per sheet (text, tables, geometry, notes) for the readers
  renders/                      overview + tiles per sheet (optional)
  03-sheets.json                per-sheet extraction (schedules, room tags, geometry) — machine input
  03-takeoff-seed.json          deterministic seed takeoff (schedule + vector + derived lines)
  04-takeoff-ledger.md/.json    consolidated ledger (readers' lines merge here in the harness path)
  04-discrepancies.json
  05-clarification.md/.json     ⏸ PAUSE — the Chief Estimator answers
  06-estimate.md/.json          priced estimate, GCs, markups, summary, benchmark
  07-review-scorecard.md/.json  gates (+ judged review when agents ran)
  08-estimate-report.md         ⏹ STOP 1
  03-Outputs/<folder>/          estimate-workbook.xlsx · basis-of-estimate.docx (on approve)
"""
from __future__ import annotations

import json
import re
import shutil
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from core.estimating import sheet_geometry, sheet_register, sheet_tables, sheet_text, spec_index
from core.estimating.cost_engine import (
    DATA_DIR,
    SEED_DISCLAIMER,
    MarkupPolicy,
    benchmark_check,
    estimate_json,
    general_conditions,
    library_paths,
    load_library,
    load_location_factor,
    markup_stack,
    price_ledger,
    summary_by_division,
)
from core.estimating.cost_engine import three_point_totals
from core.estimating.proposal import findings_markdown, proposal_markdown
from core.estimating.rfi import build_rom_questions
from core.estimating.pdfio import open_pdf
from core.estimating.report import report_markdown, write_basis_of_estimate_docx
from core.estimating.review_gates import run_gates, scorecard_markdown, verdict
from core.estimating.rfi import apply_answers, auto_assume_all, build_questions, write_questions
from core.estimating.takeoff_ledger import Ledger, load_waste_factors
from core.estimating.workbook import write_workbook

ESTIMATES_DIR = "02-Estimates"
# AACE 56R-08 (building/general construction) expected accuracy at 80% confidence, after contingency
ACCURACY_BANDS = {5: "−30% / +50%", 4: "−20% / +30%", 3: "−15% / +20%", 2: "−10% / +15%", 1: "−5% / +10%"}


def _slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:50] or "estimate"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass
class Profile:
    name: str
    slug: str
    building_type: str
    city: str
    aace_class: int = 2
    accuracy_band: str = ""
    gross_sf: float = 0.0
    stories: int = 1
    delivery: str = "hard-bid"
    bid_due: str = ""
    rfi_cutoff: str = ""
    duration_days: int = 0
    heights_ft: list[float] = field(default_factory=list)
    areas: dict = field(default_factory=dict)      # e.g. {"OFFICE AREA": 4000, "WAREHOUSE AREA": 8000}
    drawings: list[str] = field(default_factory=list)
    specs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    exclusions: dict = field(default_factory=dict)   # division → reason (cited), e.g. {"31": "site work by separate contract (01 10 00 p5)"}
    exclusion_texts: list[str] = field(default_factory=list)   # client-facing exclusions (playbook + risk mitigations)
    playbook: dict = field(default_factory=dict)               # {project_type, version, status} when a ROM playbook drove the estimate
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ------------------------------------------------------------------------------------------ S0 intake
def create_folder(vault_root: Path, name: str) -> Path:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M")
    folder = Path(vault_root) / ESTIMATES_DIR / f"{ts}-{_slug(name)}"
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def _sf(v: str) -> float | None:
    m = re.search(r"([\d,]+)\s*SF", v or "", re.IGNORECASE)
    return float(m.group(1).replace(",", "")) if m else None


def _profile_from_code_summary(sheets: list[dict], profile: Profile) -> None:
    for sh in sheets:
        for sc in sh.get("schedules", []):
            if sc["kind"] != "code":
                continue
            for row in sc["rows"]:
                if len(row) < 2:
                    continue
                key, val = row[0].strip().upper(), row[1]
                sf = _sf(val)
                if key == "GROSS AREA" and sf and not profile.gross_sf:
                    profile.gross_sf = sf
                elif key.endswith("AREA") and sf:
                    profile.areas[key] = sf
                elif key == "STORIES" and val.strip().isdigit():
                    profile.stories = int(val.strip())
                elif key == "HEIGHT":
                    profile.heights_ft = [float(h) for h in re.findall(r"(\d+)'", val)]


def extract_sheet(pdf_path: Path, page_index: int, info: sheet_register.SheetInfo) -> dict:
    with open_pdf(pdf_path) as pdf:
        page = pdf.pages[page_index]
        ws = sheet_text.words(page)
        lines = sheet_text.text_lines(ws)
        tags = sheet_text.room_tags(ws)
        dims = sheet_text.dimension_strings(ws)
        notes = sheet_text.notes_blocks(lines)
        scheds = sheet_tables.extract_schedules(page, ws, lines)
        scale = info.scale
        geo = sheet_geometry.summarize(page, scale) if info.sheet_type in ("plans", "elevations", "sections") else None
        card = sheet_text.shadow_card(info.sheet_id, info.title, scale, lines, tags, dims, notes, sheet_tables.schedules_markdown(scheds))
        if geo:
            card += ("\n## Vector geometry (candidates — confirm on the tiles)\n"
                     f"- Door swing candidates: {len(geo.doors)} (widths ft: {sorted(round(d.width_ft or 0, 1) for d in geo.doors)})\n"
                     f"- Window candidates: {len(geo.windows)}\n- Exterior perimeter: {geo.exterior_perimeter_ft:.0f} LF · footprint {geo.footprint_sf:,.0f} SF\n"
                     if geo.exterior_perimeter_ft else f"- Door swing candidates: {len(geo.doors)} · window candidates: {len(geo.windows)}\n")
    return {
        "sheet_id": info.sheet_id, "title": info.title, "discipline": info.discipline, "sheet_type": info.sheet_type,
        "scale_label": info.scale_label, "pt_per_ft": info.pt_per_ft, "revision": info.revision, "file": info.file, "page_index": page_index,
        "room_tags": [asdict(t) for t in tags], "dimension_strings": sorted({d.text for d in dims}), "notes": notes,
        "text_lines": [ln.text for ln in lines][:600],
        "schedules": [s.to_dict() for s in scheds],
        "geometry": (geo.to_dict() | {"doors": [asdict(d) for d in geo.doors], "windows": [asdict(w) for w in geo.windows]}) if geo else None,
        "card": card,
    }


def intake(vault_root: Path, package_dir: Path, name: str, building_type: str, city: str, aace_class: int = 2,
           gross_sf: float | None = None, render: bool = False) -> Path:
    vault_root, package_dir = Path(vault_root), Path(package_dir)
    folder = create_folder(vault_root, name)
    pkg = folder / "package"
    pkg.mkdir()
    pdfs = sorted(p for p in package_dir.glob("*.pdf"))
    drawings, specs = [], []
    for p in pdfs:
        shutil.copy2(p, pkg / p.name)
        (specs if re.search(r"manual|spec", p.name, re.IGNORECASE) else drawings).append(p.name)
    profile = Profile(name=name, slug=folder.name, building_type=building_type, city=city, aace_class=aace_class,
                      gross_sf=float(gross_sf or 0), drawings=drawings, specs=specs)
    # register
    register = sheet_register.build_register([pkg / d for d in drawings])
    index_ids: list[str] = []
    sheets: list[dict] = []
    for info in register:
        sh = extract_sheet(pkg / info.file, info.page_index, info)
        sheets.append(sh)
        _write(folder / "cards" / f"{info.sheet_id}.md", sh["card"])
        for sc in sh["schedules"]:
            if sc["kind"] == "index":
                index_ids.extend(r[0] for r in sc["rows"] if r)
    comp = sheet_register.completeness(register, index_ids) if index_ids else None
    _write(folder / "01-sheet-register.md", sheet_register.register_markdown(register, comp))
    _write(folder / "01-sheet-register.json", sheet_register.register_json(register))
    _write(folder / "03-sheets.json", json.dumps([{k: v for k, v in sh.items() if k != "card"} for sh in sheets], indent=2))
    # specs
    div01: dict = {}
    if specs:
        texts = spec_index.page_texts(pkg / specs[0])
        idx = spec_index.index_manual(pkg / specs[0], texts)
        div01 = spec_index.division_01_summary(texts)
        _write(folder / "02-spec-index.md", spec_index.spec_index_markdown(idx, div01))
        _write(folder / "02-spec-index.json", idx.to_json())
        _write(folder / "02-division-01.json", json.dumps(div01, indent=2))
        if div01.get("bid_due"):
            profile.bid_due = div01["bid_due"][0]["groups"][0]
        if div01.get("rfi_cutoff"):
            profile.rfi_cutoff = div01["rfi_cutoff"][0]["groups"][0]
        if div01.get("duration"):
            profile.duration_days = int(div01["duration"][0]["groups"][0])
        for h in div01.get("separate_contract", []) + div01.get("not_in_contract", []):
            m = h["match"].lower()
            if re.search(r"site ?work|civil|paving|grading|utilities beyond", m):
                for d in ("31", "32", "33"):
                    profile.exclusions.setdefault(d, f"{h['match'][:90]} (Project Manual p{h['page']})")
            if re.search(r"low-voltage cabling|cabling", m):
                profile.exclusions.setdefault("27-cabling", f"{h['match'][:90]} (Project Manual p{h['page']})")
    else:
        _write(folder / "02-spec-index.json", json.dumps({"file": None, "pages": 0, "sections": []}))
        _write(folder / "02-division-01.json", "{}")
    _profile_from_code_summary(sheets, profile)
    profile.accuracy_band = ACCURACY_BANDS.get(int(profile.aace_class), "")
    if not profile.gross_sf:
        profile.gross_sf = sum(t["area_sf"] or 0 for sh in sheets for t in sh["room_tags"])
    _write(folder / "00-project-profile.json", json.dumps(profile.to_dict(), indent=2))
    _write(folder / "00-project-profile.md", _profile_md(profile, register, comp))
    if render:
        from core.estimating.sheet_render import render_overview, render_tiles

        for info in register:
            render_overview(pkg / info.file, info.page_index, folder / "renders")
            if info.sheet_type in ("plans", "elevations", "sections"):
                render_tiles(pkg / info.file, info.page_index, folder / "renders")
    return folder


def _profile_md(p: Profile, register, comp) -> str:
    out = ["---", "type: project_profile", f"aace_class: {p.aace_class}", f"building_type: {p.building_type}", "---",
           f"# Project profile — {p.name}", "",
           f"- Building type: {p.building_type} · {p.gross_sf:,.0f} SF · {p.stories} story · {p.city}",
           f"- Delivery: {p.delivery} · AACE class {p.aace_class} (expected accuracy {p.accuracy_band or ACCURACY_BANDS.get(int(p.aace_class), '?')})",
           f"- Bid due: {p.bid_due or 'not found'} · RFI cutoff: {p.rfi_cutoff or 'not found'} · Duration: {p.duration_days or '?'} calendar days",
           f"- Areas from code summary: {p.areas}" if p.areas else "- Areas: from room tags",
           f"- Heights: {p.heights_ft} ft" if p.heights_ft else "",
           f"- Drawings: {len(p.drawings)} file(s), {len(register)} sheet(s) · Specifications: {', '.join(p.specs) or 'none'}", ""]
    if comp:
        out.append(f"- Index completeness: missing {comp['missing_from_package'] or 'none'} · not in index {comp['not_in_index'] or 'none'}")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------------------- S1/S2 takeoff
_FT_RE = re.compile(r"(\d+)'-(\d+)\"")


def _ft(s: str) -> float | None:
    m = _FT_RE.search(s or "")
    return float(m.group(1)) + float(m.group(2)) / 12 if m else None


def _dims_ft(s: str) -> list[float]:
    return [float(a) + float(b) / 12 for a, b in _FT_RE.findall(s or "")]


def _col(hdr: list[str], name: str) -> int | None:
    for i, h in enumerate(hdr):
        if name in h:
            return i
    return None


REBAR_LB_PER_FT = {"3": 0.376, "4": 0.668, "5": 1.043, "6": 1.502, "7": 2.044, "8": 2.670}


def seed_takeoff(folder: Path, waste: dict[str, float] | None = None) -> tuple[Ledger, list[dict]]:
    """Deterministic takeoff from schedules, geometry, room tags and notes. Every line says how it
    was derived
    anything not measured is `derived` with confidence ≤ 0.6 so the readers and the
    RFI gate see it."""
    folder = Path(folder)
    sheets = _load(folder / "03-sheets.json")
    profile = Profile(**_load(folder / "00-project-profile.json"))
    div01 = _load(folder / "02-division-01.json")
    waste = waste or load_waste_factors(DATA_DIR / "waste_factors.csv")
    led = Ledger()
    checks: list[dict] = []
    by_kind: dict[str, list[tuple[dict, dict]]] = {}
    for sh in sheets:
        for sc in sh["schedules"]:
            by_kind.setdefault(sc["kind"], []).append((sh, sc))
    plans = [sh for sh in sheets if sh["discipline"] == "A" and sh["sheet_type"] == "plans" and sh.get("geometry")]
    rooms = {t["number"]: t for sh in plans for t in sh["room_tags"]}
    heights = profile.heights_ft or [14.0]
    office_sf = profile.areas.get("OFFICE AREA", profile.gross_sf * 0.3)
    wh_sf = profile.areas.get("WAREHOUSE AREA", profile.gross_sf - office_sf)

    # ---- Division 08 openings from the door / window schedules
    door_total_sched = 0
    for sh, sc in by_kind.get("door", []):
        sid, rev = sh["sheet_id"], sh.get("revision")
        for row in sc["rows"]:
            mark, typ = row[0], " ".join(row[1:]).upper()
            if re.search(r"\bOH\b|SECTIONAL|OVERHEAD", typ):
                code, desc = "08-overhead-door-12x14", f"Overhead door {mark}"
            elif "STOREFRONT" in typ and ("PAIR" in typ or "PR " in typ):
                code, desc = "08-storefront-entrance-pair", f"Storefront entrance pair {mark}"
            elif "RATED" in typ or re.search(r"\d+ MIN", typ):
                code, desc = "08-hm-door-single-rated", f"HM rated door {mark}"
            elif "EXTERIOR" in typ:
                code, desc = "08-hm-door-single-exterior", f"HM exterior door {mark}"
            else:
                code, desc = "08-hm-door-single", f"HM door {mark}"
            led.add("08", code, desc, 1, "EA", sid, "schedule", "03-architectural", revision=rev, confidence=0.95, tags={"mark": mark, "type": typ[:60]})
            if code != "08-overhead-door-12x14":
                door_total_sched += 1
            if code.startswith("08-hm"):
                led.add("09", "09-paint-door-frame", f"Paint HM door and frame {mark}", 1, "EA", sid, "derived", "03-architectural", revision=rev, confidence=0.7)
    for sh, sc in by_kind.get("window", []):
        for row in sc["rows"]:
            qty = row[-1]
            if qty.isdigit():
                led.add("08", "08-window-fixed-aluminum", f"Window {row[0]} {row[1]}", int(qty), "EA", sh["sheet_id"], "schedule", "03-architectural", revision=sh.get("revision"), confidence=0.95, tags={"mark": row[0]})
    # vector cross-checks on the plans
    for sh in plans:
        g = sh["geometry"]
        checks.append({"check": "door swings (vector) vs door schedule", "sheet": sh["sheet_id"], "vector": g["door_candidates"], "schedule": door_total_sched,
                       "status": "match" if g["door_candidates"] == door_total_sched else "MISMATCH"})
        win_sched = sum(it.qty for it in led.items if it.item_code == "08-window-fixed-aluminum")
        checks.append({"check": "window symbols (vector) vs window schedule", "sheet": sh["sheet_id"], "vector": g["window_candidates"], "schedule": win_sched,
                       "status": "match" if g["window_candidates"] == win_sched else "MISMATCH"})
        tag_sum = sum(t["area_sf"] or 0 for t in sh["room_tags"])
        checks.append({"check": "room tag areas vs gross SF", "sheet": sh["sheet_id"], "vector": tag_sum, "schedule": profile.gross_sf,
                       "status": "match" if profile.gross_sf and abs(tag_sum - profile.gross_sf) / profile.gross_sf < 0.02 else "MISMATCH"})

    # ---- Division 09 interiors from the finish schedule × room tag areas
    floor_map = [("CARPET", "09-carpet-tile", "Carpet tile"), ("LVT", "09-lvt-flooring", "LVT flooring"), ("PORC", "09-porcelain-tile-floor", "Porcelain tile floor"),
                 ("SEALED", "03-concrete-sealer", "Concrete sealer")]
    for sh, sc in by_kind.get("finish", []):
        hdr = [h.upper() for h in sc["headers"]]
        c_no, c_fl, c_base, c_wall, c_clg, c_ht = (_col(hdr, n) for n in ("NO", "FLOOR", "BASE", "WALL", "CEIL", "HT"))
        for row in sc["rows"]:
            num = row[c_no] if c_no is not None else row[0]
            r = rooms.get(num)
            area = (r or {}).get("area_sf") or 0
            if not area:
                continue
            perim = 4 * (area ** 0.5)          # derived: square-equivalent perimeter; readers measure the real one
            ht = _ft(row[c_ht]) if c_ht is not None else None
            ht = ht or heights[0]
            sid = sh["sheet_id"]
            fl = row[c_fl].upper() if c_fl is not None else ""
            for key, code, desc in floor_map:
                if key in fl:
                    led.add("09" if code.startswith("09") else "03", code, f"{desc} — room {num}", area, "SF", sid, "schedule", "03-architectural",
                            revision=sh.get("revision"), confidence=0.85, waste_pct=waste.get("flooring", 8) if code.startswith("09") else 0, tags={"room": num})
            base = row[c_base].upper() if c_base is not None else ""
            if "RUBBER" in base:
                led.add("09", "09-rubber-base", f"Rubber base — room {num}", perim, "LF", sid, "derived", "03-architectural", confidence=0.55, notes="perimeter derived from area (square-equivalent)", tags={"room": num})
            elif "TILE" in base:
                led.add("09", "09-tile-base", f"Tile base — room {num}", perim, "LF", sid, "derived", "03-architectural", confidence=0.55, notes="perimeter derived from area", tags={"room": num})
            wall = row[c_wall].upper() if c_wall is not None else ""
            if "PAINT" in wall and "CMU" not in wall:
                led.add("09", "09-paint-gwb", f"Paint walls — room {num}", perim * ht, "SF", sid, "derived", "03-architectural", confidence=0.5, waste_pct=waste.get("paint", 5), notes=f"perimeter × {ht:g} ft ceiling height", tags={"room": num})
            if "WAINSCOT" in wall:
                led.add("09", "09-tile-wainscot", f"Tile wainscot — room {num}", perim * 4.0, "SF", sid, "derived", "03-architectural", confidence=0.5, notes="4 ft wainscot assumed", tags={"room": num})
            clg = row[c_clg].upper() if c_clg is not None else ""
            if "ACT" in clg:
                led.add("09", "09-act-ceiling-2x2", f"ACT ceiling — room {num}", area, "SF", sid, "schedule", "03-architectural", confidence=0.85, tags={"room": num})
            elif "GWB" in clg:
                led.add("09", "09-gwb-ceiling", f"Gypsum ceiling — room {num}", area, "SF", sid, "schedule", "03-architectural", confidence=0.85, tags={"room": num})
    # partitions: interior wall LF from vector geometry (lines not on the exterior rectangle)
    for sh in plans:
        g = sh["geometry"]
        lf = g["wall_lf_by_weight"]
        interior_lf = max(0.0, sum(lf.values()) - (g.get("exterior_perimeter_ft") or 0))
        if interior_lf:
            led.add("09", "09-partition-p1", "Interior partitions type P1 (both faces, to deck)", interior_lf * heights[0], "SF", sh["sheet_id"], "vector", "03-architectural",
                    confidence=0.6, waste_pct=waste.get("drywall", 8), notes=f"{interior_lf:.0f} LF of interior lines × {heights[0]:g} ft; includes the CMU demising line — readers to split by wall type")
    # ---- Divisions 03/04/05/07 from S sheets, elevations and notes
    for sh, sc in by_kind.get("footing", []):
        sid, rev = sh["sheet_id"], sh.get("revision")
        for row in sc["rows"]:
            mark, size, reinf, qty = row[0], row[1], row[2], row[3]
            d = _dims_ft(size)
            bars = re.search(r"\((\d+)\)\s*#(\d)", reinf)
            if "CONT" in size.upper() and len(d) >= 2:
                lf = float(re.sub(r"[^\d.]", "", qty) or 0)
                cy = d[0] * d[1] * lf / 27
                led.add("03", "03-footing-continuous", f"Continuous footing {mark} {size}", cy, "CY", sid, "schedule", "02-civil-structural", revision=rev, confidence=0.9, waste_pct=waste.get("concrete-footing", 5), tags={"mark": mark})
                led.add("03", "03-forms-footing", f"Forms — {mark} (2 sides)", 2 * d[1] * lf, "SFCA", sid, "derived", "02-civil-structural", revision=rev, confidence=0.7)
                if bars:
                    led.add("03", "03-rebar", f"Rebar — {mark} {reinf}", int(bars.group(1)) * lf * REBAR_LB_PER_FT.get(bars.group(2), 1.0) * 1.1, "LB", sid, "derived", "02-civil-structural", revision=rev, confidence=0.7, notes="+10% laps")
            elif len(d) >= 3 and qty.isdigit():
                n = int(qty)
                cy = d[0] * d[1] * d[2] / 27 * n
                led.add("03", "03-footing-spread", f"Spread footing {mark} {size} × {n}", cy, "CY", sid, "schedule", "02-civil-structural", revision=rev, confidence=0.9, waste_pct=waste.get("concrete-footing", 5), tags={"mark": mark})
                led.add("03", "03-forms-footing", f"Forms — {mark}", 2 * (d[0] + d[1]) * d[2] * n, "SFCA", sid, "derived", "02-civil-structural", revision=rev, confidence=0.7)
                if bars:
                    led.add("03", "03-rebar", f"Rebar — {mark} {reinf}", int(bars.group(1)) * 2 * d[0] * REBAR_LB_PER_FT.get(bars.group(2), 1.0) * n, "LB", sid, "derived", "02-civil-structural", revision=rev, confidence=0.7, notes="each way")
    s_sheets = [sh for sh in sheets if sh["discipline"] == "S"]
    for sh in s_sheets:
        text = " ".join(sh.get("text_lines", [])) + " " + " ".join(" ".join(v) for v in sh["notes"].values())
        sid = sh["sheet_id"]
        thicknesses = sorted({int(t) for t in re.findall(r'(\d)"\s*SOG', text)})
        areas = sorted(a for a in (office_sf, wh_sf) if a)
        if len(thicknesses) == 1:
            pairs = [(thicknesses[0], profile.gross_sf)]
        else:
            pairs = list(zip(thicknesses, areas))          # thinner slab ↔ smaller area (office), thicker ↔ larger (warehouse)
        for t, area in pairs:
            code = f"03-sog-{t}in"
            led.add("03", code, f"{t}in slab on grade", area, "SF", sid, "derived", "02-civil-structural", confidence=0.6,
                    waste_pct=waste.get("concrete-slab", 4), notes="thickness from the plan note; area from the code summary — readers to confirm zones")
        m = re.search(r"CONTROL JOINTS AT (\d+)'", text)
        if m and profile.gross_sf:
            spacing = float(m.group(1))
            side = profile.gross_sf ** 0.5
            led.add("03", "03-slab-sawcut-joints", "Slab control joints", 2 * (side / spacing + 1) * side, "LF", sid, "derived", "02-civil-structural", confidence=0.5, notes=f"{spacing:g} ft grid on a square-equivalent footprint")
    for sh, sc in by_kind.get("steel", []):
        sid, rev = sh["sheet_id"], sh.get("revision")
        tons_frame = tons_joist = 0.0
        for row in sc["rows"]:
            try:
                mark, section, length, qty, plf = row[0], row[1], _ft(row[2]) or float(re.sub(r"[^\d.]", "", row[2]) or 0), int(row[3]), float(row[4])
            except (ValueError, IndexError):
                continue
            lb = length * qty * plf
            if re.search(r"\d+K\d+", section):
                tons_joist += lb / 2000
            else:
                tons_frame += lb / 2000
        if tons_frame:
            led.add("05", "05-structural-steel", "Structural steel — beams and columns (from steel schedule)", round(tons_frame, 2), "TON", sid, "schedule", "02-civil-structural", revision=rev, confidence=0.9, notes="add connection allowance per fabricator")
        if tons_joist:
            led.add("05", "05-steel-joists", "Steel joists (from steel schedule)", round(tons_joist, 2), "TON", sid, "schedule", "02-civil-structural", revision=rev, confidence=0.9)
    for sh, sc in by_kind.get("deck", []):
        for row in sc["rows"]:
            sf = float(row[-1].replace(",", "")) if re.match(r"^[\d,]+$", row[-1]) else None
            if sf:
                led.add("05", "05-metal-deck", f"Metal deck — {row[0]} {row[1]}", sf, "SF", sh["sheet_id"], "schedule", "02-civil-structural", revision=sh.get("revision"), confidence=0.9)
    if s_sheets:
        led.add("05", "05-misc-metals", "Miscellaneous metals (lintels, bollards, RTU frames)", 1, "LS", s_sheets[0]["sheet_id"], "derived", "02-civil-structural", confidence=0.4, notes="allowance-type line — readers to itemize from details")
    # exterior walls: perimeter × heights; brick veneer from elevation notes
    for sh in plans:
        g = sh["geometry"]
        if g.get("exterior_perimeter_ft"):
            per = g["exterior_perimeter_ft"]
            h_avg = sum(heights) / len(heights)
            led.add("04", "04-cmu-8in-grouted", "8in CMU exterior walls (perimeter × average height)", per * h_avg, "SF", sh["sheet_id"], "derived", "02-civil-structural",
                    confidence=0.55, waste_pct=waste.get("cmu", 5), notes=f"{per:.0f} LF × {h_avg:g} ft avg of {heights}; readers to split office/warehouse heights and add the demising wall")
            led.add("07", "07-sealants-joints", "Exterior sealants and control joints", per, "LF", sh["sheet_id"], "derived", "03-architectural", confidence=0.5)
            led.add("06", "06-rough-carpentry-blocking", "Rough carpentry and blocking", profile.gross_sf, "SF", sh["sheet_id"], "derived", "03-architectural", confidence=0.5)
    for sh in sheets:
        if sh["discipline"] != "A":
            continue
        for items in sh["notes"].values():
            for it in items:
                m = re.search(r"BRICK VENEER[^.]*?\(([^)]*)\)", it.upper())
                if m:
                    lfs = [float(x) for x in re.findall(r"(\d+)\s*LF", m.group(1))]
                    h = _ft(m.group(1)) or heights[0]
                    if lfs:
                        led.add("04", "04-brick-veneer", "Brick veneer (from elevation note)", sum(lfs) * h, "SF", sh["sheet_id"], "spec", "02-civil-structural", confidence=0.75, waste_pct=waste.get("brick", 7), notes=it[:80])
                m = re.search(r"COPING[^.]*?(\d+)\s*LF", it.upper())
                if m:
                    led.add("07", "07-coping-aluminum", "Aluminum coping (from elevation note)", float(m.group(1)), "LF", sh["sheet_id"], "spec", "03-architectural", confidence=0.8)
                m = re.search(r"DRAINS \((\d+)\)[^.]*?OVERFLOWS \((\d+)\)", it.upper())
                if m:
                    led.add("07", "07-roof-drain", "Roof drains and overflow drains", int(m.group(1)) + int(m.group(2)), "EA", sh["sheet_id"], "spec", "03-architectural", confidence=0.85)
    # roofing from footprint
    if profile.gross_sf:
        a_ref = plans[0]["sheet_id"] if plans else "A-201"
        led.add("07", "07-tpo-roof-system", "TPO roof system over R-30 polyiso (footprint)", profile.gross_sf / 100, "SQ", a_ref, "derived", "03-architectural", confidence=0.7, waste_pct=waste.get("roofing", 7), notes="footprint area; add parapets/canopies from the roof plan")
        led.add("07", "07-tapered-insulation-crickets", "Tapered crickets (10% of roof area assumed)", profile.gross_sf * 0.10, "SF", a_ref, "derived", "03-architectural", confidence=0.4)
    # ---- Division 10 specialties
    if rooms:
        led.add("10", "10-fire-extinguisher-cabinet", "Fire extinguisher cabinets (1 per 3,000 SF)", max(1, round(profile.gross_sf / 3000)), "EA", plans[0]["sheet_id"] if plans else "A-101", "derived", "03-architectural", confidence=0.5)
    # ---- MEP from schedules and notes
    fixture_map = [("WC", "22-water-closet"), ("UR", "22-urinal"), ("LAV", "22-lavatory"), ("SK", "22-sink"), ("MS", "22-mop-sink"), ("EWC", "22-water-cooler"), ("WH", "22-water-heater-40gal"), ("HB", "22-hose-bibb")]
    plumbing_fixture_count = 0
    for sh, sc in by_kind.get("fixture", []):
        sid, rev = sh["sheet_id"], sh.get("revision")
        if sh["discipline"] == "P":
            for row in sc["rows"]:
                tag, qty = row[0].upper(), row[-1]
                if not qty.isdigit():
                    continue
                for pre, code in fixture_map:
                    if tag.startswith(pre + "-") or tag == pre:
                        led.add("22", code, f"{row[1][:50]} ({tag})", int(qty), "EA", sid, "schedule", "04-mep", revision=rev, confidence=0.95, tags={"tag": tag})
                        if pre in ("WC", "UR", "LAV"):
                            plumbing_fixture_count += int(qty)
                        break
        elif sh["discipline"] == "E":
            for row in sc["rows"]:
                typ, desc, qty = row[0].upper(), row[1].upper(), row[-1]
                if not qty.isdigit():
                    continue
                code = "26-troffer-led-2x4" if "TROFFER" in desc else "26-high-bay-led" if "HIGH BAY" in desc else "26-wall-pack-led" if "WALL PACK" in desc else "26-exit-sign" if "EXIT" in desc else None
                if code:
                    led.add("26", code, f"{row[1][:50]} (type {typ})", int(qty), "EA", sid, "schedule", "04-mep", revision=rev, confidence=0.95, tags={"type": typ})
    if plumbing_fixture_count:
        led.add("10", "10-toilet-accessories-per-fixture", "Toilet accessories and partitions (per WC/UR/LAV)", plumbing_fixture_count, "EA", "A-601", "derived", "03-architectural", confidence=0.5)
    if office_sf:
        p_ref = next((sh["sheet_id"] for sh in sheets if sh["discipline"] == "P"), "P-101")
        led.add("22", "22-pipe-domestic-per-sf", "Domestic water and sanitary distribution (per SF of office)", office_sf, "SF", p_ref, "derived", "04-mep", confidence=0.5, notes="readers to take pipe by size from risers")
    mech_connections = 0
    for sh, sc in by_kind.get("equipment", []):
        sid, rev = sh["sheet_id"], sh.get("revision")
        for row in sc["rows"]:
            tag = row[0].upper()
            code = "23-rtu-7-5-ton" if tag.startswith("RTU") else "23-unit-heater-gas" if tag.startswith("UH") else "23-exhaust-fan" if tag.startswith("EF") else None
            if code:
                led.add("23", code, f"{row[1][:40]} {tag}", 1, "EA", sid, "schedule", "04-mep", revision=rev, confidence=0.95, tags={"tag": tag})
                mech_connections += 1
                if tag.startswith("RTU"):
                    led.add("23", "23-controls-thermostats", f"Thermostat and controls — {tag}", 1, "EA", sid, "derived", "04-mep", confidence=0.7)
    for sh in sheets:
        if sh["discipline"] != "M":
            continue
        for items in sh["notes"].values():
            for it in items:
                m = re.search(r"DIFFUSERS[^.]*?QTY (\d+)", it.upper())
                n1 = int(m.group(1)) if m else 0
                m2 = re.search(r"RETURN GRILLES[^.]*?QTY (\d+)", it.upper())
                n2 = int(m2.group(1)) if m2 else 0
                if n1 or n2:
                    led.add("23", "23-diffuser-grille", "Supply diffusers and return grilles (from notes)", n1 + n2, "EA", sh["sheet_id"], "spec", "04-mep", confidence=0.8)
                    led.add("23", "23-tab", "Testing, adjusting and balancing per outlet", n1 + n2, "EA", sh["sheet_id"], "derived", "04-mep", confidence=0.6)
                m = re.search(r"APPROX\.?\s*([\d,]+)\s*LF", it.upper())
                if m and "DUCT" in it.upper():
                    lf = float(m.group(1).replace(",", ""))
                    led.add("23", "23-ductwork", "Galvanized ductwork (LF × 7 lb/LF assumed 24x12 24 ga)", lf * 7.0, "LB", sh["sheet_id"], "derived", "04-mep", confidence=0.45, waste_pct=waste.get("ductwork", 10), notes=it[:80])
    for sh in sheets:
        if sh["discipline"] != "P":
            continue
        for sc in sh["schedules"]:
            if sc["kind"] == "fire":
                heads = sum(int(r[-1]) for r in sc["rows"] if r and r[-1].isdigit())
                if heads:
                    led.add("21", "21-sprinkler-design-build", "Wet-pipe sprinkler design-build (heads from FP basis table)", heads, "EA", sh["sheet_id"], "schedule", "04-mep", revision=sh.get("revision"), confidence=0.8)
        for items in sh["notes"].values():
            for it in items:
                m = re.search(r"GAS:\s*([^.]+)", it.upper())
                if m:
                    led.add("22", "22-gas-piping", "Gas piping to equipment (LF assumed 120)", 120, "LF", sh["sheet_id"], "derived", "04-mep", confidence=0.4, notes="no LF on the sheet — question raised")
    for sh, sc in by_kind.get("panel", []):
        sid, rev = sh["sheet_id"], sh.get("revision")
        if "GEAR" in sc["title"].upper() or "ONE-LINE" in sc["title"].upper():
            for row in sc["rows"]:
                tag, desc = row[0].upper(), row[1].upper()
                code = "26-service-400a-mdp" if tag == "MDP" or "MAIN DISTRIBUTION" in desc else "26-transformer-45kva" if tag.startswith("T-") or "TRANSFORMER" in desc else "26-panelboard" if "PANELBOARD" in desc else None
                if code:
                    led.add("26", code, f"{row[1][:50]} ({tag})", 1, "EA", sid, "schedule", "04-mep", revision=rev, confidence=0.9, tags={"tag": tag})
                    if code != "26-service-400a-mdp":
                        led.add("26", "26-feeders-per-panel", f"Feeder conduit and wire — {tag}", 1, "EA", sid, "derived", "04-mep", confidence=0.6)
    for sh in sheets:
        if sh["discipline"] != "E":
            continue
        for items in sh["notes"].values():
            for it in items:
                m = re.search(r"RECEPTACLES:\s*(\d+)", it.upper())
                if m:
                    led.add("26", "26-receptacle-duplex", "Duplex receptacles (from notes)", int(m.group(1)), "EA", sh["sheet_id"], "spec", "04-mep", confidence=0.8)
                m = re.search(r"DATA OUTLETS:\s*(\d+)", it.upper())
                if m:
                    led.add("27", "27-data-outlet-raceway", "Data outlet boxes and raceway (cabling by owner)", int(m.group(1)), "EA", sh["sheet_id"], "spec", "04-mep", confidence=0.8)
        for sc in sh["schedules"]:
            if "FIRE ALARM" in sc["title"].upper():
                for row in sc["rows"]:
                    if row[-1].isdigit():
                        code = "28-facp" if "FACP" in row[0].upper() else "28-fa-device"
                        led.add("28", code, f"Fire alarm — {row[0]}", int(row[-1]), "EA", sh["sheet_id"], "schedule", "04-mep", revision=sh.get("revision"), confidence=0.9)
    if mech_connections:
        e_ref = next((sh["sheet_id"] for sh in sheets if sh["discipline"] == "E"), "E-101")
        led.add("26", "26-mechanical-connection", "Power connections to mechanical/plumbing equipment", mech_connections + 1, "EA", e_ref, "derived", "04-mep", confidence=0.6, notes="+1 for the water heater")
    # ---- Division 01 allowances from the spec
    for h in div01.get("allowances", []):
        amt = float(h["groups"][0].replace(",", "")) if h.get("groups") else 0
        what = h["groups"][1] if len(h.get("groups", [])) > 1 else "allowance"
        code = "10-signage-allowance" if "signage" in what.lower() else f"01-allowance-{_slug(what)[:30]}"
        led.add("10" if code.startswith("10") else "01", code, f"Allowance — {what}", 1, "LS", "Project Manual", "allowance", "01-bid-coordination", confidence=1.0, tags={"amount": amt, "page": h["page"]})
    disc = [d.to_dict() for d in led.reconcile()]
    _write(folder / "03-takeoff-seed.json", led.to_json())
    _write(folder / "03-takeoff-checks.json", json.dumps(checks, indent=2))
    _write(folder / "04-takeoff-ledger.json", led.to_json())
    _write(folder / "04-takeoff-ledger.md", led.to_markdown("Takeoff ledger (seed — schedule, vector and derived lines)") + "\n## Cross-checks\n\n" + "\n".join(f"- {c['check']} on {c['sheet']}: vector {c['vector']} vs schedule {c['schedule']} → **{c['status']}**" for c in checks) + "\n")
    _write(folder / "04-discrepancies.json", json.dumps(disc, indent=2))
    return led, checks


def merge_reader_lines(folder: Path, reader_json: Path) -> Ledger:
    """Harness path: merge lines written by a reader agent (same schema) into the ledger and re-reconcile."""
    led = Ledger.from_json((folder / "04-takeoff-ledger.json").read_text(encoding="utf-8"))
    for d in _load(reader_json):
        led.add(d["division"], d["item_code"], d["description"], d["qty"], d["unit"], d["sheet"], d.get("method", "vision"), d.get("discipline", ""),
                revision=d.get("revision"), section=d.get("section"), confidence=float(d.get("confidence", 0.7)), waste_pct=float(d.get("waste_pct", 0)), notes=d.get("notes", ""), tags=d.get("tags", {}))
    disc = [x.to_dict() for x in led.reconcile()]
    _write(folder / "04-takeoff-ledger.json", led.to_json())
    _write(folder / "04-takeoff-ledger.md", led.to_markdown("Takeoff ledger (merged)"))
    _write(folder / "04-discrepancies.json", json.dumps(disc, indent=2))
    return led


# --------------------------------------------------------------------------------------------- S3 RFI
def rfi(folder: Path) -> list:
    folder = Path(folder)
    register = _load(folder / "01-sheet-register.json")
    sheets = _load(folder / "03-sheets.json")
    disc = _load(folder / "04-discrepancies.json") if (folder / "04-discrepancies.json").exists() else []
    spec = _load(folder / "02-spec-index.json").get("sections", [])
    div01 = _load(folder / "02-division-01.json")
    items = _load(folder / "04-takeoff-ledger.json")
    for c in (_load(folder / "03-takeoff-checks.json") if (folder / "03-takeoff-checks.json").exists() else []):
        if c["status"] == "MISMATCH":
            disc.append({"item_code": c["check"], "description": c["check"], "a_method": "schedule", "a_qty": c["schedule"], "b_method": "vector", "b_qty": c["vector"],
                         "delta_pct": round(abs(c["vector"] - c["schedule"]) / (c["schedule"] or 1) * 100, 1), "sheet": c["sheet"]})
    qs = build_questions(register, sheets, disc, spec, div01, items)
    write_questions(folder, qs)
    return qs


def resume(folder: Path, auto_assume: bool = False) -> list:
    return auto_assume_all(folder) if auto_assume else apply_answers(folder)


# ------------------------------------------------------------------------------------------- S4 price
def policy_from_brain(vault_root: Path | None, aace_class: int, building_type: str, duration_days: int) -> MarkupPolicy:
    """Read 00-Brain/markup-policy.md + benchmarks.md; fall back to defaults and say so."""
    cont, fee, ins, bond, yoy = 3.0, 5.0, 1.2, 0.9, 5.15
    c_basis, f_basis, e_basis = "engine default [POLICY DEFAULT]", "engine default [POLICY DEFAULT]", "engine default 5.15%/yr [POLICY DEFAULT]"
    if vault_root:
        mp = Path(vault_root) / "00-Brain" / "markup-policy.md"
        if mp.exists():
            t = mp.read_text(encoding="utf-8")
            m = re.search(rf"^\|\s*{aace_class}\s*\|[^|]*\|\s*(\d+(?:\.\d+)?)%", t, re.MULTILINE)
            if m:
                cont, c_basis = float(m.group(1)), f"00-Brain/markup-policy.md class {aace_class} default"
            bt = building_type.lower()
            fm = re.search(r"Overhead and profit \(fee\):\s*([^\n]+)", t)
            if fm:
                for pct, kind in re.findall(r"(\d+(?:\.\d+)?)%\s*([a-zA-Z/ \-0-9]+?)(?:\s*·|\s*\[|$)", fm.group(1)):
                    if any(k.strip() in bt for k in kind.lower().split("/")):
                        fee, f_basis = float(pct), f"00-Brain/markup-policy.md fee for {kind.strip()}"
                        break
            im = re.search(r"insurance:\s*(\d+(?:\.\d+)?)%", t, re.IGNORECASE)
            if im:
                ins = float(im.group(1))
            bm = re.search(r"bond:\s*(\d+(?:\.\d+)?)%", t, re.IGNORECASE)
            if bm:
                bond = float(bm.group(1))
        bk = Path(vault_root) / "00-Brain" / "benchmarks.md"
        if bk.exists():
            ym = re.search(r"Turner Building Cost Index[^\n]*?\+(\d+(?:\.\d+)?)% YoY", bk.read_text(encoding="utf-8"))
            if ym:
                yoy, e_basis = float(ym.group(1)), f"Turner BCI +{ym.group(1)}% YoY (00-Brain/benchmarks.md)"
    months_to_mid = (duration_days or 240) / 30.4 / 2
    esc = round(yoy * months_to_mid / 12, 2)
    return MarkupPolicy(contingency_pct=cont, escalation_pct=esc, insurance_pct=ins, bond_pct=bond, fee_pct=fee,
                        contingency_basis=c_basis, escalation_basis=f"{e_basis} × {months_to_mid:.1f} months to mid-point", fee_basis=f_basis)


def price(folder: Path, vault_root: Path | None = None) -> dict:
    folder = Path(folder)
    profile = Profile(**_load(folder / "00-project-profile.json"))
    led = Ledger.from_json((folder / "04-takeoff-ledger.json").read_text(encoding="utf-8"))
    paths = library_paths(vault_root)
    lib = load_library(paths)
    # allowance lines price at their spec amount
    for it in led.items:
        if it.method == "allowance" and it.tags.get("amount") and it.item_code not in lib:
            from core.estimating.cost_engine import CostRow
            lib[it.item_code] = CostRow(it.item_code, it.description, "LS", 0, 0, 0, float(it.tags["amount"]), f"spec allowance p{it.tags.get('page', '?')}", pricing_basis="allowance")
    factor, f_src = load_location_factor(profile.city)
    lines = price_ledger(led, lib, location_factor=factor)
    direct = round(sum(p.total for p in lines), 2)
    materials = round(sum(p.material for p in lines), 2)
    labor = round(sum(p.labor for p in lines), 2)
    months = round((profile.duration_days or 240) / 30.4, 1)
    def rate(code: str, default: float) -> float:
        return lib[code].unit_total if code in lib else default
    concrete_cy = sum(it.qty for it in led.items if it.unit == "CY")
    perim = next((sh.get("geometry", {}) or {}).get("exterior_perimeter_ft") for sh in _load(folder / "03-sheets.json") if (sh.get("geometry") or {}).get("exterior_perimeter_ft")) or 0
    gcs = general_conditions(
        months,
        staff=[("Superintendent", 1.0, rate("01-superintendent", 15500)), ("Project manager", 0.5, rate("01-project-manager", 14500)),
               ("Project engineer", 0.5, rate("01-project-engineer", 9200)), ("Safety manager (shared)", 1.0, rate("01-safety-share", 2800))],
        temp_items=[("Job trailer", 1, "MO", rate("01-job-trailer", 1250)), ("Portable toilets (2)", 2, "MO", rate("01-temp-toilets", 210)),
                    ("Temporary power and water", 1, "MO", rate("01-temp-power-water", 1400)), ("Dumpster pulls (2/month)", 2 * months, "EA", rate("01-dumpsters", 650)),
                    ("Temporary fence (1.5 × building perimeter, derived)", 1.5 * perim, "LF", rate("01-temp-fence", 9.5)), ("Progress and final cleaning", profile.gross_sf, "SF", rate("01-cleaning", 0.45)),
                    ("Concrete testing sets (CY/100 + 1)", int(concrete_cy // 100) + 1, "EA", rate("01-concrete-testing", 180))],
        other=[("Surveying and layout", rate("01-surveying-layout", 9500), "lump sum [UNCERTAIN]")],
    )
    gc_total = round(sum(g.total for g in gcs), 2)
    policy = policy_from_brain(vault_root, profile.aace_class, profile.building_type, profile.duration_days)
    markups = markup_stack(direct, materials, gc_total, policy)
    three_point = three_point_totals(lines, materials, gc_total, policy)
    summary = summary_by_division(lines, profile.gross_sf, spec_index.DIVISIONS)
    total = markups[-1].amount
    bench = benchmark_check(total, profile.gross_sf, profile.building_type, gc_total, direct, labor)
    meta = {"generated": datetime.now().isoformat(timespec="seconds"), "library_paths": [str(p) for p in paths], "location_factor": factor, "location_source": f_src,
            "duration_months": months, "policy": asdict(policy), "three_point": three_point, "aace_class": profile.aace_class, "accuracy_band": profile.accuracy_band, "disclaimer": SEED_DISCLAIMER if any(r.uncertain for r in lib.values()) else "", "benchmark": bench}
    _write(folder / "06-estimate.json", estimate_json(lines, gcs, markups, summary, meta))
    md = ["---", "type: estimate", f"total_bid: {total}", "---", f"# Estimate — {profile.name}", "", f"Direct ${direct:,.0f} · GCs ${gc_total:,.0f} ({gc_total / direct * 100 if direct else 0:.1f}%) · **Total bid ${total:,.0f}** · ${total / profile.gross_sf:,.2f}/SF" if profile.gross_sf else "", "",
          "| Division | Title | Total | $/SF | % |", "|---|---|---|---|---|"] + [f"| {r['division']} | {r['title']} | ${r['total']:,.0f} | {r['per_sf']} | {r['pct']}% |" for r in summary] + \
         ["", "| Markup | % | Amount | Basis |", "|---|---|---|---|"] + [f"| {m.name} | {m.pct} | ${m.amount:,.0f} | {m.basis} |" for m in markups] + \
         ["", "## Benchmark", ""] + [f"- {c['check']}: {c['value']} vs {c['band']} → **{c['status']}** ({c['source']})" for c in bench["checks"]] + \
         ["", f"Three-point (same markups on low / target / high direct): **${three_point['low']['total']:,.0f} / ${three_point['target']['total']:,.0f} / ${three_point['high']['total']:,.0f}** (spread {three_point['spread_pct']}%) · class {profile.aace_class}, expected accuracy {profile.accuracy_band}", "", f"Flags: unpriced {sum('UNPRICED' in p.flags for p in lines)} · uncertain {sum('UNCERTAIN' in p.flags for p in lines)} · low-confidence {sum('LOW-CONFIDENCE' in p.flags for p in lines)}", "", meta["disclaimer"]]
    _write(folder / "06-estimate.md", "\n".join(md) + "\n")
    return _load(folder / "06-estimate.json")


# ------------------------------------------------------------------------------------------ S5 review
def review(folder: Path, confidence_floor: float = 0.6) -> tuple[list[dict], str]:
    folder = Path(folder)
    est = _load(folder / "06-estimate.json")
    register = _load(folder / "01-sheet-register.json")
    items = _load(folder / "04-takeoff-ledger.json")
    spec = _load(folder / "02-spec-index.json").get("sections", [])
    qs = _load(folder / "05-questions.json") if (folder / "05-questions.json").exists() else []
    profile = _load(folder / "00-project-profile.json")
    risks = _load(folder / "06-risks.json") if (folder / "06-risks.json").exists() else None
    playbook_trades = None
    if profile.get("playbook"):
        excl = {k[len("trade:"):]: v for k, v in (profile.get("exclusions") or {}).items() if k.startswith("trade:")}
        playbook_trades = {t: excl.get(t) for t in profile["playbook"].get("typical_trades", [])}
        if est.get("general_conditions") and "general-conditions" in playbook_trades and not playbook_trades["general-conditions"]:
            playbook_trades["general-conditions"] = "priced in the general-conditions worksheet"
    # client-facing proposal draft + client-safe scan (feeds G13); the writer agent may rephrase later, never remove findings
    proposal_text, findings = proposal_markdown(profile, est, items, qs, exclusions_extra=profile.get("exclusion_texts") or [])
    _write(folder / "09-proposal-draft.md", proposal_text)
    _write(folder / "09-client-safe-findings.md", findings_markdown(findings))
    _write(folder / "09-client-safe-findings.json", json.dumps([f.to_dict() for f in findings], indent=2))
    gates = run_gates(register, items, est["lines"], est["summary_by_division"], spec, qs, est["meta"]["benchmark"], profile["gross_sf"], confidence_floor,
                      excluded_divisions=profile.get("exclusions", {}), playbook_trades=playbook_trades, risks=risks,
                      client_findings=[f.to_dict() for f in findings])
    judged = _load(folder / "07-judged-review.json") if (folder / "07-judged-review.json").exists() else None
    gd = [g.to_dict() for g in gates]
    _write(folder / "07-review-scorecard.json", json.dumps({"verdict": verdict(gates), "gates": gd, "judged": judged}, indent=2))
    _write(folder / "07-review-scorecard.md", scorecard_markdown(gates, judged))
    return gd, verdict(gates)


# ------------------------------------------------------------------------------------------ S6 report
def report(folder: Path) -> Path:
    folder = Path(folder)
    profile = _load(folder / "00-project-profile.json")
    est = _load(folder / "06-estimate.json")
    sc = _load(folder / "07-review-scorecard.json")
    qs = _load(folder / "05-questions.json") if (folder / "05-questions.json").exists() else []
    items = _load(folder / "04-takeoff-ledger.json")
    narrative = _load(folder / "08-narrative.json") if (folder / "08-narrative.json").exists() else None
    assumptions = [f"{q['text'][:120]} → {q['assumption']}" for q in qs if q.get("assumption")]
    profile["assumptions"] = assumptions + [f"Excluded — division {d}: {why}" for d, why in profile.get("exclusions", {}).items()] + \
        ["Standing exclusions per 00-Brain/markup-policy.md apply unless the bid form says otherwise."]
    out = folder / "08-estimate-report.md"
    _write(out, report_markdown(profile, est, sc["gates"], qs, est["meta"]["benchmark"], items, narrative))
    return out


def approve(folder: Path, vault_root: Path) -> list[Path]:
    folder, vault_root = Path(folder), Path(vault_root)
    out_dir = vault_root / "03-Outputs" / folder.name
    est = _load(folder / "06-estimate.json")
    sc = _load(folder / "07-review-scorecard.json")
    qs = _load(folder / "05-questions.json") if (folder / "05-questions.json").exists() else []
    profile = _load(folder / "00-project-profile.json")
    xlsx = write_workbook(out_dir / "estimate-workbook.xlsx", est, _load(folder / "04-takeoff-ledger.json"), sc["gates"], qs, _load(folder / "01-sheet-register.json"), profile)
    docx = write_basis_of_estimate_docx(out_dir / "basis-of-estimate.docx", (folder / "08-estimate-report.md").read_text(encoding="utf-8"), f"Basis of Estimate — {profile['name']}")
    outs = [xlsx, docx]
    if (folder / "09-proposal-draft.md").exists():
        outs.append(write_basis_of_estimate_docx(out_dir / "proposal-draft.docx", (folder / "09-proposal-draft.md").read_text(encoding="utf-8"), f"Proposal — {profile['name']}"))
    _write(out_dir / "README.md", f"# Outputs — {profile['name']}\n\n" + "\n".join(f"- {o.name}" for o in outs) + f"\n- source estimate folder: `{folder.name}`\n")
    return outs



# ------------------------------------------------------------------------------------------ ROM (Class 5 / 4)
def _gc_lines(lib: dict, months: float, gross_sf: float, perimeter_lf: float, concrete_cy: float, cfg: dict | None = None) -> list:
    """General conditions from a staffing/temp-facilities config (playbook or default) and library rates."""
    cfg = cfg or {"superintendent_fte": 1.0, "pm_fte": 0.5, "pe_fte": 0.5, "safety_fte": 1.0, "trailer": True, "toilets": 2, "dumpsters_per_month": 2, "fence": True}

    def rate(code: str, default: float) -> float:
        return lib[code].unit_total if code in lib else default

    staff = [("Superintendent", float(cfg.get("superintendent_fte", 1.0)), rate("01-superintendent", 15500)),
             ("Project manager", float(cfg.get("pm_fte", 0.5)), rate("01-project-manager", 14500)),
             ("Project engineer", float(cfg.get("pe_fte", 0.5)), rate("01-project-engineer", 9200)),
             ("Safety manager (shared)", float(cfg.get("safety_fte", 1.0)), rate("01-safety-share", 2800))]
    temp = []
    if cfg.get("trailer", True):
        temp.append(("Job trailer", 1, "MO", rate("01-job-trailer", 1250)))
    temp += [("Portable toilets", float(cfg.get("toilets", 2)), "MO", rate("01-temp-toilets", 210)),
             ("Temporary power and water", 1, "MO", rate("01-temp-power-water", 1400)),
             ("Dumpster pulls", float(cfg.get("dumpsters_per_month", 2)) * months, "EA", rate("01-dumpsters", 650)),
             ("Progress and final cleaning", gross_sf, "SF", rate("01-cleaning", 0.45)),
             ("Concrete testing sets (CY/100 + 1)", int(concrete_cy // 100) + 1 if concrete_cy else 0, "EA", rate("01-concrete-testing", 180))]
    if cfg.get("fence", True) and perimeter_lf:
        temp.append(("Temporary fence (1.5 × building perimeter, derived)", 1.5 * perimeter_lf, "LF", rate("01-temp-fence", 9.5)))
    return general_conditions(months, staff=[(n, f, r) for n, f, r in staff if f > 0], temp_items=[t for t in temp if t[1] > 0],
                              other=[("Surveying and layout", rate("01-surveying-layout", 9500), "lump sum [UNCERTAIN]")])


def rom(vault_root: Path, intake: dict) -> Path:
    """Same-day ROM: an intake form + a project-type playbook → assemblies × quantity rules → three-point
    estimate with class and band, risk register, questions (defaults become stated assumptions), gates,
    report and a client-safe proposal draft. No drawings required; no model involved."""
    from core.estimating.playbooks import TRADE_DEPARTMENT, quantity_for, resolve_basis, resolve_playbook

    vault_root = Path(vault_root)
    pb = resolve_playbook(str(intake["project_type"]))
    problems = pb.validate()
    if problems:
        raise ValueError(f"playbook {pb.project_type} invalid: {problems}")
    name = str(intake.get("name") or f"{pb.project_type} ROM")
    folder = create_folder(vault_root, name)
    cls = int(intake.get("aace_class") or (4 if intake.get("plans_available") else pb.default_class))
    basis = resolve_basis(pb, intake)
    duration = int(intake.get("duration_days") or pb.schedule_range_days.get("target") or 90)
    profile = Profile(name=name, slug=folder.name, building_type=pb.building_type_band, city=str(intake.get("city") or "Dallas"), aace_class=cls,
                      gross_sf=float(basis.values.get("gross_sf") or 0), stories=int(intake.get("stories") or 1), delivery=str(intake.get("delivery") or "negotiated ROM"),
                      duration_days=duration, assumptions=list(basis.assumptions), notes=str(intake.get("notes") or ""),
                      playbook={"project_type": pb.project_type, "version": pb.version, "status": pb.status, "typical_trades": list(pb.typical_trades)})
    profile.accuracy_band = ACCURACY_BANDS.get(cls, "")
    excluded = {str(t).strip().lower() for t in (intake.get("excluded_trades") or [])}
    for t in sorted(excluded):
        profile.exclusions[f"trade:{t}"] = "excluded at intake"
    # ledger from assemblies
    led = Ledger()
    skipped: list[str] = []
    for a in pb.assemblies:
        if a.trade in excluded:
            continue
        qty, how = quantity_for(a, basis)
        if qty <= 0:
            skipped.append(f"{a.code}: {how}")
            continue
        led.add(a.division, a.code, a.description, qty, a.unit, "intake", "derived", TRADE_DEPARTMENT.get(a.trade, "05-cost-engineering"),
                confidence=a.confidence, notes=f"qty = {how}", tags={"trade": a.trade, "assembly": a.code}, pricing_basis="assembly")
    for al in intake.get("allowances") or []:
        led.add("01", f"01-allowance-{_slug(str(al['name']))[:30]}", f"Allowance — {al['name']}", 1, "LS", "intake", "allowance", "01-bid-coordination",
                confidence=1.0, tags={"amount": float(al["amount"]), "source": "intake", "trade": "general-conditions"}, pricing_basis="allowance")
    _write(folder / "00-intake.json", json.dumps(intake, indent=2))
    _write(folder / "00-playbook.json", json.dumps(profile.playbook | {"skipped_assemblies": skipped, "basis": basis.values}, indent=2))
    # risk register with playbook mitigations
    risks = []
    for r in pb.risk_checklist:
        if r.trade and r.trade in excluded:
            continue
        if r.mitigation_exclusion:
            mit = {"type": "exclusion", "ref": r.mitigation_exclusion}
        elif r.rfi:
            mit = {"type": "rfi", "ref": r.rfi}
        else:
            mit = {"type": "none", "ref": ""}
        risks.append({"risk": r.risk, "severity": r.severity, "trade": r.trade, "mitigation": mit})
    profile.exclusion_texts = list(pb.common_exclusions) + [r.mitigation_exclusion for r in pb.risk_checklist if r.mitigation_exclusion and not (r.trade and r.trade in excluded)]
    _write(folder / "06-risks.json", json.dumps(risks, indent=2))
    _write(folder / "00-project-profile.json", json.dumps(profile.to_dict(), indent=2))
    _write(folder / "00-project-profile.md", _profile_md(profile, [], None) + "\n## Playbook\n" + f"- {pb.project_type} v{pb.version} ({pb.status})\n" +
           "\n## Assumptions (defaults used)\n" + "\n".join(f"- {a}" for a in basis.assumptions) + "\n")
    _write(folder / "01-sheet-register.json", "[]")
    _write(folder / "01-sheet-register.md", "---\ntype: sheet_register\nsheets: 0\n---\n# Sheet register\n\nNo drawings — ROM from intake and playbook.\n")
    _write(folder / "02-spec-index.json", json.dumps({"file": None, "pages": 0, "sections": []}))
    _write(folder / "02-division-01.json", "{}")
    _write(folder / "03-sheets.json", "[]")
    _write(folder / "04-takeoff-ledger.json", led.to_json())
    _write(folder / "04-takeoff-ledger.md", led.to_markdown(f"ROM ledger — {pb.project_type} playbook v{pb.version}"))
    _write(folder / "04-discrepancies.json", "[]")
    # questions: missing required → CRITICAL open; defaults → WARN carried as assumption; high risks → CRITICAL carried as exclusion or open
    qs = build_rom_questions(pb, basis, risks, intake)
    write_questions(folder, qs)
    # price: assemblies first, then BYO / seed for anything else (allowances price at their amount)
    lib = pb.cost_rows()
    for k, v in load_library(library_paths(vault_root)).items():
        lib.setdefault(k, v)
    for it in led.items:
        if it.method == "allowance" and it.tags.get("amount"):
            from core.estimating.cost_engine import CostRow
            lib[it.item_code] = CostRow(it.item_code, it.description, "LS", 0, 0, 0, float(it.tags["amount"]), "intake allowance", pricing_basis="allowance")
    factor, f_src = load_location_factor(profile.city)
    lines = price_ledger(led, lib, location_factor=factor)
    direct = round(sum(p.total for p in lines), 2)
    materials = round(sum(p.material for p in lines), 2)
    labor = round(sum(p.labor for p in lines), 2)
    months = round(duration / 30.4, 1)
    concrete_cy = sum(it.qty for it in led.items if it.unit == "CY")
    gcs = _gc_lines(lib, months, profile.gross_sf, float(basis.values.get("perimeter_lf") or 0), concrete_cy, pb.general_conditions)
    gc_total = round(sum(g.total for g in gcs), 2)
    policy = policy_from_brain(vault_root, cls, profile.building_type, duration)
    markups = markup_stack(direct, materials, gc_total, policy)
    three_point = three_point_totals(lines, materials, gc_total, policy)
    summary = summary_by_division(lines, profile.gross_sf, spec_index.DIVISIONS)
    total = markups[-1].amount
    bench = benchmark_check(total, profile.gross_sf, profile.building_type, gc_total, direct, labor)
    meta = {"generated": datetime.now().isoformat(timespec="seconds"), "mode": "rom", "playbook": profile.playbook, "basis": basis.values,
            "library_paths": [pb.path] + [str(p) for p in library_paths(vault_root)], "location_factor": factor, "location_source": f_src,
            "duration_months": months, "policy": asdict(policy), "three_point": three_point, "aace_class": cls, "accuracy_band": profile.accuracy_band,
            "disclaimer": SEED_DISCLAIMER if pb.status != "approved" else "", "benchmark": bench}
    _write(folder / "06-estimate.json", estimate_json(lines, gcs, markups, summary, meta))
    md = ["---", "type: estimate", "mode: rom", f"total_bid: {total}", "---", f"# ROM estimate — {name}", "",
          f"Playbook {pb.project_type} v{pb.version} ({pb.status}) · class {cls}, expected accuracy {profile.accuracy_band} · {profile.gross_sf:,.0f} SF · {profile.city}", "",
          f"**Low ${three_point['low']['total']:,.0f} · Target ${three_point['target']['total']:,.0f} · High ${three_point['high']['total']:,.0f}** (spread {three_point['spread_pct']}%) · "
          f"target ${total / profile.gross_sf:,.2f}/SF" if profile.gross_sf else "", "",
          f"Direct ${direct:,.0f} · GCs ${gc_total:,.0f} ({gc_total / direct * 100 if direct else 0:.1f}%)", "",
          "| Division | Title | Low | Target | High | % |", "|---|---|---|---|---|---|"] + \
         [f"| {r['division']} | {r['title']} | ${r['low']:,.0f} | ${r['total']:,.0f} | ${r['high']:,.0f} | {r['pct']}% |" for r in summary] + \
         ["", "| Markup | % | Amount | Basis |", "|---|---|---|---|"] + [f"| {m.name} | {m.pct} | ${m.amount:,.0f} | {m.basis} |" for m in markups] + \
         ["", "## Benchmark", ""] + [f"- {c['check']}: {c['value']} vs {c['band']} → **{c['status']}** ({c['source']})" for c in bench["checks"]] + \
         ["", "## Assumptions (defaults used)", ""] + [f"- {a}" for a in basis.assumptions] + \
         ["", "## Skipped assemblies", ""] + ([f"- {x}" for x in skipped] or ["- none"]) + ["", meta["disclaimer"]]
    _write(folder / "06-estimate.md", "\n".join(md) + "\n")
    review(folder)
    report(folder)
    return folder

def run_all(vault_root: Path, package_dir: Path, name: str, building_type: str, city: str, aace_class: int = 2, render: bool = False) -> Path:
    """Unattended demo path (--no-llm): every open question is auto-assumed and stated."""
    folder = intake(vault_root, package_dir, name, building_type, city, aace_class, render=render)
    seed_takeoff(folder)
    rfi(folder)
    resume(folder, auto_assume=True)
    price(folder, vault_root)
    review(folder)
    report(folder)
    approve(folder, vault_root)
    return folder
