"""Pydantic schemas for the signals layer (inbound events + triage verdicts)."""
from __future__ import annotations

import hashlib
from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field

EventSource = Literal["email", "chat", "manual"]


class Severity(str, Enum):
    CRITICAL = "critical"      # convene a meeting (subject to policy)
    HIGH = "high"              # log + surface in the daily digest
    ROUTINE = "routine"        # log only
    REVIEW = "review"          # triage could not classify — human look needed


class Event(BaseModel):
    """One normalized inbound message, regardless of channel."""

    source: EventSource
    external_id: str = Field(description="Channel-native id (IMAP uid, chat message id)")
    sender: str
    subject: str = ""
    body: str
    received_at: datetime

    def fingerprint(self) -> str:
        """Stable dedup key: same sender+subject+body → same fingerprint.

        external_id is deliberately excluded so a re-sent or re-fetched copy
        of the same message does not re-trigger a meeting.
        """
        raw = f"{self.sender}\x00{self.subject}\x00{self.body}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:16]


class TriageResult(BaseModel):
    """Verdict on one Event — produced by triage (LLM or deterministic fallback)."""

    severity: Severity
    departments: list[str] = Field(default_factory=list)
    summary: str = Field(description="One-line, Department-Head-friendly (RULE 4)")
    rationale: str = ""
    triaged_by: Literal["llm", "prefilter-fallback"] = "llm"


class PolicyAction(str, Enum):
    TRIGGER_MEETING = "trigger-meeting"
    LOG_ONLY = "log-only"
    DROP = "drop"


class PolicyDecision(BaseModel):
    action: PolicyAction
    reason: str


class DispatchStatus(str, Enum):
    MEETING_STARTED = "meeting-started"        # decision report ready (Stop 1)
    PARKED_CLARIFICATION = "parked-clarification"
    NOT_DISPATCHED = "not-dispatched"
    ERROR = "error"


class DispatchResult(BaseModel):
    status: DispatchStatus
    task_folder: Optional[str] = None
    message: str = ""
