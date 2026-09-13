"""Text layer of a sheet: words with position and rotation, text lines, room tags, notes, dimensions.

Everything here is deterministic. The output feeds the reader agents as a *shadow card* (markdown)
and the geometry module (room tags anchor areas; dimension strings cross-check the scale).
Drawing text is untrusted input: it is data for the readers, never instructions.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from core.estimating.pdfio import Scale

_ROOM_RE = re.compile(r"^(?P<num>\d{3}[A-Z]?)\s+(?P<name>[A-Z][A-Z0-9 /\-&.'()]{1,40})$")
_AREA_RE = re.compile(r"^(?P<sf>[\d,]{1,9})\s*SF$", re.IGNORECASE)
_DIM_RE = re.compile(r"(?P<ft>\d{1,4})'\s*-\s*(?P<inch>\d{1,2})(?:\s*(?P<frac>\d/\d))?\"")
_NOTES_TITLE_RE = re.compile(
    r"^(?:[A-Z][A-Z &/\-]{2,40})?(GENERAL NOTES|NOTES|KEYNOTES|KEY NOTES|LEGEND|ABBREVIATIONS|SYMBOLS)(?:\s*\(.*\))?$"
)
_NUMBERED_RE = re.compile(r"^(\d{1,3})[.)]\s+(.+)$")


@dataclass
class Word:
    text: str
    x0: float
    top: float
    x1: float
    bottom: float
    upright: bool = True
    size: float = 0.0

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.top + self.bottom) / 2


@dataclass
class TextLine:
    text: str
    x0: float
    top: float
    x1: float
    bottom: float
    size: float
    words: list[Word] = field(default_factory=list)


@dataclass
class RoomTag:
    number: str
    name: str
    area_sf: float | None
    x: float
    top: float


@dataclass
class DimensionString:
    text: str
    feet: float
    x: float
    top: float
    upright: bool


def words(page) -> list[Word]:
    out: list[Word] = []
    for w in page.extract_words(keep_blank_chars=False, use_text_flow=False, extra_attrs=["upright", "size"]):
        out.append(Word(
            text=str(w["text"]), x0=float(w["x0"]), top=float(w["top"]), x1=float(w["x1"]),
            bottom=float(w["bottom"]), upright=bool(w.get("upright", True)), size=float(w.get("size", 0.0)),
        ))
    return out


def text_lines(ws: list[Word], y_tol: float = 3.0, gap_factor: float = 1.6) -> list[TextLine]:
    """Group upright words into lines by baseline, then split lines at large horizontal gaps
    (two columns of a schedule printed on one baseline must not merge)."""
    up = sorted((w for w in ws if w.upright), key=lambda w: (round(w.top / y_tol), w.x0))
    lines: list[TextLine] = []
    current: list[Word] = []

    def flush(group: list[Word]) -> None:
        if not group:
            return
        # split on gaps larger than gap_factor × median char width
        widths = [max(1.0, (w.x1 - w.x0) / max(1, len(w.text))) for w in group]
        med = sorted(widths)[len(widths) // 2]
        chunk: list[Word] = [group[0]]
        for prev, w in zip(group, group[1:]):
            if w.x0 - prev.x1 > gap_factor * med * 3:
                _emit(chunk)
                chunk = [w]
            else:
                chunk.append(w)
        _emit(chunk)

    def _emit(chunk: list[Word]) -> None:
        lines.append(TextLine(
            text=" ".join(w.text for w in chunk), x0=min(w.x0 for w in chunk), top=min(w.top for w in chunk),
            x1=max(w.x1 for w in chunk), bottom=max(w.bottom for w in chunk),
            size=max(w.size for w in chunk), words=list(chunk),
        ))

    for w in up:
        if current and abs(w.top - current[-1].top) > y_tol:
            flush(sorted(current, key=lambda q: q.x0))
            current = []
        current.append(w)
    flush(sorted(current, key=lambda q: q.x0))
    lines.sort(key=lambda ln: (ln.top, ln.x0))
    return lines


_ROOM_NUM_RE = re.compile(r"^\d{3}[A-Z]?$")
_NAME_WORD_RE = re.compile(r"^(?:[A-Z][A-Z0-9/&.'()\-]*|[/&\-])$")
_AREA_NUM_RE = re.compile(r"^[\d,]{1,9}$")


def room_tags(ws: list[Word], max_gap_pt: float = 40.0) -> list[RoomTag]:
    """`NNN NAME` from words on one baseline, with an optional `N,NNN SF` pair just below it.

    Works from words, not lines, because door/window tags and neighbouring rooms often share a
    baseline with a room tag on real plans (the fixture reproduces that collision on purpose)."""
    up = [w for w in ws if w.upright]
    tags: list[RoomTag] = []
    for w in up:
        if not _ROOM_NUM_RE.match(w.text):
            continue
        h = max(4.0, w.bottom - w.top)
        same = sorted((q for q in up if q is not w and abs(q.top - w.top) <= h * 0.5 and q.x0 > w.x1 - 1), key=lambda q: q.x0)
        name_words: list[Word] = []
        last_x1 = w.x1
        for q in same:
            if q.x0 - last_x1 > h * 1.2:
                break
            if not _NAME_WORD_RE.match(q.text) or q.text == "SF":
                break
            name_words.append(q)
            last_x1 = q.x1
        if not name_words:
            continue
        name = " ".join(q.text for q in name_words)
        cx = (w.x0 + name_words[-1].x1) / 2
        area = None
        for q in up:
            if q.text != "SF" or not (0 < q.top - w.bottom <= max_gap_pt):
                continue
            # the number is the word immediately left of `SF` on the same baseline
            left = [z for z in up if abs(z.top - q.top) <= h * 0.5 and 0 <= q.x0 - z.x1 <= h * 1.2 and _AREA_NUM_RE.match(z.text)]
            if not left:
                continue
            z = max(left, key=lambda z: z.x1)
            pair_cx = (z.x0 + q.x1) / 2
            if abs(pair_cx - cx) <= 60:
                area = float(z.text.replace(",", ""))
                break
        tags.append(RoomTag(number=w.text, name=name, area_sf=area, x=cx, top=w.top))
    # a door/window tag can look like a room number; keep only tags with a real name of ≥3 letters
    return [t for t in tags if len(re.sub(r"[^A-Z]", "", t.name)) >= 3]


def dimension_strings(ws: list[Word]) -> list[DimensionString]:
    out: list[DimensionString] = []
    for w in ws:
        for m in _DIM_RE.finditer(w.text):
            feet = float(m.group("ft")) + float(m.group("inch")) / 12.0
            if m.group("frac"):
                n, d = m.group("frac").split("/")
                feet += float(n) / float(d) / 12.0
            out.append(DimensionString(text=m.group(0), feet=feet, x=w.cx, top=w.top, upright=w.upright))
    return out


def notes_blocks(lines: list[TextLine], max_items: int = 60) -> dict[str, list[str]]:
    """Titled blocks of numbered lines (GENERAL NOTES, KEYNOTES, LEGEND, ...)."""
    blocks: dict[str, list[str]] = {}
    i = 0
    while i < len(lines):
        title = lines[i].text.strip()
        if _NOTES_TITLE_RE.match(title) and lines[i].size >= 14:
            items: list[str] = []
            col_x = lines[i].x0
            j = i + 1
            last_bottom = lines[i].bottom
            while j < len(lines) and len(items) < max_items:
                ln = lines[j]
                if abs(ln.x0 - col_x) > 250:
                    j += 1          # a line from another column of the sheet (the plan, a table) — skip it
                    continue
                if ln.top - last_bottom > 80:
                    break
                if _NOTES_TITLE_RE.match(ln.text.strip()) and ln.size >= 14:
                    break
                nm = _NUMBERED_RE.match(ln.text.strip())
                if nm:
                    items.append(nm.group(2).strip())
                elif items and ln.size <= lines[i].size:
                    items[-1] = items[-1] + " " + ln.text.strip()
                last_bottom = ln.bottom
                j += 1
            if items:
                blocks[title] = items
                i = j
                continue
        i += 1
    return blocks


def title_block_text(lines: list[TextLine], page_width: float, page_height: float) -> str:
    """Text inside the bottom-right 30% × 25% of the sheet — where title blocks live."""
    x_min, y_min = page_width * 0.70, page_height * 0.75
    return "\n".join(ln.text for ln in lines if ln.x0 >= x_min and ln.top >= y_min)


def shadow_card(sheet_id: str, title: str, scale: Scale | None, lines: list[TextLine], tags: list[RoomTag],
                dims: list[DimensionString], notes: dict[str, list[str]], tables_md: str = "") -> str:
    parts = [f"# {sheet_id} — {title}", ""]
    parts.append(f"- Scale: {scale.label if scale else 'none / not to scale'}")
    parts.append(f"- Text lines: {len(lines)} · room tags: {len(tags)} · dimension strings: {len(dims)}")
    parts.append("")
    if tags:
        parts.append("## Room tags")
        parts.append("| Room | Name | Area (SF) |")
        parts.append("|---|---|---|")
        for t in tags:
            parts.append(f"| {t.number} | {t.name} | {int(t.area_sf) if t.area_sf else ''} |")
        parts.append("")
    for name, items in notes.items():
        parts.append(f"## {name}")
        for k, it in enumerate(items, 1):
            parts.append(f"{k}. {it}")
        parts.append("")
    if dims:
        parts.append("## Dimension strings (feet)")
        parts.append(", ".join(f"{d.text}" for d in dims[:60]))
        parts.append("")
    if tables_md:
        parts.append(tables_md)
    return "\n".join(parts)
