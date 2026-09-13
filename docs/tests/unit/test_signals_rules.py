from core.signals.rules import load_rules
from core.signals.schema import Severity


def test_default_rules_load(tmp_path):
    rules = load_rules(tmp_path)  # empty vault → bundled default
    assert len(rules.departments) == 5
    assert "line down" in rules.keywords.critical
    assert rules.policy.min_severity_to_trigger == Severity.CRITICAL
    assert rules.policy.max_auto_meetings_per_day == 3


def test_vault_rules_override_default(tmp_path):
    # RULE 6: company custom beats bundled default
    brain = tmp_path / "00-Brain"
    brain.mkdir()
    (brain / "signal-rules.yaml").write_text(
        "departments: [Tax Advisory]\n"
        "keywords:\n  critical: ['audit letter']\n"
        "policy:\n  max_auto_meetings_per_day: 1\n",
        encoding="utf-8",
    )
    rules = load_rules(tmp_path)
    assert rules.departments == ["Tax Advisory"]
    assert rules.keywords.critical == ["audit letter"]
    assert rules.policy.max_auto_meetings_per_day == 1
