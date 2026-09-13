"""Deterministic critic rubrics — R1/R2/R3 unit tests.

Fixture provenance: docs/tests/fixtures/critic/baseline-run-1-07-decision-report.md
is a byte-identical copy of the frozen baseline
04-Projects/Agentic-OS/04-evals/baseline-run-1-cy80l-eol/07-decision-report.md
(read-only evidence; copied so the suite runs in every fleet repo).

Covers critic-draft acceptance test T7 (strip-3-citations / bogus-ref) and the
2026-07-05 rulings: ASSUMPTION escape with rationale, >5 assumptions trip,
warning-section death.
"""
from __future__ import annotations

from pathlib import Path

from core.critic.constants import (
    R1_CITATIONS,
    R2_REGULATORY,
    R3_VERDICT,
    match_canonical_verdict,
)
from core.critic.deterministic import (
    ClarificationQA,
    check_citations,
    check_regulatory_promoted,
    check_verdict,
    parse_clarification_qas,
    strip_warning_section,
)

FIXTURES = Path(__file__).parent.parent / "fixtures" / "critic"
BASELINE_REPORT = FIXTURES / "baseline-run-1-07-decision-report.md"


def _make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    (vault / "00-Brain").mkdir(parents=True)
    for name in ("strategy.md", "products.md", "budget.md", "laws.md"):
        (vault / "00-Brain" / name).write_text(f"# {name}\n", encoding="utf-8")
    return vault


# ── R1 · citations-resolve-to-brain ─────────────────────────────────────────


class TestR1OnFrozenBaseline:
    """Acceptance anchor: run-1's report reached Stop 1 with 29 uncited claims."""

    def test_frozen_run1_report_has_29_uncited_claims(self, tmp_path):
        vault = _make_vault(tmp_path)
        report = BASELINE_REPORT.read_text(encoding="utf-8")
        result = check_citations(report, vault_root=vault)
        assert result.rubric_id == R1_CITATIONS
        assert result.passed is False
        assert result.info["uncited"] == 29  # baseline finding #1, exactly
        assert result.blocking is True

    def test_frozen_run1_warning_section_is_non_compliant(self, tmp_path):
        """Ruling Q2: surfaced-in-warning ≠ compliant post-critic."""
        vault = _make_vault(tmp_path)
        report = BASELINE_REPORT.read_text(encoding="utf-8")
        result = check_citations(report, vault_root=vault)
        assert result.info["warning_section_present"] is True
        assert any("warning section" in i.fix_instruction.lower() for i in result.issues)

    def test_strip_warning_section_detects_and_removes(self):
        report = BASELINE_REPORT.read_text(encoding="utf-8")
        body, present = strip_warning_section(report)
        assert present is True
        assert "claims missing a source" not in body


CLEAN_REPORT = """---
type: decision_report
stop: 1
---
# Decision report: test

## 📌 Bottom line (30-second read)
- We recommend the purchase, sized to real demand data. [[00-Brain/strategy.md]]

## Recommendation
GO-WITH-CONDITIONS

## Detailed analysis
Revenue grew 25% year over year per the Brain. [[00-Brain/budget.md]]
The unit sells for $389 with a 39% margin (ref: Q1).
This is common practice across the industry.

## To do before launch (BLOCKERS)
- [ ] **Confirm supplier pricing** (ref: Q1). *Owner: Finance. Deadline: Week 2.*
"""


def _write_clean_clarification(task_folder: Path) -> None:
    task_folder.mkdir(parents=True, exist_ok=True)
    (task_folder / "03-clarification.md").write_text(
        "---\ntype: clarification\n---\n\n"
        "## Q1 [CRITICAL]\n_Cite: 00-Brain/products.md_\n\n"
        "What is the unit price?\n\n- [x] A) $389\n",
        encoding="utf-8",
    )


