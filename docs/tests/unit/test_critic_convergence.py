"""Convergence regressions from the 2026-07-05 live CY-80L replay.

The live run failed to converge (3 rounds, byte-identical blocking failures)
for a compound reason no unit test covered:
  1. the prompt the meeting flow ACTUALLY sends to the Synthesizer carried the
     conventions only as soft bullets, and BaseAgent's default REQUEST said
     "state your perspective (in plain English)";
  2. the translator (simplifier/TLDR) rewrote machine markers after the
     Synthesizer, every round;
  3. the judge — never told the canonical scale or citation grammar — invented
     "GO-CONDITIONAL | DEFER" and suggested citation formats the scanner
     rejects, and its issues were ordered BEFORE the deterministic hard gates.

These tests pin every link of that chain.
"""
from __future__ import annotations

import json
from unittest.mock import MagicMock

from core.critic.constants import (
    ACCEPTED_GRAMMAR,
    CANONICAL_VERDICTS,
    R4_NUMBERS,
    R5_DEBATE_SIDES,
)
from core.critic.judge import PASS_A_RUBRICS, build_judge_messages
from core.critic.loop import CriticLoop
from core.meeting.debate_state import new_meeting_state
from core.meeting.synthesizer import Synthesizer
from core.translator.simplifier import SIMPLIFIER_PROMPT
from core.translator.tldr_generator import TLDR_PROMPT
from core.utils.config import CriticConfig

from tests.unit.test_critic_loop import (  # reuse the loop harness
    CLEAN_DRAFT,
    _judge_sample,
    _make_task,
)


# ── 1. The prompt the meeting flow ACTUALLY executes ─────────────────────────


class TestSynthesizerPromptAsExecuted:
    """Render the exact messages the live meeting path sends (Synthesizer.run
    → BaseAgent.speak → llm.complete) and assert the contract is in them —
    not merely that the text exists somewhere in the module."""

    def _captured_messages(self):
        llm = MagicMock()
        llm.complete.return_value = "report"
        syn = Synthesizer(llm=llm)
        state = new_meeting_state(brief="EOL brief", departments=["05-service-operations"])
        state["perspectives"] = {"05-service-operations": "OK"}
        state["pro_con_debate"]["history"] = ["PRO", "CON"]
        state["perspective_debate"]["history"] = ["G", "C", "B"]
        syn.run(state)
        return llm.complete.call_args.args[0]

    def test_system_prompt_carries_the_machine_checked_contract(self):
        messages = self._captured_messages()
        system = messages[0]["content"]
        assert "MACHINE-CHECKED OUTPUT CONTRACT" in system
        for tier in CANONICAL_VERDICTS:
            assert tier in system
        # the exact grammar block, verbatim (single source of truth)
        assert ACCEPTED_GRAMMAR in system
        assert "(ref: Q<n>)" in system
        assert "ASSUMPTION:" in system
        assert "(uncitable:" in system
        # anti-patterns the live run produced are called out by name
        assert "GO-CONDITIONAL" in system  # named as forbidden
        assert "[ASSUMPTION]" in system    # inline markers named as rejected

    def test_request_line_demands_the_contract_not_a_perspective(self):
        messages = self._captured_messages()
        user = messages[1]["content"]
        assert "State your perspective" not in user
        assert "MACHINE-CHECKED OUTPUT CONTRACT" in user
        assert "decision report" in user

    def test_revision_turn_carries_the_same_contract(self):
        llm = MagicMock()
        llm.complete.return_value = "revised"
        syn = Synthesizer(llm=llm)
        syn.revise("prior draft", "revision instruction")
        messages = llm.complete.call_args.args[0]
        assert "MACHINE-CHECKED OUTPUT CONTRACT" in messages[0]["content"]
        assert "## Recommendation" in messages[1]["content"]  # heading-stability rule


# ── 2. The translator must not destroy machine markers ──────────────────────


class TestTranslatorPreservation:
    def test_simplifier_prompt_orders_marker_preservation(self):
        assert "PRESERVE MACHINE MARKERS" in SIMPLIFIER_PROMPT
        assert "GO-WITH-CONDITIONS" in SIMPLIFIER_PROMPT
        assert "(ref: Q<n>)" in SIMPLIFIER_PROMPT
        assert "ASSUMPTION:" in SIMPLIFIER_PROMPT
        # the exact live failure is named so the editor model sees the stakes
        assert "Approved — with conditions" in SIMPLIFIER_PROMPT

    def test_tldr_prompt_forbids_uncited_figures(self):
        assert "citation marker" in TLDR_PROMPT
        assert "Never introduce a figure" in TLDR_PROMPT


