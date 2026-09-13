"""Critic constants — canonical verdict scale, rubric ids, weights, model tiers.

TradingAgents lesson (critic-draft §2 R3): centralize the scale once
"so nothing drifts". Every module regex-checks against THIS list.
"""
from __future__ import annotations

import re

# ── Canonical 5-tier verdict scale (critic-draft §2 R3) ────────────────────
# Anti-fence-sitting: "cautiously optimistic, monitor closely" is not a verdict.
CANONICAL_VERDICTS: tuple[str, ...] = (
    "GO",
    "GO-WITH-CONDITIONS",
    "PROCEED-WITH-REVISIONS",
    "NEED-MORE-INFO",
    "NO-GO",
)

# Legacy fixture verdict classes map in (critic-draft §2 R3).
VERDICT_ALIASES: dict[str, str] = {
    "APPROVE-WITH-CONDITIONS": "GO-WITH-CONDITIONS",
    "PROCEED-WITH-REVISIONS": "PROCEED-WITH-REVISIONS",
    "NEED-MORE-INFO": "NEED-MORE-INFO",
}

# ── Rubric ids (byte-identical with 04-evals/fixtures/README where shared) ─
R1_CITATIONS = "citations-resolve-to-brain"
R2_REGULATORY = "regulatory-unknowns-promoted"
R3_VERDICT = "verdict-uses-canonical-scale"
R4_NUMBERS = "numbers-reconcile"
R5_DEBATE_SIDES = "both-debate-sides-represented"
R6_REPORT_VS_PLAN = "factual-consistency-report-vs-plan"

BLOCKING_RUBRICS: tuple[str, ...] = (R1_CITATIONS, R2_REGULATORY, R3_VERDICT)

# §2 weights (documentation + scorecard display). The aggregate uses only the
# judged rubrics, renormalized (§3): Pass A → R4 0.5 / R5 0.5. Deterministic
# rubrics are HARD GATES outside the aggregate (2026-07-05 ruling).
RUBRIC_WEIGHTS: dict[str, float] = {
    R1_CITATIONS: 0.30,
    R2_REGULATORY: 0.20,
    R3_VERDICT: 0.10,
    R4_NUMBERS: 0.20,
    R5_DEBATE_SIDES: 0.20,
}
JUDGED_RUBRICS_PASS_A: tuple[str, ...] = (R4_NUMBERS, R5_DEBATE_SIDES)
JUDGED_RUBRICS_PASS_B: tuple[str, ...] = (R6_REPORT_VS_PLAN,)

# ── ASSUMPTION escape hatch (ruling Q2) ─────────────────────────────────────
# Cite-or-delete with a labeled escape: `ASSUMPTION: <claim> (why uncitable: <reason>)`.
# Each ASSUMPTION must state why it cannot be cited; >MAX_ASSUMPTIONS trips the critic.
ASSUMPTION_LINE_RE = re.compile(r"^\s*(?:[-*>]\s*)*\**ASSUMPTION\**\s*:", re.IGNORECASE)
ASSUMPTION_RATIONALE_RE = re.compile(
    r"\(\s*(?:why\s+)?uncitable\b[^)]*\)|—\s*why\s+uncitable\s*:", re.IGNORECASE
)
MAX_ASSUMPTIONS = 5

# The v1 warning section is NOT compliant post-critic (ruling Q2: "warning section dies").
WARNING_SECTION_MARKER = "Warning: claims missing a source"

# ── Rounds-exhausted banner (ruling Q1: banner, no pre-gate PAUSE) ──────────
THRESHOLD_NOT_MET_BANNER_HEADER = "> [!warning] THRESHOLD-NOT-MET"

# ── Model tiers (C10: judge cost concentrated on the cheap tier) ────────────
# "quick"   → cheap judge model; "deep"/"primary" → resolve to llm.primary from
# engine config; any other value is passed through as an explicit model id.
MODEL_TIER_QUICK = "claude-haiku-4-5"


def resolve_judge_model(tier_or_model: str, primary_model: str | None = None) -> str | None:
    """Map the critic.judge_model knob to a concrete model id.

    Returns None when the provider default should be used.
    """
    value = (tier_or_model or "").strip()
    if value.lower() == "quick":
        return MODEL_TIER_QUICK
    if value.lower() in ("deep", "primary"):
        return primary_model
    return value or None


