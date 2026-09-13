"""Critic data models — NEXUS QA-feedback issue format + rubric results.

Issue object per 18-agency-agents §11.2: per-issue expected/actual/evidence +
fix instruction + files-to-modify, carried verbatim into the revision
instruction (critic-draft §4 output schema).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Issue:
    id: str
    rubric: str
    severity: str  # BLOCKER | MAJOR | MINOR
    expected: str
    actual: str
    evidence: str
    fix_instruction: str
    files_to_modify: list[str] = field(default_factory=list)
    confidence: float = 1.0  # deterministic findings are facts → 1.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any], fallback_id: str = "ISS-0") -> "Issue":
        return cls(
            id=str(data.get("id", fallback_id)),
            rubric=str(data.get("rubric", "")),
            severity=str(data.get("severity", "MAJOR")).upper(),
            expected=str(data.get("expected", "")),
            actual=str(data.get("actual", "")),
            evidence=str(data.get("evidence", "")),
            fix_instruction=str(data.get("fix_instruction", "")),
            files_to_modify=list(data.get("files_to_modify", []) or []),
            confidence=float(data.get("confidence", 1.0)),
        )


_SEVERITY_ORDER = {"BLOCKER": 0, "MAJOR": 1, "MINOR": 2}


def sort_issues(issues: list[Issue]) -> list[Issue]:
    """Severity drives issue ordering in the revision instruction (§4 notes)."""
    return sorted(issues, key=lambda i: (_SEVERITY_ORDER.get(i.severity, 3), i.id))


@dataclass
class RubricResult:
    rubric_id: str
    passed: bool
    score: float  # deterministic: 0.0/1.0 · judged: fraction of samples voting PASS
    blocking: bool
    issues: list[Issue] = field(default_factory=list)
    info: dict[str, Any] = field(default_factory=dict)  # guardrail output_info payload

    def to_dict(self) -> dict[str, Any]:
        return {
            "rubric_id": self.rubric_id,
            "passed": self.passed,
            "score": self.score,
            "blocking": self.blocking,
            "issues": [i.to_dict() for i in self.issues],
            "info": self.info,
        }


class CriticError(RuntimeError):
    """Structural failure (report unparseable, no valid judge samples) — the
    OpenAI ladder's `raise` level: engine error → PAUSE, never a retry round."""
