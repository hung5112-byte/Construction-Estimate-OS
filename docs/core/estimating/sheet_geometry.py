"""Vector geometry of a plan sheet → candidate counts and measurements (never final by themselves).

- door candidates: quarter-circle arcs with an adjacent leaf line (door swing symbol)
- window candidates: pairs of short parallel lines a few points apart sitting on a wall
- walls: long thick lines / the thick exterior rectangle → linear feet by weight class
- areas: from room tags (text) — the vision reader confirms; polygons are a later step

The reader agent confirms or rejects each numbered candidate on the tiles (Set-of-Mark), so a
false positive here costs a glance, a false negative costs a question. Tune for recall.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from core.estimating.pdfio import Scale

BBox = tuple[float, float, float, float]


@dataclass
class DoorCandidate:
    x: float
    top: float
    width_ft: float | None
    bbox: BBox
    leaf_found: bool
    confidence: float


@dataclass
class WindowCandidate:
    x: float
    top: float
    width_ft: float | None
    orientation: str  # h | v
    bbox: BBox
    confidence: float


@dataclass
class WallSegment:
    x0: float
    top: float
    x1: float
    bottom: float
    linewidth: float
    length_ft: float | None


@dataclass
class GeometrySummary:
    doors: list[DoorCandidate] = field(default_factory=list)
    windows: list[WindowCandidate] = field(default_factory=list)
    walls: list[WallSegment] = field(default_factory=list)
    exterior_perimeter_ft: float | None = None
    footprint_sf: float | None = None
    n_lines: int = 0
    n_rects: int = 0
    n_curves: int = 0

    def to_dict(self) -> dict:
        return {
            "door_candidates": len(self.doors), "window_candidates": len(self.windows),
            "wall_segments": len(self.walls),
            "wall_lf_by_weight": wall_lf_by_weight(self.walls),
            "exterior_perimeter_ft": self.exterior_perimeter_ft, "footprint_sf": self.footprint_sf,
            "primitives": {"lines": self.n_lines, "rects": self.n_rects, "curves": self.n_curves},
        }


def _pts(obj) -> list[tuple[float, float]]:
    pts = obj.get("pts") or []
    out = []
    for p in pts:
        try:
            out.append((float(p[0]), float(p[1])))
        except (TypeError, IndexError):
            continue
    return out


def _dist(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def door_candidates(page, scale: Scale | None, min_r: float = 8.0, max_r: float = 200.0) -> list[DoorCandidate]:
    """Quarter arcs: open curve, near-square bbox, endpoints on two adjacent bbox corners, plus a
    leaf line of length ≈ r touching one endpoint."""
    lines = [(float(ln["x0"]), float(ln["top"]), float(ln["x1"]), float(ln["bottom"])) for ln in page.lines]
    out: list[DoorCandidate] = []
    for c in page.curves:
        pts = _pts(c)
        if len(pts) < 3:
            continue
        x0, top, x1, bottom = float(c["x0"]), float(c["top"]), float(c["x1"]), float(c["bottom"])
        w, h = x1 - x0, bottom - top
        if w < min_r or h < min_r or w > max_r or h > max_r:
            continue
        if abs(w - h) > 0.25 * max(w, h):
            continue
        if c.get("fill") and not c.get("stroke"):
            continue  # filled slivers (dash segments, arrowheads) are never door swings
        # pdfplumber already reports `pts` as (x, top) in the same top-left frame as the bbox
        p0 = (pts[0][0], pts[0][1])
        p1 = (pts[-1][0], pts[-1][1])
        if _dist(p0, p1) < 0.5 * max(w, h):
            continue  # closed / tiny chord → circle or tag
        corners = [(x0, top), (x1, top), (x0, bottom), (x1, bottom)]
        near0 = min(_dist(p0, k) for k in corners)
        near1 = min(_dist(p1, k) for k in corners)
        if near0 > 0.2 * max(w, h) or near1 > 0.2 * max(w, h):
            continue
        r = (w + h) / 2
        # leaf: a line of length ≈ r with an endpoint within tol of p0 or p1
        leaf = False
        for (lx0, lt, lx1, lb) in lines:
            L = math.hypot(lx1 - lx0, lb - lt)
            if abs(L - r) > 0.25 * r:
                continue
            for e in ((lx0, lt), (lx1, lb)):
                if _dist(e, p0) < 4 or _dist(e, p1) < 4:
                    leaf = True
                    break
            if leaf:
                break
        conf = 0.85 if leaf else 0.5
        out.append(DoorCandidate(x=(x0 + x1) / 2, top=(top + bottom) / 2, width_ft=(scale.ft(r) if scale else None),
                                 bbox=(x0, top, x1, bottom), leaf_found=leaf, confidence=conf))
    # de-duplicate arcs drawn twice (stroke + fill)
    dedup: list[DoorCandidate] = []
    for d in out:
        if any(_dist((d.x, d.top), (e.x, e.top)) < 3 for e in dedup):
            continue
        dedup.append(d)
    return dedup


def window_candidates(page, scale: Scale | None, min_len: float = 12.0, max_len: float = 220.0,
                      gap_min: float = 4.0, gap_max: float = 22.0) -> list[WindowCandidate]:
    """Two short parallel lines, a few points apart, overlapping along their length."""
    segs = []
    for ln in page.lines:
        x0, top, x1, bottom = float(ln["x0"]), float(ln["top"]), float(ln["x1"]), float(ln["bottom"])
        if abs(bottom - top) <= 1.0 and min_len <= (x1 - x0) <= max_len:
            segs.append(("h", x0, x1, (top + bottom) / 2))
        elif abs(x1 - x0) <= 1.0 and min_len <= (bottom - top) <= max_len:
            segs.append(("v", top, bottom, (x0 + x1) / 2))
    out: list[WindowCandidate] = []
    used: set[int] = set()
    for i, a in enumerate(segs):
        if i in used:
            continue
        for j in range(i + 1, len(segs)):
            b = segs[j]
            if j in used or a[0] != b[0]:
                continue
            if not (gap_min <= abs(a[3] - b[3]) <= gap_max):
                continue
            overlap = min(a[2], b[2]) - max(a[1], b[1])
            length = max(a[2] - a[1], b[2] - b[1])
            if overlap < 0.8 * length:
                continue
            used.update((i, j))
            mid = (a[3] + b[3]) / 2
            if a[0] == "h":
                bbox = (a[1], mid - gap_max / 2, a[2], mid + gap_max / 2)
                out.append(WindowCandidate(x=(a[1] + a[2]) / 2, top=mid, width_ft=(scale.ft(length) if scale else None),
                                           orientation="h", bbox=bbox, confidence=0.7))
            else:
                bbox = (mid - gap_max / 2, a[1], mid + gap_max / 2, a[2])
                out.append(WindowCandidate(x=mid, top=(a[1] + a[2]) / 2, width_ft=(scale.ft(length) if scale else None),
                                           orientation="v", bbox=bbox, confidence=0.7))
            break
    return out


def wall_segments(page, scale: Scale | None, min_len_ft: float = 8.0, min_len_pt: float = 40.0) -> list[WallSegment]:
    """Long straight stroked lines. Line width is unreliable in some PDF writers (Chrome/Skia put it
    in an ExtGState pdfminer ignores), so length is the primary filter and width is reported as-is."""
    out: list[WallSegment] = []
    for ln in page.lines:
        if ln.get("stroke") is False:
            continue
        lw = float(ln.get("linewidth") or 0)
        x0, top, x1, bottom = float(ln["x0"]), float(ln["top"]), float(ln["x1"]), float(ln["bottom"])
        L = math.hypot(x1 - x0, bottom - top)
        if L < min_len_pt or (scale and scale.ft(L) < min_len_ft):
            continue
        if ln.get("dash"):
            continue  # dashed = hidden/overhead/grid, not a wall
        out.append(WallSegment(x0, top, x1, bottom, lw, scale.ft(L) if scale else None))
    return out


def exterior_rect(page, scale: Scale | None, min_side_pt: float = 100.0):
    """Largest stroked rectangle that is not the sheet border → (perimeter_ft, area_sf, bbox)."""
    pw, ph = float(page.width), float(page.height)
    best = None
    for r in page.rects:
        if not r.get("stroke"):
            continue
        b = (float(r["x0"]), float(r["top"]), float(r["x1"]), float(r["bottom"]))
        w, h = b[2] - b[0], b[3] - b[1]
        if w < min_side_pt or h < min_side_pt:
            continue
        if w > pw * 0.9 or h > ph * 0.9:
            continue  # sheet border
        area = w * h
        if best is None or area > best[0]:
            best = (area, b)
    if not best or not scale:
        return None
    _, b = best
    w, h = b[2] - b[0], b[3] - b[1]
    return scale.ft(2 * (w + h)), scale.sf(w * h), b


def wall_lf_by_weight(walls: list[WallSegment]) -> dict[str, float]:
    buckets: dict[str, float] = {}
    for w in walls:
        if w.length_ft is None:
            continue
        orient = "h" if abs(w.bottom - w.top) <= 1.0 else ("v" if abs(w.x1 - w.x0) <= 1.0 else "d")
        key = f"lw{round(w.linewidth)}-{orient}"
        buckets[key] = round(buckets.get(key, 0.0) + w.length_ft, 1)
    return buckets


def summarize(page, scale: Scale | None) -> GeometrySummary:
    g = GeometrySummary(
        doors=door_candidates(page, scale), windows=window_candidates(page, scale), walls=wall_segments(page, scale),
        n_lines=len(page.lines), n_rects=len(page.rects), n_curves=len(page.curves),
    )
    ext = exterior_rect(page, scale)
    if ext:
        g.exterior_perimeter_ft, g.footprint_sf, _ = ext
    return g
