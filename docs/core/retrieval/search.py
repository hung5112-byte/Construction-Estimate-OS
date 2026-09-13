"""Hybrid search over the per-vault index: BM25 + vector KNN + wikilink graph.

Deterministic fusion — reciprocal rank fusion (RRF, k=60), no LLM, no network.
Each leg degrades independently: no sqlite-vec/fastembed → BM25+graph; no
links → BM25+vector; worst case is exactly the Step-1 BM25 behavior.
Restricted-labeled notes are excluded by default (fail closed).
"""
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from core.retrieval.embedder import (
    Embedder,
    default_embedder,
    load_vec_extension,
    serialize_f32,
)
from core.retrieval.indexer import index_db_path

# Unicode-aware: FTS5's unicode61 tokenizer indexes "chiến" as one token, so the
# sanitizer must not shred non-ASCII terms (bilingual vault — Vietnamese included).
# Per-token double-quoting below is what neutralizes FTS5 operators.
_TOKEN_RE = re.compile(r"\w+", re.UNICODE)

RRF_K = 60
W_BM25, W_VECTOR, W_GRAPH = 1.0, 1.0, 0.5
OVERFETCH = 4  # candidates fetched per leg = k * OVERFETCH
FILTERED_KNN_MULTIPLIER = 4  # extra over-fetch when label/path filters apply
KNN_FETCH_CAP = 400
PPR_ALPHA = 0.85
# KNN returns the k nearest rows no matter how far — a score floor (ADR-004
# Addendum A abstention rule) keeps semantic garbage out of the fusion.
# Vectors are L2-normalized, so L2 = sqrt(2 - 2·cos); 1.0 ≈ cos 0.5, calibrated
# for bge-small (unrelated pairs cluster near cos 0.5-0.65). Override per vault
# via .bd-os.yaml → index.vec_distance_ceiling.
DEFAULT_VEC_DISTANCE_CEILING = 1.0

# Column order MUST match the ScoredChunk field order (rows unpack positionally).
_BM25_SELECT = (
    "SELECT rowid, path, anchor, breadcrumb,"
    " snippet(chunks, 0, '', '', '…', 20), bm25(chunks, 1.0, 0.6) AS rank_score,"
    " label, trust_tier"
    " FROM chunks WHERE chunks MATCH ?{extra} ORDER BY rank_score LIMIT ?"
)
_ROW_SELECT = (
    "SELECT rowid, path, anchor, breadcrumb, substr(content, 1, 200),"
    " 0.0, label, trust_tier FROM chunks WHERE rowid = ?"
)


@dataclass
class ScoredChunk:
    path: str
    anchor: str
    breadcrumb: str
    snippet: str
    score: float  # RRF fusion score — higher is better
    label: str
    trust_tier: str

    @property
    def source(self) -> str:
        return f"{self.path}#{self.anchor}" if self.anchor else self.path


class RetrieverProtocol(Protocol):
    """Seam for swapping the backend (LanceDB is the named growth path)."""

    def search(self, query: str, k: int = 8, **filters) -> list[ScoredChunk]: ...


@dataclass
class _Candidate:
    rowid: int
    path: str
    anchor: str
    breadcrumb: str
    snippet: str
    label: str
    trust_tier: str


