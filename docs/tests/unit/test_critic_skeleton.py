"""Deterministic report skeleton — unit tests (2026-07-05 replay-4 ruling).

Four live fix-cycles proved prompt mandates cannot guarantee structure (no
replay-4 draft ever contained the Blockers heading). The engine now assembles
the skeleton in code; these tests pin that behavior: blockers rows from tagged
unknowns, TBD defaults, 'None.' when empty, canonical verdict placement, and
byte-stable no-ops on compliant text.
"""
from __future__ import annotations

from core.critic.deterministic import (
    ClarificationQA,
    check_regulatory_promoted,
    check_verdict,
)
from core.critic.skeleton import (
    BLOCKERS_HEADING,
    TBD_FIELD,
    assemble_skeleton,
    ensure_blockers_section,
    ensure_verdict_line,
)

FCC_QA = ClarificationQA(
    qid="Q4",
    question="Do existing FCC Part 15 grants get voided by an MCU swap?",
    answer="D. Unknown — need regulatory counsel review",
    severity="WARN",
    tags=["regulatory", "certification"],
)
UNTAGGED_QA = ClarificationQA(qid="Q1", question="Price?", answer="B) $389", tags=[])

COMPLIANT_REPORT = """---
type: decision_report
stop: 1
---
# Decision report: test

## 📌 Bottom line (30-second read)
- Buy the stock now. [[00-Brain/strategy.md]]

## Recommendation

GO-WITH-CONDITIONS

## Detailed analysis
Prose here.

## Blockers (before Stop 2)

- [ ] **Assess FCC re-authorization** (ref: Q4). *Owner: 02-npi. Deadline: Week 2.*

## Decisions the Department Head must make
A/B
"""


class TestBlockersAssembly:
    def test_missing_section_is_created_with_synthesized_rows(self):
        text = "# R\n\n## Recommendation\n\nGO\n\n## Detailed analysis\nProse.\n"
        out, info = ensure_blockers_section(text, [FCC_QA])
        assert info["section_created"] is True
        assert info["rows_added"] == ["Q4"]
        assert BLOCKERS_HEADING in out
        assert "(ref: Q4)" in out
        assert f"*Owner: {TBD_FIELD}. Deadline: {TBD_FIELD}.*" in out
        assert "regulatory/certification unknown" in out  # tags in the action text
        assert "FCC Part 15" in out  # topic templated from the question
        # ...and the composed text now satisfies the R2 scanner.
        assert check_regulatory_promoted(out, [FCC_QA]).passed is True

    def test_empty_section_when_nothing_to_block_on(self):
        text = "# R\n\n## Detailed analysis\nProse.\n"
        out, info = ensure_blockers_section(text, [UNTAGGED_QA])
        assert info["section_created"] is True
        assert BLOCKERS_HEADING in out
        assert "None." in out

    def test_section_inserted_before_decisions_heading(self):
        text = (
            "# R\n\n## Detailed analysis\nProse.\n\n"
            "## Decisions the Department Head must make\nA/B\n"
        )
        out, _ = ensure_blockers_section(text, [FCC_QA])
        assert out.index(BLOCKERS_HEADING) < out.index("## Decisions")

    def test_existing_model_rows_are_preserved_and_missing_ones_appended(self):
        text = (
            "# R\n\n## Blockers (before Stop 2)\n\n"
            "- [ ] **Model-authored row** (ref: Q4). "
            "*Owner: 02-npi. Deadline: Week 2.*\n"
        )
        other = ClarificationQA(qid="Q6", question="PCI recertification scope?",
                                answer="Unsure — needs confirmation",
                                tags=["compliance"])
        out, info = ensure_blockers_section(text, [FCC_QA, other])
        assert "Model-authored row" in out  # preserved verbatim
        assert info["rows_added"] == ["Q6"]
        assert "(ref: Q6)" in out
        assert out.count(BLOCKERS_HEADING) == 1  # augmented, not duplicated

    def test_incomplete_model_row_is_completed_with_tbd_fields(self):
        text = (
            "# R\n\n## Blockers (before Stop 2)\n\n"
            "- [ ] **Assess FCC re-authorization** (ref: Q4).\n"
        )
        out, info = ensure_blockers_section(text, [FCC_QA])
        assert info["rows_completed"] == ["Q4"]
        assert f"*Owner: {TBD_FIELD}.*" in out
        assert f"*Deadline: {TBD_FIELD}.*" in out
        assert check_regulatory_promoted(out, [FCC_QA]).passed is True

    def test_compliant_section_is_a_byte_stable_no_op(self):
        out, info = ensure_blockers_section(COMPLIANT_REPORT, [FCC_QA])
        assert out == COMPLIANT_REPORT
        assert info["rows_added"] == [] and info["rows_completed"] == []


