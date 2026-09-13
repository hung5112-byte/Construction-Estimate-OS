"""Parse YAML frontmatter trong Obsidian markdown."""
from __future__ import annotations
import re
import yaml

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)", re.DOTALL)


def parse(content: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_str)."""
    # Strip a UTF-8 BOM (would defeat the ^--- match and silently drop labels),
    # normalize CRLF → LF (Obsidian on Windows writes CRLF)
    content = content.lstrip("\ufeff").replace("\r\n", "\n")
    m = FRONTMATTER_RE.match(content)
    if not m:
        return {}, content
    fm_yaml, body = m.groups()
    try:
        data = yaml.safe_load(fm_yaml)
    except yaml.YAMLError as e:
        raise ValueError(f"Malformed YAML frontmatter: {e}") from e
    if not isinstance(data, dict):
        # A leading thematic-break block ("---\nintro\n---") parses as a YAML
        # scalar/list — that's not frontmatter; treat the whole file as body.
        return {}, content
    return data, body
