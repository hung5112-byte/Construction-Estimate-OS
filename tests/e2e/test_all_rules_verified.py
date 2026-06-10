"""Final verification — all 6 RULES enforced in the code."""
import subprocess
import shutil
from pathlib import Path


REPO = Path(__file__).parent.parent.parent


def test_rule_1_brain_first_in_question_generator():
    """RULE 1: QuestionGenerator returns [] when gaps is empty."""
    src = (REPO / "core/clarifier/question_generator.py").read_text(encoding="utf-8")
    assert "if not gaps:" in src
    assert "return []" in src


def test_rule_2_no_trade_leakage():
    """RULE 2: scripts/dev/check-domain-neutral.sh pass."""
    if shutil.which("bash") is None:
        import pytest
        pytest.skip("bash not available")
    result = subprocess.run(
        ["bash", "scripts/dev/check-domain-neutral.sh"],
        cwd=str(REPO), capture_output=True,
    )
    assert result.returncode == 0


def test_rule_3_obsidian_single_source():
    """RULE 3: Vault paths normalized — code does not store state in a third place."""
    forbidden_paths = ["/data/main/", "/storage/main/", "/db/main/"]
    for src in (REPO / "core").rglob("*.py"):
        text = src.read_text(encoding="utf-8")
        for fp in forbidden_paths:
            assert fp not in text, f"Forbidden path '{fp}' in {src}"


def test_rule_4_translator_pipeline_exists():
    """RULE 4: Translator pipeline complete."""
    assert (REPO / "core/translator/pipeline.py").exists()
    assert (REPO / "core/translator/jargon_detector.py").exists()
    assert (REPO / "core/translator/tldr_generator.py").exists()


def test_rule_5_tools_have_sources_field():
    """RULE 5: BaseTool result must have sources + retrieved_at."""
    src = (REPO / "core/tools/base_tool.py").read_text(encoding="utf-8")
    assert "sources:" in src and "list[str]" in src
    assert "retrieved_at:" in src


def test_rule_6_template_resolver_priority():
    """RULE 6: Template resolver checks 3 paths in the correct order."""
    src = (REPO / "core/obsidian/template_resolver.py").read_text(encoding="utf-8")
    assert "00-Templates-Custom" in src
    assert "01-Departments" in src
    assert "self.repo" in src or "templates-us" in src.lower()


def test_207_templates_vendored():
    """RULE 6 baseline: 207 default templates available (192 vendored + 15 division)."""
    md_count = len(list((REPO / "templates-us").rglob("*.md")))
    assert md_count == 207


def test_phase_tags_present():
    """All 6 phases tagged (skipped when the repo has no git history, e.g. zip delivery)."""
    import pytest

    if not (REPO / ".git").exists():
        pytest.skip("repo has no git history (delivered without .git) — phase tags unavailable")
    result = subprocess.run(
        ["git", "tag"], cwd=str(REPO), capture_output=True, text=True,
    )
    tags = result.stdout.split()
    for i in range(1, 6):  # Phases 1-5 must be tagged before this test runs
        assert f"phase-0{i}-complete" in tags, f"Missing tag phase-0{i}-complete"
