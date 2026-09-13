"""LLM-judged critic rubrics — 5-sample majority vote, fully mocked LLM.

Covers: majority scoring, ≥4/5 blocking rule (2026-07-05 ruling Q4: 3/5 split
only lowers the aggregate), confidence-floor filtering, ≥3/5 issue
corroboration, unparseable-sample handling, structural CriticError.
"""
from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from core.critic.constants import R4_NUMBERS, R5_DEBATE_SIDES, R6_REPORT_VS_PLAN
from core.critic.judge import PASS_A_RUBRICS, PASS_B_RUBRICS, CriticJudge
from core.critic.models import CriticError


def _sample(r4="PASS", r5="PASS", issues=None, score=0.9):
    return json.dumps({
        "rubric_verdicts": {R4_NUMBERS: r4, R5_DEBATE_SIDES: r5},
        "overall_score": score,
        "issues": issues or [],
    })


def _issue(rubric=R4_NUMBERS, evidence="the $240/unit figure in section 3",
           confidence=0.9, id_="ISS-1"):
    return {
        "id": id_, "rubric": rubric, "severity": "MAJOR",
        "expected": "figures reconcile", "actual": "totals disagree",
        "evidence": evidence, "fix_instruction": "fix the total",
        "files_to_modify": ["07-decision-report.md"], "confidence": confidence,
    }


def _judge(llm, **kwargs):
    defaults = dict(judge_samples=5, confidence_floor=0.80,
                    issue_vote_floor=3, blocking_vote_floor=4)
    defaults.update(kwargs)
    return CriticJudge(llm=llm, **defaults)


class TestMajorityVote:
    def test_all_pass_scores_one(self):
        llm = MagicMock()
        llm.complete.side_effect = [_sample() for _ in range(5)]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.results[R4_NUMBERS].score == 1.0
        assert outcome.results[R5_DEBATE_SIDES].score == 1.0
        assert outcome.aggregate == 1.0
        assert llm.complete.call_count == 5  # ADK default: 5 samples

    def test_three_of_five_fail_lowers_aggregate_but_does_not_block(self):
        """Ruling Q4: a 3/5 split failure only lowers the aggregate."""
        llm = MagicMock()
        llm.complete.side_effect = (
            [_sample(r4="FAIL") for _ in range(3)] + [_sample() for _ in range(2)]
        )
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        r4 = outcome.results[R4_NUMBERS]
        assert r4.score == pytest.approx(0.4)  # 2/5 PASS
        assert r4.info["high_confidence_fail"] is False
        # aggregate = 0.5*0.4 + 0.5*1.0 = 0.7 — R4 shaky alone stays above 0.6
        assert outcome.aggregate == pytest.approx(0.7)

    def test_four_of_five_fail_blocks(self):
        """Ruling Q4: ≥4/5 FAIL agreement blocks (= ECC 80% confidence rule)."""
        llm = MagicMock()
        llm.complete.side_effect = (
            [_sample(r4="FAIL") for _ in range(4)] + [_sample()]
        )
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        r4 = outcome.results[R4_NUMBERS]
        assert r4.info["high_confidence_fail"] is True
        assert r4.passed is False

    def test_both_rubrics_shaky_drops_aggregate_below_threshold(self):
        """§3: with two judged rubrics at 0.5/0.5, both can't be shaky at once."""
        llm = MagicMock()
        llm.complete.side_effect = [
            _sample(r4="FAIL", r5="FAIL"), _sample(r4="FAIL", r5="PASS"),
            _sample(r4="PASS", r5="FAIL"), _sample(r4="FAIL", r5="PASS"),
            _sample(r4="PASS", r5="FAIL"),
        ]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        # R4: 2/5 PASS = 0.4 · R5: 2/5 PASS = 0.4 → aggregate 0.4 < 0.6
        assert outcome.aggregate == pytest.approx(0.4)


class TestSampleRobustness:
    def test_unparseable_samples_are_discarded(self):
        llm = MagicMock()
        llm.complete.side_effect = ["not json at all", _sample(), _sample(),
                                    _sample(), _sample()]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.invalid_samples == 1
        assert len(outcome.samples) == 4
        assert outcome.results[R4_NUMBERS].score == 1.0

    def test_all_samples_unparseable_raises_critic_error(self):
        """Structural failure = OpenAI ladder `raise`, never a retry round."""
        llm = MagicMock()
        llm.complete.side_effect = ["garbage"] * 5
        with pytest.raises(CriticError):
            _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)

    def test_json_in_code_fence_is_parsed(self):
        llm = MagicMock()
        llm.complete.side_effect = [f"```json\n{_sample()}\n```"] * 5
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.invalid_samples == 0

    def test_judge_model_tier_is_passed_through(self):
        llm = MagicMock()
        llm.complete.side_effect = [_sample()] * 5
        judge = _judge(llm, model="claude-haiku-4-5")
        judge.run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        for call in llm.complete.call_args_list:
            assert call.kwargs.get("model") == "claude-haiku-4-5"


