"""Compliance / certification tracker — deterministic status & expiry monitor.

Given a certification or compliance item (RoHS, REACH, UL, FCC, CE, ITAR/export,
conflict minerals, ...) with a status and/or expiry date, this returns a
normalized status (Valid / Expiring soon / Expired / Pending / Missing /
Non-compliant), days-to-expiry, whether the product is shippable with respect to
that item, a risk tier, and a recommended action. Deterministic — no API key.

Division-of-labor: the AGENT gathers the cert facts (issue/expiry dates, current
status) from the certificate or the compliance system; this tool does the
date math and status logic so the answer is consistent every run.

⚠ GENERAL INFORMATION ONLY — NOT legal or regulatory advice. Confirm applicability
(which certs are required for which region/product) and every date against the
certificate of record and a qualified compliance/regulatory professional.
"""
from __future__ import annotations
import re
from datetime import date
from core.tools.base_tool import BaseTool, ToolResult

# explicit status inputs → canonical status (date logic can still override "valid")
_STATUS = {
    "valid": "Valid", "active": "Valid", "certified": "Valid",
    "pending": "Pending", "in_progress": "Pending", "applied": "Pending",
    "expired": "Expired",
    "missing": "Missing", "none": "Missing",
    "noncompliant": "Non-compliant", "non_compliant": "Non-compliant", "fail": "Non-compliant",
}

_DISCLAIMER = (
    "General information only, NOT legal/regulatory advice. Confirm which certs are "
    "required for the region/product and verify every date against the certificate "
    "of record with a qualified compliance professional."
)


class ComplianceTracker(BaseTool):
    name = "compliance_tracker"
    description = (
        "Track a certification / compliance item's status & expiry. Inputs: status "
        "(valid|pending|expired|missing|noncompliant), expiry (YYYY-MM-DD) or "
        "days_to_expiry, required (yes/no), lead_time_days (renewal lead, default 90), "
        "as_of (YYYY-MM-DD, default today). Returns normalized status, days-to-expiry, "
        "shippable flag, risk tier, recommended action. "
        "Query: 'cert RoHS status=valid expiry=2026-09-15 required=yes'. "
        "Deterministic; general info only."
    )

    def run(self, query: str, **kwargs) -> ToolResult:
        cert, p = self._parse(query)

        required = self._truthy(p.get("required", "yes"))  # default: it matters
        lead = int(self._num(p.get("lead_time_days", "90")))
        as_of = self._date(p.get("as_of")) or date.today()

        days_to_expiry = None
        expiry_date = None
        if "expiry" in p or "expiry_date" in p:
            expiry_date = self._date(p.get("expiry", p.get("expiry_date")))
            if expiry_date:
                days_to_expiry = (expiry_date - as_of).days
        elif "days_to_expiry" in p:
            days_to_expiry = int(self._num(p["days_to_expiry"]))

        explicit = _STATUS.get(str(p.get("status", "")).strip().lower())

        status = self._resolve_status(explicit, days_to_expiry, lead)
        if status is None:
            return ToolResult(
                data={}, notes="no cert status or expiry provided — see tool description"
            )

        # A REQUIRED cert only permits shipment once it is actually in force. Pending
        # (not yet issued), Expired, Missing, and Non-compliant all block shipment
        # when the cert is required; an optional cert never blocks.
        shippable = status in ("Valid", "Expiring soon") or not required
        tier = self._tier(status, required)
        action = self._action(status, required, days_to_expiry, lead)

        data = {
            "cert": cert or "(unnamed)",
            "status": status,
            "required": required,
            "expiry_date": expiry_date.isoformat() if expiry_date else None,
            "days_to_expiry": days_to_expiry,
            "renewal_lead_days": lead,
            "risk_tier": tier,
            "shippable": shippable,
            "recommended_action": action,
            "as_of": as_of.isoformat(),
            "disclaimer": _DISCLAIMER,
        }
        return ToolResult(
            data=data,
            sources=[
                "Compliance-status model (bd-business-os): expiry-date math + "
                "renewal-lead window; a required cert that is Expired/Missing/"
                "Non-compliant blocks shipment.",
                "Applicability and dates must be primary-sourced from the certificate "
                "of record and confirmed with a qualified compliance professional "
                "[UNCERTAIN — verify which certs each region/product requires].",
            ],
            notes=_DISCLAIMER,
        )

    # ---- logic ----
    @staticmethod
    def _resolve_status(explicit, days_to_expiry, lead):
        # explicit non-valid states win outright
        if explicit in ("Expired", "Missing", "Non-compliant", "Pending"):
            return explicit
        # otherwise derive from the expiry date if we have one
        if days_to_expiry is not None:
            if days_to_expiry < 0:
                return "Expired"
            if days_to_expiry <= lead:
                return "Expiring soon"
            return "Valid"
        if explicit == "Valid":
            return "Valid"
        return None

    @staticmethod
    def _tier(status, required) -> str:
        base = {
            "Valid": "Low", "Pending": "Moderate", "Expiring soon": "High",
            "Expired": "Critical", "Missing": "Critical", "Non-compliant": "Critical",
        }[status]
        if not required and base in ("Critical", "High"):
            # non-required cert can't be shipment-blocking → down-rate one notch
            return {"Critical": "Moderate", "High": "Low"}[base]
        return base

    @staticmethod
    def _action(status, required, days_to_expiry, lead) -> str:
        req = "required" if required else "optional"
        if status == "Valid":
            return f"Valid ({req}) — no action; monitor before the renewal window."
        if status == "Expiring soon":
            d = f"{days_to_expiry}d left" if days_to_expiry is not None else "within lead window"
            return f"Start renewal now — {d}, inside the {lead}d renewal lead ({req})."
        if status == "Expired":
            return ("Expired — product NOT shippable until renewed; escalate to compliance."
                    if required else "Expired — renew when convenient (not shipment-blocking).")
        if status == "Missing":
            return ("Obtain certification before launch — product NOT shippable ({}).".format(req)
                    if required else "Optional cert not held — no shipment impact.")
        if status == "Non-compliant":
            return ("Non-compliant — halt shipment, open a corrective action, re-test."
                    if required else "Non-compliant on an optional item — assess and remediate.")
        if status == "Pending":
            return f"Certification in progress ({req}) — track to issuance before launch."
        return "Review status."

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
        if bare and bare[0].lower() in ("cert", "compliance", "compliance_tracker"):
            bare = bare[1:]
        return " ".join(bare).strip(), kv

    @staticmethod
    def _date(s):
        if not s:
            return None
        try:
            return date.fromisoformat(str(s).strip())
        except ValueError:
            return None

    @staticmethod
    def _num(s) -> float:
        return float(re.sub(r"[_,$%]", "", str(s)))

    @staticmethod
    def _truthy(v) -> bool:
        return str(v).strip().lower() in ("1", "yes", "y", "true", "t", "required")