# ── 3. The judge is told the grammar it may suggest ──────────────────────────


class TestJudgePromptGrammar:
    def test_judge_system_prompt_contains_canonical_scale_and_grammar(self):
        messages = build_judge_messages(PASS_A_RUBRICS, "draft", 1, 3)
        system = messages[0]["content"]
        assert ACCEPTED_GRAMMAR in system
        for tier in CANONICAL_VERDICTS:
            assert tier in system
        # the live run's wrong suggestions are named as forbidden
        assert "GO-CONDITIONAL" in system
        assert "(Dept 01 position paper)" in system
        assert "(Q1 answer)" in system

    def test_judge_is_told_not_to_duplicate_deterministic_findings(self):
        messages = build_judge_messages(PASS_A_RUBRICS, "draft", 1, 3)
        assert "DO NOT DUPLICATE DETERMINISTIC FINDINGS" in messages[0]["content"]


# ── 4. Revision instruction: hard gates first, grammar echoed, capped ───────

BAD_VERDICT_DRAFT = CLEAN_DRAFT.replace(
    "GO-WITH-CONDITIONS",
    "Cautiously optimistic, monitor closely.",
)


class TestRevisionInstructionStructure:
    def _revision_md(self, tmp_path, draft):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(15)]
        captured = []

        def revise(instruction, prior):
            captured.append(instruction)
            return draft  # never fixes anything

        # max_rounds=3 pinned: these tests inspect revision instructions across
        # rounds (shipped default is 1 round since 2026-07-06)
        loop = CriticLoop(llm=llm, config=CriticConfig(max_rounds=3),
                          vault_root=vault)
        loop.run_pass_a(task, draft, revise)
        return captured, task

    def test_hard_gates_come_before_rules_and_judged_issues(self, tmp_path):
        captured, _ = self._revision_md(tmp_path, BAD_VERDICT_DRAFT)
        md = captured[0]
        gate_pos = md.index("⛔ HARD GATES")
        grammar_pos = md.index("REQUIRED GRAMMAR")
        rules_pos = md.index("## Rules")
        assert gate_pos < grammar_pos < rules_pos
        # explicit rejected-again preamble (goal B(i))
        assert "WILL be\nrejected again" in md or "WILL be rejected again" in md.replace(
            "\n", " ")

    def test_grammar_block_is_echoed_verbatim_in_every_revision(self, tmp_path):
        captured, _ = self._revision_md(tmp_path, BAD_VERDICT_DRAFT)
        assert len(captured) == 2  # rounds 1→2, 2→3
        for md in captured:
            assert ACCEPTED_GRAMMAR in md

    def test_repetitive_r1_findings_are_capped_with_apply_to_all_note(self, tmp_path):
        # 9 uncited claim lines → more than the 6-example cap
        uncited = "\n".join(
            f"The projected saving for area {n} is ${n}00,000 next quarter."
            for n in range(1, 10)
        )
        draft = CLEAN_DRAFT + "\n" + uncited + "\n"
        captured, _ = self._revision_md(tmp_path, draft)
        md = captured[0]
        assert md.count("### R1-") == 6  # capped at _MAX_EXAMPLES_PER_RUBRIC
        assert "more finding(s) of the SAME kind" in md
        assert "EVERY remaining instance" in md

    def test_ignoring_the_verdict_issue_fails_again_with_the_same_issue_id(
        self, tmp_path
    ):
        """Goal C: a revision that ignores the verdict-line issue must fail the
        next round with the SAME issue id — pinning the livelock signature."""
        captured, task = self._revision_md(tmp_path, BAD_VERDICT_DRAFT)
        assert len(captured) == 2
        for md in captured:  # both rounds report the identical unfixed gate
            assert "### R3-1 · verdict-uses-canonical-scale · BLOCKER" in md
        state = json.loads(
            (task / "critic" / "state.json").read_text(encoding="utf-8")
        )
        for entry in state["history"]:
            assert entry["blocking"]["verdict-uses-canonical-scale"] is False
        assert state["final_verdict"] == "THRESHOLD-NOT-MET"

    def test_judged_issue_cap(self, tmp_path):
        """Corroborated judged issues are capped so the Synthesizer is never
        buried under 19 issue blocks again."""
        vault, task = _make_task(tmp_path)
        many_issues = [
            {
                "id": f"ISS-{n}", "rubric": R4_NUMBERS, "severity": "MAJOR",
                "expected": "e", "actual": f"defect {n}",
                "evidence": f"unique evidence token {n} zzz{n}",
                "fix_instruction": "fix", "files_to_modify": [], "confidence": 0.9,
            }
            for n in range(1, 13)
        ]
        sample = json.dumps({
            "rubric_verdicts": {R4_NUMBERS: "FAIL", R5_DEBATE_SIDES: "FAIL"},
            "overall_score": 0.1,
            "issues": many_issues,
        })
        llm = MagicMock()
        llm.complete.side_effect = [sample] * 15
        captured = []

        def revise(instruction, prior):
            captured.append(instruction)
            return CLEAN_DRAFT.replace("GO-WITH-CONDITIONS", "NO-GO")  # still judged-failed

        # max_rounds=3 pinned: a revision instruction requires a second round
        loop = CriticLoop(llm=llm, config=CriticConfig(max_rounds=3),
                          vault_root=vault)
        loop.run_pass_a(task, CLEAN_DRAFT, revise)
        md = captured[0]
        assert md.count("### ISS-") <= CriticLoop._MAX_JUDGED_ISSUES


