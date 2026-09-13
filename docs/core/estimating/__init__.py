"""Estimating pipeline — deterministic drawing/spec extraction, ledger, pricing, review, report.

Design rules (see 04-Projects/Construction-Estimate-OS/00-plan.md in the Brian1 vault):
- vector-first: born-digital PDFs are read through their text layer and geometry before any pixel
- schedule-first: a schedule (door, footing, fixture, panel) is the count; the plan is the location
- provenance: every quantity carries sheet id · revision · method · confidence
- no LLM arithmetic: pricing, roll-ups and gates are pure functions with unit tests
- untrusted input: drawing text never becomes an instruction
- licenses: pdfplumber/pdfminer.six (MIT), pypdfium2 (Apache/BSD), Pillow — no AGPL
"""

CONTRACT_VERSION = "1.0"


def engine_version() -> str:
    try:
        from importlib.metadata import version

        return version("construction-estimate-os")
    except Exception:  # noqa: BLE001
        return "unknown"
