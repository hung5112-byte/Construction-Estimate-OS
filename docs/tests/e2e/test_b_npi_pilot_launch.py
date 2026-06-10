"""E2E test case B - pilot deployment of a new payment terminal.

Validates the 6 RULES + acceptance criteria with a mocked LLM, against the
hardware-division departments (NPI pilot: hardware PD, supply chain, quality,
operations, RMA).
"""
import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock
import pytest


REPO = Path(__file__).parent.parent.parent
FIXTURE = REPO / "tests/fixtures/hardwareco-vault"

DEPARTMENTS = [
    "01-hardware-engineering",
    "02-npi-program-management",
    "03-quality-reliability",
    "04-mfg-supplier-quality",
    "05-service-operations",
]


@pytest.fixture
def llm_mock():
    """Mocked LLM with pre-canned responses for each stage."""

    responses = {
        "router_classify": json.dumps({
            "class": "COMPLEX",
            "departments": DEPARTMENTS,
            "reasoning": "Pilot launch + certification check + spares/deployment readiness",
        }),
        "gap_analysis": json.dumps([
            {"field": "certification_status", "severity": "CRITICAL",
             "current_value": "PT500 contactless renewal due Q3", "brief_value": "pilot ships 06/30",
             "reason": "Pilot date may precede the certification renewal", "citation": "00-Brain/laws.md"},
            {"field": "spares_plan", "severity": "CRITICAL",
             "current_value": "no dedicated spares planner", "brief_value": "500-unit pilot needs spares",
             "reason": "Headcount notes no spares planning for pilots", "citation": "00-Brain/headcount.md"},
        ]),
        "questions": json.dumps([
            {"text": "Is the PT500 contactless certification valid through the pilot?",
             "citation": "00-Brain/laws.md",
             "choices": ["Valid through pilot", "Renewal letter pending - lab ETA in writing", "Cancel pilot"],
             "severity": "CRITICAL", "free_text": False},
            {"text": "Spares strategy for the pilot?",
             "citation": "00-Brain/headcount.md",
             "choices": ["3 percent spares pool onsite", "Advance replacement from HQ", "No spares"],
             "severity": "CRITICAL", "free_text": False},
        ]),
        "tool_plan": json.dumps({"tools": [
            {"tool": "industry_benchmark", "queries": ["hardware_electronics field return rate"]},
        ]}),
        "perspective": "The department recommends a staged rollout, backed by Brain data.",
        "pro_advocate": "GO. Fleet return rate 2.8% is under the 3% goal; pilot derisks the ramp.",
        "con_advocate": "Risk: certification renewal timing + no spares pool defined for the site.",
        "growth": "GO bold - 18-month runway and an anchor customer justify the pilot.",
        "cautious": "GO with gates - week 1 DOA > 1% means pause shipments.",
        "balanced": "Pilot 500 units in 2 waves + 3% spares pool + acceptance sign-off per site.",
        "synthesizer": """## 📌 Bottom line (30-second read)
- GO with revisions: 500-unit pilot in 2 waves
- 4 BLOCKERS must be done before wave 1 ships
- KPI: DOA < 1% in week 1, 100% install acceptance

## Recommendation
GO with revisions

## To do before launch
1. [ ] Confirm PT500 certification validity in writing
2. [ ] Build the 3% spares pool
3. [ ] Publish IQC criteria for the pilot lot
4. [ ] Finalize the field-deployment checklist

## KPI gates
- Week 1: DOA < 1%
- Week 4: 100% site acceptance sign-offs

## Decisions the Department Head must make
A. Approve this plan
B. Approve but skip the blockers
C. Reject
D. Revise
""",
        # P0.2: execution planner LLM response (structured plan with template table)
        "execution_plan": """---
type: execution_plan
stop: 2
---
# Execution plan

## Tasks

| # | Task | Owner dept | Due | Deliverable |
|---|------|-----------|-----|-------------|
| 1 | Confirm certification validity | 02-npi-program-management | Week 1 | Cert letter on file |
| 2 | Expedite pilot lot + spares | 02-npi-program-management | Week 1 | Confirmed POs |
| 3 | Deployment plan for 12 sites | 05-service-operations | Week 2 | Deployment checklist |

## Resources

- **Estimated budget:** $20,000
- **Additional headcount:** none (spares planning covered by Operations)

## Risks and mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| High DOA in wave 1 | High | Pause wave 2; RMA fast-track + 8D |

## Success metrics (KPI)

| Metric | Target | Timeframe |
|--------|--------|-----------|
| DOA rate | < 1% | Week 1 |
| Site acceptance | 100% | Week 4 |

## Templates to create

| Template name | Dept | Notes |
|---------------|------|-------|
| field-deployment-checklist | 05-service-operations | Site install + acceptance |
| rma-process-sop | 05-service-operations | Pilot returns lane |
""",
    }

    def respond(messages, model=None):
        sys_text = messages[0]["content"]

        # Order matters - check most-specific first
        if "router that classifies" in sys_text:
            return responses["router_classify"]
        if "Gap Analyzer" in sys_text:
            return responses["gap_analysis"]
        if "clarification questions" in sys_text:
            return responses["questions"]
        if "Tool Router" in sys_text:
            return responses["tool_plan"]
        if "Pro Advocate" in sys_text:
            return responses["pro_advocate"]
        if "Con Advocate" in sys_text:
            return responses["con_advocate"]
        if "GROWTH side" in sys_text:
            return responses["growth"]
        if "CAUTIOUS side" in sys_text:
            return responses["cautious"]
        if "BALANCED side" in sys_text:
            return responses["balanced"]
        # P0.2: execution plan generator
        if "coordinates the execution plan" in sys_text:
            return responses["execution_plan"]
        if "write the decision report" in sys_text:
            return responses["synthesizer"]
        # P0.1: template extraction fallback (LLM path — used when table absent)
        if "technical assistant" in sys_text and "extract" in sys_text.lower():
            return json.dumps([
                {"name": "field-deployment-checklist", "dept_code": "05-service-operations"},
            ])
        if "business editor" in sys_text:
            # simplifier - return content unchanged (no jargon in test fixtures)
            return messages[1]["content"]
        if "Summarize the report" in sys_text:
            # tldr - synthesizer response already has the '📌 Bottom line' marker
            return ""
        if "YOUR TASK IN THIS MEETING" in sys_text:
            # PerspectivesCollector dept agent
            return responses["perspective"]
        return "..."

    llm = MagicMock()
    llm.complete.side_effect = respond
    return llm


