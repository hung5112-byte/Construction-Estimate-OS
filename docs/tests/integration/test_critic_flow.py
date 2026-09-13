"""Integration: critic loop wired into FlowController (Pass A + Pass B).

Mocked LLM throughout (lab rule: merge code never data, no real debates).
Verifies: tier-gated activation, draft/scorecard artifacts, Synthesizer-only
revision wiring, legacy warning path preserved when the critic is skipped,
and Pass B running inside approve_decision.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock

from core.critic.constants import R4_NUMBERS, R5_DEBATE_SIDES, R6_REPORT_VS_PLAN
from core.orchestrator.flow_controller import FlowController, FlowStage

REPO = Path(__file__).parent.parent.parent
FIXTURE = REPO / "tests/fixtures/hardwareco-vault"

DEPARTMENTS = ["02-npi-program-management", "05-service-operations"]

CLEAN_SYNTH_REPORT = """## 📌 Bottom line (30-second read)
- Pilot the deployment in two waves, gated by acceptance sign-off. [state.md]

## Recommendation
PROCEED-WITH-REVISIONS

## Detailed analysis
Fleet return rate is 2.8% against the 3% goal. [state.md]

## To do before launch (BLOCKERS)
- [ ] **Scope the PT500 re-certification path** (ref: Q1). *Owner: 02-npi-program-management. Deadline: Week 1.*
"""

# An uncited figure + hedged verdict → R1 and R3 hard gates both fail.
BAD_SYNTH_REPORT = """## 📌 Bottom line (30-second read)
- Ship it, mostly.

## Recommendation
Cautiously optimistic, monitor closely.

## Detailed analysis
Fleet return rate is 2.8% against the 3% goal, trust me.
"""

CLEAN_PLAN = """---
type: execution_plan
stop: 2
---
# Execution plan

## Tasks

| # | Task | Owner dept | Due | Deliverable |
|---|------|-----------|-----|-------------|
| 1 | Scope the PT500 re-certification path | 02-npi-program-management | Week 1 | Cert scope memo |

