"""Build the handoff contract from a finished task.

The contract is a small, self-describing JSON envelope that downstream agents
consume instead of re-parsing .docx files. Everything here is derived from
artifacts the pipeline already produces:

    02-Tasks/<slug>/08-execution-plan.md   → actions[], key_points, intents
    02-Tasks/<slug>/00-brief.md            → title
    02-Tasks/<slug>/01-routing.md          → recipients (informed), classification hint
    03-Outputs/<slug>/*.docx|*.xlsx        → artifacts[]

No LLM call is needed: the execution plan is already structured.
"""
from __future__ import annotations

import dataclasses
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "1.0"
PRODUCED_BY = "bd-business-os"

# Department codes used across the vault, in canonical order.
DEPARTMENTS = [
    "01-bid-coordination",
    "02-civil-structural",
    "03-architectural",
    "04-mep",
    "05-cost-engineering",
    "06-estimate-review",
]
# The department that signs off by default when none is obvious from the plan.
DEFAULT_APPROVER = "02-civil-structural"
# Keywords that classify a task as confidential (→ local-model routing).
CONFIDENTIAL_HINTS = ("cyber", "classified", "itar", "ear", "defense", "export-control")


# ──────────────────────────────────────────────────────────────────────────────
# Data model
# ──────────────────────────────────────────────────────────────────────────────
@dataclass
class Action:
    """One row of the execution plan's Tasks table → one unit of trackable work."""

    id: str
    title: str
    owners: list[str]
    due: str
    deliverable: str
    priority: str = "normal"  # "high" | "normal"


@dataclass
class Artifact:
    """A document the pipeline rendered into 03-Outputs/<slug>/."""

    path: str  # vault-relative for portability
    type: str  # "docx" | "xlsx" | ...
    title: str


@dataclass
class Recipient:
    """A stakeholder, expressed as a role + department — never a raw email.

    Real addresses are resolved by the email agent at draft time so no PII
    lives in the artifact or in version control.
    """

    role: str  # "approver" | "responsible" | "informed"
    dept: str


@dataclass
class HandoffManifest:
    task_id: str
    title: str
    summary: str
    classification: str
    intents: list[str]
    key_points: list[str] = field(default_factory=list)
    artifacts: list[Artifact] = field(default_factory=list)
    actions: list[Action] = field(default_factory=list)
    recipients: list[Recipient] = field(default_factory=list)
    policy: dict = field(default_factory=lambda: {
        "external_actions": "draft_only",
        "needs_human_approval": True,
    })
    schema_version: str = SCHEMA_VERSION
    produced_by: str = PRODUCED_BY
    produced_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────────────────────────────────────
# Markdown helpers
# ──────────────────────────────────────────────────────────────────────────────
def _strip_md(cell: str) -> str:
    """Remove bold/code emphasis so values are clean for machines."""
    cell = re.sub(r"\*\*(.+?)\*\*", r"\1", cell)
    cell = cell.replace("`", "").replace("*", "")
    return cell.strip()


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def _find_table(text: str, heading: str) -> list[dict]:
    """Return rows (as dicts keyed by header) of the first markdown table that
    appears after ``heading``. Empty list if not found."""
    lines = text.splitlines()
    start = None
    target = heading.strip().lower()
    for i, ln in enumerate(lines):
        if ln.strip().lower() == target:
            start = i
            break
    if start is None:
        return []

    # Collect the first contiguous block of pipe-rows after the heading.
    block: list[str] = []
    seen_table = False
    for ln in lines[start + 1:]:
        if ln.strip().startswith("|"):
            seen_table = True
            block.append(ln.strip())
        elif seen_table:
            break  # table ended
    if len(block) < 2:
        return []

    def cells(row: str) -> list[str]:
        return [c for c in row.strip().strip("|").split("|")]

    header = [_strip_md(c) for c in cells(block[0])]
    rows: list[dict] = []
    for row in block[2:]:  # skip header + separator
        vals = [_strip_md(c) for c in cells(row)]
        if not any(vals):
            continue
        rows.append({header[i]: (vals[i] if i < len(vals) else "") for i in range(len(header))})
    return rows


def _extract_bottom_line(text: str) -> list[str]:
    """Bullets under the 'Bottom line' heading."""
    lines = text.splitlines()
    out: list[str] = []
    capturing = False
    for ln in lines:
        s = ln.strip()
        if "bottom line" in s.lower() and s.startswith("#"):
            capturing = True
            continue
        if capturing:
            if s.startswith("- "):
                out.append(_strip_md(s[2:]))
            elif s.startswith("#") or s == "---":
                break
    return out


