"""Critic Pass B — report↔plan consistency before Stop 2.

T2 drift canary (mechanism level): run 1's ACTUAL execution plan (which calls
the EOL chip "faulty") against its decision report → Pass B must fail R6 with
an issue whose evidence quotes the "faulty" line, and the corrected plan must
pass. The judge is mocked here (lab rule: never run real debates); the
semantic detection itself is verified in the live CY-80L replay (follow-up).

Fixtures are byte-identical copies of the frozen
04-Projects/Agentic-OS/04-evals/baseline-run-1-cy80l-eol/ artifacts.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from core.critic.constants import R6_REPORT_VS_PLAN
from core.critic.pass_b import check_plan_new_claims, run_pass_b
from core.utils.config import CriticConfig

FIXTURES = Path(__file__).parent.parent / "fixtures" / "critic"
RUN1_REPORT = FIXTURES / "baseline-run-1-07-decision-report.md"
RUN1_PLAN = FIXTURES / "baseline-run-1-08-execution-plan.md"

FAULTY_LINE = (
    "We have a faulty chip in our main product (CY-80L) and need to place a "
    "large bulk order fast"
)


def _r6_sample(verdict="PASS", issues=None):
    return json.dumps({
        "rubric_verdicts": {R6_REPORT_VS_PLAN: verdict},
        "overall_score": 1.0 if verdict == "PASS" else 0.2,
        "issues": issues or [],
    })


def _faulty_issue():
    return {
        "id": "ISS-1", "rubric": R6_REPORT_VS_PLAN, "severity": "BLOCKER",
        "expected": "EOL is a lifecycle status, not a defect — no characterization drift.",
        "actual": "The plan calls the end-of-life chip 'faulty'.",
        "evidence": FAULTY_LINE,
        "fix_instruction": "Replace 'faulty chip' with 'end-of-life (EOL) chip'.",
        "files_to_modify": ["08-execution-plan.md"], "confidence": 0.95,
    }


def _make_task(tmp_path: Path, plan_text: str, report_text: str) -> tuple[Path, Path]:
    vault = tmp_path / "vault"
    (vault / "00-Brain").mkdir(parents=True)
    (vault / "00-Brain" / "products.md").write_text("# products\n", encoding="utf-8")
    task = vault / "02-Tasks" / "task-x"
    task.mkdir(parents=True)
    (task / "07-decision-report.md").write_text(report_text, encoding="utf-8")
    (task / "08-execution-plan.md").write_text(plan_text, encoding="utf-8")
    return vault, task


class TestDeterministicNewClaims:
    def test_run1_plan_introduces_one_uncited_new_figure(self, tmp_path):
        """Real baseline evidence: the plan states '10,000' units, absent from
        the report and uncited — a new factual claim without a resolving ref."""
        report = RUN1_REPORT.read_text(encoding="utf-8")
        plan = RUN1_PLAN.read_text(encoding="utf-8")
        result = check_plan_new_claims(plan, report, vault_root=tmp_path)
        assert result.passed is False
        assert result.info["new_figures"] == ["10,000"]
        assert len(result.issues) == 1
        assert "10,000" in result.issues[0].actual

    def test_plan_reusing_only_report_figures_passes(self, tmp_path):
        report = "# R\n\nThe unit sells for $389 with a 39% margin.\n"
        plan = "# P\n\n| 1 | Sell at $389 (39% margin) | Sales | Week 1 | PO |\n"
        result = check_plan_new_claims(plan, report, vault_root=tmp_path)
        assert result.passed is True
        assert result.info["new_figures"] == []

    def test_new_figure_with_resolving_citation_passes(self, tmp_path):
        (tmp_path / "00-Brain").mkdir(parents=True)
        (tmp_path / "00-Brain" / "budget.md").write_text("# b\n", encoding="utf-8")
        report = "# R\n\nThe unit sells for $389.\n"
        plan = "# P\n\nContingency of $25,000 applies [[00-Brain/budget.md]].\n"
        result = check_plan_new_claims(plan, report, vault_root=tmp_path)
        assert result.passed is True

    def test_new_uncited_figure_in_table_row_is_caught(self, tmp_path):
        """The plan template is mostly tables — table rows must be covered."""
        report = "# R\n\nThe unit sells for $389.\n"
        plan = "# P\n\n| 1 | Order 10,000 units | Ops | Week 1 | PO |\n"
        result = check_plan_new_claims(plan, report, vault_root=tmp_path)
        assert result.passed is False
        assert "10,000" in result.issues[0].actual


class TestT2DriftCanary:
    """T2 mechanism: judged R6 failure on the real 'faulty' plan propagates."""

    def test_run1_faulty_plan_fails_r6_with_evidence_quoting_faulty(self, tmp_path):
        report = RUN1_REPORT.read_text(encoding="utf-8")
        plan = RUN1_PLAN.read_text(encoding="utf-8")
        assert "faulty chip" in plan  # the planted defect is really in the fixture
        vault, task = _make_task(tmp_path, plan, report)

        llm = MagicMock()
        # 2 evaluation rounds (initial + 1 fix) × 5 samples, all FAIL with the quote.
        llm.complete.side_effect = [_r6_sample("FAIL", [_faulty_issue()])] * 10
        replan_calls = []

        def replan(revision_md, prior_plan):
            replan_calls.append(revision_md)
            return prior_plan  # plan stays broken → banner

        outcome = run_pass_b(
            task_folder=task, llm=llm, config=CriticConfig(),
            vault_root=vault, replan_fn=replan,
        )

        assert outcome.verdict == "THRESHOLD-NOT-MET"
        assert outcome.banner is True
        assert len(replan_calls) == 1  # max ONE fix round — lightweight by design
        # The revision instruction quotes the 'faulty' evidence (NEXUS format).
        assert "faulty" in replan_calls[0]
        # Scorecard artifact attached at Stop 2.
        scorecard = (task / "08b-critic-scorecard.md").read_text(encoding="utf-8")
        assert "faulty" in scorecard
        assert "THRESHOLD-NOT-MET" in (task / "08-execution-plan.md").read_text(
            encoding="utf-8")

    def test_corrected_plan_passes_as_positive_control(self, tmp_path):
        """T2 positive control: the same plan with 'faulty' → 'EOL' passes."""
        report = RUN1_REPORT.read_text(encoding="utf-8")
        plan = RUN1_PLAN.read_text(encoding="utf-8").replace(
            "a faulty chip", "an end-of-life (EOL) chip"
        ).replace(
            "subtly faulty chips", "subtly out-of-spec chips"
        )
        # Resolve the one genuinely-new figure so the deterministic gate passes too.
        plan = plan.replace(
            "unit pricing and **MOQ**",
            "unit pricing (ref: Q1) and **MOQ**",
        )
        vault, task = _make_task(tmp_path, plan, report)
        (task / "03-clarification.md").write_text(
            "## Q1 [CRITICAL]\n\nWhat is the MOQ?\n\n- [x] A) 10,000\n",
            encoding="utf-8",
        )
        llm = MagicMock()
        llm.complete.side_effect = [_r6_sample("PASS")] * 5

        outcome = run_pass_b(
            task_folder=task, llm=llm, config=CriticConfig(),
            vault_root=vault, replan_fn=MagicMock(),
        )
        assert outcome.verdict == "PASS"
        assert outcome.banner is False
        assert outcome.rounds_used == 1
        assert "THRESHOLD-NOT-MET" not in (task / "08-execution-plan.md").read_text(
            encoding="utf-8")


class TestPassBFixRound:
    def test_fix_round_repairs_plan_and_promotes_clean(self, tmp_path):
        report = "# R\n\n## Recommendation\nGO\n\nThe unit sells for $389.\n"
        bad_plan = "# P\n\n| 1 | Order 10,000 units | Ops | Week 1 | PO |\n"
        good_plan = "# P\n\n| 1 | Order units at $389 | Ops | Week 1 | PO |\n"
        vault, task = _make_task(tmp_path, bad_plan, report)

        llm = MagicMock()
        llm.complete.side_effect = [_r6_sample("PASS")] * 10

        def replan(revision_md, prior_plan):
            (task / "08-execution-plan.md").write_text(good_plan, encoding="utf-8")
            return good_plan

        outcome = run_pass_b(
            task_folder=task, llm=llm, config=CriticConfig(),
            vault_root=vault, replan_fn=replan,
        )
        assert outcome.verdict == "PASS"
        assert outcome.rounds_used == 2
        # Append-only plan draft chain.
        assert (task / "08-execution-plan.draft-r1.md").read_text(
            encoding="utf-8") == bad_plan
        assert (task / "08-execution-plan.draft-r2.md").read_text(
            encoding="utf-8") == good_plan
        assert (task / "08-execution-plan.md").read_text(encoding="utf-8") == good_plan
        # Pass-B guardrail spans carry pass="B".
        events = [json.loads(x) for x in (task / "events.jsonl").read_text(
            encoding="utf-8").splitlines()]
        assert any(e["name"] == f"critic:{R6_REPORT_VS_PLAN}" and e["pass"] == "B"
                   for e in events)
