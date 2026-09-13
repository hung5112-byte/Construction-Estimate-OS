"""LLM-judged critic rubrics — 5-sample majority vote on the cheap model tier.

ADK lesson: "we found 5 to be a good default" — never trust a single sample.
ECC anti-noise: per-issue self-reported confidence ≥0.8, and only issues
corroborated by ≥issue_vote_floor samples reach the Synthesizer.
2026-07-05 ruling Q4: a judged rubric BLOCKS only on ≥4/5 FAIL agreement;
a 3/5 split failure just lowers the aggregate (anti-churn).
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from typing import Any, Optional

from core.critic.constants import (
    ACCEPTED_GRAMMAR,
    JUDGED_RUBRICS_PASS_A,
    JUDGED_RUBRICS_PASS_B,
    R4_NUMBERS,
    R5_DEBATE_SIDES,
    R6_REPORT_VS_PLAN,
    RUBRIC_WEIGHTS,
)
from core.critic.models import CriticError, Issue, RubricResult

# ── The critic prompt (critic-draft §4, verbatim structure) ─────────────────

_PROMPT_HEADER = """You are the CRITIC for a division decision report. You are not a co-author, not a
diplomat, and not a debater. Your only job is to decide, per rubric, whether this
draft is fit to put in front of a human decision-maker, and to report every defect
precisely enough that the author can fix it without guessing.

INPUTS PROVIDED
- DRAFT: the decision report draft (round {round} of {max_rounds}).
- TRANSCRIPTS: debate rounds R1-R3 and the department positions.
- CLARIFICATIONS: the clarification questions (with tags) and the human's answers.
- RESEARCH: the research-findings index, including queries that returned not_found.
- DETERMINISTIC RESULTS: pre-computed checker output for citations, regulatory
  promotion, and verdict scale. Treat these as ground truth. Do not re-check them;
  do not contradict them.

RUBRICS TO JUDGE (verdict must be exactly PASS or FAIL for each)
"""

_RUBRIC_TEXT = {
    R4_NUMBERS: """numbers-reconcile — Figures appearing more than once agree everywhere. Derived
   figures trace arithmetically to stated inputs. No benchmark or figure appears
   that research did not support. IMPORTANT: if research returned not_found and the
   draft REFUSES to name a figure, that refusal is CORRECT — a PASS, never a gap to
   fix. Do not invent work.
   SANCTIONED SOURCES (2026-07-05 calibration — a live run failed this rubric 6
   rounds straight for the wrong reasons): a figure carried on a labeled
   `ASSUMPTION: ... (uncitable: ...)` line, or cited to the meeting record
   `(ref: 04-meeting-r1-perspectives.md)` (or r2/r3), IS a supported figure for
   this rubric. Judge only its INTERNAL CONSISTENCY — same value everywhere it
   appears, arithmetic that traces — never its absence from research. Citation
   coverage is the deterministic citations rubric's job; regulatory blockers are
   the deterministic regulatory rubric's job — NOT yours. A FAIL from you must
   point at a genuine numeric defect: the same figure disagreeing across
   sections, a derivation that does not compute, or a benchmark invented where
   research returned not_found. If you find no such defect, the verdict is PASS.""",
    R5_DEBATE_SIDES: """both-debate-sides-represented — For each contested point in the transcripts, the
   draft presents the strongest opposing position and why it lost. Department
   conflicts are surfaced with a named resolution demand, not smoothed over.""",
    R6_REPORT_VS_PLAN: """factual-consistency-report-vs-plan — Nothing in the plan contradicts or
   mischaracterizes the approved report: same verdict class, same figures, same
   gates, owners, deadlines. Watch for characterization drift (e.g. calling an
   end-of-life part "faulty" or "defective" — EOL is a lifecycle status, not a
   defect). No new factual claims without a resolving citation.""",
}

_PROMPT_FOOTER = """
ANTI-FENCE-SITTING — MANDATORY
Commit. Every rubric verdict is PASS or FAIL. "Partially compliant", "mostly fine",
"acceptable with caveats", and hedged language are FORBIDDEN as verdicts. If you
find yourself hedging, you have not looked hard enough: go back to the evidence and
decide. A wrong-but-precise verdict is recoverable; a vague one is useless.

CONFIDENCE DISCIPLINE — MANDATORY
Report ONLY issues you are more than 80% confident are real defects, where you can
quote the exact evidence. If you cannot point at the line, do not report it. Noise
in your report costs a full revision round. Zero issues is a legitimate finding.

