"""Anti-poisoning gate for ingested documents (ADR-004 Addendum A §6).

Vendor PDFs and third-party documents are the MINJA-class injection vector:
instruction-like text inside them must never read as instructions to an agent.

Screening is done on a NORMALIZED, BOUNDARY-COLLAPSED view of the document —
NFKC + zero-width/soft-hyphen stripping + common homoglyph folding, with
newlines and table delimiters collapsed to spaces — because the attacker
controls the source document's line wrapping and cell layout (the review
fleet defeated a naive per-line screen with a single Enter press). Matched
directives cause their ORIGINAL lines to be removed and replaced with a
visible marker + short excerpt, so a human reviewing the card sees exactly
what was defused. Defense wins over fidelity on flagged lines.

A regex blocklist is inherently incomplete — this is one layer. The others:
`trust_tier: ingested-doc` on every card (ranking discount, Step 7),
`extraction_confidence` gating judge injection, and the human at Stop 1/2.
"""
from __future__ import annotations

import re
import unicodedata

DIRECTIVE_RE = re.compile(
    r"(always\s|never\s|remember\s+that|for\s+future\s+reference|from\s+now\s+on"
    r"|if\s+the\s+user\s+later|ignore\s+(all\s+)?previous|disregard\s+(all\s+)?prior"
    r"|you\s+must\s+now|new\s+instructions?\s*:"
    r"|you\s+are\s+(now|really)\s|developer\s+mode"
    r"|override\s+(your|all|the|any)\s|reveal\s+(the\s+)?(system\s+)?prompt"
    r"|do\s+not\s+(tell|inform|alert)\s+the\s+(user|owner|head)"
    r"|(?:^|\s)(system|assistant|developer)\s*:\s"
    r"|please\s+forward\s+all"
    r"|(wire|transfer|send|forward|route)\s+(the\s+|all\s+|any\s+)?"
    r"(\w+\s+){0,3}(funds?|balance|deposits?|payments?|money|invoices?|emails?|"
    r"credentials?|purchase\s+orders?)\s+to\b)",
    re.IGNORECASE,
)

# Zero-width & format characters attackers hide inside trigger words.
_STRIP_RE = re.compile("[\u200b-\u200f\u00ad\ufeff\u2060\u180e]")
# Common Cyrillic/Greek → Latin confusables (lowercase; NFKC runs first).
_HOMOGLYPHS = str.maketrans(
    "аеорсухіјѕԁһνο",
    "aeopcyxijsdhvo",
)

_MARKER = "> ⚠️ QUARANTINED (instruction-like text — data, not a directive): "
_EXCERPT_LEN = 80


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = _STRIP_RE.sub("", text)
    return text.lower().translate(_HOMOGLYPHS)


def screen_markdown(text: str) -> tuple[str, int]:
    """Remove directive-bearing lines, replace with visible markers.

    Returns (screened_text, count of quarantined matches).
    """
    lines = text.splitlines()
    # Collapsed view: every line normalized, joined by single spaces, with a
    # char-offset → line-index map so cross-line matches flag every line they
    # touch. Table pipes collapse too, so cell-split directives still match.
    collapsed_parts: list[str] = []
    line_spans: list[tuple[int, int]] = []  # (start, end) in collapsed coords
    pos = 0
    for line in lines:
        norm = _normalize(re.sub(r"\s*\|\s*", " ", line)).strip()
        start = pos
        collapsed_parts.append(norm)
        pos += len(norm) + 1  # +1 for the joining space
        line_spans.append((start, pos - 1))
    collapsed = " ".join(collapsed_parts)

    flagged_lines: dict[int, str] = {}  # line index → excerpt
    count = 0
    for m in DIRECTIVE_RE.finditer(collapsed):
        count += 1
        excerpt = collapsed[m.start(): m.start() + _EXCERPT_LEN].strip()
        for i, (s, e) in enumerate(line_spans):
            if s < m.end() and e > m.start():  # spans overlap
                flagged_lines.setdefault(i, excerpt)

    if not count:
        return text, 0
    out: list[str] = []
    for i, line in enumerate(lines):
        if i in flagged_lines:
            out.append(f'{_MARKER}[content removed: "{flagged_lines[i]}…"]')
        else:
            out.append(line)
    return "\n".join(out), count