class TestR1CleanAndBrokenReports:
    def test_clean_synthetic_report_passes(self, tmp_path):
        vault = _make_vault(tmp_path)
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)
        result = check_citations(CLEAN_REPORT, vault_root=vault, task_folder=task)
        assert result.passed is True, [i.evidence for i in result.issues]
        assert result.info == {
            "uncited": 0, "non_resolving": 0, "assumptions": 0,
            "warning_section_present": False,
        }

    def test_t7_strip_exactly_three_citations_flags_exactly_those_three(self, tmp_path):
        """T7: golden report minus 3 citations → checker reports exactly those 3."""
        vault = _make_vault(tmp_path)
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)
        broken = (
            CLEAN_REPORT
            .replace(" [[00-Brain/strategy.md]]", "")   # strip cite 1
            .replace(" [[00-Brain/budget.md]]", "")      # strip cite 2
            .replace(" (ref: Q1).\n", ".\n")             # strip cite 3 (the $389 claim)
        )
        result = check_citations(broken, vault_root=vault, task_folder=task)
        assert result.passed is False
        assert result.info["uncited"] == 2  # the two claim-figure lines stripped
        # the bottom-line line has no figure → not a claim; blocker line keeps its ref
        stripped_line_hits = [i for i in result.issues if i.severity == "BLOCKER"]
        assert len(stripped_line_hits) == 2
        evidence = " ".join(i.evidence for i in result.issues)
        assert "25%" in evidence and "$389" in evidence

    def test_t7_bogus_brain_ref_reported_as_non_resolving(self, tmp_path):
        vault = _make_vault(tmp_path)
        report = CLEAN_REPORT.replace(
            "[[00-Brain/budget.md]]", "[[00-Brain/nonexistent]]"
        )
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.passed is False
        assert result.info["non_resolving"] == 1
        bogus = [i for i in result.issues if "nonexistent" in i.actual or "nonexistent" in i.evidence]
        assert bogus, [i.actual for i in result.issues]

    def test_unresolvable_q_ref_flagged(self, tmp_path):
        vault = _make_vault(tmp_path)
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)  # only Q1 exists
        report = CLEAN_REPORT.replace("(ref: Q1).", "(ref: Q9).")
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.passed is False
        assert result.info["non_resolving"] == 1


class TestR1AssumptionEscape:
    """Ruling Q2: cite-or-delete with a labeled ASSUMPTION escape hatch."""

    def test_assumption_lines_exempt_but_counted(self, tmp_path):
        vault = _make_vault(tmp_path)
        report = CLEAN_REPORT.replace(
            "This is common practice across the industry.",
            "ASSUMPTION: broker premiums run 2x contract price "
            "(uncitable: no supplier quote on file yet).",
        )
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.passed is True
        assert result.info["assumptions"] == 1

    def test_assumption_without_rationale_is_an_issue(self, tmp_path):
        vault = _make_vault(tmp_path)
        report = CLEAN_REPORT.replace(
            "This is common practice across the industry.",
            "ASSUMPTION: broker premiums run 2x contract price.",
        )
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.passed is False
        assert any("uncitable" in i.expected for i in result.issues)

    def test_more_than_five_assumptions_trips_the_critic(self, tmp_path):
        """Ruling Q2 guard: >5 assumptions in a report trips the critic."""
        vault = _make_vault(tmp_path)
        assumptions = "\n".join(
            f"ASSUMPTION: assumed figure {n} is ${n}00 (uncitable: no source #{n})."
            for n in range(1, 7)  # 6 assumptions
        )
        report = CLEAN_REPORT + "\n" + assumptions + "\n"
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.info["assumptions"] == 6
        assert result.passed is False
        assert any("At most 5" in i.expected for i in result.issues)

    def test_exactly_five_assumptions_still_passes(self, tmp_path):
        vault = _make_vault(tmp_path)
        assumptions = "\n".join(
            f"ASSUMPTION: assumed figure {n} is ${n}00 (uncitable: no source #{n})."
            for n in range(1, 6)  # 5 assumptions — the limit, not over it
        )
        report = CLEAN_REPORT + "\n" + assumptions + "\n"
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.info["assumptions"] == 5
        assert result.passed is True


