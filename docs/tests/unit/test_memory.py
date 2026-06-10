from datetime import date
from core.brain.memory import DecisionLog
from core.brain.schema import DecisionEntry


def test_append_creates_entry(tmp_path):
    log_path = tmp_path / "decisions-log.md"
    log_path.write_text("---\ntype: brain\n---\n# Log\n", encoding="utf-8")

    log = DecisionLog(log_path)
    entry = DecisionEntry(
        date=date(2026, 5, 6), slug="test-decision",
        owner="Department Head", decision="Approve pilot",
        reason="Brain showed budget OK"
    )
    log.append(entry)

    content = log_path.read_text(encoding="utf-8")
    assert "test-decision" in content
    assert "Department Head" in content


def test_search_finds_matches(tmp_path):
    log_path = tmp_path / "decisions-log.md"
    log_path.write_text(
        "---\n---\n# Log\n\n### 2026-05-06 — campaign-pilot\n- Decision: launch\n- Reason: foo\n",
        encoding="utf-8",
    )
    log = DecisionLog(log_path)
    matches = log.search("campaign")
    assert len(matches) == 1
