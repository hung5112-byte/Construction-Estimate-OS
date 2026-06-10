from unittest.mock import MagicMock
import json
from core.orchestrator.research_phase import ResearchPhase


def test_research_phase_writes_findings_file(tmp_path):
    llm = MagicMock(complete=MagicMock(return_value=json.dumps({
        "tools": [{"tool": "industry_benchmark", "queries": ["saas_b2b cac"]}]
    })))

    rp = ResearchPhase(llm=llm)
    results = rp.run(
        brief="Test", brain_summary="...", task_folder=tmp_path,
    )

    assert "industry_benchmark" in results
    assert (tmp_path / "03b-research-findings.md").exists()
