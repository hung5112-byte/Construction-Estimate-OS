"""Deterministic pricing: ledger × cost library → priced lines, general conditions, markups, summary.

No model runs here. The library resolves in priority order (BYO first, seed second)
a line with no
row is carried as [UNPRICED], never guessed. Every number the report shows is computed here and
cites the row and policy it came from.
"""
from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

from core.estimating.takeoff_ledger import Ledger

DATA_DIR = Path(__file__).resolve().parent.parent / "tools" / "data" / "estimating"
SEED_LIBRARY = DATA_DIR / "unit_costs_seed.csv"
SEED_DISCLAIMER = ("Seed library — national-average PLACEHOLDERS marked [UNCERTAIN]; replace with the company's "
                   "buyout history and quotes in 03-Cost-Library/ before relying on any figure.")


@dataclass
class CostRow:
    item_code: str
    description: str
    unit: str
    labor: float
    material: float
    equipment: float
    sub: float
    source: str
    quote_date: str = ""
    valid_until: str = ""
    location: str = "national"
    notes: str = ""

    @property
    def unit_total(self) -> float:
        return self.labor + self.material + self.equipment + self.sub

    @property
    def uncertain(self) -> bool:
        return "seed" in self.source.lower() or "[UNCERTAIN]" in self.notes


def _f(v: str) -> float:
    try:
        return float(str(v).replace(",", "").replace("$", "") or 0)
    except ValueError:
        return 0.0


def load_library(paths: list[Path]) -> dict[str, CostRow]:
    """First path wins per item_code (pass BYO files before the seed)."""
    lib: dict[str, CostRow] = {}
    for p in paths:
        if not p or not Path(p).exists():
            continue
        with Path(p).open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                code = (row.get("item_code") or "").strip()
                if not code or code in lib:
                    continue
                lib[code] = CostRow(
                    item_code=code, description=(row.get("description") or "").strip(), unit=(row.get("unit") or "").strip().upper(),
                    labor=_f(row.get("labor", 0)), material=_f(row.get("material", 0)), equipment=_f(row.get("equipment", 0)),
                    sub=_f(row.get("sub", 0)), source=(row.get("source") or Path(p).name).strip(),
                    quote_date=(row.get("quote_date") or "").strip(), valid_until=(row.get("valid_until") or "").strip(),
                    location=(row.get("location") or "national").strip(), notes=(row.get("notes") or "").strip(),
                )
    return lib


def library_paths(vault_root: Path | None) -> list[Path]:
    paths: list[Path] = []
    if vault_root:
        byo = Path(vault_root) / "03-Cost-Library"
        if byo.exists():
            paths.extend(sorted(byo.glob("*.csv")))
    paths.append(SEED_LIBRARY)
    return paths


@dataclass
class PricedLine:
    item_id: str
    division: str
    item_code: str
    description: str
    qty: float
    unit: str
    unit_labor: float
    unit_material: float
    unit_equipment: float
    unit_sub: float
    labor: float
    material: float
    equipment: float
    sub: float
    total: float
    source: str
    sheet: str
    method: str
    confidence: float
    flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def price_ledger(ledger: Ledger, library: dict[str, CostRow], location_factor: float = 1.0,
                 as_of: date | None = None) -> list[PricedLine]:
    as_of = as_of or date.today()
    lines: list[PricedLine] = []
    for it in ledger.items:
        row = library.get(it.item_code)
        flags: list[str] = []
        if row is None:
            lines.append(PricedLine(it.id, it.division, it.item_code, it.description, it.qty_with_waste, it.unit,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, "", it.sheet, it.method, it.confidence, ["UNPRICED"]))
            continue
        if row.unit != it.unit:
            flags.append(f"UNIT-MISMATCH library {row.unit} vs takeoff {it.unit}")
        if row.uncertain:
            flags.append("UNCERTAIN")
        if row.valid_until:
            try:
                y, m, d = (int(x) for x in row.valid_until.split("-"))
                if date(y, m, d) < as_of:
                    flags.append("STALE-QUOTE")
            except ValueError:
                pass
        if it.confidence < 0.6:
            flags.append("LOW-CONFIDENCE")
        q = it.qty_with_waste
        # location factor applies to labor and material; subcontract quotes are already local
        ul, um, ue, us = row.labor * location_factor, row.material * location_factor, row.equipment * location_factor, row.sub
        L, M, Eq, S = round(q * ul, 2), round(q * um, 2), round(q * ue, 2), round(q * us, 2)
        lines.append(PricedLine(it.id, it.division, it.item_code, it.description, q, it.unit, ul, um, ue, us,
                                L, M, Eq, S, round(L + M + Eq + S, 2), row.source, it.sheet, it.method, it.confidence, flags))
    return lines


