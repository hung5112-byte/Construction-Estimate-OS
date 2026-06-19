"""Generate 00-Dashboard.md — agent / task / token-usage dashboard for the Obsidian vault.

Usage:
    python docs/scripts/agent_dashboard.py                      # vault = BD_OS_DEFAULT_VAULT or repo root
    python docs/scripts/agent_dashboard.py --vault <path>

Data sources (all read-only):
    01-Departments/*/department.yaml   agents, managers, debate roles
    02-Tasks/*/                        pipeline stage detection by file presence
    03-Outputs/<task>/                 rendered deliverables (stage DONE)
    .bd-usage.jsonl                    real token usage (logged by core/llm/usage_log.py)

Re-run any time; the output file is fully regenerated. Schedule it or run it from the
Obsidian terminal plugin for a refresh-on-demand workflow.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import yaml

# $/1M tokens (input, output). Edit to your contracted rates — costs shown are estimates.
RATES = {
    "deepseek": (0.28, 1.14),
    "claude": (3.00, 15.00),
    "mcp-sampling": (0.0, 0.0),  # subscription — no marginal cost
}

# Task-folder files produced by LLM calls (used for chars/4 estimates of old tasks)
GENERATED = (
    "03b-research-findings.md",
    "04-meeting-r1-perspectives.md",
    "05-meeting-r2-debate.md",
    "06-meeting-r3-perspectives.md",
    "07-decision-report.md",
    "08-execution-plan.md",
)


def detect_stage(task: Path, outputs_root: Path) -> tuple[str, str, str]:
    """Return (stage_label, waiting_on, next_step) for a task folder."""
    has = lambda name: (task / name).exists()  # noqa: E731
    out_dir = outputs_root / task.name
    has_outputs = out_dir.exists() and any(out_dir.iterdir())

    if has_outputs:
        return "✅ DONE", "", f"Outputs in `03-Outputs/{task.name}/`"
    if has("08-execution-plan.md"):
        return (
            "⏸️ STOP 2 — execution plan awaits approval",
            "Department Head",
            f"Review [[02-Tasks/{task.name}/08-execution-plan|execution plan]] → run `bd_execute`",
        )
    if has("07-decision-report.md"):
        return (
            "⏸️ STOP 1 — decision report awaits approval",
            "Department Head",
            f"Review [[02-Tasks/{task.name}/07-decision-report|decision report]] → run `bd_approve`",
        )
    if has("03-clarification.md") and not has("03-clarification-answered.md"):
        return (
            "⏸️ CLARIFICATION — agents have questions",
            "Department Head",
            f"Answer [[02-Tasks/{task.name}/03-clarification|clarification]] → run `bd_resume`",
        )
    if has("03b-research-findings.md") or has("04-meeting-r1-perspectives.md"):
        return (
            "🔄 MEETING incomplete",
            "system",
            f"Re-run: `.venv\\Scripts\\bd-os.exe meeting \"02-Tasks\\{task.name}\"`",
        )
    if has("01-routing.md"):
        return (
            "🔄 ROUTED — ready for meeting",
            "system",
            f"Run: `.venv\\Scripts\\bd-os.exe meeting \"02-Tasks\\{task.name}\"`",
        )
    return "🆕 BRIEF only", "system", "Run `bd_run` to route"


def task_title(task: Path) -> str:
    """First body line of 00-brief.md — skip frontmatter and headings like '# Brief'."""
    brief = task / "00-brief.md"
    if brief.exists():
        in_fm = False
        for i, line in enumerate(brief.read_text(encoding="utf-8", errors="replace").splitlines()):
            s = line.strip()
            if i == 0 and s == "---":
                in_fm = True
                continue
            if in_fm:
                in_fm = s != "---"
                continue
            if not s or s.startswith("#"):
                continue
            return s[:90] + ("…" if len(s) > 90 else "")
    return task.name


def load_departments(vault: Path) -> list[dict]:
    depts = []
    root = vault / "01-Departments"
    if not root.exists():
        return depts
    for yml in sorted(root.glob("*/department.yaml")):
        try:
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
            data["_folder"] = yml.parent.name
            depts.append(data)
        except Exception as e:  # noqa: BLE001
            print(f"warn: cannot parse {yml}: {e}", file=sys.stderr)
    return depts


def agent_activity(vault: Path, depts: list[dict]) -> dict[str, dict]:
    """Scan meeting transcripts: per-department participation + per-agent mentions."""
    stats: dict[str, dict] = {}
    for d in depts:
        stats[d["code"]] = {"meetings": 0, "last": None}
        for a in d.get("agents", []):
            stats[a] = {"mentions": 0, "last": None}

    for task in sorted((vault / "02-Tasks").glob("*/")):
        transcripts = [task / n for n in GENERATED[1:4] if (task / n).exists()]
        if not transcripts:
            continue
        text = "\n".join(
            t.read_text(encoding="utf-8", errors="replace") for t in transcripts
        ).lower()
        mtime = max(t.stat().st_mtime for t in transcripts)
        day = time.strftime("%m/%d", time.localtime(mtime))
        for d in depts:
            if d["code"].lower() in text:
                stats[d["code"]]["meetings"] += 1
                stats[d["code"]]["last"] = day
            for a in d.get("agents", []):
                # match 'ee-team' or 'ee team' (transcripts write "EE team")
                hits = text.count(a.lower()) + text.count(a.lower().replace("-", " "))
                if hits:
                    stats[a]["mentions"] += hits
                    stats[a]["last"] = day
    return stats


def read_usage(vault: Path) -> list[dict]:
    log = vault / ".bd-usage.jsonl"
    if not log.exists():
        return []
    records = []
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            records.append(json.loads(line))
        except Exception:  # noqa: BLE001
            continue
    return records


def usage_rollup(records: list[dict]) -> tuple[list[str], float]:
    """Markdown rows by provider/model + grand total cost."""
    rows, total_cost = [], 0.0
    by_key: dict[tuple[str, str], dict] = {}
    today = time.strftime("%Y-%m-%d")
    for r in records:
        key = (r.get("provider", "?"), r.get("model", "?"))
        b = by_key.setdefault(
            key, {"calls": 0, "in": 0, "out": 0, "today_in": 0, "today_out": 0, "est": False}
        )
        b["calls"] += 1
        b["in"] += r.get("prompt_tokens", 0)
        b["out"] += r.get("completion_tokens", 0)
        if str(r.get("ts", "")).startswith(today):
            b["today_in"] += r.get("prompt_tokens", 0)
            b["today_out"] += r.get("completion_tokens", 0)
        b["est"] = b["est"] or r.get("estimated", False)
    for (prov, model), b in sorted(by_key.items()):
        rate_in, rate_out = RATES.get(prov, (0.0, 0.0))
        cost = b["in"] / 1e6 * rate_in + b["out"] / 1e6 * rate_out
        total_cost += cost
        flag = " *(est.)*" if b["est"] else ""
        rows.append(
            f"| {prov} / {model}{flag} | {b['calls']} | {b['in']:,} | {b['out']:,} "
            f"| {b['today_in'] + b['today_out']:,} | ${cost:.2f} |"
        )
    return rows, total_cost


def main() -> None:
    ap = argparse.ArgumentParser()
    # Script lives at <repo>/docs/scripts/ — repo root (= vault) is three levels up.
    ap.add_argument("--vault", default=os.getenv("BD_OS_DEFAULT_VAULT") or str(Path(__file__).parent.parent.parent))
    args = ap.parse_args()
    vault = Path(args.vault).resolve()
    tasks_root, outputs_root = vault / "02-Tasks", vault / "03-Outputs"

    depts = load_departments(vault)
    stats = agent_activity(vault, depts)
    records = read_usage(vault)

    # ---- tasks & permission queue -------------------------------------------------
    pending_rows, pipeline_rows = [], []
    est_total_out = 0
    for task in sorted(tasks_root.glob("*/"), reverse=True):
        stage, waiting, next_step = detect_stage(task, outputs_root)
        title = task_title(task)
        link = f"[[02-Tasks/{task.name}/00-brief\\|{title}]]"
        gen_bytes = sum((task / n).stat().st_size for n in GENERATED if (task / n).exists())
        est_out = gen_bytes // 4
        est_total_out += est_out
        pipeline_rows.append(f"| {link} | {stage} | ~{est_out:,} |")
        if waiting == "Department Head":
            pending_rows.append(f"| {link} | {stage} | {next_step} |")
        elif waiting == "system":
            pending_rows.append(f"| {link} | {stage} | {next_step} |")

    usage_rows, total_cost = usage_rollup(records)

    # ---- agents table ---------------------------------------------------------------
    agent_lines = []
    for d in depts:
        code, mgr = d["code"], d.get("default_speaker", "")
        role = d.get("debate_role", {}).get("default", "pro")
        dstat = stats.get(code, {})
        agent_lines.append(
            f"### [[01-Departments/{d['_folder']}/index|{d.get('name_vn', code)}]] "
            f"(`{code}`) — debate role: **{role}** · meetings: {dstat.get('meetings', 0)}"
            + (f" · last: {dstat['last']}" if dstat.get("last") else "")
        )
        agent_lines.append("")
        agent_lines.append("| Agent | Role | Transcript mentions | Last active |")
        agent_lines.append("|---|---|---|---|")
        for a in d.get("agents", []):
            astat = stats.get(a, {})
            star = " ⭐ manager" if a == mgr else ""
            agent_lines.append(
                f"| [[01-Departments/{d['_folder']}/agents/{a}\\|{a}]]{star} "
                f"| {'speaks for dept' if a == mgr else 'team take (≤150 words)'} "
                f"| {astat.get('mentions', 0)} | {astat.get('last') or '—'} |"
            )
        agent_lines.append("")

    n_agents = sum(len(d.get("agents", [])) for d in depts)
    now = time.strftime("%Y-%m-%d %H:%M")
    pending_block = (
        "\n".join(pending_rows)
        if pending_rows
        else "| — | nothing waiting | enjoy the silence |"
    )

    md = f"""---
