"""Tests for Step-7 consolidation: instincts + promotion arithmetic + forgetting.

Spec: ADR-004 §2-§4. quality = 0.3 + 0.7·successRate; promote candidate→active
when used≥3 AND quality≥0.6 across ≥2 distinct tasks; money/legal/safety needs
avg confidence≥0.8; 30-day candidate TTL; disuse decay after 10 task-cycles.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from core.brain.ledger import DecisionLedger, ledger_path
from core.brain.schema import DecisionEntry
from core.memory.instincts import Instinct, InstinctStore, quality_score
from core.memory.consolidation import consolidate

TODAY = date(2026, 7, 17)


def _seed_ledger(vault: Path, entries: list[DecisionEntry]) -> None:
    (vault / "00-Brain").mkdir(parents=True, exist_ok=True)
    ledger = DecisionLedger(ledger_path(vault))
    for e in entries:
        ledger.append(e)


def _resolved(slug: str, d: date, decision: str, quality: float,
              reflection: str) -> DecisionEntry:
    return DecisionEntry(
        date=d, slug=slug, owner="Department Head", decision=decision,
        status="resolved", quality=quality, outcome="done",
        reflection=reflection, resolved_date=d,
    )


# ------------------------------------------------------------------ arithmetic

def test_quality_score_formula():
    assert quality_score(successes=0, used=0) == 0.3  # no evidence → floor
    assert abs(quality_score(successes=1, used=1) - 1.0) < 1e-9
    assert abs(quality_score(successes=1, used=2) - 0.65) < 1e-9  # 0.3+0.7*0.5


# ------------------------------------------------------------------ store CRUD

def test_instinct_round_trips(tmp_path: Path):
    store = InstinctStore(tmp_path / "vault", scope="company")
    inst = Instinct(
        slug="warranty-from-afr", trigger="warranty term decisions",
        action="price warranty length from measured AFR, not competitors",
        confidence=0.5, scope="company", used=2, tasks=["t1", "t2"],
        successes=2, evidence=["t1: worked", "t2: worked"],
        created=TODAY, last_used=TODAY, status="candidate",
    )
    store.save(inst)
    got = store.load("warranty-from-afr")
    assert got.action.startswith("price warranty length")
    assert got.tasks == ["t1", "t2"] and got.status == "candidate"
    text = (tmp_path / "vault" / "00-Brain" / "instincts" / "warranty-from-afr.md").read_text()
    assert "label: internal" in text  # enforced-scope labeling
    assert "type: instinct" in text


def test_instinct_note_excluded_from_doc_search(tmp_path: Path):
    from core.retrieval.indexer import VaultIndexer
    from core.retrieval.search import VaultSearcher

    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    store.save(Instinct(
        slug="zebra-rule", trigger="x", action="unique zanzibar instinct payload",
        confidence=0.5, scope="company", created=TODAY, last_used=TODAY,
    ))
    (vault / "00-Brain" / "strategy.md").write_text(
        "---\nlabel: internal\ntrust_tier: brain\n---\n# S\n\nregular\n", encoding="utf-8"
    )
    VaultIndexer(vault, embed=False).build()
    # Instincts are judge-only semantic memory — not doc-searchable
    assert VaultSearcher(vault).search("zanzibar instinct payload") == []


# ------------------------------------------------------------------ promotion

def test_promotion_requires_uses_quality_and_two_tasks(tmp_path: Path):
    vault = tmp_path / "vault"
    # 3 resolved decisions, same NON-SENSITIVE topic, high quality, 3 tasks
    _seed_ledger(vault, [
        _resolved(f"2026-07-0{i}-rma-queue-{i}", date(2026, 7, i),
                  "Standardize the RMA intake queue routing rules.", 0.9,
                  "Lesson: route RMA intake by defect class, not arrival order.")
        for i in (1, 2, 3)
    ])
    report = consolidate(vault, today=TODAY)
    store = InstinctStore(vault, scope="company")
    active = [i for i in store.all() if i.status == "active"]
    assert active, "a repeated high-quality lesson should promote"
    inst = active[0]
    assert inst.used >= 3 and len(set(inst.tasks)) >= 2
    assert quality_score(inst.successes, inst.used) >= 0.6
    assert report.promoted >= 1


def test_no_promotion_below_thresholds(tmp_path: Path):
    vault = tmp_path / "vault"
    # Only 2 tasks, and low quality → stays candidate
    _seed_ledger(vault, [
        _resolved("2026-07-01-warranty-a", date(2026, 7, 1),
                  "Warranty tweak.", 0.2, "Lesson: minor warranty note."),
        _resolved("2026-07-02-warranty-b", date(2026, 7, 2),
                  "Warranty tweak.", 0.3, "Lesson: minor warranty note."),
    ])
    consolidate(vault, today=TODAY)
    store = InstinctStore(vault, scope="company")
    assert all(i.status != "active" for i in store.all())


def test_money_legal_safety_needs_high_confidence(tmp_path: Path):
    vault = tmp_path / "vault"
    _seed_ledger(vault, [
        _resolved(f"2026-07-0{i}-tax-{i}", date(2026, 7, i),
                  "Adjust the tax withholding payment schedule.", 0.62,
                  "Lesson: file tax payments on the federal schedule.")
        for i in (1, 2, 3)
    ])
    consolidate(vault, today=TODAY)
    store = InstinctStore(vault, scope="company")
    money = [i for i in store.all() if "tax" in i.trigger or "tax" in i.action]
    assert money
    # quality just clears 0.6 but avg confidence starts below 0.8 → held as candidate
    assert all(i.status == "candidate" for i in money)


# ------------------------------------------------------------------ forgetting

def test_stale_candidate_expires_after_30_days(tmp_path: Path):
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    old = TODAY - timedelta(days=31)
    store.save(Instinct(
        slug="stale-idea", trigger="x", action="unreviewed candidate",
        confidence=0.4, scope="company", used=1, tasks=["t1"], successes=1,
        created=old, last_used=old, status="candidate",
    ))
    report = consolidate(vault, today=TODAY)
    assert store.load("stale-idea").status == "archived"
    assert report.archived >= 1


def test_active_instinct_decays_after_disuse(tmp_path: Path):
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    store.save(Instinct(
        slug="rusty-rule", trigger="zzz stale unrelated topic",
        action="active but unused",
        confidence=0.8, scope="company", used=5, tasks=["a", "b", "c"],
        successes=5, status="active", created=TODAY - timedelta(days=200),
        last_used=TODAY, task_cycles_idle=11,
    ))
    # Decay requires an ACTIVITY run (a new unrelated resolved decision), not a
    # bare no-op run — otherwise cron cadence would drive retention.
    _seed_ledger(vault, [_resolved("2026-07-01-other", date(2026, 7, 1),
                                   "Unrelated onboarding decision.", 0.9,
                                   "Lesson: onboard early.")])
    consolidate(vault, today=TODAY)
    got = store.load("rusty-rule")
    assert got.confidence < 0.8  # decayed on the activity run


# ------------------------------------------------------------------ dedup

def test_near_duplicate_instincts_merged_keeping_higher_quality(tmp_path: Path):
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    store.save(Instinct(
        slug="dup-a", trigger="warranty term decisions",
        action="price warranty from measured AFR data",
        confidence=0.5, scope="company", used=2, tasks=["t1", "t2"], successes=1,
        created=TODAY, last_used=TODAY,
    ))
    store.save(Instinct(
        slug="dup-b", trigger="warranty term decisions",
        action="price warranty from measured AFR data",
        confidence=0.7, scope="company", used=3, tasks=["t3", "t4"], successes=3,
        created=TODAY, last_used=TODAY,
    ))
    report = consolidate(vault, today=TODAY)
    survivors = [i for i in store.all() if i.status != "archived"]
    # one survives, and it aggregates evidence from both
    kept = [i for i in survivors if i.trigger == "warranty term decisions"]
    assert len(kept) == 1
    assert set(kept[0].tasks) >= {"t1", "t2", "t3", "t4"}
    assert report.merged >= 1


# ------------------------------------------------------------------ idempotency

def test_consolidation_is_idempotent(tmp_path: Path):
    vault = tmp_path / "vault"
    _seed_ledger(vault, [
        _resolved(f"2026-07-0{i}-warranty-{i}", date(2026, 7, i),
                  "Set CY80 warranty from AFR.", 0.9, "Lesson: warranty from AFR.")
        for i in (1, 2, 3)
    ])
    consolidate(vault, today=TODAY)
    store = InstinctStore(vault, scope="company")
    n1 = len(store.all())
    consolidate(vault, today=TODAY)  # second run, same day
    assert len(store.all()) == n1  # no duplicate instincts


def test_last_processed_marker_written(tmp_path: Path):
    vault = tmp_path / "vault"
    _seed_ledger(vault, [
        _resolved("2026-07-01-x", date(2026, 7, 1), "d", 0.9, "Lesson: something.")
    ])
    consolidate(vault, today=TODAY)
    marker = vault / "00-Brain" / "instincts" / ".consolidation-state.json"
    assert marker.exists()


# --------------------------------------------- audit fast-follow 1: arithmetic fixes

def test_sensitive_batch_does_not_promote_in_one_run(tmp_path: Path):
    """H2/quarantine: 4 same-topic sensitive entries in ONE run must not vault
    a candidate past the 0.8 confidence gate — confidence moves ≤0.1 per run."""
    vault = tmp_path / "vault"
    _seed_ledger(vault, [
        _resolved(f"2026-07-0{i}-pricing-{i}", date(2026, 7, i),
                  "Set the CY80 list price from the cost-plus margin model.", 0.95,
                  "Lesson: derive list price from the cost-plus margin model.")
        for i in (1, 2, 3, 4)
    ])
    consolidate(vault, today=TODAY)
    store = InstinctStore(vault, scope="company")
    money = [i for i in store.all() if i.status != "archived"]
    assert money and all(i.status == "candidate" for i in money)
    assert all(i.confidence <= 0.6 for i in money)  # BASE 0.5, no per-entry stacking


def test_sensitive_confidence_builds_one_step_per_run(tmp_path: Path):
    """Across runs WITH new evidence, a sensitive instinct climbs +0.1/run and
    eventually clears the 0.8 gate — but only over multiple runs."""
    vault = tmp_path / "vault"
    ledger_all = [
        _resolved(f"2026-07-{d:02d}-pricing-{d}", date(2026, 7, d),
                  "Set the CY80 list price from the cost-plus margin model.", 0.95,
                  "Lesson: price from cost-plus margin.")
        for d in range(1, 8)
    ]

    def seed_first(n):
        _seed_ledger(vault, ledger_all[:n])

    seed_first(3)
    consolidate(vault, today=date(2026, 7, 3))
    store = InstinctStore(vault, scope="company")
    c1 = store.all()[0].confidence
    assert store.all()[0].status == "candidate" and c1 <= 0.6

    # append more entries over later runs → confidence climbs, promotes late
    from core.brain.ledger import DecisionLedger, ledger_path
    led = DecisionLedger(ledger_path(vault))
    statuses = []
    for d in range(4, 8):
        led.append(ledger_all[d - 1])
        consolidate(vault, today=date(2026, 7, d))
        statuses.append(store.all()[0].status)
    assert "active" in statuses  # eventually promotes
    # ...but not on the first batch run
    assert statuses[0] == "candidate"


def test_candidate_ttl_keys_on_last_access_not_birth(tmp_path: Path):
    """M2: a candidate created 40 days ago but reviewed 5 days ago must NOT be
    archived — TTL is expire-on-last-access per Addendum A."""
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    store.save(Instinct(
        slug="fresh-review", trigger="supplier audit topic", action="audit first",
        confidence=0.5, scope="company", used=2, tasks=["t1", "t2"], successes=2,
        created=TODAY - timedelta(days=40), last_used=TODAY - timedelta(days=5),
        last_reviewed=TODAY - timedelta(days=5), status="candidate",
    ))
    consolidate(vault, today=TODAY)
    assert store.load("fresh-review").status == "candidate"  # survived


def test_candidate_ttl_archives_when_truly_stale(tmp_path: Path):
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    old = TODAY - timedelta(days=40)
    store.save(Instinct(
        slug="really-stale", trigger="x topic y", action="unreviewed",
        confidence=0.4, scope="company", used=1, tasks=["t1"], successes=1,
        created=old, last_used=old, last_reviewed=old, status="candidate",
    ))
    consolidate(vault, today=TODAY)
    assert store.load("really-stale").status == "archived"


def test_noop_run_does_not_age_active_instinct(tmp_path: Path):
    """M1: idle decay is driven by task activity, not run cadence. A run with no
    new ledger entries must not increment idle or decay a healthy instinct."""
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    store.save(Instinct(
        slug="steady", trigger="x topic", action="a", confidence=0.8,
        scope="company", used=5, tasks=["a", "b", "c"], successes=5,
        status="active", created=TODAY, last_used=TODAY, task_cycles_idle=5,
    ))
    for _ in range(20):  # 20 no-op nightly runs, no new ledger entries
        consolidate(vault, today=TODAY)
    got = store.load("steady")
    assert got.status == "active" and got.confidence == 0.8  # never aged
    assert got.task_cycles_idle == 5


def test_active_instinct_ages_only_on_activity_elsewhere(tmp_path: Path):
    """Idle accrues when other tasks are consolidated that don't touch this
    instinct — that is the real disuse signal."""
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    store.save(Instinct(
        slug="lonely", trigger="zzz unrelated topic", action="a", confidence=0.8,
        scope="company", used=5, tasks=["a", "b", "c"], successes=5,
        status="active", created=TODAY, last_used=TODAY, task_cycles_idle=8,
    ))
    from core.brain.ledger import DecisionLedger, ledger_path
    led = DecisionLedger(ledger_path(vault))
    (vault / "00-Brain").mkdir(parents=True, exist_ok=True)
    for d in range(1, 4):  # 3 runs, each with a NEW unrelated resolved decision
        led.append(_resolved(f"2026-07-0{d}-other-{d}", date(2026, 7, d),
                             "Unrelated supplier onboarding decision.", 0.9,
                             "Lesson: onboard suppliers early."))
        consolidate(vault, today=date(2026, 7, d))
    got = store.load("lonely")
    assert got.task_cycles_idle >= 10 and got.confidence < 0.8  # aged + decayed


# ------------------------------------------- review-fleet regression fixes (round 2)

def test_noop_runs_never_decay_even_past_idle_threshold(tmp_path: Path):
    """The review's major: decay must NOT fire on no-op runs once idle≥10."""
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    store.save(Instinct(
        slug="at-threshold", trigger="zzz topic", action="a", confidence=0.9,
        scope="company", used=5, tasks=["a", "b", "c"], successes=5,
        status="active", created=TODAY, last_used=TODAY, task_cycles_idle=10,
    ))
    for _ in range(6):  # 6 empty nightly crons
        consolidate(vault, today=TODAY)
    got = store.load("at-threshold")
    assert got.status == "active" and got.confidence == 0.9  # untouched by no-ops


