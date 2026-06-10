"""US federal + Texas tax estimates: sales/use tax, self-employment tax,
federal income tax (progressive), federal corporate tax, Texas franchise tax.

⚠️ GENERAL INFORMATION ONLY — NOT TAX ADVICE. These are rough estimates.
Tax rates, brackets, thresholds, and deadlines change every year and depend on
filing status, entity type, and locality. Confirm every figure with a licensed
Texas CPA and the current IRS / Texas Comptroller publications before relying on
it. Values marked [UNCERTAIN] are year-specific placeholders that MUST be verified.

Note: Texas has NO state personal income tax. Personal income is taxed only at
the federal level (IRS). Texas does levy a franchise (margin) tax on entities
and a sales-and-use tax, both administered by the Texas Comptroller.
"""
from __future__ import annotations
import re
from core.tools.base_tool import BaseTool, ToolResult


# Federal individual income-tax MARGINAL RATES are statutory (IRC § 1): the seven
# 2018–2025 rates below are stable, but the DOLLAR THRESHOLDS are inflation-adjusted
# every year and differ by filing status. The thresholds here are single-filer
# PLACEHOLDERS and are NOT verified — they must be confirmed against the current-year
# IRS Revenue Procedure before use.
# [UNCERTAIN — verify current-year thresholds & filing status: IRS Rev. Proc.]
FEDERAL_SINGLE_BRACKETS_UNVERIFIED = [
    (11_600, 0.10),    # [UNCERTAIN — threshold year-specific]
    (47_150, 0.12),    # [UNCERTAIN]
    (100_525, 0.22),   # [UNCERTAIN]
    (191_950, 0.24),   # [UNCERTAIN]
    (243_725, 0.32),   # [UNCERTAIN]
    (609_350, 0.35),   # [UNCERTAIN]
    (float("inf"), 0.37),
]

_DISCLAIMER = (
    "General estimate only, NOT tax advice. Verify with a licensed Texas CPA "
    "and current IRS / Texas Comptroller publications."
)


