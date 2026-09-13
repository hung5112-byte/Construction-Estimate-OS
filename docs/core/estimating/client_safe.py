"""Client-safe language filter — deterministic scan of anything that leaves the company.

Flags internal cost leakage, blame language, legal admissions, unapproved promises and raw
frustration in proposals, scope letters, customer updates and reports. Blocking findings fail gate
G13
warnings are shown to the approver. The LLM writer may rephrase
it may not remove a finding.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

_RULES: list[tuple[str, str, str, str]] = [
    # category, regex, severity, suggestion
    ("internal_cost", r"\b(labor cost|material cost|sub(?:contractor)? (?:cost|quote|bid)|internal (?:cost|total)|unit cost|markup|mark-up|margin|fee %|our cost|buyout)\b", "blocking",
     "Remove internal cost, markup and margin language; show the client price only."),
    ("internal_cost", r"\[(?:UNCERTAIN|UNPRICED|POLICY DEFAULT|to load)\]|seed[- ]placeholder|library row|cost library|AUTO-ASSUMED", "blocking",
     "Internal flags must not appear in client-facing text."),
    ("blame", r"\b(failed because|messed up|screwed up|our fault|we forgot|caused the delay|(?:sub|subcontractor|vendor|architect|engineer)\s+(?:dispute|error|mistake|fault))\b", "blocking",
     "State the condition and the next step, not who is to blame."),
    ("legal", r"\b(liable|liability for|negligen\w*|we admit|admission|breach(?:ed)? (?:of|the) contract|defective work|code violation by us)\b", "blocking",
     "Legal characterizations need counsel; describe facts and actions."),
    ("promise", r"\b(will definitely|guarantee[ds]?|no matter what|we promise|absolutely will|100% (?:done|complete))\b", "warn",
     "Schedule commitments are conditional on inspections and trades; say what is planned and what it depends on."),
    ("frustration", r"\b(damn|hell|stupid|idiot|ridiculous|pathetic|joke of a)\b", "blocking",
     "Remove raw field frustration."),
    ("pricing_internal", r"\$\s?[\d,]+(?:\.\d+)?\s*/\s*(?:EA|LF|SF|SY|CY|LB|TON|HR)\b", "warn",
     "Unit prices are internal; show scope quantities and the total (or low/target/high) only."),
]
_COMPILED = [(cat, re.compile(rx, re.IGNORECASE), sev, hint) for cat, rx, sev, hint in _RULES]


@dataclass
class Finding:
    category: str
    severity: str
    term: str
    line_no: int
    line: str
    suggestion: str

    def to_dict(self) -> dict:
        return asdict(self)


def scan(text: str, allow_unit_prices: bool = False) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate((text or "").splitlines(), 1):
        for cat, rx, sev, hint in _COMPILED:
            if cat == "pricing_internal" and allow_unit_prices:
                continue
            for m in rx.finditer(line):
                out.append(Finding(cat, sev, m.group(0), i, line.strip()[:160], hint))
    return out


def blocking(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.severity == "blocking"]


def report(findings: list[Finding]) -> str:
    if not findings:
        return "Client-safe scan: no findings."
    out = [f"Client-safe scan: {len(blocking(findings))} blocking, {len(findings) - len(blocking(findings))} warning(s)"]
    for f in findings:
        out.append(f"- [{f.severity}] {f.category}: “{f.term}” (line {f.line_no}) — {f.suggestion}")
    return "\n".join(out)