@dataclass
class GCLine:
    name: str
    qty: float
    unit: str
    rate: float
    total: float
    basis: str


def general_conditions(duration_months: float, staff: list[tuple[str, float, float]] | None = None,
                       temp_items: list[tuple[str, float, str, float]] | None = None,
                       other: list[tuple[str, float, str]] | None = None) -> list[GCLine]:
    """staff: (role, fte, monthly burdened rate); temp_items: (name, qty, unit, rate per unit per month
    or per each); other: (name, amount, basis)."""
    out: list[GCLine] = []
    for role, fte, rate in (staff or []):
        out.append(GCLine(role, round(fte * duration_months, 2), "MO", rate, round(fte * duration_months * rate, 2), f"{fte:g} FTE × {duration_months:g} months"))
    for name, qty, unit, rate in (temp_items or []):
        if unit == "MO":
            out.append(GCLine(name, round(qty * duration_months, 2), "MO", rate, round(qty * duration_months * rate, 2), f"{qty:g} × {duration_months:g} months"))
        else:
            out.append(GCLine(name, qty, unit, rate, round(qty * rate, 2), "quantity × rate"))
    for name, amount, basis in (other or []):
        out.append(GCLine(name, 1, "LS", amount, round(amount, 2), basis))
    return out


@dataclass
class MarkupPolicy:
    contingency_pct: float
    escalation_pct: float
    insurance_pct: float
    bond_pct: float
    fee_pct: float
    tax_pct: float = 8.25
    tax_basis: str = "materials"     # materials (lump-sum contract) | none (separated, owner pays)
    contingency_basis: str = "policy"
    escalation_basis: str = ""
    fee_basis: str = "policy"


@dataclass
class MarkupLine:
    name: str
    pct: float
    base: float
    amount: float
    basis: str


def markup_stack(direct_total: float, materials_total: float, gc_total: float, policy: MarkupPolicy) -> list[MarkupLine]:
    lines: list[MarkupLine] = []
    running = direct_total + gc_total
    lines.append(MarkupLine("Direct cost", 0, direct_total, direct_total, "sum of priced lines"))
    lines.append(MarkupLine("General conditions", (gc_total / direct_total * 100) if direct_total else 0, direct_total, gc_total, "duration-driven worksheet"))
    c = round(running * policy.contingency_pct / 100, 2)
    lines.append(MarkupLine("Contingency", policy.contingency_pct, running, c, policy.contingency_basis))
    running += c
    e = round(running * policy.escalation_pct / 100, 2)
    lines.append(MarkupLine("Escalation", policy.escalation_pct, running, e, policy.escalation_basis or "index to bid mid-point"))
    running += e
    tax_base = materials_total if policy.tax_basis == "materials" else 0.0
    t = round(tax_base * policy.tax_pct / 100, 2)
    lines.append(MarkupLine("Sales tax on materials", policy.tax_pct if tax_base else 0, tax_base, t, f"Texas, basis={policy.tax_basis} (Comptroller Pub. 94-116)"))
    running += t
    i = round(running * policy.insurance_pct / 100, 2)
    lines.append(MarkupLine("Insurance (GL + builder's risk)", policy.insurance_pct, running, i, "policy default — verify with broker"))
    running += i
    b = round(running * policy.bond_pct / 100, 2)
    lines.append(MarkupLine("Performance & payment bond", policy.bond_pct, running, b, "policy default — verify with surety"))
    running += b
    f = round(running * policy.fee_pct / 100, 2)
    lines.append(MarkupLine("Overhead & profit (fee)", policy.fee_pct, running, f, policy.fee_basis))
    running += f
    lines.append(MarkupLine("TOTAL BID", 0, running, round(running, 2), "sum"))
    return lines


