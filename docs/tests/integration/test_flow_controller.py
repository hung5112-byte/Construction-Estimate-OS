from unittest.mock import MagicMock
from pathlib import Path
import json
import shutil
from core.orchestrator.flow_controller import FlowController, FlowStage


def test_flow_pauses_at_clarification_when_gaps_exist(tmp_path):
    """When gaps exist → the flow creates clarification + pauses → returns PAUSE_CLARIFICATION."""

    fixture = Path(__file__).parent.parent / "fixtures" / "demo-vault"

    # Set up a temp vault
    vault = tmp_path / "vault"
    shutil.copytree(fixture, vault)

    # Need 02-Tasks dir for create_task_folder
    (vault / "02-Tasks").mkdir(exist_ok=True)

    llm = MagicMock()
    # Router output
    router_resp = json.dumps({"class": "COMPLEX", "departments": ["05-service-operations", "02-npi-program-management"], "reasoning": "x"})
    # Gap analyzer output (1 gap)
    gap_resp = json.dumps([{
        "field": "ICP", "severity": "CRITICAL",
        "current_value": "SME", "brief_value": "high income",
        "reason": "diverges", "citation": "00-Brain/strategy.md"
    }])
    # Question gen output
    q_resp = json.dumps([{
        "text": "Pivot or test?",
        "citation": "00-Brain/strategy.md",
        "choices": ["Pivot", "Test"],
        "severity": "CRITICAL",
        "free_text": False,
    }])
    llm.complete.side_effect = [router_resp, gap_resp, q_resp]

    fc = FlowController(vault_root=vault, llm=llm)
    result = fc.run(brief="Create an ad campaign targeting high-income individuals")

    assert result.stage == FlowStage.PAUSE_CLARIFICATION
    assert result.task_folder.exists()
    assert (result.task_folder / "03-clarification.md").exists()
