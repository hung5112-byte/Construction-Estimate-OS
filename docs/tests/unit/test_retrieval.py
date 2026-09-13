"""Tests for the per-vault retrieval index (ADR-004 Addendum A, Step 1: FTS5 only)."""
from __future__ import annotations

from pathlib import Path

import pytest

from core.retrieval.chunker import chunk_markdown
from core.retrieval.indexer import VaultIndexer, index_db_path
from core.retrieval.search import VaultSearcher


# ------------------------------------------------------------------ fixtures

def _make_vault(root: Path) -> Path:
    """Minimal vault with Brain notes, a task note, and noise dirs to exclude."""
    brain = root / "00-Brain"
    brain.mkdir(parents=True)
    (brain / "products.md").write_text(
        "---\ntype: brain\nsection: products\nlabel: internal\ntrust_tier: brain\n---\n"
        "# Products\n\n## Lineup\n\n"
        "| CY80 | Field controller | $1_200 | 42 | active |\n\n"
        "## Warranty\n\nThe CY80 field controller carries a two-year limited warranty.\n",
        encoding="utf-8",
    )
    (brain / "secret.md").write_text(
        "---\ntype: brain\nlabel: restricted\ntrust_tier: brain\n---\n"
        "# Secret\n\nConfidential acquisition target codename BLUEBIRD.\n",
        encoding="utf-8",
    )
    tasks = root / "02-Tasks" / "2026-01-01-rma-sop"
    tasks.mkdir(parents=True)
    (tasks / "07-decision-report.md").write_text(
        "# Decision Report\n\n## Verdict\n\n"
        "Approved a 10-business-day RMA turnaround for repair intake.\n",
        encoding="utf-8",
    )
    # Noise that must NOT be indexed
    (root / ".obsidian").mkdir()
    (root / ".obsidian" / "workspace.md").write_text("noise", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "engine-note.md").write_text(
        "engine internals mention RMA too", encoding="utf-8"
    )
    return root


@pytest.fixture()
def vault(tmp_path: Path) -> Path:
    return _make_vault(tmp_path / "vault")


@pytest.fixture()
def indexed_vault(vault: Path) -> Path:
    VaultIndexer(vault).build()
    return vault


# ------------------------------------------------------------------ chunker

def test_chunker_breadcrumbs_and_anchors():
    body = (
        "---\ntype: brain\n---\n"
        "# Products\n\nIntro line.\n\n## Warranty\n\nTwo-year limited warranty.\n"
    )
    chunks = chunk_markdown(body, "00-Brain/products.md")
    breadcrumbs = [c.breadcrumb for c in chunks]
    assert any("products.md > Products > Warranty" in b for b in breadcrumbs)
    warranty = next(c for c in chunks if c.anchor == "Warranty")
    assert "Two-year limited warranty" in warranty.content
    # Frontmatter must not leak into any chunk
    assert all("type: brain" not in c.content for c in chunks)


def test_chunker_splits_long_sections():
    para = "Reliability data point about thermal soak testing. " * 40
    body = "# Doc\n\n## Big\n\n" + "\n\n".join([para] * 6)
    chunks = chunk_markdown(body, "note.md")
    big = [c for c in chunks if c.anchor == "Big"]
    assert len(big) > 1  # split, not one giant chunk
    assert all(len(c.content) <= 6000 for c in big)


def test_chunker_no_headings_falls_back_to_whole_doc():
    chunks = chunk_markdown("Just a paragraph with no headings.", "plain.md")
    assert len(chunks) == 1
    assert chunks[0].anchor == ""


# ------------------------------------------------------------------ indexer

def test_build_indexes_vault_notes_only(indexed_vault: Path):
    s = VaultSearcher(indexed_vault)
    hits = s.search("RMA turnaround")
    assert hits, "expected a hit for RMA turnaround"
    assert all(not h.path.startswith("docs/") for h in hits)
    assert all(".obsidian" not in h.path for h in hits)