def summary_by_division(priced: list[PricedLine], gross_sf: float, divisions_titles: dict[str, str]) -> list[dict]:
    rows: dict[str, dict] = {}
    for ln in priced:
        r = rows.setdefault(ln.division, {"division": ln.division, "title": divisions_titles.get(ln.division, ""), "labor": 0.0, "material": 0.0,
                                          "equipment": 0.0, "sub": 0.0, "total": 0.0, "lines": 0, "unpriced": 0})
        r["labor"] += ln.labor
        r["material"] += ln.material
        r["equipment"] += ln.equipment
        r["sub"] += ln.sub
        r["total"] += ln.total
        r["lines"] += 1
        r["unpriced"] += 1 if "UNPRICED" in ln.flags else 0
    grand = sum(r["total"] for r in rows.values()) or 1.0
    out = []
    for div in sorted(rows):
        r = rows[div]
        r["per_sf"] = round(r["total"] / gross_sf, 2) if gross_sf else None
        r["pct"] = round(r["total"] / grand * 100, 1)
        for k in ("labor", "material", "equipment", "sub", "total"):
            r[k] = round(r[k], 2)
        out.append(r)
    return out


def load_benchmarks(path: Path | None = None) -> list[dict]:
    p = path or (DATA_DIR / "benchmarks_dfw_2026.csv")
    with Path(p).open(encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def benchmark_check(total_hard_cost: float, gross_sf: float, building_type: str, gc_total: float, direct_total: float,
                    labor_total: float, benchmarks: list[dict] | None = None) -> dict:
    """$/SF vs band for the building type plus the standard ratio checks; every result names its source."""
    bm = benchmarks or load_benchmarks()
    per_sf = round(total_hard_cost / gross_sf, 2) if gross_sf else None
    band = next((b for b in bm if b["building_type"].lower() == building_type.lower()), None)
    checks = []
    if band and per_sf is not None:
        lo, hi = float(band["low_per_sf"]), float(band["high_per_sf"])
        status = "inside" if lo <= per_sf <= hi else ("below" if per_sf < lo else "above")
        checks.append({"check": "$/SF vs building-type band", "value": per_sf, "band": f"{lo:.0f}–{hi:.0f}", "status": status, "source": band["source"]})
    else:
        checks.append({"check": "$/SF vs building-type band", "value": per_sf, "band": "n/a", "status": "no-band", "source": "benchmarks_dfw_2026.csv"})
    gc_pct = round(gc_total / direct_total * 100, 1) if direct_total else None
    checks.append({"check": "General conditions % of direct", "value": gc_pct, "band": "8–15", "status": ("inside" if gc_pct is not None and 8 <= gc_pct <= 15 else "outside"), "source": "SmartBarrel / Procore (benchmarks.md)"})
    labor_pct = round(labor_total / direct_total * 100, 1) if direct_total else None
    checks.append({"check": "Labor share of self-performed + priced lines", "value": labor_pct, "band": "n/a (≈60% of budgets industry-wide incl. sub labor)", "status": "info", "source": "ConstructConnect (benchmarks.md)"})
    return {"per_sf": per_sf, "building_type": building_type, "checks": checks}


def load_location_factor(city: str, path: Path | None = None) -> tuple[float, str]:
    p = path or (DATA_DIR / "location_factors.csv")
    with Path(p).open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["city"].lower() == city.lower():
                return float(r["factor"]), r["source"]
    return 1.0, "no match — national 1.00"


def estimate_json(priced: list[PricedLine], gcs: list[GCLine], markups: list[MarkupLine], summary: list[dict], meta: dict) -> str:
    return json.dumps({"meta": meta, "summary_by_division": summary, "lines": [p.to_dict() for p in priced],
                       "general_conditions": [asdict(g) for g in gcs], "markups": [asdict(m) for m in markups]}, indent=2)
