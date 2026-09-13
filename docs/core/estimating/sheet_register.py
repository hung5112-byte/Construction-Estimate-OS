"""Sheet register: every page of every drawing PDF → sheet id, title, discipline, scale, revision.

This is document control. Readers never take off from a sheet that is not in the register, and a
sheet without a parsable scale cannot produce measured quantities (the scale gate).
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from core.estimating.pdfio import (
    Scale,
    is_not_to_scale,
    open_pdf,
    page_size_in,
    parse_scale,
    sheet_size_name,
)
from core.estimating.sheet_text import text_lines, title_block_text, words

# NCS discipline designators (National CAD Standard) — one or two letters
DISCIPLINES = {
    "G": "General", "H": "Hazardous Materials", "V": "Survey/Mapping", "B": "Geotechnical", "C": "Civil",
    "L": "Landscape", "S": "Structural", "A": "Architectural", "I": "Interiors", "Q": "Equipment",
    "F": "Fire Protection", "FP": "Fire Protection", "FA": "Fire Alarm", "P": "Plumbing", "D": "Process",
    "M": "Mechanical", "E": "Electrical", "W": "Distributed Energy", "T": "Telecommunications",
    "R": "Resource", "X": "Other", "Z": "Contractor/Shop", "O": "Operations",
}
SHEET_TYPES = {"0": "general", "1": "plans", "2": "elevations", "3": "sections", "4": "large-scale views",
               "5": "details", "6": "schedules and diagrams", "7": "user-defined", "8": "user-defined", "9": "3D"}
# Discipline group each reader department owns
DISCIPLINE_GROUP = {
    "G": "01-bid-coordination", "C": "02-civil-structural", "L": "02-civil-structural", "S": "02-civil-structural",
    "B": "02-civil-structural", "V": "02-civil-structural", "A": "03-architectural", "I": "03-architectural",
    "Q": "03-architectural", "M": "04-mep", "P": "04-mep", "F": "04-mep", "FP": "04-mep", "FA": "04-mep",
    "E": "04-mep", "T": "04-mep", "D": "04-mep",
}

_SHEET_ID_RE = re.compile(r"^(?P<disc>[A-Z]{1,2})-?(?P<num>\d{3})(?:\.\d{1,2})?[A-Z]?$")
_REV_RE = re.compile(r"\bREV(?:ISION)?[:.\s#]*\s*(?P<rev>\d{1,2}|[A-Z])\b")
_DATE_RE = re.compile(r"\b(\d{1,2}/\d{1,2}/\d{4})\b")


@dataclass
class SheetInfo:
    file: str
    page_index: int
    sheet_id: str
    title: str
    discipline: str
    discipline_name: str
    sheet_type: str
    reader_department: str
    scale_label: str | None
    pt_per_ft: float | None
    not_to_scale: bool
    revision: str | None
    date: str | None
    width_in: float
    height_in: float
    size_name: str
    is_vector: bool
    word_count: int
    line_count: int
    rect_count: int
    curve_count: int

    @property
    def scale(self) -> Scale | None:
        if self.scale_label and self.pt_per_ft:
            return parse_scale(self.scale_label)
        return None


def _pick_sheet_id(lines, page_w: float, page_h: float) -> str | None:
    """Prefer an id inside the title block region and the largest font; fall back to any id."""
    cands = []
    for ln in lines:
        for w in ln.words:
            m = _SHEET_ID_RE.match(w.text.strip())
            if m:
                in_tb = w.x0 >= page_w * 0.70 and w.top >= page_h * 0.75
                cands.append((in_tb, w.size, w.text.strip()))
    if not cands:
        return None
    cands.sort(key=lambda c: (c[0], c[1]), reverse=True)
    return cands[0][2]


def _pick_title(lines, sheet_id: str | None, page_w: float, page_h: float) -> str:
    tb = [ln for ln in lines if ln.x0 >= page_w * 0.70 and ln.top >= page_h * 0.75]
    # explicit label
    for i, ln in enumerate(tb):
        if ln.text.strip().upper() == "SHEET TITLE" and i + 1 < len(tb):
            return tb[i + 1].text.strip()
    # else: largest non-id, non-scale line in the title block
    best = None
    for ln in tb:
        t = ln.text.strip()
        if not t or t == sheet_id or t.upper().startswith(("SCALE", "DATE", "REV", "SHEET NUMBER", "PROJECT")):
            continue
        if best is None or ln.size > best.size:
            best = ln
    return best.text.strip() if best else ""


def describe_page(page, file: str, page_index: int) -> SheetInfo:
    w_in, h_in = page_size_in(page)
    ws = words(page)
    lines = text_lines(ws)
    pw, ph = float(page.width), float(page.height)
    tb_text = title_block_text(lines, pw, ph)
    all_text = "\n".join(ln.text for ln in lines)
    sheet_id = _pick_sheet_id(lines, pw, ph) or f"{Path(file).stem}"
    m = _SHEET_ID_RE.match(sheet_id)
    disc = m.group("disc") if m else ""
    num = m.group("num") if m else ""
    scale = parse_scale(tb_text) or parse_scale(all_text)
    nts = is_not_to_scale(tb_text) if not scale else False
    rev = _REV_RE.search(tb_text)
    date = _DATE_RE.search(tb_text)
    return SheetInfo(
        file=file, page_index=page_index, sheet_id=sheet_id, title=_pick_title(lines, sheet_id, pw, ph),
        discipline=disc, discipline_name=DISCIPLINES.get(disc, "Unknown"),
        sheet_type=SHEET_TYPES.get(num[:1], "unknown") if num else "unknown",
        reader_department=DISCIPLINE_GROUP.get(disc, "01-bid-coordination"),
        scale_label=scale.label if scale else None, pt_per_ft=scale.pt_per_ft if scale else None,
        not_to_scale=nts, revision=rev.group("rev") if rev else None, date=date.group(1) if date else None,
        width_in=round(w_in, 2), height_in=round(h_in, 2), size_name=sheet_size_name(w_in, h_in),
        is_vector=len(ws) >= 25, word_count=len(ws), line_count=len(page.lines), rect_count=len(page.rects),
        curve_count=len(page.curves),
    )


def build_register(pdf_paths: list[Path]) -> list[SheetInfo]:
    out: list[SheetInfo] = []
    for p in pdf_paths:
        with open_pdf(p) as pdf:
            for i, page in enumerate(pdf.pages):
                out.append(describe_page(page, p.name, i))
    return out


def completeness(register: list[SheetInfo], index_ids: list[str]) -> dict:
    have = {s.sheet_id for s in register}
    want = {i.strip() for i in index_ids if i.strip()}
    return {"missing_from_package": sorted(want - have), "not_in_index": sorted(have - want),
            "duplicates": sorted({s.sheet_id for s in register if sum(1 for t in register if t.sheet_id == s.sheet_id) > 1})}


def register_markdown(register: list[SheetInfo], completeness_info: dict | None = None) -> str:
    out = ["---", "type: sheet_register", f"sheets: {len(register)}", "---", "# Sheet register", "",
           "| # | Sheet | Title | Discipline | Type | Scale | Rev | Date | Size | Vector | Reader dept |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, s in enumerate(register, 1):
        scale = s.scale_label or ("NTS" if s.not_to_scale else "⚠ none")
        out.append(f"| {k} | **{s.sheet_id}** | {s.title} | {s.discipline_name} | {s.sheet_type} | {scale} | "
                   f"{s.revision or ''} | {s.date or ''} | {s.size_name} | {'yes' if s.is_vector else '⚠ scanned'} | {s.reader_department} |")
    unscaled = [s.sheet_id for s in register if not s.scale_label and s.sheet_type in ("plans", "elevations", "sections")]
    scanned = [s.sheet_id for s in register if not s.is_vector]
    out += ["", "## Gates", f"- Scale gate: {len(unscaled)} measured-type sheet(s) without a parsable scale{': ' + ', '.join(unscaled) if unscaled else ''}",
            f"- Scanned sheets (no text layer): {len(scanned)}{': ' + ', '.join(scanned) if scanned else ''}"]
    if completeness_info:
        out += ["", "## Completeness vs cover-sheet index",
                f"- Missing from package: {', '.join(completeness_info['missing_from_package']) or 'none'}",
                f"- Not in index: {', '.join(completeness_info['not_in_index']) or 'none'}",
                f"- Duplicates: {', '.join(completeness_info['duplicates']) or 'none'}"]
    return "\n".join(out) + "\n"


def register_json(register: list[SheetInfo]) -> str:
    return json.dumps([asdict(s) for s in register], indent=2)