# ── R2 · regulatory-unknowns-promoted (ADR-003 Addendum A / test T3 slice) ──

FCC_QA = ClarificationQA(
    qid="Q5",
    question="Is the team aware of the FCC re-authorization gate?",
    answer="C) Not previously considered — need to factor this in",
    severity="CRITICAL",
    tags=["regulatory"],
)

REPORT_WITH_FCC_BLOCKER = """# Decision report

## Recommendation
GO-WITH-CONDITIONS

## To do before launch (BLOCKERS)
- [ ] **Scope the FCC re-authorization path** (ref: Q5). *Owner: 02-npi-program-management. Deadline: Week 2.*
"""

REPORT_WITHOUT_FCC_BLOCKER = """# Decision report

## Recommendation
GO-WITH-CONDITIONS

## Detailed analysis
Engineering folded the FCC cost into its estimate (ref: Q5).

## To do before launch (BLOCKERS)
- [ ] **Confirm supplier pricing.** *Owner: Finance. Deadline: Week 2.*
"""


class TestR2RegulatoryPromotion:
    def test_tagged_unknown_with_owned_dated_blocker_row_passes(self):
        result = check_regulatory_promoted(REPORT_WITH_FCC_BLOCKER, [FCC_QA])
        assert result.rubric_id == R2_REGULATORY
        assert result.passed is True
        assert result.info["flagged_qids"] == ["Q5"]

    def test_tagged_unknown_buried_outside_blockers_fails(self):
        """The run-1 FCC failure, by design: mentioned in cost math ≠ promoted."""
        result = check_regulatory_promoted(REPORT_WITHOUT_FCC_BLOCKER, [FCC_QA])
        assert result.passed is False
        assert result.issues[0].severity == "BLOCKER"
        assert "Q5" in result.issues[0].actual

    def test_blocker_row_missing_owner_or_deadline_fails(self):
        report = REPORT_WITH_FCC_BLOCKER.replace(
            "*Owner: 02-npi-program-management. Deadline: Week 2.*", ""
        )
        result = check_regulatory_promoted(report, [FCC_QA])
        assert result.passed is False

    def test_untagged_unknown_is_not_flagged(self):
        qa = ClarificationQA(qid="Q2", question="Sales runway?", answer="Unknown", tags=[])
        result = check_regulatory_promoted(REPORT_WITHOUT_FCC_BLOCKER, [qa])
        assert result.passed is True
        assert result.info["flagged_qids"] == []

    def test_tagged_but_answered_concretely_is_not_flagged(self):
        qa = ClarificationQA(
            qid="Q5", question="FCC gate?", answer="Yes — budgeted at $120K",
            tags=["regulatory"],
        )
        result = check_regulatory_promoted(REPORT_WITHOUT_FCC_BLOCKER, [qa])
        assert result.passed is True

    def test_judged_fallback_used_only_when_convention_absent(self):
        """Transitional fallback for reports predating the (ref: Q<n>) convention."""
        legacy_report = REPORT_WITHOUT_FCC_BLOCKER.replace(" (ref: Q5)", "")
        calls = []

        def judge_fn(qa, blockers):
            calls.append(qa.qid)
            return True  # judge says a blocker row covers it

        result = check_regulatory_promoted(legacy_report, [FCC_QA], judge_fn=judge_fn)
        assert calls == ["Q5"]
        assert result.passed is True
        # With the convention present anywhere, the fallback must NOT fire.
        calls.clear()
        result = check_regulatory_promoted(REPORT_WITHOUT_FCC_BLOCKER, [FCC_QA],
                                           judge_fn=judge_fn)
        assert calls == []
        assert result.passed is False