# ── Serialized scorecard invariants (2026-07-05 replay 3) ────────────────────
# The no-silent-zeros invariant was previously tested at the RubricResult
# level only; replay 3's coordinator audit parsed the WRITTEN JSON and (due to
# the dict-keyed `judged` field) concluded issues were missing. These tests
# pin the invariant on the file actually written to disk, and the schema
# itself is now documented in critic-draft §7.


class TestSerializedScorecardInvariants:
    def test_failing_judged_rubric_carries_issues_in_the_written_json(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        # R4 fails 5/5 with a real (non-duplicate) issue every sample.
        fail_sample = json.dumps({
            "rubric_verdicts": {R4_NUMBERS: "FAIL", R5_DEBATE_SIDES: "PASS"},
            "overall_score": 0.4,
            "issues": [{
                "id": "ISS-1", "rubric": R4_NUMBERS, "severity": "MAJOR",
                "expected": "figures agree", "actual": "Stage 1 sizing conflicts",
                "evidence": "10-12 months vs 12 months vs 3,000 units",
                "fix_instruction": "reconcile the sizing", "files_to_modify": [],
                "confidence": 0.9,
            }],
        })
        llm.complete.side_effect = [fail_sample] * 15
        # max_rounds=3 pinned: asserts the written scorecard for all 3 rounds
        loop = CriticLoop(llm=llm, config=CriticConfig(max_rounds=3),
                          vault_root=vault)
        loop.run_pass_a(task, CLEAN_DRAFT, MagicMock(side_effect=lambda i, p: CLEAN_DRAFT))

        for n in (1, 2, 3):
            written = json.loads(
                (task / "critic" / f"round-{n}-scorecard.json").read_text(
                    encoding="utf-8")
            )
            # documented schema: judged is a dict keyed by rubric id; each
            # value repeats rubric_id and carries the issues.
            assert isinstance(written["judged"], dict)
            nr = written["judged"][R4_NUMBERS]
            assert nr["rubric_id"] == R4_NUMBERS
            assert nr["score"] < 1.0
            assert len(nr["issues"]) >= 1  # no silent zeros — ON DISK
            assert written["corroborated_issues"]
            assert "duplicate_issues_discarded" in written
            assert "invalid_sample_raws" in written

    def test_revision_rules_allow_restoring_required_sections(self, tmp_path):
        """Replay 3 conflict: FIX ONLY forbade adding sections while the R2 fix
        demanded a blocker row in a section that did not exist."""
        captured, _ = TestRevisionInstructionStructure()._revision_md(
            tmp_path, BAD_VERDICT_DRAFT)
        assert "EXCEPTION" in captured[0]
        assert "never new scope" in captured[0]
