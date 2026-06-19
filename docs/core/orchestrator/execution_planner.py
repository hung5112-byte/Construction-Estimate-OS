"""Generate structured execution plan from decision report (P0.2 fix).

Input:  07-decision-report.md  (written by Synthesizer after meeting)
Output: 08-execution-plan.md  (structured YAML frontmatter + markdown body)

Structure of the generated plan:
  - tasks: list of {title, owner, deadline, deliverable}
  - resources: {budget, headcount}
  - risks: list of {risk, mitigation}
  - kpis: list of {metric, target, timeframe}
  - templates_needed: list of {name, dept_code}  ← used by DocumentExecutor
"""
from __future__ import annotations
import logging
from pathlib import Path

log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# System prompt for execution plan generation (English, Department-Head-friendly)
# ──────────────────────────────────────────────────────────────────────────────
_SYSTEM_PROMPT = """You are the strategist who coordinates the execution plan for the company.
Task: read the Decision Report and produce a complete EXECUTION PLAN.

Return in exactly this format:

---
type: execution_plan
stop: 2
---
# Execution plan

## Tasks

| # | Task | Owner dept | Due | Deliverable |
|---|------|-----------|-----|-------------|
| 1 | ...  | ...       | ... | ...         |

## Resources

- **Estimated budget:** ...
- **Additional headcount:** ...

## Risks and mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| ...  | High     | ...        |

## Success metrics (KPI)

| Metric | Target | Timeframe |
|--------|--------|-----------|
| ...    | ...    | ...       |

## Templates to create

| Template name | Dept | Notes |
|---------------|------|-------|
| engineering-change-order | 02-npi-program-management | Change with disposition |
| rma-process-sop | 05-service-operations | Returns process |

RULES:
- Plain English, avoid technical jargon
- Keep the numbers from the Decision Report unchanged
- "Templates to create" table: list only practical recommendations (1-5 templates), do not invent
- Owner dept uses the code (e.g. 03-quality-reliability, 04-mfg-supplier-quality)
- Due: a specific date or "Week X" from the approval date
"""


_DIVISION_DEPTS = [
    "01-hardware-engineering",
    "02-npi-program-management",
    "03-quality-reliability",
    "04-mfg-supplier-quality",
    "05-service-operations",
]


def _available_templates(templates_root: Path) -> dict[str, list[str]]:
    """Catalog of real template slugs per dept (finance routed from _shared/03-finance)."""
    index: dict[str, list[str]] = {}
    for dept in _DIVISION_DEPTS:
        folder = templates_root / dept
        if folder.is_dir():
            index[dept] = sorted(p.stem for p in folder.glob("*.md"))
    fin = templates_root / "_shared" / "03-finance"
    if fin.is_dir():
        index["06-finance"] = sorted(p.stem for p in fin.glob("*.md"))
    return {k: v for k, v in index.items() if v}


def _catalog_text(index: dict[str, list[str]]) -> str:
    out: list[str] = []
    for dept, slugs in index.items():
        out.append(f"[{dept}]")
        out.extend(f"- {s}" for s in slugs)
    return "\n".join(out)


def _grounded_prompt(templates_root: Path | None) -> str:
    """Append the real template catalog so the planner cannot invent template names."""
    if not templates_root:
        return _SYSTEM_PROMPT
    index = _available_templates(Path(templates_root))
    if not index:
        return _SYSTEM_PROMPT
    return _SYSTEM_PROMPT + (
        "\n\nAVAILABLE TEMPLATES — for the 'Templates to create' table you MUST pick "
        "names ONLY from this catalog. Use the exact slug shown and the dept code in "
        "[brackets]. If no listed template fits a document you need, OMIT it — never "
        "invent a template name.\n\n" + _catalog_text(index)
    )


def generate_execution_plan(
    task_folder: Path,
    llm,
    translator,
    templates_root: Path | None = None,
) -> Path:
    """Read 07-decision-report.md, call LLM, write 08-execution-plan.md.

    Args:
        task_folder: path to the task folder containing decision report.
        llm: LLM provider with .complete(messages) interface.
        translator: TranslatorPipeline instance (RULE 4).

    Returns:
        Path to the written 08-execution-plan.md.

    Raises:
        FileNotFoundError: if 07-decision-report.md does not exist.
    """
    decision_path = task_folder / "07-decision-report.md"
    if not decision_path.exists():
        raise FileNotFoundError(
            f"07-decision-report.md not found in {task_folder}. "
            "Run bd_meeting first to generate the decision report."
        )

    decision_text = decision_path.read_text(encoding="utf-8")

    # Build prompt: include the full decision report as context
    messages = [
        {"role": "system", "content": _grounded_prompt(templates_root)},
        {
            "role": "user",
            "content": (
                "DECISION REPORT:\n\n"
                f"{decision_text}\n\n"
                "Generate the execution plan in exactly the format described above."
            ),
        },
    ]

    try:
        raw_plan = llm.complete(messages)
    except Exception as exc:
        log.error("LLM call failed during execution plan generation: %s", exc)
        raise

    # Apply translator pipeline (RULE 4 — Department-Head-friendly language)
    try:
        translated_plan = translator.apply(raw_plan)
    except Exception as exc:
        log.warning(
            "Translator failed during execution plan generation (%s), using raw output.",
            exc,
        )
        translated_plan = raw_plan

    # Ensure YAML frontmatter present (defensive: LLM may omit it)
    if not translated_plan.strip().startswith("---"):
        translated_plan = (
            "---\ntype: execution_plan\nstop: 2\n---\n" + translated_plan
        )

    out_path = task_folder / "08-execution-plan.md"
    out_path.write_text(translated_plan, encoding="utf-8")
    log.info("Execution plan written to %s", out_path)
    return out_path


def parse_templates_from_plan(plan_path: Path) -> list[dict]:
    """Parse the 'Templates to create' table from 08-execution-plan.md.

    Returns list of dicts: [{name: str, dept_code: str}, ...]
    Falls back to [] if table not found.
    """
    try:
        text = plan_path.read_text(encoding="utf-8")
    except OSError as exc:
        log.warning("Cannot read execution plan at %s: %s", plan_path, exc)
        return []

    templates: list[dict] = []
    in_table = False

    for line in text.splitlines():
        stripped = line.strip()

        # Detect start of the templates table
        if "templates to create" in stripped.lower():
            in_table = True
            continue

        if not in_table:
            continue

        # Table rows start with |
        if not stripped.startswith("|"):
            # End of table only on a new heading — blank lines between heading
            # and table header are allowed.
            if stripped.startswith("#"):
                in_table = False
            continue

        # Skip header/divider rows
        if "---" in stripped or "template name" in stripped.lower():
            continue

        # Parse | name | dept | notes |
        parts = [p.strip() for p in stripped.split("|") if p.strip()]
        if len(parts) >= 2:
            name = parts[0].strip()
            dept = parts[1].strip()
            # Skip if name looks like a header
            if name and dept and name.lower() not in ("template name", "#", "task"):
                templates.append({"name": name, "dept_code": dept})

    log.debug("Parsed %d template requests from execution plan", len(templates))
    return templates
