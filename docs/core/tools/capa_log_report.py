"""CAPA log report generator.

Scores a list of open/closed 8D/CAPA records through the `capa_8d` tool and
writes a filed 2-sheet .xlsx:

  • Summary — counts by status, P1 count, escalation count, and the CAPAs that
              need attention (escalate / overdue), most urgent first
  • Log     — one row per CAPA (status, completeness, discipline, priority,
              escalate, next action), most urgent first

Every value is computed by `capa_8d`, so the log can never disagree with the tool.
"""
from __future__ import annotations
from datetime import date
from pathlib import Path

from core.tools.capa_8d import Capa8D, _DISCLAIMER

_C = Capa8D()

_QUERY_KEYS = ("step", "days_open", "sla_days", "severity", "containment", "recurrence")
_STATUS_RANK = {"Overdue": 0, "At Risk": 1, "On Track": 2, "Closed": 3}
_LOG_HEADER = (
    "CAPA", "Status", "Complete %", "Current discipline", "Priority",
    "Escalate", "Next action",
)


def score_capa(capa: dict) -> dict:
    return _C.run(_capa_query(capa)).data


def build_capa_log_report(capas: list[dict], out_path: str | Path, *, as_of: str | None = None) -> Path:
    from openpyxl import Workbook

    if not capas:
        raise ValueError("need at least one CAPA")
    as_of = as_of or date.today().isoformat()
    scored = [(c, score_capa(c)) for c in capas]
    scored.sort(key=lambda cd: (
        _STATUS_RANK.get(cd[1].get("status"), 9),
        not cd[1].get("escalate", False),
        -cd[1].get("aging_ratio", 0.0),
    ))

    wb = Workbook()
    wb.remove(wb.active)
    _sheet_summary(wb, scored, as_of)
    _sheet_log(wb, scored, as_of)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(out_path))
    return out_path


def _sheet_summary(wb, scored, as_of):
    ws = wb.create_sheet("Summary")
    _title(ws, "CAPA / 8D Log Summary", as_of, ncols=2)
    statuses = [d.get("status") for _, d in scored]
    rows = [
        ("Total CAPAs", len(scored)),
        ("Overdue", statuses.count("Overdue")),
        ("At Risk", statuses.count("At Risk")),
        ("On Track", statuses.count("On Track")),
        ("Closed", statuses.count("Closed")),
        ("P1 (top priority)", sum(1 for _, d in scored if d.get("priority") == "P1")),
        ("Needs escalation", sum(1 for _, d in scored if d.get("escalate"))),
    ]
    _header_row(ws, 4, ["Metric", "Value"])
    r = 5
    for label, val in rows:
        ws.cell(r, 1, label)
        ws.cell(r, 2, val)
        r += 1
    r += 1
    ws.cell(r, 1, "Needs attention (escalate / overdue)").font = _bold()
    r += 1
    _header_row(ws, r, ["CAPA", "Status", "Priority", "Recommended action"])
    r += 1
    attention = [(c, d) for c, d in scored if d.get("escalate")]
    for c, d in attention[:10]:
        ws.cell(r, 1, str(d.get("capa", c.get("capa", "?"))))
        ws.cell(r, 2, d.get("status", ""))
        ws.cell(r, 3, d.get("priority", ""))
        ws.cell(r, 4, d.get("recommended_action", ""))
        r += 1
    if not attention:
        ws.cell(r, 1, "None — no CAPA needs escalation.").font = _italic()
        r += 1
    _note(ws, r + 1, _DISCLAIMER, ncols=4)
    _autofit(ws, {1: 20, 2: 12, 3: 10, 4: 66})


def _sheet_log(wb, scored, as_of):
    ws = wb.create_sheet("Log")
    _title(ws, "CAPA / 8D Log — most urgent first", as_of, ncols=len(_LOG_HEADER))
    _header_row(ws, 4, list(_LOG_HEADER))
    r = 5
    for c, d in scored:
        ws.cell(r, 1, str(d.get("capa", c.get("capa", "?"))))
        ws.cell(r, 2, d.get("status", ""))
        ws.cell(r, 3, d.get("completeness_pct", 0.0)).number_format = "0.0"
        ws.cell(r, 4, d.get("current_discipline", ""))
        ws.cell(r, 5, d.get("priority", ""))
        ws.cell(r, 6, "yes" if d.get("escalate") else "")
        ws.cell(r, 7, d.get("next_action", ""))
        r += 1
    _note(ws, r + 1, _DISCLAIMER, ncols=len(_LOG_HEADER))
    _autofit(ws, {1: 16, 2: 10, 4: 30, 7: 52})
    ws.freeze_panes = "B5"


# ---- helpers ----
def _capa_query(capa: dict) -> str:
    name = capa.get("capa", capa.get("id", ""))
    parts = [f"capa {name}".strip()]
    for k in _QUERY_KEYS:
        if capa.get(k) is not None:
            parts.append(f"{k}={capa[k]}")
    return " ".join(str(p) for p in parts)


def _bold():
    from openpyxl.styles import Font
    return Font(bold=True)


def _italic():
    from openpyxl.styles import Font
    return Font(italic=True, color="555555")


def _title(ws, text, as_of, ncols):
    from openpyxl.styles import Font
    ws.cell(1, 1, text).font = Font(bold=True, size=14)
    ws.cell(2, 1, f"As of {as_of} · process aid — confirm records in the QMS").font = _italic()
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
