"""Critic loop (Pass A) — rounds, banner, counter, tier awareness, artifacts.

Covers critic-draft acceptance test T8 (rounds-exhaustion: promoted WITH
THRESHOLD-NOT-MET banner, scorecard attached, counter == 3 never 4, no
infinite loop) plus the §1 loop rules and §5 revision template.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from core.critic.constants import (
    R1_CITATIONS,
    R2_REGULATORY,
    R3_VERDICT,
    R4_NUMBERS,
    R5_DEBATE_SIDES,
    THRESHOLD_NOT_MET_BANNER_HEADER,
)
from core.critic.loop import CriticLoop, read_task_class
from core.utils.config import CriticConfig

CLEAN_DRAFT = """---
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

## To do before launch (BLOCKERS)
- [ ] **Confirm supplier pricing** (ref: Q1). *Owner: Finance. Deadline: Week 2.*
"""

# An uncited figure → R1 (hard gate) fails every round.
BAD_DRAFT = CLEAN_DRAFT.replace(
    "Revenue grew 25% year over year per the Brain. [[00-Brain/budget.md]]",
    "Revenue grew 25% year over year, trust me.",
)


def _judge_sample(r4="PASS", r5="PASS"):
    return json.dumps({
        "rubric_verdicts": {R4_NUMBERS: r4, R5_DEBATE_SIDES: r5},
        "overall_score": 0.9,
        "issues": [],
    })


def _make_task(tmp_path: Path, task_class: str = "COMPLEX") -> tuple[Path, Path]:
    vault = tmp_path / "vault"
    (vault / "00-Brain").mkdir(parents=True)
    for name in ("strategy.md", "budget.md", "products.md"):
        (vault / "00-Brain" / name).write_text(f"# {name}\n", encoding="utf-8")
    task = vault / "02-Tasks" / "task-x"
    task.mkdir(parents=True)
    (task / "01-routing.md").write_text(
        f"---\ntype: routing\n---\n# Task classification\n\n"
        f"- **Class:** {task_class}\n- **Departments:** x\n",
        encoding="utf-8",
    )
    (task / "03-clarification.md").write_text(
        "---\ntype: clarification\n---\n\n## Q1 [CRITICAL]\n_Cite: 00-Brain/products.md_\n\n"
        "What is the unit price?\n\n- [x] A) $389\n",
        encoding="utf-8",
    )
    return vault, task


def _loop(vault: Path, llm=None, **cfg_overrides) -> CriticLoop:
    llm = llm or MagicMock()
    # Mechanics tests exercise the multi-round loop, so they pin max_rounds=3
    # explicitly. The SHIPPED default is 1 (Brian's 2026-07-06 ruling: score once,
    # no revision loop; failures reach Stop 1 bannered) — asserted in
    # TestShippedDefaults below.
    cfg_overrides.setdefault("max_rounds", 3)
    config = CriticConfig(**cfg_overrides)
    return CriticLoop(llm=llm, config=config, vault_root=vault)


class TestShippedDefaults:
    def test_pass_a_default_is_single_round(self):
        assert CriticConfig().max_rounds == 1

    def test_single_round_failure_promotes_with_banner_no_revision(self, tmp_path):
        vault, task = _make_task(tmp_path)
        revise = MagicMock()
        outcome = _loop(vault, max_rounds=1).run_pass_a(task, BAD_DRAFT, revise)
        assert outcome.verdict == "THRESHOLD-NOT-MET"
        assert outcome.banner is True
        revise.assert_not_called()


class TestCleanPass:
    def test_clean_draft_promotes_in_round_one(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(5)]
        revise = MagicMock()

        outcome = _loop(vault, llm).run_pass_a(task, CLEAN_DRAFT, revise)

        assert outcome.verdict == "PASS"
        assert outcome.banner is False
        assert outcome.rounds_used == 1
        revise.assert_not_called()
        # Promotion = COPY of the passing draft (append-only chain).
        assert (task / "07-decision-report.md").read_text(encoding="utf-8") == CLEAN_DRAFT
        assert (task / "07-decision-report.draft-r1.md").exists()
        # Every promotion attaches the scorecard — the human never sees an unscored draft.
        assert (task / "07b-critic-scorecard.md").exists()
        assert (task / "critic" / "final-scorecard.md").exists()
        assert (task / "critic" / "round-1-scorecard.json").exists()
        state = json.loads((task / "critic" / "state.json").read_text(encoding="utf-8"))
        assert state["final_verdict"] == "PASS"
        assert state["round"] == 1

    def test_guardrail_spans_one_per_rubric_per_round(self, tmp_path):
        """T1 telemetry slice: events.jsonl has one guardrail span per rubric per round."""
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(5)]
        _loop(vault, llm).run_pass_a(task, CLEAN_DRAFT, MagicMock())

        events = [
            json.loads(line)
            for line in (task / "events.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        guardrails = [e for e in events if e["span"] == "guardrail" and e.get("round") == 1]
        names = {e["name"] for e in guardrails}
        for rid in (R1_CITATIONS, R2_REGULATORY, R3_VERDICT, R4_NUMBERS, R5_DEBATE_SIDES):
            assert f"critic:{rid}" in names
        assert "critic" in names  # the round's aggregate decision span
        # ADR-003 §2 contract: triggered=False on a passing rubric
        r1_span = next(e for e in guardrails if e["name"] == f"critic:{R1_CITATIONS}")
        assert r1_span["triggered"] is False
        # generation spans per judge sample (C6 dual budget)
        gens = [e for e in events if e["span"] == "generation"]
        assert len(gens) == 5
        # audit tuple per round (ADR-003 §3)
        audits = (task / "audit.jsonl").read_text(encoding="utf-8").splitlines()
        assert len(audits) == 1
        audit = json.loads(audits[0])
        assert audit["caller"] == "critic"
        assert "input_hash" in audit and "output_hash" in audit


class TestRoundsExhaustion:
    def test_t8_persistent_failure_promotes_with_banner_after_three_rounds(self, tmp_path):
        """T8: draft engineered to keep failing R1 → promoted, bannered, counter==3."""
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(5 * 3)]
        revise = MagicMock(side_effect=lambda instruction, prior: BAD_DRAFT)

        outcome = _loop(vault, llm).run_pass_a(task, BAD_DRAFT, revise)

        assert outcome.verdict == "THRESHOLD-NOT-MET"
        assert outcome.banner is True
        assert outcome.rounds_used == 3
        assert revise.call_count == 2  # rounds 1→2 and 2→3; round 3 exhausts
        # Draft IS promoted (never blocked forever), banner + scorecard attached.
        final = (task / "07-decision-report.md").read_text(encoding="utf-8")
        assert THRESHOLD_NOT_MET_BANNER_HEADER in final
        assert R1_CITATIONS in final  # the failing rubric named in the banner
        assert (task / "07b-critic-scorecard.md").exists()
        # Counter == 3, never 4 (increment only when continuing).
        state = json.loads((task / "critic" / "state.json").read_text(encoding="utf-8"))
        assert state["round"] == 3
        assert state["final_verdict"] == "THRESHOLD-NOT-MET"
        assert [h["round"] for h in state["history"]] == [1, 2, 3]
        # Append-only draft chain: one file per round, revisions for 1 and 2 only.
        for n in (1, 2, 3):
            assert (task / f"07-decision-report.draft-r{n}.md").exists()
        assert (task / "critic" / "round-1-revision.md").exists()
        assert (task / "critic" / "round-2-revision.md").exists()
        assert not (task / "critic" / "round-3-revision.md").exists()

    def test_banner_inserted_after_frontmatter(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(15)]
        outcome = _loop(vault, llm).run_pass_a(
            task, BAD_DRAFT, MagicMock(side_effect=lambda i, p: BAD_DRAFT)
        )
        lines = outcome.final_report_text.splitlines()
        assert lines[0] == "---"  # frontmatter intact at the top
        banner_idx = lines.index(THRESHOLD_NOT_MET_BANNER_HEADER)
        assert banner_idx < 10  # banner right after the frontmatter block


class TestRevisionRound:
    def test_failing_then_fixed_draft_promotes_clean_in_round_two(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(10)]
        revise = MagicMock(side_effect=lambda instruction, prior: CLEAN_DRAFT)

        outcome = _loop(vault, llm).run_pass_a(task, BAD_DRAFT, revise)

        assert outcome.verdict == "PASS"
        assert outcome.banner is False
        assert outcome.rounds_used == 2
        assert revise.call_count == 1
        assert (task / "07-decision-report.md").read_text(encoding="utf-8") == CLEAN_DRAFT
        state = json.loads((task / "critic" / "state.json").read_text(encoding="utf-8"))
        assert state["round"] == 2
        assert state["history"][0]["verdict"] == "REVISE"
        assert state["history"][1]["verdict"] == "PASS"
        # §3 history shape: blocking bools + judged scores + aggregate.
        # Round 1 failed a hard gate → judged was short-circuited (v2.1) and
        # the audit trail says so honestly; round 2 (gates green) carries the
        # judged scores — a PASS always comes from a fully-judged round.
        h1, h2 = state["history"][0], state["history"][1]
        assert h1["blocking"][R1_CITATIONS] is False
        assert h1["judged"] == "skipped (gates failed)"
        assert h1["aggregate"] is None
        assert h1["draft"] == "07-decision-report.draft-r1.md"
        assert h2["judged"][R4_NUMBERS] == 1.0
        assert h2["aggregate"] == 1.0

    def test_revision_instruction_follows_the_template(self, tmp_path):
        """§5: score+iteration header, fix-only rules, NEXUS issue blocks."""
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(10)]
        captured = {}

        def revise(instruction, prior):
            captured["instruction"] = instruction
            return CLEAN_DRAFT

        _loop(vault, llm).run_pass_a(task, BAD_DRAFT, revise)

        md = captured["instruction"]
        assert "# REVISION INSTRUCTION — round 1 of 3" in md
        assert "threshold 0.6" in md
        assert f"Blocking failures: {R1_CITATIONS}" in md
        assert "FIX ONLY" in md
        assert "PRESERVE what passed" in md
        assert "ASSUMPTION:" in md  # cite-or-delete escape hatch (ruling Q2)
        assert "NEW draft" in md
        # NEXUS per-issue format
        assert "- **Expected:**" in md
        assert "- **Actual:**" in md
        assert "- **Evidence:**" in md
        assert "- **Fix:**" in md
        assert "25%" in md  # the uncited claim is quoted as evidence
        # Persisted copy in the task folder
        assert (task / "critic" / "round-1-revision.md").read_text(
            encoding="utf-8") == md


class TestJudgedGating:
    def test_judged_high_confidence_fail_blocks_even_when_hard_gates_pass(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        # Round 1: R4 fails 5/5 → REVISE; round 2: all pass.
        llm.complete.side_effect = (
            [_judge_sample(r4="FAIL") for _ in range(5)]
            + [_judge_sample() for _ in range(5)]
        )
        revise = MagicMock(side_effect=lambda i, p: CLEAN_DRAFT)
        outcome = _loop(vault, llm).run_pass_a(task, CLEAN_DRAFT, revise)
        assert outcome.rounds_used == 2
        assert revise.call_count == 1

    def test_aggregate_below_threshold_blocks(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        # Both rubrics 3/5 FAIL → each 0.4 → aggregate 0.4 < 0.6 → REVISE.
        round1 = (
            [_judge_sample(r4="FAIL", r5="FAIL") for _ in range(3)]
            + [_judge_sample() for _ in range(2)]
        )
        llm.complete.side_effect = round1 + [_judge_sample() for _ in range(5)]
        revise = MagicMock(side_effect=lambda i, p: CLEAN_DRAFT)
        outcome = _loop(vault, llm).run_pass_a(task, CLEAN_DRAFT, revise)
        assert outcome.rounds_used == 2

    def test_single_rubric_split_failure_does_not_block(self, tmp_path):
        """Ruling Q4 anti-churn: one rubric at 3/5 FAIL → aggregate 0.7 → PASS."""
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = (
            [_judge_sample(r4="FAIL") for _ in range(3)]
            + [_judge_sample() for _ in range(2)]
        )
        outcome = _loop(vault, llm).run_pass_a(task, CLEAN_DRAFT, MagicMock())
        assert outcome.verdict == "PASS"
        assert outcome.rounds_used == 1


class TestTierAwareness:
    """ADR-003 Addendum B: read the tier, don't hardcode it."""

    def test_simple_task_skips_the_critic(self, tmp_path):
        vault, task = _make_task(tmp_path, task_class="SIMPLE")
        assert _loop(vault).should_run(task) is False

    def test_complex_and_strategic_require_the_critic(self, tmp_path):
        for cls in ("COMPLEX", "STRATEGIC"):
            vault, task = _make_task(tmp_path / cls.lower(), task_class=cls)
            assert _loop(vault).should_run(task) is True

    def test_missing_routing_fails_closed_to_running_the_critic(self, tmp_path):
        vault, task = _make_task(tmp_path)
        (task / "01-routing.md").unlink()
        assert read_task_class(task) is None
        assert _loop(vault).should_run(task) is True  # fail-closed UNKNOWN (ADR-003 §2)

    def test_apply_to_classes_is_policy_data_not_code(self, tmp_path):
        vault, task = _make_task(tmp_path, task_class="SIMPLE")
        loop = _loop(vault, apply_to_classes=["SIMPLE", "COMPLEX", "STRATEGIC"])
        assert loop.should_run(task) is True
        vault2, task2 = _make_task(tmp_path / "b", task_class="STRATEGIC")
        loop2 = _loop(vault2, apply_to_classes=["STRATEGIC"])
        assert loop2.should_run(task2) is True
        vault3, task3 = _make_task(tmp_path / "c", task_class="COMPLEX")
        loop3 = _loop(vault3, apply_to_classes=["STRATEGIC"])
        assert loop3.should_run(task3) is False

    def test_disabled_critic_never_runs(self, tmp_path):
        vault, task = _make_task(tmp_path, task_class="STRATEGIC")
        assert _loop(vault, enabled=False).should_run(task) is False


