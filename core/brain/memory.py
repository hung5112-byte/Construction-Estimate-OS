"""Append-only decision log for 00-Brain/decisions-log.md."""
from __future__ import annotations
from pathlib import Path
import re
from core.brain.schema import DecisionEntry


class DecisionLog:
    def __init__(self, path: Path):
        self.path = Path(path)

    def append(self, entry: DecisionEntry) -> None:
        block = (
            f"\n### {entry.date.isoformat()} — {entry.slug}\n"
            f"- Owner: {entry.owner}\n"
            f"- Decision: {entry.decision}\n"
            f"- Reason: {entry.reason}\n"
        )
        if entry.task_ref:
            block += f"- Reference: {entry.task_ref}\n"
        with self.path.open("a", encoding="utf-8") as f:
            f.write(block)

    def search(self, query: str) -> list[str]:
        if not self.path.exists():
            return []
        content = self.path.read_text(encoding="utf-8")
        blocks = re.split(r"(?=^### )", content, flags=re.MULTILINE)
        return [b for b in blocks if query.lower() in b.lower() and b.startswith("###")]
