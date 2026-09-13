"""Dispatcher — reads the handoff contract, routes intents to consumers under
policy, enforces idempotency, and appends every action to an event log.

It holds no business logic and no credentials; it only delegates. This is the
thin routing agent from the architecture: route · dedupe · policy gate.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from core.handoff.consumers import ROUTES
from core.handoff.manifest import HandoffManifest


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _log_event(log_path: Path, event: dict) -> None:
    """Append one JSON line to the event log — the audit trail / lineage spine."""
    event = {"ts": _now(), **event}
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def dispatch(manifest: HandoffManifest, output_folder: Path, *, force: bool = False) -> list[dict]:
    """Route the manifest's intents to consumer agents.

    output_folder: <vault>/03-Outputs/<slug>/  (drafts land in its handoff/ subdir)
    force: re-run even if an intent was already dispatched (defaults False = idempotent)

    Returns one result dict per intent. Re-running without ``force`` skips intents
    already done, so the same manifest never produces duplicate tickets or drafts.
    """
    output_folder = Path(output_folder)
    outdir = output_folder / "handoff"
    outdir.mkdir(parents=True, exist_ok=True)

    state_path = outdir / "dispatch-state.json"
    log_path = outdir / "dispatch.log"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}

    # Policy gate: this slice only ever prepares drafts. Assert the contract agrees.
    policy = manifest.policy or {}
    if policy.get("external_actions") not in (None, "draft_only"):
        raise PermissionError(
            f"Policy '{policy.get('external_actions')}' would commit external actions; "
            "this dispatcher is draft-only. A human commits via the approval inbox."
        )

    results: list[dict] = []
    for intent in manifest.intents:
        consumer = ROUTES.get(intent)
        if consumer is None:
            results.append({"intent": intent, "status": "no_route"})
            _log_event(log_path, {"actor": "dispatcher", "event": "intent_unrouted",
                                  "task_id": manifest.task_id, "intent": intent})
            continue

        if state.get(intent) == "done" and not force:
            res = {"intent": intent, "status": "skipped_idempotent"}
            results.append(res)
            _log_event(log_path, {"actor": "dispatcher", "event": "intent_skipped_idempotent",
                                  "task_id": manifest.task_id, "intent": intent})
            continue

        result = consumer(manifest, outdir)
        result["intent"] = intent
        results.append(result)
        state[intent] = "done"
        _log_event(log_path, {
            "actor": f"agent:{result.get('channel', intent)}",
            "event": "external_action_prepared",
            "task_id": manifest.task_id,
            "intent": intent,
            "channel": result.get("channel"),
            "status": result.get("status"),
            "policy": "draft_only",
        })

    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return results