class TestVerdictPlacement:
    def test_compliant_verdict_is_a_no_op(self):
        out, verdict, changed = ensure_verdict_line(COMPLIANT_REPORT)
        assert (out, verdict, changed) == (COMPLIANT_REPORT, "GO-WITH-CONDITIONS", False)

    def test_missing_heading_with_lone_tier_in_body_gets_section_rendered(self):
        text = (
            "# R\n\n## 📌 Bottom line (30-second read)\n- Buy now.\n\n"
            "## Detailed analysis\nThe verdict of the meeting was:\n\n"
            "**GO-WITH-CONDITIONS**\n\nMore prose.\n"
        )
        out, verdict, changed = ensure_verdict_line(text)
        assert changed is True and verdict == "GO-WITH-CONDITIONS"
        assert "## Recommendation" in out
        assert check_verdict(out).passed is True
        # rendered after the Bottom-line section, before Detailed analysis
        assert out.index("## Recommendation") < out.index("## Detailed analysis")

    def test_unparseable_verdict_is_left_for_the_model(self):
        """The engine never invents a verdict — R3 stays as the safety assert."""
        text = "# R\n\n## Recommendation\n\nCautiously optimistic, monitor closely.\n"
        out, verdict, changed = ensure_verdict_line(text)
        assert (out, verdict, changed) == (text, None, False)
        assert check_verdict(out).passed is False

    def test_ambiguous_two_tier_body_is_left_for_the_model(self):
        text = "# R\n\nGO\n\nSome prose.\n\nNO-GO\n"
        out, verdict, changed = ensure_verdict_line(text)
        assert verdict is None and changed is False

    def test_glossary_table_row_defining_go_is_not_mistaken_for_a_verdict(self):
        """Replay-3 hazard: a glossary table defined 'GO' — table rows must
        never be parsed as the verdict."""
        text = (
            "# R\n\n## Glossary\n\n| **GO** | A formal decision to proceed |\n\n"
            "## Detailed analysis\nProse without any tier.\n"
        )
        out, verdict, changed = ensure_verdict_line(text)
        assert verdict is None and changed is False

    def test_noncompliant_verdict_line_with_lone_tier_elsewhere_is_repaired(self):
        text = (
            "# R\n\n## Recommendation\n\nApproved — with conditions.\n\n"
            "## Summary\n\nPROCEED-WITH-REVISIONS\n"
        )
        out, verdict, changed = ensure_verdict_line(text)
        assert changed is True and verdict == "PROCEED-WITH-REVISIONS"
        assert check_verdict(out).passed is True


class TestAssembleSkeleton:
    def test_composed_report_always_carries_the_structural_invariants(self):
        """The decisive replay-4 assertion: whatever the model emitted, the
        composed draft contains the Blockers heading."""
        model_output = (
            "# Decision report\n\n## 📌 Bottom line (30-second read)\n"
            "- Buy the last-time-buy stock now.\n\n"
            "## Our recommendation\n\n**GO-WITH-CONDITIONS** — proceed after "
            "data checks.\n\n## Detailed analysis\nFCC question is open, "
            "mentioned only in prose.\n"
        )
        result = assemble_skeleton(model_output, [FCC_QA])
        assert result.changed is True
        assert BLOCKERS_HEADING in result.text
        assert "(ref: Q4)" in result.text
        assert result.verdict == "GO-WITH-CONDITIONS"
        assert result.blockers_section_created is True
        assert check_regulatory_promoted(result.text, [FCC_QA]).passed is True
        assert check_verdict(result.text).passed is True

    def test_idempotent_second_pass_is_a_no_op(self):
        model_output = "# R\n\nGO\n\nProse only, no structure.\n"
        first = assemble_skeleton(model_output, [FCC_QA])
        second = assemble_skeleton(first.text, [FCC_QA])
        assert second.changed is False
        assert second.text == first.text

    def test_fully_compliant_report_is_byte_stable(self):
        result = assemble_skeleton(COMPLIANT_REPORT, [FCC_QA])
        assert result.changed is False
        assert result.text == COMPLIANT_REPORT
