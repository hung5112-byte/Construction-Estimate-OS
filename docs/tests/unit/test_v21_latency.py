"""v2.1 Tier-0 latency work — regression coverage (pass 7).

THE IRON RULE: zero semantic change to decision-making. These tests pin that
parallelism/short-circuiting/telemetry changes alter WAITING, never verdicts:
(1) parallel voting ≡ serial voting, order-independent;
(2) gates-failed rounds skip judging, say so in the audit trail, and can
    never produce a PASS;
(3) team-take assembly order is completion-order-independent;
(4) judge telemetry reports the TRUE sent-prompt size (was undercounting by
    rebuilding messages without context);
(5) per-sample generation spans stream as samples complete, monotonically
    ordered, plus live status markers.
"""
from __future__ import annotations

import json
import random
import threading
import time
from unittest.mock import MagicMock

from core.critic.constants import R4_NUMBERS, R5_DEBATE_SIDES
from core.critic.judge import PASS_A_RUBRICS, CriticJudge, JudgeSample
from core.critic.loop import CriticLoop
from core.llm.usage_log import estimate_tokens
from core.utils.config import CriticConfig

from tests.unit.test_critic_loop import (  # reuse the loop harness
    BAD_DRAFT,
    CLEAN_DRAFT,
    _judge_sample,
    _make_task,
)


def _sample_json(r4="PASS", r5="PASS", score=0.9):
    return json.dumps({
        "rubric_verdicts": {R4_NUMBERS: r4, R5_DEBATE_SIDES: r5},
        "overall_score": score,
        "issues": [],
    })


class _FakeProvider:
    """Thread-safe fake with a real provider name and per-call delays."""

    def __init__(self, name: str, responses: list[str], delays: list[float] | None = None):
        self.name = name
        self._responses = list(responses)
        self._delays = list(delays or [0.0] * len(responses))
        self._lock = threading.Lock()
        self._in_flight = 0
        self.max_concurrent = 0
        self.calls = 0

    def complete(self, messages, model=None):
        with self._lock:
            idx = self.calls
            self.calls += 1
            self._in_flight += 1
            self.max_concurrent = max(self.max_concurrent, self._in_flight)
        try:
            time.sleep(self._delays[idx % len(self._delays)])
            return self._responses[idx % len(self._responses)]
        finally:
            with self._lock:
                self._in_flight -= 1


class TestParallelJudging:
    """Item 1: 5 samples run concurrently for thread-safe providers, with
    results collected in submission order — vote math identical to serial."""

    def _distinct_samples(self):
        # A mixed vote so every aggregation path is exercised.
        return [
            _sample_json(r4="FAIL"), _sample_json(), _sample_json(r4="FAIL"),
            _sample_json(), _sample_json(r5="FAIL"),
        ]

    def test_parallel_outcome_identical_to_serial(self):
        samples = self._distinct_samples()
        # Serial reference: unknown provider name → serial path.
        serial = CriticJudge(llm=_FakeProvider("mcp-sampling", samples)).run(
            PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)
        # Parallel: claude-cli name + reversed delays (last submitted finishes first).
        parallel = CriticJudge(llm=_FakeProvider(
            "claude-cli", samples, delays=[0.05, 0.04, 0.03, 0.02, 0.01])).run(
            PASS_A_RUBRICS, draft="d", round_no=1, max_rounds=3)

        for rid in PASS_A_RUBRICS:
            assert parallel.results[rid].score == serial.results[rid].score
            assert parallel.results[rid].passed == serial.results[rid].passed
            assert parallel.results[rid].info == serial.results[rid].info
        assert parallel.aggregate == serial.aggregate
        assert [s.rubric_verdicts for s in parallel.samples] == [
            s.rubric_verdicts for s in serial.samples]  # submission order kept

    def test_thread_safe_provider_actually_runs_concurrently(self):
        provider = _FakeProvider("claude-cli", self._distinct_samples(),
                                 delays=[0.05] * 5)
        CriticJudge(llm=provider).run(PASS_A_RUBRICS, draft="d", round_no=1,
                                      max_rounds=3)
        assert provider.max_concurrent > 1

    def test_mcp_sampling_provider_stays_serial(self):
        provider = _FakeProvider("mcp-sampling", self._distinct_samples(),
                                 delays=[0.01] * 5)
        CriticJudge(llm=provider).run(PASS_A_RUBRICS, draft="d", round_no=1,
                                      max_rounds=3)
        assert provider.max_concurrent == 1

    def test_vote_math_is_order_independent(self):
        """The frozen decision rule cannot depend on sample order."""
        judge = CriticJudge(llm=MagicMock())
        base = [JudgeSample(
            rubric_verdicts={R4_NUMBERS: v, R5_DEBATE_SIDES: "PASS"},
            overall_score=0.5) for v in ("FAIL", "FAIL", "PASS", "FAIL", "PASS")]
        reference = judge._vote(PASS_A_RUBRICS, base)
        for seed in range(5):
            shuffled = base[:]
            random.Random(seed).shuffle(shuffled)
            voted = judge._vote(PASS_A_RUBRICS, shuffled)
            for rid in PASS_A_RUBRICS:
                assert voted[rid].score == reference[rid].score
                assert voted[rid].passed == reference[rid].passed


