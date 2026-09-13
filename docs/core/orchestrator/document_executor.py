"""Render documents from execution plan via DocWriter + TemplateResolver (P0.1 fix).

Flow:
  1. Parse template requests from 08-execution-plan.md
  2. For each request: TemplateResolver.resolve(name, dept_code)
  3. DocWriter.write_docx() or write_xlsx() depending on resolved extension
  4. Write outputs to <vault>/03-Outputs/<task-folder-name>/
  5. Return list of generated file paths + list of skipped items

Fallback: if execution plan has no template table, LLM extracts template
requests from plan body text.
"""
from __future__ import annotations
import logging
from pathlib import Path

log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# LLM fallback prompt: extract template requests when table is absent/empty
# ──────────────────────────────────────────────────────────────────────────────
_EXTRACT_TEMPLATES_PROMPT = """You are a technical assistant. Read the execution plan below and extract
the list of TEMPLATES to create.

Return a JSON array (JSON only, nothing else):
[
  {{"name": "pre-bid-rfi-log", "dept_code": "01-bid-coordination"}},
  {{"name": "estimate-summary", "dept_code": "05-cost-engineering"}}
]

Suggest only 1-5 practical templates. Use the department codes (01-bid-coordination,
02-civil-structural, 03-architectural, 04-mep, 05-cost-engineering, 06-estimate-review).

EXECUTION PLAN:
{plan_text}
"""


def _llm_extract_templates(plan_text: str, llm) -> list[dict]:
    """Ask LLM to extract template requests when structured table is absent."""
    import json

    messages = [
        {
            "role": "system",
            "content": _EXTRACT_TEMPLATES_PROMPT.format(plan_text=plan_text[:3000]),
        },
        {"role": "user", "content": "Extract the templates."},
    ]
    try:
        raw = llm.complete(messages)
        # Find JSON array in response
        import re
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as exc:
        log.warning("LLM template extraction failed: %s", exc)
    return []


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


_DOC_GEN_PROMPT = """You are producing a FINISHED, ready-to-file {doc_label} for a hardware
engineering & supply chain division. Follow the TEMPLATE's structure, but do NOT copy its meta
sections ("Description", "Information to collect", "Suggested template", "File-generation prompt").
Output ONLY the finished document in clean markdown — a clear title (#), section headings (##),
real markdown tables where the structure calls for them, and specific content drawn from the
decision and plan below. Fill in concrete part numbers, costs, owners, dates, decisions, KPI
targets, dispositions and approvals from the context. No placeholders, no brackets, no "[TBD]" —
write it as if it is being filed today.

TEMPLATE (structure to follow):
{template}

DECISION REPORT (the approved solution to document):
{decision}

EXECUTION PLAN (tasks, owners, gates):
{plan}

TASK BRIEF:
{brief}
"""


def _generate_filled(template_text: str, task_folder: Path, doc_label: str, llm) -> str | None:
    """LLM-generate the filled document from the template structure + this task's decision + plan."""
    if llm is None:
        return None
    prompt = _DOC_GEN_PROMPT.format(
        doc_label=doc_label,
        template=template_text[:3500],
        decision=_read(task_folder / "07-decision-report.md")[:7000],
        plan=_read(task_folder / "08-execution-plan.md")[:4000],
        brief=_read(task_folder / "00-brief.md")[:800],
    )
    try:
        import re
        out = llm.complete([
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Produce the finished document now — markdown only, no commentary."},
        ]).strip()
        out = re.sub(r"^```(?:markdown)?\s*", "", out)
        out = re.sub(r"\s*```$", "", out).strip()
        return out if len(out) > 200 else None
    except Exception as exc:  # noqa: BLE001
        log.warning("Doc generation failed for %s: %s", doc_label, exc)
        return None


