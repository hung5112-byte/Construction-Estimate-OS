"""Broker-ready landed-cost workbook generator.

Turns a list of sourcing scenarios (same params the `landed_cost` tool accepts)
into a multi-sheet .xlsx a customs broker can review:

  • Inputs      — every rate/assumption, dated, with a verify-with-broker note
  • <Scenario>  — one sheet per scenario: cost build-up ex-works → landed/unit
  • Comparison  — scenarios side by side + delta vs cheapest + tariff share
  • Sensitivity — tariff swing table: at what additional-tariff rate the winner flips

Every number is computed by the `landed_cost` tool (single source of truth), so
the workbook can never disagree with the engine. Rates are the caller's inputs and
carry the tool's own "verify with a licensed customs broker" caveat.
"""
from __future__ import annotations
import re
from datetime import date
from pathlib import Path

from core.tools.landed_cost import LandedCost, _DISCLAIMER

_LC = LandedCost()

# scenario dict keys that map straight to `landed_cost` query params
_QUERY_KEYS = (
    "units", "duty", "tariff", "freight", "freight_unit", "insurance",
    "hmf", "mpf", "broker", "transit_days", "cost_of_capital", "cv",
)

# (row label, ToolResult.data key) — the ex-works → landed build-up, in order
_BUILD_UP = (
    ("Ex-works unit price", "ex_works_unit"),
    ("+ Freight / unit", "freight_unit"),
    ("+ Insurance / unit", "insurance_unit"),
    ("+ Base HTS duty", "base_duty_unit"),
    ("+ Additional tariff (e.g. §301)", "tariff_unit"),
    ("+ MPF (merchandise processing)", "mpf_unit"),
    ("+ HMF (harbor maintenance, ocean)", "hmf_unit"),
    ("+ Customs broker / unit", "broker_unit"),
    ("+ In-transit carrying cost", "in_transit_carrying_unit"),
    ("= LANDED COST / unit", "landed_unit"),
)

# (row label, key, kind) for the Inputs sheet
_INPUT_ROWS = (
    ("Ex-works unit price ($)", "ex_works", "money"),
    ("Units per entry", "units", "int"),
    ("Base HTS duty (%)", "duty", "pct"),
    ("Additional tariff — §301 etc. (%)", "tariff", "pct"),
    ("Freight per shipment ($)", "freight", "money"),
    ("HMF — ocean only (%)", "hmf", "pct"),
    ("Customs broker per shipment ($)", "broker", "money"),
    ("Transit days", "transit_days", "int"),
    ("Cost of capital — annual (%)", "cost_of_capital", "pct"),
)

_MONEY_UNIT = '$#,##0.0000'
_MONEY_TOTAL = '$#,##0.00'
_PCT = '0.0"%"'


def compute_scenario(scenario: dict) -> dict:
    """Run one scenario through the landed_cost tool → its data dict."""
    return _LC.run(_scenario_query(scenario)).data


def build_landed_cost_workbook(
    scenarios: list[dict],
    out_path: str | Path,
    *,
    as_of: str | None = None,
    tariff_swing_max: float = 50.0,
    tariff_swing_step: float = 5.0,
) -> Path:
    """Build a broker-ready landed-cost workbook.

    Args:
        scenarios: list of dicts, each with a `name` plus any `landed_cost`
            params (ex_works, units, duty, tariff, freight, hmf, broker,
            transit_days, cost_of_capital, ...).
        out_path: destination .xlsx path.
        as_of: as-of date string (defaults to today) stamped on every sheet.
        tariff_swing_max/step: range for the Sensitivity tariff sweep (percent).

    Returns:
        The written Path.
    """
    from openpyxl import Workbook

    if not scenarios:
        raise ValueError("need at least one scenario")

    as_of = as_of or date.today().isoformat()
    computed = [(s, compute_scenario(s)) for s in scenarios]

    wb = Workbook()
    wb.remove(wb.active)  # drop default sheet; we add named ones

    _sheet_inputs(wb, computed, as_of)
    used_titles: set[str] = set()
    for scenario, data in computed:
        _sheet_scenario(wb, scenario, data, as_of, used_titles)
    _sheet_comparison(wb, computed, as_of)
    _sheet_sensitivity(wb, computed, as_of, tariff_swing_max, tariff_swing_step)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(out_path))
    return out_path


