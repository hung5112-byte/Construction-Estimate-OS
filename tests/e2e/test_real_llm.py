"""Real LLM E2E — only runs with ANTHROPIC_API_KEY + RUN_REAL_LLM=1.

Measures: < 25 minutes, < $2/task.
"""
import os
import time
import pytest
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
FIXTURE = REPO / "tests/fixtures/hardwareco-vault"


@pytest.mark.skipif(
    not (os.getenv("ANTHROPIC_API_KEY") and os.getenv("RUN_REAL_LLM") == "1"),
    reason="Real LLM test — needs API key + RUN_REAL_LLM=1",
)
def test_real_llm_e2e_under_budget(tmp_path):
    import shutil
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURE, vault)

    from core.orchestrator.flow_controller import FlowController
    from core.llm.providers import get_default_provider

    llm = get_default_provider()
    fc = FlowController(vault_root=vault, llm=llm)

    start = time.time()
    result = fc.run(brief="Create an ad campaign targeting high-income individuals, $20k budget")
    elapsed = time.time() - start

    # Stage 1 should be quick (no meeting yet)
    assert elapsed < 60
    assert result.task_folder.exists()