def execute_documents(
    task_folder: Path,
    vault_root: Path,
    repo_root: Path,
    llm,
    brain_context: dict | None = None,
) -> dict:
    """Render documents from execution plan.

    Args:
        task_folder: task folder containing 08-execution-plan.md.
        vault_root: vault root (for TemplateResolver + output path).
        repo_root: repo root (for TemplateResolver fallback templates).
        llm: LLM provider (used only for fallback template extraction).
        brain_context: optional brain context dict for substitutions.

    Returns:
        dict with keys:
          - generated: list[str] relative paths of generated files
          - skipped: list[str] template names that had no resolved template
          - outputs_dir: str absolute path to outputs directory
    """
    from core.obsidian.doc_writer import DocWriter
    from core.obsidian.template_resolver import TemplateResolver
    from core.orchestrator.execution_planner import parse_templates_from_plan

    plan_path = task_folder / "08-execution-plan.md"
    if not plan_path.exists():
        raise FileNotFoundError(
            f"08-execution-plan.md not found in {task_folder}. "
            "Run bd_approve first."
        )

    # Parse template requests from structured table
    template_requests = parse_templates_from_plan(plan_path)

    # Fallback: LLM extraction if structured table is absent/empty
    if not template_requests:
        log.info("No template table found in execution plan — using LLM extraction fallback.")
        plan_text = plan_path.read_text(encoding="utf-8")
        template_requests = _llm_extract_templates(plan_text, llm)

    repo_templates = repo_root / "templates-us"
    if not repo_templates.is_dir():
        # Self-heal: caller passed a root without templates-us — resolve robustly.
        from core.paths import templates_root
        repo_templates = templates_root()
    resolver = TemplateResolver(vault_root=vault_root, repo_templates=repo_templates)

    outputs_dir = vault_root / "03-Outputs" / task_folder.name
    outputs_dir.mkdir(parents=True, exist_ok=True)
    writer = DocWriter(output_root=outputs_dir)

    # Build substitution context from brain + plan metadata
    substitutions = _build_substitutions(task_folder, brain_context)

    generated: list[str] = []
    skipped: list[str] = []

    for req in template_requests:
        tname = req.get("name", "").strip()
        dept = req.get("dept_code", "").strip()

        if not tname:
            continue

        # Resolve template path (BYOT > pack > default per RULE 6)
        resolved = resolver.resolve(tname, dept)

        if not resolved:
            log.warning(
                "Template '%s' (dept=%s) not found — skipping. "
                "Add to vault/00-Templates-Custom/%s/ to override.",
                tname, dept, dept,
            )
            skipped.append(f"{tname} (dept={dept})")
            continue

        ext = resolved.suffix.lower()
        out_rel = f"{tname}{ext}"

        try:
            if ext == ".xlsx":
                out_path = writer.write_xlsx(
                    template_path=resolved,
                    output_rel=out_rel,
                    rows=[substitutions],
                )
            elif ext == ".docx":
                out_path = writer.write_docx(
                    template_path=resolved,
                    output_rel=out_rel,
                    substitutions=substitutions,
                )
            else:
                # .md template → LLM-generate the FILLED document from the template
                # structure + this task's decision report + execution plan, then render.
                template_text = _read(resolved)
                filled = _generate_filled(template_text, task_folder, tname.replace("-", " "), llm)
                out_path = writer.write_docx_text(
                    filled or template_text,
                    out_rel.replace(ext, ".docx"),
                    substitutions,
                )
            rel = out_path.relative_to(vault_root)
            generated.append(str(rel))
            log.info("Generated: %s (from %s)", rel, resolved.name)

        except Exception as exc:
            log.warning(
                "Failed to render template '%s' from %s: %s — skipping.",
                tname, resolved, exc,
            )
            skipped.append(f"{tname} (error: {exc})")

    # Write README manifest (complements, not replaces, real docs)
    _write_manifest(outputs_dir, task_folder.name, generated, skipped)

    return {
        "generated": generated,
        "skipped": skipped,
        "outputs_dir": str(outputs_dir),
    }


def _build_substitutions(task_folder: Path, brain_context: dict | None) -> dict:
    """Build {{key}} substitution map from brain context + task metadata."""
    subs: dict = {
        "task_id": task_folder.name,
        "task_folder": task_folder.name,
    }

    # Read brief for company name / task context
    brief_path = task_folder / "00-brief.md"
    if brief_path.exists():
        brief_text = brief_path.read_text(encoding="utf-8")
        parts = brief_text.split("---", 2)
        body = (parts[2] if len(parts) >= 3 else brief_text).strip()
        subs["brief"] = body[:500]

    if brain_context:
        # Flatten top-level string/int fields from brain into substitutions
        for k, v in brain_context.items():
            if isinstance(v, (str, int, float)):
                subs[k] = str(v)
            elif isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    if isinstance(sub_v, (str, int, float)):
                        subs[f"{k}_{sub_k}"] = str(sub_v)

    return subs


def _write_manifest(
    outputs_dir: Path,
    task_name: str,
    generated: list[str],
    skipped: list[str],
) -> None:
    """Write README.md manifest listing generated + skipped files."""
    lines = [f"# Outputs for {task_name}\n"]

    if generated:
        lines.append("## Documents created\n")
        for g in generated:
            lines.append(f"- {g}")
        lines.append("")

    if skipped:
        lines.append("## Templates not found (skipped)\n")
        for s in skipped:
            lines.append(f"- {s}")
        lines.append("")

    if not generated and not skipped:
        lines.append("_No templates were requested in the execution plan._\n")

    (outputs_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")