# ────────────────────────── sheet builders ──────────────────────────
def _sheet_inputs(wb, computed, as_of):
    ws = wb.create_sheet("Inputs")
    names = [s.get("name", f"Scenario {i+1}") for i, (s, _) in enumerate(computed)]
    _title(ws, "Landed-Cost Inputs & Assumptions", as_of, ncols=len(names) + 2)

    header = ["Parameter", *names, "Source / verify"]
    _header_row(ws, 4, header)
    verify = "Verify HTS code + all duty/tariff rates with a licensed customs broker"
    r = 5
    for label, key, kind in _INPUT_ROWS:
        ws.cell(r, 1, label)
        for c, (s, _) in enumerate(computed, start=2):
            cell = ws.cell(r, c, _as_num(s.get(key)))
            cell.number_format = {"money": _MONEY_TOTAL, "pct": _PCT}.get(kind, "0")
        ws.cell(r, len(names) + 2, verify if kind == "pct" else "")
        r += 1
    _note(ws, r + 1, _DISCLAIMER, ncols=len(names) + 2)
    _autofit(ws, {1: 34, len(names) + 2: 52})
    ws.freeze_panes = "B5"


def _sheet_scenario(wb, scenario, data, as_of, used_titles):
    title = _safe_title(scenario.get("name", "Scenario"), used_titles)
    ws = wb.create_sheet(title)
    _title(ws, f"Cost Build-Up — {scenario.get('name', title)}", as_of, ncols=2)
    _header_row(ws, 4, ["Cost component ($/unit)", "Amount"])
    r = 5
    for label, key in _BUILD_UP:
        ws.cell(r, 1, label)
        cell = ws.cell(r, 2, _as_num(data.get(key)))
        cell.number_format = _MONEY_UNIT
        if key == "landed_unit":
            for c in (1, 2):
                ws.cell(r, c).font = _bold()
        r += 1
    # tariff share callout
    r += 1
    ws.cell(r, 1, "Additional-tariff share of landed cost").font = _bold()
    ws.cell(r, 2, _as_num(data.get("tariff_share_pct"))).number_format = _PCT
    ws.cell(r + 1, 1, "Biggest add-on cost driver")
    ws.cell(r + 1, 2, str(data.get("biggest_add_on_driver") or "—"))
    _note(ws, r + 3, _DISCLAIMER, ncols=2)
    _autofit(ws, {1: 38, 2: 16})


def _sheet_comparison(wb, computed, as_of):
    ws = wb.create_sheet("Comparison")
    names = [s.get("name", f"Scenario {i+1}") for i, (s, _) in enumerate(computed)]
    _title(ws, "Scenario Comparison — total landed cost wins", as_of, ncols=len(names) + 1)
    _header_row(ws, 4, ["Cost component ($/unit)", *names])
    r = 5
    for label, key in _BUILD_UP:
        ws.cell(r, 1, label)
        for c, (_, data) in enumerate(computed, start=2):
            cell = ws.cell(r, c, _as_num(data.get(key)))
            cell.number_format = _MONEY_UNIT
            if key == "landed_unit":
                cell.font = _bold()
        if key == "landed_unit":
            ws.cell(r, 1).font = _bold()
        r += 1

    landeds = [data.get("landed_unit", 0.0) for _, data in computed]
    best = min(landeds)
    best_name = names[landeds.index(best)]
    # delta vs cheapest
    ws.cell(r, 1, "Δ vs cheapest / unit").font = _bold()
    for c, land in enumerate(landeds, start=2):
        cell = ws.cell(r, c, round(land - best, 4))
        cell.number_format = _MONEY_UNIT
    r += 1
    # delta per entry (× units)
    ws.cell(r, 1, "Δ vs cheapest / entry").font = _bold()
    for c, (s, data) in enumerate(computed, start=2):
        units = data.get("units_per_entry", 1)
        cell = ws.cell(r, c, round((data.get("landed_unit", 0.0) - best) * units, 2))
        cell.number_format = _MONEY_TOTAL
    r += 2
    ws.cell(r, 1, f"Lowest landed cost: {best_name} (${best:,.4f}/unit)").font = _bold()
    _note(ws, r + 2, _DISCLAIMER, ncols=len(names) + 1)
    _autofit(ws, {1: 34})
    ws.freeze_panes = "B5"


