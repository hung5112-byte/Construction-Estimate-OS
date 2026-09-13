"""Append-only agent-activity log → <vault>/.bd-agent-activity.jsonl.

Feeds live visualizations (BD Micro Office) with which agent is speaking right
now: one start/end record per agent turn, tagged with the pipeline stage and
task folder name.

Same contract as usage_log: best-effort by design — logging must NEVER break
an LLM call or the meeting flow, so every entry point swallows its own
exceptions. The vault is resolved from BD_OS_ACTIVE_VAULT (set by
apply_vault_env_to_os) with BD_OS_DEFAULT_VAULT as fallback; if neither points
to an existing directory the record is silently dropped.
"""
from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
from pathlib import Path

ACTIVITY_FILENAME = ".bd-agent-activity.jsonl"


def _log_path() -> Path | None:
    # Skip under pytest, same as usage_log — providers run against mock servers.
    if "PYTEST_CURRENT_TEST" in os.environ:
        return None
    vault = os.getenv("BD_OS_ACTIVE_VAULT") or os.getenv("BD_OS_DEFAULT_VAULT")
    if not vault:
        return None
    root = Path(vault)
    return root / ACTIVITY_FILENAME if root.is_dir() else None


def log_activity(agent: str, event: str, stage: str = "", dept: str = "",
                 task: str = "", text: str = "") -> None:
    """Append one record. event is "start", "end" or "say" (say carries the
    agent's utterance, truncated); task is the task folder name."""
    try:
        path = _log_path()
        if path is None:
            return
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "agent": agent,
            "event": event,
            "stage": stage,
            "dept": dept,
            "task": task,
        }
        if text:
            record["text"] = text[:2000]
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:  # noqa: BLE001 — never fail a turn over bookkeeping
        pass


@contextmanager
def agent_span(agent: str, stage: str = "", dept: str = "", task: str = ""):
    """start/end pair around one agent turn; exceptions still emit the end."""
    log_activity(agent, "start", stage=stage, dept=dept, task=task)
    try:
        yield
    finally:
        log_activity(agent, "end", stage=stage, dept=dept, task=task)
