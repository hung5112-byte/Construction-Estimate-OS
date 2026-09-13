"""Consumer agents — they *prepare* external actions, never commit them.

Each consumer reads the manifest and writes draft artifacts into
<output_folder>/handoff/. Nothing is sent. In production these become real
MCP calls (Gmail create_draft, Atlassian create-issue, Slack post) behind the
same function boundary — the human approves at the morning command center.

Each returns a small result dict the dispatcher records to the event log.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from core.handoff.manifest import HandoffManifest

# Role/department directory. In production this is a lookup against the company
# directory; kept inline here so the demo is self-contained and PII-free.
DEPT_DIRECTORY = {
    "01-bid-coordination": ("Bid Coordinator", "bids@precon.example"),
    "02-civil-structural": ("Civil & Structural Lead", "structural@precon.example"),
    "03-architectural": ("Architectural Lead", "architectural@precon.example"),
    "04-mep": ("MEP Lead", "mep@precon.example"),
    "05-cost-engineering": ("Pricing Lead", "pricing@precon.example"),
    "06-estimate-review": ("Chief Estimator", "chief-estimator@precon.example"),
}


def _resolve(dept: str) -> tuple[str, str]:
    return DEPT_DIRECTORY.get(dept, (dept, f"{dept}@division.example"))


# ──────────────────────────────────────────────────────────────────────────────
# Email agent  (intent: request_approval)
# ──────────────────────────────────────────────────────────────────────────────
def email_agent(m: HandoffManifest, outdir: Path) -> dict:
    to = [_resolve(r.dept) for r in m.recipients if r.role == "approver"]
    cc = [_resolve(r.dept) for r in m.recipients if r.role in ("responsible", "informed")]
    subject = f"[Decision · approval needed] {m.title}"

    lines = [f"Hi {to[0][0] if to else 'team'},", ""]
    lines.append("The division agents have prepared a decision and execution plan. Summary:")
    lines.append("")
    for kp in (m.key_points or [m.summary]):
        lines.append(f"  • {kp}")
    lines.append("")
    lines.append(f"This breaks into {len(m.actions)} tracked actions (staged in Jira for your release).")
    if m.artifacts:
        lines.append("")
        lines.append("Supporting documents:")
        for a in m.artifacts:
            lines.append(f"  • {a.title} ({a.type})")
    lines.append("")
    lines.append("Prepared by the sourcing agent as a DRAFT. Please review and send if you approve.")
    body = "\n".join(lines)

    payload = {
        "to": [e for _, e in to],
        "cc": [e for _, e in cc],
        "subject": subject,
        "body": body,
        "attachments": [a.path for a in m.artifacts],
    }
    (outdir / "email-draft.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    preview = f"To: {', '.join(payload['to']) or '(none)'}\nCc: {', '.join(payload['cc']) or '(none)'}\nSubject: {subject}\n\n{body}\n"
    (outdir / "email-draft.md").write_text(preview, encoding="utf-8")

    return {
        "channel": "email",
        "action": "create_draft",
        "status": "drafted",
        "to": payload["to"],
        "subject": subject,
        "files": ["email-draft.md", "email-draft.json"],
    }


# ──────────────────────────────────────────────────────────────────────────────
# Jira agent  (intent: track_work)
# ──────────────────────────────────────────────────────────────────────────────
def jira_agent(m: HandoffManifest, outdir: Path) -> dict:
    issues = []
    for a in m.actions:
        assignee = a.owners[0] if a.owners else "unassigned"
        issues.append({
            "summary": a.title[:120],
            "description": (
                f"Deliverable: {a.deliverable}\n"
                f"Owner department(s): {', '.join(a.owners)}\n"
                f"Due: {a.due}\n"
                f"Source decision: {m.task_id}"
            ),
            "assignee_dept": assignee,
            "duedate": a.due,
            "priority": "High" if a.priority == "high" else "Medium",
            # Idempotency keys: a re-run can find and skip these instead of duplicating.
            "labels": [f"task:{m.task_id}", f"action:{a.id}", "bd-business-os"],
            "status": "Backlog",  # staged, never auto-transitioned
        })
    (outdir / "jira-issues.json").write_text(json.dumps(issues, indent=2, ensure_ascii=False), encoding="utf-8")

    md = ["| # | Summary | Assignee (dept) | Due | Priority |",
          "|---|---------|-----------------|-----|----------|"]
    for a, iss in zip(m.actions, issues):
        md.append(f"| {a.id} | {iss['summary']} | {iss['assignee_dept']} | {iss['duedate']} | {iss['priority']} |")
    md.append("")
    md.append(f"_{len(issues)} issues staged in Backlog with label `task:{m.task_id}` — released on human approval._")
    (outdir / "jira-issues-preview.md").write_text("\n".join(md), encoding="utf-8")

    return {
        "channel": "jira",
        "action": "stage_issues",
        "status": "staged",
        "count": len(issues),
        "files": ["jira-issues.json", "jira-issues-preview.md"],
    }


# ──────────────────────────────────────────────────────────────────────────────
# Slack agent  (intent: notify_stakeholders)
# ──────────────────────────────────────────────────────────────────────────────
def _slack_channel(m: HandoffManifest) -> str:
    """Derive a tidy channel from a product/project code in the title (e.g. cy-80)."""
    code = re.search(r"\b([a-z]{2,4}-?\d{2,3})\b", m.title, re.I)
    if code:
        return "#" + code.group(1).lower().replace("-", "") + "-program"
    cyber = re.search(r"project\s+([a-z]+)", m.title, re.I)
    if cyber:
        return "#project-" + cyber.group(1).lower()
    return "#division-decisions"


def slack_agent(m: HandoffManifest, outdir: Path) -> dict:
    channel = _slack_channel(m)
    text_lines = [f":memo: *Decision ready — {m.title}*", ""]
    for kp in (m.key_points or [m.summary])[:3]:
        text_lines.append(f"• {kp}")
    text_lines.append("")
    text_lines.append(f"{len(m.actions)} actions staged · {len(m.artifacts)} documents · awaiting approval.")
    text = "\n".join(text_lines)

    payload = {"channel": channel, "text": text}
    (outdir / "slack-post.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (outdir / "slack-post.md").write_text(f"Channel: {channel}\n\n{text}\n", encoding="utf-8")

    return {
        "channel": "slack",
        "action": "post_message",
        "status": "drafted",
        "target": channel,
        "files": ["slack-post.md", "slack-post.json"],
    }


# Intent → consumer routing table. Adding a new downstream system is one line.
ROUTES = {
    "request_approval": email_agent,
    "track_work": jira_agent,
    "notify_stakeholders": slack_agent,
}