class TestIssueCorroboration:
    def test_issue_corroborated_by_three_samples_is_sent_back(self):
        llm = MagicMock()
        llm.complete.side_effect = (
            [_sample(r4="FAIL", issues=[_issue()]) for _ in range(3)]
            + [_sample() for _ in range(2)]
        )
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert len(outcome.corroborated_issues) == 1
        assert outcome.corroborated_issues[0].rubric == R4_NUMBERS
        assert outcome.low_confidence == []

    def test_one_or_two_sample_issues_stay_low_confidence(self):
        """§3 confidence gate: 1–2-sample issues never reach the Synthesizer."""
        llm = MagicMock()
        llm.complete.side_effect = (
            [_sample(issues=[_issue()]) for _ in range(2)]
            + [_sample() for _ in range(3)]
        )
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.corroborated_issues == []
        assert len(outcome.low_confidence) == 1

    def test_issues_below_confidence_floor_are_dropped_outright(self):
        llm = MagicMock()
        llm.complete.side_effect = (
            [_sample(issues=[_issue(confidence=0.5)]) for _ in range(5)]
        )
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.corroborated_issues == []
        assert outcome.low_confidence == []

    def test_different_evidence_issues_are_not_merged(self):
        llm = MagicMock()
        llm.complete.side_effect = (
            [_sample(issues=[_issue(evidence="the $240/unit RMA benchmark row")]),
             _sample(issues=[_issue(evidence="week 6 kill-gate paragraph omission")]),
             _sample(issues=[_issue(evidence="the $240/unit RMA benchmark row")])]
            + [_sample()] * 2
        )
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.corroborated_issues == []
        assert len(outcome.low_confidence) == 2


class TestPassBPrompt:
    def test_pass_b_judges_r6_and_sees_the_plan(self):
        llm = MagicMock()
        llm.complete.side_effect = [json.dumps({
            "rubric_verdicts": {R6_REPORT_VS_PLAN: "FAIL"},
            "overall_score": 0.2,
            "issues": [_issue(rubric=R6_REPORT_VS_PLAN,
                              evidence='plan calls the EOL chip "faulty"')],
        })] * 5
        outcome = _judge(llm).run(
            PASS_B_RUBRICS, draft="the report", plan="the faulty plan",
            round_no=1, max_rounds=2,
        )
        r6 = outcome.results[R6_REPORT_VS_PLAN]
        assert r6.info["high_confidence_fail"] is True  # 5/5 FAIL
        assert len(outcome.corroborated_issues) == 1
        assert "faulty" in outcome.corroborated_issues[0].evidence
        # the judge prompt must carry both documents + the EOL drift warning
        user_msg = llm.complete.call_args_list[0].args[0][1]["content"]
        sys_msg = llm.complete.call_args_list[0].args[0][0]["content"]
        assert "the faulty plan" in user_msg and "the report" in user_msg
        assert "end-of-life" in sys_msg  # R6 rubric text carries the canary


# ── No silent zeros (2026-07-05 replay 2 regression) ─────────────────────────
# numbers-reconcile scored 0.0 in all 6 live rounds while the revision
# instruction carried none of its issues: round-3 sample attrition (3/5
# unparseable) made the ABSOLUTE corroboration floor unreachable, demoting
# 0.95-confidence issues that named the exact defective lines.


