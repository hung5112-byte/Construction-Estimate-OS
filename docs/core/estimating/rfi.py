"""Deterministic clarification questions (the RFI gate) in the engine's checkbox format.

The readers and pricers add their own questions on top; these are the ones the package itself
proves: unscaled/scanned sheets, schedule-vs-plan disagreements, divisions with no takeoff, and
Division 00/01 items an estimator always confirms. Every question carries a citation and a cost
exposure so the Chief Estimator can rank them in 30 seconds.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from core.brain.gap_analyzer import Severity
from core.clarifier.clarification_io import read_answers, write_clarification
from core.clarifier.question_generator import Question

CHOICES = ["Carry as a written assumption (state it on the bid form)", "Issue a pre-bid RFI to the architect",
           "Resolved — see my note"]


@dataclass
class EstimateQuestion:
    text: str
    citation: str
    severity: str            # CRITICAL | WARN | INFO
    exposure: str = "n/a"
    tags: list[str] = field(default_factory=list)
    answer: str | None = None
    assumption: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def build_questions(register: list[dict], sheets: list[dict], discrepancies: list[dict], spec_sections: list[dict],
                    div01: dict, ledger_items: list[dict], priced_lines: list[dict] | None = None,
                    confidence_floor: float = 0.6) -> list[EstimateQuestion]:
    qs: list[EstimateQuestion] = []
    measured = {"plans", "elevations", "sections", "large-scale views"}
    for s in register:
        if s["sheet_type"] in measured and not s.get("scale_label"):
            qs.append(EstimateQuestion(f"Sheet {s['sheet_id']} ({s['title']}) has no parsable scale. Which scale governs, or should quantities be taken from dimension strings only?",
                                       f"{s['sheet_id']} title block", "CRITICAL", "all measured quantities on this sheet", ["scale"]))
        if not s.get("is_vector"):
            qs.append(EstimateQuestion(f"Sheet {s['sheet_id']} is scanned (no text layer). Can a vector PDF or the CAD export be provided? Quantities from it carry lower confidence.",
                                       f"{s['sheet_id']}", "WARN", "confidence of every quantity on the sheet", ["scanned"]))
    for d in discrepancies:
        sev = "CRITICAL" if d["delta_pct"] >= 25 else "WARN"
        qs.append(EstimateQuestion(f"{d['description']}: the {d['a_method']} count is {d['a_qty']:g} but the {d['b_method']} count is {d['b_qty']:g} ({d['delta_pct']:g}% apart) on {d['sheet']}. Which governs?",
                                   f"{d['sheet']} ({d['a_method']} vs {d['b_method']})", sev, f"{abs(d['a_qty'] - d['b_qty']):g} units of {d['item_code']}", ["discrepancy"]))
    kinds = {sc["kind"] for sh in sheets for sc in sh.get("schedules", [])}
    discs = {s["discipline"] for s in register}
    if "A" in discs and "door" not in kinds:
        qs.append(EstimateQuestion("No door schedule was found in the set. Doors are counted from plan swings only — confirm sizes, types, ratings and hardware sets.", "A-sheets (no door schedule)", "CRITICAL", "Division 08 doors, frames, hardware", ["schedule"]))
    if "A" in discs and "finish" not in kinds:
        qs.append(EstimateQuestion("No room finish schedule was found. Floor, base, wall and ceiling finishes per room are assumed — confirm.", "A-sheets (no finish schedule)", "WARN", "Division 09 finishes", ["schedule"]))
    if "S" in discs and "footing" not in kinds:
        qs.append(EstimateQuestion("No footing schedule was found. Footing sizes and reinforcing are needed for concrete and rebar quantities.", "S-sheets (no footing schedule)", "CRITICAL", "Division 03 foundations", ["schedule"]))
    if "P" in discs and "fixture" not in kinds:
        qs.append(EstimateQuestion("No plumbing fixture schedule was found. Fixture types and counts are taken from plan symbols only.", "P-sheets", "WARN", "Division 22 fixtures", ["schedule"]))
    if "E" in discs and "panel" not in kinds and "fixture" not in kinds:
        qs.append(EstimateQuestion("No panel or lighting fixture schedule was found on the E-sheets. Gear sizes and fixture counts are assumed.", "E-sheets", "CRITICAL", "Division 26", ["schedule"]))
    if "C" not in discs:
        qs.append(EstimateQuestion("No civil (C) sheets are in the package. Is site work by a separate contract (the manual may say so), or are civil drawings missing from the set?", "package index / 01 10 00", "WARN", "Divisions 31–33 in full", ["scope"]))
    spec_divs = {s["division"] for s in spec_sections if s["division"] not in ("00", "01")}
    led_divs = {it["division"] for it in ledger_items}
    for div in sorted(spec_divs - led_divs):
        qs.append(EstimateQuestion(f"Specification division {div} has sections but no takeoff lines. Is the scope shown on a sheet not in the package, or excluded?", f"Project Manual division {div}", "WARN", f"division {div} scope", ["coverage"]))
    for h in div01.get("allowances", [])[:6]:
        qs.append(EstimateQuestion(f"Allowance found: \"{h['match']}\". Carried verbatim in the estimate — confirm the amount and that it is a cash allowance (not a contingency).", f"Project Manual p{h['page']} (01 21 00)", "INFO", h["match"], ["allowance"]))
    for h in div01.get("special_inspections", [])[:2]:
        qs.append(EstimateQuestion(f"Special inspections: \"{h['match']}\". Confirm who pays (owner vs contractor) — the estimate carries none if the owner pays.", f"Project Manual p{h['page']} (01 45 00)", "INFO", "testing and inspection costs", ["div01"]))
    for h in div01.get("prevailing_wage", [])[:1]:
        qs.append(EstimateQuestion("Prevailing wage / Davis-Bacon language found. Confirm the wage determination that applies; labor rates in the estimate are private-work rates.", f"Project Manual p{h['page']}", "CRITICAL", "all labor lines", ["wages"]))
    if not div01.get("bid_due"):
        qs.append(EstimateQuestion("No bid due date was found in Division 00. Confirm the bid date and time and the RFI cutoff.", "Project Manual Division 00", "WARN", "schedule of the estimate itself", ["div00"]))
    low = [it for it in ledger_items if it["confidence"] < confidence_floor]
    if low:
        txt = ", ".join(f"{it['id']} {it['description'][:30]}" for it in low[:6])
        qs.append(EstimateQuestion(f"{len(low)} derived quantities are below the confidence floor ({txt}{'…' if len(low) > 6 else ''}). Should the readers measure them from the sheets before pricing is final?",
                                   "04-takeoff-ledger (method=derived)", "WARN", "see the ledger lines listed", ["confidence"]))
    order = {"CRITICAL": 0, "WARN": 1, "INFO": 2}
    qs.sort(key=lambda q: order[q.severity])
    return qs


def write_questions(folder: Path, qs: list[EstimateQuestion]) -> tuple[Path, Path]:
    md = folder / "05-clarification.md"
    js = folder / "05-questions.json"
    write_clarification(md, [Question(text=q.text, citation=q.citation, severity=Severity(q.severity), choices=CHOICES, free_text=True, tags=q.tags)
                             for q in qs if q.severity in ("CRITICAL", "WARN")])
    js.write_text(json.dumps([q.to_dict() for q in qs], indent=2), encoding="utf-8")
    return md, js


def apply_answers(folder: Path) -> list[EstimateQuestion]:
    """Read the ticked choices / free text from 05-clarification.md back into 05-questions.json."""
    js = folder / "05-questions.json"
    qs = [EstimateQuestion(**d) for d in json.loads(js.read_text(encoding="utf-8"))]
    md = folder / "05-clarification.md"
    if not md.exists():
        return qs
    answers = read_answers(md)
    asked = [q for q in qs if q.severity in ("CRITICAL", "WARN")]
    for q, a in zip(asked, answers):
        if a.choice and a.choice.startswith("Carry as a written assumption"):
            q.assumption = a.free_text_answer or "carried as a written assumption on the bid form"
        elif a.choice or a.free_text_answer:
            q.answer = a.free_text_answer or a.choice
    js.write_text(json.dumps([q.to_dict() for q in qs], indent=2), encoding="utf-8")
    return qs


def auto_assume_all(folder: Path) -> list[EstimateQuestion]:
    """--no-llm demo path: every open question becomes a stated assumption (never silent)."""
    js = folder / "05-questions.json"
    qs = [EstimateQuestion(**d) for d in json.loads(js.read_text(encoding="utf-8"))]
    for q in qs:
        if not q.answer and not q.assumption:
            q.assumption = "AUTO-ASSUMED for the unattended run — must be confirmed before bid"
    js.write_text(json.dumps([q.to_dict() for q in qs], indent=2), encoding="utf-8")
    return qs
