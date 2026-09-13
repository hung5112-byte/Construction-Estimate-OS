"""Critic telemetry — guardrail spans (events.jsonl) + audit tuples (audit.jsonl).

ADR-006 vocabulary, adopted not invented:
  guardrail(name="critic:<rubric-id>", triggered=<bool>) — triggered=true means
  the rubric FAILED, consistent with tripwire semantics {name, triggered,
  output_info} (ADR-003 §2).
ADR-003 §3 audit tuple: {ts, caller, input hash, output hash, engine version} —
append-only, per critic action, so scorecards are non-repudiable.

Telemetry wraps the stage; it never lives inside judge logic (ADR-006 §7).
Emission is best-effort — a telemetry failure must not break the flow.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _engine_version() -> str:
    try:
        from importlib.metadata import version
        return version("construction-estimate-os")
    except Exception:  # noqa: BLE001
        return "unknown"


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    try:
        with Path(path).open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001
        pass  # best-effort — never break the flow on telemetry


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit_guardrail(
    task_folder: Path,
    name: str,
    triggered: bool,
    output_info: dict[str, Any] | None = None,
    round_no: int | None = None,
    pass_id: str = "A",
) -> None:
    """One guardrail span per rubric per round (+ one aggregate span per round)."""
    _append_jsonl(Path(task_folder) / "events.jsonl", {
        "ts": _now(),
        "span": "guardrail",
        "name": name,
        "triggered": triggered,
        "output_info": output_info or {},
        "round": round_no,
        "pass": pass_id,
    })


def emit_generation(
    task_folder: Path,
    model: str | None,
    input_text: str,
    output_text: str,
    round_no: int | None = None,
    sample_no: int | None = None,
    pass_id: str = "A",
    wall_seconds: float | None = None,
) -> None:
    """Generation span per judge sample — feeds the run's dual budget (C6).

    v2.1: emitted AS EACH SAMPLE COMPLETES (streamed, thread-safe append) with
    the true sent-prompt size and measured wall time; mono_ns orders spans
    even when wall-clock timestamps collide.
    """
    import time as _time

    try:
        from core.llm.usage_log import estimate_tokens
        input_tokens = estimate_tokens(input_text)
        output_tokens = estimate_tokens(output_text)
    except Exception:  # noqa: BLE001
        input_tokens = len(input_text) // 4
        output_tokens = len(output_text) // 4
    record = {
        "ts": _now(),
        "mono_ns": _time.monotonic_ns(),
        "span": "generation",
        "caller": "critic",
        "model": model or "default",
        "gen_ai.usage.input_tokens": input_tokens,
        "gen_ai.usage.output_tokens": output_tokens,
        "estimated": True,
        "round": round_no,
        "sample": sample_no,
        "pass": pass_id,
    }
    if wall_seconds is not None:
        record["wall_seconds"] = round(wall_seconds, 2)
    _append_jsonl(Path(task_folder) / "events.jsonl", record)


def emit_status(
    task_folder: Path,
    status: str,
    info: dict[str, Any] | None = None,
    round_no: int | None = None,
    pass_id: str = "A",
) -> None:
    """Live progress marker (v2.1): judged-phase entry/skip, gate reached —
    so bd_status and a tail of events.jsonl show progress instead of silence."""
    import time as _time

    _append_jsonl(Path(task_folder) / "events.jsonl", {
        "ts": _now(),
        "mono_ns": _time.monotonic_ns(),
        "span": "status",
        "status": status,
        "info": info or {},
        "round": round_no,
        "pass": pass_id,
    })


def emit_audit(task_folder: Path, input_text: str, output_text: str) -> None:
    """ADR-003 §3 tuple per critic round — draft in, scorecard out."""
    _append_jsonl(Path(task_folder) / "audit.jsonl", {
        "ts": _now(),
        "caller": "critic",
        "input_hash": hashlib.sha256(input_text.encode("utf-8")).hexdigest(),
        "output_hash": hashlib.sha256(output_text.encode("utf-8")).hexdigest(),
        "engine_version": _engine_version(),
    })


def emit_memory_injection(task_folder: Path, items: list, total_chars: int) -> None:
    """ADR-004 Step-3 audit: every episodic item shown to the judge is a logged
    event (AutoGen MemoryQueryEvent pattern) — the raw material for the used≥3
    promotion counters (Step 7). Best-effort like every emitter here."""
    _append_jsonl(Path(task_folder) / "events.jsonl", {
        "ts": _now(),
        "event": "memory_injection",
        "target": "synthesizer",
        "total_chars": total_chars,
        "items": [
            {"index": i.index, "slug": i.slug, "kind": i.kind,
             "score": i.score, "chars": i.chars}
            for i in items
        ],
        "engine_version": _engine_version(),
    })
