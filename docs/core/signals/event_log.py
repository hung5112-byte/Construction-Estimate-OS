"""Event log — every inbound event lands in the vault first (RULE 3).

One markdown note per event in 01-Inbox/Events/ with the triage verdict,
the policy decision, and (when a meeting fired) a wikilink to the task
folder — the audit trail of WHY a meeting was auto-convened.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from core.obsidian.vault import ObsidianVault
from core.signals.schema import DispatchResult, Event, PolicyDecision, TriageResult

EVENTS_DIR = "01-Inbox/Events"
_MAX_BODY_CHARS = 3000


def _slug(text: str, max_len: int = 40) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:max_len].rstrip("-") or "event"


def log_event(vault_root: Path, event: Event, result: TriageResult,
              decision: PolicyDecision,
              dispatch: DispatchResult | None = None) -> str:
    """Write the event note; returns its vault-relative path."""
    vault = ObsidianVault(Path(vault_root))
    stamp = event.received_at.strftime("%Y-%m-%d-%H%M")
    rel_path = f"{EVENTS_DIR}/{stamp}-{_slug(event.subject or event.body)}.md"

    frontmatter = {
        "type": "signal-event",
        "source": event.source,
        "sender": event.sender,
        "received_at": event.received_at.isoformat(),
        "fingerprint": event.fingerprint(),
        "severity": result.severity.value,
        "triaged_by": result.triaged_by,
        "policy_action": decision.action.value,
    }
    if dispatch and dispatch.task_folder:
        frontmatter["task_folder"] = dispatch.task_folder

    lines = [
        f"# {event.subject or '(no subject)'}",
        "",
        f"**Summary:** {result.summary}",
        f"**Severity:** {result.severity.value} — {result.rationale}",
        f"**Departments:** {', '.join(result.departments) or '—'}",
        f"**Policy:** {decision.action.value} — {decision.reason}",
    ]
    if dispatch:
        lines.append(f"**Dispatch:** {dispatch.status.value} — {dispatch.message}")
        if dispatch.task_folder:
            lines.append(f"**Task:** [[{Path(dispatch.task_folder).name}]]")
    lines += [
        "",
        "## Original message (untrusted)",
        "",
        "```text",
        event.body[:_MAX_BODY_CHARS],
        "```",
        "",
    ]
    vault.write(rel_path, "\n".join(lines), frontmatter=frontmatter)
    return rel_path
