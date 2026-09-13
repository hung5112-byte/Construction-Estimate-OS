"""BOM health report generator.

Scores a whole BOM (list of part dicts) through the `bom_health` tool and writes
a filed 2-sheet .xlsx:

  • Summary — BOM risk score + tier, counts by risk tier, single-source count,
              EOL/obsolete count, and the worst parts ranked
  • Parts   — one row per part (inputs + risk + tier + disposition), worst first

Every score is computed by `bom_health` (single source of truth), so the report
can never disagree with the tool.
"""
from __future__ import annotations
from datetime import date
from pathlib import Path

from core.tools.bom_health import BomHealth, _DISCLAIMER

_BH = BomHealth()

# part-dict keys that map straight to bom_health query params
_QUERY_KEYS = (
    "lifecycle", "sources", "avl", "lead_time", "coverage", "compliance",
    "ltb_days", "coverage_target", "lead_time_ceiling", "ltb_horizon",
)

_PARTS_HEADER = (
    "Part", "Lifecycle", "Sources", "Lead time (wk)", "Coverage (wk)",
    "Compliance", "Risk", "Tier", "Disposition",
)


def score_part(part: dict) -> dict:
    """Run one part dict through the bom_health tool → its data dict."""
    return _BH.run(_part_query(part)).data


def build_bom_health_report(
    parts: list[dict],
    out_path: str | Path,
    *,
    as_of: str | None = None,
) -> Path:
    """Score a BOM and write the 2-sheet health report .xlsx. Returns the Path."""
    from openpyxl import Workbook

    if not parts:
        raise ValueError("need at least one part")

    as_of = as_of or date.today().isoformat()
    scored = [(part, score_part(part)) for part in parts]
    # rank worst-first
    scored.sort(key=lambda pd: pd[1].get("risk_score", 0.0), reverse=True)

    wb = Workbook()
    wb.remove(wb.active)
    _sheet_summary(wb, scored, as_of)
    _sheet_parts(wb, scored, as_of)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(out_path))
    return out_path


def _sheet_summary(wb, scored, as_of):
    ws = wb.create_sheet("Summary")
    _title(ws, "BOM Health Summary", as_of, ncols=2)

    risks = [d.get("risk_score", 0.0) for _, d in scored]
    bom_risk = round(sum(risks) / len(risks), 2)
    tiers = [d.get("risk_tier") for _, d in scored]
    single = sum(1 for _, d in scored if d.get("single_source"))
    eol = sum(1 for _, d in scored if d.get("lifecycle") in ("EOL", "Obsolete"))

    rows = [
        ("BOM risk score (avg)", bom_risk),
        ("BOM risk tier", _tier(bom_risk)),
        ("Total parts", len(scored)),
        ("Critical parts", tiers.count("Critical")),
        ("High-risk parts", tiers.count("High")),
        ("Moderate-risk parts", tiers.count("Moderate")),
        ("Low-risk parts", tiers.count("Low")),
        ("Single-source parts", single),
        ("EOL / obsolete parts", eol),
    ]
    _header_row(ws, 4, ["Metric", "Value"])
    r = 5
    for label, val in rows:
        ws.cell(r, 1, label)
        cell = ws.cell(r, 2, val)
        if label.startswith("BOM risk score"):
            cell.number_format = "0.0"
            cell.font = _bold()
        r += 1

    r += 1
    ws.cell(r, 1, "Worst parts").font = _bold()
    r += 1
    _header_row(ws, r, ["Part", "Risk", "Tier", "Disposition"])
    r += 1
    for part, d in scored[:5]:
        ws.cell(r, 1, str(d.get("part", part.get("part", "?"))))
        ws.cell(r, 2, d.get("risk_score", 0.0)).number_format = "0.0"
        ws.cell(r, 3, d.get("risk_tier", ""))
        ws.cell(r, 4, d.get("disposition", ""))
        r += 1
    _note(ws, r + 1, _DISCLAIMER, ncols=4)
    _autofit(ws, {1: 24, 2: 12, 3: 12, 4: 60})


def _sheet_parts(wb, scored, as_of):
    ws = wb.create_sheet("Parts")
    _title(ws, "BOM Parts — worst first", as_of, ncols=len(_PARTS_HEADER))
    _header_row(ws, 4, list(_PARTS_HEADER))
    r = 5
    for part, d in scored:
        ws.cell(r, 1, str(d.get("part", part.get("part", "?"))))
        ws.cell(r, 2, d.get("lifecycle", ""))
        ws.cell(r, 3, _opt(part.get("sources", part.get("avl"))))
        ws.cell(r, 4, _opt(part.get("lead_time")))
        ws.cell(r, 5, _opt(part.get("coverage")))
        ws.cell(r, 6, str(part.get("compliance", "")))
        ws.cell(r, 7, d.get("risk_score", 0.0)).number_format = "0.0"
        ws.cell(r, 8, d.get("risk_tier", ""))
        ws.cell(r, 9, d.get("disposition", ""))
        r += 1
    _note(ws, r + 1, _DISCLAIMER, ncols=len(_PARTS_HEADER))
    _autofit(ws, {1: 22, 2: 12, 6: 14, 9: 60})
    ws.freeze_panes = "B5"


# ---- helpers ----
def _part_query(part: dict) -> str:
    name = part.get("part", part.get("name", ""))
    parts = [f"bom {name}".strip()]
    for k in _QUERY_KEYS:
        if part.get(k) is not None:
            parts.append(f"{k}={part[k]}")
    return " ".join(str(p) for p in parts)


def _opt(v):
    return "" if v is None else v


def _tier(score: float) -> str:
    if score >= 75:
        return "Critical"
    if score >= 50:
        return "High"
    if score >= 25:
        return "Moderate"
    return "Low"


def _bold():
    from openpyxl.styles import Font
    return Font(bold=True)


def _italic():
    from openpyxl.styles import Font
    return Font(italic=True, color="555555")


def _title(ws, text, as_of, ncols):
    from openpyxl.styles import Font
    ws.cell(1, 1, text).font = Font(bold=True, size=14)
    ws.cell(2, 1, f"As of {as_of} · general estimate — verify lifecycle/LTB with distributor").font = _italic()
    if ncols > 1:
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)


def _header_row(ws, row, headers):
    from openpyxl.styles import Font, PatternFill, Alignment
    fill = PatternFill("solid", fgColor="1F4E78")
    for c, h in enumerate(headers, start=1):
        cell = ws.cell(row, c, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = fill
        cell.alignment = Alignment(horizontal="left" if c == 1 else "center")


def _note(ws, row, text, ncols):
    cell = ws.cell(row, 1, f"⚠ {text}")
    cell.font = _italic()
    if ncols > 1:
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)


def _autofit(ws, widths):
    from openpyxl.utils import get_column_letter
    for col, w in widths.items():
        ws.column_dimensions[get_column_letter(col)].width = w
