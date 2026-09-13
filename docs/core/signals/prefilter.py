"""Deterministic prefilter — decides which events are worth an LLM triage call.

Pure keyword/sender matching, no LLM: newsletters and noise never cost tokens.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from core.signals.rules import SignalRules
from core.signals.schema import Event


@dataclass
class PrefilterVerdict:
    pass_to_triage: bool
    reason: str
    matched_critical: list[str] = field(default_factory=list)
    matched_high: list[str] = field(default_factory=list)


def _hits(text: str, keywords: list[str]) -> list[str]:
    return [k for k in keywords if k.lower() in text]


def prefilter(event: Event, rules: SignalRules) -> PrefilterVerdict:
    sender = event.sender.lower()
    text = f"{event.subject}\n{event.body}".lower()

    critical = _hits(text, rules.keywords.critical)
    high = _hits(text, rules.keywords.high)

    if any(b.lower() in sender for b in rules.senders.block):
        return PrefilterVerdict(False, "sender blocked")

    # Ignore-list noise is dropped — unless a critical keyword also matched
    # (a real alert forwarded by a newsletter-ish relay must still get through).
    if not critical and _hits(text, rules.keywords.ignore):
        return PrefilterVerdict(False, "ignore keyword, no critical hit")

    if any(a.lower() in sender for a in rules.senders.allow):
        return PrefilterVerdict(True, "sender allowlisted", critical, high)
    if critical:
        return PrefilterVerdict(True, "critical keyword hit", critical, high)
    if high:
        return PrefilterVerdict(True, "high keyword hit", critical, high)

    return PrefilterVerdict(False, "no keyword or sender match")
