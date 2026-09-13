"""Deterministic critic rubrics — pure functions, zero LLM calls, HARD GATES.

R1 citations-resolve-to-brain   (critic-draft §2 R1 + ruling Q2 cite-or-delete)
R2 regulatory-unknowns-promoted (ADR-003 Addendum A, verbatim pass criterion)
R3 verdict-uses-canonical-scale (critic-draft §2 R3)

Claim detection reuses the v1 engine's extractor patterns
(core.orchestrator.citation_validator) so the uncited-claim count stays
byte-compatible with the baseline run-1 evidence (29 uncited claims).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from core.orchestrator.citation_validator import (
    _MIN_SENTENCE_LEN,
    _RE_BRAIN_FILE,
    _RE_CITATION,
    _RE_HEADING,
    _RE_LEGAL_CLAIM,
    _RE_NUMERIC_CLAIM,
    _is_common_knowledge,
    _split_sentences,
)
from core.critic.constants import (
    ASSUMPTION_LINE_RE,
    ASSUMPTION_RATIONALE_RE,
    MAX_ASSUMPTIONS,
    R1_CITATIONS,
    R2_REGULATORY,
    R3_VERDICT,
    WARNING_SECTION_MARKER,
    match_canonical_verdict,
)
from core.critic.models import Issue, RubricResult

# ── Ref extraction patterns (R1 resolver) ───────────────────────────────────

_RE_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]*))?(?:\|[^\]]*)?\]\]")
_RE_Q_REF = re.compile(r"[\(\[]\s*(?:ref\s*:\s*)?(Q\d+)\s*[\)\]]", re.IGNORECASE)
_RE_MD_PATH = re.compile(r"([\w\-./]+\.md)\b")
_RE_URL = re.compile(r"https?://\S+")
# Transcript/file citation marker: `(ref: 04-meeting-r1-perspectives.md)` —
# sanctioned grammar for debate-sourced claims (2026-07-05 replay-2 amendment:
# the Synthesizer's PRIMARY source is the meeting record, which previously had
# no citable form). Resolution goes through _RE_MD_PATH against the task folder.
_RE_REF_MD = re.compile(r"[\(\[]\s*ref\s*:\s*[^\)\]]*\.md[^\)\]]*[\)\]]", re.IGNORECASE)

_RE_REF_CONVENTION = re.compile(r"ref\s*:\s*Q\d+", re.IGNORECASE)
_UNKNOWN_ANSWER_RE = re.compile(
    r"not\s+previously\s+considered|not\s+considered|unknown|needs?\s+confirmation"
    r"|need\s+to\s+confirm|\bTBD\b|unsure",
    re.IGNORECASE,
)
REGULATORY_TAGS = {"regulatory", "compliance", "certification"}

_RE_BLOCKER_HEADING = re.compile(r"^#{2,4}\s.*blocker", re.IGNORECASE)
_RE_OWNER = re.compile(r"owner\s*:?\**\s*[:：]?\s*([^.;|*\n]+)", re.IGNORECASE)
_RE_DEADLINE = re.compile(r"(?:deadline|due)\s*[:：]\s*([^.;|*\n]+)", re.IGNORECASE)

def _is_recommendation_heading(line: str) -> bool:
    """Heading that IS the recommendation section — tolerant of live drift.

    Live replay 2026-07-05: round 3 renamed the heading to '## Our
    recommendation' and the old `^#\\s+recommendation` regex missed it,
    contributing to a 3-round livelock. Accept headings whose text starts or
    ends with recommendation/verdict ('Recommendation', 'Our recommendation',
    'Final verdict', 'Recommendation & next steps') while still rejecting
    prose headings that merely mention it mid-sentence ('How this
    recommendation differs from the original brief')."""
    stripped = line.strip()
    if not re.match(r"#{1,4}\s", stripped):
        return False
    text = stripped.lstrip("#").strip().lower().rstrip(":")
    for word in ("recommendation", "verdict"):
        if text == word or text == word + "s":
            return True
        if text.startswith(word):
            return True
        if text.endswith(" " + word) or text.endswith(" " + word + "s"):
            return True
    return False


# ── Shared helpers ───────────────────────────────────────────────────────────


def strip_warning_section(report_text: str) -> tuple[str, bool]:
    """Drop the v1 'claims missing a source' warning section from the body.

    Returns (body, warning_section_present). The warning section quotes the
    uncited claims — leaving it in would double-count every claim.
    """
    lines = report_text.splitlines()
    for idx, line in enumerate(lines):
        if line.lstrip().startswith("#") and WARNING_SECTION_MARKER in line:
            # Also strip the '---' separator immediately above (template shape).
            cut = idx
            j = idx - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            if j >= 0 and lines[j].strip() in ("---", "***"):
                cut = j
            return "\n".join(lines[:cut]), True
    return report_text, False


# Figure tokens for the pass-B identity diff. Deliberately TIGHTER than the v1
# claim regex: units are word-boundary-anchored (so "$25,000 must" is not
# "$25,000 M"), and durations (weeks/days) are excluded — schedule labels are
# plan-native and belong to the judged R6 check, not the deterministic diff.
_RE_FIGURE = re.compile(
    r"""
    (?:
        \d+[\.,]?\d*\s*%                                                    # 20%, 3.5%
      | \$\s*\d[\d,]*(?:\.\d+)?(?:\s*(?:K|M|B|thousand|million|billion)\b)? # $5,000, $1.2M
      | \d+[\.,]?\d*\s*(?:K|M|B|thousand|million|billion)\b                 # 5 million
      | \d{1,3}(?:,\d{3})+                                                  # 1,000,000
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)


def extract_figures(text: str) -> set[str]:
    """Normalized numeric-figure tokens (pass-B deterministic identity diff)."""
    body, _ = strip_warning_section(text)
    return {
        re.sub(r"\s+", "", m.group(0)).upper()
        for m in _RE_FIGURE.finditer(body)
    }


@dataclass
class ClarificationQA:
    qid: str  # "Q5"
    question: str
    answer: str
    severity: str = ""
    tags: list[str] = field(default_factory=list)


def parse_clarification_qas(clarification_path: Path) -> list["ClarificationQA"]:
    """Parse 03-clarification.md → QAs with qid, tags, and the given answer.

    Tag convention (ADR-003 Addendum A): an optional `_Tags: regulatory_` line
    inside the question block, written by clarification_io.write_clarification.
    """
    path = Path(clarification_path)
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")

    qas: list[ClarificationQA] = []
    blocks = re.split(r"^##\s+(Q\d+)\s*(\[[A-Z]+\])?\s*$", content, flags=re.MULTILINE)
    # re.split with 2 groups → [pre, qid, sev, block, qid, sev, block, ...]
    for i in range(1, len(blocks) - 2, 3):
        qid = blocks[i].strip()
        severity = (blocks[i + 1] or "").strip("[] ")
        block = blocks[i + 2]

        tags_m = re.search(r"^_?Tags?\s*:\s*([^_\n]+)_?\s*$", block, re.MULTILINE | re.IGNORECASE)
        tags = (
            [t.strip().lower() for t in tags_m.group(1).split(",") if t.strip()]
            if tags_m else []
        )

        checked = re.search(r"^-\s+\[x\]\s+(.+)$", block, re.MULTILINE | re.IGNORECASE)
        free = re.search(r"```\n(.*?)\n```", block, re.DOTALL)
        answer = ""
        if checked:
            answer = checked.group(1).strip()
        elif free:
            txt = free.group(1).strip()
            if txt and txt != "(fill in here)":
                answer = txt

        q_match = re.search(r"^(.+\?)\s*$", block, re.MULTILINE)
        question = q_match.group(1).strip() if q_match else ""

        qas.append(ClarificationQA(
            qid=qid, question=question, answer=answer, severity=severity, tags=tags,
        ))
    return qas


def _resolves_in_vault(candidate: str, vault_root: Path, task_folder: Optional[Path]) -> bool:
    """True if a path-like ref points at a file that actually exists."""
    rel = candidate.strip().lstrip("/")
    probes = [rel, f"{rel}.md"] if not rel.endswith(".md") else [rel]
    roots = [Path(vault_root)]
    if task_folder is not None:
        roots.append(Path(task_folder))
    for root in roots:
        for probe in probes:
            if (root / probe).exists():
                return True
            # Bare Brain filenames (strategy.md, laws.md, ...) live in 00-Brain/
            if "/" not in probe and (root / "00-Brain" / probe).exists():
                return True
    return False


def _line_refs_resolve(
    line: str,
    vault_root: Path,
    task_folder: Optional[Path],
    clarification_qids: set[str],
) -> tuple[bool, list[str]]:
    """Resolve every checkable ref on a line.

    Returns (at_least_one_resolves, unresolved_refs). A URL counts as resolving
    (external research source — not checkable offline); everything else must
    point at a real file/anchor in the vault (critic-draft §2 R1 mechanics).
    """
    unresolved: list[str] = []
    resolved = False

    for m in _RE_WIKILINK.finditer(line):
        target = m.group(1).strip()
        if _resolves_in_vault(target, vault_root, task_folder):
            resolved = True
        else:
            unresolved.append(f"[[{target}]]")

    for m in _RE_Q_REF.finditer(line):
        qid = m.group(1).upper()
        if qid in clarification_qids:
            resolved = True
        else:
            unresolved.append(qid)

    for m in _RE_MD_PATH.finditer(line):
        target = m.group(1)
        if _resolves_in_vault(target, vault_root, task_folder):
            resolved = True
        else:
            unresolved.append(target)

    if _RE_URL.search(line):
        resolved = True

    return resolved, unresolved


# ── R1 · citations-resolve-to-brain ─────────────────────────────────────────


def check_citations(
    report_text: str,
    vault_root: Path,
    task_folder: Optional[Path] = None,
    report_name: str = "07-decision-report.md",
    max_assumptions: int = MAX_ASSUMPTIONS,
) -> RubricResult:
    """R1 — every claim-figure carries a ref that resolves; uncited count MUST be 0.

    ASSUMPTION-labeled lines are exempt from the count but tallied — each must
    state why it is uncitable, and >max_assumptions trips the rubric
    (2026-07-05 ruling Q2). A populated v1 warning section is non-compliant.

    AMENDMENT (2026-07-05, replay 2): resolvable sources are the Brain, research
    findings, clarification answers, AND the task's own meeting record
    (04/05/06-meeting-*.md via `(ref: <transcript>.md)` — the Synthesizer's
    primary source material previously had no citable form, making
    debate-sourced claims permanently unciteable). Spec note added to
    critic-draft §2 R1.
    """
    body, warning_present = strip_warning_section(report_text)
    clarification_qids: set[str] = set()
    if task_folder is not None:
        clar = Path(task_folder) / "03-clarification.md"
        clarification_qids = {qa.qid for qa in parse_clarification_qas(clar)}

    issues: list[Issue] = []
    uncited = 0
    non_resolving = 0
    assumptions = 0
    seq = 0

    def _issue(severity: str, expected: str, actual: str, evidence: str, fix: str) -> None:
        nonlocal seq
        seq += 1
        issues.append(Issue(
            id=f"R1-{seq}",
            rubric=R1_CITATIONS,
            severity=severity,
            expected=expected,
            actual=actual,
            evidence=evidence[:300],
            fix_instruction=fix,
            files_to_modify=[report_name],
        ))

    for line_no, raw in enumerate(body.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or _RE_HEADING.match(stripped):
            continue
        if stripped.startswith("```") or stripped.startswith("|"):
            continue

        if ASSUMPTION_LINE_RE.match(stripped):
            assumptions += 1
            if not ASSUMPTION_RATIONALE_RE.search(stripped):
                _issue(
                    "MAJOR",
                    "Every ASSUMPTION line states why the claim cannot be cited, "
                    "e.g. `ASSUMPTION: <claim> (uncitable: <reason>)`.",
                    "ASSUMPTION carries no uncitable-reason.",
                    f"[Line {line_no}] {stripped}",
                    "Append the reason the claim has no source, in the "
                    "`(uncitable: <reason>)` form — or cite/delete the claim.",
                )
            continue

        line_has_cite = bool(
            _RE_CITATION.search(stripped)
            or _RE_BRAIN_FILE.search(stripped)
            or _RE_WIKILINK.search(stripped)
            or _RE_Q_REF.search(stripped)
            or _RE_REF_MD.search(stripped)
        )

        if line_has_cite:
            # The claim carries a ref — verify it RESOLVES (this is the piece
            # v1 never did; run-1 evidence: 29 uncited claims reached Stop 1).
            has_claim = bool(
                _RE_NUMERIC_CLAIM.search(stripped) or _RE_LEGAL_CLAIM.search(stripped)
            )
            if not has_claim:
                continue
            resolved, unresolved = _line_refs_resolve(
                stripped, vault_root, task_folder, clarification_qids
            )
            if not resolved:
                non_resolving += 1
                _issue(
                    "BLOCKER",
                    "Every claim ref resolves to a real Brain file, research "
                    "path, or clarification answer (Q<n>).",
                    f"Ref(s) do not resolve: {', '.join(unresolved) or 'no checkable target'}.",
                    f"[Line {line_no}] {stripped}",
                    "Point the citation at a file/anchor that exists — or delete "
                    "the claim / downgrade it to a labeled ASSUMPTION.",
                )
            continue

        for sentence in _split_sentences(stripped):
            if len(sentence) < _MIN_SENTENCE_LEN:
                continue
            if _is_common_knowledge(sentence):
                continue
            if _RE_NUMERIC_CLAIM.search(sentence) or _RE_LEGAL_CLAIM.search(sentence):
                uncited += 1
                _issue(
                    "BLOCKER",
                    "Every claim-figure carries a source ref that resolves to "
                    "the Brain, research findings, or a clarification answer.",
                    "Claim has no citation at all.",
                    f"[Line {line_no}] {sentence[:200]}",
                    "Cite the claim from the Brain/research/clarifications; if no "
                    "source exists, delete it or downgrade to a labeled "
                    "`ASSUMPTION:` line stating why it is uncitable.",
                )

    if warning_present:
        _issue(
            "BLOCKER",
            "No 'claims missing a source' warning section — the critic forces "
            "resolution before the human, not disclosure to the human.",
            "The draft still carries the v1 warning section.",
            f"## ⚠️ {WARNING_SECTION_MARKER}",
            "Resolve every listed claim (cite, delete, or ASSUMPTION-downgrade) "
            "and remove the warning section entirely.",
        )
    if assumptions > max_assumptions:
        _issue(
            "BLOCKER",
            f"At most {max_assumptions} ASSUMPTION lines per report.",
            f"{assumptions} ASSUMPTION lines found.",
            f"{assumptions} lines labeled ASSUMPTION:",
            "Resolve assumptions into cited claims or delete the weakest — "
            "a report built on assumptions is not fit for a human gate.",
        )

    rationale_missing = sum(1 for i in issues if "uncitable-reason" in i.actual)
    passed = (
        uncited == 0
        and non_resolving == 0
        and assumptions <= max_assumptions
        and not warning_present
        and rationale_missing == 0
    )
    return RubricResult(
        rubric_id=R1_CITATIONS,
        passed=passed,
        score=1.0 if passed else 0.0,
        blocking=True,
        issues=issues,
        info={
            "uncited": uncited,
            "non_resolving": non_resolving,
            "assumptions": assumptions,
            "warning_section_present": warning_present,
        },
    )


# ── R2 · regulatory-unknowns-promoted ───────────────────────────────────────


def flagged_regulatory_qas(qas: list["ClarificationQA"]) -> list["ClarificationQA"]:
    """QAs whose tags ∈ {regulatory, compliance, certification} AND whose
    answer matches the unknown-set (ADR-003 Addendum A). Shared by the R2
    rubric and the deterministic skeleton assembler."""
    return [
        qa for qa in qas
        if REGULATORY_TAGS & set(qa.tags) and _UNKNOWN_ANSWER_RE.search(qa.answer or "")
    ]


def find_blocker_row(blockers_text: str, qid: str) -> Optional[str]:
    """The blocker row line carrying `(ref: <qid>)`, or None."""
    row_re = re.compile(
        r"^.*[\(\[]\s*ref\s*:\s*" + re.escape(qid) + r"\s*[\)\]].*$",
        re.IGNORECASE | re.MULTILINE,
    )
    m = row_re.search(blockers_text)
    return m.group(0) if m else None


def row_completeness(row_text: str) -> tuple[bool, bool]:
    """(owner_present, deadline_present) for a blocker row."""
    owner = _RE_OWNER.search(row_text)
    deadline = _RE_DEADLINE.search(row_text)
    return (
        bool(owner and owner.group(1).strip()),
        bool(deadline and deadline.group(1).strip()),
    )


def _blocker_section(report_text: str) -> str:
    """All blocker sections' text (from a /blocker/ heading to the next ## heading)."""
    lines = report_text.splitlines()
    captured: list[str] = []
    in_section = False
    section_level = 2
    for line in lines:
        if _RE_BLOCKER_HEADING.match(line.strip()):
            in_section = True
            section_level = len(line.strip()) - len(line.strip().lstrip("#"))
            continue
        if in_section:
            stripped = line.strip()
            if stripped.startswith("#"):
                level = len(stripped) - len(stripped.lstrip("#"))
                if level <= section_level:
                    in_section = False
                    continue
            captured.append(line)
    return "\n".join(captured)


def check_regulatory_promoted(
    report_text: str,
    qas: list[ClarificationQA],
    judge_fn: Optional[Callable[[ClarificationQA, str], bool]] = None,
    report_name: str = "07-decision-report.md",
) -> RubricResult:
    """R2 — ADR-003 Addendum A, verbatim: any clarification answer matching
    {not previously considered / unknown / needs confirmation / TBD} on a
    question tagged regulatory/compliance/certification MUST appear in the
    blocker list with an owner and a deadline.

    Deterministic where the `(ref: Q<n>)` convention exists; `judge_fn` is the
    transitional judged fallback for reports predating the convention.
    """
    body, _ = strip_warning_section(report_text)
    flagged = flagged_regulatory_qas(qas)

    issues: list[Issue] = []
    blockers = _blocker_section(body)
    convention_present = bool(_RE_REF_CONVENTION.search(body))

    def _row_template(qa: ClarificationQA) -> str:
        return (
            f"`- [ ] **<action for the {qa.qid} unknown>** (ref: {qa.qid}). "
            "*Owner: <dept/person>. Deadline: <date/week>.*`"
        )

    # Live replay 3 regression: the draft had NO blockers section at all — the
    # FCC unknown lived in prose and every per-row fix was unanchored. When the
    # section is missing AND regulatory unknowns exist, say so as its own
    # issue, with the exact heading + row grammar (replay-2 passed only
    # because that draft happened to include a section — structural, not luck).
    if flagged and not blockers.strip():
        issues.append(Issue(
            id="R2-0",
            rubric=R2_REGULATORY,
            severity="BLOCKER",
            expected=(
                "The report always contains a blockers section (canonical "
                "heading `## Blockers (before Stop 2)` — the heading must "
                "contain the word 'Blockers'), holding one row per regulatory "
                "unknown."
            ),
            actual=(
                "No blockers section exists anywhere in the report — the "
                f"regulatory unknown(s) {', '.join(qa.qid for qa in flagged)} "
                "have no home."
            ),
            evidence="(no heading containing 'Blockers'/'blocker' found)",
            fix_instruction=(
                "Add the section `## Blockers (before Stop 2)` (restoring this "
                "REQUIRED section is a fix, not new scope) containing exactly "
                "one row per regulatory unknown, e.g. "
                + "; ".join(_row_template(qa) for qa in flagged)
            ),
            files_to_modify=[report_name],
        ))

    for n, qa in enumerate(flagged, start=1):
        row_text = find_blocker_row(blockers, qa.qid)
        if row_text is not None:
            owner_ok, deadline_ok = row_completeness(row_text)
            if owner_ok and deadline_ok:
                continue
            issues.append(Issue(
                id=f"R2-{n}",
                rubric=R2_REGULATORY,
                severity="BLOCKER",
                expected=f"The blocker row for {qa.qid} carries a non-empty owner AND deadline.",
                actual=(
                    f"Blocker row found for {qa.qid} but "
                    f"{'owner' if not owner_ok else 'deadline'} is missing/empty."
                ),
                evidence=row_text.strip()[:300],
                fix_instruction=(
                    f"Complete the {qa.qid} blocker row to EXACTLY this form: "
                    f"{_row_template(qa)}"
                ),
                files_to_modify=[report_name],
            ))
            continue

        if not convention_present and judge_fn is not None and judge_fn(qa, blockers):
            continue  # transitional judged match: a blocker row covers this unknown

        issues.append(Issue(
            id=f"R2-{n}",
            rubric=R2_REGULATORY,
            severity="BLOCKER",
            expected=(
                "A regulatory/compliance/certification unknown is a first-class "
                "blocker with an owner and a deadline — never buried in one "
                "department's cost math (ADR-003 Addendum A)."
            ),
            actual=f"No blocker row references {qa.qid} (`ref: {qa.qid}`).",
            evidence=f"{qa.qid} [{','.join(qa.tags)}] answered: {qa.answer[:150]}",
            fix_instruction=(
                f"Add one row to the blockers section (heading contains "
                f"'Blockers'), in EXACTLY this form: {_row_template(qa)}"
            ),
            files_to_modify=[report_name],
        ))

    passed = not issues
    return RubricResult(
        rubric_id=R2_REGULATORY,
        passed=passed,
        score=1.0 if passed else 0.0,
        blocking=True,
        issues=issues,
        info={
            "flagged_qids": [qa.qid for qa in flagged],
            "convention_present": convention_present,
        },
    )


# ── R3 · verdict-uses-canonical-scale ───────────────────────────────────────


def find_verdict_line(report_text: str) -> Optional[str]:
    """First non-empty line after the '## Recommendation' (or Verdict) heading."""
    lines = strip_warning_section(report_text)[0].splitlines()
    for idx, line in enumerate(lines):
        if _is_recommendation_heading(line):
            for follower in lines[idx + 1:]:
                stripped = follower.strip()
                if stripped and not stripped.startswith("#"):
                    return stripped
            return None
    return None


def check_verdict(
    report_text: str,
    report_name: str = "07-decision-report.md",
) -> RubricResult:
    """R3 — the verdict line matches EXACTLY one of the five canonical tiers.

    GO | GO-WITH-CONDITIONS | PROCEED-WITH-REVISIONS | NEED-MORE-INFO | NO-GO

    Decision rule (per spec §2 R3, "the verdict line matches exactly one of
    the five canonical tiers"): PASS iff exactly ONE canonical tier token
    appears on the verdict line. Zero tiers (hedged prose, invented scales)
    and two-plus tiers (fence-sitting) both fail. Live-replay lesson
    2026-07-05: requiring the whole line to EQUAL the tier livelocked round 2's
    `**GO-WITH-CONDITIONS** — Proceed, but only after ...` for 3 rounds —
    trailing elaboration is not fence-sitting.
    """
    from core.critic.constants import CANONICAL_VERDICTS, find_verdict_tokens

    line = find_verdict_line(report_text)
    verdict: Optional[str] = None
    tokens: list[str] = []
    if line:
        # Whole-line match first (also maps legacy fixture aliases like
        # "Approve with conditions"), then the exactly-one-token rule.
        verdict = match_canonical_verdict(line)
        if verdict is None:
            tokens = find_verdict_tokens(line)
            if len(tokens) == 1:
                verdict = tokens[0]
    passed = verdict is not None

    issues: list[Issue] = []
    if not passed:
        if line and len(tokens) > 1:
            actual = (
                f"Verdict line names {len(tokens)} tiers ({', '.join(tokens)}) — "
                "fence-sitting."
            )
        elif line:
            actual = f"Verdict line is '{line}' — no canonical tier token present."
        else:
            actual = "No verdict line found under a Recommendation/Verdict heading."
        issues.append(Issue(
            id="R3-1",
            rubric=R3_VERDICT,
            severity="BLOCKER",
            expected=(
                "The first line under '## Recommendation' contains exactly one of: "
                + " | ".join(CANONICAL_VERDICTS)
                + " — written verbatim (ALL-CAPS, hyphenated), ideally alone on the line."
            ),
            actual=actual,
            evidence=line or "(missing '## Recommendation' section)",
            fix_instruction=(
                "Under a '## Recommendation' heading, commit to exactly one "
                "canonical tier token, e.g. `GO-WITH-CONDITIONS`. Never use any "
                "other scale word (no 'Approved', 'GO-CONDITIONAL', 'DEFER'). "
                "Hedged language is not a verdict."
            ),
            files_to_modify=[report_name],
        ))

    return RubricResult(
        rubric_id=R3_VERDICT,
        passed=passed,
        score=1.0 if passed else 0.0,
        blocking=True,
        issues=issues,
        info={"verdict": verdict, "verdict_line": line},
    )