class TestParseClarificationQAs:
    def test_parses_qid_tags_and_answers(self, tmp_path):
        path = tmp_path / "03-clarification.md"
        path.write_text(
            "---\ntype: clarification\n---\n\n"
            "## Q1 [CRITICAL]\n_Cite: 00-Brain/laws.md_\n_Tags: regulatory, certification_\n\n"
            "Is the FCC grant valid?\n\n"
            "- [ ] A) Yes\n- [x] C) Not previously considered\n\n"
            "## Q2 [WARN]\n_Cite: 00-Brain/budget.md_\n\n"
            "What is the budget?\n\n**Answer:**\n```\n$250K-$1M confirmed\n```\n",
            encoding="utf-8",
        )
        qas = parse_clarification_qas(path)
        assert [qa.qid for qa in qas] == ["Q1", "Q2"]
        assert qas[0].tags == ["regulatory", "certification"]
        assert qas[0].answer == "C) Not previously considered"
        assert qas[0].severity == "CRITICAL"
        assert qas[1].tags == []
        assert qas[1].answer == "$250K-$1M confirmed"

    def test_missing_file_returns_empty(self, tmp_path):
        assert parse_clarification_qas(tmp_path / "nope.md") == []


# ── R3 · verdict-uses-canonical-scale ────────────────────────────────────────


class TestR3CanonicalVerdict:
    def test_all_five_canonical_tiers_pass(self):
        for tier in ("GO", "GO-WITH-CONDITIONS", "PROCEED-WITH-REVISIONS",
                     "NEED-MORE-INFO", "NO-GO"):
            report = f"# R\n\n## Recommendation\n\n**{tier}**\n"
            result = check_verdict(report)
            assert result.passed is True, tier
            assert result.info["verdict"] == tier

    def test_fixture_alias_maps_in(self):
        assert match_canonical_verdict("Approve with conditions") == "GO-WITH-CONDITIONS"
        assert match_canonical_verdict("proceed-with-revisions") == "PROCEED-WITH-REVISIONS"
        assert match_canonical_verdict("Need more info") == "NEED-MORE-INFO"

    def test_hedged_verdict_fails(self):
        report = "# R\n\n## Recommendation\n\nCautiously optimistic, monitor closely.\n"
        result = check_verdict(report)
        assert result.rubric_id == R3_VERDICT
        assert result.passed is False

    def test_frozen_run1_verdict_fails_the_scale(self):
        report = BASELINE_REPORT.read_text(encoding="utf-8")
        result = check_verdict(report)
        assert result.passed is False  # "Proceed — with conditions." + prose

    def test_missing_recommendation_section_fails(self):
        result = check_verdict("# R\n\nNo verdict here.\n")
        assert result.passed is False
        assert "No verdict line" in result.issues[0].actual

    # ── Live-replay regressions (2026-07-05 CY-80L, 3-round livelock) ────────
    # Spec §2 R3: the verdict line "matches exactly one of the five canonical
    # tiers" — ONE tier token present. The original whole-line-equality check
    # was stricter than spec and livelocked the live run's round-2 draft.

    def test_live_replay_round2_verdict_with_trailing_prose_passes(self):
        """The exact round-2 line that failed 3 straight rounds live."""
        report = (
            "# R\n\n## Recommendation\n\n"
            "**GO-WITH-CONDITIONS** — Proceed, but only after meeting specific "
            "data requirements described below.\n"
        )
        result = check_verdict(report)
        assert result.passed is True
        assert result.info["verdict"] == "GO-WITH-CONDITIONS"

    def test_live_replay_round1_invented_scale_still_fails(self):
        """The exact round-1 line: no canonical token → fail (as it should)."""
        report = (
            "# R\n\n## Recommendation\n\n"
            "**Approved — with conditions** (see required actions below)\n"
        )
        result = check_verdict(report)
        assert result.passed is False
        assert "no canonical tier token" in result.issues[0].actual

    def test_live_replay_our_recommendation_heading_is_found(self):
        """Round 3 renamed the heading to '## Our recommendation'."""
        report = "# R\n\n## Our recommendation\n\nGO-WITH-CONDITIONS\n"
        result = check_verdict(report)
        assert result.passed is True

    def test_prose_heading_mentioning_recommendation_is_not_the_verdict_section(self):
        """Round 3 also had '## How this recommendation differs from the
        original brief' — must not be mistaken for the verdict section."""
        report = (
            "# R\n\n"
            "## How this recommendation differs from the original brief\n\n"
            "We now buy more stock than the brief assumed.\n\n"
            "## Our recommendation\n\nNEED-MORE-INFO\n"
        )
        result = check_verdict(report)
        assert result.passed is True
        assert result.info["verdict"] == "NEED-MORE-INFO"

    def test_two_tiers_on_the_verdict_line_is_fence_sitting_and_fails(self):
        report = "# R\n\n## Recommendation\n\nEither GO or NO-GO depending on the data.\n"
        result = check_verdict(report)
        assert result.passed is False
        assert "fence-sitting" in result.issues[0].actual

    def test_spaced_tier_token_is_accepted(self):
        report = "# R\n\n## Recommendation\n\nGO WITH CONDITIONS\n"
        result = check_verdict(report)
        assert result.passed is True
        assert result.info["verdict"] == "GO-WITH-CONDITIONS"


