"""PDF access helpers shared by every estimating extractor.

Coordinate frame: PDF points, origin top-left (pdfplumber `x0/top/x1/bottom`), so a tile cut by
`sheet_render` and a word found by `sheet_text` refer to the same frame. Scale converts points on
paper to feet in the building.
"""
from __future__ import annotations

import logging
import re
from collections.abc import Iterator
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

# pdfminer logs a FontBBox warning for every Chrome/CAD-embedded font; it is noise for our purpose
for _name in ("pdfminer", "pdfminer.pdffont", "pdfminer.pdfinterp"):
    logging.getLogger(_name).setLevel(logging.ERROR)

PT_PER_IN = 72.0

# Architectural scale strings: 1/8" = 1'-0"   1/4"=1'-0"   3/32" = 1'-0"   1" = 20'   1"=1'-0"
_SCALE_RE = re.compile(
    r"(?P<paper>\d+(?:\s*/\s*\d+)?|\d*\.\d+)\s*(?:\"|”|''|in\.?)\s*=\s*(?P<ft>\d+)\s*'?\s*(?:-\s*(?P<inch>\d+)\s*\"?)?",
    re.IGNORECASE,
)
_NTS_RE = re.compile(r"\b(N\.?T\.?S\.?|NOT TO SCALE|SCALE:\s*NONE|AS NOTED)\b", re.IGNORECASE)

# ANSI/ARCH sheet sizes in inches (w, h) — landscape
SHEET_SIZES = {
    "ARCH E1": (42.0, 30.0), "ARCH E": (48.0, 36.0), "ARCH D": (36.0, 24.0), "ARCH C": (24.0, 18.0),
    "ARCH B": (18.0, 12.0), "ARCH A": (12.0, 9.0), "ANSI E": (44.0, 34.0), "ANSI D": (34.0, 22.0),
    "ANSI C": (22.0, 17.0), "ANSI B": (17.0, 11.0), "Letter": (11.0, 8.5),
}


@dataclass(frozen=True)
class Scale:
    label: str            # normalized, e.g. 1/8" = 1'-0"
    paper_in: float       # inches on paper
    real_ft: float        # feet in the building
    pt_per_ft: float      # PDF points per real foot

    def ft(self, points: float) -> float:
        return points / self.pt_per_ft

    def sf(self, area_pt2: float) -> float:
        return area_pt2 / (self.pt_per_ft ** 2)


def parse_scale(text: str) -> Scale | None:
    """First architectural scale found in `text`; None for NTS/none/unparsable."""
    if not text:
        return None
    m = _SCALE_RE.search(text)
    if not m:
        return None
    paper_raw = m.group("paper").replace(" ", "")
    try:
        paper = float(Fraction(paper_raw)) if "/" in paper_raw else float(paper_raw)
    except (ValueError, ZeroDivisionError):
        return None
    real = float(m.group("ft")) + (float(m.group("inch") or 0) / 12.0)
    if paper <= 0 or real <= 0:
        return None
    label = f'{paper_raw}" = {int(real)}\'-{int(round((real - int(real)) * 12))}"'
    return Scale(label=label, paper_in=paper, real_ft=real, pt_per_ft=paper * PT_PER_IN / real)


def is_not_to_scale(text: str) -> bool:
    return bool(_NTS_RE.search(text or ""))


def sheet_size_name(width_in: float, height_in: float, tol: float = 0.6) -> str:
    w, h = max(width_in, height_in), min(width_in, height_in)
    for name, (sw, sh) in SHEET_SIZES.items():
        if abs(w - sw) <= tol and abs(h - sh) <= tol:
            return name
    return f"{w:.1f}x{h:.1f} in"


def open_pdf(path: Path):
    import pdfplumber  # lazy — heavy import

    return pdfplumber.open(str(path))


def iter_pages(path: Path) -> Iterator[tuple[int, object]]:
    with open_pdf(path) as pdf:
        for i, page in enumerate(pdf.pages):
            yield i, page


def page_size_in(page) -> tuple[float, float]:
    return float(page.width) / PT_PER_IN, float(page.height) / PT_PER_IN


def bbox_area(b: tuple[float, float, float, float]) -> float:
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def inside(b: tuple[float, float, float, float], outer: tuple[float, float, float, float], tol: float = 1.0) -> bool:
    return b[0] >= outer[0] - tol and b[1] >= outer[1] - tol and b[2] <= outer[2] + tol and b[3] <= outer[3] + tol