class TaxCalculator(BaseTool):
    name = "tax_calculator"
    description = (
        "Estimate US federal + Texas taxes: sales/use tax, self-employment tax, "
        "federal income tax, federal corporate tax, Texas franchise tax. "
        "General info only — not tax advice."
    )

    def run(self, query: str, **kwargs) -> ToolResult:
        parts = query.split()
        if len(parts) < 2:
            return ToolResult(data={}, notes="invalid format")

        tax_type = parts[0].lower()
        amount = self._parse_amount(parts[1])
        params = self._parse_kv(parts[2:])

        if tax_type in ("sales_tax", "sales", "use_tax"):
            # Texas state sales-and-use tax is 6.25% (Tex. Tax Code § 151.051);
            # local jurisdictions may add up to 2% (max combined 8.25%).
            rate = float(params.get("rate", 6.25)) / 100
            tax = int(round(amount * rate))
            return ToolResult(
                data={"base_usd": amount, "rate_pct": rate * 100,
                      "tax_amount_usd": tax, "total_usd": amount + tax,
                      "disclaimer": _DISCLAIMER},
                sources=[
                    "Texas Tax Code § 151.051 — state sales-and-use tax rate 6.25%; "
                    "local rates up to 2% (Texas Comptroller, comptroller.texas.gov). "
                    "[UNCERTAIN — confirm your local combined rate]",
                ],
                notes=_DISCLAIMER,
            )

        if tax_type in ("self_employment_tax", "se_tax", "self_employment"):
            # SE tax = 15.3% (12.4% Social Security + 2.9% Medicare) on 92.35% of
            # net self-employment earnings; the Social Security portion is capped
            # at the annual wage base (year-specific).
            # [UNCERTAIN — verify current-year Social Security wage base with IRS/CPA]
            wage_base = self._parse_amount(params.get("ss_wage_base", "168600"))
            net_se = amount * 0.9235
            ss = min(net_se, wage_base) * 0.124
            medicare = net_se * 0.029
            total = int(round(ss + medicare))
            return ToolResult(
                data={"net_se_earnings_usd": amount,
                      "taxable_base_usd": int(round(net_se)),
                      "social_security_usd": int(round(ss)),
                      "medicare_usd": int(round(medicare)),
                      "se_tax_usd": total,
                      "disclaimer": _DISCLAIMER},
                sources=[
                    "IRS Schedule SE; IRC § 1401 — self-employment tax 15.3% "
                    "(12.4% Social Security + 2.9% Medicare) on 92.35% of net earnings. "
                    "Social Security wage base is year-specific "
                    "[UNCERTAIN — verify current-year wage base: IRS].",
                ],
                notes=_DISCLAIMER,
            )

        if tax_type in ("federal_income_tax", "income_tax", "fit"):
            # Progressive federal individual income tax. Thresholds are UNVERIFIED
            # placeholders (see FEDERAL_SINGLE_BRACKETS_UNVERIFIED).
            deduction = self._parse_amount(params.get("deduction", "0"))
            taxable = max(0, amount - deduction)
            tax = self._progressive(taxable, FEDERAL_SINGLE_BRACKETS_UNVERIFIED)
            eff = (tax / amount * 100) if amount else 0
            return ToolResult(
                data={"gross_income_usd": amount, "deduction_usd": deduction,
                      "taxable_usd": taxable, "tax_usd": tax,
                      "net_usd": amount - tax,
                      "effective_rate_pct": round(eff, 2),
                      "disclaimer": _DISCLAIMER},
                sources=[
                    "IRS — federal individual income tax is progressive "
                    "(marginal rates 10/12/22/24/32/35/37%, IRC § 1). Bracket dollar "
                    "thresholds are inflation-adjusted yearly and depend on filing "
                    "status [UNCERTAIN — verify current-year thresholds: IRS Rev. Proc.]. "
                    "Texas has NO state personal income tax.",
                ],
                notes=(
                    "Single-filer brackets, UNVERIFIED placeholders. " + _DISCLAIMER
                ),
            )

        if tax_type in ("federal_corporate_tax", "corporate_tax", "cit"):
            # C corporation flat rate 21% (IRC § 11). Most single-member LLCs and
            # sole proprietorships are pass-through (reported on Form 1040), not
            # subject to corporate income tax.
            rate = float(params.get("rate", 21)) / 100
            tax = int(round(amount * rate))
            return ToolResult(
                data={"profit_usd": amount, "rate_pct": rate * 100,
                      "tax_usd": tax, "net_usd": amount - tax,
                      "disclaimer": _DISCLAIMER},
                sources=[
                    "IRS — C corporation flat 21% (IRC § 11). Most single-member "
                    "LLCs / sole proprietorships are pass-through entities (income "
                    "reported on the owner's Form 1040), not subject to corporate tax. "
                    "[Verify entity treatment with CPA]",
                ],
                notes=_DISCLAIMER,
            )

        if tax_type in ("franchise_tax", "franchise", "margin_tax"):
            # Texas franchise (margin) tax (Tex. Tax Code ch. 171). Entities below
            # the annual no-tax-due revenue threshold owe no franchise tax. Margin
            # rates and the threshold are year-specific.
            # [UNCERTAIN — verify threshold + rate with Texas Comptroller/CPA]
            no_tax_due_threshold = self._parse_amount(
                params.get("no_tax_due_threshold", "2470000"))
            rate = float(params.get("rate", 0.75)) / 100  # 0.375% retail/wholesale, else 0.75%
            if amount < no_tax_due_threshold:
                tax = 0
                note = (
                    f"Revenue below the no-tax-due threshold "
                    f"(~${no_tax_due_threshold:,}) [UNCERTAIN] — likely no franchise "
                    f"tax due, but a Public Information Report may still be required. "
                    + _DISCLAIMER
                )
            else:
                tax = int(round(amount * rate))
                note = _DISCLAIMER
            return ToolResult(
                data={"total_revenue_usd": amount,
                      "no_tax_due_threshold_usd": no_tax_due_threshold,
                      "rate_pct": rate * 100, "franchise_tax_usd": tax,
                      "disclaimer": _DISCLAIMER},
                sources=[
                    "Texas franchise (margin) tax — Tex. Tax Code ch. 171 "
                    "(Texas Comptroller, comptroller.texas.gov). No-tax-due revenue "
                    "threshold and margin rates (0.375% retail/wholesale, 0.75% other) "
                    "are year-specific [UNCERTAIN — verify with Texas Comptroller/CPA].",
                ],
                notes=note,
            )

        return ToolResult(data={}, notes=f"Unknown tax type: {tax_type}")

    @staticmethod
    def _parse_amount(s) -> int:
        s = str(s)
        return int(re.sub(r"[_,.$]", "", s))

    @staticmethod
    def _parse_kv(parts: list[str]) -> dict:
        out = {}
        for p in parts:
            if "=" in p:
                k, v = p.split("=", 1)
                out[k] = v
        return out

    @staticmethod
    def _progressive(taxable: int, brackets: list[tuple[float, float]]) -> int:
        tax = 0
        prev = 0
        for ceil, rate in brackets:
            if taxable <= prev:
                break
            slice_amount = min(taxable, ceil) - prev
            tax += int(slice_amount * rate)
            prev = ceil
            if taxable <= ceil:
                break
        return tax
