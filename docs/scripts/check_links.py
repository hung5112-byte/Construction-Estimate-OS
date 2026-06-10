"""Scan every .md in the repo/vault for broken markdown links and wikilinks.

Usage:
    python docs/scripts/check_links.py            # root = repo root (3 levels up)
    python docs/scripts/check_links.py --root <p>

Checks:
    [text](relative/path.md)  — resolved against the file's folder, then the root
    [[wikilink]] / [[path/to/note|alias]] — Obsidian-style: path from root, else
                                            unique basename match anywhere

Skips http(s)/mailto/anchors/obsidian:// targets and fenced code blocks.
Exit code 1 if any broken link is found (CI-friendly).
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

EXCLUDE_DIRS = {".git", ".venv", ".obsidian", ".pytest_cache", ".ruff_cache", "node_modules", ".cache", "__pycache__"}
MD_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
WIKILINK = re.compile(r"\[\[([^\]\|#]+)")
FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]+`")


def md_files(root: Path) -> list[Path]:
    out = []
    for p in root.rglob("*.md"):
        if not any(part in EXCLUDE_DIRS for part in p.parts):
            out.append(p)
    return out


def build_index(root: Path) -> dict[str, list[Path]]:
    """stem(lower) -> all files with that stem (any extension), for wikilink resolution."""
    idx: dict[str, list[Path]] = {}
    for p in root.rglob("*"):
        if p.is_file() and not any(part in EXCLUDE_DIRS for part in p.parts):
            idx.setdefault(p.stem.lower(), []).append(p)
    return idx


def check_md_target(target: str, file: Path, root: Path) -> bool:
    t = urllib.parse.unquote(target.split("#")[0]).strip()
    if not t or t.startswith(("http://", "https://", "mailto:", "obsidian://", "<", "data:")):
        return True
    candidates = [file.parent / t, root / t]
    if not Path(t).suffix:
        candidates += [file.parent / f"{t}.md", root / f"{t}.md"]
    return any(c.exists() for c in candidates)


def check_wikilink(target: str, file: Path, root: Path, idx: dict[str, list[Path]]) -> bool:
    # In markdown tables the alias pipe is escaped ("[[x\|alias]]") — strip the backslash.
    t = urllib.parse.unquote(target).strip().rstrip("\\").strip()
    if not t:
        return True
    if "/" in t:
        for base in (root, file.parent):
            p = base / t
            if p.exists() or p.with_suffix(".md").exists():
                return True
        # fall through to basename match (Obsidian resolves by shortest unique path)
        t = t.rsplit("/", 1)[-1]
    return t.lower() in idx or f"{t}.md".lower().rstrip(".md") in idx


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).parent.parent.parent))
    args = ap.parse_args()
    root = Path(args.root).resolve()

    idx = build_index(root)
    broken: list[tuple[Path, str, str]] = []

    for f in md_files(root):
        text = f.read_text(encoding="utf-8", errors="replace")
        text = FENCE.sub("", text)
        text = INLINE_CODE.sub("", text)
        for m in MD_LINK.finditer(text):
            if not check_md_target(m.group(1), f, root):
                broken.append((f, "md", m.group(1)))
        for m in WIKILINK.finditer(text):
            if not check_wikilink(m.group(1), f, root, idx):
                broken.append((f, "wiki", m.group(1)))

    if not broken:
        print(f"OK: no broken links across {len(md_files(root))} markdown files.")
        return
    print(f"BROKEN: {len(broken)} link(s):\n")
    for f, kind, target in broken:
        print(f"  {f.relative_to(root)}  [{kind}]  ->  {target}")
    sys.exit(1)


if __name__ == "__main__":
    main()
