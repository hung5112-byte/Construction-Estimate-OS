"""Two-minute live demo of the multi-agent handoff slice.

Run from the repo root (no API keys, nothing is sent):

    python docs/core/handoff/demo.py
    python docs/core/handoff/demo.py "02-Tasks/<some-task-folder>"

It takes a finished task, emits the handoff contract, dispatches it to the
email / Jira / Slack consumer agents (draft-only), then re-runs to prove the
flow is idempotent. Output drafts land in 03-Outputs/<slug>/handoff/.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Make `core` importable when run as a plain script (docs/ is the package root).
_DOCS = Path(__file__).resolve().parents[2]
if str(_DOCS) not in sys.path:
    sys.path.insert(0, str(_DOCS))

from core.handoff.manifest import build_manifest_from_task, write_manifest  # noqa: E402
from core.handoff.dispatcher import dispatch  # noqa: E402

VAULT_ROOT = Path(__file__).resolve().parents[3]
BAR = "─" * 74


def _step(n: int, title: str) -> None:
    print(f"\n{BAR}\n  STEP {n} — {title}\n{BAR}")


def _find_default_task() -> Path:
    """Prefer the Cyber CY-80 task; otherwise the newest task with a plan."""
    tasks = VAULT_ROOT / "02-Tasks"
    candidates = [p for p in tasks.iterdir() if p.is_dir() and (p / "08-execution-plan.md").exists()]
    if not candidates:
        raise SystemExit("No task with an 08-execution-plan.md found under 02-Tasks/.")
    for p in candidates:
        if "cyber" in p.name and "cy-80" in p.name:
            return p
    return sorted(candidates)[-1]


def run(task_folder: Path) -> None:
    slug = task_folder.name
    output_folder = VAULT_ROOT / "03-Outputs" / slug

    print(f"\n{BAR}\n  bd-business-os · multi-agent handoff  ·  task: {slug}\n{BAR}")

    # STEP 1 — a decision already exists -------------------------------------
    _step(1, "A decision + execution plan already exist (pipeline output)")
    brief = (task_folder / "00-brief.md")
    if brief.exists():
        text = brief.read_text(encoding="utf-8").split("# Brief", 1)[-1].strip()
        print(f"  Brief: {text[:140]}")
    docs = [p.name for p in sorted(output_folder.glob('*')) if p.suffix in ('.docx', '.xlsx')] if output_folder.exists() else []
    print(f"  Rendered documents in 03-Outputs/: {len(docs)}")
    for d in docs:
        print(f"     - {d}")

    # STEP 2 — emit the handoff contract -------------------------------------
    _step(2, "Emit the handoff contract  (the seam every downstream agent uses)")
    m = build_manifest_from_task(task_folder, output_folder)
    path = write_manifest(m, output_folder)
    print(f"  classification : {m.classification}"
          + ("   → reasoning routed to a LOCAL model (never leaves the building)"
             if m.classification == "confidential" else ""))
    print(f"  intents        : {', '.join(m.intents)}")
    print(f"  actions        : {len(m.actions)}   recipients: {len(m.recipients)}   artifacts: {len(m.artifacts)}")
    print(f"  → wrote {path.relative_to(VAULT_ROOT)}")

    # STEP 3 — dispatch under policy -----------------------------------------
    _step(3, "Dispatcher routes each intent to an agent  (policy: draft-only)")
    results = dispatch(m, output_folder)
    for r in results:
        detail = (f"{r.get('count')} issues" if r.get("count") is not None
                  else r.get("subject") or r.get("target") or "")
        print(f"  {r['intent']:<20} → {r.get('channel','-'):<6} [{r.get('status')}]  {detail}")

    # STEP 4 — show what was prepared (nothing sent) -------------------------
    _step(4, "What the agents PREPARED  (nothing was sent)")
    hd = output_folder / "handoff"
    email = hd / "email-draft.md"
    jira = hd / "jira-issues-preview.md"
    if email.exists():
        print("  ┌ EMAIL DRAFT " + "─" * 58)
        for ln in email.read_text(encoding="utf-8").splitlines()[:8]:
            print(f"  │ {ln}")
        print("  └" + "─" * 71)
    if jira.exists():
        print("  ┌ JIRA (staged in backlog) " + "─" * 45)
        for ln in jira.read_text(encoding="utf-8").splitlines()[:6]:
            print(f"  │ {ln}")
        print("  └" + "─" * 71)

    # STEP 5 — idempotency ---------------------------------------------------
    _step(5, "Re-run is safe  (idempotent — no duplicate tickets or drafts)")
    again = dispatch(m, output_folder)
    for r in again:
        print(f"  {r['intent']:<20} → [{r.get('status')}]")

    print(f"\n{BAR}")
    print("  Nothing left the building. A human approves these in the morning")
    print("  command center — drafts become real Gmail / Jira / Slack actions on click.")
    print(f"  Drafts: 03-Outputs/{slug}/handoff/")
    print(f"{BAR}\n")


def main() -> None:
    if len(sys.argv) > 1:
        tf = Path(sys.argv[1])
        if not tf.is_absolute():
            tf = VAULT_ROOT / tf
    else:
        tf = _find_default_task()
    run(tf)


if __name__ == "__main__":
    main()