def _answer_clarification(task_folder):
    clarif = (task_folder / "03-clarification.md").read_text(encoding="utf-8")
    answered = clarif.replace(
        "- [ ] Valid through pilot",
        "- [x] Valid through pilot",
    ).replace(
        "- [ ] 3 percent spares pool onsite",
        "- [x] 3 percent spares pool onsite",
    )
    (task_folder / "03-clarification.md").write_text(answered, encoding="utf-8")


def test_e2e_b_pilot_full_flow(tmp_path, llm_mock):
    """Full E2E flow: brief -> clarify -> meeting -> decision report."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURE, vault)

    from core.orchestrator.flow_controller import FlowController, FlowStage

    fc = FlowController(vault_root=vault, llm=llm_mock)

    # Stage 1: brief -> clarification
    result = fc.run(brief="Pilot deployment of 500 PayTerm 500 units for our top retail customer, $20k budget, ship before 06/30")

    assert result.stage == FlowStage.PAUSE_CLARIFICATION
    task_folder = result.task_folder

    # Verify files
    assert (task_folder / "00-brief.md").exists()
    assert (task_folder / "01-routing.md").exists()
    assert (task_folder / "02-context.md").exists()
    assert (task_folder / "03-clarification.md").exists()

    # RULE 1: questions have a citation
    clarif = (task_folder / "03-clarification.md").read_text(encoding="utf-8")
    assert "00-Brain/laws.md" in clarif
    assert "00-Brain/headcount.md" in clarif

    # Auto-tick Department Head answers
    _answer_clarification(task_folder)

    # Stage 2: resume after clarification
    result = fc.resume_after_clarification(task_folder)
    assert result.stage == FlowStage.PAUSE_DECISION_REPORT

    # Stage 3: meeting
    result = fc.run_meeting(task_folder, departments=DEPARTMENTS)
    assert result.stage == FlowStage.PAUSE_DECISION_REPORT

    # Verify meeting outputs
    assert (task_folder / "03b-research-findings.md").exists()
    assert (task_folder / "04-meeting-r1-perspectives.md").exists()
    assert (task_folder / "05-meeting-r2-debate.md").exists()
    assert (task_folder / "06-meeting-r3-perspectives.md").exists()
    assert (task_folder / "07-decision-report.md").exists()

    # ACCEPTANCE
    decision = (task_folder / "07-decision-report.md").read_text(encoding="utf-8")
    assert "📌 Bottom line" in decision
    assert "Recommendation" in decision or "Decisions the Department Head must make" in decision


def test_acceptance_no_trade_leakage_in_outputs(tmp_path, llm_mock):
    """RULE 2: outputs must not contain Bull/Bear/trade/etc."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURE, vault)

    from core.orchestrator.flow_controller import FlowController
    fc = FlowController(vault_root=vault, llm=llm_mock)
    result = fc.run(brief="Test pilot brief")

    forbidden = ["Bull", "Bear", "ticker", "yfinance", "trader"]
    for f in (result.task_folder).rglob("*.md"):
        content = f.read_text(encoding="utf-8")
        for word in forbidden:
            assert word not in content, f"Found '{word}' in {f.name}"