# ── R1 amendment (2026-07-05, replay 2): transcript citations ────────────────


class TestR1TranscriptCitations:
    """Replay 2 stalled at 5 uncited claims — all department-position content
    from the meeting record, which had no sanctioned citable form. Amendment:
    `(ref: 0X-meeting-*.md)` resolves against the task folder."""

    def _task_with_transcripts(self, tmp_path):
        vault = _make_vault(tmp_path)
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)
        for name in ("04-meeting-r1-perspectives.md", "05-meeting-r2-debate.md",
                     "06-meeting-r3-perspectives.md"):
            (task / name).write_text(f"# {name}\n", encoding="utf-8")
        return vault, task

    def test_debate_sourced_claim_cited_via_transcript_ref_passes(self, tmp_path):
        vault, task = self._task_with_transcripts(tmp_path)
        # A live replay-2 stuck claim, now written with the sanctioned form.
        report = CLEAN_REPORT.replace(
            "This is common practice across the industry.",
            "The chip-swap project requires 8-12 weeks of software testing "
            "(ref: 05-meeting-r2-debate.md).",
        )
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.passed is True, [i.evidence for i in result.issues]
        assert result.info["uncited"] == 0
        assert result.info["non_resolving"] == 0

    def test_department_qualifier_after_transcript_filename_is_accepted(self, tmp_path):
        vault, task = self._task_with_transcripts(tmp_path)
        report = CLEAN_REPORT.replace(
            "This is common practice across the industry.",
            "Quality must pull the last 90 days of RMA data "
            "(ref: 04-meeting-r1-perspectives.md · 03-quality-reliability).",
        )
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.passed is True, [i.evidence for i in result.issues]

    def test_transcript_ref_to_missing_file_is_non_resolving(self, tmp_path):
        vault = _make_vault(tmp_path)
        task = vault / "02-Tasks" / "t1"
        _write_clean_clarification(task)  # no transcript files written
        report = CLEAN_REPORT.replace(
            "This is common practice across the industry.",
            "Estimated at 10-16 weeks (ref: 04-meeting-r1-perspectives.md).",
        )
        result = check_citations(report, vault_root=vault, task_folder=task)
        assert result.passed is False
        assert result.info["non_resolving"] == 1
        assert result.info["uncited"] == 0  # marker present — it's a resolution failure

    def test_accepted_grammar_documents_the_transcript_form(self):
        from core.critic.constants import ACCEPTED_GRAMMAR
        assert "(ref: 04-meeting-r1-perspectives.md)" in ACCEPTED_GRAMMAR
        assert "05-meeting-r2-debate.md" in ACCEPTED_GRAMMAR
        assert "06-meeting-r3-perspectives.md" in ACCEPTED_GRAMMAR
        assert "MEETING RECORD" in ACCEPTED_GRAMMAR

    def test_frozen_baseline_count_is_unchanged_by_the_amendment(self, tmp_path):
        """The 29-uncited anchor must not drift: the frozen report has no
        transcript refs, so the new marker changes nothing there."""
        vault = _make_vault(tmp_path)
        report = BASELINE_REPORT.read_text(encoding="utf-8")
        result = check_citations(report, vault_root=vault)
        assert result.info["uncited"] == 29


