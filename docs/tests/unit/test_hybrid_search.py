"""Tests for the Step-4 hybrid upgrade: vectors + wikilink graph + RRF fusion."""
from __future__ import annotations

import math
import re
from pathlib import Path

from core.retrieval.indexer import VaultIndexer, index_db_path
from core.retrieval.search import VaultSearcher

_WORD = re.compile(r"\w+")


class FakeEmbedder:
    """Deterministic, network-free, collision-free: a fixed vocabulary gets
    dedicated orthogonal dimensions; everything else is faint shared noise.
    SYNONYMS lets tests exercise genuinely semantic (non-lexical) recall."""

    SYNONYMS = {"overheating": "thermal", "overheat": "thermal"}
    VOCAB = ["thermal", "soak", "cy80", "quasar", "telemetry", "pulsar",
             "cadence", "nightjar", "fixture", "jig"]

    def __init__(self, model_id: str = "fake-vocab-v1", dims: int = 16):
        self.model_id = model_id
        self.dims = dims

    def _vec(self, text: str) -> list[float]:
        v = [0.0] * self.dims
        noise_dim = self.dims - 1
        for t in _WORD.findall(text.lower()):
            t = self.SYNONYMS.get(t, t)
            if t in self.VOCAB:
                v[self.VOCAB.index(t) % noise_dim] += 1.0
            else:
                v[noise_dim] += 0.1
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / norm for x in v]

    def embed_docs(self, texts: list[str]) -> list[list[float]]:
        return [self._vec(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._vec(text)


def _mk_vault(root: Path) -> Path:
    brain = root / "00-Brain"
    brain.mkdir(parents=True)
    (brain / "reliability.md").write_text(
        "---\nlabel: internal\ntrust_tier: brain\n---\n"
        "# Reliability\n\n## Soak\n\nThermal soak failures spiked on the CY80 "
        "batch; thermal margin collapsed and thermal reruns are scheduled.\n",
        encoding="utf-8",
    )
    (root / "02-Tasks").mkdir()
    (root / "02-Tasks" / "quasar.md").write_text(
        "# Quasar\n\nQuasar telemetry rollout notes. See [[fixture-plan]].\n",
        encoding="utf-8",
    )
    (root / "02-Tasks" / "fixture-plan.md").write_text(
        "# Fixture Plan\n\nBed-of-nails jig procurement schedule.\n",
        encoding="utf-8",
    )
    return root


def _build(root: Path, **kw) -> VaultIndexer:
    idx = VaultIndexer(root, **kw)
    idx.build()
    return idx


def test_vector_leg_finds_semantic_match(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embedder=FakeEmbedder())
    # "overheating" appears nowhere lexically; the fake embedder maps it onto
    # "thermal" — only the vector leg can produce this hit.
    hits = VaultSearcher(vault, embedder=FakeEmbedder()).search("overheating")
    assert hits and hits[0].path == "00-Brain/reliability.md"


def test_bm25_only_when_embedding_disabled(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embed=False)
    assert not index_db_has_vectors(vault)
    hits = VaultSearcher(vault).search("thermal soak")
    assert hits and hits[0].path == "00-Brain/reliability.md"
    # semantic-only query finds nothing without vectors — and must not crash
    assert VaultSearcher(vault).search("overheating") == []


def index_db_has_vectors(vault: Path) -> bool:
    import sqlite3

    conn = sqlite3.connect(index_db_path(vault))
    try:
        return conn.execute(
            "SELECT name FROM sqlite_master WHERE name='chunks_vec'"
        ).fetchone() is not None
    finally:
        conn.close()


def test_graph_leg_surfaces_linked_note(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embed=False)
    hits = VaultSearcher(vault).search("quasar telemetry rollout", k=8)
    paths = [h.path for h in hits]
    assert "02-Tasks/quasar.md" in paths
    # fixture-plan shares no query tokens — it arrives via the wikilink graph
    assert "02-Tasks/fixture-plan.md" in paths


def test_model_change_forces_full_rebuild(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embedder=FakeEmbedder(model_id="fake-1"))
    stats = VaultIndexer(vault, embedder=FakeEmbedder(model_id="fake-2")).build()
    assert stats.files_indexed == stats.files_total  # everything re-embedded
    import sqlite3

    conn = sqlite3.connect(index_db_path(vault))
    model = conn.execute(
        "SELECT value FROM meta WHERE key='embedding_model'"
    ).fetchone()[0]
    conn.close()
    assert model == "fake-2"


def test_dims_mismatch_degrades_to_bm25(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embedder=FakeEmbedder(dims=16))
    # Query-side embedder with different dims → vec query fails → BM25 still works
    hits = VaultSearcher(vault, embedder=FakeEmbedder(dims=32)).search("thermal soak")
    assert hits and hits[0].path == "00-Brain/reliability.md"


def test_restricted_stays_hidden_in_all_legs(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    (vault / "00-Brain" / "secret.md").write_text(
        "---\nlabel: restricted\ntrust_tier: brain\n---\n"
        "# S\n\nThermal soak codename NIGHTJAR. See [[reliability]].\n",
        encoding="utf-8",
    )
    _build(vault, embedder=FakeEmbedder())
    for query in ("NIGHTJAR", "overheating NIGHTJAR", "thermal soak"):
        hits = VaultSearcher(vault, embedder=FakeEmbedder()).search(query)
        assert all(h.label != "restricted" for h in hits), query


def test_incremental_reindex_updates_vectors_and_links(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embedder=FakeEmbedder())
    target = vault / "02-Tasks" / "quasar.md"
    target.write_text(
        "# Quasar\n\nRewritten: pulsar cadence notes only. See [[reliability]].\n",
        encoding="utf-8",
    )
    stats = VaultIndexer(vault, embedder=FakeEmbedder()).build()
    assert stats.files_indexed == 1
    assert stats.vectors_total == stats.chunks_total  # no orphaned vectors
    s = VaultSearcher(vault, embedder=FakeEmbedder())
    assert all(h.path != "02-Tasks/quasar.md" for h in s.search("telemetry rollout"))
    assert any(h.path == "02-Tasks/quasar.md" for h in s.search("pulsar cadence"))


def test_rrf_scores_are_positive_and_ordered(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embedder=FakeEmbedder())
    hits = VaultSearcher(vault, embedder=FakeEmbedder()).search("thermal soak CY80")
    assert hits
    assert all(h.score > 0 for h in hits)
    assert [h.score for h in hits] == sorted((h.score for h in hits), reverse=True)


# ------------------------------------------------- review-fleet regression fixes

def test_build_survives_vec_extension_loss(tmp_path: Path, monkeypatch):
    """vec available → unavailable must NOT crash or mispair; it rebuilds
    vector-less (correct and rebuildable beats corrupt)."""
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embedder=FakeEmbedder())
    assert index_db_has_vectors(vault)

    monkeypatch.setattr("core.retrieval.indexer.load_vec_extension", lambda c: False)
    target = vault / "02-Tasks" / "quasar.md"
    target.write_text("# Quasar\n\nRewritten: pulsar cadence only.\n", encoding="utf-8")
    stats = VaultIndexer(vault, embedder=FakeEmbedder()).build()  # no flag needed
    assert stats.files_total == stats.files_indexed  # auto full rebuild
    monkeypatch.undo()

    s = VaultSearcher(vault, embedder=FakeEmbedder())
    assert s.search("thermal soak")  # BM25 intact
    # the stale-vector mispair from the review: the OLD content ("telemetry")
    # is gone from the vault — a leftover vector must not resurrect it
    assert all(h.path != "02-Tasks/quasar.md" for h in s.search("telemetry rollout"))


def test_failed_rebuild_preserves_old_index(tmp_path: Path, monkeypatch):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embed=False)

    def boom(self, conn):
        raise RuntimeError("simulated crash mid-rebuild")

    monkeypatch.setattr(VaultIndexer, "_sync", boom)
    import pytest

    with pytest.raises(RuntimeError):
        VaultIndexer(vault, embed=False).build(rebuild=True)
    monkeypatch.undo()
    # Old index intact, no temp litter
    assert VaultSearcher(vault).search("thermal soak")
    assert not list((vault / ".cache").glob("*.rebuild"))


def test_dims_change_same_model_rebuilds_cleanly(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embedder=FakeEmbedder(model_id="m", dims=16))
    stats = VaultIndexer(vault, embedder=FakeEmbedder(model_id="m", dims=32)).build()
    assert stats.files_indexed == stats.files_total  # rebuild, not a crash
    hits = VaultSearcher(vault, embedder=FakeEmbedder(model_id="m", dims=32)).search(
        "overheating"
    )
    assert hits and hits[0].path == "00-Brain/reliability.md"


def test_dead_link_becomes_edge_when_target_appears(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    (vault / "02-Tasks" / "quasar.md").write_text(
        "# Quasar\n\nQuasar telemetry rollout notes. See [[future-note]].\n",
        encoding="utf-8",
    )
    _build(vault, embed=False)
    # Target created AFTER the linking note was indexed (Obsidian dead-link flow)
    (vault / "02-Tasks" / "future-note.md").write_text(
        "# Future Note\n\nCompletely different vocabulary here.\n", encoding="utf-8"
    )
    VaultIndexer(vault, embed=False).build()  # only future-note reindexes
    hits = VaultSearcher(vault).search("quasar telemetry rollout", k=8)
    assert "02-Tasks/future-note.md" in [h.path for h in hits]


def test_deleted_link_target_is_ignored(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embed=False)
    (vault / "02-Tasks" / "fixture-plan.md").unlink()
    VaultIndexer(vault, embed=False).build()
    hits = VaultSearcher(vault).search("quasar telemetry rollout", k=8)
    assert all(h.path != "02-Tasks/fixture-plan.md" for h in hits)


def test_graph_leg_filters_restricted_before_truncation(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    (vault / "02-Tasks" / "quasar.md").write_text(
        "# Quasar\n\nQuasar telemetry rollout. See [[secret-note]] and [[fixture-plan]].\n",
        encoding="utf-8",
    )
    (vault / "00-Brain" / "secret-note.md").write_text(
        "---\nlabel: restricted\ntrust_tier: brain\n---\n# S\n\nhidden content\n",
        encoding="utf-8",
    )
    _build(vault, embed=False)
    hits = VaultSearcher(vault).search("quasar telemetry rollout", k=8)
    paths = [h.path for h in hits]
    assert "00-Brain/secret-note.md" not in paths
    assert "02-Tasks/fixture-plan.md" in paths  # restricted did not eat its slot


def test_vec_ceiling_configurable_via_bd_os_yaml(tmp_path: Path):
    vault = _mk_vault(tmp_path / "v")
    _build(vault, embedder=FakeEmbedder())
    assert VaultSearcher(vault, embedder=FakeEmbedder()).search("overheating")
    (vault / ".bd-os.yaml").write_text(
        "index:\n  vec_distance_ceiling: 0.01\n", encoding="utf-8"
    )
    assert VaultSearcher(vault, embedder=FakeEmbedder()).search("overheating") == []


def test_tool_auto_sync_never_touches_embedding_model(tmp_path: Path, monkeypatch):
    from core.tools.vault_search import VaultSearchTool

    vault = _mk_vault(tmp_path / "v")
    _build(vault, embed=False)

    def explode():
        raise AssertionError("meeting path must never init the embedding model")

    monkeypatch.setattr("core.retrieval.indexer.default_embedder", explode)
    (vault / "02-Tasks" / "fresh.md").write_text(
        "# Fresh\n\nGasket supplier shortlist for the enclosure.\n", encoding="utf-8"
    )
    result = VaultSearchTool(vault_root=vault).run("gasket supplier shortlist")
    assert result.sources  # synced + found via BM25, no model init
