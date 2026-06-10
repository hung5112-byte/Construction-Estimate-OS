from core.clarifier.question_generator import Question
from core.brain.gap_analyzer import Severity
from core.clarifier.clarification_io import (
    write_clarification, read_answers,
)


def test_write_clarification_creates_file(tmp_path):
    qs = [Question(
        text="Pivot or test?",
        citation="00-Brain/strategy.md",
        choices=["Long-term pivot", "One-time test"],
        severity=Severity.CRITICAL,
    )]
    f = tmp_path / "03-clarification.md"
    write_clarification(f, qs)
    content = f.read_text(encoding="utf-8")
    assert "Pivot or test?" in content
    assert "[ ] Long-term pivot" in content
    assert "00-Brain/strategy.md" in content


def test_read_answers_parses_user_choice(tmp_path):
    f = tmp_path / "03-clarification.md"
    f.write_text(
        "---\ntype: clarification\n---\n"
        "## Q1 [CRITICAL]\n_Cite: 00-Brain/strategy.md_\n"
        "Pivot or test?\n\n"
        "- [ ] Long-term pivot\n"
        "- [x] One-time test\n"
        "- [ ] Cancel\n",
        encoding="utf-8",
    )
    answers = read_answers(f)
    assert len(answers) == 1
    assert answers[0].choice == "One-time test"
