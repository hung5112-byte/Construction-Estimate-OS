"""Project-type playbooks — reusable company knowledge as DATA, not as fourteen prompts.

A playbook drives the ROM stage: which trades apply, which assemblies price them (low / target /
high per unit), how quantities derive from intake facts, which questions to ask, which exclusions
to state, which risks to check, and the $/SF band to sanity-check against. Playbooks are versioned
and approval-gated (status seed → approved)
assemblies marked `[to load]` are placeholders until
the company's buyout history replaces them.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from core.estimating.cost_engine import CostRow, DATA_DIR

PLAYBOOK_DIR = DATA_DIR / "playbooks"

TRADE_DEPARTMENT = {
    "demo": "03-architectural", "framing-drywall": "03-architectural", "paint-finish": "03-architectural", "flooring": "03-architectural",
    "ceiling": "03-architectural", "millwork": "03-architectural", "specialties": "03-architectural", "storefront-openings": "03-architectural",
    "roofing-envelope": "03-architectural", "doors-hardware": "03-architectural",
    "concrete-slab": "02-civil-structural", "site-civil": "02-civil-structural", "structural": "02-civil-structural", "masonry": "02-civil-structural",
    "plumbing": "04-mep", "hvac": "04-mep", "electrical": "04-mep", "hood-kitchen": "04-mep", "fire-suppression": "04-mep",
    "fire-alarm": "04-mep", "fire-sprinkler": "04-mep", "low-voltage": "04-mep",
    "general-conditions": "05-cost-engineering",
}


@dataclass
class Assembly:
    code: str
    trade: str
    description: str
    unit: str
    qty_basis: str
    qty_factor: float
    low: float
    target: float
    high: float
    source: str
    confidence: float = 0.5
    labor_share: float = 0.0     # fraction of target that is self-performed labor (rest priced as sub/material)
    notes: str = ""

    @property
    def division(self) -> str:
        return self.code[:2]


@dataclass
class Risk:
    risk: str
    severity: str              # high | medium | low
    trade: str = ""
    mitigation_exclusion: str = ""
    rfi: str = ""


@dataclass
class Playbook:
    project_type: str
    version: str
    status: str
    aliases: list[str]
    building_type_band: str
    default_class: int
    schedule_range_days: dict
    typical_trades: list[str]
    intake_fields: dict
    assemblies: list[Assembly]
    common_rfis: list[str]
    common_exclusions: list[str]
    risk_checklist: list[Risk]
    general_conditions: dict
    path: str = ""
    approved_by: str | None = None
    notes: str = ""

    def validate(self) -> list[str]:
        problems = []
        seen = set()
        for a in self.assemblies:
            if a.code in seen:
                problems.append(f"duplicate assembly code {a.code}")
            seen.add(a.code)
            if not (a.low <= a.target <= a.high):
                problems.append(f"{a.code}: low ≤ target ≤ high violated ({a.low}, {a.target}, {a.high})")
            if a.trade not in self.typical_trades:
                problems.append(f"{a.code}: trade {a.trade!r} not in typical_trades")
            if a.trade not in TRADE_DEPARTMENT:
                problems.append(f"{a.code}: unknown trade {a.trade!r}")
            if not re.match(r"^\d{2}-[a-z0-9\-]+$", a.code):
                problems.append(f"{a.code}: code must be NN-slug")
        for r in self.risk_checklist:
            if r.severity not in ("high", "medium", "low"):
                problems.append(f"risk {r.risk!r}: bad severity")
            if r.severity == "high" and not (r.mitigation_exclusion or r.rfi):
                problems.append(f"risk {r.risk!r}: high severity needs an exclusion or an RFI")
        if not (1 <= int(self.default_class) <= 5):
            problems.append("default_class must be 1–5")
        return problems

    def cost_rows(self) -> dict[str, CostRow]:
        rows: dict[str, CostRow] = {}
        for a in self.assemblies:
            labor = round(a.target * a.labor_share, 4)
            rows[a.code] = CostRow(item_code=a.code, description=a.description, unit=a.unit, labor=labor, material=0.0, equipment=0.0,
                                   sub=round(a.target - labor, 4), source=a.source, quote_date="", valid_until="", location="national",
                                   notes=("[UNCERTAIN] " if "to load" in a.source.lower() or "placeholder" in a.source.lower() else "") + a.notes,
                                   pricing_basis="assembly", unit_low=a.low, unit_high=a.high)
        return rows


def _as_assembly(d: dict) -> Assembly:
    q = d.get("qty") or {}
    return Assembly(code=d["code"], trade=d["trade"], description=d["description"], unit=str(d["unit"]).upper(),
                    qty_basis=str(q.get("basis", "each")), qty_factor=float(q.get("factor", 1.0)),
                    low=float(d["low"]), target=float(d["target"]), high=float(d["high"]), source=str(d.get("source", "")),
                    confidence=float(d.get("confidence", 0.5)), labor_share=float(d.get("labor_share", 0.0)), notes=str(d.get("notes", "")))


def load_playbook_file(path: Path) -> Playbook:
    d = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return Playbook(
        project_type=d["project_type"], version=str(d.get("version", "1.0")), status=str(d.get("status", "seed")),
        aliases=[str(a).lower() for a in d.get("aliases", [])], building_type_band=str(d.get("building_type_band", "")),
        default_class=int(d.get("default_class", 5)), schedule_range_days=dict(d.get("schedule_range_days", {})),
        typical_trades=list(d.get("typical_trades", [])), intake_fields=dict(d.get("intake_fields", {})),
        assemblies=[_as_assembly(a) for a in d.get("assemblies", [])], common_rfis=list(d.get("common_rfis", [])),
        common_exclusions=list(d.get("common_exclusions", [])),
        risk_checklist=[Risk(risk=r["risk"], severity=str(r.get("severity", "medium")), trade=str(r.get("trade", "")),
                             mitigation_exclusion=str(r.get("mitigation_exclusion", "")), rfi=str(r.get("rfi", ""))) for r in d.get("risk_checklist", [])],
        general_conditions=dict(d.get("general_conditions", {})), path=str(path), approved_by=d.get("approved_by"), notes=str(d.get("notes", "")),
    )


def list_playbooks(directory: Path | None = None) -> dict[str, Playbook]:
    out: dict[str, Playbook] = {}
    for p in sorted((directory or PLAYBOOK_DIR).glob("*.yaml")):
        pb = load_playbook_file(p)
        out[pb.project_type] = pb
    return out


def resolve_playbook(project_type: str, directory: Path | None = None) -> Playbook:
    key = (project_type or "").strip().lower()
    books = list_playbooks(directory)
    if key in books:
        return books[key]
    for pb in books.values():
        if key == pb.project_type or key in pb.aliases:
            return pb
    slug = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    for pb in books.values():
        if slug == pb.project_type or slug in [re.sub(r"[^a-z0-9]+", "-", a).strip("-") for a in pb.aliases]:
            return pb
    raise KeyError(f"no playbook for project type {project_type!r}; known: {', '.join(sorted(books))}")


@dataclass
class BasisResolution:
    values: dict = field(default_factory=dict)
    assumptions: list[str] = field(default_factory=list)   # human-readable defaults used
    missing: list[str] = field(default_factory=list)       # fields that had no default → question


def resolve_basis(pb: Playbook, intake: dict) -> BasisResolution:
    """Turn intake facts into the numbers assemblies multiply. Every default used becomes an assumption
    (and, downstream, a question); nothing is silently invented."""
    res = BasisResolution()
    fields = dict(intake.get("fields") or {})
    gross = float(intake.get("gross_sf") or fields.get("gross_sf") or 0)
    if not gross:
        res.missing.append("gross_sf")
    res.values["gross_sf"] = gross
    res.values["each"] = 1.0
    res.values["perimeter_lf"] = round(4 * math.sqrt(gross), 1) if gross else 0.0
    if "perimeter_lf" not in fields and gross:
        res.assumptions.append(f"perimeter_lf = 4 × √gross_sf = {res.values['perimeter_lf']:.0f} LF (square-equivalent)")
    days = intake.get("duration_days") or pb.schedule_range_days.get("target") or 90
    res.values["duration_months"] = round(float(days) / 30.4, 2)
    if not intake.get("duration_days"):
        res.assumptions.append(f"duration = {days} days (playbook target range)")
    for name, spec in pb.intake_fields.items():
        if name in ("gross_sf",):
            continue
        spec = spec or {}
        if name in fields and fields[name] not in (None, ""):
            res.values[name] = float(fields[name])
            continue
        if "default_ratio_of_gross" in spec and gross:
            res.values[name] = round(gross * float(spec["default_ratio_of_gross"]), 1)
            res.assumptions.append(f"{name} = {spec['default_ratio_of_gross']:g} × gross_sf = {res.values[name]:.0f} — {spec.get('note', 'default ratio')}")
        elif "default" in spec:
            res.values[name] = float(spec["default"])
            res.assumptions.append(f"{name} = {spec['default']:g} — {spec.get('note', 'playbook default')}")
        elif spec.get("required"):
            res.missing.append(name)
            res.values[name] = 0.0
        else:
            res.values[name] = 0.0
    # any explicit field the playbook did not declare still counts
    for name, val in fields.items():
        if name not in res.values:
            try:
                res.values[name] = float(val)
            except (TypeError, ValueError):
                pass
    return res


def quantity_for(a: Assembly, basis: BasisResolution) -> tuple[float, str]:
    base = basis.values.get(a.qty_basis)
    if base is None:
        return 0.0, f"no basis value for {a.qty_basis!r}"
    return round(base * a.qty_factor, 3), f"{a.qty_factor:g} × {a.qty_basis} ({base:g})"