BOUNDED OUTPUT — MANDATORY
Report AT MOST 5 issues per response — the 5 most severe. Keep every evidence
quote under 200 characters and every other field to one sentence. Your ENTIRE
response must be a single valid JSON object: an over-long response gets
truncated mid-JSON and your whole sample is discarded (a live run lost 3 of 5
samples this way).

DO NOT DUPLICATE DETERMINISTIC FINDINGS — MANDATORY
Defects already listed under DETERMINISTIC RESULTS (uncited claims, missing
regulatory blockers, non-canonical verdict) are ALREADY queued for fixing with
their own instructions. Do not re-report them as your issues; judge only what
your rubrics cover. The engine DISCARDS any issue of yours whose evidence
quotes the deterministic results. If your only findings for a rubric duplicate
DETERMINISTIC RESULTS, that rubric's verdict is PASS — deterministic coverage
is not your rubric. A live run wasted 6 rounds on duplicated, contradictory
guidance.

THE MACHINE-CHECKED GRAMMAR — your fix_instruction text MUST comply
When a fix_instruction of yours touches a verdict, citation, assumption, or
blocker, suggest ONLY the exact formats below. Suggesting anything else (e.g.
"GO-CONDITIONAL", "DEFER", "(Dept 01 position paper)", "(Q1 answer)") sends the
author into another automatic rejection:

""" + ACCEPTED_GRAMMAR + """

OUTPUT — JSON only, this schema:
{
  "rubric_verdicts": {"<rubric-id>": "PASS" | "FAIL", ...},
  "overall_score": <0.0-1.0>,
  "issues": [
    {
      "id": "ISS-<n>",
      "rubric": "<rubric-id>",
      "severity": "BLOCKER" | "MAJOR" | "MINOR",
      "expected": "<what the rubric requires, one sentence>",
      "actual": "<what the draft actually says/does, one sentence>",
      "evidence": "<exact quote or section/table reference from the draft>",
      "fix_instruction": "<the specific edit that resolves it — imperative, concrete>",
      "files_to_modify": ["<draft filename and section>"],
      "confidence": <0.80-1.0>
    }
  ]
}

