"""Nightly consolidation — the single memory writer (ADR-004 §3-§6, Step 7).

Deterministic offline pass, meant to run once per day/N-tasks (cron / the
sprint-checkpoint cadence), NEVER on the live meeting path. The live pipeline
only appends (ledger, events); this is the only process that edits instinct
notes — so there is exactly one writer and no concurrent-edit hazard.

INCREMENTAL and STATEFUL — a run folds only ledger entries it has not seen
before (tracked in `.consolidation-state.json`). This is what makes the
lifecycle coherent across repeated runs: confidence rises only on genuinely
NEW confirming evidence (not on every no-op run), archived instincts are
durable tombstones (their entries are already processed and won't resurrect
them), and idle instincts accrue disuse cycles.

Everything is arithmetic — no LLM required:
  1. fold each NEW resolved-ledger reflection into a matching instinct
     (token-Jaccard ≥ threshold) or a fresh candidate;
  2. dedup near-duplicate instincts, keeping the higher-quality twin;
  3. promote candidate→active (used≥3 ∧ quality≥0.6 ∧ ≥2 distinct tasks;
     money/legal/safety also needs confidence≥0.8, built ±0.1 per run WITH
     new evidence, never off raw quality);
  4. forget: candidates unreviewed >30 days archived; active instincts idle
     ≥10 consolidation cycles decayed, then archived at the floor.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from core.brain.ledger import TOPIC_STOPWORDS, DecisionLedger, ledger_path
from core.brain.schema import DecisionEntry
from core.memory.instincts import (
    CONFIDENCE_MAX,
    CONFIDENCE_MIN,
    Instinct,
    InstinctStore,
    quality_score,
)

CANDIDATE_TTL_DAYS = 30
IDLE_DECAY_CYCLES = 10
PROMOTE_MIN_USES = 3
PROMOTE_MIN_QUALITY = 0.6
PROMOTE_MIN_TASKS = 2
SENSITIVE_MIN_CONFIDENCE = 0.8
MATCH_JACCARD = 0.6
CONFIDENCE_STEP = 0.1
DECAY_STEP = 0.15
BASE_CONFIDENCE = 0.5

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)
_SENSITIVE_RE = re.compile(
    r"\b(tax|withhold|payroll|wage|salar\w*|price|pricing|cost|margin|revenue|"
    r"budget|discount|payment|invoice|refund|money|fund|financ\w*|"
    r"legal|liabilit|complian|contract|warrant|safety|hazard|recall|"
    r"osha|itar|export|patent|\bip\b)\w*", re.IGNORECASE,
)
_STATE_FILE = ".consolidation-state.json"


@dataclass
class ConsolidationReport:
    proposed: int = 0
    promoted: int = 0
    archived: int = 0
    merged: int = 0
    decayed: int = 0


def _tokens(text: str) -> set[str]:
    return {
        t.lower() for t in _TOKEN_RE.findall(text)
        if len(t) >= 3 and not t.isdigit() and t.lower() not in TOPIC_STOPWORDS
    }


def _slugify(text: str, n: int = 6) -> str:
    words = [w.lower() for w in _TOKEN_RE.findall(text)
             if not w.isdigit() and w.lower() not in TOPIC_STOPWORDS]
    return "-".join(words[:n]) or "instinct"


def _is_sensitive(text: str) -> bool:
    return bool(_SENSITIVE_RE.search(text))


def consolidate(
    vault_root: Path, today: date | None = None, scope: str = "company"
) -> ConsolidationReport:
    vault_root = Path(vault_root)
    today = today or date.today()
    store = InstinctStore(vault_root, scope=scope)
    store.dir.mkdir(parents=True, exist_ok=True)
    report = ConsolidationReport()

    existing = {i.slug: i for i in store.all()}
    pre_run = set(existing)  # instincts that existed BEFORE this run
    state = _load_state(store.dir)
    processed: set[str] = set(state.get("processed_slugs", []))

    # 1. Fold only NEW resolved ledger entries.
    ledger = DecisionLedger(ledger_path(vault_root))
    new_entries = [
        e for e in ledger.entries()
        if e.status == "resolved" and e.reflection and e.quality is not None
        and e.slug not in processed
    ]
    touched: set[str] = set()
    # slug → list of per-entry outcome booleans (quality≥threshold) folded this
    # run. Confidence moves AT MOST ±0.1 per RUN (not per entry) — a single
    # batch of same-topic sensitive entries must not vault past the 0.8 gate.
    run_outcomes: dict[str, list[bool]] = {}
    for e in sorted(new_entries, key=lambda x: x.date):
        _fold_entry(e, existing, today, report, touched, run_outcomes)
        processed.add(e.slug)

    # 1b. Apply the once-per-run confidence step to instincts that ALREADY
    #     existed before this run (new candidates keep BASE_CONFIDENCE and wait
    #     for a later run's confirming evidence — "confidence rises on repeat").
    for slug, outcomes in run_outcomes.items():
        if slug not in pre_run or not outcomes:
            continue
        inst = existing[slug]
        if any(not ok for ok in outcomes):  # any correction → down
            inst.confidence = round(max(CONFIDENCE_MIN, inst.confidence - CONFIDENCE_STEP), 3)
        else:  # all confirming → up
            inst.confidence = round(min(CONFIDENCE_MAX, inst.confidence + CONFIDENCE_STEP), 3)

    # 2. Dedup near-duplicate instincts.
    _dedup(existing, report, touched)

    # 3. Promotion arithmetic.
    for inst in existing.values():
        if inst.status == "candidate" and _should_promote(inst):
            inst.status = "active"
            inst.confidence = round(min(CONFIDENCE_MAX, max(inst.confidence, 0.7)), 3)
            report.promoted += 1

    # 4. Forgetting — durable, and driven by TASK ACTIVITY not run cadence.
    #    - Candidate TTL keys on last-ACCESS (last review), not birth, so an
    #      actively-confirmed candidate is never archived out from under itself.
    #    - Idle cycles accrue only on runs that actually processed new ledger
    #      entries elsewhere; a no-op nightly run ages nothing, so retention no
    #      longer swings ~7x with the cron interval.
    had_activity = bool(new_entries)
    for inst in existing.values():
        if inst.status == "archived":
            continue
        if inst.status == "candidate":
            anchor = inst.last_reviewed or inst.created
            if anchor and (today - anchor).days > CANDIDATE_TTL_DAYS:
                inst.status = "archived"
                report.archived += 1
        elif inst.status == "active":
            if inst.slug in touched:
                inst.task_cycles_idle = 0
            elif had_activity:  # tasks happened, but none about this instinct
                inst.task_cycles_idle += 1
                # Decay ONLY on the activity run that advanced the counter — a
                # no-op cron run must age nothing, else retention scales with
                # cron cadence again (the M1 defect this fix removes).
                if inst.task_cycles_idle >= IDLE_DECAY_CYCLES:
                    inst.confidence = round(max(CONFIDENCE_MIN, inst.confidence - DECAY_STEP), 3)
                    report.decayed += 1
                    if inst.confidence <= CONFIDENCE_MIN:
                        inst.status = "archived"
                        report.archived += 1

    # 5. Persist (single writer) + advance the incremental marker.
    for inst in existing.values():
        store.save(inst)
    _save_state(store.dir, today, processed, len(existing))
    return report


def _fold_entry(
    e: DecisionEntry,
    existing: dict[str, Instinct],
    today: date,
    report: ConsolidationReport,
    touched: set[str],
    run_outcomes: dict[str, list[bool]],
) -> None:
    etok = _tokens(f"{e.slug} {e.decision}")
    if not etok:
        return
    sensitive = _is_sensitive(f"{e.decision} {e.reflection or ''}")

    # Best-matching NON-archived instinct (archived are durable tombstones —
    # already-processed entries can't revive them, and a fresh matching entry
    # starts a NEW instinct rather than resurrecting the retired one).
    best, best_j = None, 0.0
    for inst in existing.values():
        if inst.status == "archived":
            continue
        # Match on the TRIGGER (decision-derived topic) only — the action is
        # the reflection, whose extra tokens would dilute overlap below the
        # threshold and stop genuinely-repeated lessons from folding together.
        itok = _tokens(inst.trigger)
        if not itok:
            continue
        j = len(etok & itok) / len(etok | itok)
        if j > best_j:
            best, best_j = inst, j

    ev = f"{e.slug} (q={e.quality}): {e.reflection}"
    good = (e.quality or 0) >= PROMOTE_MIN_QUALITY
    if best is not None and best_j >= MATCH_JACCARD:
        # Fold evidence in; confidence is NOT touched here — the caller applies
        # at most one ±0.1 step per run from run_outcomes (per-entry bumping
        # let a single batch defeat the sensitive-confidence gate).
        if e.slug not in best.tasks:
            best.tasks.append(e.slug)
        best.used += 1
        if good:
            best.successes += 1
        if ev not in best.evidence:
            best.evidence.append(ev)
        best.last_used = max(best.last_used or e.date, e.date)
        best.last_reviewed = today  # last-access clock for the TTL
        best.sensitive = best.sensitive or sensitive
        touched.add(best.slug)
        run_outcomes.setdefault(best.slug, []).append(good)
        return

    # New candidate — starts at BASE_CONFIDENCE (not read off quality, so a
    # sensitive instinct cannot vault past the 0.8 gate on first sighting) and
    # takes NO per-run step this run; confidence rises only on a LATER run's
    # confirming evidence.
    trigger = " ".join(sorted(etok))[:120]
    slug = _slugify(trigger)
    while slug in existing:  # avoid colliding with a tombstone/other instinct
        slug += "-x"
    inst = Instinct(
        slug=slug, trigger=trigger, action=e.reflection or e.decision,
        confidence=BASE_CONFIDENCE, scope="company",
        used=1, tasks=[e.slug], successes=1 if good else 0,
        evidence=[ev], created=today, last_used=e.date, last_reviewed=today,
        status="candidate", sensitive=sensitive,
    )
    existing[slug] = inst
    touched.add(slug)
    report.proposed += 1


def _should_promote(inst: Instinct) -> bool:
    if inst.used < PROMOTE_MIN_USES:
        return False
    if len(set(inst.tasks)) < PROMOTE_MIN_TASKS:
        return False
    if quality_score(inst.successes, inst.used) < PROMOTE_MIN_QUALITY:
        return False
    if inst.sensitive and inst.confidence < SENSITIVE_MIN_CONFIDENCE:
        return False  # money/legal/safety held until confidence proves out
    return True


def _dedup(
    existing: dict[str, Instinct], report: ConsolidationReport, touched: set[str]
) -> None:
    insts = [i for i in existing.values() if i.status != "archived"]
    for i, a in enumerate(insts):
        if a.status == "archived":  # a was merged away as a loser earlier
            continue
        atok = _tokens(a.trigger)
        for b in insts[i + 1:]:
            if b.status == "archived" or b.slug == a.slug:
                continue
            btok = _tokens(b.trigger)
            if not atok or not btok:
                continue
            jac = len(atok & btok) / len(atok | btok)
            if jac >= MATCH_JACCARD:
                keeper, loser = (a, b) if a.quality >= b.quality else (b, a)
                keeper.tasks = sorted(set(keeper.tasks) | set(loser.tasks))
                keeper.evidence = list(dict.fromkeys(keeper.evidence + loser.evidence))
                # used counts confirmations; successes ≤ used stays invariant.
                keeper.used = keeper.used + loser.used
                keeper.successes = keeper.successes + loser.successes
                keeper.confidence = max(keeper.confidence, loser.confidence)
                keeper.sensitive = keeper.sensitive or loser.sensitive
                # Carry the fresher recency + touched-this-run flag forward, so a
                # keeper that absorbed this run's evidence via a truncated-trigger
                # twin is not aged or TTL-archived out from under itself.
                keeper.last_reviewed = _max_date(keeper.last_reviewed, loser.last_reviewed)
                keeper.last_used = _max_date(keeper.last_used, loser.last_used)
                if loser.slug in touched:
                    touched.add(keeper.slug)
                    keeper.task_cycles_idle = 0
                loser.status = "archived"  # tombstone, not a silent disk drop
                report.merged += 1
                if loser is a:
                    break


def _max_date(a: date | None, b: date | None) -> date | None:
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)


def _load_state(instinct_dir: Path) -> dict:
    path = instinct_dir / _STATE_FILE
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_state(instinct_dir: Path, today: date, processed: set[str], n: int) -> None:
    (instinct_dir / _STATE_FILE).write_text(
        json.dumps({
            "last_processed": today.isoformat(),
            "processed_slugs": sorted(processed),
            "instincts": n,
        }, indent=2),
        encoding="utf-8",
    )