class TestResumeIdempotency:
    def test_existing_draft_file_is_rescored_not_overwritten(self, tmp_path):
        """§1 rule 1: re-scoring on resume is idempotent (same pause_id discipline)."""
        vault, task = _make_task(tmp_path)
        # Simulate a crash after draft-r1 was written: the persisted draft wins.
        (task / "07-decision-report.draft-r1.md").write_text(CLEAN_DRAFT, encoding="utf-8")
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(5)]
        outcome = _loop(vault, llm).run_pass_a(task, BAD_DRAFT, MagicMock())
        # The persisted (clean) draft was scored, not the passed-in bad draft.
        assert outcome.verdict == "PASS"
        assert (task / "07-decision-report.md").read_text(encoding="utf-8") == CLEAN_DRAFT

    def test_rescoring_a_round_replaces_its_history_entry(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(10)]
        loop = _loop(vault, llm)
        loop.run_pass_a(task, CLEAN_DRAFT, MagicMock())
        # Run again (resume): round 1 history must not duplicate.
        llm.complete.side_effect = [_judge_sample() for _ in range(5)]
        loop.run_pass_a(task, CLEAN_DRAFT, MagicMock())
        state = json.loads((task / "critic" / "state.json").read_text(encoding="utf-8"))
        assert [h["round"] for h in state["history"]] == [1]


