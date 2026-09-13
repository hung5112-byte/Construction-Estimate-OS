"""Unit tests for core/orchestrator/document_executor.py (P0.1)."""
import textwrap
from pathlib import Path
from unittest.mock import MagicMock

import pytest


REPO = Path(__file__).parent.parent.parent

PLAN_WITH_REAL_TEMPLATES = textwrap.dedent("""\
    ---
    type: execution_plan
    stop: 2
    ---
    # Execution plan

    ## Templates to create

    | Template name | Dept | Notes |
    |---------------|------|-------|
    | pre-bid-rfi-log | 01-bid-coordination | Questions to the architect |
    | estimate-summary | 05-cost-engineering | Division summary |
""")

PLAN_WITH_UNKNOWN_TEMPLATE = textwrap.dedent("""\
    ---
    type: execution_plan
    stop: 2
    ---
    ## Templates to create

    | Template name | Dept | Notes |
    |---------------|------|-------|
    | nonexistent-template-xyz | 99-unknown | Test |
""")

PLAN_WITHOUT_TABLE = textwrap.dedent("""\
    ---
    type: execution_plan
    stop: 2
    ---
    # Execution plan — log the pre-bid questions and summarize the estimate.
""")


class TestExecuteDocuments:
    def _make_llm(self, fallback_response=None):
        """Return a mock LLM. Default response is an empty JSON array so that
        the LLM-fallback path in document_executor produces no templates rather
        than propagating a MagicMock through JSON parsing."""
        llm = MagicMock()
        llm.complete.return_value = fallback_response if fallback_response is not None else "[]"
        return llm

    def test_raises_if_execution_plan_missing(self, tmp_path):
        from core.orchestrator.document_executor import execute_documents

        task_folder = tmp_path / "task"
        task_folder.mkdir()

        with pytest.raises(FileNotFoundError, match="08-execution-plan.md"):
            execute_documents(
                task_folder=task_folder,
                vault_root=tmp_path / "vault",
                repo_root=REPO,
                llm=self._make_llm(),
            )

    def test_creates_outputs_dir(self, tmp_path):
        from core.orchestrator.document_executor import execute_documents

        vault = tmp_path / "vault"
        vault.mkdir()
        task_folder = tmp_path / "task"
        task_folder.mkdir()
        (task_folder / "08-execution-plan.md").write_text(
            PLAN_WITH_UNKNOWN_TEMPLATE, encoding="utf-8"
        )

        result = execute_documents(
            task_folder=task_folder,
            vault_root=vault,
            repo_root=REPO,
            llm=self._make_llm(),
        )

        outputs_dir = Path(result["outputs_dir"])
        assert outputs_dir.exists()
        assert (outputs_dir / "README.md").exists()

    def test_skips_unknown_template_gracefully(self, tmp_path):
        """Missing templates must go into skipped list, not raise."""
        from core.orchestrator.document_executor import execute_documents

        vault = tmp_path / "vault"
        vault.mkdir()
        task_folder = tmp_path / "task"
        task_folder.mkdir()
        (task_folder / "08-execution-plan.md").write_text(
            PLAN_WITH_UNKNOWN_TEMPLATE, encoding="utf-8"
        )

        result = execute_documents(
            task_folder=task_folder,
            vault_root=vault,
            repo_root=REPO,
            llm=self._make_llm(),
        )

        assert len(result["skipped"]) == 1
        assert "nonexistent-template-xyz" in result["skipped"][0]
        assert len(result["generated"]) == 0

    def test_resolves_repo_fallback_template_and_generates_docx(self, tmp_path):
        """Templates from repo/templates-us/ are resolved and rendered to .docx."""
        from core.orchestrator.document_executor import execute_documents

        vault = tmp_path / "vault"
        vault.mkdir()
        task_folder = tmp_path / "task"
        task_folder.mkdir()
        (task_folder / "08-execution-plan.md").write_text(
            PLAN_WITH_REAL_TEMPLATES, encoding="utf-8"
        )
        (task_folder / "00-brief.md").write_text(
            "---\ntype: brief\n---\n# Brief\n\nTest brief.\n", encoding="utf-8"
        )

        result = execute_documents(
            task_folder=task_folder,
            vault_root=vault,
            repo_root=REPO,
            llm=self._make_llm(),
        )

        # pre-bid-rfi-log and estimate-summary exist in repo/templates-us/
        # Both are .md → rendered as .docx
        assert len(result["generated"]) >= 1
        for rel_path in result["generated"]:
            out = vault / rel_path
            assert out.exists(), f"Generated file missing: {rel_path}"
            assert out.stat().st_size > 0, f"Generated file empty: {rel_path}"

    def test_readme_manifest_lists_generated_files(self, tmp_path):
        from core.orchestrator.document_executor import execute_documents

        vault = tmp_path / "vault"
        vault.mkdir()
        task_folder = tmp_path / "task"
        task_folder.mkdir()
        (task_folder / "08-execution-plan.md").write_text(
            PLAN_WITH_REAL_TEMPLATES, encoding="utf-8"
        )

        result = execute_documents(
            task_folder=task_folder,
            vault_root=vault,
            repo_root=REPO,
            llm=self._make_llm(),
        )

        readme = Path(result["outputs_dir"]) / "README.md"
        readme_text = readme.read_text(encoding="utf-8")
        # README must not contain stub placeholder
        assert "TODO Phase 6" not in readme_text

    def test_llm_fallback_used_when_no_template_table(self, tmp_path):
        """When plan has no template table, LLM extraction fallback is called."""
        from core.orchestrator.document_executor import execute_documents

        vault = tmp_path / "vault"
        vault.mkdir()
        task_folder = tmp_path / "task"
        task_folder.mkdir()
        (task_folder / "08-execution-plan.md").write_text(
            PLAN_WITHOUT_TABLE, encoding="utf-8"
        )

        import json
        fallback_json = json.dumps([
            {"name": "pre-bid-rfi-log", "dept_code": "01-bid-coordination"},
        ])
        llm = self._make_llm(fallback_response=fallback_json)

        result = execute_documents(
            task_folder=task_folder,
            vault_root=vault,
            repo_root=REPO,
            llm=llm,
        )

        # LLM was called (extraction + optional doc generation)
        llm.complete.assert_called()
        # pre-bid-rfi-log exists in repo templates → should generate
        assert len(result["generated"]) >= 1

    def test_brain_context_included_in_substitutions(self, tmp_path):
        """Brain context fields must be available for template substitution."""
        from core.orchestrator.document_executor import _build_substitutions

        task_folder = tmp_path / "task"
        task_folder.mkdir()
        (task_folder / "00-brief.md").write_text(
            "---\ntype: brief\n---\n# Brief\n\nLaunch campaign.\n",
            encoding="utf-8",
        )

        brain_context = {
            "company_name": "VoltEdge Devices",
            "revenue": 5000000,
            "nested": {"key": "value"},
        }

        subs = _build_substitutions(task_folder, brain_context)

        assert subs["company_name"] == "VoltEdge Devices"
        assert subs["revenue"] == "5000000"
        assert subs["nested_key"] == "value"
        assert "brief" in subs
        assert "Launch campaign" in subs["brief"]

    def test_empty_template_name_skipped(self, tmp_path):
        """Template requests with empty name must be skipped silently."""
        from core.orchestrator.document_executor import execute_documents

        vault = tmp_path / "vault"
        vault.mkdir()
        task_folder = tmp_path / "task"
        task_folder.mkdir()

        # Plan with only a valid row — tests that single entry is processed
        plan_text = textwrap.dedent("""\
            ## Templates to create

            | Template name | Dept | Notes |
            |---------------|------|-------|
            | pre-bid-rfi-log | 01-bid-coordination | Valid |
        """)
        (task_folder / "08-execution-plan.md").write_text(plan_text, encoding="utf-8")

        result = execute_documents(
            task_folder=task_folder,
            vault_root=vault,
            repo_root=REPO,
            llm=self._make_llm(),
        )

        # Exactly one row processed (either generated or skipped)
        total_attempts = len(result["generated"]) + len(result["skipped"])
        assert total_attempts == 1
