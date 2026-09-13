"""Deterministic report skeleton — the engine assembles structure, the model writes prose.

Design ruling (2026-07-05, after live replay 4): four fix-cycles proved that
prompt mandates cannot guarantee structure — no replay-4 draft ever contained
the Blockers heading despite a mandated template, and gates oscillated between
rounds. ADR house style: deterministic-first — "the model can forget; the hook
does not." This module ASSEMBLES the structural skeleton in code after the
model/translator produce prose:

- Blockers section: built from the structured data the engine already holds
  (clarification QAs with tags + unknown-set answers). One row per tagged
  unknown in the exact scanner grammar; Owner/Deadline default to
  `TBD — assign at Stop 1` when the model didn't supply them (honest — the
  human sees the TBD at Stop 1). R2 becomes a build-time invariant.
- Verdict line: the model must still EMIT a tier (only it can decide); the
  engine parses it (verdict line → whole-line tier anywhere in the body) and
  renders the canonical `## Recommendation` line/heading. R3 becomes an
  invariant whenever a tier is parseable; unparseable drafts still fail R3
  and the issue goes back to the Synthesizer (the engine never invents a verdict).

Both operations are no-ops on compliant text (byte-stable), so re-assembly on
every round is idempotent.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from core.critic.constants import match_canonical_verdict
from core.critic.deterministic import (
    ClarificationQA,
    _RE_BLOCKER_HEADING,
    _is_recommendation_heading,
    find_blocker_row,
    flagged_regulatory_qas,
    row_completeness,
)

TBD_FIELD = "TBD — assign at Stop 1"
BLOCKERS_HEADING = "## Blockers (before Stop 2)"

_RE_DECISIONS_HEADING = re.compile(r"^#{1,4}\s+.*decisions", re.IGNORECASE)
_RE_BOTTOM_LINE_HEADING = re.compile(r"^#{1,4}\s+.*bottom line", re.IGNORECASE)


@dataclass
class SkeletonResult:
    text: str
    changed: bool
    verdict: Optional[str] = None          # canonical tier, when parseable
    verdict_rendered: bool = False         # engine had to place/normalize it
    blockers_section_created: bool = False
    blocker_rows_added: list[str] = field(default_factory=list)      # qids
    blocker_rows_completed: list[str] = field(default_factory=list)  # qids

    def info(self) -> dict:
        return {
            "verdict": self.verdict,
            "verdict_rendered": self.verdict_rendered,
            "blockers_section_created": self.blockers_section_created,
            "blocker_rows_added": self.blocker_rows_added,
            "blocker_rows_completed": self.blocker_rows_completed,
        }


# ── Verdict-line placement ───────────────────────────────────────────────────


def _line_is_lone_tier(line: str) -> Optional[str]:
    """Canonical tier when the line IS a tier (whole-line match), else None."""
    return match_canonical_verdict(line)


def _verdict_line_compliant(line: str) -> Optional[str]:
    """Tier when the line already satisfies R3 (exactly one token), else None."""
    from core.critic.constants import find_verdict_tokens

    verdict = match_canonical_verdict(line)
    if verdict:
        return verdict
    tokens = find_verdict_tokens(line)
    return tokens[0] if len(tokens) == 1 else None


def ensure_verdict_line(text: str) -> tuple[str, Optional[str], bool]:
    """Render the canonical verdict placement. Returns (text, verdict, changed).

    Cases:
    A. Recommendation heading + compliant verdict line → no-op.
    B. Heading exists, line non-compliant, a lone-tier line exists in the body
       → insert that tier as the first line under the heading (no deletion).
    C. Heading missing, exactly one distinct lone-tier line in the body
       → synthesize the `## Recommendation` section after the Bottom-line
       section (or after the title / frontmatter).
    D. Nothing parseable / ambiguous (two distinct tiers) → no-op, verdict=None
       (R3 fails as the safety assert; only the model can supply a verdict).
    """
    lines = text.splitlines()
    trailing_nl = text.endswith("\n")

    heading_idx: Optional[int] = None
    for idx, line in enumerate(lines):
        if _is_recommendation_heading(line):
            heading_idx = idx
            break

    def _body_tiers() -> list[tuple[int, str]]:
        found: list[tuple[int, str]] = []
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("|"):
                continue
            tier = _line_is_lone_tier(stripped)
            if tier:
                found.append((idx, tier))
        return found

    if heading_idx is not None:
        # First non-empty line under the heading.
        for idx in range(heading_idx + 1, len(lines)):
            stripped = lines[idx].strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                break  # empty section
            tier = _verdict_line_compliant(stripped)
            if tier:
                return text, tier, False  # case A — no-op
            # Case B: non-compliant line; look for a lone tier in the body.
            body = _body_tiers()
            distinct = sorted({t for _, t in body})
            if len(distinct) == 1:
                lines.insert(idx, distinct[0])
                lines.insert(idx + 1, "")
                new_text = "\n".join(lines) + ("\n" if trailing_nl else "")
                return new_text, distinct[0], True
            return text, None, False  # case D
        # Heading with an empty section: fall through to the body scan.
        body = _body_tiers()
        distinct = sorted({t for _, t in body})
        if len(distinct) == 1:
            lines.insert(heading_idx + 1, "")
            lines.insert(heading_idx + 2, distinct[0])
            new_text = "\n".join(lines) + ("\n" if trailing_nl else "")
            return new_text, distinct[0], True
        return text, None, False

    # Case C — heading missing entirely.
    body = _body_tiers()
    distinct = sorted({t for _, t in body})
    if len(distinct) != 1:
        return text, None, False  # case D
    tier = distinct[0]

    insert_at = _default_insert_index(lines)
    section = ["## Recommendation", "", tier, ""]
    lines[insert_at:insert_at] = section
    new_text = "\n".join(lines) + ("\n" if trailing_nl else "")
    return new_text, tier, True


def _default_insert_index(lines: list[str]) -> int:
    """After the Bottom-line section if present, else after the first H1,
    else after the frontmatter block, else at the top."""
    for idx, line in enumerate(lines):
        if _RE_BOTTOM_LINE_HEADING.match(line.strip()):
            for j in range(idx + 1, len(lines)):
                if lines[j].strip().startswith("#"):
                    return j
            return len(lines)
    for idx, line in enumerate(lines):
        if re.match(r"^#\s", line.strip()):
            return idx + 1
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                return j + 1
    return 0


# ── Blockers-section assembly ────────────────────────────────────────────────


def _synthesized_row(qa: ClarificationQA) -> str:
    topic = re.sub(r"\s+", " ", (qa.question or f"clarification {qa.qid}")).strip()
    topic = topic.rstrip("?").strip()
    if len(topic) > 90:
        topic = topic[:87].rstrip() + "..."
    tags = "/".join(qa.tags) if qa.tags else "regulatory"
    return (
        f"- [ ] **Resolve the {tags} unknown from {qa.qid}: {topic}** "
        f"(ref: {qa.qid}). *Owner: {TBD_FIELD}. Deadline: {TBD_FIELD}.*"
    )


def _find_blockers_span(lines: list[str]) -> Optional[tuple[int, int]]:
    """(heading_idx, end_idx_exclusive) of the first blockers section."""
    for idx, line in enumerate(lines):
        if _RE_BLOCKER_HEADING.match(line.strip()):
            level = len(line.strip()) - len(line.strip().lstrip("#"))
            for j in range(idx + 1, len(lines)):
                stripped = lines[j].strip()
                if stripped.startswith("#"):
                    j_level = len(stripped) - len(stripped.lstrip("#"))
                    if j_level <= level:
                        return idx, j
            return idx, len(lines)
    return None


def ensure_blockers_section(
    text: str, qas: list[ClarificationQA]
) -> tuple[str, dict]:
    """Assemble the Blockers section from the engine's structured data.

    - Section exists: keep every model-authored row; append a synthesized row
      per flagged unknown that has none; complete incomplete rows with TBD
      Owner/Deadline fields.
    - Section missing: create it (canonical heading) with one row per flagged
      unknown, or `None.` when there is nothing to block on — the section is
      ALWAYS present in the composed report.
    """
    lines = text.splitlines()
    trailing_nl = text.endswith("\n")
    flagged = flagged_regulatory_qas(qas)
    info: dict = {
        "section_created": False,
        "rows_added": [],
        "rows_completed": [],
    }

    span = _find_blockers_span(lines)
    changed = False

    if span is None:
        rows = [_synthesized_row(qa) for qa in flagged] or ["None."]
        info["section_created"] = True
        info["rows_added"] = [qa.qid for qa in flagged]
        section = ["", BLOCKERS_HEADING, "", *rows, ""]
        insert_at = len(lines)
        for idx, line in enumerate(lines):
            if _RE_DECISIONS_HEADING.match(line.strip()):
                insert_at = idx
                break
        lines[insert_at:insert_at] = section
        changed = True
    else:
        heading_idx, end_idx = span
        section_text = "\n".join(lines[heading_idx:end_idx])
        appended: list[str] = []
        for qa in flagged:
            row = find_blocker_row(section_text, qa.qid)
            if row is None:
                appended.append(_synthesized_row(qa))
                info["rows_added"].append(qa.qid)
                continue
            owner_ok, deadline_ok = row_completeness(row)
            if owner_ok and deadline_ok:
                continue
            # Complete the model's row in place — append only missing fields.
            suffix = ""
            if not owner_ok:
                suffix += f" *Owner: {TBD_FIELD}.*"
            if not deadline_ok:
                suffix += f" *Deadline: {TBD_FIELD}.*"
            for k in range(heading_idx, end_idx):
                if lines[k] == row:
                    lines[k] = row + suffix
                    break
            info["rows_completed"].append(qa.qid)
            changed = True
        if appended:
            # Insert before the trailing blank lines of the section.
            insert_at = end_idx
            while insert_at > heading_idx + 1 and not lines[insert_at - 1].strip():
                insert_at -= 1
            lines[insert_at:insert_at] = appended
            changed = True

    if not changed:
        return text, info
    return "\n".join(lines) + ("\n" if trailing_nl else ""), info


# ── Composition ──────────────────────────────────────────────────────────────


def assemble_skeleton(text: str, qas: list[ClarificationQA]) -> SkeletonResult:
    """Apply the full structural skeleton. Idempotent; no-op on compliant text."""
    out, verdict, verdict_changed = ensure_verdict_line(text)
    out, blockers_info = ensure_blockers_section(out, qas)
    changed = verdict_changed or out != text
    return SkeletonResult(
        text=out,
        changed=changed,
        verdict=verdict,
        verdict_rendered=verdict_changed,
        blockers_section_created=blockers_info["section_created"],
        blocker_rows_added=blockers_info["rows_added"],
        blocker_rows_completed=blockers_info["rows_completed"],
    )
