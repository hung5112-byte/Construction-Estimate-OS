"""Tests for P1.8 — CitationValidator post-Synthesizer."""
from __future__ import annotations

from pathlib import Path


from core.orchestrator.citation_validator import (
    CitationValidator,
    _is_common_knowledge,
    _split_sentences,
)


# ── helpers ───────────────────────────────────────────────────────────────


def _write_report(tmp_path: Path, content: str, name: str = "07-decision-report.md") -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


# ── _split_sentences ──────────────────────────────────────────────────────


class TestSplitSentences:
    def test_single_sentence(self):
        result = _split_sentences("Revenue grew 20% year over year.")
        assert result == ["Revenue grew 20% year over year."]

    def test_multiple_sentences(self):
        text = "Revenue grew 20%. Costs fell $5,000. This is a good result."
        result = _split_sentences(text)
        assert len(result) == 3

    def test_question_and_exclamation(self):
        text = "Is 30% growth feasible? This is an ambitious target!"
        result = _split_sentences(text)
        assert len(result) == 2

    def test_empty_string(self):
        assert _split_sentences("") == []

    def test_no_punctuation(self):
        result = _split_sentences("a sentence with no period")
        assert result == ["a sentence with no period"]


# ── _is_common_knowledge ──────────────────────────────────────────────────


class TestIsCommonKnowledge:
    def test_holiday_is_common(self):
        assert _is_common_knowledge("The holiday season is the biggest sales period of the year.")

    def test_common_practice_is_common(self):
        assert _is_common_knowledge("This is common practice across the industry.")

    def test_claim_with_number_not_common(self):
        assert not _is_common_knowledge("Revenue grew 20% over the prior quarter.")

    def test_legal_ref_not_common(self):
        assert not _is_common_knowledge("Under the Fair Labor Standards Act, overtime must be paid.")

    def test_industry_norm_is_common(self):
        assert _is_common_knowledge("This follows the industry norm.")


# ── CitationValidator core logic ──────────────────────────────────────────


class TestCitationValidatorFindClaims:
    """Test _find_uncited_claims directly with string content."""

    def setup_method(self):
        self.validator = CitationValidator()

    def test_numeric_claim_no_citation_flagged(self):
        content = "Revenue in March grew 25% over February."
        flags = self.validator._find_uncited_claims(content)
        assert any(f.reason == "numeric_claim" for f in flags)

    def test_numeric_claim_with_source_not_flagged(self):
        content = "Revenue in March grew 25% over February. [source: finance.md]"
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_numeric_claim_with_brain_file_not_flagged(self):
        content = "Labor cost is 23.5% of total cost (strategy.md section 4)."
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_numeric_claim_with_url_not_flagged(self):
        content = "Up 15% per https://census.gov/report-2024."
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_legal_claim_no_citation_flagged(self):
        content = "Under the Fair Labor Standards Act, overtime pay is required."
        flags = self.validator._find_uncited_claims(content)
        assert any(f.reason == "legal_claim" for f in flags)

    def test_legal_claim_with_brain_laws_not_flagged(self):
        content = "Under the Fair Labor Standards Act [laws.md section 3], overtime is required."
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_act_with_deadline_flagged(self):
        content = "Under the Americans with Disabilities Act, the response deadline is 30 days."
        flags = self.validator._find_uncited_claims(content)
        # Has both legal AND numeric — at least one flag
        assert len(flags) >= 1

    def test_common_knowledge_not_flagged(self):
        content = "The holiday season is the biggest sales period of the year for most of retail."
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_heading_lines_skipped(self):
        content = "## Revenue grew 25% this quarter\n\nContent with no number."
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_code_block_skipped(self):
        content = "```yaml\nrevenue: 25000000\ngrowth: 20%\n```"
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_table_row_skipped(self):
        content = "| March | 25% | up |"
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_short_sentence_skipped(self):
        # < 20 chars — not enough context
        content = "Up 20%."
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_usd_currency_flagged(self):
        content = "The marketing budget is projected at $500,000 for Q3."
        flags = self.validator._find_uncited_claims(content)
        assert any(f.reason == "numeric_claim" for f in flags)

    def test_usd_estimate_flagged(self):
        content = "Rollout cost is estimated at $50,000 for the first year."
        flags = self.validator._find_uncited_claims(content)
        assert any(f.reason == "numeric_claim" for f in flags)

    def test_multiple_flags_from_multiple_lines(self):
        content = (
            "Revenue in March grew 25% over February.\n"
            "This is a good result given the market context.\n"
            "Labor cost is 23.5% of total cost.\n"
        )
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) >= 2

    def test_flag_contains_line_number(self):
        content = "Line one has no figure here.\nLine two grew 25% over last month.\n"
        flags = self.validator._find_uncited_claims(content)
        assert any(f.line_no == 2 for f in flags)

    def test_sentence_truncated_to_200_chars(self):
        long_sentence = "Revenue grew 50% " + "x" * 300 + "."
        flags = self.validator._find_uncited_claims(long_sentence)
        if flags:
            assert len(flags[0].sentence) <= 200

    def test_brain_file_inline_reference_clears_flag(self):
        content = "Gross margin is 45% per strategy.md financial-plan section."
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_markdown_link_with_url_clears_flag(self):
        content = "The industry grew 12% per [Census report](https://census.gov/2024)."
        flags = self.validator._find_uncited_claims(content)
        assert len(flags) == 0

    def test_no_claims_returns_empty(self):
        content = "This is a report with absolutely no figures or legal references."
        flags = self.validator._find_uncited_claims(content)
        assert flags == []


