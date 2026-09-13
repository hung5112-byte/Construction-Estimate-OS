"""BOM Health & EOL Monitor — deterministic per-part risk scorecard.

Scores one BOM line item's supply risk 0–100 from lifecycle status, source
count, lead time, inventory coverage, compliance, and last-time-buy urgency,
then returns a risk tier and a concrete disposition (redesign-out, last-time-buy,
qualify second source, monitor). Deterministic — no API key needed.

Division-of-labor: the AGENT gathers the signals (lifecycle & LTB dates from the
distributor / SiliconExpert-style feed, source count from the AVL, coverage from
the MRP) — each ideally sourced — and feeds them here as values. This tool does
the scoring, so the disposition is consistent and testable every run.

⚠ GENERAL DECISION-SUPPORT ONLY. Lifecycle status, last-time-buy dates, and
compliance flags MUST be verified against the manufacturer / authorized
distributor before you place a last-time-buy or redesign a part out.
"""
from __future__ import annotations
import re
from core.tools.base_tool import BaseTool, ToolResult

# lifecycle input → (risk 0–100, canonical label)
_LIFECYCLE = {
    "active": (0.0, "Active"), "production": (0.0, "Active"),
    "nrnd": (60.0, "NRND"), "not_recommended": (60.0, "NRND"),
    "eol": (85.0, "EOL"), "ltb": (85.0, "EOL"), "end_of_life": (85.0, "EOL"),
    "obsolete": (100.0, "Obsolete"), "discontinued": (100.0, "Obsolete"),
}
_COMPLIANCE = {
    "ok": 0.0, "compliant": 0.0, "pass": 0.0,
    "unknown": 50.0, "at_risk": 60.0, "at-risk": 60.0,
    "noncompliant": 100.0, "non_compliant": 100.0, "fail": 100.0,
}

_WEIGHTS = {
    "lifecycle": 0.30,      # active / NRND / EOL / obsolete
    "single_source": 0.20,  # AVL source count
    "lead_time": 0.15,      # procurement lead time
    "coverage": 0.15,       # inventory coverage vs demand
    "compliance": 0.10,     # RoHS / REACH status
    "ltb_urgency": 0.10,    # days left in the last-time-buy window (EOL only)
}
_LABELS = {
    "lifecycle": "Lifecycle status",
    "single_source": "Single-source dependency",
    "lead_time": "Lead time",
    "coverage": "Inventory coverage",
    "compliance": "Compliance (RoHS/REACH)",
    "ltb_urgency": "Last-time-buy urgency",
}

_DISCLAIMER = (
    "General decision-support only — verify lifecycle status, last-time-buy dates, "
    "and compliance with the manufacturer / authorized distributor before acting."
)