class TestGateFirstShortCircuit:
    """Item 2: blocking hard-gate failure ⇒ no judge calls that round, honest
    audit trail; a PASS is impossible without a fully-judged round."""

    def test_gates_failed_round_makes_zero_judge_calls(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()  # any judge call would blow up: no side_effect set
        llm.complete.side_effect = AssertionError("judge must not be called")
        revise = MagicMock(side_effect=lambda i, p: BAD_DRAFT)

        # max_rounds=3 pinned: this test asserts the skip marker on EVERY round
        # of a multi-round exhaustion (shipped default is 1 round since 2026-07-06)
        outcome = CriticLoop(llm=llm, config=CriticConfig(max_rounds=3),
                             vault_root=vault).run_pass_a(task, BAD_DRAFT, revise)

        assert outcome.verdict == "THRESHOLD-NOT-MET"  # exhausted, never judged
        assert llm.complete.call_count == 0
        state = json.loads((task / "critic" / "state.json").read_text(
            encoding="utf-8"))
        for entry in state["history"]:
            assert entry["judged"] == "skipped (gates failed)"
            assert entry["aggregate"] is None
            assert entry["verdict"] == "REVISE"
        # events.jsonl carries the live skip marker per round
        events = [json.loads(x) for x in (task / "events.jsonl").read_text(
            encoding="utf-8").splitlines()]
        skips = [e for e in events if e.get("span") == "status"
                 and "skipped" in e.get("status", "")]
        assert len(skips) == 3

    def test_pass_requires_a_fully_judged_gates_green_round(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(5)]
        outcome = CriticLoop(llm=llm, config=CriticConfig(), vault_root=vault
                             ).run_pass_a(task, CLEAN_DRAFT, MagicMock())
        assert outcome.verdict == "PASS"
        assert llm.complete.call_count == 5  # the PASS round was fully judged
        state = json.loads((task / "critic" / "state.json").read_text(
            encoding="utf-8"))
        passing = [h for h in state["history"] if h["verdict"] == "PASS"]
        assert passing and all(isinstance(h["judged"], dict) for h in passing)

    def test_gates_failed_revision_carries_deterministic_issues_only(self, tmp_path):
        vault, task = _make_task(tmp_path)
        llm = MagicMock()
        captured = []
        revise = MagicMock(side_effect=lambda i, p: captured.append(i) or BAD_DRAFT)
        # max_rounds=3 pinned: a revision instruction only exists when a second
        # round is allowed (shipped default is 1 round since 2026-07-06)
        CriticLoop(llm=llm, config=CriticConfig(max_rounds=3), vault_root=vault
                   ).run_pass_a(task, BAD_DRAFT, revise)
        md = captured[0]
        assert "⛔ HARD GATES" in md
        assert "### ISS-" not in md  # no judged issues exist on a skipped round
        assert "judged rubrics were skipped this round" in md
        assert "threshold 0.6" in md


class TestTeamTakeOrdering:
    """Item 3: takes complete out of order; assembly stays in team order."""

    def test_manager_input_preserves_original_team_order(self, tmp_path):
        from core.meeting.debate_state import new_meeting_state
        from core.orchestrator.perspectives_collector import PerspectivesCollector

        code = "01-hardware-engineering"
        dept = tmp_path / code
        (dept / "agents").mkdir(parents=True)
        teams = ["t-one", "t-two", "t-three"]
        (dept / "department.yaml").write_text(
            f"code: {code}\nname_local: D\ntier: 1\ndescription: d\n"
            f"agents: [mgr, {', '.join(teams)}]\ndefault_speaker: mgr\n",
            encoding="utf-8",
        )
        (dept / "agents" / "mgr.md").write_text(
            f"---\nid: mgr\nname_local: M\ndepartment: {code}\n---\nManager.",
            encoding="utf-8")
        for tid in teams:
            (dept / "agents" / f"{tid}.md").write_text(
                f"---\nid: {tid}\nname_local: {tid}\ndepartment: {code}\n---\n"
                f"You are {tid}.", encoding="utf-8")

        # First-submitted team is the SLOWEST — completion order reversed.
        delays = {"t-one": 0.06, "t-two": 0.03, "t-three": 0.0}

        def respond(messages, model=None):
            system = messages[0]["content"]
            for tid, delay in delays.items():
                if f"You are {tid}" in system:
                    time.sleep(delay)
                    return f"take-from-{tid}"
            return "synthesis"

        llm = MagicMock()
        llm.complete = MagicMock(side_effect=respond)
        collector = PerspectivesCollector(
            departments_root=tmp_path, llm=llm, intra_department=True)
        out = collector.collect(new_meeting_state(brief="b", departments=[code]))

        takes = out["team_inputs"][code]
        assert list(takes.keys()) == teams  # original order, not completion order
        manager_system = llm.complete.call_args_list[-1][0][0][0]["content"]
        assert (manager_system.index("take-from-t-one")
                < manager_system.index("take-from-t-two")
                < manager_system.index("take-from-t-three"))


class TestTelemetryTruth:
    """Items 4+5: spans carry the true sent-prompt size, stream per sample,
    and the loop emits live phase/gate markers."""

    def _run_clean_round(self, tmp_path, transcript_chars=20_000):
        vault, task = _make_task(tmp_path)
        (task / "04-meeting-r1-perspectives.md").write_text(
            "x" * transcript_chars, encoding="utf-8")
        llm = MagicMock()
        llm.complete.side_effect = [_judge_sample() for _ in range(5)]
        CriticLoop(llm=llm, config=CriticConfig(), vault_root=vault
                   ).run_pass_a(task, CLEAN_DRAFT, MagicMock())
        return [json.loads(x) for x in (task / "events.jsonl").read_text(
            encoding="utf-8").splitlines()]

    def test_generation_span_reports_true_context_size(self, tmp_path):
        events = self._run_clean_round(tmp_path)
        gens = [e for e in events if e.get("span") == "generation"]
        assert len(gens) == 5
        # The judge prompt includes the 20K transcript + the draft — the span
        # must account for at least that much (old code logged ~1-2K).
        floor = estimate_tokens("x" * 20_000)
        for g in gens:
            assert g["gen_ai.usage.input_tokens"] >= floor
            assert "wall_seconds" in g

    def test_per_sample_spans_stream_in_monotonic_order(self, tmp_path):
        events = self._run_clean_round(tmp_path)
        gens = [e for e in events if e.get("span") == "generation"]
        monos = [g["mono_ns"] for g in gens]
        assert monos == sorted(monos)
        assert len(set(monos)) == len(monos)  # strictly increasing
        # serial mock → sample numbers in submission order too
        assert [g["sample"] for g in gens] == [1, 2, 3, 4, 5]

    def test_live_status_markers_for_phase_and_gate(self, tmp_path):
        events = self._run_clean_round(tmp_path)
        statuses = [e["status"] for e in events if e.get("span") == "status"]
        assert "judged-phase:start" in statuses
        assert "gate:stop-1 reached" in statuses
        # the phase marker precedes the samples; the gate marker is last
        first_status_idx = next(i for i, e in enumerate(events)
                                if e.get("span") == "status")
        first_gen_idx = next(i for i, e in enumerate(events)
                             if e.get("span") == "generation")
        assert first_status_idx < first_gen_idx
