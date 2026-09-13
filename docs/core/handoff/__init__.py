"""Handoff layer — the seam between bd-business-os (producer) and downstream agents.

This package turns a finished execution plan into a machine-readable handoff
contract (``handoff.json``) and dispatches it, under policy, to consumer agents
that *prepare* (never send) external actions: a stakeholder email draft, a set
of staged Jira issues, and a Slack notification.

It is pure standard library on purpose: it runs with no API keys and produces
only draft artifacts, so it is safe to run live in a demo.

See ``README.md`` in this folder for the two-minute demo script.
"""
from core.handoff.manifest import (
    Action,
    Artifact,
    HandoffManifest,
    Recipient,
    build_manifest_from_task,
    write_manifest,
)
from core.handoff.dispatcher import dispatch

__all__ = [
    "Action",
    "Artifact",
    "Recipient",
    "HandoffManifest",
    "build_manifest_from_task",
    "write_manifest",
    "dispatch",
]
