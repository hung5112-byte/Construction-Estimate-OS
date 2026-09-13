"""Suite-wide guards.

Tests must never hit the network: the real fastembed model (~130MB download on
first use) is disabled everywhere; hybrid tests inject a FakeEmbedder
explicitly (VaultIndexer(embedder=...) / VaultSearcher(embedder=...) take
precedence over the patched default).
"""
from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _no_default_embedder(monkeypatch):
    monkeypatch.setattr("core.retrieval.indexer.default_embedder", lambda: None)
    monkeypatch.setattr("core.retrieval.search.default_embedder", lambda: None)
