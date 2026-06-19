"""Single-call document drafting — bypass the debate engine for boilerplate docs.

Use case: simple SOPs, ECO forms, RMA disposition letters, work instructions,
checklists, supplier letters, policies — no multi-agent debate needed, just
Brain context + 1 LLM call to render the full content.

Trade-off: fast (~10-30s instead of 1-3 minutes) but NO pro/con review and
NO citation validation. Only use for docs with a clear template/structure.

When to use bd_meeting/bd_run instead:
  - Strategic decisions (new ODM, factory transfer, certification program, EOL)
  - Significant legal/financial/quality risk
  - Needs multi-perspective review

Output: <vault>/02-Tasks/<ts>-draft-<slug>/draft.md (frontmatter + body).
"""
from __future__ import annotations
from datetime import datetime
from pathlib import Path

from core.brain.reader import BrainReader
from core.obsidian.vault import ObsidianVault


_DRAFT_PROMPT = """You are a document drafting specialist for a US hardware engineering & supply chain division (Texas).

Draft one complete Markdown document based on the manager's request + Brain context.

MANAGER REQUEST:
{brief}

DOCUMENT TYPE: {doc_type}

BRAIN CONTEXT (division info):
{brain_summary}

RULES:
1. Natural US English, professional tone; hardware-industry terms are fine but define
   them on first use (ECO, RMA, AQL, ...).
2. Reference US federal / Texas law and applicable standards when relevant (e.g.
   FCC Part 15, UL/IEC safety, Magnuson-Moss warranty, customs/HTS rules, the Texas
   Business Organizations Code). This is general information, NOT legal advice —
   recommend confirming with a licensed Texas attorney/broker/lab where appropriate.
3. Fill in division info from the Brain (products, sites, terms); use placeholders
   [...] for parts the manager must fill in.
4. Standard Markdown formatting: H1/H2 headings, lists, tables where needed.
5. Do NOT add your own "AI note / disclaimer" section at the end.

Return ONLY the Markdown content (no explanation, not wrapped in a code fence).
"""


def _prepare_draft(brief: str, vault_root: Path, doc_type: str) -> tuple[Path, list[dict]]:
    """Common setup for sync/async draft: create the task folder, write brief, build messages."""
    vault = ObsidianVault(vault_root)

    from core.orchestrator.flow_controller import _slugify
    slug = "draft-" + _slugify(brief, max_len=40)
    task_folder = vault.create_task_folder(slug)

    brain_summary = "(Brain not initialized)"
    try:
        brain = BrainReader(vault_root).load()
        brain_summary = brain.model_dump_json()[:2500]
    except Exception:
        pass

    (task_folder / "00-brief.md").write_text(
        f"---\ntype: brief\ndoc_type: {doc_type}\n---\n# Brief\n\n{brief}\n",
        encoding="utf-8",
    )

    messages = [
        {
            "role": "system",
            "content": _DRAFT_PROMPT.format(
                brief=brief, doc_type=doc_type, brain_summary=brain_summary,
            ),
        },
        {"role": "user", "content": f"Draft the {doc_type} per the request above."},
    ]
    return task_folder, messages


def _finalize_draft(task_folder: Path, body: str, doc_type: str, vault_root: Path) -> dict:
    """Strip fences, write draft.md, return result dict."""
    body = body.strip()
    if body.startswith("```"):
        lines = body.splitlines()
        if len(lines) >= 2:
            body = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    draft_path = task_folder / "draft.md"
    draft_path.write_text(
        f"---\ntype: draft\ndoc_type: {doc_type}\ngenerated_at: {ts}\n"
        f"source: bd_draft (single-call, no debate)\n---\n\n{body}\n",
        encoding="utf-8",
    )
    return {
        "task_folder": str(task_folder),
        "draft_path": str(draft_path),
        "message": (
            f"Drafted the {doc_type} at {draft_path.relative_to(vault_root)}. "
            "Note: this is a single-call draft, not reviewed from multiple perspectives. "
            "For a major decision, run bd_run/bd_meeting to debate it."
        ),
    }


def draft_document(
    brief: str,
    vault_root: Path,
    llm,
    doc_type: str = "document",
) -> dict:
    """Sync version — used for the CLI / tests. Do NOT use from a sync MCP tool (deadlock)."""
    task_folder, messages = _prepare_draft(brief, vault_root, doc_type)
    body = llm.complete(messages)
    return _finalize_draft(task_folder, body, doc_type, vault_root)


async def adraft_document(
    brief: str,
    vault_root: Path,
    llm,
    doc_type: str = "document",
) -> dict:
    """Async version — required from an async MCP tool to avoid an event-loop deadlock.

    Same logic as draft_document but awaits llm.acomplete() directly on the current
    event loop (no new loop / threading).
    """
    task_folder, messages = _prepare_draft(brief, vault_root, doc_type)
    body = await llm.acomplete(messages)
    return _finalize_draft(task_folder, body, doc_type, vault_root)
