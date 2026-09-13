"""Schedules (door, window, finish, footing, steel, equipment, fixture, panel) from a sheet.

CAD-exported PDFs draw a schedule as a frame rectangle plus horizontal and vertical rules; the
cells are not PDF table objects. We reconstruct the grid from geometry (frame → rules → cells)
and drop words into cells by position. pdfplumber's own table finder is used as a fallback.
The title is the bold text line just above the frame.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from core.estimating.pdfio import bbox_area, inside
from core.estimating.sheet_text import TextLine, Word

BBox = tuple[float, float, float, float]


@dataclass
class Schedule:
    title: str
    headers: list[str]
    rows: list[list[str]]
    bbox: BBox
    kind: str = "table"     # door | window | finish | footing | steel | equipment | fixture | panel | table
    source: str = "geometry"

    def to_markdown(self) -> str:
        out = [f"### {self.title} ({len(self.rows)} rows)", "", "| " + " | ".join(self.headers) + " |",
               "|" + "---|" * len(self.headers)]
        for r in self.rows:
            out.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
        return "\n".join(out)

    def to_dict(self) -> dict:
        return {"title": self.title, "kind": self.kind, "headers": self.headers, "rows": self.rows,
                "bbox": [round(v, 1) for v in self.bbox], "source": self.source}


_KIND_PATTERNS = [
    ("door", r"\bDOOR\b"), ("window", r"\bWINDOW\b"), ("finish", r"\bFINISH\b"), ("footing", r"\bFOOTING\b"),
    ("steel", r"\bSTEEL\b|\bFRAMING\b|\bBEAM\b|\bCOLUMN SCHEDULE\b"), ("equipment", r"\bEQUIPMENT\b|\bHVAC\b|\bMECHANICAL\b"),
    ("fixture", r"\bFIXTURE\b|\bLIGHTING\b|\bPLUMBING\b"), ("panel", r"\bPANEL\b|\bONE-LINE\b|\bGEAR\b"),
    ("hardware", r"\bHARDWARE\b"), ("partition", r"\bPARTITION\b|\bWALL TYPE\b"), ("deck", r"\bDECK\b"),
    ("fire", r"\bFIRE\b|\bSPRINKLER\b"), ("index", r"\bINDEX\b"), ("code", r"\bCODE SUMMARY\b"),
]


def classify(title: str) -> str:
    for kind, pat in _KIND_PATTERNS:
        if re.search(pat, title, re.IGNORECASE):
            return kind
    return "table"


def _frames(page, max_page_fraction: float = 0.6) -> list[BBox]:
    pw, ph = float(page.width), float(page.height)
    page_area = pw * ph
    frames: list[BBox] = []
    for r in page.rects:
        b = (float(r["x0"]), float(r["top"]), float(r["x1"]), float(r["bottom"]))
        if bbox_area(b) < 2000 or bbox_area(b) > page_area * max_page_fraction:
            continue
        if (b[2] - b[0]) < 120 or (b[3] - b[1]) < 30:
            continue
        frames.append(b)
    # drop frames nested inside another candidate frame (cells drawn as rects)
    keep = []
    for b in frames:
        if any(o != b and inside(b, o, 0.5) and bbox_area(o) > bbox_area(b) * 1.2 for o in frames):
            continue
        keep.append(b)
    return keep


def _rules(page, frame: BBox, tol: float = 2.0) -> tuple[list[float], list[float]]:
    xs: set[float] = set()
    ys: set[float] = set()
    for ln in page.lines:
        b = (float(ln["x0"]), float(ln["top"]), float(ln["x1"]), float(ln["bottom"]))
        if not inside(b, frame, tol):
            continue
        if abs(b[3] - b[1]) <= 1.0 and (b[2] - b[0]) >= (frame[2] - frame[0]) * 0.5:
            ys.add(round((b[1] + b[3]) / 2, 1))
        elif abs(b[2] - b[0]) <= 1.0 and (b[3] - b[1]) >= (frame[3] - frame[1]) * 0.5:
            xs.add(round((b[0] + b[2]) / 2, 1))
    return sorted(xs), sorted(ys)


def _grid_table(page, frame: BBox, ws: list[Word], lines: list[TextLine]) -> Schedule | None:
    xs, ys = _rules(page, frame)
    if len(ys) < 1:
        return None
    col_edges = [frame[0]] + [x for x in xs if frame[0] + 3 < x < frame[2] - 3] + [frame[2]]
    row_edges = [frame[1]] + [y for y in ys if frame[1] + 3 < y < frame[3] - 3] + [frame[3]]
    if len(col_edges) < 3:
        return None
    ncols, nrows = len(col_edges) - 1, len(row_edges) - 1
    cells: list[list[list[Word]]] = [[[] for _ in range(ncols)] for _ in range(nrows)]
    for w in ws:
        if not w.upright or not (frame[0] <= w.cx <= frame[2] and frame[1] <= w.cy <= frame[3]):
            continue
        ci = max(0, min(ncols - 1, sum(1 for e in col_edges[1:-1] if w.cx > e)))
        ri = max(0, min(nrows - 1, sum(1 for e in row_edges[1:-1] if w.cy > e)))
        cells[ri][ci].append(w)
    grid = [[" ".join(q.text for q in sorted(c, key=lambda q: (round(q.top), q.x0))).strip() for c in row] for row in cells]
    grid = [r for r in grid if any(r)]
    if len(grid) < 2:
        return None
    # title: nearest text line above the frame, left-aligned with it
    title = ""
    best = None
    for ln in lines:
        if ln.bottom <= frame[1] + 1 and frame[1] - ln.bottom < 40 and ln.x0 >= frame[0] - 5 and ln.x0 <= frame[0] + 120:
            if best is None or ln.bottom > best.bottom:
                best = ln
    if best:
        title = best.text.strip()
    headers, rows = grid[0], grid[1:]
    return Schedule(title=title or "TABLE", headers=headers, rows=rows, bbox=frame, kind=classify(title))


def extract_schedules(page, ws: list[Word], lines: list[TextLine]) -> list[Schedule]:
    out: list[Schedule] = []
    for frame in _frames(page):
        t = _grid_table(page, frame, ws, lines)
        if t:
            out.append(t)
    if not out:
        # pdfplumber fallback — line strategy, ignoring page-sized tables
        try:
            settings = {"vertical_strategy": "lines", "horizontal_strategy": "lines", "snap_tolerance": 3,
                        "intersection_tolerance": 5}
            for tbl in page.find_tables(settings):
                b = tuple(float(v) for v in tbl.bbox)
                if bbox_area(b) > float(page.width) * float(page.height) * 0.6:
                    continue
                data = [[(c or "").replace("\n", " ").strip() for c in row] for row in tbl.extract()]
                data = [r for r in data if any(r)]
                if len(data) >= 2:
                    out.append(Schedule(title="TABLE", headers=data[0], rows=data[1:], bbox=b, source="pdfplumber"))
        except Exception:  # noqa: BLE001, S110 — the fallback finder must never break extraction
            return out
    out.sort(key=lambda s: (s.bbox[1], s.bbox[0]))
    return out


def schedules_markdown(schedules: list[Schedule]) -> str:
    if not schedules:
        return ""
    return "## Schedules\n\n" + "\n\n".join(s.to_markdown() for s in schedules) + "\n"
