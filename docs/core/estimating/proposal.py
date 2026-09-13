"""Client-facing proposal / scope letter — assembled from the approved estimate, never from a model's
numbers. Hides every internal figure (unit costs, sources, markups, flags)
shows scope, quantities
where useful, the price (single for Class ≤ 3, low / target / high for Class ≥ 4), allowances,
alternates, assumptions, exclusions, validity and the accuracy statement. Runs the client-safe scan.
"""
from __future__ import annotations

from core.estimating.client_safe import blocking, report as scan_report, scan
from core.estimating.spec_index import DIVISIONS

_HIDE_NOTE_TOKENS = ("[UNCERTAIN]", "seed", "placeholder", "library", "AUTO-ASSUMED", "derived", "readers", "confidence")


def _client_description(desc: str) -> str:
    d = desc
    for tok in ("(from steel schedule)", "(from notes)", "(from elevation note)", "(footprint)", "(perimeter × average height)"):
        d = d.replace(tok, "")
    return d.strip(" —-")


def proposal_markdown(profile: dict, estimate: dict, ledger_items: list[dict], questions: list[dict], company: dict | None = None,
                      exclusions_extra: list[str] | None = None, validity_days: int = 30) -> tuple[str, list]:
    company = company or {"name": "[Company name]", "contact": "[Name, title]", "email": "[email]", "phone": "[phone]"}
    markups = {m["name"]: m for m in estimate["markups"]}
    total = markups.get("TOTAL BID", {}).get("amount", 0.0)
    cls = int(profile.get("aace_class", 2))
    band = profile.get("accuracy_band", "")
    tp = estimate["meta"].get("three_point")
    gsf = float(profile.get("gross_sf") or 0)
    allowances = [it for it in ledger_items if it.get("method") == "allowance"]
    out = ["---", "type: proposal_draft", "status: draft", f"class: {cls}", "---",
           f"# Proposal — {profile.get('name', '')}", "",
           f"**To:** [Client name] · **From:** {company['name']} · **Date:** [date] · **Valid for:** {validity_days} days", "",
           "## Project", f"- {profile.get('building_type', '')}, approximately {gsf:,.0f} SF, {profile.get('city', '')}",
           f"- Estimate basis: {'construction documents and Project Manual' if cls <= 3 else 'preliminary information (' + ('partial drawings' if cls == 4 else 'program, notes and photos') + ')'} — "
           f"AACE Class {cls} estimate, expected accuracy {band}", ""]
    # scope by division
    out += ["## Scope of work", ""]
    by_div: dict[str, list[dict]] = {}
    for it in ledger_items:
        if it.get("method") == "allowance":
            continue
        by_div.setdefault(it["division"], []).append(it)
    for div in sorted(by_div):
        out.append(f"**Division {div} — {DIVISIONS.get(div, '')}**")
        seen = set()
        for it in by_div[div]:
            d = _client_description(it["description"])
            key = d.lower()
            if key in seen:
                continue
            seen.add(key)
            qty = f" — {it['qty']:,.0f} {it['unit']}" if it["unit"] in ("EA", "LF", "SF", "SY", "CY", "SQ", "TON") and it["qty"] >= 1 else ""
            out.append(f"- {d}{qty}")
        out.append("")
    # price
    out += ["## Price", ""]
    if cls >= 4 and tp:
        out += ["| Low | Target | High |", "|---|---|---|",
                f"| ${tp['low']['total']:,.0f} | **${tp['target']['total']:,.0f}** | ${tp['high']['total']:,.0f} |", "",
                f"Budgetary range for planning; a firm price follows complete drawings and subcontractor pricing. Expected accuracy for this estimate class: {band}.", ""]
    else:
        out += [f"**Lump sum: ${total:,.0f}**" + (f" (${total / gsf:,.2f} per SF)" if gsf else ""), "", f"Expected accuracy for this estimate class: {band}.", ""]
    if allowances:
        out += ["## Allowances (included in the price, adjusted to actual cost)", ""]
        for a in allowances:
            amt = float((a.get("tags") or {}).get("amount") or 0)
            out.append(f"- {_client_description(a['description'])}: ${amt:,.0f}" if amt else f"- {_client_description(a['description'])}")
        out.append("")
    assumptions = [q for q in questions if q.get("assumption")]
    out += ["## Assumptions and clarifications", ""]
    if assumptions:
        for q in assumptions[:30]:
            out.append(f"- {q['text'].split('.')[0].strip()}: assumed {('as stated in our review' if 'AUTO' in (q.get('assumption') or '') else q.get('assumption'))}.")
    out.append("- Work is priced for normal business hours unless stated otherwise.")
    out.append("")
    out += ["## Exclusions", ""]
    excl = list(exclusions_extra or []) + [f"Division {d}: {why.split(' (')[0]}" for d, why in (profile.get("exclusions") or {}).items()]
    excl += ["Permit and impact fees unless stated", "Hazardous materials abatement", "Unforeseen subsurface or concealed conditions", "Utility company fees and service extensions",
             "Owner-furnished equipment and furnishings", "Low-voltage cabling beyond raceway"]
    seen = set()
    for e in excl:
        if e.lower() in seen:
            continue
        seen.add(e.lower())
        out.append(f"- {e}")
    out += ["", "## Schedule", f"- Estimated duration: {profile.get('duration_days') or '[to be confirmed]'} calendar days from notice to proceed, subject to permitting and inspections.", "",
            "## Terms", f"- This proposal is valid for {validity_days} days. Pricing is subject to written acceptance and a mutually agreed contract form.",
            "- Retainage, payment terms and bonding per the contract documents.", "",
            f"{company['name']} · {company['contact']} · {company['email']} · {company['phone']}", ""]
    text = "\n".join(out)
    findings = scan(text)
    if blocking(findings):
        text = text.replace("status: draft", "status: HOLD — client-safe scan found blocking items", 1)
    return text, findings


def findings_markdown(findings: list) -> str:
    return scan_report(findings)