def test_dedup_keeper_keeps_fresh_recency_and_touched(tmp_path: Path):
    """The review's minor: a keeper that absorbs a touched loser inherits its
    recency + touched flag, so it is not aged/TTL-archived out from under itself."""
    vault = tmp_path / "vault"
    store = InstinctStore(vault, scope="company")
    stale = TODAY - timedelta(days=29)
    # keeper: a stale candidate about to hit TTL
    store.save(Instinct(
        slug="keeper", trigger="warranty pricing topic",
        action="price warranty from AFR", confidence=0.7,
        scope="company", used=3, tasks=["t1", "t2"], successes=3,
        created=stale, last_used=stale, last_reviewed=stale, status="candidate",
    ))
    # a NEW resolved entry on the same topic arrives this run → folds/creates a
    # twin that dedup merges into keeper, carrying today's recency
    _seed_ledger(vault, [_resolved("2026-07-17-warranty-pricing-x", TODAY,
                                   "Warranty pricing topic revisited.", 0.9,
                                   "Lesson: price warranty from AFR.")])
    consolidate(vault, today=TODAY)
    surv = [i for i in store.all() if i.status != "archived"
            and "warranty" in i.trigger]
    assert surv, "the actively-confirmed lesson must survive"
    assert surv[0].last_reviewed == TODAY  # recency carried forward
