"""Unit tests for core/orchestrator/execution_planner.py (P0.2)."""
import textwrap
from unittest.mock import MagicMock

import pytest


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

PLAN_WITH_TABLE = textwrap.dedent("""\
    ---
    type: execution_plan
    stop: 2
    ---
    # Execution plan

    ## Templates to create

    | Template name | Dept | Notes |
    |---------------|------|-------|
    | engineering-change-order | 02-npi-program-management | ECO |
    | rma-process-sop | 05-service-operations | Returns |
""")

PLAN_WITHOUT_TABLE = textwrap.dedent("""\
    ---
    type: execution_plan
    stop: 2
    ---
    # Execution plan

    Steps to perform: deployment, sourcing.
""")


# ──────────────────────────────────────────────────────────────────────────────
# parse_templates_from_plan
# ──────────────────────────────────────────────────────────────────────────────

class TestParseTemplatesFromPlan:
    def test_parses_two_rows(self, tmp_path):
        from core.orchestrator.execution_planner import parse_templates_from_plan

        plan_path = tmp_path / "08-execution-plan.md"
        plan_path.write_text(PLAN_WITH_TABLE, encoding="utf-8")

        result = parse_templates_from_plan(plan_path)

        assert len(result) == 2
        assert result[0]["name"] == "engineering-change-order"
        assert result[0]["dept_code"] == "02-npi-program-management"
        assert result[1]["name"] == "rma-process-sop"
        assert result[1]["dept_code"] == "05-service-operations"

    def test_returns_empty_when_no_table(self, tmp_path):
        from core.orchestrator.execution_planner import parse_templates_from_plan

        plan_path = tmp_path / "08-execution-plan.md"
        plan_path.write_text(PLAN_WITHOUT_TABLE, encoding="utf-8")

        result = parse_templates_from_plan(plan_path)
        assert result == []

    def test_returns_empty_when_file_missing(self, tmp_path):
        from core.orchestrator.execution_planner import parse_templates_from_plan

        result = parse_templates_from_plan(tmp_path / "nonexistent.md")
        assert result == []

    def test_skips_header_row(self, tmp_path):
        """Header row 'Ten mau | Phong' must not appear in results."""
        from core.orchestrator.execution_planner import parse_templates_from_plan

        plan_path = tmp_path / "08-execution-plan.md"
        plan_path.write_text(PLAN_WITH_TABLE, encoding="utf-8")

        result = parse_templates_from_plan(plan_path)
        names = [r["name"] for r in result]
        assert "Ten mau" not in names
        assert "ten mau" not in names


# ──────────────────────────────────────────────────────────────────────────────
# generate_execution_plan
# ──────────────────────────────────────────────────────────────────────────────

class TestGenerateExecutionPlan:
    def _make_translator_mock(self):
        """Translator that passes input through unchanged."""
        t = MagicMock()
        t.apply.side_effect = lambda text: text
        return t

    def test_raises_if_decision_report_missing(self, tmp_path):
        from core.orchestrator.execution_planner import generate_execution_plan

        llm = MagicMock()
        translator = self._make_translator_mock()

        with pytest.raises(FileNotFoundError, match="07-decision-report.md"):
            generate_execution_plan(tmp_path, llm, translator)

    def test_writes_plan_file(self, tmp_path):
        from core.orchestrator.execution_planner import generate_execution_plan

        # Create a decision report
        (tmp_path / "07-decision-report.md").write_text(
            "---\ntype: decision_report\n---\nGO with revisions.\n",
            encoding="utf-8",
        )

        llm_response = PLAN_WITH_TABLE
        llm = MagicMock()
        llm.complete.return_value = llm_response
        translator = self._make_translator_mock()

        out = generate_execution_plan(tmp_path, llm, translator)

        assert out == tmp_path / "08-execution-plan.md"
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert "type: execution_plan" in content
        assert "stop: 2" in content

    def test_adds_frontmatter_when_llm_omits_it(self, tmp_path):
        """If LLM returns plain text without YAML front-matter, add it."""
        from core.orchestrator.execution_planner import generate_execution_plan

        (tmp_path / "07-decision-report.md").write_text("GO.", encoding="utf-8")

        llm = MagicMock()
        llm.complete.return_value = "# Plan\n\nCac buoc thuc hien."
        translator = self._make_translator_mock()

        out = generate_execution_plan(tmp_path, llm, translator)
        content = out.read_text(encoding="utf-8")
        assert content.startswith("---")
        assert "type: execution_plan" in content

    def test_translator_applied(self, tmp_path):
        """Translator.apply() must be called on the LLM output."""
        from core.orchestrator.execution_planner import generate_execution_plan

        (tmp_path / "07-decision-report.md").write_text("GO.", encoding="utf-8")

        llm = MagicMock()
        llm.complete.return_value = PLAN_WITH_TABLE

        translator = MagicMock()
        translator.apply.return_value = PLAN_WITH_TABLE  # passthrough

        generate_execution_plan(tmp_path, llm, translator)
        translator.apply.assert_called_once()

    def test_continues_if_translator_raises(self, tmp_path):
        """Translator failure must not crash plan generation (fallback to raw)."""
        from core.orchestrator.execution_planner import generate_execution_plan

        (tmp_path / "07-decision-report.md").write_text("GO.", encoding="utf-8")

        llm = MagicMock()
        llm.complete.return_value = PLAN_WITH_TABLE

        translator = MagicMock()
        translator.apply.side_effect = RuntimeError("translator down")

        # Should not raise
        out = generate_execution_plan(tmp_path, llm, translator)
        assert out.exists()
