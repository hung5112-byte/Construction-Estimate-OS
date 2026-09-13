"""Signal rules loader — vault custom > bundled default (RULE 6).

Rules are DATA, not code: keyword lists, sender lists, and policy knobs live
in YAML so each deployment (tax, real-estate, F&B forks) defines its own
critical events without touching the engine (RULE 2).
"""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from core.signals.schema import Severity

VAULT_RULES_REL_PATH = "00-Brain/signal-rules.yaml"
_DEFAULT_RULES_PATH = Path(__file__).resolve().parent / "data" / "signal-rules.yaml"


class SenderRules(BaseModel):
    allow: list[str] = Field(default_factory=list)
    block: list[str] = Field(default_factory=list)


class KeywordRules(BaseModel):
    critical: list[str] = Field(default_factory=list)
    high: list[str] = Field(default_factory=list)
    ignore: list[str] = Field(default_factory=list)


class PolicyKnobs(BaseModel):
    min_severity_to_trigger: Severity = Severity.CRITICAL
    dedup_window_hours: int = Field(default=24, ge=0)
    max_auto_meetings_per_day: int = Field(default=3, ge=0)


class SignalRules(BaseModel):
    departments: list[str] = Field(default_factory=list)
    senders: SenderRules = Field(default_factory=SenderRules)
    keywords: KeywordRules = Field(default_factory=KeywordRules)
    policy: PolicyKnobs = Field(default_factory=PolicyKnobs)


def load_rules(vault_root: Path) -> SignalRules:
    """Resolve rules: <vault>/00-Brain/signal-rules.yaml wins over the default."""
    custom = Path(vault_root) / VAULT_RULES_REL_PATH
    path = custom if custom.exists() else _DEFAULT_RULES_PATH
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return SignalRules.model_validate(data)
