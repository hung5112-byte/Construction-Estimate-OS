"""Semantic instinct notes (ADR-004 §2) — atomic trigger→action lessons with
frontmatter counters, stored under `<scope-root>/instincts/`.

One YAML note = one trigger + one action + confidence (0.3–0.9) + evidence +
scope (dept|company). Confidence rises on repeat/no-correction, falls on
correction or disuse. These are judge-only semantic memory — excluded from the
doc-search index like the decision ledger.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from core.obsidian.frontmatter import parse as parse_frontmatter

CONFIDENCE_MIN = 0.3
CONFIDENCE_MAX = 0.9


def quality_score(successes: int, used: int) -> float:
    """ADR-004 §3: quality = 0.3 + 0.7·successRate (0.3 floor with no evidence)."""
    if used <= 0:
        return 0.3
    return 0.3 + 0.7 * (successes / used)


@dataclass
class Instinct:
    slug: str
    trigger: str
    action: str
    confidence: float = 0.5
    scope: str = "company"  # dept | company
    used: int = 0
    tasks: list[str] = field(default_factory=list)
    successes: int = 0
    evidence: list[str] = field(default_factory=list)
    created: date | None = None
    last_used: date | None = None
    last_reviewed: date | None = None  # last consolidation run that folded evidence
    status: str = "candidate"  # candidate | active | archived
    task_cycles_idle: int = 0
    sensitive: bool = False  # money/legal/safety → stricter promotion

    @property
    def quality(self) -> float:
        return quality_score(self.successes, self.used)

    def to_frontmatter(self) -> dict:
        return {
            "type": "instinct",
            "label": "internal",
            "trust_tier": "brain",
            "trigger": self.trigger,
            "action": self.action,
            "confidence": round(self.confidence, 3),
            "scope": self.scope,
            "status": self.status,
            "used": self.used,
            "tasks": list(self.tasks),
            "successes": self.successes,
            "sensitive": self.sensitive,
            "task_cycles_idle": self.task_cycles_idle,
            "created": self.created.isoformat() if self.created else "",
            "last_used": self.last_used.isoformat() if self.last_used else "",
            "last_reviewed": self.last_reviewed.isoformat() if self.last_reviewed else "",
        }


class InstinctStore:
    def __init__(self, vault_root: Path, scope: str = "company"):
        self.vault_root = Path(vault_root)
        self.scope = scope
        # company instincts live in 00-Brain/instincts/; dept instincts under
        # the department folder (kept simple here — company scope by default).
        self.dir = self.vault_root / "00-Brain" / "instincts"

    def save(self, inst: Instinct) -> Path:
        self.dir.mkdir(parents=True, exist_ok=True)
        fm = yaml.safe_dump(inst.to_frontmatter(), sort_keys=False, allow_unicode=True)
        body = (
            f"---\n{fm}---\n"
            f"# Instinct: {inst.slug}\n\n"
            f"**When** {inst.trigger}\n\n**Then** {inst.action}\n\n"
            f"## Evidence\n\n" + "\n".join(f"- {e}" for e in inst.evidence) + "\n"
        )
        path = self.dir / f"{inst.slug}.md"
        path.write_text(body, encoding="utf-8")
        return path

    def load(self, slug: str) -> Instinct | None:
        path = self.dir / f"{slug}.md"
        if not path.exists():
            return None
        try:
            fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        except ValueError:
            return None
        if not fm:
            return None
        evidence = re.findall(r"^-\s+(.*)$", body.split("## Evidence", 1)[-1], re.MULTILINE)
        return Instinct(
            slug=slug,
            trigger=str(fm.get("trigger", "")),
            action=str(fm.get("action", "")),
            confidence=float(fm.get("confidence", 0.5)),
            scope=str(fm.get("scope", "company")),
            used=int(fm.get("used", 0)),
            tasks=list(fm.get("tasks", []) or []),
            successes=int(fm.get("successes", 0)),
            evidence=evidence,
            created=_parse_date(fm.get("created")),
            last_used=_parse_date(fm.get("last_used")),
            last_reviewed=_parse_date(fm.get("last_reviewed")),
            status=str(fm.get("status", "candidate")),
            task_cycles_idle=int(fm.get("task_cycles_idle", 0)),
            sensitive=bool(fm.get("sensitive", False)),
        )

    def all(self) -> list[Instinct]:
        if not self.dir.exists():
            return []
        out = []
        for p in sorted(self.dir.glob("*.md")):
            inst = self.load(p.stem)
            if inst is not None:
                out.append(inst)
        return out


def _parse_date(v) -> date | None:
    if not v:
        return None
    if isinstance(v, date):
        return v
    try:
        return date.fromisoformat(str(v))
    except ValueError:
        return None
