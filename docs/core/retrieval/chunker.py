"""Heading-aware markdown chunking for the vault index.

Each chunk carries a breadcrumb ("file.md > H1 > H2") so a BM25 hit on a
heading term still lands, and an anchor usable in `path#heading` citations.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from core.obsidian.frontmatter import parse as parse_frontmatter

# ~800 tokens at ~4 chars/token; sections longer than this get split on
# paragraph boundaries so no chunk blows past the injection bounds downstream.
MAX_CHUNK_CHARS = 3200

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")


@dataclass
class Chunk:
    path: str  # vault-relative posix path
    anchor: str  # innermost heading text ("" for preamble / heading-less docs)
    breadcrumb: str  # "file.md > H1 > H2"
    content: str
    seq: int


def chunk_markdown(text: str, rel_path: str) -> list[Chunk]:
    try:
        _, body = parse_frontmatter(text)
    except ValueError:
        body = text  # malformed frontmatter → index the raw text rather than drop the note

    filename = rel_path.rsplit("/", 1)[-1]
    sections: list[tuple[list[str], str]] = []  # (heading stack titles, section text)
    stack: list[tuple[int, str]] = []  # (level, title)
    current: list[str] = []
    open_fence: str | None = None  # the marker that opened the current fence

    def flush() -> None:
        section = "\n".join(current).strip()
        if section:
            sections.append(([t for _, t in stack], section))
        current.clear()

    for line in body.splitlines():
        fence = _FENCE_RE.match(line.strip())
        if fence:
            marker = fence.group(1)
            if open_fence is None:
                open_fence = marker
            elif marker[0] == open_fence[0] and len(marker) >= len(open_fence):
                # CommonMark: only a fence of the SAME char, at least as long,
                # closes — so ``` inside a ~~~ block stays literal text.
                open_fence = None
            current.append(line)
            continue
        m = None if open_fence else _HEADING_RE.match(line)
        if m:
            flush()
            level = len(m.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, m.group(2).strip()))
        else:
            current.append(line)
    flush()

    if not sections and body.strip():
        sections = [([], body.strip())]

    chunks: list[Chunk] = []
    for titles, section in sections:
        anchor = titles[-1] if titles else ""
        breadcrumb = " > ".join([filename, *titles])
        for piece in _split_long(section):
            chunks.append(Chunk(rel_path, anchor, breadcrumb, piece, len(chunks)))
    return chunks


def _split_long(section: str) -> list[str]:
    if len(section) <= MAX_CHUNK_CHARS:
        return [section]
    pieces: list[str] = []
    buf = ""
    for para in section.split("\n\n"):
        if len(para) > MAX_CHUNK_CHARS:  # oversized block (e.g. a big table)
            if buf:
                pieces.append(buf.strip())
                buf = ""
            pieces.extend(_split_block(para))
            continue
        if buf and len(buf) + len(para) + 2 > MAX_CHUNK_CHARS:
            pieces.append(buf.strip())
            buf = para
        else:
            buf = f"{buf}\n\n{para}" if buf else para
    if buf.strip():
        pieces.append(buf.strip())
    return pieces


def _split_block(block: str) -> list[str]:
    """Split an oversized single block on LINE boundaries first — a markdown
    table must never be cut mid-row (part numbers straddling a chunk boundary
    become unsearchable). Only a single monster line gets hard-split."""
    pieces: list[str] = []
    buf = ""
    for line in block.splitlines():
        while len(line) > MAX_CHUNK_CHARS:  # one pathological line
            if buf:
                pieces.append(buf)
                buf = ""
            pieces.append(line[:MAX_CHUNK_CHARS])
            line = line[MAX_CHUNK_CHARS:]
        if buf and len(buf) + len(line) + 1 > MAX_CHUNK_CHARS:
            pieces.append(buf)
            buf = line
        else:
            buf = f"{buf}\n{line}" if buf else line
    if buf.strip():
        pieces.append(buf)
    return pieces
