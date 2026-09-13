"""8D / CAPA engine — deterministic corrective-action progress & aging tracker.

Given a corrective action's state — how far through the 8 Disciplines it is, how
long it has been open, its severity, whether interim containment is in place, and
whether it is a repeat — this returns a status (On Track / At Risk / Overdue /
Closed), completeness %, the current & next discipline, risk flags, and a
recommended action. Deterministic — no API key needed.

The 8 Disciplines (8D): D1 team · D2 problem description · D3 interim containment
· D4 root cause · D5 choose permanent corrective action · D6 implement & validate
PCA · D7 prevent recurrence · D8 closure & recognition.

⚠ GENERAL DECISION-SUPPORT ONLY — a process aid for tracking 8D/CAPA discipline,
not a substitute for your QMS's controlled records or a quality engineer's review.
"""
from __future__ import annotations
import re
from core.tools.base_tool import BaseTool, ToolResult

_DISCIPLINES = {
    1: "D1 — Form the team",
    2: "D2 — Describe the problem",
    3: "D3 — Interim containment action",
    4: "D4 — Root-cause analysis",
    5: "D5 — Choose permanent corrective action (PCA)",
    6: "D6 — Implement & validate the PCA",
    7: "D7 — Prevent recurrence",
    8: "D8 — Closure & team recognition",
}

# severity → default SLA days to close (used when sla_days not supplied)
_SEVERITY_SLA = {"critical": 30, "high": 45, "medium": 60, "low": 90}

_DISCLAIMER = (
    "General decision-support only — a process aid, not a controlled QMS record; "
    "confirm containment, root cause, and closure with the quality owner."
)


class Capa8D(BaseTool):
    name = "capa_8d"
    description = (
        "Track an 8D/CAPA's progress & aging. Inputs: step (highest completed "
        "discipline 1-8), days_open, sla_days (or inferred from severity), severity "
        "(low|medium|high|critical), containment (yes/no), recurrence (yes/no). "
        "Returns status (On Track/At Risk/Overdue/Closed), completeness %, current & "
        "next discipline, flags, recommended action. "
        "Query: 'capa <id> step=4 days_open=45 sla_days=60 severity=high "
        "containment=yes recurrence=no'. Deterministic; general info only."
    )

    def run(self, query: str, **kwargs) -> ToolResult:
        capa_id, p = self._parse(query)
        if not any(k in p for k in ("step", "days_open", "severity")):
            return ToolResult(
                data={}, notes="no CAPA signals provided — see tool description"
            )

        step = int(self._clamp(self._num(p.get("step", "0")), 0, 8))
        severity = str(p.get("severity", "medium")).strip().lower()
        if severity not in _SEVERITY_SLA:
            severity = "medium"
        sla = int(self._num(p["sla_days"])) if "sla_days" in p else _SEVERITY_SLA[severity]
        days_open = self._num(p.get("days_open", "0"))
        containment = self._truthy(p.get("containment", "")) or step >= 3
        recurrence = self._truthy(p.get("recurrence", ""))

        closed = step >= 8
        completeness = round(step / 8 * 100, 1)
        aging_ratio = round(days_open / sla, 2) if sla else 0.0
        overdue = not closed and aging_ratio > 1.0
        containment_gap = (
            severity in ("high", "critical") and not containment and not closed
        )

        flags: list[str] = []
        if containment_gap:
            flags.append("No interim containment (D3) on an open high/critical issue")
        if overdue:
            flags.append(f"Overdue — {days_open:.0f}d open vs {sla}d SLA")
        if recurrence:
            flags.append("Recurrence — repeat problem; verify prior CAPA effectiveness")
        if not closed and step < 4 and aging_ratio > 0.5:
            flags.append("Root cause (D4) not reached past half the SLA window")

        # "Overdue" is reserved for genuinely past-SLA. A containment gap is loud but
        # separate: it drives escalation/priority, not the Overdue label.
        status = self._status(closed, overdue, aging_ratio, bool(flags))
        current = _DISCIPLINES.get(step, "Not started")
        next_action = (
            "Closed — confirm D6/D7 effectiveness is signed off."
            if closed else _DISCIPLINES[step + 1]
        )

        escalate = overdue or containment_gap
        rec = self._recommend(status, next_action, escalate, containment_gap, recurrence)
        priority = "P1" if severity == "critical" or escalate else (
            "P2" if severity == "high" or recurrence else "P3"
        )

        data = {
            "capa": capa_id or "(unnamed)",
            "status": status,
            "completeness_pct": completeness,
            "current_discipline": current,
            "next_action": next_action,
            "aging_ratio": aging_ratio,      # days_open / SLA (>1 = overdue)
            "sla_days": sla,
            "severity": severity,
            "priority": priority,
            "containment_in_place": containment,
            "recurrence": recurrence,
            "escalate": escalate,
            "flags": flags,
            "recommended_action": rec,
            "disclaimer": _DISCLAIMER,
        }
        return ToolResult(
            data=data,
            sources=[
                "8D / CAPA discipline model (bd-business-os): D1–D8 completeness + "
                "aging vs SLA + containment/recurrence flags. SLA defaults by severity "
                "(critical 30d, high 45d, medium 60d, low 90d) unless sla_days supplied.",
                "Status is a process aid — the controlled 8D record, containment "
                "evidence, and closure sign-off live in the QMS "
                "[UNCERTAIN — confirm with the quality owner].",
            ],
            notes=_DISCLAIMER,
        )

    # ---- logic ----
    @staticmethod
    def _status(closed, overdue, aging_ratio, has_flags) -> str:
        if closed:
            return "Closed"
        if overdue:
            return "Overdue"
        if aging_ratio >= 0.75 or has_flags:
            return "At Risk"
        return "On Track"

    @staticmethod
    def _recommend(status, next_action, escalate, containment_gap, recurrence) -> str:
        if status == "Closed":
            return "Closed — archive the 8D and monitor for recurrence."
        prefix = {"Overdue": "Overdue — ", "At Risk": "At risk — ",
                  "On Track": "On track — "}[status]
        steps: list[str] = []
        if escalate:
            steps.append("escalate to the quality manager")
        if containment_gap:
            steps.append("put interim containment (D3) in place now")
        steps.append(f"advance to {next_action}")
        rec = prefix + "; ".join(steps) + "."
        if recurrence:
            rec += " Re-open the prior CAPA's effectiveness check."
        return rec

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
        if bare and bare[0].lower() in ("capa", "8d", "capa_8d"):
            bare = bare[1:]
        return " ".join(bare).strip(), kv

    @staticmethod
    def _num(s) -> float:
        return float(re.sub(r"[_,$%]", "", str(s)))

    @staticmethod
    def _truthy(v) -> bool:
        return str(v).strip().lower() in ("1", "yes", "y", "true", "t", "done", "complete")

    @staticmethod
    def _clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))