# ── The machine-checked grammar (single source of truth) ────────────────────
# Injected verbatim into the Synthesizer contract, the judge prompt, and every
# revision instruction. Live replay 2026-07-05 lesson: the judge invented a
# wrong verdict scale ("GO-CONDITIONAL | DEFER") and suggested citation formats
# the scanner rejects — because nothing ever told either of them the grammar.
ACCEPTED_GRAMMAR = """VERDICT (deterministic scanner):
- Under a heading named `## Recommendation`, the first line contains EXACTLY ONE of:
  GO | GO-WITH-CONDITIONS | PROCEED-WITH-REVISIONS | NEED-MORE-INFO | NO-GO
- Write the tier token verbatim (ALL-CAPS, hyphenated). Best form: the token alone
  on its own line. Never use any other scale word (no "Approved", "GO-CONDITIONAL",
  "DEFER", "Conditional GO", ...).

CITATIONS (deterministic scanner) — a claim line is cited ONLY by one of:
- `[[00-Brain/<file>.md]]` — wikilink to a Brain file that exists
- `(ref: Q<n>)` or `(Q<n>)` — a clarification question that exists
- `(ref: 04-meeting-r1-perspectives.md)` — a claim sourced from the MEETING RECORD
  (department positions R1, debate R2, perspectives R3). Use the transcript file
  the claim came from: `04-meeting-r1-perspectives.md`, `05-meeting-r2-debate.md`,
  or `06-meeting-r3-perspectives.md`. You may name the department after the file:
  `(ref: 04-meeting-r1-perspectives.md · 03-quality-reliability)`
- `<file>.md` mentioned on the line (e.g. `products.md`, `05-research/findings.md`)
- a full URL (`https://...`) for an external research source
Nothing else counts: "(Dept 01 position paper)", "(Q1 answer)", "(internal
meeting)", "see transcripts" are ALL rejected by the scanner. Department
estimates and positions from the meeting ARE citable — use the transcript form
above, never leave them uncited.

ASSUMPTIONS (deterministic scanner):
- A claim with no source is either DELETED or written as its own line:
  `ASSUMPTION: <claim> (uncitable: <why no source exists>)`
- The line must start with `ASSUMPTION:` — inline `[ASSUMPTION]` markers are
  rejected. More than 5 ASSUMPTION lines in a report is an automatic rejection.

BLOCKERS SECTION (deterministic scanner):
- The report ALWAYS contains a blockers section — canonical heading:
  `## Blockers (before Stop 2)`. The heading MUST contain the word "Blockers".
  If there are no blockers, keep the section and write `None.`
- NEVER rename it or substitute another heading ("Regulatory & Approval
  Gates", "Required actions", "Open items" are all invisible to the scanner).
- Every regulatory/compliance/certification clarification answered
  unknown/not-considered/needs-confirmation gets EXACTLY ONE row in that
  section, in EXACTLY this form:
  `- [ ] **<action>** (ref: Q<n>). *Owner: <dept/person>. Deadline: <date/week>.*"""


# Normalization used by the R3 checker and anywhere a verdict line is compared.
_VERDICT_STRIP_RE = re.compile(r"[*_`#>\[\]]")


def normalize_verdict_line(line: str) -> str:
    """Uppercase, strip markdown emphasis + surrounding punctuation, spaces→dashes."""
    text = _VERDICT_STRIP_RE.sub("", line).strip()
    text = re.sub(r"[.!:;,]+$", "", text).strip()
    text = re.sub(r"[\s_]+", "-", text.upper())
    text = re.sub(r"-{2,}", "-", text)
    return text


def match_canonical_verdict(line: str) -> str | None:
    """Return the canonical verdict if the line IS exactly one tier, else None."""
    normalized = normalize_verdict_line(line)
    if normalized in CANONICAL_VERDICTS:
        return normalized
    return VERDICT_ALIASES.get(normalized)
def find_verdict_tokens(line: str) -> list[str]:
    """Canonical tier tokens present in a verdict line (longest-first, boundary-safe).

    Live replay 2026-07-05: round 2 produced `**GO-WITH-CONDITIONS** — Proceed,
    but only after ...` and the old whole-line-equality check failed it for 3
    straight rounds. Spec §2 R3 says the verdict line "matches exactly one" of
    the five tiers — one tier present, no second tier. Trailing elaboration is
    not fence-sitting; zero tiers or two tiers is.
    """
    text = re.sub(r"[*_`#>\[\]()\u2014\u2013—–]", " ", line).upper()
    found: list[str] = []
    for tier in sorted(CANONICAL_VERDICTS, key=len, reverse=True):
        pattern = re.compile(
            r"(?<![A-Z0-9-])" + tier.replace("-", r"[-\s]+") + r"(?![A-Z0-9-])"
        )
        if pattern.search(text):
            found.append(tier)
            text = pattern.sub(" \u00a7 ", text)  # blank out so GO ⊄ GO-WITH-CONDITIONS
    return found
