"""US-import landed-cost & tariff engine.

Builds a per-unit landed cost from ex-works price + freight + insurance
+ base HTS duty + additional tariffs (Section 301 / IEEPA / AD-CVD, etc.)
+ CBP fees (MPF, HMF) + customs-broker fee + in-transit carrying cost, and
ISOLATES the tariff portion so sourcing and site decisions compare TOTAL
landed cost, not unit price. Deterministic — no API key needed.

⚠️ GENERAL ESTIMATE ONLY — NOT customs, legal, or tax advice. HTS
classification and every duty/tariff rate MUST be verified with a licensed
customs broker; Section 301, IEEPA, and similar additional tariffs change
frequently. CBP fee rates (MPF/HMF) and their per-entry min/max are
year-specific — the values here are placeholders marked [UNCERTAIN] and must
be confirmed against the current CBP fee schedule before use.

US customs valuation is generally the FOB / ex-works transaction value
(19 U.S.C. § 1401a): base duty, additional tariffs, MPF, and HMF are assessed
on that customs value, NOT on international freight. This tool follows that
convention — customs value defaults to the ex-works unit price unless the
caller overrides it with `cv=`.
"""
from __future__ import annotations
import re
from core.tools.base_tool import BaseTool, ToolResult


# CBP fee defaults — YEAR-SPECIFIC, set by U.S. Customs and Border Protection.
# [UNCERTAIN — verify against the current CBP fee schedule (19 CFR 24.23 / 24.24).]
MPF_PCT_DEFAULT = 0.3464   # Merchandise Processing Fee, ad valorem %, formal entries
MPF_MIN_DEFAULT = 32.71    # per-entry minimum [UNCERTAIN — year-specific]
MPF_MAX_DEFAULT = 634.62   # per-entry maximum [UNCERTAIN — year-specific]
HMF_PCT_DEFAULT = 0.125    # Harbor Maintenance Fee, ad valorem %, OCEAN imports only

_DISCLAIMER = (
    "General estimate only, NOT customs/legal advice. Verify HTS classification "
    "and all duty/tariff rates with a licensed customs broker; Section 301 and "
    "similar tariffs and CBP fee schedules change and are year-specific."
)


