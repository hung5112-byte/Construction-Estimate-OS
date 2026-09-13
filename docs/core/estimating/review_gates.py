"""Deterministic review gates — pure functions, zero LLM calls, the estimate's hard floor.

G1 every measured sheet claimed        G2 every quantity has sheet+revision+method
G3 spec divisions covered              G4 arithmetic ties ledger→lines→summary
G5 units valid for the division        G6 $/SF inside the building-type band (or overridden)
G7 CRITICAL RFIs answered/assumed      G8 scale gate passed on measured sheets
G9 confidence floor                    G10 no unpriced lines above the materiality threshold
G11 every allowance sourced            G12 every high risk mitigated (exclusion / RFI / allowance)
G13 client-facing text passes the client-safe scan     G3b (ROM) every playbook trade covered or excluded
A failed blocking gate makes the verdict REVISE regardless of the judged review — same philosophy
as the critic loop: the model may add issues, never remove a gate failure.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from core.estimating.takeoff_ledger import DIVISION_UNITS


@dataclass
class GateResult:
    id: str
    name: str
    passed: bool
    blocking: bool
    details: str
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def run_gates(register: list[dict], ledger_items: list[dict], priced_lines: list[dict], summary: list[dict],
              spec_sections: list[dict], rfi_questions: list[dict], benchmark: dict, gross_sf: float,
              confidence_floor: float = 0.6, materiality_pct: float = 1.0, per_sf_override: bool = False,
              excluded_divisions: dict | None = None, playbook_trades: dict | None = None, risks: list[dict] | None = None,
              client_findings: list[dict] | None = None) -> list[GateResult]:
    """`playbook_trades`: {trade: excluded_reason|None} for ROM runs (G3b). `risks`: risk register rows with
    `severity` and `mitigation` (G12). `client_findings`: client-safe scan findings on client-facing text (G13)."""
    gates: list[GateResult] = []
    excluded_divisions = excluded_divisions or {}
    measured_types = {"plans", "elevations", "sections", "large-scale views"}

    # G1 — every measured-type sheet claimed by at least one ledger line (schedules/general may be unclaimed)
    used = {it["sheet"] for it in ledger_items}
    measured = [s for s in register if s.get("sheet_type") in measured_types]
    unclaimed = [s["sheet_id"] for s in measured if s["sheet_id"] not in used]
    gates.append(GateResult("G1", "Every measured sheet is claimed by the takeoff", not unclaimed, True,
                            f"{len(measured) - len(unclaimed)}/{len(measured)} measured sheets claimed", unclaimed))

    # G2 — provenance on every line
    bad = [it["id"] for it in ledger_items if not it.get("sheet") or not it.get("method")]
    gates.append(GateResult("G2", "Every quantity carries sheet + method provenance", not bad, True,
                            f"{len(ledger_items) - len(bad)}/{len(ledger_items)} lines with provenance", bad))

    # G3 — spec divisions with technical sections have ledger lines (Division 00/01 exempt)
    spec_divs = {s["division"] for s in spec_sections if s["division"] not in ("00", "01")}
    led_divs = {it["division"] for it in ledger_items}
    excluded = {d for d in excluded_divisions if d in spec_divs}
    missing = sorted(spec_divs - led_divs - excluded)
    gates.append(GateResult("G3", "Every technical spec division has takeoff lines or a cited exclusion", not missing, True,
                            f"{len(spec_divs) - len(missing)}/{len(spec_divs)} spec divisions covered"
                            + (f"; excluded with citation: {', '.join(sorted(excluded))}" if excluded else ""), missing))
    if playbook_trades is not None:
        # G3b — every playbook trade has lines or a stated exclusion (ROM runs have no spec index)
        covered = {(it.get("tags") or {}).get("trade") for it in ledger_items}
        missing_trades = sorted(t for t, why in playbook_trades.items() if not why and t not in covered)
        gates.append(GateResult("G3b", "Every playbook trade has takeoff lines or a stated exclusion", not missing_trades, True,
                                f"{len(playbook_trades) - len(missing_trades)}/{len(playbook_trades)} trades covered", missing_trades))

    # G4 — arithmetic ties: sum of priced lines == sum of summary totals
    lines_total = round(sum(p["total"] for p in priced_lines), 2)
    summary_total = round(sum(r["total"] for r in summary), 2)
    line_ext_ok = all(abs(round(p["labor"] + p["material"] + p["equipment"] + p["sub"], 2) - round(p["total"], 2)) <= 0.05 for p in priced_lines)
    ties = abs(lines_total - summary_total) <= 0.05 and line_ext_ok
    gates.append(GateResult("G4", "Arithmetic ties from lines to summary", ties, True,
                            f"lines ${lines_total:,.2f} vs summary ${summary_total:,.2f}; extensions {'ok' if line_ext_ok else 'BROKEN'}"))

    # G5 — units valid for division
    bad_units = [f"{it['id']} {it['unit']} in div {it['division']}" for it in ledger_items
                 if DIVISION_UNITS.get(it["division"]) and it["unit"] not in DIVISION_UNITS[it["division"]] and it["unit"] != "LS"
                 and it.get("pricing_basis") != "assembly"]
    gates.append(GateResult("G5", "Units are valid for their division", not bad_units, True,
                            f"{len(bad_units)} unit problems", bad_units))

    # G6 — $/SF inside band (non-blocking if explicitly overridden with a reason)
    band = next((c for c in benchmark.get("checks", []) if c["check"].startswith("$/SF")), None)
    inside = bool(band and band["status"] in ("inside", "no-band"))
    gates.append(GateResult("G6", "$/SF inside the building-type benchmark band", inside or per_sf_override, not per_sf_override,
                            f"{band['value'] if band else '?'} $/SF vs band {band['band'] if band else '?'} → {band['status'] if band else 'n/a'}",
                            [band["source"]] if band else []))

    # G7 — CRITICAL questions answered or carried as assumptions
    open_crit = [q["text"][:80] for q in rfi_questions if q.get("severity") == "CRITICAL" and not q.get("answer") and not q.get("assumption")]
    gates.append(GateResult("G7", "Every CRITICAL question is answered or carried as a written assumption", not open_crit, True,
                            f"{len(open_crit)} open CRITICAL question(s)", open_crit))

    # G8 — scale gate: measured sheets that produced quantities must have a scale
    unscaled = [s["sheet_id"] for s in register if s.get("sheet_type") in measured_types and not s.get("scale_label")
                and s["sheet_id"] in used and any(it["method"] in ("vector", "vision") for it in ledger_items if it["sheet"] == s["sheet_id"])]
    gates.append(GateResult("G8", "Measured quantities come only from sheets with a parsed scale", not unscaled, True,
                            f"{len(unscaled)} sheet(s) measured without a scale", unscaled))

    # G9 — confidence floor (non-blocking; they go to the verify-before-bid list)
    low = [f"{it['id']} {it['description'][:40]} ({it['confidence']:.2f})" for it in ledger_items if it["confidence"] < confidence_floor]
    gates.append(GateResult("G9", f"Lines below the confidence floor ({confidence_floor}) are listed for verification", True, False,
                            f"{len(low)} line(s) below floor — verify before bid", low))

    # G10 — unpriced lines above materiality (by count share, since they have no $)
    unpriced = [p["item_code"] for p in priced_lines if "UNPRICED" in p.get("flags", [])]
    share = (len(unpriced) / len(priced_lines) * 100) if priced_lines else 0
    gates.append(GateResult("G10", "Unpriced lines stay below the materiality threshold", share <= materiality_pct * 5, True,
                            f"{len(unpriced)} unpriced of {len(priced_lines)} ({share:.1f}% of lines; threshold {materiality_pct * 5:.0f}%)", unpriced))

    # G11 — every allowance carries an amount and a source (spec page or intake)
    bad_allow = [it["id"] for it in ledger_items if it.get("method") == "allowance"
                 and not (float((it.get("tags") or {}).get("amount") or 0) > 0 and ((it.get("tags") or {}).get("page") or (it.get("tags") or {}).get("source")))]
    n_allow = sum(1 for it in ledger_items if it.get("method") == "allowance")
    gates.append(GateResult("G11", "Every allowance has an amount and a source", not bad_allow, True,
                            f"{n_allow - len(bad_allow)}/{n_allow} allowances sourced", bad_allow))

    # G12 — every high-severity risk has a mitigation (exclusion, RFI or allowance)
    if risks is not None:
        unmitigated = [r["risk"] for r in risks if r.get("severity") == "high" and not (r.get("mitigation") or {}).get("type") or
                       (r.get("severity") == "high" and (r.get("mitigation") or {}).get("type") == "none")]
        n_high = sum(1 for r in risks if r.get("severity") == "high")
        gates.append(GateResult("G12", "Every high-severity risk has an exclusion, an RFI or an allowance", not unmitigated, True,
                                f"{n_high - len(unmitigated)}/{n_high} high risks mitigated", unmitigated))
    else:
        gates.append(GateResult("G12", "Every high-severity risk has an exclusion, an RFI or an allowance", True, False, "no risk register on this run"))

    # G13 — client-facing text passed the client-safe scan (no blocking findings)
    if client_findings is not None:
        blockers = [f"{f['category']}: {f['term']} (line {f['line_no']})" for f in client_findings if f.get("severity") == "blocking"]
        gates.append(GateResult("G13", "Client-facing text has no internal cost, blame, legal admission or raw language", not blockers, True,
                                f"{len(blockers)} blocking finding(s), {sum(1 for f in client_findings if f.get('severity') != 'blocking')} warning(s)", blockers))
    else:
        gates.append(GateResult("G13", "Client-facing text has no internal cost, blame, legal admission or raw language", True, False, "no client-facing text on this run"))
    return gates


def verdict(gates: list[GateResult]) -> str:
    return "REVISE" if any(g.blocking and not g.passed for g in gates) else "APPROVE"


def scorecard_markdown(gates: list[GateResult], judged: list[dict] | None = None) -> str:
    v = verdict(gates)
    out = ["---", "type: review_scorecard", f"verdict: {v}", "---", f"# Review scorecard — verdict: **{v}**", "",
           "## Hard gates (deterministic)", "", "| Gate | Check | Result | Details |", "|---|---|---|---|"]
    for g in gates:
        res = "✅ pass" if g.passed else ("❌ FAIL (blocking)" if g.blocking else "⚠ warn")
        out.append(f"| {g.id} | {g.name} | {res} | {g.details} |")
    for g in gates:
        if g.evidence and (not g.passed or g.id == "G9"):
            out += ["", f"### {g.id} evidence", *[f"- {e}" for e in g.evidence[:40]]]
    if judged:
        out += ["", "## Judged review (agents may add issues, never remove a gate failure)", "", "| Reviewer | Rubric | Score | Issues |", "|---|---|---|---|"]
        for j in judged:
            out.append(f"| {j.get('reviewer','')} | {j.get('rubric','')} | {j.get('score','')} | {'; '.join(j.get('issues', []))[:200]} |")
    return "\n".join(out) + "\n"
