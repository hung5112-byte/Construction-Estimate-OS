"""Supplier Risk Radar — deterministic weighted supplier-risk scorecard.

Turns supplier signals (financial health, single-source dependency, geographic
risk, quality PPM, on-time delivery, lead time, capacity utilization) into a
repeatable 0–100 risk score, a risk tier, the top risk drivers, and a
recommended action. Deterministic — no API key needed.

Division-of-labor: the AGENT gathers the raw signals (financial news, country
risk, quality/OTD from the scorecard system) — ideally via web_search / the
Brain so each is sourced — and feeds them here as numbers. This tool does the
scoring, not the sourcing, so the number is consistent every run.

⚠ GENERAL DECISION-SUPPORT ONLY. The score is a weighted model, not a rating
agency opinion; every INPUT signal must itself be verified against a primary
source (audited financials, the supplier scorecard, a country-risk index)
before you act on the result.
"""
from __future__ import annotations
import re
from core.tools.base_tool import BaseTool, ToolResult

# Factor default weights (sum = 1.00). Renormalized over whichever factors the
# caller actually supplies, so partial data still yields an honest score.
_WEIGHTS = {
    "financial": 0.20,      # supplier financial health
    "single_source": 0.20,  # sole-source dependency
    "geo": 0.15,            # geographic / country risk
    "quality": 0.15,        # defect PPM
    "delivery": 0.15,       # on-time delivery
    "lead_time": 0.10,      # lead time
    "capacity": 0.05,       # capacity utilization
}

_LABELS = {
    "financial": "Supplier financial health",
    "single_source": "Single-source dependency",
    "geo": "Geographic / country risk",
    "quality": "Quality (defect PPM)",
    "delivery": "On-time delivery",
    "lead_time": "Lead time",
    "capacity": "Capacity utilization",
}

# Per-tier + per-driver recommended actions (deterministic mapping).
_TIER_ACTION = {
    "Critical": "Immediate action — qualify a second source and build buffer inventory now; escalate to Sourcing + Quality.",
    "High": "Near-term — stand up a dual-source plan and a supplier improvement plan; raise safety-inventory levels.",
    "Moderate": "Monitor quarterly and close the top risk driver before it escalates.",
    "Low": "Maintain — standard scorecard cadence; no special mitigation.",
}
_DRIVER_ACTION = {
    "single_source": "Prioritize qualifying a second source / alternate part.",
    "quality": "Open a SCAR / 8D and require a containment + corrective-action plan.",
    "delivery": "Put the supplier on an OTD improvement plan; add expedite/buffer.",
    "financial": "Add to credit watch and pre-qualify an alternate before exposure grows.",
    "geo": "Evaluate near-shore / dual-region sourcing to cut concentration.",
    "lead_time": "Negotiate shorter lead time or hold consignment / VMI inventory.",
    "capacity": "Secure allocation commitments and monitor utilization vs your demand.",
}

_DISCLAIMER = (
    "General decision-support only — weighted model, not a credit-rating opinion. "
    "Verify every input signal against a primary source before acting."
)