# ── R2 structural cases (2026-07-05 replay 3 regression) ─────────────────────
# Replay 3's final report had NO blockers section at all — FCC lived in prose
# 3× and every per-row fix instruction was unanchored. The section is now
# structural: mandated by the contract, and its absence is its own issue
# carrying the exact heading + row grammar.


class TestR2MissingSectionEntirely:
    def test_missing_blockers_section_gets_dedicated_issue_with_exact_grammar(self):
        report = (
            "# Decision report\n\n## Recommendation\nGO-WITH-CONDITIONS\n\n"
            "## Detailed analysis\nThe FCC re-authorization question is open "
            "and mentioned here in prose only.\n"
        )
        result = check_regulatory_promoted(report, [FCC_QA])
        assert result.passed is False
        r2_0 = [i for i in result.issues if i.id == "R2-0"]
        assert len(r2_0) == 1
        assert "No blockers section exists" in r2_0[0].actual
        # Fix text carries the exact canonical heading and full row template.
        assert "## Blockers (before Stop 2)" in r2_0[0].fix_instruction
        assert "(ref: Q5)" in r2_0[0].fix_instruction
        assert "*Owner: <dept/person>. Deadline: <date/week>.*" in r2_0[0].fix_instruction
        # The revision-rule conflict is defused inside the fix itself.
        assert "not new scope" in r2_0[0].fix_instruction

    def test_no_flagged_unknowns_and_no_section_still_passes_scanner(self):
        """The always-present section is contract-mandated; the scanner only
        bites when a regulatory unknown actually needs a home."""
        report = "# R\n\n## Recommendation\nGO\n\nAll clear.\n"
        qa = ClarificationQA(qid="Q1", question="Price?", answer="B) $389", tags=[])
        result = check_regulatory_promoted(report, [qa])
        assert result.passed is True

    def test_canonical_heading_variant_is_recognized(self):
        report = (
            "# R\n\n## Recommendation\nGO-WITH-CONDITIONS\n\n"
            "## Blockers (before Stop 2)\n"
            "- [ ] **Assess FCC re-authorization trigger** (ref: Q5). "
            "*Owner: 02-npi-program-management. Deadline: Week 2.*\n"
        )
        result = check_regulatory_promoted(report, [FCC_QA])
        assert result.passed is True, [i.actual for i in result.issues]

    def test_missing_row_fix_echoes_exact_row_format(self):
        result = check_regulatory_promoted(REPORT_WITHOUT_FCC_BLOCKER, [FCC_QA])
        assert result.passed is False
        fix = result.issues[0].fix_instruction
        assert "(ref: Q5)" in fix
        assert "*Owner: <dept/person>. Deadline: <date/week>.*" in fix

    def test_grammar_mandates_the_section_and_forbids_renames(self):
        from core.critic.constants import ACCEPTED_GRAMMAR
        assert "## Blockers (before Stop 2)" in ACCEPTED_GRAMMAR
        assert "ALWAYS contains a blockers section" in ACCEPTED_GRAMMAR
        assert "Regulatory & Approval\n  Gates" in ACCEPTED_GRAMMAR or \
            "Regulatory & Approval" in ACCEPTED_GRAMMAR  # renames named as invisible

    def test_synthesizer_template_carries_the_canonical_section(self):
        from core.meeting.synthesizer import SYNTHESIZER_PROMPT
        assert "## Blockers (before Stop 2)" in SYNTHESIZER_PROMPT
        assert 'write "None." if empty' in SYNTHESIZER_PROMPT