# ──────────────────────────────────────────────────────────────────────────────
# Builder
# ──────────────────────────────────────────────────────────────────────────────
def _classify(brief: str, title: str) -> str:
    blob = f"{brief} {title}".lower()
    return "confidential" if any(h in blob for h in CONFIDENTIAL_HINTS) else "internal"


def _derive_intents(actions: list[Action]) -> list[str]:
    intents = ["notify_stakeholders"]
    if actions:
        intents.append("track_work")
    needs_approval = any(
        a.priority == "high"
        or re.search(r"\b(approve|release funds|sign[- ]?off|authoriz)", a.title, re.I)
        for a in actions
    )
    if needs_approval:
        intents.append("request_approval")
    return intents


def build_manifest_from_task(task_folder: Path, output_folder: Path | None = None) -> HandoffManifest:
    """Construct a HandoffManifest from a completed task folder.

    task_folder: <vault>/02-Tasks/<slug>/  (must contain 08-execution-plan.md)
    output_folder: defaults to <vault>/03-Outputs/<slug>/
    """
    task_folder = Path(task_folder)
    slug = task_folder.name
    vault_root = task_folder.parent.parent
    output_folder = Path(output_folder) if output_folder else vault_root / "03-Outputs" / slug

    plan_path = task_folder / "08-execution-plan.md"
    if not plan_path.exists():
        raise FileNotFoundError(f"No execution plan at {plan_path} — run bd_approve first.")
    plan = plan_path.read_text(encoding="utf-8")

    # --- title (from the brief) ---
    title = slug
    brief_text = ""
    brief_path = task_folder / "00-brief.md"
    if brief_path.exists():
        brief_body = _strip_frontmatter(brief_path.read_text(encoding="utf-8"))
        brief_body = re.sub(r"^#.*$", "", brief_body, flags=re.M).strip()
        brief_text = brief_body
        first = next((line.strip() for line in brief_body.splitlines() if line.strip()), "")
        if first:
            # first sentence, capped
            title = re.split(r"(?<=[.!?])\s", first)[0][:90].rstrip(" .") or slug

    # --- actions (Tasks table) ---
    actions: list[Action] = []
    for i, row in enumerate(_find_table(plan, "## Tasks"), start=1):
        task_txt = row.get("Task", "")
        if not task_txt:
            continue
        owners = [o.strip() for o in re.split(r"[,/]| and ", row.get("Owner Department", "")) if o.strip()]
        due = row.get("Due", "")
        priority = "high" if "week 1" in due.lower() else "normal"
        actions.append(Action(
            id=f"T{i}",
            title=task_txt,
            owners=owners or ["unassigned"],
            due=due,
            deliverable=row.get("Deliverable", ""),
            priority=priority,
        ))

    # --- key points / summary (bottom line) ---
    key_points = _extract_bottom_line(plan)
    summary = " ".join(key_points) if key_points else f"Execution plan for {title}."

    # --- artifacts (rendered outputs) ---
    artifacts: list[Artifact] = []
    if output_folder.exists():
        for p in sorted(output_folder.iterdir()):
            if p.is_dir() or p.name.lower() in {"readme.md", "handoff.json"} or p.name.startswith("."):
                continue
            ext = p.suffix.lstrip(".").lower()
            if ext not in {"docx", "xlsx", "pdf", "pptx"}:
                continue
            rel = p.relative_to(vault_root).as_posix()
            artifacts.append(Artifact(path=rel, type=ext, title=p.stem.replace("-", " ").replace("_", " ").title()))

    # --- recipients (roles, not addresses) ---
    owners_seen: list[str] = []
    for a in actions:
        for o in a.owners:
            if o in DEPARTMENTS and o not in owners_seen:
                owners_seen.append(o)
    approver = DEFAULT_APPROVER if DEFAULT_APPROVER in owners_seen or not owners_seen else owners_seen[0]
    recipients = [Recipient("approver", approver)]
    recipients += [Recipient("responsible", o) for o in owners_seen if o != approver]
    if "03-architectural" in DEPARTMENTS and "03-architectural" not in owners_seen:
        recipients.append(Recipient("informed", "03-architectural"))

    return HandoffManifest(
        task_id=slug,
        title=title,
        summary=summary,
        classification=_classify(brief_text, title),
        intents=_derive_intents(actions),
        key_points=key_points,
        artifacts=artifacts,
        actions=actions,
        recipients=recipients,
    )


def write_manifest(manifest: HandoffManifest, output_folder: Path) -> Path:
    """Write handoff.json into the task's output folder; return its path."""
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    path = output_folder / "handoff.json"
    path.write_text(manifest.to_json(), encoding="utf-8")
    return path