class TestNoSilentZeros:
    def test_failing_rubric_with_uncorroborated_issues_promotes_them(self):
        """Invariant: a judged rubric scoring < passing MUST carry ≥1 issue.
        Each sample reports a DIFFERENT-evidence issue (groups of 1 — below
        any floor) → the best ones are promoted, never silently dropped."""
        evidences = [
            "the $240 benchmark row invents a figure",
            "week six kill gate paragraph contradicts itself",
            "landed cost table sums wrong across scenarios",
            "margin percentage disagrees between summary and detail",
            "freight estimate lacks arithmetic trace to inputs",
        ]
        llm = MagicMock()
        llm.complete.side_effect = [
            _sample(r4="FAIL", issues=[_issue(
                evidence=evidences[n],
                confidence=0.90 + n / 100,
            )])
            for n in range(5)
        ]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.results[R4_NUMBERS].score == 0.0
        r4_issues = [i for i in outcome.corroborated_issues if i.rubric == R4_NUMBERS]
        assert len(r4_issues) >= 1  # promoted for actionability
        assert outcome.results[R4_NUMBERS].issues  # attached to the rubric result
        assert outcome.results[R4_NUMBERS].info.get(
            "issues_promoted_for_actionability") == 2
        # highest-confidence candidates were chosen
        assert all(i.confidence >= 0.92 for i in r4_issues)

    def test_failing_rubric_with_no_issues_at_all_gets_synthetic_issue(self):
        llm = MagicMock()
        llm.complete.side_effect = [_sample(r4="FAIL", issues=[]) for _ in range(5)]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        r4 = outcome.results[R4_NUMBERS]
        assert r4.score == 0.0
        assert r4.info.get("synthetic_issue") is True
        syn = [i for i in outcome.corroborated_issues if i.rubric == R4_NUMBERS]
        assert len(syn) == 1
        assert syn[0].id == f"SYN-{R4_NUMBERS}"
        assert "FAIL" in syn[0].actual

    def test_passing_rubric_gets_no_promotion_or_synthetic(self):
        llm = MagicMock()
        llm.complete.side_effect = [_sample() for _ in range(5)]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        for rid in PASS_A_RUBRICS:
            assert outcome.results[rid].issues == []
            assert "synthetic_issue" not in outcome.results[rid].info
        assert outcome.corroborated_issues == []

    def test_corroboration_floor_scales_with_valid_samples(self):
        """The live round-3 signature: 3/5 samples unparseable. With 2 valid
        samples agreeing on the same evidence, the issue must corroborate
        (floor scales to 2) instead of demoting to low-confidence."""
        llm = MagicMock()
        llm.complete.side_effect = (
            ["truncated garbage"] * 3
            + [_sample(r4="FAIL", issues=[_issue()]) for _ in range(2)]
        )
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.invalid_samples == 3
        assert len(outcome.samples) == 2
        r4_issues = [i for i in outcome.corroborated_issues if i.rubric == R4_NUMBERS]
        assert len(r4_issues) == 1
        assert outcome.results[R4_NUMBERS].info.get(
            "issues_promoted_for_actionability") is None  # corroborated, not promoted

    def test_invalid_sample_raws_are_captured_for_diagnosis(self):
        llm = MagicMock()
        long_garbage = "x" * 2000  # truncated capture keeps head and tail
        llm.complete.side_effect = [long_garbage] + [_sample() for _ in range(4)]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert len(outcome.invalid_raws) == 1
        assert "…[cut]…" in outcome.invalid_raws[0]
        assert len(outcome.invalid_raws[0]) < 700

    def test_prompt_bounds_issue_count_and_evidence_length(self):
        from core.critic.judge import build_judge_messages
        system = build_judge_messages(PASS_A_RUBRICS, "d", 1, 3)[0]["content"]
        assert "AT MOST 5 issues" in system
        assert "under 200 characters" in system


# ── Deterministic-duplicate discard (2026-07-05 replay 3 regression) ─────────
# The judge's corroborated "numbers-reconcile" issues in live rounds 1 and 3
# were verbatim restatements of the R1/R2 checker output (evidence quoting
# "DETERMINISTIC RESULTS ..."), steering revisions with duplicated and — in
# round 3 — wrong-grammar guidance. Such issues are discarded mechanically.


class TestDeterministicDuplicateDiscard:
    def test_issue_quoting_deterministic_results_is_discarded(self):
        dup = _issue(evidence=(
            "DETERMINISTIC RESULTS shows: regulatory-unknowns-promoted: FAIL "
            "— [BLOCKER] No blocker row references Q4."
        ))
        real = _issue(evidence="Stage 1 sizing stated three ways: 10-12 months, "
                               "12 months, and 3,000 units — figures conflict")
        llm = MagicMock()
        llm.complete.side_effect = [
            _sample(r4="FAIL", issues=[dup, real]) for _ in range(5)
        ]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.duplicate_issues_discarded == 5  # one per sample
        evidences = [i.evidence for i in outcome.corroborated_issues]
        assert any("Stage 1 sizing" in e for e in evidences)
        assert not any("DETERMINISTIC RESULTS" in e for e in evidences)
        assert not any("DETERMINISTIC RESULTS" in i.evidence
                       for i in outcome.low_confidence)

    def test_actual_field_quoting_deterministic_scanner_is_discarded(self):
        dup = _issue(evidence="Line 112: the $6.8M annual budget figure")
        dup["actual"] = "Deterministic scanner reports 25 uncited claims including..."
        llm = MagicMock()
        llm.complete.side_effect = [_sample(r4="FAIL", issues=[dup]) for _ in range(5)]
        outcome = _judge(llm).run(PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        assert outcome.duplicate_issues_discarded == 5
        # verdicts stand (judge's call) — no-silent-zeros still guarantees an
        # actionable payload via the synthetic path.
        assert outcome.results[R4_NUMBERS].score == 0.0
        assert outcome.results[R4_NUMBERS].issues  # synthetic

    def test_r4_rubric_text_sanctions_assumption_and_transcript_figures(self):
        from core.critic.judge import build_judge_messages
        system = build_judge_messages(PASS_A_RUBRICS, "d", 1, 3)[0]["content"]
        assert "SANCTIONED SOURCES" in system
        assert "INTERNAL CONSISTENCY" in system
        assert "never its absence from research" in system
        # the discard mechanism is announced so the judge doesn't waste output
        assert "DISCARDS any issue" in system
