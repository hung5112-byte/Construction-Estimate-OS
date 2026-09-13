"""Tests for confidentiality-label frontmatter (ADR-004 Addendum A, Phase 0)."""
from __future__ import annotations

from pathlib import Path

from core.obsidian.labels import (
    ALLOWED_LABELS,
    ALLOWED_TRUST_TIERS,
    DEFAULT_LABEL,
    DEFAULT_TRUST_TIER,
    audit_labels,
    read_labels,
)


def test_allowed_values():
    assert ALLOWED_LABELS == {"public", "internal", "restricted"}
    assert ALLOWED_TRUST_TIERS == {"brain", "vault-note", "ingested-doc"}


def test_read_labels_defaults_when_absent():
    label, tier = read_labels({})
    assert label == DEFAULT_LABEL == "internal"
    assert tier == DEFAULT_TRUST_TIER == "vault-note"


def test_read_labels_normalizes_invalid_to_restricted():
    # Fail-closed: an unknown label must never widen access
    label, _ = read_labels({"label": "totally-open"})
    assert label == "restricted"


def test_audit_labels_flags_unlabeled_brain_note(tmp_path: Path):
    brain = tmp_path / "00-Brain"
    brain.mkdir(parents=True)
    (brain / "ok.md").write_text(
        "---\nlabel: internal\ntrust_tier: brain\n---\n# ok\n", encoding="utf-8"
    )
    (brain / "missing.md").write_text("# no frontmatter\n", encoding="utf-8")
    (brain / "bad.md").write_text(
        "---\nlabel: wide-open\ntrust_tier: brain\n---\n# bad\n", encoding="utf-8"
    )
    issues = audit_labels(tmp_path)
    paths = {i.path: i.problem for i in issues}
    assert "00-Brain/missing.md" in paths
    assert "00-Brain/bad.md" in paths
    assert "00-Brain/ok.md" not in paths
