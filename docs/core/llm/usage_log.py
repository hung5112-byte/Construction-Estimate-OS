"""Append-only token usage log → <vault>/.bd-usage.jsonl (consumed by the dashboard).

Best-effort by design: logging must NEVER break an LLM call, so every entry point
swallows its own exceptions. The vault is resolved from BD_OS_ACTIVE_VAULT (set by
apply_vault_env_to_os) with BD_OS_DEFAULT_VAULT as fallback; if neither points to an
existing directory the record is silently dropped.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

USAGE_FILENAME = ".bd-usage.jsonl"


def _log_path() -> Path | None:
    # Unit tests exercise providers with mock servers; BD_OS_DEFAULT_VAULT may point at
    # a real vault machine-wide, so explicitly skip logging under pytest.
    if "PYTEST_CURRENT_TEST" in os.environ:
        return None
    vault = os.getenv("BD_OS_ACTIVE_VAULT") or os.getenv("BD_OS_DEFAULT_VAULT")
    if not vault:
        return None
    root = Path(vault)
    return root / USAGE_FILENAME if root.is_dir() else None


def log_usage(
    provider: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    estimated: bool = False,
) -> None:
    """Append one usage record. estimated=True → counts derived from char/4, not API."""
    try:
        path = _log_path()
        if path is None:
            return
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "provider": provider,
            "model": model,
            "prompt_tokens": int(prompt_tokens),
            "completion_tokens": int(completion_tokens),
            "estimated": bool(estimated),
        }
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:  # noqa: BLE001 — never fail a completion over bookkeeping
        pass


def estimate_tokens(text: str) -> int:
    """Rough chars/4 heuristic for providers that return no usage data (MCP sampling)."""
    return max(1, len(text) // 4)
