"""Episodic decision ledger — 00-Brain/decision-ledger.md (ADR-004 §1).

Structured successor to the frozen prose decisions-log.md. The ENGINE owns the
lifecycle (never the LLM): Stop-2 approval appends a pending entry; recording
the real-world outcome resolves it. Entries are markdown blocks — readable in
Obsidian, parsed deterministically, and indexed by vault_search like any note.

Retrieval is by recency (CrewAI's lesson: outcome-scored episodic records
don't need vectors). Injection into agents is Step 3 and is judge-only.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from core.brain.schema import DecisionEntry

LEDGER_FILENAME = "decision-ledger.md"

_HEADER = """---
type: brain
section: decision-ledger
label: internal
trust_tier: brain
---
# Decision Ledger

Episodic memory: one block per approved decision, appended automatically at
Stop-2 approval. Record outcomes with `bd-os outcome <task-folder> ...` —
entries stay `pending` until then and are never dropped. Do not edit by hand;
the prose history lives in [[decisions-log]] (frozen).
"""

_BLOCK_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2}) — (.+?)\s*$", re.MULTILINE)
_FIELD_RE = re.compile(r"^- (\w+): (.*)$", re.MULTILINE)
_TOKEN_RE = re.compile(r"\w+", re.UNICODE)
TOPIC_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "for", "by",
    "we", "is", "are", "was", "be", "do", "did", "it", "our", "with", "from",
}
_TOPIC_STOPWORDS = TOPIC_STOPWORDS  # internal alias
# Mini anti-poisoning screen (full gates are Step 5): directive-like text from
# downstream-of-web reports must not be laundered into a trust_tier:brain file.
_DIRECTIVE_RE = re.compile(
    r"(always\s|never\s|remember\s+that|for\s+future\s+reference|from\s+now\s+on"
    r"|if\s+the\s+user\s+later|ignore\s+(all\s+)?previous|disregard\s+(all\s+)?prior)",
    re.IGNORECASE,
)


def _screen_directives(text: str) -> str:
    if _DIRECTIVE_RE.search(text):
        return "[directive-like text quarantined] " + _DIRECTIVE_RE.sub("[…]", text)
    return text


def _render_block(e: DecisionEntry) -> str:
    lines = [
        f"\n### {e.date.isoformat()} — {_one_line(e.slug)}",
        f"- Status: {e.status}",
        f"- Owner: {e.owner}",
        f"- Decision: {_one_line(e.decision)}",
    ]
    if e.reason:
        lines.append(f"- Reason: {_one_line(e.reason)}")
    if e.task_ref:
        lines.append(f"- Reference: {_one_line(e.task_ref)}")
    if e.status == "resolved":
        lines.append(f"- Quality: {e.quality if e.quality is not None else ''}")
        lines.append(f"- Outcome: {_one_line(e.outcome or '')}")
        if e.reflection:
            lines.append(f"- Reflection: {_one_line(e.reflection)}")
        if e.resolved_date:
            lines.append(f"- Resolved: {e.resolved_date.isoformat()}")
    return "\n".join(lines) + "\n"


def _one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class DecisionLedger:
    def __init__(self, path: Path):
        self.path = Path(path)

    # ------------------------------------------------------------- writes

    def ensure_file(self) -> None:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(_HEADER, encoding="utf-8")

    def append(self, entry: DecisionEntry) -> bool:
        """Append a new entry. Idempotent by slug (Stop-2 re-runs must not duplicate)."""
        if self.has(entry.slug):
            return False
        self.ensure_file()
        with self.path.open("a", encoding="utf-8") as f:
            f.write(_render_block(entry))
        return True

    def resolve(
        self,
        slug: str,
        outcome: str,
        quality: float,
        reflection: str = "",
        resolved_date: date | None = None,
    ) -> bool:
        """Flip an entry pending→resolved in place. Returns False if slug unknown.

        Raises ValueError on out-of-range or non-finite quality — NaN slips
        through click.FloatRange and would render an unparseable block.
        """
        if not (0.0 <= quality <= 1.0):  # NaN fails both comparisons → rejected
            raise ValueError(f"quality must be a finite value in [0, 1], got {quality}")
        entries = self.entries()
        target = next((e for e in entries if e.slug == slug), None)
        if target is None:
            return False
        target.status = "resolved"
        target.outcome = _screen_directives(outcome)
        target.quality = quality
        target.reflection = _screen_directives(reflection) if reflection else target.reflection
        target.resolved_date = resolved_date or date.today()
        self._rewrite_block(target)
        return True

    def _rewrite_block(self, entry: DecisionEntry) -> None:
        text = self.path.read_text(encoding="utf-8")
        spans = self._block_spans(text)
        start, end = spans[entry.slug]
        self.path.write_text(
            text[:start] + _render_block(entry) + text[end:], encoding="utf-8"
        )

    # ------------------------------------------------------------- reads

    def has(self, slug: str) -> bool:
        """Header-based, NOT parse-based: a malformed block must still count,
        otherwise a Stop-2 re-run would append a duplicate slug and the older
        block would become an unreachable zombie in _block_spans."""
        if not self.path.exists():
            return False
        return slug in self._block_spans(self.path.read_text(encoding="utf-8"))

    def entries(self) -> list[DecisionEntry]:
        if not self.path.exists():
            return []
        text = self.path.read_text(encoding="utf-8")
        out: list[DecisionEntry] = []
        for slug, (start, end) in self._block_spans(text).items():
            entry = self._parse_block(text[start:end])
            if entry is not None:
                out.append(entry)
        return out

    def recent(self, k: int = 5, topic: str | None = None) -> list[DecisionEntry]:
        """Newest-first, optional topic filter (token overlap on slug + decision).

        Short tokens survive (RMA/BOM/ECO/LTB are this division's vocabulary);
        only stopwords are dropped. A topic with no usable tokens degrades to
        plain recency rather than filtering everything out.
        """
        entries = sorted(self.entries(), key=lambda e: e.date, reverse=True)
        if topic:
            tokens = {
                t.lower() for t in _TOKEN_RE.findall(topic)
                if len(t) >= 2 and t.lower() not in _TOPIC_STOPWORDS
            }
            if tokens:
                entries = [
                    e for e in entries
                    if tokens & {t.lower() for t in _TOKEN_RE.findall(f"{e.slug} {e.decision}")}
                ]
        return entries[:k]

    def _block_spans(self, text: str) -> dict[str, tuple[int, int]]:
        matches = list(_BLOCK_RE.finditer(text))
        spans: dict[str, tuple[int, int]] = {}
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            spans[m.group(2).strip()] = (m.start(), end)
        return spans

    def _parse_block(self, block: str) -> DecisionEntry | None:
        head = _BLOCK_RE.match(block)
        if not head:
            return None
        fields = {m.group(1).lower(): m.group(2).strip() for m in _FIELD_RE.finditer(block)}
        try:
            quality = float(fields["quality"]) if fields.get("quality") else None
        except ValueError:
            quality = None
        if quality is not None and not (0.0 <= quality <= 1.0):
            quality = None  # keep the block parseable instead of dropping the entry
        try:
            return DecisionEntry(
                date=date.fromisoformat(head.group(1)),
                slug=head.group(2).strip(),
                owner=fields.get("owner", "Department Head"),
                decision=fields.get("decision", ""),
                reason=fields.get("reason", ""),
                task_ref=fields.get("reference") or None,
                status="resolved" if fields.get("status") == "resolved" else "pending",
                quality=quality,
                outcome=fields.get("outcome") or None,
                reflection=fields.get("reflection") or None,
                resolved_date=(
                    date.fromisoformat(fields["resolved"]) if fields.get("resolved") else None
                ),
            )
        except (ValueError, TypeError):
            return None  # a malformed block must not break Brain loading


# ------------------------------------------------------------------ Stop-2 hook

def ledger_path(vault_root: Path) -> Path:
    return Path(vault_root) / "00-Brain" / LEDGER_FILENAME


def extract_decision_summary(report_md: str, max_chars: int = 400) -> str:
    """Deterministic one-liner from 07-decision-report.md: TL;DR section first,
    then a Decision/Verdict section, then the first body paragraph."""
    for heading in (r"TL;?DR", r"Decision", r"Verdict"):
        # (?![#\n]) — the capture must start at real content: an empty section
        # falls through instead of swallowing the next heading (\n+ backtracking
        # would otherwise sneak past a bare (?!#) guard via the blank line).
        m = re.search(
            rf"^#{{2,4}}\s+{heading}[^\n]*\n+(?![#\n])(.+?)(?=\n#{{1,6}}\s|\Z)",
            report_md, re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        if m and m.group(1).strip():
            return _one_line(m.group(1))[:max_chars]
    body = re.sub(r"^---\n.*?\n---\n", "", report_md, flags=re.DOTALL)
    for para in body.split("\n\n"):
        para = para.strip()
        if para and not para.startswith("#"):
            return _one_line(para)[:max_chars]
    return "(no decision report found)"


def record_approved_decision(vault_root: Path, task_folder: Path) -> bool:
    """Called by FlowController.execute() at Stop-2 approval. Engine-owned,
    deterministic, idempotent — the ledger never depends on an LLM remembering."""
    vault_root, task_folder = Path(vault_root), Path(task_folder)
    report = task_folder / "07-decision-report.md"
    summary = (
        extract_decision_summary(report.read_text(encoding="utf-8", errors="replace"))
        if report.exists() else "(no decision report found)"
    )
    try:
        rel = task_folder.resolve().relative_to(vault_root.resolve()).as_posix()
    except ValueError:
        rel = f"02-Tasks/{task_folder.name}"
    entry = DecisionEntry(
        date=date.today(),
        slug=task_folder.name,
        owner="Department Head",
        decision=_screen_directives(summary),
        task_ref=f"{rel}/07-decision-report.md",
    )
    return DecisionLedger(ledger_path(vault_root)).append(entry)


def write_outcome_note(task_folder: Path, outcome: str, quality: float) -> Path:
    path = Path(task_folder) / "outcome.md"
    path.write_text(
        "---\ntype: outcome\n"
        f"quality: {quality}\n"
        f"recorded: {date.today().isoformat()}\n---\n"
        f"# Outcome\n\n{outcome}\n",
        encoding="utf-8",
    )
    return path