class VaultSearcher:
    def __init__(self, vault_root: Path, embedder: Embedder | None = None):
        self.db_path = index_db_path(Path(vault_root))
        self._embedder = embedder  # None → lazy default when vectors exist
        from core.retrieval.indexer import _load_vault_config

        index_cfg = _load_vault_config(Path(vault_root)).get("index") or {}
        try:
            self._vec_ceiling = float(
                index_cfg.get("vec_distance_ceiling", DEFAULT_VEC_DISTANCE_CEILING)
            )
        except (TypeError, ValueError):
            self._vec_ceiling = DEFAULT_VEC_DISTANCE_CEILING

    # --------------------------------------------------------------- public

    def search(
        self,
        query: str,
        k: int = 8,
        include_restricted: bool = False,
        path_prefix: str | None = None,
    ) -> list[ScoredChunk]:
        tokens = _TOKEN_RE.findall(query)
        if not tokens or not self.db_path.exists():
            return []
        conn = sqlite3.connect(self.db_path)
        vec_ok = load_vec_extension(conn)
        try:
            fetch = max(k * OVERFETCH, k)
            legs: list[tuple[float, list[int]]] = []  # (weight, ranked rowids)
            pool: dict[int, _Candidate] = {}

            bm25 = self._bm25_leg(conn, tokens, fetch, include_restricted, path_prefix)
            for cand in bm25:
                pool.setdefault(cand.rowid, cand)
            legs.append((W_BM25, [c.rowid for c in bm25]))

            vector = (
                self._vector_leg(conn, query, fetch, include_restricted, path_prefix)
                if vec_ok else []
            )
            for cand in vector:
                pool.setdefault(cand.rowid, cand)
            if vector:
                legs.append((W_VECTOR, [c.rowid for c in vector]))

            graph = self._graph_leg(conn, pool, k, include_restricted, path_prefix)
            for cand in graph:
                pool.setdefault(cand.rowid, cand)
            if graph:
                legs.append((W_GRAPH, [c.rowid for c in graph]))

            fused: dict[int, float] = {}
            for weight, ranked in legs:
                for rank, rowid in enumerate(ranked):
                    fused[rowid] = fused.get(rowid, 0.0) + weight / (RRF_K + rank + 1)

            top = sorted(fused.items(), key=lambda kv: kv[1], reverse=True)[:k]
            return [
                ScoredChunk(
                    path=pool[rid].path, anchor=pool[rid].anchor,
                    breadcrumb=pool[rid].breadcrumb, snippet=pool[rid].snippet,
                    score=round(score, 5), label=pool[rid].label,
                    trust_tier=pool[rid].trust_tier,
                )
                for rid, score in top
            ]
        finally:
            conn.close()

    # ----------------------------------------------------------------- legs

    def _filters(self, include_restricted: bool, path_prefix: str | None):
        extra, params = "", []
        if not include_restricted:
            extra += " AND label != 'restricted'"
        if path_prefix:
            extra += " AND path LIKE ?"
            params.append(f"{path_prefix}%")
        return extra, params

    def _bm25_leg(
        self, conn, tokens: list[str], fetch: int,
        include_restricted: bool, path_prefix: str | None,
    ) -> list[_Candidate]:
        extra, params = self._filters(include_restricted, path_prefix)
        sql = _BM25_SELECT.format(extra=extra)
        quoted = [f'"{t}"' for t in tokens]  # quoting neutralizes FTS5 operators
        rows = conn.execute(sql, (" ".join(quoted), *params, fetch)).fetchall()
        if not rows and len(quoted) > 1:
            # AND found nothing — degrade to OR so one bad term can't blank the leg
            rows = conn.execute(sql, (" OR ".join(quoted), *params, fetch)).fetchall()
        return [_Candidate(r[0], r[1], r[2], r[3], r[4], r[6], r[7]) for r in rows]

    def _vector_leg(
        self, conn, query: str, fetch: int,
        include_restricted: bool, path_prefix: str | None,
    ) -> list[_Candidate]:
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE name = 'chunks_vec'"
        ).fetchone()
        if row is None:
            return []
        embedder = self._embedder or default_embedder()
        if embedder is None:
            return []
        # KNN truncates BEFORE our label/path filters can run, so a
        # restricted-dense neighborhood would starve the leg — over-fetch
        # when filters are active.
        knn_fetch = fetch
        if not include_restricted or path_prefix:
            knn_fetch = min(fetch * FILTERED_KNN_MULTIPLIER, KNN_FETCH_CAP)
        try:
            qvec = serialize_f32(embedder.embed_query(query))
            knn = conn.execute(
                "SELECT rowid, distance FROM chunks_vec"
                " WHERE embedding MATCH ? AND k = ? ORDER BY distance",
                (qvec, knn_fetch),
            ).fetchall()
        except sqlite3.Error:
            return []  # dims mismatch / stale table — degrade, never fail search
        out: list[_Candidate] = []
        for rid, distance in knn:
            if distance > self._vec_ceiling:
                break  # ordered by distance — everything after is farther
            cand = self._fetch_row(conn, rid)
            if cand is None:
                continue
            if not include_restricted and cand.label == "restricted":
                continue
            if path_prefix and not cand.path.startswith(path_prefix):
                continue
            out.append(cand)
            if len(out) >= fetch:
                break
        return out

    def _graph_leg(
        self, conn, seed_pool: dict[int, _Candidate], k: int,
        include_restricted: bool, path_prefix: str | None,
    ) -> list[_Candidate]:
        """Personalized PageRank over the wikilink graph, seeded by the other
        legs' hit notes — surfaces linked-but-differently-worded notes.
        Pure-Python power iteration: deterministic, no scipy/networkx, and a
        417-note vault converges in microseconds."""
        if not seed_pool:
            return []
        edges = conn.execute("SELECT src, target_stem FROM links").fetchall()
        if not edges:
            return []
        # Resolve raw stems against the CURRENT files table — a note created
        # after its [[link]] was written becomes an edge with no re-index.
        labels = dict(conn.execute("SELECT path, label FROM files").fetchall())
        stem_to_path: dict[str, str] = {}
        for p in sorted(labels, reverse=True):  # alphabetically-first path wins
            stem_to_path[Path(p).stem.lower()] = p
        adj: dict[str, set[str]] = {}
        for src, stem in edges:  # undirected: backlinks count as much as links
            dst = stem_to_path.get(stem)
            if dst is None or dst == src or src not in labels:
                continue
            adj.setdefault(src, set()).add(dst)
            adj.setdefault(dst, set()).add(src)
        seeds = {c.path for c in seed_pool.values() if c.path in adj}
        if not seeds:
            return []
        ppr = _personalized_pagerank(adj, seeds, alpha=PPR_ALPHA)
        # Filter BEFORE truncating to k — a restricted-heavy neighborhood must
        # not consume the leg's slots.
        ranked_paths = [
            p for p, _ in sorted(ppr.items(), key=lambda kv: (-kv[1], kv[0]))
            if p not in seeds  # seeds already rank via their own legs
            and (include_restricted or labels.get(p) != "restricted")
            and (not path_prefix or p.startswith(path_prefix))
        ][:k]
        out: list[_Candidate] = []
        for path in ranked_paths:
            extra, params = self._filters(include_restricted, path_prefix)
            row = conn.execute(
                f"SELECT rowid FROM chunks WHERE path = ?{extra}"
                " ORDER BY rowid LIMIT 1",
                (path, *params),
            ).fetchone()
            if row:
                cand = self._fetch_row(conn, row[0])
                if cand:
                    out.append(cand)
        return out

    def _fetch_row(self, conn, rowid: int) -> _Candidate | None:
        r = conn.execute(_ROW_SELECT, (rowid,)).fetchone()
        if r is None:
            return None
        return _Candidate(r[0], r[1], r[2], r[3], r[4], r[6], r[7])


def _personalized_pagerank(
    adj: dict[str, set[str]],
    seeds: set[str],
    alpha: float = PPR_ALPHA,
    iterations: int = 30,
) -> dict[str, float]:
    teleport = {n: (1.0 / len(seeds) if n in seeds else 0.0) for n in adj}
    score = dict(teleport)
    for _ in range(iterations):
        nxt = {n: (1.0 - alpha) * teleport[n] for n in adj}
        for node, s in score.items():
            neighbors = adj[node]
            if neighbors:
                share = alpha * s / len(neighbors)
                for m in neighbors:
                    nxt[m] += share
            else:  # dangling node keeps its mass
                nxt[node] += alpha * s
        score = nxt
    return score
