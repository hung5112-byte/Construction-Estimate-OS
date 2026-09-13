"""The takeoff ledger — every quantity with provenance, in one normalized structure.

A ledger line is the unit of truth downstream: pricing multiplies it, gates audit it, the report
cites it. Lines from different methods for the same thing (a door schedule count, a vector arc
count, a vision confirmation) are reconciled here, and disagreements become discrepancies that the
RFI stage turns into questions.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

METHODS = ("schedule", "vector", "vision", "manual", "derived", "spec", "allowance")
# How a PRICE was obtained (GrandVista-compatible enum + our honest placeholder value)
PRICING_BASES = ("historical", "assembly", "manual", "allowance", "sub_bid", "online_check", "seed_placeholder")
UNITS = {
    "EA": "each", "LF": "linear feet", "SF": "square feet", "SY": "square yards", "CY": "cubic yards",
    "SQ": "roofing squares (100 SF)", "TON": "tons (2,000 lb)", "LB": "pounds", "LS": "lump sum",
    "HR": "hours", "MO": "months", "SFCA": "square feet of contact area (forms)", "BCY": "bank cubic yards",
    "CCY": "compacted cubic yards", "GAL": "gallons", "KVA": "kVA", "DAY": "days", "WK": "weeks",
}
_UNIT_ALIASES = {"EACH": "EA", "PCS": "EA", "PC": "EA", "SQFT": "SF", "SQ FT": "SF", "FT": "LF", "LIN FT": "LF",
                 "CU YD": "CY", "CUYD": "CY", "SQ YD": "SY", "LBS": "LB", "TONS": "TON", "SQUARES": "SQ",
                 "MONTH": "MO", "MONTHS": "MO", "HOUR": "HR", "HOURS": "HR", "SQUARE": "SQ"}

# Unit classes a division may legitimately use — gate G5 checks against this
DIVISION_UNITS = {
    "01": {"LS", "MO", "EA", "HR", "WK", "DAY", "LF", "SF"}, "02": {"SF", "CY", "LS", "EA", "LF"},
    "03": {"CY", "SFCA", "LB", "SF", "LF", "EA", "TON"}, "04": {"SF", "EA", "CY", "LF", "LB"},
    "05": {"TON", "LB", "EA", "SF", "LF"}, "06": {"LF", "SF", "EA", "LS"}, "07": {"SQ", "SF", "LF", "EA", "LS"},
    "08": {"EA", "SF", "LF", "LS"}, "09": {"SF", "SY", "LF", "EA", "LS"}, "10": {"EA", "LF", "SF", "LS"},
    "11": {"EA", "LS"}, "12": {"EA", "LF", "SF", "LS"}, "13": {"SF", "EA", "LS"}, "14": {"EA", "LS"},
    "21": {"EA", "LF", "SF", "LS"}, "22": {"EA", "LF", "LS", "SF"}, "23": {"EA", "LB", "LF", "SF", "LS"},
    "26": {"EA", "LF", "KVA", "LS"}, "27": {"EA", "LF", "LS"}, "28": {"EA", "LS"},
    "31": {"BCY", "CY", "CCY", "SF", "LF", "LS"}, "32": {"SF", "SY", "LF", "EA", "LS"}, "33": {"LF", "EA", "LS"},
}


def normalize_unit(u: str) -> str:
    k = (u or "").strip().upper().replace(".", "")
    return _UNIT_ALIASES.get(k, k)


@dataclass
class TakeoffItem:
    id: str
    division: str
    item_code: str
    description: str
    qty: float
    unit: str
    sheet: str
    method: str
    discipline: str
    revision: str | None = None
    section: str | None = None
    confidence: float = 0.8
    waste_pct: float = 0.0
    notes: str = ""
    tags: dict = field(default_factory=dict)
    pricing_basis: str = ""      # set at pricing time unless the line dictates it (allowance, manual, sub_bid)

    @property
    def qty_with_waste(self) -> float:
        return round(self.qty * (1 + self.waste_pct / 100.0), 3)

    def validate(self) -> list[str]:
        problems = []
        if self.method not in METHODS:
            problems.append(f"{self.id}: unknown method {self.method!r}")
        if self.unit not in UNITS:
            problems.append(f"{self.id}: unknown unit {self.unit!r}")
        if not self.sheet:
            problems.append(f"{self.id}: no sheet reference")
        if self.qty < 0:
            problems.append(f"{self.id}: negative quantity")
        if not (0.0 <= self.confidence <= 1.0):
            problems.append(f"{self.id}: confidence out of range")
        if self.pricing_basis and self.pricing_basis not in PRICING_BASES:
            problems.append(f"{self.id}: unknown pricing_basis {self.pricing_basis!r}")
        allowed = DIVISION_UNITS.get(self.division)
        if allowed and self.unit not in allowed and self.unit != "LS" and self.pricing_basis != "assembly":   # LS and assembly lines are valid anywhere
            problems.append(f"{self.id}: unit {self.unit} unusual for division {self.division}")
        return problems


@dataclass
class Discrepancy:
    item_code: str
    description: str
    a_method: str
    a_qty: float
    b_method: str
    b_qty: float
    delta_pct: float
    sheet: str

    def to_dict(self) -> dict:
        return asdict(self)


class Ledger:
    def __init__(self) -> None:
        self.items: list[TakeoffItem] = []
        self._n = 0

    def add(self, division: str, item_code: str, description: str, qty: float, unit: str, sheet: str,
            method: str, discipline: str, **kw) -> TakeoffItem:
        self._n += 1
        item = TakeoffItem(id=f"T-{self._n:04d}", division=str(division).zfill(2), item_code=item_code,
                           description=description, qty=float(qty), unit=normalize_unit(unit), sheet=sheet,
                           method=method, discipline=discipline, **kw)
        self.items.append(item)
        return item

    def by_division(self) -> dict[str, list[TakeoffItem]]:
        out: dict[str, list[TakeoffItem]] = {}
        for it in self.items:
            out.setdefault(it.division, []).append(it)
        return dict(sorted(out.items()))

    def sheets_used(self) -> set[str]:
        return {it.sheet for it in self.items}

    def validate(self) -> list[str]:
        problems: list[str] = []
        for it in self.items:
            problems.extend(it.validate())
        return problems

    def reconcile(self, tolerance_pct: float = 10.0) -> list[Discrepancy]:
        """Same item_code counted by two methods on the same sheet → keep the most authoritative
        (schedule > vector > vision > manual > derived) and record the disagreement."""
        rank = {m: i for i, m in enumerate(("schedule", "manual", "vector", "vision", "derived", "spec", "allowance"))}
        groups: dict[tuple, list[TakeoffItem]] = {}
        for it in self.items:
            ident = tuple(sorted((k, str(v)) for k, v in it.tags.items() if k in ("room", "mark", "tag")))
            groups.setdefault((it.item_code, it.sheet, it.description if not ident else "", ident), []).append(it)
        keep: list[TakeoffItem] = []
        disc: list[Discrepancy] = []
        for (code, sheet, _desc, _ident), its in groups.items():
            if len(its) == 1 or len({i.method for i in its}) == 1:
                keep.extend(its)      # one line, or several lines of the same kind (not a disagreement)
                continue
            its = sorted(its, key=lambda i: rank.get(i.method, 99))
            best = its[0]
            for other in its[1:]:
                base = best.qty if best.qty else 1.0
                delta = abs(other.qty - best.qty) / base * 100.0
                if delta > tolerance_pct:
                    disc.append(Discrepancy(code, best.description, best.method, best.qty, other.method, other.qty, round(delta, 1), sheet))
            keep.append(best)
        self.items = sorted(keep, key=lambda i: (i.division, i.id))
        return disc

    def to_json(self) -> str:
        return json.dumps([asdict(i) for i in self.items], indent=2)

    @classmethod
    def from_json(cls, text: str) -> Ledger:
        led = cls()
        for d in json.loads(text):
            led.items.append(TakeoffItem(**d))
        led._n = len(led.items)
        return led

    def to_markdown(self, title: str = "Takeoff ledger") -> str:
        out = ["---", "type: takeoff_ledger", f"items: {len(self.items)}", "---", f"# {title}", ""]
        for div, its in self.by_division().items():
            out.append(f"## Division {div}")
            out.append("| ID | Item | Qty | Unit | Waste % | Sheet | Rev | Method | Conf | Notes |")
            out.append("|---|---|---|---|---|---|---|---|---|---|")
            for it in its:
                out.append(f"| {it.id} | {it.description} | {it.qty:,.2f} | {it.unit} | {it.waste_pct:g} | {it.sheet} | "
                           f"{it.revision or ''} | {it.method} | {it.confidence:.2f} | {it.notes} |")
            out.append("")
        return "\n".join(out)


def load_waste_factors(path: Path) -> dict[str, float]:
    import csv

    out: dict[str, float] = {}
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["item_class"]] = float(row["waste_pct"])
    return out
