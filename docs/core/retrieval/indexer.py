"""Per-vault hybrid index — a rebuildable cache, never a source of truth (RULE 3).

One `index.db` per vault under `<vault>/.cache/` (gitignored, never synced,
never home-level). Incremental by (mtime, size) fast path + sha256; a schema
version bump or `build(rebuild=True)` forces a full rebuild, and deleting the
file returns the system to pre-index behavior.

Fail-closed labeling: a note whose frontmatter cannot be parsed, or a note in
an enforced scope (00-Brain) with no explicit label, is indexed as
`restricted` — unreadable labels must never widen access.

Three retrieval legs live here (Step 4): FTS5/BM25, sqlite-vec KNN over local
fastembed embeddings, and a wikilink graph (links table). The embedding model
+ dims are recorded in meta — changing the model forces a full rebuild. Both
vector deps degrade: without sqlite-vec or fastembed the index is BM25-only.
"""
from __future__ import annotations

import hashlib
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml

from core.obsidian.frontmatter import parse as parse_frontmatter
from core.obsidian.labels import ENFORCED_SCOPES, read_labels
from core.retrieval.chunker import chunk_markdown
from core.retrieval.embedder import (
    EMBED_MODEL,
    Embedder,
    default_embedder,
    load_vec_extension,
    serialize_f32,
)

SCHEMA_VERSION = 5  # v5: link stems keep binary extensions ([[spec.docx]] → card)

# [[wikilink]] / [[wikilink#heading]] / [[wikilink|alias]] — target = group(1)
_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")

# Directory names skipped anywhere in the tree.
EXCLUDE_DIR_NAMES = {
    ".git", ".obsidian", ".venv", ".cache", ".tools", ".claude", ".github",
    ".pytest_cache", ".ruff_cache", "__pycache__", "node_modules", ".smart-env",
}
# Top-level dirs that are engine/tooling, not business notes, in the default
# deployment layout. Vaults with different layouts extend these via .bd-os.yaml:
#   index:
#     exclude_top: [my-engine-dir]
#     exclude_dirs: [drafts]
EXCLUDE_TOP_LEVEL = {"docs", "scripts", "tools", "Claude Token Dashboard"}
# Episodic memory is judge-only (ADR-004 §5): the decision ledger must reach
# the Synthesizer via the bounded Step-3 injection, never via doc search where
# every debater would see it.
EXCLUDE_FILES = {"00-Brain/decision-ledger.md"}
# Per-task copies of ledger-derived content (same judge-only rule).
EXCLUDE_FILENAMES = {"03c-memory-context.md"}
# Semantic instinct notes are judge-only memory too (ADR-004 §2) — never
# surfaced through doc search; the consolidation writer owns them.
EXCLUDE_DIR_SEGMENTS = {"instincts"}


def index_db_path(vault_root: Path) -> Path:
    return Path(vault_root) / ".cache" / "index.db"


def _load_vault_config(vault_root: Path) -> dict:
    cfg = Path(vault_root) / ".bd-os.yaml"
    if cfg.exists():
        try:
            return yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            pass
    return {}


def _vault_group_id(vault_root: Path) -> str:
    data = _load_vault_config(vault_root)
    if data.get("group_id"):
        return str(data["group_id"])
    return Path(vault_root).resolve().name.lower().replace(" ", "-")


@dataclass
class IndexStats:
    files_total: int = 0
    files_indexed: int = 0
    files_removed: int = 0
    chunks_total: int = 0
    vectors_total: int = 0