class LandedCost(BaseTool):
    name = "landed_cost"
    description = (
        "Estimate US-import landed cost per unit from ex-works price + freight + "
        "insurance + HTS duty + additional tariffs (e.g. Section 301) + CBP fees "
        "(MPF/HMF) + broker + in-transit carrying cost. Isolates the tariff share "
        "so sourcing/origin scenarios compare total landed cost. "
        "Query: 'landed <ex_works_unit> units=<n> duty=<pct> tariff=<pct> "
        "freight=<per_shipment> [freight_unit=<per_unit>] insurance=<pct> "
        "hmf=0.125 broker=<per_shipment> transit_days=<n> cost_of_capital=<annual_pct> "
        "[cv=<customs_value_unit>] [mpf=<pct>|mpf=0]'. General info only."
    )

    def run(self, query: str, **kwargs) -> ToolResult:
        bare, p = self._parse(query)
        # ex-works unit price: from cv-less `ex=`/`ex_works=`, else first bare number
        ex = p.get("ex", p.get("ex_works", p.get("exworks")))
        if ex is None:
            ex = next((b for b in bare if self._is_num(b)), None)
        if ex is None:
            return ToolResult(
                data={}, notes="invalid format — need an ex-works unit price"
            )
        ex_works = self._num(ex)

        units = max(1, int(self._num(p.get("units", "1"))))
        cv_unit = self._num(p["cv"]) if "cv" in p else ex_works  # customs value basis

        # freight per unit: explicit per-unit wins, else per-shipment / units
        if "freight_unit" in p:
            freight_unit = self._num(p["freight_unit"])
        else:
            freight_unit = self._num(p.get("freight", "0")) / units

        insurance_pct = self._num(p.get("insurance", "0"))
        insurance_unit = cv_unit * insurance_pct / 100

        duty_pct = self._num(p.get("duty", "0"))
        base_duty_unit = cv_unit * duty_pct / 100

        tariff_pct = self._num(p.get("tariff", "0"))   # Section 301 / additional
        tariff_unit = cv_unit * tariff_pct / 100

        # MPF is a per-ENTRY ad-valorem fee with a min/max, amortized over units
        mpf_pct = self._num(p.get("mpf", str(MPF_PCT_DEFAULT)))
        mpf_min = self._num(p.get("mpf_min", str(MPF_MIN_DEFAULT)))
        mpf_max = self._num(p.get("mpf_max", str(MPF_MAX_DEFAULT)))
        mpf_advalorem = cv_unit * units * mpf_pct / 100 if mpf_pct > 0 else 0.0
        mpf_entry = min(max(mpf_advalorem, mpf_min), mpf_max) if mpf_pct > 0 else 0.0
        # If the ad-valorem MPF is below the per-entry floor, the $32.71 minimum binds
        # and — spread over a tiny `units` — silently dominates. Flag it so callers see
        # the per-unit figure is a minimum-fee artifact, not a real ad-valorem cost.
        mpf_at_minimum = mpf_pct > 0 and mpf_advalorem < mpf_min
        mpf_unit = mpf_entry / units

        hmf_pct = self._num(p.get("hmf", "0"))  # ocean only — opt in with hmf=0.125
        hmf_unit = cv_unit * hmf_pct / 100

        broker_unit = self._num(p.get("broker", "0")) / units

        # In-transit inventory carrying cost = value × annual cost of capital × days/365
        transit_days = self._num(p.get("transit_days", "0"))
        cost_of_capital = self._num(p.get("cost_of_capital", "0"))
        carrying_unit = cv_unit * (cost_of_capital / 100) * (transit_days / 365)

        landed_unit = (
            ex_works + freight_unit + insurance_unit + base_duty_unit
            + tariff_unit + mpf_unit + hmf_unit + broker_unit + carrying_unit
        )

        # Identify the biggest add-on cost driver beyond the ex-works price.
        drivers = {
            "freight": freight_unit, "insurance": insurance_unit,
            "base_duty": base_duty_unit, "tariff": tariff_unit,
            "mpf": mpf_unit, "hmf": hmf_unit, "broker": broker_unit,
            "in_transit_carrying": carrying_unit,
        }
        biggest = max(drivers, key=drivers.get) if any(drivers.values()) else None

        r = self._r
        data = {
            "ex_works_unit": r(ex_works),
            "customs_value_unit": r(cv_unit),
            "units_per_entry": units,
            "freight_unit": r(freight_unit),
            "insurance_unit": r(insurance_unit),
            "base_duty_unit": r(base_duty_unit),
            "base_duty_pct": duty_pct,
            "tariff_unit": r(tariff_unit),
            "tariff_pct": tariff_pct,
            "mpf_unit": r(mpf_unit),
            "mpf_entry": r(mpf_entry),
            "mpf_at_minimum": mpf_at_minimum,
            "hmf_unit": r(hmf_unit),
            "broker_unit": r(broker_unit),
            "in_transit_carrying_unit": r(carrying_unit),
            "landed_unit": r(landed_unit),
            "duty_plus_tariff_unit": r(base_duty_unit + tariff_unit),
            # The optimization signal: how much of landed cost is additional tariff.
            "tariff_share_pct": r(tariff_unit / landed_unit * 100) if landed_unit else 0.0,
            "biggest_add_on_driver": biggest,
            "disclaimer": _DISCLAIMER,
        }
        return ToolResult(
            data=data,
            sources=[
                "U.S. customs valuation — transaction (FOB/ex-works) value, "
                "19 U.S.C. § 1401a; duty/tariff/MPF/HMF assessed on customs value.",
                "HTS base duty rate — classify with the current Harmonized Tariff "
                "Schedule (USITC, hts.usitc.gov) [UNCERTAIN — verify HTS code + rate].",
                "Additional tariffs (e.g. Section 301, USTR) stack on base duty and "
                "change frequently [UNCERTAIN — verify current action + rate].",
                "CBP fees — Merchandise Processing Fee 0.3464% (min/max per entry) "
                "and Harbor Maintenance Fee 0.125% (ocean only), 19 CFR 24.23/24.24 "
                "[UNCERTAIN — year-specific, verify current CBP fee schedule].",
            ],
            notes=(
                f"MPF is at the per-entry minimum (${mpf_min:,.2f}) spread over "
                f"{units} unit(s) — set realistic units for a meaningful per-unit cost. "
                + _DISCLAIMER
            ) if mpf_at_minimum else _DISCLAIMER,
        )

    # ---- parsing helpers ----
    @staticmethod
    def _parse(query: str) -> tuple[list[str], dict]:
        bare: list[str] = []
        kv: dict[str, str] = {}
        for tok in query.split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                kv[k.lower()] = v
            else:
                bare.append(tok)
        return bare, kv

    @staticmethod
    def _num(s) -> float:
        return float(re.sub(r"[_,$%]", "", str(s)))

    @staticmethod
    def _is_num(s) -> bool:
        try:
            LandedCost._num(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def _r(x: float) -> float:
        return round(x, 4)
