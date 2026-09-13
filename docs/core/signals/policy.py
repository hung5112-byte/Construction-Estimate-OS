"""Trigger policy — deterministic code decides what may convene a meeting.

The LLM only *rates* an event (triage); whether a meeting fires is decided
here by plain rules: severity gate, dedup window, daily cap. State persists
in the vault (RULE 3) so restarts and cron runs share one memory.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

from core.obsidian.vault import ObsidianVault
from core.signals.rules import SignalRules
from core.signals.schema import Event, PolicyAction, PolicyDecision, Severity, TriageResult

STATE_REL_PATH = "01-Inbox/Events/signals-state.json"

_RANK = {Severity.REVIEW: 0, Severity.ROUTINE: 1, Severity.HIGH: 2, Severity.CRITICAL: 3}


class TriggerPolicy:
    def __init__(self, vault_root: Path, rules: SignalRules,
                 now_fn: Callable[[], datetime] = datetime.now):
        self._vault = ObsidianVault(Path(vault_root))
        self._rules = rules.policy
        self._now_fn = now_fn
        self._state = self._load_state()

    def decide(self, event: Event, result: TriageResult) -> PolicyDecision:
        """Gate one triaged event. Records state when a trigger is granted."""
        now = self._now_fn()
        self._prune(now)

        if _RANK[result.severity] < _RANK[self._rules.min_severity_to_trigger]:
            return PolicyDecision(
                action=PolicyAction.LOG_ONLY,
                reason=f"severity {result.severity.value} below trigger threshold "
                       f"{self._rules.min_severity_to_trigger.value}",
            )

        fp = event.fingerprint()
        if fp in self._state["triggered"]:
            return PolicyDecision(
                action=PolicyAction.LOG_ONLY,
                reason=f"duplicate of an event already escalated within "
                       f"{self._rules.dedup_window_hours}h (fingerprint {fp})",
            )

        if len(self._state["meetings"]) >= self._rules.max_auto_meetings_per_day:
            return PolicyDecision(
                action=PolicyAction.LOG_ONLY,
                reason=f"daily cap reached ({self._rules.max_auto_meetings_per_day} "
                       f"auto-meetings) — review the event log manually",
            )

        self._state["triggered"][fp] = now.isoformat()
        self._state["meetings"].append(now.isoformat())
        self._save_state()
        return PolicyDecision(action=PolicyAction.TRIGGER_MEETING,
                              reason=f"severity {result.severity.value} passed all gates")

    # -- state ------------------------------------------------------------

    def _load_state(self) -> dict:
        try:
            data = json.loads(self._vault.read(STATE_REL_PATH))
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        return {"triggered": dict(data.get("triggered", {})),
                "meetings": list(data.get("meetings", []))}

    def _save_state(self) -> None:
        self._vault.write(STATE_REL_PATH, json.dumps(self._state, indent=2))

    def _prune(self, now: datetime) -> None:
        window = timedelta(hours=self._rules.dedup_window_hours)
        self._state["triggered"] = {
            fp: ts for fp, ts in self._state["triggered"].items()
            if now - datetime.fromisoformat(ts) < window
        }
        day_ago = now - timedelta(hours=24)
        self._state["meetings"] = [
            ts for ts in self._state["meetings"]
            if datetime.fromisoformat(ts) > day_ago
        ]