class BomHealth(BaseTool):
    name = "bom_health"
    description = (
        "Score one BOM part's supply risk 0–100 from lifecycle "
        "(active|nrnd|eol|obsolete), sources (AVL count), lead_time (weeks), "
        "coverage (weeks of inventory vs demand), compliance (ok|at_risk|noncompliant), "
        "ltb_days (days left in last-time-buy window). Returns risk tier + a "
        "disposition (redesign-out / last-time-buy / qualify second source / monitor). "
        "Query: 'bom <part_no> lifecycle=eol sources=1 lead_time=40 coverage=6 "
        "compliance=at_risk ltb_days=90'. Deterministic; general info only."
    )

    def run(self, query: str, **kwargs) -> ToolResult:
        part, p = self._parse(query)

        risks: dict[str, float] = {}
        lifecycle_label: str | None = None

        if "lifecycle" in p:
            risk, lifecycle_label = _LIFECYCLE.get(
                str(p["lifecycle"]).strip().lower(), (50.0, "Unknown")
            )
            risks["lifecycle"] = risk

        sources = None
        if "sources" in p or "avl" in p:
            sources = int(self._num(p.get("sources", p.get("avl"))))
            risks["single_source"] = 100.0 if sources <= 1 else 0.0

        if "lead_time" in p or "lead_time_weeks" in p:
            ceil = self._num(p.get("lead_time_ceiling", "52"))
            weeks = self._num(p.get("lead_time", p.get("lead_time_weeks")))
            risks["lead_time"] = self._clamp(weeks / ceil * 100)

        coverage_ok = True
        if "coverage" in p or "coverage_weeks" in p:
            target = self._num(p.get("coverage_target", "12"))
            weeks = self._num(p.get("coverage", p.get("coverage_weeks")))
            coverage_ok = weeks >= target
            risks["coverage"] = self._clamp((target - weeks) / target * 100)

        if "compliance" in p:
            risks["compliance"] = _COMPLIANCE.get(
                str(p["compliance"]).strip().lower(), 50.0
            )

        # LTB urgency only matters for an EOL part with a stated deadline.
        if lifecycle_label == "EOL" and ("ltb_days" in p or "ltb" in p):
            horizon = self._num(p.get("ltb_horizon", "180"))
            days = self._num(p.get("ltb_days", p.get("ltb")))
            risks["ltb_urgency"] = self._clamp((horizon - days) / horizon * 100)

        if not risks:
            return ToolResult(
                data={}, notes="no BOM part signals provided — see tool description"
            )

        wsum = sum(_WEIGHTS[f] for f in risks)
        contributions = {f: risks[f] * _WEIGHTS[f] / wsum for f in risks}
        score = round(sum(contributions.values()), 2)
        tier = self._tier(score)

        drivers = sorted(
            ((f, contributions[f]) for f in risks if risks[f] > 0),
            key=lambda kv: kv[1], reverse=True,
        )
        top = [
            {"factor": _LABELS[f], "risk": round(risks[f], 1),
             "contribution_pts": round(contributions[f], 2)}
            for f, _ in drivers[:3]
        ]

        disposition = self._disposition(lifecycle_label, tier, sources, coverage_ok)

        data = {
            "part": part or "(unnamed)",
            "risk_score": score,           # 0–100, higher = riskier
            "risk_tier": tier,
            "lifecycle": lifecycle_label or "(not given)",
            "single_source": risks.get("single_source") == 100.0,
            "factor_risks": {_LABELS[f]: round(v, 1) for f, v in risks.items()},
            "top_risk_drivers": top,
            "disposition": disposition,
            "factors_scored": len(risks),
            "disclaimer": _DISCLAIMER,
        }
        return ToolResult(
            data=data,
            sources=[
                "BOM health model (bd-business-os): lifecycle, single-source, lead "
                "time, inventory coverage, compliance, last-time-buy urgency — weights "
                "renormalized over supplied inputs.",
                "Input signals must be primary-sourced: lifecycle & LTB dates from the "
                "manufacturer / authorized distributor; source count from the approved "
                "vendor list; coverage from MRP [UNCERTAIN — verify before LTB/redesign].",
            ],
            notes=_DISCLAIMER,
        )

    # ---- disposition ----
    @staticmethod
    def _disposition(lifecycle, tier, sources, coverage_ok) -> str:
        if lifecycle == "Obsolete":
            return "Redesign-out / qualify an alternate now — part is obsolete."
        if lifecycle == "EOL":
            return ("Last-time-buy: size an LTB to cover the redesign horizon and "
                    "start alternate qualification in parallel.")
        if lifecycle == "NRND":
            return ("Do not design into new products; plan an alternate for the next "
                    "board revision.")
        if sources is not None and sources <= 1 and lifecycle in (None, "Active"):
            return "Active but single-source — qualify a second source."
        if not coverage_ok and tier in ("High", "Critical"):
            return "Active — coverage below target; raise the buffer / expedite."
        return "Active — monitor at standard cadence."

    # ---- helpers ----
    @staticmethod
    def _parse(query: str) -> tuple[str, dict]:
        bare: list[str] = []
        kv: dict[str, str] = {}
        for tok in query.split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k.lower()] = v
            else:
                bare.append(tok)
        if bare and bare[0].lower() in ("bom", "part", "bom_health"):
            bare = bare[1:]
        return " ".join(bare).strip(), kv

    @staticmethod
    def _num(s) -> float:
        return float(re.sub(r"[_,$%]", "", str(s)))

    @staticmethod
    def _clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
        return max(lo, min(hi, x))

    @staticmethod
    def _tier(score: float) -> str:
        if score >= 75:
            return "Critical"
        if score >= 50:
            return "High"
        if score >= 25:
            return "Moderate"
        return "Low"