def test_incremental_reindex_only_changed_file(indexed_vault: Path):
    idx = VaultIndexer(indexed_vault)
    stats1 = idx.build()
    assert stats1.files_indexed == 0  # nothing changed since fixture build
    target = indexed_vault / "00-Brain" / "products.md"
    target.write_text(
        target.read_text(encoding="utf-8") + "\n## Returns\n\nRefurbished units policy.\n",
        encoding="utf-8",
    )
    stats2 = idx.build()
    assert stats2.files_indexed == 1
    hits = VaultSearcher(indexed_vault).search("refurbished units policy")
    assert hits and hits[0].path == "00-Brain/products.md"


def test_deleted_file_purged_from_index(indexed_vault: Path):
    (indexed_vault / "02-Tasks" / "2026-01-01-rma-sop" / "07-decision-report.md").unlink()
    VaultIndexer(indexed_vault).build()
    assert VaultSearcher(indexed_vault).search("RMA turnaround") == []


def test_rebuild_from_scratch(indexed_vault: Path):
    stats = VaultIndexer(indexed_vault).build(rebuild=True)
    assert stats.files_indexed >= 3
    assert VaultSearcher(indexed_vault).search("warranty")


# ------------------------------------------------------------------ search

def test_search_returns_snippet_and_anchor(indexed_vault: Path):
    hits = VaultSearcher(indexed_vault).search("two-year warranty")
    assert hits[0].path == "00-Brain/products.md"
    assert hits[0].anchor == "Warranty"
    assert "warranty" in hits[0].snippet.lower()


def test_search_excludes_restricted_by_default(indexed_vault: Path):
    hits = VaultSearcher(indexed_vault).search("BLUEBIRD codename")
    assert hits == []
    hits = VaultSearcher(indexed_vault).search("BLUEBIRD codename", include_restricted=True)
    assert hits and hits[0].label == "restricted"


def test_search_sanitizes_fts_operators(indexed_vault: Path):
    # Quotes/parens/stars are FTS5 syntax — must not raise
    for q in ['"warranty (CY80)*"', "warranty AND OR NOT", "c++ -x --y", "  "]:
        VaultSearcher(indexed_vault).search(q)


def test_search_or_fallback_when_and_finds_nothing(indexed_vault: Path):
    # 'warranty' exists, 'zephyrblaster' doesn't → AND fails, OR fallback still hits
    hits = VaultSearcher(indexed_vault).search("warranty zephyrblaster")
    assert hits and hits[0].anchor == "Warranty"


def test_search_no_match_returns_empty(indexed_vault: Path):
    assert VaultSearcher(indexed_vault).search("xylophone quasar nonsense") == []


def test_index_db_lives_in_vault_cache(indexed_vault: Path):
    assert index_db_path(indexed_vault) == indexed_vault / ".cache" / "index.db"
    assert index_db_path(indexed_vault).exists()


# ------------------------------------------------- review-fleet regression fixes

def test_malformed_frontmatter_fails_closed_to_restricted(vault: Path):
    """A restricted note whose YAML breaks must NOT downgrade to searchable."""
    (vault / "00-Brain" / "broken.md").write_text(
        "---\nlabel: restricted\nnotes: [unclosed\n---\n# Broken\n\nCodename FIREFLY here.\n",
        encoding="utf-8",
    )
    VaultIndexer(vault).build()
    assert VaultSearcher(vault).search("FIREFLY codename") == []
    hits = VaultSearcher(vault).search("FIREFLY codename", include_restricted=True)
    assert hits and hits[0].label == "restricted"


def test_unlabeled_note_in_enforced_scope_is_restricted(vault: Path):
    (vault / "00-Brain" / "unlabeled.md").write_text(
        "# No frontmatter\n\nSensitive salary bands table.\n", encoding="utf-8"
    )
    VaultIndexer(vault).build()
    assert VaultSearcher(vault).search("salary bands") == []
    # Outside the enforced scope, unlabeled notes keep the internal default
    assert VaultSearcher(vault).search("RMA turnaround")


