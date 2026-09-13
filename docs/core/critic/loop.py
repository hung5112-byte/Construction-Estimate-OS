"""Critic loop (Pass A) — score the Synthesizer's draft before Stop 1.

Flow (critic-draft §1): Synthesizer draft → critic scores (6 rubrics) →
below threshold or hard-gate trip ⇒ fix-only revision instruction back to the
Synthesizer (Synthesizer-only, 2026-07-05 ruling Q3); ≤3 rounds; exhaustion ⇒
promote WITH a THRESHOLD-NOT-MET banner + attached scorecard. The human never
sees an unscored draft.

Loop constants (C4): threshold 0.6, max 3 rounds (OpenHands), 5 judge samples
(ADK), counter incremented ONLY when actually continuing — a crash between
scoring and revision does not burn a round; re-scoring on resume is idempotent.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from core.critic.constants import (
    THRESHOLD_NOT_MET_BANNER_HEADER,
    resolve_judge_model,
)
from core.critic.deterministic import (
    check_citations,
    check_regulatory_promoted,
    check_verdict,
    parse_clarification_qas,
)
from core.critic.judge import PASS_A_RUBRICS, CriticJudge, JudgedOutcome
from core.critic.models import Issue, RubricResult, sort_issues
from core.critic.skeleton import assemble_skeleton
from core.critic.telemetry import emit_audit, emit_generation, emit_guardrail, emit_status

_RE_ROUTING_CLASS = re.compile(r"\*\*Class:\*\*\s*([A-Z]+)")
_CONTEXT_CAP = 12_000  # chars per context document fed to the judge


@dataclass
class PassOutcome:
    final_report_path: Path
    final_report_text: str
    banner: bool
    rounds_used: int
    verdict: str  # "PASS" | "THRESHOLD-NOT-MET"
    scorecard_path: Path


def read_task_class(task_folder: Path) -> Optional[str]:
    """Task classification from 01-routing.md (SIMPLE | COMPLEX | STRATEGIC)."""
    routing = Path(task_folder) / "01-routing.md"
    if not routing.exists():
        return None
    m = _RE_ROUTING_CLASS.search(routing.read_text(encoding="utf-8"))
    return m.group(1) if m else None


class CriticLoop:
    def __init__(self, llm, config, vault_root: Path, primary_model: str | None = None):
        """
        config: core.utils.config.CriticConfig
        primary_model: llm.primary from engine config — resolves the 'deep' tier.
        """
        self.llm = llm
        self.config = config
        self.vault_root = Path(vault_root)
        self.judge_model = resolve_judge_model(config.judge_model, primary_model)

    # ── Tier awareness (ADR-003 Addendum B) ─────────────────────────────────

    def should_run(self, task_folder: Path) -> bool:
        """Critic is mandatory at COMPLEX/STRATEGIC (≙ T2+), skippable at
        SIMPLE (≙ T0/T1) — read from the task classification + the
        `critic.apply_to_classes` policy knob, never hardcoded. A task with no
        readable classification runs the critic (fail-closed UNKNOWN,
        ADR-003 §2)."""
        if not self.config.enabled:
            return False
        task_class = read_task_class(task_folder)
        if task_class is None:
            return True
        return task_class in set(self.config.apply_to_classes)

    # ── Pass A ───────────────────────────────────────────────────────────────

    def run_pass_a(
        self,
        task_folder: Path,
        draft_text: str,
        revise_fn: Callable[[str, str], str],
    ) -> PassOutcome:
        """Run the full evaluator-optimizer loop on the decision-report draft.

        revise_fn(revision_instruction_md, prior_draft) → new full draft text
        (the Synthesizer's revision turn; fix-only).
        """
        task_folder = Path(task_folder)
        critic_dir = task_folder / "critic"
        critic_dir.mkdir(parents=True, exist_ok=True)

        state = self._load_state(critic_dir)
        round_no = int(state.get("round", 1))
        max_rounds = int(self.config.max_rounds)
        context = self._load_context(task_folder)
        qas = parse_clarification_qas(task_folder / "03-clarification.md")

        current_draft = draft_text
        while True:
            draft_path = task_folder / f"07-decision-report.draft-r{round_no}.md"
            if draft_path.exists():
                # Idempotent resume (C3 discipline): re-score the persisted draft.
                current_draft = draft_path.read_text(encoding="utf-8")
            else:
                # Deterministic skeleton assembly (2026-07-05 design ruling,
                # replay 4): the engine builds the structural skeleton in code
                # AFTER the model/translator produce prose — Blockers section
                # from the clarification data, canonical verdict placement.
                # Idempotent; no-op on compliant text.
                skeleton = assemble_skeleton(current_draft, qas)
                current_draft = skeleton.text
                if skeleton.changed:
                    emit_guardrail(
                        task_folder, "critic:skeleton", triggered=False,
                        output_info=skeleton.info(), round_no=round_no,
                    )
                draft_path.write_text(current_draft, encoding="utf-8")

            det_results = self._run_deterministic(current_draft, task_folder, qas)
            blocking_failed = [r.rubric_id for r in det_results if not r.passed]

            # Gate-first short-circuit (v2.1 Tier-0): a blocking hard-gate
            # failure already forces REVISE — the 5 judge samples would be
            # pure waiting. Skip them, record the skip honestly in the audit
            # trail. PASS still requires a fully-judged, gates-green round
            # (the verdict rule below is unchanged; a skipped round can never
            # satisfy it because blocking_failed is non-empty by definition).
            if blocking_failed:
                judged = JudgedOutcome(
                    results={}, aggregate=0.0, corroborated_issues=[],
                    low_confidence=[], skipped=True,
                )
                emit_status(
                    task_folder, "judged-phase:skipped (gates failed)",
                    info={"blocking_failed": blocking_failed}, round_no=round_no,
                )
            else:
                det_summary = self._deterministic_summary(det_results)
                emit_status(
                    task_folder, "judged-phase:start",
                    info={"samples": int(self.config.judge_samples)},
                    round_no=round_no,
                )
                judged = self._run_judged(
                    task_folder, current_draft, round_no, max_rounds, context,
                    det_summary,
                )
            judged_blockers = [
                rid for rid, r in judged.results.items() if r.info.get("high_confidence_fail")
            ]
            below_threshold = judged.aggregate < float(self.config.threshold)

            # Decision rule (§3), evaluated in order.
            if blocking_failed or judged_blockers or below_threshold:
                verdict = "REVISE"
            else:
                verdict = "PASS"

            issues = sort_issues(
                [i for r in det_results for i in r.issues] + judged.corroborated_issues
            )

            scorecard_md = self._write_scorecards(
                task_folder, critic_dir, round_no, det_results, judged,
                verdict, issues, blocking_failed,
            )
            self._emit_round_telemetry(
                task_folder, round_no, det_results, judged, verdict, current_draft,
                scorecard_md,
            )
            # Idempotent re-score: a resumed round replaces its history entry.
            state["history"] = [
                h for h in state.get("history", []) if h.get("round") != round_no
            ]
            state["history"].append(self._history_entry(
                round_no, draft_path.name, det_results, judged, verdict,
            ))
            state["round"] = round_no  # scoring never burns a round by itself
            self._save_state(critic_dir, state)

            if verdict == "PASS":
                return self._promote(
                    task_folder, critic_dir, current_draft, scorecard_md,
                    banner=False, rounds_used=round_no, state=state,
                )

            if round_no >= max_rounds:
                # Rounds exhausted ⇒ present anyway, never loop forever, never
                # silently pass (ruling Q1: banner; tri-state gate escalates).
                banner_text = self._banner(
                    round_no, blocking_failed + judged_blockers, judged.aggregate,
                    judged_skipped=judged.skipped,
                )
                return self._promote(
                    task_folder, critic_dir, current_draft, scorecard_md,
                    banner=True, rounds_used=round_no, state=state,
                    banner_text=banner_text,
                )

            # Continue: write the revision instruction, THEN increment the
            # counter — incremented only when actually continuing (§1 rule 1).
            revision_md = self._revision_instruction(
                round_no, max_rounds, judged.aggregate, blocking_failed,
                det_results, judged, issues,
            )
            revision_path = critic_dir / f"round-{round_no}-revision.md"
            revision_path.write_text(revision_md, encoding="utf-8")
            state["round"] = round_no + 1
            state["history"][-1]["revision"] = f"critic/{revision_path.name}"
            self._save_state(critic_dir, state)

            current_draft = self._guarded_revision(
                task_folder, round_no, revision_md, current_draft,
                det_results, revise_fn, qas, state, critic_dir,
            )
            round_no += 1

    # ── Monotonic non-regression guard (2026-07-05, replay 4) ────────────────
    #
    # Replay 4 oscillated: citations flipped green in r2 then regressed in r3
    # while the revision cannibalized previously-passing content. Deterministic
    # gates must make monotonic progress: a revision that breaks a
    # previously-passing deterministic rubric is retried ONCE with an explicit
    # regression warning; if it regresses again, the loop falls back to the
    # prior draft (keeping its green gates) and reports the rejection.

    def _guarded_revision(
        self,
        task_folder: Path,
        round_no: int,
        revision_md: str,
        prior_draft: str,
        prior_det: list[RubricResult],
        revise_fn: Callable[[str, str], str],
        qas,
        state: dict,
        critic_dir: Path,
    ) -> str:
        prior_pass = {r.rubric_id: r.passed for r in prior_det}

        def _regressions(draft: str) -> list[str]:
            results = self._run_deterministic(draft, task_folder, qas)
            return [
                r.rubric_id for r in results
                if prior_pass.get(r.rubric_id) and not r.passed
            ]

        candidate = assemble_skeleton(revise_fn(revision_md, prior_draft), qas).text
        regressed = _regressions(candidate)
        if not regressed:
            return candidate

        retry_md = revision_md + self._regression_block(regressed)
        candidate2 = assemble_skeleton(revise_fn(retry_md, prior_draft), qas).text
        regressed2 = _regressions(candidate2)

        if not regressed2:
            action = "retry_succeeded"
            result = candidate2
        else:
            # Fall back: keep the prior draft's green gates; the next round
            # re-scores it and revises again with the remaining budget.
            action = "fallback_to_prior_draft"
            result = prior_draft

        record = {
            "round": round_no,
            "regressed_first_attempt": regressed,
            "regressed_retry": regressed2,
            "action": action,
        }
        state.setdefault("regression_guard", []).append(record)
        self._save_state(critic_dir, state)
        emit_guardrail(
            task_folder, "critic:non-regression", triggered=True,
            output_info=record, round_no=round_no,
        )
        return result

    @staticmethod
    def _regression_block(regressed: list[str]) -> str:
        return (
            "\n\n## ⛔ REGRESSION REJECTED — your revision was discarded\n\n"
            "Your revised draft BROKE previously-passing gates: "
            + ", ".join(regressed)
            + ".\nRe-apply ONLY the listed fixes while preserving everything "
            "that already passed:\n"
            "- every citation mark (`[[...]]`, `(ref: ...)`, `<file>.md`, URL) "
            "from your prior draft must survive verbatim;\n"
            "- every `ASSUMPTION:` line must survive verbatim;\n"
            "- never delete debate coverage (Pro AND Con positions) while "
            "fixing other issues.\n"
            "A revision that fixes one gate by breaking another is rejected."
        )

    # ── Deterministic + judged runners ───────────────────────────────────────

    def _run_deterministic(
        self, draft: str, task_folder: Path, qas
    ) -> list[RubricResult]:
        return [
            check_citations(
                draft, self.vault_root, task_folder,
                max_assumptions=int(self.config.max_assumptions),
            ),
            check_regulatory_promoted(draft, qas),
            check_verdict(draft),
        ]

    def _run_judged(
        self,
        task_folder: Path,
        draft: str,
        round_no: int,
        max_rounds: int,
        context: dict[str, str],
        det_summary: str,
    ) -> JudgedOutcome:
        # Stream one generation span per sample AS IT COMPLETES (v2.1) with
        # the TRUE sent-prompt size — the old post-hoc batch rebuilt the
        # messages WITHOUT transcripts/clarifications/research and undercounted
        # the input by an order of magnitude vs .bd-usage.jsonl.
        def _on_sample(sample_no: int, raw: str, wall: float, prompt_chars: int) -> None:
            emit_generation(
                task_folder, self.judge_model, " " * prompt_chars, raw,
                round_no=round_no, sample_no=sample_no, wall_seconds=wall,
            )

        judge = CriticJudge(
            llm=self.llm,
            judge_samples=int(self.config.judge_samples),
            confidence_floor=float(self.config.confidence_floor),
            issue_vote_floor=int(self.config.issue_vote_floor),
            blocking_vote_floor=int(self.config.blocking_vote_floor),
            model=self.judge_model,
            on_sample=_on_sample,
        )
        return judge.run(
            rubric_ids=PASS_A_RUBRICS,
            draft=draft,
            round_no=round_no,
            max_rounds=max_rounds,
            transcripts=context.get("transcripts", ""),
            clarifications=context.get("clarifications", ""),
            research=context.get("research", ""),
            memory=context.get("memory", ""),
            deterministic_summary=det_summary,
        )

    @staticmethod
    def _deterministic_summary(results: list[RubricResult]) -> str:
        lines = []
        for r in results:
            status = "PASS" if r.passed else "FAIL"
            lines.append(f"- {r.rubric_id}: {status} · {json.dumps(r.info, ensure_ascii=False)}")
            for issue in r.issues:
                lines.append(f"  - [{issue.severity}] {issue.actual} — {issue.evidence[:120]}")
        return "\n".join(lines)

    # ── Context ──────────────────────────────────────────────────────────────

    @staticmethod
    def _load_context(task_folder: Path) -> dict[str, str]:
        def _read(name: str) -> str:
            p = Path(task_folder) / name
            if not p.exists():
                return ""
            return p.read_text(encoding="utf-8")[:_CONTEXT_CAP]

        transcripts = "\n\n".join(filter(None, (
            _read("04-meeting-r1-perspectives.md"),
            _read("05-meeting-r2-debate.md"),
            _read("06-meeting-r3-perspectives.md"),
        )))
        return {
            "transcripts": transcripts,
            "clarifications": _read("03-clarification.md"),
            "research": _read("03b-research-findings.md"),
            # Judge-only episodic block (ADR-004 Step 3) — the judge is the
            # sanctioned consumer, and without it R4 flags memory-derived
            # numbers as unsupported.
            "memory": _read("03c-memory-context.md"),
        }

    # ── State (critic/state.json, §3 shape) ─────────────────────────────────

    @staticmethod
    def _load_state(critic_dir: Path) -> dict:
        state_path = critic_dir / "state.json"
        if state_path.exists():
            try:
                return json.loads(state_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"pass": "A", "round": 1, "history": []}

    def _save_state(self, critic_dir: Path, state: dict) -> None:
        state["pass"] = "A"
        state["max_rounds"] = int(self.config.max_rounds)
        (critic_dir / "state.json").write_text(
            json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8",
        )

    @staticmethod
    def _history_entry(
        round_no: int,
        draft_name: str,
        det_results: list[RubricResult],
        judged: JudgedOutcome,
        verdict: str,
    ) -> dict:
        return {
            "round": round_no,
            "draft": draft_name,
            "blocking": {r.rubric_id: r.passed for r in det_results},
            "judged": (
                "skipped (gates failed)" if judged.skipped
                else {rid: r.score for rid, r in judged.results.items()}
            ),
            "aggregate": None if judged.skipped else round(judged.aggregate, 4),
            "verdict": verdict,
        }

    # ── Scorecards ───────────────────────────────────────────────────────────

    def _write_scorecards(
        self,
        task_folder: Path,
        critic_dir: Path,
        round_no: int,
        det_results: list[RubricResult],
        judged: JudgedOutcome,
        verdict: str,
        issues: list[Issue],
        blocking_failed: list[str],
    ) -> str:
        raw = {
            "round": round_no,
            "verdict": verdict,
            "deterministic": [r.to_dict() for r in det_results],
            "judged": {rid: r.to_dict() for rid, r in judged.results.items()},
            "judged_skipped": judged.skipped,
            "aggregate": None if judged.skipped else judged.aggregate,
            "threshold": float(self.config.threshold),
            "invalid_samples": judged.invalid_samples,
            # Truncated raws of unparseable samples — live replay 2 lost 3/5
            # samples in round 3 with no way to diagnose why from the artifacts.
            "invalid_sample_raws": judged.invalid_raws,
            "duplicate_issues_discarded": judged.duplicate_issues_discarded,
            "samples": [
                {"rubric_verdicts": s.rubric_verdicts, "overall_score": s.overall_score,
                 "issues": [i.to_dict() for i in s.issues]}
                for s in judged.samples
            ],
            "corroborated_issues": [i.to_dict() for i in judged.corroborated_issues],
            "low_confidence_observations": [i.to_dict() for i in judged.low_confidence],
        }
        (critic_dir / f"round-{round_no}-scorecard.json").write_text(
            json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8",
        )

        md = self._scorecard_md(round_no, det_results, judged, verdict, issues, blocking_failed)
        (Path(task_folder) / "07b-critic-scorecard.md").write_text(md, encoding="utf-8")
        return md

    def _scorecard_md(
        self,
        round_no: int,
        det_results: list[RubricResult],
        judged: JudgedOutcome,
        verdict: str,
        issues: list[Issue],
        blocking_failed: list[str],
    ) -> str:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        parts = [
            "---",
            "type: critic_scorecard",
            "pass: A",
            f"round: {round_no}",
            f"verdict: {verdict}",
            "---",
            f"# Critic scorecard — round {round_no} of {self.config.max_rounds} ({ts})",
            "",
            f"**Decision:** {verdict}"
            + (f" · blocking failures: {', '.join(blocking_failed)}" if blocking_failed else ""),
            "",
            "## Hard gates (deterministic — outside the aggregate)",
            "",
            "| Rubric | Result | Detail |",
            "|---|---|---|",
        ]
        for r in det_results:
            detail = ", ".join(f"{k}={v}" for k, v in r.info.items())
            parts.append(f"| {r.rubric_id} | {'PASS' if r.passed else '**FAIL**'} | {detail} |")
        parts += [
            "",
            "## Judged rubrics (5-sample majority)",
            "",
        ]
        if judged.skipped:
            parts += [
                "**Skipped (gates failed)** — the hard-gate failures above already "
                "force REVISE; the judged rubrics re-run once the gates are green. "
                "A PASS always requires a fully-judged round.",
                "",
            ]
        else:
            parts += [
                "| Rubric | PASS votes | Score | Blocks (≥4/5 FAIL) |",
                "|---|---|---|---|",
            ]
            for rid, r in judged.results.items():
                parts.append(
                    f"| {rid} | {r.info.get('pass_votes')}/{r.info.get('valid_samples')} "
                    f"| {r.score:.2f} | {'YES' if r.info.get('high_confidence_fail') else 'no'} |"
                )
            parts += [
                "",
                f"**Judged aggregate:** {judged.aggregate:.2f} (threshold {self.config.threshold})",
                "",
            ]
        if issues:
            parts.append(f"## Issues ({len(issues)}, ordered by severity)")
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
        if judged.low_confidence:
            parts.append("## Low-confidence observations (not sent to the Synthesizer)")
            parts.append("")
            for issue in judged.low_confidence:
                parts.append(f"- [{issue.rubric}] {issue.actual} — {issue.evidence[:160]}")
            parts.append("")
        return "\n".join(parts)

    # ── Revision instruction (§5 template) ───────────────────────────────────
    #
    # Live-replay 2026-07-05 restructure: the flat severity-sorted list put
    # judge-authored issues (with wrong grammar suggestions) ahead of the
    # deterministic hard gates and buried the grammar in one Rules bullet —
    # 3 rounds failed with byte-identical blocking failures. Now: hard gates
    # first with an explicit rejected-again preamble, the accepted grammar
    # echoed verbatim, and repetitive per-line issues capped per rubric.

    _MAX_EXAMPLES_PER_RUBRIC = 6   # deterministic per-line findings shown per rubric
    _MAX_JUDGED_ISSUES = 8         # corroborated judged issues sent per round

    def _issue_block(self, issue: Issue) -> list[str]:
        return [
            f"### {issue.id} · {issue.rubric} · {issue.severity}",
            f"- **Expected:** {issue.expected}",
            f"- **Actual:** {issue.actual}",
            f"- **Evidence:** {issue.evidence}",
            f"- **Fix:** {issue.fix_instruction}",
            f"- **Where:** {', '.join(issue.files_to_modify) or '07-decision-report'}",
            "",
        ]

    def _revision_instruction(
        self,
        round_no: int,
        max_rounds: int,
        aggregate: float,
        blocking_failed: list[str],
        det_results: list[RubricResult],
        judged: JudgedOutcome,
        issues: list[Issue],
    ) -> str:
        from core.critic.constants import ACCEPTED_GRAMMAR

        passing = [r.rubric_id for r in det_results if r.passed] + [
            rid for rid, r in judged.results.items() if r.score >= 0.8
        ]
        passing_summary = ", ".join(passing) if passing else "(nothing passed cleanly)"
        blocking_list = ", ".join(blocking_failed) if blocking_failed else "none"
        failed_det = [r for r in det_results if not r.passed]

        score_line = (
            f"Score: n/a — judged rubrics were skipped this round (hard gates "
            f"failed; they re-score once gates are green, threshold "
            f"{self.config.threshold}). "
            if judged.skipped
            else f"Score: {aggregate:.2f} (threshold {self.config.threshold}). "
        )
        lines = [
            f"# REVISION INSTRUCTION — round {round_no} of {max_rounds}",
            "",
            "Your draft decision report did not clear the pre-Stop-1 critic.",
            score_line + f"Blocking failures: {blocking_list}.",
            f"This is fix round {round_no} of {max_rounds}; the same rubrics re-score "
            "your next draft.",
            "",
        ]

        if failed_det:
            lines += [
                "## ⛔ HARD GATES — fix these first, or the report is rejected again",
                "",
                "The checks below are DETERMINISTIC machine scanners, not judgment",
                "calls. They re-run unchanged on your next draft: the report WILL be",
                "rejected again unless every one of these is fixed exactly as",
                "specified, no matter how good the rest of the document is.",
                "",
            ]
            for result in failed_det:
                shown = result.issues[: self._MAX_EXAMPLES_PER_RUBRIC]
                remainder = len(result.issues) - len(shown)
                lines.append(f"### GATE: {result.rubric_id} — FAILED")
                lines.append("")
                for issue in shown:
                    lines += self._issue_block(issue)
                if remainder > 0:
                    lines += [
                        f"...and {remainder} more finding(s) of the SAME kind under "
                        f"`{result.rubric_id}` (see the scorecard for the full list).",
                        "Apply the identical fix to EVERY remaining instance — the "
                        "scanner counts them all, not just the examples above.",
                        "",
                    ]

        lines += [
            "## REQUIRED GRAMMAR — machine-scanned, copy exactly",
            "",
            "The scanners accept ONLY the following forms. Anything else — however",
            "reasonable it looks — counts as a violation:",
            "",
            ACCEPTED_GRAMMAR,
            "",
            "## Rules — read before touching anything",
            "1. FIX ONLY. Resolve the issues in this instruction and nothing else. Do NOT add",
            "   new options, sections, recommendations, or scope. Do NOT change the verdict",
            "   class unless an issue explicitly requires it. EXCEPTION: when a HARD-GATE",
            "   issue reports a missing REQUIRED section (e.g. the Blockers section),",
            "   adding that section back IS the fix — required structure is never new scope.",
            "2. PRESERVE what passed. The following were found compliant and must survive your",
            f"   edits intact: {passing_summary}.",
            "3. If an issue asks for a citation you cannot supply from the Brain, research",
            "   findings, or clarification answers: either delete the claim or downgrade it to a",
            "   labeled `ASSUMPTION:` line in the form "
            "`ASSUMPTION: <claim> (uncitable: <reason>)`. Never invent a source.",
            "4. Write the full revised report as a NEW draft. Do not describe your edits;",
            "   produce the document. Keep the required section headings unchanged",
            "   (especially `## Recommendation`).",
            "5. NON-REGRESSION. A revision that breaks a previously-passing gate is",
            "   REJECTED by a deterministic guard. Every citation mark and ASSUMPTION",
            "   line from your prior draft survives verbatim unless an issue names it;",
            "   never delete debate coverage (Pro AND Con) while fixing other issues.",
            "",
        ]

        judged_issues = sort_issues(judged.corroborated_issues)[: self._MAX_JUDGED_ISSUES]
        if judged_issues:
            lines += [
                f"## Judged issues to fix ({len(judged_issues)}, ordered by severity)",
                "",
            ]
            for issue in judged_issues:
                lines += self._issue_block(issue)

        return "\n".join(lines)

    # ── Promotion (append-only: the passing/exhausted draft is COPIED) ───────

    def _banner(
        self, rounds: int, failed: list[str], aggregate: float,
        judged_skipped: bool = False,
    ) -> str:
        failed_list = ", ".join(sorted(set(failed))) or "judged aggregate below threshold"
        aggregate_text = (
            "n/a (judged skipped — hard gates failed)" if judged_skipped
            else f"{aggregate:.2f}"
        )
        return "\n".join([
            THRESHOLD_NOT_MET_BANNER_HEADER,
            f"> This report did NOT clear the critic after {rounds} revision round(s).",
            f"> Failing: {failed_list}. Judged aggregate: {aggregate_text} "
            f"(threshold {self.config.threshold}).",
            "> The full scorecard is attached (07b-critic-scorecard.md / "
            "critic/final-scorecard.md).",
            "> Stop-1 options: approve / revise / reject / waive (ADR-003 §1).",
        ])

    def _promote(
        self,
        task_folder: Path,
        critic_dir: Path,
        draft: str,
        scorecard_md: str,
        banner: bool,
        rounds_used: int,
        state: dict,
        banner_text: str = "",
    ) -> PassOutcome:
        final_text = draft
        if banner and banner_text:
            final_text = _insert_after_frontmatter(draft, banner_text + "\n")

        report_path = Path(task_folder) / "07-decision-report.md"
        report_path.write_text(final_text, encoding="utf-8")
        (critic_dir / "final-scorecard.md").write_text(scorecard_md, encoding="utf-8")

        verdict = "THRESHOLD-NOT-MET" if banner else "PASS"
        state["final_verdict"] = verdict
        self._save_state(critic_dir, state)
        emit_status(
            task_folder, "gate:stop-1 reached",
            info={"verdict": verdict, "banner": banner}, round_no=rounds_used,
        )
        emit_guardrail(
            task_folder, "critic:promotion", triggered=banner,
            output_info={"verdict": verdict, "rounds_used": rounds_used},
            round_no=rounds_used,
        )
        return PassOutcome(
            final_report_path=report_path,
            final_report_text=final_text,
            banner=banner,
            rounds_used=rounds_used,
            verdict=verdict,
            scorecard_path=Path(task_folder) / "07b-critic-scorecard.md",
        )

    # ── Telemetry per round ──────────────────────────────────────────────────

    def _emit_round_telemetry(
        self,
        task_folder: Path,
        round_no: int,
        det_results: list[RubricResult],
        judged: JudgedOutcome,
        verdict: str,
        draft: str,
        scorecard_md: str,
    ) -> None:
        for r in det_results:
            emit_guardrail(
                task_folder, f"critic:{r.rubric_id}", triggered=not r.passed,
                output_info={**r.info, "issues": [i.id for i in r.issues]},
                round_no=round_no,
            )
        for rid, r in judged.results.items():
            emit_guardrail(
                task_folder, f"critic:{rid}",
                triggered=bool(r.info.get("high_confidence_fail")),
                output_info=r.info, round_no=round_no,
            )
        emit_guardrail(
            task_folder, "critic", triggered=(verdict != "PASS"),
            output_info={
                "aggregate": None if judged.skipped else judged.aggregate,
                "judged_skipped": judged.skipped,
                "corroborated_issues": [i.id for i in judged.corroborated_issues],
            },
            round_no=round_no,
        )
        emit_audit(task_folder, draft, scorecard_md)


def _insert_after_frontmatter(text: str, block: str) -> str:
    """Insert a banner block right after the YAML frontmatter (or at the top)."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            end = text.find("\n", end)
            if end != -1:
                return text[:end + 1] + "\n" + block + text[end + 1:]
    return block + "\n" + text