type: dashboard
aliases: ["Dashboard", "Agent Dashboard"]
generated: {now}
---
# 🎛️ Division Dashboard

> Generated **{now}** · refresh: `python docs/scripts/agent_dashboard.py` (works in the Obsidian terminal plugin)
> Agents: **{n_agents}** in **{len(depts)} departments** · Tasks: **{len(pipeline_rows)}** · LLM calls logged: **{len(records)}**

## ⏸️ Needs action — agents waiting for permission

> [!warning] Mandatory stops — the flow does not continue until these are answered
>
> | Task | Waiting at | Next step |
> |---|---|---|
> {pending_block}

## 🔄 Task pipeline

| Task | Stage | Gen. tokens (est.) |
|---|---|---|
{chr(10).join(pipeline_rows) if pipeline_rows else "| — | no tasks yet | |"}

Pipeline: `bd_run` → *(clarify?)* → `bd_meeting` → **Stop 1** `bd_approve` → **Stop 2** `bd_execute` → `.docx/.xlsx`

## 🔢 Token usage

| Provider / model | Calls | Input tok | Output tok | Today | Cost (≈) |
|---|---|---|---|---|---|
{chr(10).join(usage_rows) if usage_rows else "| no calls logged yet — usage logging starts with the next LLM call | | | | | |"}

- **Total logged cost ≈ ${total_cost:.2f}** (rates in `docs/scripts/agent_dashboard.py` → RATES; edit to your contract)
- Historical artifacts (pre-logging) estimated at chars/4: **~{est_total_out:,} generated tokens** across all task folders
- Real per-call logging: `.bd-usage.jsonl` (gitignored), written by every provider in `core/llm/providers.py`

## 🤖 Agents

{chr(10).join(agent_lines)}
---
*Auto-generated — do not edit by hand; changes are overwritten on refresh.*
"""
    out = vault / "00-Dashboard.md"
    out.write_text(md, encoding="utf-8")
    print(f"dashboard -> {out}  (tasks={len(pipeline_rows)}, pending={len(pending_rows)}, calls={len(records)})")


if __name__ == "__main__":
    main()