class VaultIndexer:
    def __init__(
        self,
        vault_root: Path,
        embedder: Embedder | None = None,
        embed: bool = True,
    ):
        """embedder: explicit instance (tests) or None → lazy default_embedder().
        embed=False skips the vector leg entirely (BM25 + graph only)."""
        self.vault_root = Path(vault_root)
        self._embedder = embedder
        self._embed_enabled = embed
        index_cfg = _load_vault_config(self.vault_root).get("index") or {}
        self.exclude_top = EXCLUDE_TOP_LEVEL | set(index_cfg.get("exclude_top") or [])
        self.exclude_dirs = EXCLUDE_DIR_NAMES | set(index_cfg.get("exclude_dirs") or [])

    def _get_embedder(self) -> Embedder | None:
        """Resolve lazily — model init is expensive and only needed when new
        chunks actually have to be embedded."""
        if not self._embed_enabled:
            return None
        if self._embedder is None:
            self._embedder = default_embedder()
        return self._embedder

    def _expected_model(self) -> str:
        # Comparable WITHOUT instantiating the model (avoids a download just
        # to discover nothing changed).
        if self._embedder is not None:
            return self._embedder.model_id
        return EMBED_MODEL if self._embed_enabled else ""

    # ------------------------------------------------------------- public

    def build(self, rebuild: bool = False) -> IndexStats:
        db_path = index_db_path(self.vault_root)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        if not rebuild and db_path.exists():
            rebuild = self._needs_rebuild(db_path)

        if rebuild or not db_path.exists():
            return self._rebuild_atomic(db_path)

        conn = sqlite3.connect(db_path)
        self._vec_ok = load_vec_extension(conn)
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            self._ensure_schema(conn)
            stats = self._sync(conn)
            conn.commit()
            return stats
        finally:
            conn.close()

    def _needs_rebuild(self, db_path: Path) -> bool:
        """Inspect the existing index read-only; never mutate here."""
        conn = sqlite3.connect(db_path)
        vec_ok = load_vec_extension(conn)
        try:
            if self._schema_is_stale(conn):
                return True
            if self._embedding_model_changed(conn):
                return True  # embeddings from different models never mix
            if not vec_ok and self._table_exists_static(conn, "chunks_vec"):
                # Vectors exist but sqlite-vec can't load: incremental sync
                # could not clean vec rows, and FTS5 rowid reuse would silently
                # mispair stale vectors with new chunks. Rebuild WITHOUT
                # vectors — correct and rebuildable beats corrupt.
                return True
            return False
        finally:
            conn.close()

    def _rebuild_atomic(self, db_path: Path) -> IndexStats:
        """Build into a temp file, then atomically swap. No DROP TABLE — a
        vec0 table can't even be dropped without the extension loaded, and
        in-place drops left readers a half-empty committed state. A crashed
        rebuild leaves the previous index fully intact."""
        import os

        tmp = db_path.parent / (db_path.name + ".rebuild")
        tmp.unlink(missing_ok=True)
        conn = sqlite3.connect(tmp)  # default journal — no stray -wal/-shm
        self._vec_ok = load_vec_extension(conn)
        try:
            self._ensure_schema(conn)
            stats = self._sync(conn)
            conn.commit()
        except BaseException:
            conn.close()
            tmp.unlink(missing_ok=True)
            raise
        conn.close()
        for suffix in ("-wal", "-shm"):  # stale WAL from the old file
            Path(str(db_path) + suffix).unlink(missing_ok=True)
        os.replace(tmp, db_path)
        return stats

    @staticmethod
    def _table_exists_static(conn: sqlite3.Connection, name: str) -> bool:
        return conn.execute(
            "SELECT name FROM sqlite_master WHERE name = ?", (name,)
        ).fetchone() is not None

    # ------------------------------------------------------------ internals

    def _schema_is_stale(self, conn: sqlite3.Connection) -> bool:
        try:
            row = conn.execute(
                "SELECT value FROM meta WHERE key = 'schema_version'"
            ).fetchone()
        except sqlite3.OperationalError:
            # No meta table: fresh db is fine, an older layout must rebuild.
            has_tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE name IN ('files', 'chunks')"
            ).fetchone()
            return has_tables is not None
        return row is None or row[0] != str(SCHEMA_VERSION)

    def _embedding_model_changed(self, conn: sqlite3.Connection) -> bool:
        try:
            rows = dict(conn.execute(
                "SELECT key, value FROM meta WHERE key IN"
                " ('embedding_model', 'embedding_dims')"
            ))
        except sqlite3.OperationalError:
            return False
        stored_model = rows.get("embedding_model", "")
        expected = self._expected_model()
        # "" on either side is not a conflict — it means vectors absent or not built yet.
        if bool(stored_model) and bool(expected) and stored_model != expected:
            return True
        # Same model id but different dims (custom embedder) still can't mix.
        stored_dims = rows.get("embedding_dims", "")
        if stored_dims and self._embedder is not None:
            return stored_dims != str(self._embedder.dims)
        return False

    def _ensure_schema(self, conn: sqlite3.Connection) -> None:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS files ("
            " path TEXT PRIMARY KEY, sha256 TEXT NOT NULL,"
            " mtime REAL NOT NULL, size INTEGER NOT NULL,"
            " label TEXT NOT NULL, trust_tier TEXT NOT NULL, indexed_at TEXT NOT NULL)"
        )
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5("
            " content, breadcrumb,"
            " path UNINDEXED, anchor UNINDEXED, label UNINDEXED, trust_tier UNINDEXED)"
        )
        # Raw target STEMS, resolved against the files table at query time —
        # so a [[dead link]] becomes a live edge the moment its note is
        # created, without re-indexing the linking note; deleted targets
        # simply stop resolving.
        conn.execute(
            "CREATE TABLE IF NOT EXISTS links (src TEXT NOT NULL, target_stem TEXT NOT NULL)"
        )
        conn.execute("CREATE INDEX IF NOT EXISTS links_src ON links(src)")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)"
        )
        meta = {
            "schema_version": str(SCHEMA_VERSION),
            "group_id": _vault_group_id(self.vault_root),
            # Set once vectors are first written; a model change → full rebuild.
            "embedding_model": "",
            "embedding_dims": "",
        }
        for k, v in meta.items():
            conn.execute("INSERT OR IGNORE INTO meta VALUES (?, ?)", (k, v))

    def _scan_disk(self) -> dict[str, tuple[float, int]]:
        """Return {vault-relative posix path: (mtime, size)} for indexable notes."""
        found: dict[str, tuple[float, int]] = {}
        for f in self.vault_root.rglob("*.md"):
            rel = f.relative_to(self.vault_root)
            parts = rel.parts
            if parts[0] in self.exclude_top:
                continue
            if any(p in self.exclude_dirs for p in parts):
                continue
            if any(seg in EXCLUDE_DIR_SEGMENTS for seg in parts):
                continue
            if rel.as_posix() in EXCLUDE_FILES or rel.name in EXCLUDE_FILENAMES:
                continue
            try:
                st = f.stat()
                found[rel.as_posix()] = (st.st_mtime, st.st_size)
            except OSError:
                continue
        return found

    def _sync(self, conn: sqlite3.Connection) -> IndexStats:
        stats = IndexStats()
        disk = self._scan_disk()
        stats.files_total = len(disk)
        db_rows = {
            path: (sha, mtime, size)
            for path, sha, mtime, size in conn.execute(
                "SELECT path, sha256, mtime, size FROM files"
            )
        }

        for gone in set(db_rows) - set(disk):
            self._delete_file_rows(conn, gone)
            stats.files_removed += 1

        for rel, (mtime, size) in disk.items():
            row = db_rows.get(rel)
            if row is not None and row[1] == mtime and row[2] == size:
                continue  # fast path: unchanged (mtime, size) → skip hashing
            text = (self.vault_root / rel).read_text(encoding="utf-8", errors="replace")
            sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if row is not None and row[0] == sha:
                conn.execute(
                    "UPDATE files SET mtime = ?, size = ? WHERE path = ?",
                    (mtime, size, rel),
                )
                continue  # content identical, only stat metadata drifted
            self._index_file(conn, rel, text, sha, mtime, size)
            stats.files_indexed += 1

        stats.chunks_total = conn.execute("SELECT count(*) FROM chunks").fetchone()[0]
        stats.vectors_total = self._count_vectors(conn)
        return stats

    def _delete_file_rows(self, conn: sqlite3.Connection, rel: str) -> None:
        if self._vec_ok and self._table_exists(conn, "chunks_vec"):
            rowids = [r[0] for r in conn.execute(
                "SELECT rowid FROM chunks WHERE path = ?", (rel,)
            )]
            for rid in rowids:
                conn.execute("DELETE FROM chunks_vec WHERE rowid = ?", (rid,))
        conn.execute("DELETE FROM chunks WHERE path = ?", (rel,))
        conn.execute("DELETE FROM links WHERE src = ?", (rel,))
        conn.execute("DELETE FROM files WHERE path = ?", (rel,))

    @staticmethod
    def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
        return conn.execute(
            "SELECT name FROM sqlite_master WHERE name = ?", (name,)
        ).fetchone() is not None

    def _count_vectors(self, conn: sqlite3.Connection) -> int:
        if self._vec_ok and self._table_exists(conn, "chunks_vec"):
            return conn.execute("SELECT count(*) FROM chunks_vec").fetchone()[0]
        return 0

    def _index_file(
        self,
        conn: sqlite3.Connection,
        rel: str,
        text: str,
        sha: str,
        mtime: float,
        size: int,
    ) -> None:
        parse_failed = False
        try:
            fm, _ = parse_frontmatter(text)
        except ValueError:
            fm, parse_failed = {}, True
        label, trust_tier = read_labels(fm)
        in_enforced_scope = any(rel.startswith(f"{s}/") for s in ENFORCED_SCOPES)
        if parse_failed or (in_enforced_scope and "label" not in fm):
            # Fail closed: unreadable labels, or an unlabeled note in a scope
            # where labels are mandatory, must never be default-searchable.
            label = "restricted"
        self._delete_file_rows(conn, rel)
        chunks = chunk_markdown(text, rel)
        rowids: list[int] = []
        cur = conn.cursor()
        for c in chunks:
            cur.execute(
                "INSERT INTO chunks (content, breadcrumb, path, anchor, label, trust_tier)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (c.content, c.breadcrumb, c.path, c.anchor, label, trust_tier),
            )
            rowids.append(cur.lastrowid)
        self._embed_chunks(conn, chunks, rowids)
        for target in {m.group(1).strip().lower() for m in _WIKILINK_RE.finditer(text)}:
            # Basename only — do NOT Path().stem it: [[spec.docx]] must keep
            # its extension to resolve against the shadow card spec.docx.md
            # (whose stem IS "spec.docx"); [[v1.2-spec]] must not become "v1".
            stem = target.rsplit("/", 1)[-1].strip()
            if stem and stem != Path(rel).stem.lower():
                conn.execute("INSERT INTO links VALUES (?, ?)", (rel, stem))
        conn.execute(
            "INSERT OR REPLACE INTO files VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rel, sha, mtime, size, label, trust_tier, datetime.now().isoformat()),
        )

    def _embed_chunks(
        self, conn: sqlite3.Connection, chunks: list, rowids: list[int]
    ) -> None:
        if not self._vec_ok or not chunks:
            return
        embedder = self._get_embedder()
        if embedder is None:
            return
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS chunks_vec"
            f" USING vec0(embedding float[{embedder.dims}])"
        )
        vectors = embedder.embed_docs(
            [f"{c.breadcrumb}\n{c.content}" for c in chunks]
        )
        for rid, vec in zip(rowids, vectors):
            conn.execute(
                "INSERT INTO chunks_vec (rowid, embedding) VALUES (?, ?)",
                (rid, serialize_f32(vec)),
            )
        conn.execute(
            "INSERT OR REPLACE INTO meta VALUES ('embedding_model', ?)",
            (embedder.model_id,),
        )
        conn.execute(
            "INSERT OR REPLACE INTO meta VALUES ('embedding_dims', ?)",
            (str(embedder.dims),),
        )