FIX-ONLY CONSTRAINT (write this into every fix_instruction's spirit)
Fixes may ONLY resolve the stated defect. Never instruct the author to add new
options, new sections, new recommendations, or new scope. A fix that grows the
document is not a fix."""


def build_judge_messages(
    rubric_ids: tuple[str, ...],
    draft: str,
    round_no: int,
    max_rounds: int,
    transcripts: str = "",
    clarifications: str = "",
    research: str = "",
    deterministic_summary: str = "",
    plan: str = "",
    memory: str = "",
) -> list[dict]:
    header = _PROMPT_HEADER.format(round=round_no, max_rounds=max_rounds)
    rubric_lines = "\n".join(
        f"{n}. {_RUBRIC_TEXT[rid]}" for n, rid in enumerate(rubric_ids, start=1)
    )
    system = header + rubric_lines + "\n" + _PROMPT_FOOTER

    user_parts = [f"## DRAFT\n{draft}"]
    if plan:
        user_parts.append(f"## EXECUTION PLAN (judge against the DRAFT report)\n{plan}")
    if transcripts:
        user_parts.append(f"## TRANSCRIPTS\n{transcripts}")
    if clarifications:
        user_parts.append(f"## CLARIFICATIONS\n{clarifications}")
    if research:
        user_parts.append(f"## RESEARCH\n{research}")
    if memory:
        user_parts.append(
            "## PAST DECISIONS (episodic memory shown to the drafter)\n" + memory
        )
    if deterministic_summary:
        user_parts.append(f"## DETERMINISTIC RESULTS (ground truth)\n{deterministic_summary}")
    user_parts.append("Return the JSON verdict object now.")

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n\n".join(user_parts)},
    ]


# ── Sample parsing ───────────────────────────────────────────────────────────


def _parse_json_object(raw: str) -> dict:
    """Robust JSON extraction: direct → fenced → first balanced object."""
    text = raw.strip()
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1))
        except json.JSONDecodeError:
            pass
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    data = json.loads(text[start:i + 1])
                    if isinstance(data, dict):
                        return data
                    break
    raise ValueError(f"Judge sample is not a JSON object: {raw[:200]}")


@dataclass
class JudgeSample:
    rubric_verdicts: dict[str, str]
    overall_score: float
    issues: list[Issue] = field(default_factory=list)
    raw: str = ""


@dataclass
class JudgedOutcome:
    results: dict[str, RubricResult]  # rubric_id → result (score = PASS fraction)
    aggregate: float                  # weighted mean over judged rubrics only
    corroborated_issues: list[Issue]  # corroborated (or promoted) → revision
    low_confidence: list[Issue]       # under-corroborated → scorecard only
    samples: list[JudgeSample] = field(default_factory=list)
    invalid_samples: int = 0
    invalid_raws: list[str] = field(default_factory=list)  # truncated, for diagnosis
    duplicate_issues_discarded: int = 0  # judge issues that re-litigated det results
    skipped: bool = False  # gate-first short-circuit: hard gates failed, judging skipped


# Judge issues whose evidence/actual quotes the injected deterministic results
# are re-litigations of ground truth (live replay 3: the corroborated
# "numbers-reconcile" issues in rounds 1 and 3 were verbatim restatements of
# the R1/R2 checker output, steering revisions with duplicated — and in round
# 3, WRONG-grammar — guidance). They are discarded mechanically.
_RE_DET_DUPLICATE = re.compile(
    r"deterministic\s+(?:results?|scanner|checker)", re.IGNORECASE
)


def _is_deterministic_duplicate(issue: Issue) -> bool:
    return bool(
        _RE_DET_DUPLICATE.search(issue.evidence or "")
        or _RE_DET_DUPLICATE.search(issue.actual or "")
    )


def _evidence_overlap(a: str, b: str) -> bool:
    """Issue-matching heuristic: quoted-evidence overlap (§3 confidence gate)."""
    ta = set(re.findall(r"[a-z0-9$%.]+", a.lower()))
    tb = set(re.findall(r"[a-z0-9$%.]+", b.lower()))
    if not ta or not tb:
        return False
    if a.lower() in b.lower() or b.lower() in a.lower():
        return True
    inter = len(ta & tb)
    return inter / min(len(ta), len(tb)) >= 0.5


class CriticJudge:
    """Run judge samples against the engine's existing LLM interface."""

    #: providers whose complete() is stateless per call (subprocess / HTTP) —
    #: safe to sample concurrently. MCP sampling stays serial (event-loop
    #: plumbing). v2.1 Tier-0: parallelism changes WAITING, never decisions —
    #: results are collected in submission order, identical to the serial loop.
    THREAD_SAFE_PROVIDERS = ("claude-cli", "claude")

    def __init__(
        self,
        llm,
        judge_samples: int = 5,
        confidence_floor: float = 0.80,
        issue_vote_floor: int = 3,
        blocking_vote_floor: int = 4,
        model: Optional[str] = None,
        on_sample=None,
    ):
        """
        on_sample: optional callback fired as EACH sample completes —
            on_sample(sample_no, raw_text, wall_seconds, prompt_chars).
            Used to stream per-sample telemetry instead of a post-hoc batch.
            Callback errors are swallowed (telemetry never breaks judging).
        """
        self.llm = llm
        self.judge_samples = judge_samples
        self.confidence_floor = confidence_floor
        self.issue_vote_floor = issue_vote_floor
        self.blocking_vote_floor = blocking_vote_floor
        self.model = model
        self.on_sample = on_sample

    def run(
        self,
        rubric_ids: tuple[str, ...],
        draft: str,
        round_no: int,
        max_rounds: int,
        transcripts: str = "",
        clarifications: str = "",
        research: str = "",
        deterministic_summary: str = "",
        plan: str = "",
        memory: str = "",
    ) -> JudgedOutcome:
        messages = build_judge_messages(
            rubric_ids=rubric_ids,
            draft=draft,
            round_no=round_no,
            max_rounds=max_rounds,
            transcripts=transcripts,
            clarifications=clarifications,
            research=research,
            deterministic_summary=deterministic_summary,
            plan=plan,
            memory=memory,
        )

        raws = self._collect_raws(messages)

        samples: list[JudgeSample] = []
        invalid = 0
        invalid_raws: list[str] = []
        duplicates_discarded = 0
        for raw in raws:
            try:
                data = _parse_json_object(raw)
                verdicts = {
                    str(k): str(v).upper()
                    for k, v in (data.get("rubric_verdicts") or {}).items()
                }
                issues = [
                    Issue.from_dict(d, fallback_id=f"ISS-{n}")
                    for n, d in enumerate(data.get("issues") or [], start=1)
                ]
                kept = [i for i in issues if not _is_deterministic_duplicate(i)]
                duplicates_discarded += len(issues) - len(kept)
                issues = kept
                samples.append(JudgeSample(
                    rubric_verdicts=verdicts,
                    overall_score=float(data.get("overall_score", 0.0)),
                    issues=issues,
                    raw=raw,
                ))
            except (ValueError, json.JSONDecodeError, TypeError):
                invalid += 1
                # Keep the tail too — truncation shows at the END of the raw.
                invalid_raws.append(raw[:300] + " …[cut]… " + raw[-300:]
                                    if len(raw) > 650 else raw)

        if not samples:
            # Structural failure — OpenAI ladder `raise`: engine error, not a retry.
            raise CriticError(
                f"All {self.judge_samples} judge samples were unparseable — "
                "cannot score the judged rubrics."
            )

        results = self._vote(rubric_ids, samples)
        aggregate = self._aggregate(rubric_ids, results)
        corroborated, low_conf = self._corroborate(samples)
        corroborated, low_conf = self._guarantee_actionability(
            rubric_ids, results, corroborated, low_conf
        )
        for rid, result in results.items():
            result.issues = [i for i in corroborated if i.rubric == rid]
        return JudgedOutcome(
            results=results,
            aggregate=aggregate,
            corroborated_issues=corroborated,
            low_confidence=low_conf,
            samples=samples,
            invalid_samples=invalid,
            invalid_raws=invalid_raws,
            duplicate_issues_discarded=duplicates_discarded,
        )

    def _collect_raws(self, messages: list[dict]) -> list[str]:
        """Run the N judge samples; return raws in SUBMISSION order.

        Thread-safe providers (claude-cli / anthropic-api: stateless
        subprocess/HTTP per call) run concurrently — identical inputs,
        identical outputs, identical ORDER as the serial loop, just without
        the serial waiting. MCP sampling (or any unknown provider, incl.
        mocks) keeps the serial path. Zero semantic change by construction:
        the vote math consumes the same ordered list either way.
        """
        import time as _time

        prompt_chars = sum(len(str(m.get("content", ""))) for m in messages)

        def _one(sample_no: int) -> str:
            t0 = _time.monotonic()
            raw = self.llm.complete(messages, model=self.model)
            if self.on_sample is not None:
                try:
                    self.on_sample(
                        sample_no, raw, _time.monotonic() - t0, prompt_chars
                    )
                except Exception:  # noqa: BLE001 — telemetry never breaks judging
                    pass
            return raw

        provider = getattr(self.llm, "name", "")
        if provider in self.THREAD_SAFE_PROVIDERS and self.judge_samples > 1:
            from concurrent.futures import ThreadPoolExecutor

            with ThreadPoolExecutor(max_workers=self.judge_samples) as pool:
                futures = [
                    pool.submit(_one, n)
                    for n in range(1, self.judge_samples + 1)
                ]
                return [f.result() for f in futures]  # submission order
        return [_one(n) for n in range(1, self.judge_samples + 1)]

    # ── internals ───────────────────────────────────────────────────────────

    def _vote(
        self, rubric_ids: tuple[str, ...], samples: list[JudgeSample]
    ) -> dict[str, RubricResult]:
        results: dict[str, RubricResult] = {}
        valid = len(samples)
        # Blocking needs ≥ blocking_vote_floor of judge_samples agreement; with
        # fewer valid samples, keep the same fraction (4/5 = 0.8).
        block_fraction = self.blocking_vote_floor / self.judge_samples
        for rid in rubric_ids:
            passes = sum(1 for s in samples if s.rubric_verdicts.get(rid) == "PASS")
            fails = valid - passes
            score = passes / valid
            high_confidence_fail = (fails / valid) >= block_fraction
            results[rid] = RubricResult(
                rubric_id=rid,
                passed=not high_confidence_fail,
                score=score,
                blocking=high_confidence_fail,
                issues=[],
                info={
                    "pass_votes": passes,
                    "fail_votes": fails,
                    "valid_samples": valid,
                    "high_confidence_fail": high_confidence_fail,
                },
            )
        return results

    @staticmethod
    def _aggregate(rubric_ids: tuple[str, ...], results: dict[str, RubricResult]) -> float:
        """Weighted mean over the JUDGED rubrics only, weights renormalized (§3)."""
        weights = {rid: RUBRIC_WEIGHTS.get(rid, 1.0) for rid in rubric_ids}
        total = sum(weights.values()) or 1.0
        return sum(results[rid].score * (weights[rid] / total) for rid in rubric_ids)

    def _corroborate(
        self, samples: list[JudgeSample]
    ) -> tuple[list[Issue], list[Issue]]:
        """Group issues across samples by rubric + evidence overlap.

        ≥ the effective vote floor distinct samples → corroborated (sent back);
        fewer → low-confidence observations (scorecard only).
        Issues below the confidence floor are dropped outright.

        The floor SCALES with valid samples (live replay 2, round 3: only 2 of
        5 samples parsed, so the absolute floor of 3 was unreachable and every
        issue — including 0.95-confidence ones naming the exact defective
        lines — was silently demoted). ceil(valid × issue_vote_floor /
        judge_samples): 5→3, 4→3, 3→2, 2→2, 1→1.
        """
        valid = len(samples)
        effective_floor = max(
            1, math.ceil(valid * self.issue_vote_floor / self.judge_samples)
        )

        groups: list[dict[str, Any]] = []  # {"issue": Issue, "samples": set[int]}
        for idx, sample in enumerate(samples):
            for issue in sample.issues:
                if issue.confidence < self.confidence_floor:
                    continue
                for group in groups:
                    rep: Issue = group["issue"]
                    if rep.rubric == issue.rubric and _evidence_overlap(
                        rep.evidence, issue.evidence
                    ):
                        group["samples"].add(idx)
                        if issue.confidence > rep.confidence:
                            group["issue"] = issue
                        break
                else:
                    groups.append({"issue": issue, "samples": {idx}})

        corroborated: list[Issue] = []
        low_confidence: list[Issue] = []
        for group in groups:
            if len(group["samples"]) >= effective_floor:
                corroborated.append(group["issue"])
            else:
                low_confidence.append(group["issue"])
        return corroborated, low_confidence

    def _guarantee_actionability(
        self,
        rubric_ids: tuple[str, ...],
        results: dict[str, RubricResult],
        corroborated: list[Issue],
        low_confidence: list[Issue],
    ) -> tuple[list[Issue], list[Issue]]:
        """No silent zeros: a judged rubric that scores below passing MUST send
        ≥1 actionable issue forward (live replay 2: numbers-reconcile scored
        0.0 in all 6 rounds while the revision instruction carried none of its
        issues — the Synthesizer was failed on a rubric it was never told about).

        For each rubric with score < 1.0 and no corroborated issue: promote up
        to 2 highest-confidence low-confidence issues of that rubric; if none
        exist at all, emit a synthetic calibration issue so the failure is
        never invisible.
        """
        corroborated = list(corroborated)
        low_confidence = list(low_confidence)
        for rid in rubric_ids:
            result = results[rid]
            if result.score >= 1.0:
                continue
            if any(i.rubric == rid for i in corroborated):
                continue
            candidates = sorted(
                (i for i in low_confidence if i.rubric == rid),
                key=lambda i: i.confidence,
                reverse=True,
            )[:2]
            if candidates:
                for issue in candidates:
                    low_confidence.remove(issue)
                    corroborated.append(issue)
                result.info["issues_promoted_for_actionability"] = len(candidates)
            else:
                synthetic = Issue(
                    id=f"SYN-{rid}",
                    rubric=rid,
                    severity="MAJOR",
                    expected=f"The draft passes the `{rid}` rubric.",
                    actual=(
                        f"{result.info.get('fail_votes')}/{result.info.get('valid_samples')} "
                        f"judge samples voted FAIL on `{rid}` but no sample supplied a "
                        "usable defect record (calibration gap)."
                    ),
                    evidence="(no per-line evidence survived sampling — see raw samples "
                             "in the round scorecard)",
                    fix_instruction=(
                        f"Re-verify the draft against the `{rid}` criterion end-to-end "
                        "and correct anything that does not hold; the judge majority "
                        "found it failing."
                    ),
                    files_to_modify=["07-decision-report.md"],
                    confidence=self.confidence_floor,
                )
                corroborated.append(synthetic)
                result.info["synthetic_issue"] = True
        return corroborated, low_confidence


PASS_A_RUBRICS = JUDGED_RUBRICS_PASS_A
PASS_B_RUBRICS = JUDGED_RUBRICS_PASS_B
