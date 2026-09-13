"""Confidentiality labels on vault notes (ADR-004 Addendum A, Phase 0).

Labels are inert metadata until a retrieval layer filters on them; they must
exist BEFORE any index is exposed cross-vault (ADR-001 §2 prerequisite).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.obsidian.frontmatter import parse as parse_frontmatter

ALLOWED_LABELS = {"public", "internal", "restricted"}
ALLOWED_TRUST_TIERS = {"brain", "vault-note", "ingested-doc"}
DEFAULT_LABEL = "internal"
DEFAULT_TRUST_TIER = "vault-note"

# Scopes where a missing/invalid label is an error, not a default.
ENFORCED_SCOPES = ("00-Brain",)


def read_labels(frontmatter: dict) -> tuple[str, str]:
    """Return (label, trust_tier) with fail-closed normalization.

    An unknown label value must never widen access, so anything outside
    ALLOWED_LABELS collapses to "restricted".
    """
    if not isinstance(frontmatter, dict):
        frontmatter = {}
    label = str(frontmatter.get("label", DEFAULT_LABEL)).strip().lower()
    if label not in ALLOWED_LABELS:
        label = "restricted"
    tier = str(frontmatter.get("trust_tier", DEFAULT_TRUST_TIER)).strip().lower()
    if tier not in ALLOWED_TRUST_TIERS:
        tier = DEFAULT_TRUST_TIER
    return label, tier


@dataclass
class LabelIssue:
    path: str  # vault-relative
    problem: str


def audit_labels(vault_root: Path, scopes: tuple[str, ...] = ENFORCED_SCOPES) -> list[LabelIssue]:
    """Report notes in enforced scopes with missing or invalid labels."""
    vault_root = Path(vault_root)
    issues: list[LabelIssue] = []
    for scope in scopes:
        base = vault_root / scope
        if not base.exists():
            continue
        for f in sorted(base.rglob("*.md")):
            rel = f.relative_to(vault_root).as_posix()
            try:
                fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
            except ValueError as e:
                issues.append(LabelIssue(rel, f"malformed frontmatter: {e}"))
                continue
            problems: list[str] = []
            if "label" not in fm:
                problems.append("missing label")
            elif str(fm["label"]).strip().lower() not in ALLOWED_LABELS:
                problems.append(f"invalid label '{fm['label']}'")
            if "trust_tier" not in fm:
                problems.append("missing trust_tier")
            elif str(fm["trust_tier"]).strip().lower() not in ALLOWED_TRUST_TIERS:
                problems.append(f"invalid trust_tier '{fm['trust_tier']}'")
            if problems:
                issues.append(LabelIssue(rel, "; ".join(problems)))
    return issues