def test_non_dict_frontmatter_does_not_crash_build(vault: Path):
    # A thematic-break intro parses as a YAML scalar — must index, not crash
    (vault / "02-Tasks" / "intro.md").write_text(
        "---\nJust an intro separated by thematic breaks\n---\nBody about flux capacitors.\n",
        encoding="utf-8",
    )
    (vault / "02-Tasks" / "list-fm.md").write_text(
        "---\n- a\n- b\n---\nBody about warp coils.\n", encoding="utf-8"
    )
    stats = VaultIndexer(vault).build()
    assert stats.files_indexed >= 2
    assert VaultSearcher(vault).search("flux capacitors")
    assert VaultSearcher(vault).search("warp coils")


def test_bom_prefixed_frontmatter_labels_respected(vault: Path):
    (vault / "00-Brain" / "bom.md").write_text(
        "﻿---\nlabel: restricted\ntrust_tier: brain\n---\n# BOM\n\nCodename KESTREL.\n",
        encoding="utf-8",
    )
    VaultIndexer(vault).build()
    assert VaultSearcher(vault).search("KESTREL codename") == []


def test_unicode_query_hits_vietnamese_note(vault: Path):
    (vault / "02-Tasks" / "vi.md").write_text(
        "# Kế hoạch\n\n## Chiến lược\n\nChiến lược sản phẩm năm 2026 cho CY80.\n",
        encoding="utf-8",
    )
    VaultIndexer(vault).build()
    hits = VaultSearcher(vault).search("chiến lược sản phẩm")
    assert hits and hits[0].path == "02-Tasks/vi.md"


def test_fence_of_other_type_stays_closed():
    body = (
        "# Doc\n\n~~~\ninside tilde fence\n```\nstill inside — not a toggle\n"
        "## not a heading\n~~~\n\n## Real Heading\n\nreal content\n"
    )
    chunks = chunk_markdown(body, "note.md")
    anchors = {c.anchor for c in chunks}
    assert "Real Heading" in anchors
    assert "not a heading" not in anchors


def test_same_mtime_different_size_still_reindexed(indexed_vault: Path):
    import os

    target = indexed_vault / "00-Brain" / "products.md"
    st = target.stat()
    target.write_text(
        target.read_text(encoding="utf-8") + "\n## Firmware\n\nBootloader v2 rollout notes.\n",
        encoding="utf-8",
    )
    os.utime(target, (st.st_atime, st.st_mtime))  # force identical mtime
    stats = VaultIndexer(indexed_vault).build()
    assert stats.files_indexed == 1
    assert VaultSearcher(indexed_vault).search("bootloader rollout")


def test_schema_version_bump_forces_rebuild(indexed_vault: Path):
    import sqlite3

    from core.retrieval.indexer import index_db_path

    conn = sqlite3.connect(index_db_path(indexed_vault))
    conn.execute("UPDATE meta SET value = '0' WHERE key = 'schema_version'")
    conn.commit()
    conn.close()
    stats = VaultIndexer(indexed_vault).build()
    assert stats.files_indexed == stats.files_total  # full rebuild happened
    assert VaultSearcher(indexed_vault).search("warranty")


def test_exclude_top_configurable_via_bd_os_yaml(tmp_path: Path):
    root = tmp_path / "vault"
    (root / "00-Brain").mkdir(parents=True)
    (root / "00-Brain" / "a.md").write_text(
        "---\nlabel: internal\ntrust_tier: brain\n---\n# A\n\nalpha content\n",
        encoding="utf-8",
    )
    (root / "engine-src").mkdir()
    (root / "engine-src" / "b.md").write_text("# B\n\nbravo engine internals\n", encoding="utf-8")
    (root / ".bd-os.yaml").write_text("index:\n  exclude_top: [engine-src]\n", encoding="utf-8")
    VaultIndexer(root).build()
    assert VaultSearcher(root).search("alpha content")
    assert VaultSearcher(root).search("bravo engine internals") == []