## Success metrics (KPI)

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Fleet return rate | 2.8% | ongoing |
"""


def _judge_pass():
    return json.dumps({
        "rubric_verdicts": {R4_NUMBERS: "PASS", R5_DEBATE_SIDES: "PASS",
                            R6_REPORT_VS_PLAN: "PASS"},
        "overall_score": 0.95,
        "issues": [],
    })


def _make_llm(synth_first: str, synth_revised: str | None = None):
    """Dispatching mock in the e2e-suite style — keyed off the system prompt."""
    state = {"synth_calls": 0}

    def respond(messages, model=None):
        sys_text = messages[0]["content"]
        user_text = messages[1]["content"] if len(messages) > 1 else ""
        if "You are the CRITIC" in sys_text:
            return _judge_pass()
        if "Tool Router" in sys_text:
            return json.dumps({"tools": []})
        if "coordinates the execution plan" in sys_text:
            return CLEAN_PLAN
        if "write the decision report" in sys_text:
            if "REVISION INSTRUCTION FROM THE CRITIC" in user_text:
                return synth_revised or synth_first
            state["synth_calls"] += 1
            return synth_first
        if "business editor" in sys_text:
            return user_text
        if "Summarize the report" in sys_text:
            return "## 📌 Bottom line (30-second read)\n- summary\n"
        return "Perspective: proceed carefully, per the Brain."

    llm = MagicMock()
    llm.complete.side_effect = respond
    return llm


def _make_task(vault: Path, task_class: str = "COMPLEX") -> Path:
    task = vault / "02-Tasks" / "critic-task"
    task.mkdir(parents=True)
    (task / "00-brief.md").write_text(
        "---\ntype: brief\n---\n# Brief\n\nPilot deployment decision\n",
        encoding="utf-8",
    )
    (task / "01-routing.md").write_text(
        f"---\ntype: routing\n---\n# Task classification\n\n"
        f"- **Class:** {task_class}\n- **Departments:** {', '.join(DEPARTMENTS)}\n",
        encoding="utf-8",
    )
    (task / "03-clarification.md").write_text(
        "---\ntype: clarification\n---\n\n"
        "## Q1 [CRITICAL]\n_Cite: 00-Brain/laws.md_\n_Tags: certification_\n\n"
        "Is the PT500 re-certification budgeted?\n\n"
        "- [x] C) Not previously considered\n",
        encoding="utf-8",
    )
    return task


def _setup(tmp_path, task_class="COMPLEX"):
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURE, vault)
    (vault / "02-Tasks").mkdir(exist_ok=True)
    task = _make_task(vault, task_class)
    return vault, task


class TestPassAWiring:
    def test_complex_task_runs_critic_and_promotes_clean(self, tmp_path):
        vault, task = _setup(tmp_path)
        llm = _make_llm(CLEAN_SYNTH_REPORT)
        fc = FlowController(vault_root=vault, llm=llm)

        result = fc.run_meeting(task, departments=DEPARTMENTS)

        assert result.stage == FlowStage.PAUSE_DECISION_REPORT
        assert "Critic: PASS after 1 round(s)" in result.message
        report = (task / "07-decision-report.md").read_text(encoding="utf-8")
        assert "PROCEED-WITH-REVISIONS" in report
        # Ruling Q2: the warning section is dead on the critic path.
        assert "claims missing a source" not in report
        assert (task / "07-decision-report.draft-r1.md").exists()
        assert (task / "07b-critic-scorecard.md").exists()
        assert (task / "critic" / "state.json").exists()
        assert (task / "events.jsonl").exists()

    def test_failing_draft_is_revised_by_the_synthesizer_only(self, tmp_path):
        """Ruling Q3: revision goes to the Synthesizer only — no debate re-open.

        The shipped default is max_rounds=1 (2026-07-06 ruling), so this test
        raises the cap via the vault .bd-os.yaml — the documented per-vault
        escape hatch — to exercise the revision wiring.
        """
        vault, task = _setup(tmp_path)
        (vault / ".bd-os.yaml").write_text(
            "critic:\n  max_rounds: 3\n", encoding="utf-8"
        )
        llm = _make_llm(BAD_SYNTH_REPORT, synth_revised=CLEAN_SYNTH_REPORT)
        fc = FlowController(vault_root=vault, llm=llm)

        result = fc.run_meeting(task, departments=DEPARTMENTS)

        assert result.stage == FlowStage.PAUSE_DECISION_REPORT
        assert "Critic: PASS after 2 round(s)" in result.message
        state = json.loads((task / "critic" / "state.json").read_text(encoding="utf-8"))
        assert [h["verdict"] for h in state["history"]] == ["REVISE", "PASS"]
        assert (task / "critic" / "round-1-revision.md").exists()
        # The promoted report is the revised (clean) one.
        report = (task / "07-decision-report.md").read_text(encoding="utf-8")
        assert "PROCEED-WITH-REVISIONS" in report
        assert "Cautiously optimistic" not in report

    def test_regulatory_unknown_is_promoted_by_the_skeleton_in_round_one(self, tmp_path):
        """T3 as a build-time invariant (2026-07-05 replay-4 ruling): the
        engine assembles the missing blocker row from the clarification data —
        the certification-tagged 'not previously considered' answer lands in
        blockers with (ref: Q1) and honest TBD owner/deadline, round 1, no
        revision cycle spent on structure."""
        vault, task = _setup(tmp_path)
        # Clean report EXCEPT the blocker row for Q1 is missing — previously a
        # full revision round; now repaired in code before scoring.
        no_blocker = CLEAN_SYNTH_REPORT.replace(
            "- [ ] **Scope the PT500 re-certification path** (ref: Q1). "
            "*Owner: 02-npi-program-management. Deadline: Week 1.*",
            "- [ ] **Confirm spares pool.** *Owner: Ops. Deadline: Week 1.*",
        )
        llm = _make_llm(no_blocker)
        fc = FlowController(vault_root=vault, llm=llm)

        result = fc.run_meeting(task, departments=DEPARTMENTS)

        assert "Critic: PASS after 1 round(s)" in result.message
        report = (task / "07-decision-report.md").read_text(encoding="utf-8")
        assert "(ref: Q1)" in report
        assert "TBD — assign at Stop 1" in report  # honest default, visible at Stop 1
        # R2 never triggered — invariant, not luck.
        events = [json.loads(x) for x in (task / "events.jsonl").read_text(
            encoding="utf-8").splitlines()]
        r2_spans = [e for e in events
                    if e.get("name") == "critic:regulatory-unknowns-promoted"]
        assert r2_spans and all(e["triggered"] is False for e in r2_spans)
        skeleton_spans = [e for e in events if e.get("name") == "critic:skeleton"]
        assert skeleton_spans and skeleton_spans[0]["output_info"][
            "blocker_rows_added"] == ["Q1"]

    def test_simple_task_skips_critic_and_keeps_legacy_warning_path(self, tmp_path):
        """Tier awareness: SIMPLE ≙ T0/T1 → critic skipped; P1.8 warning
        section preserved unchanged for the legacy path."""
        vault, task = _setup(tmp_path, task_class="SIMPLE")
        llm = _make_llm(BAD_SYNTH_REPORT)
        fc = FlowController(vault_root=vault, llm=llm)

        result = fc.run_meeting(task, departments=DEPARTMENTS)

        assert result.stage == FlowStage.PAUSE_DECISION_REPORT
        assert "Critic" not in result.message
        assert "missing a citation" in result.message
        report = (task / "07-decision-report.md").read_text(encoding="utf-8")
        assert "claims missing a source" in report  # legacy warning appended
        assert not (task / "critic").exists()
        assert not (task / "07-decision-report.draft-r1.md").exists()

    def test_critic_disabled_via_config_knob(self, tmp_path):
        vault, task = _setup(tmp_path)  # COMPLEX
        (vault / ".bd-os.yaml").write_text(
            "critic:\n  enabled: false\n", encoding="utf-8",
        )
        llm = _make_llm(CLEAN_SYNTH_REPORT)
        fc = FlowController(vault_root=vault, llm=llm)
        result = fc.run_meeting(task, departments=DEPARTMENTS)
        assert result.stage == FlowStage.PAUSE_DECISION_REPORT
        assert not (task / "critic").exists()


class TestPassBWiring:
    def test_approve_decision_runs_pass_b_and_attaches_scorecard(self, tmp_path):
        vault, task = _setup(tmp_path)
        llm = _make_llm(CLEAN_SYNTH_REPORT)
        fc = FlowController(vault_root=vault, llm=llm)
        fc.run_meeting(task, departments=DEPARTMENTS)

        result = fc.approve_decision(task)

        assert result.stage == FlowStage.PAUSE_EXECUTE, result.error
        assert "Critic Pass B: PASS" in result.message
        assert (task / "08-execution-plan.md").exists()
        assert (task / "08-execution-plan.draft-r1.md").exists()
        assert (task / "08b-critic-scorecard.md").exists()

    def test_plan_pass_disabled_skips_pass_b(self, tmp_path):
        vault, task = _setup(tmp_path)
        (vault / ".bd-os.yaml").write_text(
            "critic:\n  plan_pass:\n    enabled: false\n", encoding="utf-8",
        )
        llm = _make_llm(CLEAN_SYNTH_REPORT)
        fc = FlowController(vault_root=vault, llm=llm)
        fc.run_meeting(task, departments=DEPARTMENTS)

        result = fc.approve_decision(task)
        assert result.stage == FlowStage.PAUSE_EXECUTE, result.error
        assert "Pass B" not in result.message
        assert not (task / "08b-critic-scorecard.md").exists()


class TestSkeletonAsExecuted:
    """2026-07-05 replay-4 decisive assertion, at the pipeline level: the final
    composed draft ALWAYS contains the Blockers heading — regardless of what
    the model (or the translator) emitted."""

    def test_final_report_always_contains_the_blockers_heading(self, tmp_path):
        vault, task = _setup(tmp_path)
        # Model output with NO blockers section anywhere (the replay-4 shape),
        # citations clean, verdict parseable.
        structureless = """## 📌 Bottom line (30-second read)
- Pilot the deployment in two waves. [state.md]

## Recommendation
PROCEED-WITH-REVISIONS

## Detailed analysis
Fleet return rate is 2.8% against the 3% goal. [state.md]
The PT500 re-certification question remains open — prose only.
"""
        llm = _make_llm(structureless)
        fc = FlowController(vault_root=vault, llm=llm)

        result = fc.run_meeting(task, departments=DEPARTMENTS)

        assert result.stage == FlowStage.PAUSE_DECISION_REPORT
        report = (task / "07-decision-report.md").read_text(encoding="utf-8")
        assert "## Blockers (before Stop 2)" in report
        assert "(ref: Q1)" in report  # the certification unknown, promoted
        assert "TBD — assign at Stop 1" in report
        # Structure cost zero revision rounds.
        assert "Critic: PASS after 1 round(s)" in result.message
        # Every persisted round draft carries the heading too.
        draft = (task / "07-decision-report.draft-r1.md").read_text(encoding="utf-8")
        assert "## Blockers (before Stop 2)" in draft