# ── CitationValidator.validate (file I/O) ────────────────────────────────


class TestCitationValidatorFileIO:
    def setup_method(self):
        self.validator = CitationValidator()

    def test_returns_empty_for_nonexistent_file(self, tmp_path):
        flags = self.validator.validate(tmp_path / "missing.md")
        assert flags == []

    def test_no_warning_appended_when_no_flags(self, tmp_path):
        p = _write_report(tmp_path, "# Report\n\nThere are no figures here.")
        original = p.read_text(encoding="utf-8")
        flags = self.validator.validate(p)
        assert flags == []
        assert p.read_text(encoding="utf-8") == original

    def test_warning_appended_when_flags_found(self, tmp_path):
        content = (
            "---\ntype: decision_report\n---\n"
            "# Report\n\n"
            "Revenue in March grew 25% over February.\n"
        )
        p = _write_report(tmp_path, content)
        flags = self.validator.validate(p)
        assert len(flags) > 0
        result = p.read_text(encoding="utf-8")
        assert "⚠️" in result
        assert "claims missing a source" in result

    def test_warning_section_contains_flagged_sentence(self, tmp_path):
        content = "# Report\n\nThe marketing budget is projected at $500,000 for Q3.\n"
        p = _write_report(tmp_path, content)
        self.validator.validate(p)
        result = p.read_text(encoding="utf-8")
        assert "$500,000" in result

    def test_no_double_append_on_second_validate_call(self, tmp_path):
        content = "# Report\n\nRevenue grew 25% over last month.\n"
        p = _write_report(tmp_path, content)
        self.validator.validate(p)
        self.validator.validate(p)
        result = p.read_text(encoding="utf-8")
        # Warning header should appear exactly once
        assert result.count("claims missing a source") == 1

    def test_warning_section_format(self, tmp_path):
        content = "# Report\n\nRevenue in March grew 25%.\nUnder the Fair Labor Standards Act, register first.\n"
        p = _write_report(tmp_path, content)
        self.validator.validate(p)
        result = p.read_text(encoding="utf-8")
        # Each flag listed as a bullet
        assert "- **[Line" in result

    def test_original_content_preserved_before_warning(self, tmp_path):
        content = "---\ntype: decision_report\n---\n# Report\n\nRevenue grew 25%.\n"
        p = _write_report(tmp_path, content)
        self.validator.validate(p)
        result = p.read_text(encoding="utf-8")
        assert result.startswith("---\ntype: decision_report")

    def test_flag_count_matches_return_value(self, tmp_path):
        content = (
            "Revenue grew 25% over last month.\n"
            "Costs were about $500,000 this year.\n"
            "Under the Fair Labor Standards Act, a permit is required.\n"
        )
        p = _write_report(tmp_path, content)
        flags = self.validator.validate(p)
        # All flagged lines should be in the return list (at least 2)
        assert len(flags) >= 2


# ── integration: clean report round-trip ─────────────────────────────────


class TestCitationValidatorIntegration:
    def test_full_report_with_citations_passes_clean(self, tmp_path):
        content = (
            "---\ntype: decision_report\nstop: 1\n---\n"
            "# Decision report\n\n"
            "## Bottom line\n"
            "A feasible plan based on the available data.\n\n"
            "## Analysis\n"
            "Gross margin reached 45% per [strategy.md] financial-plan section.\n"
            "Labor cost is 23.5% [source: finance.md] under US GAAP.\n"
            "Under the Fair Labor Standards Act [laws.md section 3], overtime is required.\n"
        )
        p = tmp_path / "07-decision-report.md"
        p.write_text(content, encoding="utf-8")
        validator = CitationValidator()
        flags = validator.validate(p)
        assert flags == []
        # File unchanged
        assert p.read_text(encoding="utf-8") == content

    def test_full_report_with_missing_citations_gets_warning(self, tmp_path):
        content = (
            "---\ntype: decision_report\nstop: 1\n---\n"
            "# Decision report\n\n"
            "## Analysis\n"
            "Gross margin reached 45% in the last quarter.\n"
            "Personnel cost was about $500,000.\n"
            "This follows the industry norm.\n"
        )
        p = tmp_path / "07-decision-report.md"
        p.write_text(content, encoding="utf-8")
        validator = CitationValidator()
        flags = validator.validate(p)
        assert len(flags) >= 2
        result = p.read_text(encoding="utf-8")
        assert "⚠️ Warning" in result