class TestMonotonicNonRegressionGuard:
    """2026-07-05 replay-4 ruling: deterministic gates make monotonic progress.
    A revision that breaks a previously-passing gate is retried once with an
    explicit regression warning, then rejected in favor of the prior draft."""

    def test_regressing_revision_is_retried_then_rejected(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        # Judged R4 fails every round (drives REVISE); citations green in draft.
        llm.complete.side_effect = [_judge_sample(r4="FAIL") for _ in range(15)]
        # The Synthesizer keeps returning a draft that LOSES citations.
        revise = MagicMock(side_effect=lambda instruction, prior: BAD_DRAFT)

        outcome = _loop(vault, llm).run_pass_a(task, CLEAN_DRAFT, revise)

        assert outcome.verdict == "THRESHOLD-NOT-MET"  # judged never fixed
        # 2 revise calls per continuing round (attempt + retry) × 2 rounds.
        assert revise.call_count == 4
        retry_instruction = revise.call_args_list[1].args[0]
        assert "REGRESSION REJECTED" in retry_instruction
        assert R1_CITATIONS in retry_instruction
        # Monotonicity: the regressing drafts were rejected — every scored
        # round kept citations green.
        state = json.loads((task / "critic" / "state.json").read_text(encoding="utf-8"))
        for entry in state["history"]:
            assert entry["blocking"][R1_CITATIONS] is True
        guard = state["regression_guard"]
        assert [g["action"] for g in guard] == ["fallback_to_prior_draft"] * 2
        assert guard[0]["regressed_first_attempt"] == [R1_CITATIONS]
        # The kept drafts are the prior (green) draft, not the regression.
        for n in (2, 3):
            assert (task / f"07-decision-report.draft-r{n}.md").read_text(
                encoding="utf-8") == CLEAN_DRAFT
        # Observable: non-regression guardrail spans emitted.
        events = [json.loads(x) for x in (task / "events.jsonl").read_text(
            encoding="utf-8").splitlines()]
        spans = [e for e in events if e.get("name") == "critic:non-regression"]
        assert len(spans) == 2 and all(e["triggered"] for e in spans)

    def test_retry_that_restores_the_gate_is_accepted(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        # Round 1: R4 fails → REVISE. Round 2: all pass → PASS.
        llm.complete.side_effect = (
            [_judge_sample(r4="FAIL") for _ in range(5)]
            + [_judge_sample() for _ in range(5)]
        )
        revise = MagicMock(side_effect=[BAD_DRAFT, CLEAN_DRAFT])

        outcome = _loop(vault, llm).run_pass_a(task, CLEAN_DRAFT, revise)

        assert outcome.verdict == "PASS"
        assert outcome.rounds_used == 2
        assert revise.call_count == 2  # attempt regressed, retry accepted
        state = json.loads((task / "critic" / "state.json").read_text(encoding="utf-8"))
        assert state["regression_guard"][0]["action"] == "retry_succeeded"
        assert (task / "07-decision-report.draft-r2.md").read_text(
            encoding="utf-8") == CLEAN_DRAFT

    def test_non_regressing_revision_needs_no_retry(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = (
            [_judge_sample(r4="FAIL") for _ in range(5)]
            + [_judge_sample() for _ in range(5)]
        )
        revise = MagicMock(side_effect=[CLEAN_DRAFT])
        outcome = _loop(vault, llm).run_pass_a(task, CLEAN_DRAFT, revise)
        assert outcome.verdict == "PASS"
        assert revise.call_count == 1  # no retry spent
        state = json.loads((task / "critic" / "state.json").read_text(encoding="utf-8"))
        assert "regression_guard" not in state
