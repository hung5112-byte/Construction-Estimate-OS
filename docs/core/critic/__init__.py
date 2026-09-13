"""Critic loop (evaluator-optimizer) — pre-Stop-1 / pre-Stop-2 quality gate.

Spec: 04-Projects/Agentic-OS/03-build/critic-draft.md
Rulings: 04-Projects/Agentic-OS/03-build/2026-07-05-draft-rulings.md
Guardrail contract: ADR-003 §2 {name, triggered, output_info}; Addendum A
(regulatory-unknowns promotion); Addendum B (tier awareness — mandatory at
COMPLEX/STRATEGIC ≙ T2+, skippable at SIMPLE ≙ T0/T1, read from task
classification, never hardcoded).
"""
from core.critic.loop import CriticLoop, PassOutcome  # noqa: F401
from core.critic.models import Issue, RubricResult  # noqa: F401
