"""Tests for the multi-agent handoff slice (manifest + dispatcher + consumers)."""
from __future__ import annotations

import json
from pathlib import Path

from core.handoff.manifest import build_manifest_from_task, write_manifest
from core.handoff.dispatcher import dispatch

PLAN = """---
type: execution_plan
stop: 2
---
## \U0001F4CC Bottom line (30-second read)
- We can ship one day earlier if four urgent tasks finish first.
- The speed-up carries quality risk; stop if a gate fails.

---

# Execution Plan (Plain English)

## Tasks

| # | Task | Owner Department | Due | Deliverable |
|---|------|------------------|-----|-------------|
| 1 | Approve the serial-number tracking plan | 04-mfg-supplier-quality | Week 1 (2 days) | Approved tracking plan |
| 2 | Model the financial loss if a customer leaves | 06-finance | Week 2 | Risk-cost model |

## Templates to Create

| Template Name | Department | Notes |
|---------------|------------|-------|
| engineering-change-order | 02-npi-program-management | process exception |
"""


def _make_vault(tmp_path: Path, slug: str = "2026-01-01-0000-for-project-cyber-cy-80-test") -> Path:
    task = tmp_path / "02-Tasks" / slug
    task.mkdir(parents=True)
    (task / "00-brief.md").write_text(
        "---\ntype: brief\n---\n# Brief\n\nFor Project Cyber (CY-80), shorten the run by 1 day.\n",
        encoding="utf-8",
    )
    (task / "08-execution-plan.md").write_text(PLAN, encoding="utf-8")
    out = tmp_path / "03-Outputs" / slug
    out.mkdir(parents=True)
    (out / "engineering-change-order.docx").write_bytes(b"PK\x03\x04 fake docx")
    (out / "README.md").write_text("# outputs\n", encoding="utf-8")
    return task


def test_manifest_parses_actions_and_artifacts(tmp_path: Path):
    task = _make_vault(tmp_path)
    m = build_manifest_from_task(task)

    assert len(m.actions) == 2
    assert m.actions[0].id == "T1"
    assert m.actions[0].owners == ["04-mfg-supplier-quality"]
    assert m.actions[0].priority == "high"          # "Week 1" → high
    assert m.actions[1].priority == "normal"        # "Week 2" → normal
    # README.md and handoff.json excluded; only the .docx counted
    assert len(m.artifacts) == 1
    assert m.artifacts[0].type == "docx"
    assert m.artifacts[0].path.startswith("03-Outputs/")


def test_classification_and_intents(tmp_path: Path):
    task = _make_vault(tmp_path)
    m = build_manifest_from_task(task)
    assert m.classification == "confidential"        # "cyber" keyword
    assert set(m.intents) == {"notify_stakeholders", "track_work", "request_approval"}
    # recipients are roles/depts, never raw emails
    assert all("@" not in r.dept for r in m.recipients)
    assert any(r.role == "approver" for r in m.recipients)


def test_write_manifest_is_valid_json(tmp_path: Path):
    task = _make_vault(tmp_path)
    m = build_manifest_from_task(task)
    out = tmp_path / "03-Outputs" / task.name
    path = write_manifest(m, out)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    assert data["policy"]["external_actions"] == "draft_only"
    assert len(data["actions"]) == 2


def test_dispatch_prepares_drafts_only(tmp_path: Path):
    task = _make_vault(tmp_path)
    m = build_manifest_from_task(task)
    out = tmp_path / "03-Outputs" / task.name
    results = dispatch(m, out)

    by_channel = {r.get("channel"): r for r in results if r.get("channel")}
    assert by_channel["jira"]["count"] == 2
    assert by_channel["email"]["status"] == "drafted"
    assert by_channel["slack"]["status"] == "drafted"

    hd = out / "handoff"
    assert (hd / "email-draft.md").exists()
    assert (hd / "jira-issues.json").exists()
    assert (hd / "slack-post.md").exists()
    # event log recorded one line per prepared action
    log_lines = (hd / "dispatch.log").read_text(encoding="utf-8").strip().splitlines()
    assert len(log_lines) == 3
    assert all(json.loads(line)["policy"] == "draft_only" for line in log_lines)

    # staged Jira issues carry idempotency labels and never auto-transition
    issues = json.loads((hd / "jira-issues.json").read_text(encoding="utf-8"))
    assert all(i["status"] == "Backlog" for i in issues)
    assert all(f"task:{m.task_id}" in i["labels"] for i in issues)


def test_dispatch_is_idempotent(tmp_path: Path):
    task = _make_vault(tmp_path)
    m = build_manifest_from_task(task)
    out = tmp_path / "03-Outputs" / task.name

    dispatch(m, out)
    second = dispatch(m, out)
    assert all(r["status"] == "skipped_idempotent" for r in second)

    # forcing re-runs the consumers
    forced = dispatch(m, out, force=True)
    assert any(r.get("status") in ("drafted", "staged") for r in forced)


def test_policy_blocks_non_draft_actions(tmp_path: Path):
    task = _make_vault(tmp_path)
    m = build_manifest_from_task(task)
    m.policy["external_actions"] = "auto_send"   # would commit → must be refused
    out = tmp_path / "03-Outputs" / task.name
    try:
        dispatch(m, out)
        assert False, "dispatcher must refuse non-draft policy"
    except PermissionError:
        pass
