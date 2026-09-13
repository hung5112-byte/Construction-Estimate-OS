"""Smoke tests: all Phase 1 modules import + work."""
from pathlib import Path
import subprocess
import sys


def test_import_all():
    """All Phase 1 modules import cleanly."""
    from core.brain.schema import BrainContext  # noqa: F401
    from core.brain.reader import BrainReader  # noqa: F401
    from core.brain.memory import DecisionLog  # noqa: F401
    from core.obsidian.vault import ObsidianVault  # noqa: F401
    from core.obsidian.frontmatter import parse  # noqa: F401
    from core.agents.department import Department, DepartmentLoader  # noqa: F401
    from core.utils.config import load_config  # noqa: F401
    from core.llm.providers import ClaudeProvider  # noqa: F401


def test_cli_status_works():
    repo = Path(__file__).parent.parent.parent
    fixture = repo / "tests" / "fixtures" / "demo-vault"
    result = subprocess.run(
        [sys.executable, "-m", "core.cli", "status", "--vault", str(fixture)],
        capture_output=True, text=True, cwd=str(repo)
    )
    assert result.returncode == 0
    assert "Brain loaded" in result.stdout


def test_dept_loader_loads_6_depts():
    from core.agents.department import DepartmentLoader
    repo = Path(__file__).parent.parent.parent
    depts = DepartmentLoader(repo / "departments").load_all()
    assert len(depts) == 6


def test_templates_us_has_180_files():
    # Lower bound for this fork: 155 generic + 9 orchestrator + 16 estimating templates;
    # additions are allowed and must not break this.
    repo = Path(__file__).parent.parent.parent
    md_files = list((repo / "templates-us").rglob("*.md"))
    assert len(md_files) >= 180