class SupplierRisk(BaseTool):
    name = "supplier_risk"
    description = (
        "Score a supplier's risk 0–100 from signals: financial (health 0–100), "
        "single_source (yes/no), geo (0–100 country risk), quality (defect ppm), "
        "otd (on-time delivery %), lead_time (days), capacity (utilization %). "
        "Returns risk tier, top drivers, and a recommended action. "
        "Query: 'supplier <name> financial=72 single_source=yes geo=65 ppm=1200 "
        "otd=94 lead_time=45 capacity=88'. Deterministic; general info only."
    )

    def run(self, query: str, **kwargs) -> ToolResult:
        name, p = self._parse(query)

        # Compute a 0–100 risk sub-score for each factor the caller supplied.
        risks: dict[str, float] = {}
        if "financial" in p:  # health 0–100 (higher = healthier) → risk = 100 − health
            risks["financial"] = self._clamp(100 - self._num(p["financial"]))
        if any(k in p for k in ("single_source", "sole_source", "single")):
            v = p.get("single_source", p.get("sole_source", p.get("single", "")))
            risks["single_source"] = 100.0 if self._truthy(v) else 0.0
        if "geo" in p or "geo_risk" in p:
            risks["geo"] = self._clamp(self._num(p.get("geo", p.get("geo_risk"))))
        if "ppm" in p:
            ceil = self._num(p.get("ppm_ceiling", "5000"))
            risks["quality"] = self._clamp(self._num(p["ppm"]) / ceil * 100)
        if "otd" in p:  # on-time delivery % (higher = better)
            risks["delivery"] = self._clamp(100 - self._num(p["otd"]))
        if "lead_time" in p or "lead_time_days" in p:
            ceil = self._num(p.get("lead_time_ceiling", "90"))
            days = self._num(p.get("lead_time", p.get("lead_time_days")))
            risks["lead_time"] = self._clamp(days / ceil * 100)
        if "capacity" in p:  # utilization % — risk only above a comfort threshold
            comfort = self._num(p.get("capacity_comfort", "85"))
            util = self._num(p["capacity"])
            span = max(1.0, 100 - comfort)
            risks["capacity"] = self._clamp((util - comfort) / span * 100)

        if not risks:
            return ToolResult(
                data={}, notes="no supplier signals provided — see tool description"
            )

        # Weighted score, renormalized over supplied factors.
        wsum = sum(_WEIGHTS[f] for f in risks)
        contributions = {f: risks[f] * _WEIGHTS[f] / wsum for f in risks}
        score = round(sum(contributions.values()), 2)
        tier = self._tier(score)

        # Top drivers = factors with the largest weighted contribution (risk > 0).
        drivers = sorted(
            ((f, contributions[f]) for f in risks if risks[f] > 0),
            key=lambda kv: kv[1], reverse=True,
        )
        top = [
            {"factor": _LABELS[f], "risk": round(risks[f], 1),
             "contribution_pts": round(contributions[f], 2)}
            for f, _ in drivers[:3]
        ]

        action = _TIER_ACTION[tier]
        if drivers:
            top_factor = drivers[0][0]
            if top_factor in _DRIVER_ACTION:
                action = f"{action} {_DRIVER_ACTION[top_factor]}"

        missing = [_LABELS[f] for f in _WEIGHTS if f not in risks]
        data = {
            "supplier": name or "(unnamed)",
            "risk_score": score,           # 0–100, higher = riskier
            "risk_tier": tier,
            "single_source": risks.get("single_source") == 100.0,
            "factor_risks": {_LABELS[f]: round(v, 1) for f, v in risks.items()},
            "top_risk_drivers": top,
            "recommended_action": action,
            "factors_scored": len(risks),
            "factors_missing": missing,
            "disclaimer": _DISCLAIMER,
        }
        return ToolResult(
            data=data,
            sources=[
                "Weighted supplier-risk model (bd-business-os): factors financial, "
                "single-source, geographic, quality PPM, on-time delivery, lead time, "
                "capacity — weights renormalized over supplied inputs.",
                "Input signals must be primary-sourced: audited financials / D&B or "
                "similar for financial health; the supplier scorecard for PPM & OTD; "
                "a recognized country-risk index for geographic risk "
                "[UNCERTAIN — verify each input before acting].",
            ],
            notes=_DISCLAIMER,
        )

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
        # drop a leading command word ("supplier") if present
        if bare and bare[0].lower() in ("supplier", "score", "risk"):
            bare = bare[1:]
        return " ".join(bare).strip(), kv

    @staticmethod
    def _num(s) -> float:
        return float(re.sub(r"[_,$%]", "", str(s)))

    @staticmethod
    def _truthy(v) -> bool:
        return str(v).strip().lower() in ("1", "yes", "y", "true", "t", "single", "sole")

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
