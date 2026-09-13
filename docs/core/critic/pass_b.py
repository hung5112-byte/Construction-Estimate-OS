"""Critic Pass B — lightweight report↔plan consistency check before Stop 2.

Scope (critic-draft §2 R6): R6 factual-consistency-report-vs-plan (judged,
5-sample) + R1-over-plan-new-claims (deterministic) + a deterministic
figure-identity diff of figures present in both documents. Max ONE fix round
(lightweight by design); on second failure, promote with banner to Stop 2.

Run-1 canary: the execution plan calling an EOL chip "faulty" (it is
end-of-life, not defective) is exactly the drift this pass exists to catch.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from core.critic.constants import R6_REPORT_VS_PLAN, resolve_judge_model
from core.critic.deterministic import (
    _line_refs_resolve,
    _RE_CITATION,
    _RE_BRAIN_FILE,
    _RE_FIGURE,
    _RE_Q_REF,
    _RE_REF_MD,
    _RE_WIKILINK,
    extract_figures,
    parse_clarification_qas,
    strip_warning_section,
)
from core.critic.judge import PASS_B_RUBRICS, CriticJudge
from core.critic.loop import _insert_after_frontmatter
from core.critic.models import Issue, RubricResult, sort_issues
from core.critic.telemetry import emit_audit, emit_guardrail

_PLAN_NAME = "08-execution-plan.md"


@dataclass
class PassBOutcome:
    plan_path: Path
    plan_text: str
    banner: bool
    rounds_used: int
    verdict: str  # "PASS" | "THRESHOLD-NOT-MET"


def check_plan_new_claims(
    plan_text: str,
    report_text: str,
    vault_root: Path,
    task_folder: Path | None = None,
) -> RubricResult:
    """Deterministic Pass-B slice: figures the plan introduces that the report
    never stated are NEW factual claims — each must carry a resolving citation
    (R1 re-run over plan-only claims). Works at figure level so table rows are
    covered (the plan template is mostly tables)."""
    plan_body, _ = strip_warning_section(plan_text)
    report_figures = extract_figures(report_text)
    plan_figures = extract_figures(plan_text)
    new_figures = plan_figures - report_figures

    clarification_qids: set[str] = set()
    if task_folder is not None:
        clarification_qids = {
            qa.qid for qa in parse_clarification_qas(Path(task_folder) / "03-clarification.md")
        }

    issues: list[Issue] = []
    seq = 0
    for line_no, line in enumerate(plan_body.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("```"):
            continue
        line_figures = {
            re.sub(r"\s+", "", m.group(0)).upper()
            for m in _RE_FIGURE.finditer(stripped)
        }
        introduced = line_figures & new_figures
        if not introduced:
            continue
        has_cite = bool(
            _RE_CITATION.search(stripped)
            or _RE_BRAIN_FILE.search(stripped)
            or _RE_WIKILINK.search(stripped)
            or _RE_Q_REF.search(stripped)
            or _RE_REF_MD.search(stripped)
        )
        resolved = False
        if has_cite:
            resolved, _unresolved = _line_refs_resolve(
                stripped, Path(vault_root), task_folder, clarification_qids
            )
        if not resolved:
            seq += 1
            issues.append(Issue(
                id=f"R1B-{seq}",
                rubric="citations-resolve-to-brain",
                severity="BLOCKER",
                expected=(
                    "The plan introduces no new factual claims without a "
                    "resolving citation (critic-draft §2 R6 Pass-B scope)."
                ),
                actual=(
                    f"Figure(s) {', '.join(sorted(introduced))} appear in the plan "
                    "but not in the approved report, with no resolving citation."
                ),
                evidence=f"[Line {line_no}] {stripped[:250]}",
                fix_instruction=(
                    "Take the figure from the approved decision report, cite a "
                    "resolving source, or remove the claim from the plan."
                ),
                files_to_modify=[_PLAN_NAME],
            ))

    passed = not issues
    return RubricResult(
        rubric_id="plan-new-claims-cited",
        passed=passed,
        score=1.0 if passed else 0.0,
        blocking=True,
        issues=issues,
        info={"new_figures": sorted(new_figures), "flagged": len(issues)},
    )


def run_pass_b(
    task_folder: Path,
    llm,
    config,
    vault_root: Path,
    replan_fn: Callable[[str, str], str],
    primary_model: str | None = None,
) -> PassBOutcome:
    """Evaluate 08-execution-plan.md against the approved 07-decision-report.md.

    replan_fn(revision_instruction_md, prior_plan) → new full plan text.
    """
    task_folder = Path(task_folder)
    critic_dir = task_folder / "critic"
    critic_dir.mkdir(parents=True, exist_ok=True)

    report_text = (task_folder / "07-decision-report.md").read_text(encoding="utf-8")
    plan_path = task_folder / _PLAN_NAME
    plan_text = plan_path.read_text(encoding="utf-8")

    max_fix_rounds = int(config.plan_pass.max_rounds)
    judge = CriticJudge(
        llm=llm,
        judge_samples=int(config.judge_samples),
        confidence_floor=float(config.confidence_floor),
        issue_vote_floor=int(config.issue_vote_floor),
        blocking_vote_floor=int(config.blocking_vote_floor),
        model=resolve_judge_model(config.judge_model, primary_model),
    )

    round_no = 1
    while True:
        draft_path = task_folder / f"08-execution-plan.draft-r{round_no}.md"
        if not draft_path.exists():
            draft_path.write_text(plan_text, encoding="utf-8")

        det = check_plan_new_claims(plan_text, report_text, vault_root, task_folder)
        det_summary = (
            f"- plan-new-claims-cited: {'PASS' if det.passed else 'FAIL'} · "
            f"{json.dumps(det.info, ensure_ascii=False)}"
        )
        judged = judge.run(
            rubric_ids=PASS_B_RUBRICS,
            draft=report_text,
            plan=plan_text,
            round_no=round_no,
            max_rounds=max_fix_rounds + 1,
            deterministic_summary=det_summary,
        )
        r6 = judged.results[R6_REPORT_VS_PLAN]
        failed = (
            not det.passed
            or bool(r6.info.get("high_confidence_fail"))
            or judged.aggregate < float(config.threshold)
        )
        verdict = "REVISE" if failed else "PASS"
        issues = sort_issues(det.issues + judged.corroborated_issues)

        _write_pass_b_scorecard(
            task_folder, critic_dir, round_no, det, judged, verdict, issues, config,
        )
        emit_guardrail(
            task_folder, f"critic:{R6_REPORT_VS_PLAN}",
            triggered=bool(r6.info.get("high_confidence_fail")),
            output_info=r6.info, round_no=round_no, pass_id="B",
        )
        emit_guardrail(
            task_folder, "critic:plan-new-claims-cited", triggered=not det.passed,
            output_info=det.info, round_no=round_no, pass_id="B",
        )
        emit_guardrail(
            task_folder, "critic", triggered=failed,
            output_info={"aggregate": judged.aggregate}, round_no=round_no, pass_id="B",
        )
        emit_audit(task_folder, plan_text, verdict)

        if not failed:
            plan_path.write_text(plan_text, encoding="utf-8")
            return PassBOutcome(plan_path, plan_text, banner=False,
                                rounds_used=round_no, verdict="PASS")

        if round_no > max_fix_rounds:
            banner = "\n".join([
                "> [!warning] THRESHOLD-NOT-MET",
                f"> This execution plan did NOT clear the pre-Stop-2 critic after "
                f"{max_fix_rounds} fix round(s).",
                f"> Judged aggregate: {judged.aggregate:.2f} (threshold {config.threshold}).",
                "> Scorecard: 08b-critic-scorecard.md. Stop-2 options: "
                "approve / revise / reject / waive.",
            ])
            final_text = _insert_after_frontmatter(plan_text, banner + "\n")
            plan_path.write_text(final_text, encoding="utf-8")
            return PassBOutcome(plan_path, final_text, banner=True,
                                rounds_used=round_no, verdict="THRESHOLD-NOT-MET")

        revision_md = _pass_b_revision(round_no, max_fix_rounds, judged.aggregate,
                                       issues, config)
        (critic_dir / f"pass-b-round-{round_no}-revision.md").write_text(
            revision_md, encoding="utf-8",
        )
        plan_text = replan_fn(revision_md, plan_text)
        round_no += 1


def _pass_b_revision(round_no, max_rounds, aggregate, issues, config) -> str:
    lines = [
        f"# REVISION INSTRUCTION (execution plan) — fix round {round_no} of {max_rounds}",
        "",
        "The execution plan did not clear the pre-Stop-2 critic.",
        f"Score: {aggregate:.2f} (threshold {config.threshold}).",
        "",
        "## Rules",
        "1. FIX ONLY. Resolve the issues below and nothing else — no new tasks,",
        "   resources, risks, or scope.",
        "2. The approved decision report is the source of truth: same verdict class,",
        "   same figures, same gates, owners, and deadlines.",
        "3. Produce the FULL revised plan document, not a description of edits.",
        "",
        f"## Issues to fix ({len(issues)}, ordered by severity)",
        "",
    ]
    for issue in issues:
        lines += [
            f"### {issue.id} · {issue.rubric} · {issue.severity}",
            f"- **Expected:** {issue.expected}",
            f"- **Actual:** {issue.actual}",
            f"- **Evidence:** {issue.evidence}",
            f"- **Fix:** {issue.fix_instruction}",
            "",
        ]
    return "\n".join(lines)


def _write_pass_b_scorecard(
    task_folder, critic_dir, round_no, det, judged, verdict, issues, config,
) -> None:
    raw = {
        "pass": "B",
        "round": round_no,
        "verdict": verdict,
        "deterministic": [det.to_dict()],
        "judged": {rid: r.to_dict() for rid, r in judged.results.items()},
        "aggregate": judged.aggregate,
        "threshold": float(config.threshold),
        "corroborated_issues": [i.to_dict() for i in judged.corroborated_issues],
        "low_confidence_observations": [i.to_dict() for i in judged.low_confidence],
    }
    (Path(critic_dir) / f"pass-b-round-{round_no}-scorecard.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8",
    )
    r6 = judged.results[R6_REPORT_VS_PLAN]
    parts = [
        "---",
        "type: critic_scorecard",
        "pass: B",
        f"round: {round_no}",
        f"verdict: {verdict}",
        "---",
        f"# Critic scorecard (Pass B — report↔plan) — round {round_no}",
        "",
        f"**Decision:** {verdict}",
        "",
        "| Rubric | Result | Detail |",
        "|---|---|---|",
        f"| plan-new-claims-cited | {'PASS' if det.passed else '**FAIL**'} "
        f"| new figures: {len(det.info.get('new_figures', []))}, "
        f"flagged: {det.info.get('flagged')} |",
        f"| {R6_REPORT_VS_PLAN} | {r6.info.get('pass_votes')}/"
        f"{r6.info.get('valid_samples')} PASS votes "
        f"| blocks: {'YES' if r6.info.get('high_confidence_fail') else 'no'} |",
        "",
        f"**Judged aggregate:** {judged.aggregate:.2f} (threshold {config.threshold})",
        "",
    ]
    if issues:
        parts.append(f"## Issues ({len(issues)})")
        parts.append("")
        for issue in issues:
            parts += [
                f"### {issue.id} · {issue.rubric} · {issue.severity}",
                f"- **Expected:** {issue.expected}",
                f"- **Actual:** {issue.actual}",
                f"- **Evidence:** {issue.evidence}",
                f"- **Fix:** {issue.fix_instruction}",
                "",
            ]
    (Path(task_folder) / "08b-critic-scorecard.md").write_text(
        "\n".join(parts), encoding="utf-8",
    )