def _sheet_sensitivity(wb, computed, as_of, swing_max, step):
    """Sweep the additional tariff on the currently-costliest tariffed scenario and
    show at what rate the cheapest alternative overtakes / is overtaken."""
    ws = wb.create_sheet("Sensitivity")

    # primary = scenario with the highest current landed cost (the one a tariff bites)
    primary_s, _primary_d = max(computed, key=lambda sd: sd[1].get("landed_unit", 0.0))
    others = [(s, d) for s, d in computed if s is not primary_s]

    _title(ws, "Tariff Sensitivity — does the decision flip?", as_of, ncols=4)
    p_name = primary_s.get("name", "Primary")
    if not others:
        _note(ws, 4, "Only one scenario supplied — add an alternative origin to compare.", ncols=4)
        _autofit(ws, {1: 28})
        return

    alt_s, alt_d = min(others, key=lambda sd: sd[1].get("landed_unit", 0.0))
    alt_name = alt_s.get("name", "Alternative")
    alt_landed = alt_d.get("landed_unit", 0.0)

    ws.cell(3, 1, f"Sweeping additional tariff on {p_name}; {alt_name} held fixed "
                  f"at ${alt_landed:,.4f}/unit").font = _italic()
    _header_row(ws, 4, [f"{p_name} tariff (%)", f"{p_name} landed",
                        f"{alt_name} landed", "Winner"])

    r = 5
    n = int(swing_max / step)
    flip_note = None
    prev_winner = None
    for i in range(n + 1):
        tpct = round(i * step, 4)
        scen = dict(primary_s)
        scen["tariff"] = tpct
        d = compute_scenario(scen)
        p_landed = d.get("landed_unit", 0.0)
        winner = p_name if p_landed < alt_landed else alt_name
        ws.cell(r, 1, tpct).number_format = _PCT
        ws.cell(r, 2, round(p_landed, 4)).number_format = _MONEY_UNIT
        ws.cell(r, 3, round(alt_landed, 4)).number_format = _MONEY_UNIT
        ws.cell(r, 4, winner)
        if prev_winner and winner != prev_winner and flip_note is None:
            flip_note = (f"Decision flips between {tpct - step:.0f}% and {tpct:.0f}% "
                         f"additional tariff on {p_name}.")
        prev_winner = winner
        r += 1

    ws.cell(r + 1, 1, flip_note or
            f"No flip in 0–{swing_max:.0f}% range — {prev_winner} stays cheapest throughout."
            ).font = _bold()
    _note(ws, r + 3, _DISCLAIMER, ncols=4)
    _autofit(ws, {1: 18, 2: 16, 3: 16, 4: 16})
    ws.freeze_panes = "A5"


# ────────────────────────── formatting helpers ──────────────────────────
def _scenario_query(s: dict) -> str:
    ex = s.get("ex_works", s.get("ex"))
    if ex is None:
        raise ValueError(f"scenario '{s.get('name', '?')}' missing ex_works")
    parts = [f"landed {ex}"]
    for k in _QUERY_KEYS:
        if s.get(k) is not None:
            parts.append(f"{k}={s[k]}")
    return " ".join(str(p) for p in parts)


def _as_num(v):
    if v is None:
        return 0
    try:
        return float(v)
    except (TypeError, ValueError):
        return v


def _safe_title(name: str, used: set[str]) -> str:
    t = re.sub(r"[:\\/?*\[\]]", "-", str(name))[:28] or "Scenario"
    base, i = t, 2
    while t in used:
        t = f"{base[:26]}-{i}"
        i += 1
    used.add(t)
    return t


def _bold():
    from openpyxl.styles import Font
    return Font(bold=True)


def _italic():
    from openpyxl.styles import Font
    return Font(italic=True, color="555555")


def _title(ws, text, as_of, ncols):
    from openpyxl.styles import Font
    ws.cell(1, 1, text).font = Font(bold=True, size=14)
    ws.cell(2, 1, f"As of {as_of} · general estimate — verify with customs broker").font = _italic()
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
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left")


def _note(ws, row, text, ncols):
    cell = ws.cell(row, 1, f"⚠ {text}")
    cell.font = _italic()
    if ncols > 1:
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)


def _autofit(ws, widths: dict[int, int]):
    from openpyxl.utils import get_column_letter
    for col, w in widths.items():
        ws.column_dimensions[get_column_letter(col)].width = w
