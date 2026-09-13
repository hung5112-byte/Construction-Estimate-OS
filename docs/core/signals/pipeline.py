"""Pipeline — glue one Event through prefilter → triage → policy → dispatch.

Kept free of channel and CLI concerns so watchers, the daemon, and tests
all drive the exact same path.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from core.orchestrator.flow_controller import FlowController
from core.signals import event_log
from core.signals.policy import TriggerPolicy
from core.signals.prefilter import prefilter
from core.signals.rules import SignalRules, load_rules
from core.signals.schema import (DispatchResult, DispatchStatus, Event,
                                 PolicyAction, PolicyDecision)
from core.signals.triage import triage

FCFactory = Callable[[Path], FlowController]


def _default_fc_factory(vault_root: Path) -> FlowController:
    from core.llm.providers import get_default_provider
    return FlowController(vault_root=vault_root, llm=get_default_provider())


def process_event(event: Event, vault_root: Path, llm=None,
                  rules: Optional[SignalRules] = None,
                  policy: Optional[TriggerPolicy] = None,
                  fc_factory: FCFactory = _default_fc_factory,
                  dry_run: bool = False) -> dict:
    """Run one event end-to-end. Returns a plain-dict summary for the caller.

    dry_run: triage + policy verdicts are computed and logged, but no
    meeting is started — use it to tune signal-rules.yaml safely.
    """
    vault_root = Path(vault_root)
    rules = rules or load_rules(vault_root)

    verdict = prefilter(event, rules)
    if not verdict.pass_to_triage:
        return {"event": event.subject, "outcome": "dropped", "reason": verdict.reason}

    result = triage(event, verdict, rules, llm=llm)
    policy = policy or TriggerPolicy(vault_root, rules)
    decision = (PolicyDecision(action=PolicyAction.LOG_ONLY, reason="dry run")
                if dry_run else policy.decide(event, result))

    dispatch_result: Optional[DispatchResult] = None
    if decision.action == PolicyAction.TRIGGER_MEETING:
        from core.signals.dispatcher import dispatch
        dispatch_result = dispatch(event, result, fc_factory(vault_root))

    note = event_log.log_event(vault_root, event, result, decision, dispatch_result)
    return {
        "event": event.subject,
        "outcome": decision.action.value,
        "reason": decision.reason,
        "severity": result.severity.value,
        "note": note,
        "dispatch": dispatch_result.status.value if dispatch_result else None,
        "task_folder": dispatch_result.task_folder if dispatch_result else None,
        "needs_human": dispatch_result is not None and dispatch_result.status in
                       (DispatchStatus.MEETING_STARTED, DispatchStatus.PARKED_CLARIFICATION),
    }
