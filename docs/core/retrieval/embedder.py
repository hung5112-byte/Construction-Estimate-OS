"""Local in-process embeddings for the hybrid index (ADR-004 Addendum A §1).

Strictly in-process (fastembed ONNX) — no daemon, no API key, deterministic
across the fleet. Everything degrades: if fastembed or its model is
unavailable, callers fall back to BM25-only search (Step-1 behavior).
"""
from __future__ import annotations

import sqlite3
import struct
import threading
from typing import Protocol

# Ungated Apache/MIT model (EmbeddingGemma rejected — Gemma-ToU gated).
# Changing this constant forces a full index rebuild (model+dims live in meta).
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
EMBED_DIMS = 384


class Embedder(Protocol):
    model_id: str
    dims: int

    def embed_docs(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, text: str) -> list[float]: ...


class FastEmbedEmbedder:
    """fastembed-backed embedder. First use downloads the ONNX model once."""

    def __init__(self, model_id: str = EMBED_MODEL, dims: int = EMBED_DIMS):
        from fastembed import TextEmbedding  # lazy — heavy import

        self.model_id = model_id
        self.dims = dims
        self._model = TextEmbedding(model_id)

    def embed_docs(self, texts: list[str]) -> list[list[float]]:
        return [v.tolist() for v in self._model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        # query_embed applies the model's query prefix (bge asymmetric search)
        return next(iter(self._model.query_embed(text))).tolist()


_default: Embedder | None = None
_default_failed = False
_default_lock = threading.Lock()


def default_embedder() -> Embedder | None:
    """Singleton — model init is expensive; None (cached) when unavailable.
    Lock prevents two ResearchPhase worker threads double-initializing."""
    global _default, _default_failed
    with _default_lock:
        if _default is None and not _default_failed:
            try:
                _default = FastEmbedEmbedder()
            except Exception:  # noqa: BLE001 — degrade to BM25-only
                _default_failed = True
    return _default


def serialize_f32(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def load_vec_extension(conn: sqlite3.Connection) -> bool:
    """Load sqlite-vec into this connection. Every connection that touches
    vec0 tables must call this. False → callers skip the vector leg."""
    try:
        import sqlite_vec  # lazy

        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        return True
    except Exception:  # noqa: BLE001
        return False
