"""Base class for every live-research tool.

🔒 RULE 5: Every ToolResult MUST have sources + retrieved_at to cite.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ToolResult:
    data: Any
    sources: list[str] = field(default_factory=list)
    retrieved_at: str = field(default_factory=lambda: datetime.now().isoformat())
    cached: bool = False
    notes: str = ""


class BaseTool(ABC):
    name: str = ""
    description: str = ""
    cache_ttl_seconds: int = 86400

    @abstractmethod
    def run(self, query: str, **kwargs) -> ToolResult:
        ...

    def is_available(self) -> bool:
        """Check whether the tool has the needed credentials/dependencies.

        Default: True. Tools that need an API key override this to check key presence.
        """
        return True

    def skipped_result(self, reason: str) -> ToolResult:
        """Helper returning a ToolResult that states why the tool was skipped.

        When the caller (ResearchPhase) sees `data["skipped"]=True`, it knows the tool
        did not actually run, so RULE 5 is still respected (no silent violation).
        """
        return ToolResult(
            data={"skipped": True, "reason": reason},
            sources=[],
            notes=f"SKIPPED: {reason}",
        )

    def cache_key(self, query: str, **kwargs) -> str:
        import json
        return f"{self.name}::{query}::{json.dumps(sorted(kwargs.items()))}"
