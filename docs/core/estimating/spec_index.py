"""Project Manual → spec index (sections by MasterFormat number) + Division 00/01 key requirements.

MasterFormat section numbers look like `01 21 00` (six digits in three pairs, sometimes with a
`.13` suffix). The index is built from the manual itself — the canonical CSI title list is CSI's IP,
and a project's own titles are what the estimator must match anyway.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from core.estimating.pdfio import open_pdf

DIVISIONS = {
    "00": "Procurement and Contracting Requirements", "01": "General Requirements", "02": "Existing Conditions",
    "03": "Concrete", "04": "Masonry", "05": "Metals", "06": "Wood, Plastics, and Composites",
    "07": "Thermal and Moisture Protection", "08": "Openings", "09": "Finishes", "10": "Specialties",
    "11": "Equipment", "12": "Furnishings", "13": "Special Construction", "14": "Conveying Equipment",
    "21": "Fire Suppression", "22": "Plumbing", "23": "Heating, Ventilating, and Air Conditioning (HVAC)",
    "25": "Integrated Automation", "26": "Electrical", "27": "Communications", "28": "Electronic Safety and Security",
    "31": "Earthwork", "32": "Exterior Improvements", "33": "Utilities", "34": "Transportation",
    "35": "Waterway and Marine Construction", "40": "Process Interconnections", "41": "Material Processing and Handling Equipment",
    "42": "Process Heating, Cooling, and Drying Equipment", "43": "Process Gas and Liquid Handling, Purification, and Storage Equipment",
    "44": "Pollution and Waste Control Equipment", "45": "Industry-Specific Manufacturing Equipment",
    "46": "Water and Wastewater Equipment", "48": "Electrical Power Generation",
}

_SECTION_RE = re.compile(
    r"(?:^|\n)\s*(?:SECTION\s+)?(?P<num>\d{2}\s?\d{2}\s?\d{2}(?:\.\d{2})?)\s*[—–\-:]?\s*(?P<title>[A-Z][A-Z0-9 ,&/()'\-\.]{3,80})(?=\n|$)"
)
_MONEY_RE = r"\$\s?([\d,]+(?:\.\d{2})?)"


@dataclass
class SpecSection:
    number: str
    division: str
    title: str
    page_start: int
    page_end: int


@dataclass
class SpecIndex:
    file: str
    pages: int
    sections: list[SpecSection] = field(default_factory=list)

    @property
    def divisions(self) -> dict[str, list[SpecSection]]:
        out: dict[str, list[SpecSection]] = {}
        for s in self.sections:
            out.setdefault(s.division, []).append(s)
        return out

    def to_json(self) -> str:
        return json.dumps({"file": self.file, "pages": self.pages, "sections": [asdict(s) for s in self.sections]}, indent=2)


def _norm(num: str) -> str:
    digits = re.sub(r"\s", "", num)
    base, _, suffix = digits.partition(".")
    base = f"{base[0:2]} {base[2:4]} {base[4:6]}"
    return base + (f".{suffix}" if suffix else "")


def page_texts(pdf_path: Path) -> list[str]:
    with open_pdf(pdf_path) as pdf:
        return [(pg.extract_text() or "") for pg in pdf.pages]


def index_manual(pdf_path: Path, texts: list[str] | None = None) -> SpecIndex:
    texts = texts if texts is not None else page_texts(pdf_path)
    idx = SpecIndex(file=pdf_path.name, pages=len(texts))
    seen: dict[str, SpecSection] = {}
    toc_pages = {i for i, t in enumerate(texts) if re.search(r"TABLE OF CONTENTS", t, re.IGNORECASE)}
    for i, t in enumerate(texts):
        if i in toc_pages:
            continue
        for m in _SECTION_RE.finditer(t):
            num = _norm(m.group("num"))
            title = re.sub(r"\s+", " ", m.group("title")).strip(" -—")
            if num in seen:
                seen[num].page_end = max(seen[num].page_end, i + 1)
                continue
            s = SpecSection(number=num, division=num[:2], title=title, page_start=i + 1, page_end=i + 1)
            seen[num] = s
            idx.sections.append(s)
    # page_end = page before the next section starts
    ordered = sorted(idx.sections, key=lambda s: s.page_start)
    for a, b in zip(ordered, ordered[1:]):
        a.page_end = max(a.page_start, b.page_start - 1) if b.page_start > a.page_start else a.page_end
    if ordered:
        ordered[-1].page_end = max(ordered[-1].page_start, len(texts))
    idx.sections = sorted(idx.sections, key=lambda s: s.number)
    return idx


def division_01_summary(texts: list[str]) -> dict:
    """Cost-carrying items from Division 00/01 found by pattern; every value cites the page."""
    joined = "\n".join(f"[[p{i + 1}]]\n{t}" for i, t in enumerate(texts))

    def find(pattern: str, flags=re.IGNORECASE) -> list[dict]:
        out = []
        for m in re.finditer(pattern, joined, flags):
            page = joined.rfind("[[p", 0, m.start())
            pno = int(re.match(r"\[\[p(\d+)\]\]", joined[page:]).group(1)) if page >= 0 else None
            groups = [g for g in m.groups() if g]
            if any(o["groups"] == groups and groups for o in out):
                continue  # the same alternate/unit price/allowance restated on another page
            out.append({"match": m.group(0).strip()[:160], "page": pno, "groups": groups})
        return out

    summary = {
        "bid_due": find(r"bids?\s+(?:are\s+)?due\s+(?:on\s+)?(\d{1,2}/\d{1,2}/\d{4})[^\n]*"),
        "rfi_cutoff": find(r"(?:RFI|requests? for information)[^\n]{0,80}?(\d{1,2}/\d{1,2}/\d{4})"),
        "bid_bond": find(r"bid bond[^\n]{0,40}?(\d{1,2})\s?%"),
        "bonds_100": find(r"(performance and payment bonds?)[^\n]{0,60}?(\d{2,3})\s?%"),
        "duration": find(r"(\d{2,4})\s+(?:calendar|working)\s+days"),
        "liquidated_damages": find(r"liquidated damages[^\n]{0,40}?" + _MONEY_RE + r"\s*per\s+(?:calendar\s+)?day"),
        "allowances": find(r"allowance of\s*" + _MONEY_RE + r"\s+for\s+([^\n.;]{3,80})"),
        "alternates": find(r"Alternate No\.?\s*(\d+)\s*\((ADD|DEDUCT)\)"),
        "unit_prices": find(r"Unit Price No\.?\s*(\d+)[:\s]+([^\n.]{3,80})"),
        "addenda": find(r"Addend(?:um|a) No\.?\s*(\d+)[^\n]{0,40}?(\d{1,2}/\d{1,2}/\d{4})?"),
        "retainage": find(r"retainage[^\n]{0,60}?(\d{1,2})\s?%"),
        "prevailing_wage": find(r"(Davis-Bacon|prevailing wage)"),
        "special_inspections": find(r"special inspections?[^\n]{0,120}?(paid by the (?:owner|contractor))"),
        "leed": find(r"\b(LEED|green building certification)\b"),
        "temporary_facilities": find(r"(job trailer|temporary (?:power|water|fence|toilets?)|dumpsters?)"),
        "not_in_contract": find(r"not in contract[:\s]+([^\n.]{3,160})"),
        "separate_contract": find(r"([^\n.]{3,120}?(?:by|under) a separate contract)"),
        "owner_furnished": find(r"owner-furnished[^\n]{0,120}"),
    }
    return summary


def spec_index_markdown(idx: SpecIndex, div01: dict | None = None) -> str:
    out = ["---", "type: spec_index", f"sections: {len(idx.sections)}", f"pages: {idx.pages}", "---",
           f"# Specification index — {idx.file}", "", "| Section | Division | Title | Pages |", "|---|---|---|---|"]
    for s in idx.sections:
        out.append(f"| {s.number} | {s.division} {DIVISIONS.get(s.division, '')} | {s.title} | {s.page_start}–{s.page_end} |")
    if div01:
        out += ["", "## Division 00 / 01 — cost-carrying items (pattern hits, cite the page)"]
        for key, hits in div01.items():
            if not hits:
                continue
            out.append(f"- **{key}**: " + " · ".join(f"{h['match']} (p{h['page']})" for h in hits[:6]))
    return "\n".join(out) + "\n"