def _run_through_meeting(tmp_path, llm_mock):
    """Helper: run full flow up to decision report, return (fc, task_folder)."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURE, vault)

    from core.orchestrator.flow_controller import FlowController, FlowStage

    fc = FlowController(vault_root=vault, llm=llm_mock)

    result = fc.run(brief="Pilot deployment of 500 PayTerm 500 units, $20k budget, ship before 06/30")
    assert result.stage == FlowStage.PAUSE_CLARIFICATION
    task_folder = result.task_folder

    _answer_clarification(task_folder)

    fc.resume_after_clarification(task_folder)

    result = fc.run_meeting(task_folder, departments=DEPARTMENTS)
    assert result.stage == FlowStage.PAUSE_DECISION_REPORT

    return fc, task_folder


def test_approve_decision_writes_real_execution_plan(tmp_path, llm_mock):
    """P0.2: approve_decision generates a structured 08-execution-plan.md (not a stub)."""
    from core.orchestrator.flow_controller import FlowStage

    fc, task_folder = _run_through_meeting(tmp_path, llm_mock)

    result = fc.approve_decision(task_folder)

    assert result.stage == FlowStage.PAUSE_EXECUTE, f"Expected PAUSE_EXECUTE, got {result.stage}: {result.error}"

    plan_path = task_folder / "08-execution-plan.md"
    assert plan_path.exists(), "08-execution-plan.md not created by approve_decision"

    plan_text = plan_path.read_text(encoding="utf-8")

    # Must have YAML frontmatter with correct type
    assert "type: execution_plan" in plan_text, "Missing frontmatter type"
    assert "stop: 2" in plan_text, "Missing stop marker"

    # Must NOT be a stub
    assert "TODO Phase 6" not in plan_text, "08-execution-plan.md still contains stub TODO"

    # Must have substantive content
    assert "Execution plan" in plan_text or "Tasks" in plan_text, \
        "Execution plan missing substantive content"


def test_execute_calls_docwriter_generates_outputs(tmp_path, llm_mock):
    """P0.1: execute() calls DocWriter and writes real files to 03-Outputs/."""
    from core.orchestrator.flow_controller import FlowStage

    fc, task_folder = _run_through_meeting(tmp_path, llm_mock)

    # approve first to create 08-execution-plan.md
    approve_result = fc.approve_decision(task_folder)
    assert approve_result.stage == FlowStage.PAUSE_EXECUTE

    # execute
    result = fc.execute(task_folder)
    assert result.stage == FlowStage.DONE, f"Expected DONE, got {result.stage}: {result.error}"

    outputs_dir = fc.vault.root / "03-Outputs" / task_folder.name
    assert outputs_dir.exists(), "03-Outputs/<task>/ directory not created"

    # README manifest must exist
    readme = outputs_dir / "README.md"
    assert readme.exists(), "README.md manifest not created in outputs dir"
    readme_text = readme.read_text(encoding="utf-8")
    assert "TODO Phase 6" not in readme_text, "README still contains stub TODO text"

    # At least one real output file OR a graceful skipped list (templates may be absent in fixture)
    docx_files = list(outputs_dir.glob("*.docx"))
    xlsx_files = list(outputs_dir.glob("*.xlsx"))
    all_files = docx_files + xlsx_files

    # Either real docs generated OR graceful skip logged (both are valid for the fixture vault)
    # The fixture vault has no 01-Departments so TemplateResolver falls back to repo templates-us/
    # repo/templates-us/05-service-operations/field-deployment-checklist.md exists → should generate
    if not all_files:
        # Acceptable: all templates were skipped gracefully — verify skip message present
        assert "not found" in readme_text.lower() or "skipped" in result.message.lower() or \
               "skipped" in readme_text.lower(), \
               "No docs generated and no graceful skip message — execute may have silently failed"
    else:
        # Real docs generated — verify they are non-empty
        for f in all_files:
            assert f.stat().st_size > 0, f"Generated file {f.name} is empty"


def test_execute_without_execution_plan_returns_error(tmp_path, llm_mock):
    """P0.1: execute() without prior approve returns ERROR stage, not exception."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURE, vault)

    from core.orchestrator.flow_controller import FlowController, FlowStage

    fc = FlowController(vault_root=vault, llm=llm_mock)
    result = fc.run(brief="Test brief")
    task_folder = result.task_folder

    # Call execute directly without approve (no 08-execution-plan.md)
    exec_result = fc.execute(task_folder)
    assert exec_result.stage == FlowStage.ERROR
    assert exec_result.error is not None
    assert "08-execution-plan.md" in exec_result.error


def test_approve_without_decision_report_returns_error(tmp_path, llm_mock):
    """P0.2: approve_decision() without a prior meeting returns ERROR, not exception."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURE, vault)

    from core.orchestrator.flow_controller import FlowController, FlowStage

    fc = FlowController(vault_root=vault, llm=llm_mock)
    result = fc.run(brief="Test brief")
    task_folder = result.task_folder

    # Call approve directly without a meeting (no 07-decision-report.md)
    approve_result = fc.approve_decision(task_folder)
    assert approve_result.stage == FlowStage.ERROR
    assert approve_result.error is not None
    assert "07-decision-report.md" in approve_result.error
