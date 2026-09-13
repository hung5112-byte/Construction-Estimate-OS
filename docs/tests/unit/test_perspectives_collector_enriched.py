"""Tests for P1.1 — PerspectivesCollector loads per-agent enriched prompts."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock


from core.meeting.debate_state import new_meeting_state
from core.orchestrator.perspectives_collector import (
    PerspectivesCollector,
    _STANCE_SUFFIX,
)


# ── helpers ──────────────────────────────────────────────────────────────


def _make_llm(response: str = "mock-response") -> MagicMock:
    llm = MagicMock()
    llm.complete = MagicMock(return_value=response)
    return llm


REPO_ROOT = Path(__file__).parent.parent.parent


# ── Task 1: enriched agent prompt ────────────────────────────────────────


class TestEnrichedPromptLoading:
    """PerspectivesCollector should use agent .md body when file exists."""

    def test_uses_generic_prompt_when_no_agent_file(self, tmp_path):
        """Fallback to PERSPECTIVE_PROMPT when agent .md missing."""
        # Create minimal department structure without agents/ dir
        dept_dir = tmp_path / "05-service-operations"
        dept_dir.mkdir()
        (dept_dir / "department.yaml").write_text(
            "code: 05-service-operations\nname_local: Operations\ntier: 2\n"
            "description: Operations\nagents: []\ndefault_speaker: ops-manager\n",
            encoding="utf-8",
        )

        llm = _make_llm()
        collector = PerspectivesCollector(departments_root=tmp_path, llm=llm)
        state = new_meeting_state(brief="test brief", departments=["05-service-operations"])
        result = collector.collect(state)

        assert "05-service-operations" in result["perspectives"]
        # Verify LLM was called with generic fallback (system contains dept name)
        call_args = llm.complete.call_args
        messages = call_args[0][0]
        system_content = messages[0]["content"]
        assert "Operations" in system_content
        # Should NOT contain enriched suffix when falling back
        assert _STANCE_SUFFIX.strip()[:30] not in system_content

    def test_uses_enriched_prompt_when_agent_file_exists(self, tmp_path):
        """Use agent .md system_prompt body when file present."""
        dept_dir = tmp_path / "02-npi-program-management"
        agents_dir = dept_dir / "agents"
        agents_dir.mkdir(parents=True)
        (dept_dir / "department.yaml").write_text(
            "code: 02-npi-program-management\nname_local: Supply Chain\ntier: 2\n"
            "description: Supply Chain\nagents: [buyer]\ndefault_speaker: buyer\n",
            encoding="utf-8",
        )
        (agents_dir / "buyer.md").write_text(
            "---\nid: buyer\nname_local: Buyer\ndepartment: 02-npi-program-management\n---\n"
            "You are a professional Buyer with expertise in P&L and cash flow.",
            encoding="utf-8",
        )

        llm = _make_llm()
        collector = PerspectivesCollector(departments_root=tmp_path, llm=llm)
        state = new_meeting_state(brief="test brief", departments=["02-npi-program-management"])
        result = collector.collect(state)

        assert "02-npi-program-management" in result["perspectives"]
        call_args = llm.complete.call_args
        messages = call_args[0][0]
        system_content = messages[0]["content"]
        # Enriched body should be in system message
        assert "professional Buyer" in system_content
        # Stance suffix appended
        assert "YOUR TASK IN THIS MEETING" in system_content

    def test_fallback_when_agent_file_has_no_body(self, tmp_path):
        """Fallback to generic prompt when .md body is empty."""
        dept_dir = tmp_path / "02-npi-program-management"
        agents_dir = dept_dir / "agents"
        agents_dir.mkdir(parents=True)
        (dept_dir / "department.yaml").write_text(
            "code: 02-npi-program-management\nname_local: Supply Chain\ntier: 2\n"
            "description: Supply Chain\nagents: [buyer]\ndefault_speaker: buyer\n",
            encoding="utf-8",
        )
        # .md with frontmatter but empty body
        (agents_dir / "buyer.md").write_text(
            "---\nid: buyer\nname_local: Buyer\ndepartment: 02-npi-program-management\n---\n",
            encoding="utf-8",
        )

        llm = _make_llm()
        collector = PerspectivesCollector(departments_root=tmp_path, llm=llm)
        state = new_meeting_state(brief="test brief", departments=["02-npi-program-management"])
        result = collector.collect(state)

        assert "02-npi-program-management" in result["perspectives"]
        call_args = llm.complete.call_args
        messages = call_args[0][0]
        system_content = messages[0]["content"]
        # Generic fallback used — dept name present
        assert "Supply Chain" in system_content

    def test_fallback_on_parse_error(self, tmp_path):
        """Fallback gracefully when agent .md has malformed frontmatter."""
        dept_dir = tmp_path / "02-npi-program-management"
        agents_dir = dept_dir / "agents"
        agents_dir.mkdir(parents=True)
        (dept_dir / "department.yaml").write_text(
            "code: 02-npi-program-management\nname_local: Supply Chain\ntier: 2\n"
            "description: Supply Chain\nagents: [buyer]\ndefault_speaker: buyer\n",
            encoding="utf-8",
        )
        # Missing 'id' field — AgentLoader raises ValueError
        (agents_dir / "buyer.md").write_text(
            "---\nname_local: Buyer\ndepartment: 02-npi-program-management\n---\nSome body text.",
            encoding="utf-8",
        )

        llm = _make_llm()
        collector = PerspectivesCollector(departments_root=tmp_path, llm=llm)
        state = new_meeting_state(brief="test brief", departments=["02-npi-program-management"])
        # Should NOT raise — graceful degradation
        result = collector.collect(state)
        assert "02-npi-program-management" in result["perspectives"]

    def test_unknown_department_returns_placeholder(self, tmp_path):
        """Missing department returns placeholder string, not exception."""
        llm = _make_llm()
        collector = PerspectivesCollector(departments_root=tmp_path, llm=llm)
        state = new_meeting_state(brief="test", departments=["99-unknown"])
        result = collector.collect(state)

        text = result["perspectives"].get("99-unknown", "")
        assert "99-unknown" in text or "does not exist" in text

    def test_vault_root_fallback_for_agent_path(self, tmp_path):
        """vault_root param allows finding agent .md in vault when not in departments_root."""
        # Simulated: departments_root = repo/departments (no agents/ there)
        repo_depts = tmp_path / "repo_departments"
        dept_dir = repo_depts / "02-npi-program-management"
        dept_dir.mkdir(parents=True)
        (dept_dir / "department.yaml").write_text(
            "code: 02-npi-program-management\nname_local: Supply Chain\ntier: 2\n"
            "description: Supply Chain\nagents: [buyer]\ndefault_speaker: buyer\n",
            encoding="utf-8",
        )
        # Agent .md lives in vault, not repo
        vault_root = tmp_path / "vault"
        vault_agents_dir = vault_root / "01-Departments" / "02-npi-program-management" / "agents"
        vault_agents_dir.mkdir(parents=True)
        (vault_agents_dir / "buyer.md").write_text(
            "---\nid: buyer\nname_local: Buyer\ndepartment: 02-npi-program-management\n---\n"
            "Buyer from vault with enriched prompt.",
            encoding="utf-8",
        )

        llm = _make_llm()
        collector = PerspectivesCollector(
            departments_root=repo_depts, llm=llm, vault_root=vault_root
        )
        state = new_meeting_state(brief="brief", departments=["02-npi-program-management"])
        collector.collect(state)

        call_args = llm.complete.call_args
        system_content = call_args[0][0][0]["content"]
        assert "Buyer from vault with enriched prompt." in system_content

    def test_multiple_departments_parallel(self, tmp_path):
        """Collector handles multiple departments in parallel correctly."""
        for code, name in [("03-architectural", "Quality"), ("05-service-operations", "Operations")]:
            d = tmp_path / code
            d.mkdir()
            # default_speaker must be a non-null string in Department model
            (d / "department.yaml").write_text(
                f'code: {code}\nname_local: "{name}"\ntier: 1\n'
                f'description: "{name}"\nagents: []\ndefault_speaker: ""\n',
                encoding="utf-8",
            )

        llm = _make_llm("dept response")
        collector = PerspectivesCollector(departments_root=tmp_path, llm=llm)
        state = new_meeting_state(
            brief="brief", departments=["03-architectural", "05-service-operations"]
        )
        result = collector.collect(state)

        assert "03-architectural" in result["perspectives"]
        assert "05-service-operations" in result["perspectives"]
        assert llm.complete.call_count == 2

    def test_uses_repo_departments_for_real_dept(self):
        """Integration: collector works against real repo departments/ folder."""
        llm = _make_llm("response from real dept")
        collector = PerspectivesCollector(
            departments_root=REPO_ROOT / "departments", llm=llm
        )
        state = new_meeting_state(brief="expand the product line", departments=["03-architectural"])
        result = collector.collect(state)

        assert "03-architectural" in result["perspectives"]
        assert llm.complete.call_count == 1
        # Verify messages were actually passed
        messages = llm.complete.call_args[0][0]
        assert any(m["role"] == "system" for m in messages)
        system_msg = next(m for m in messages if m["role"] == "system")
        # With the enriched quality-manager.md present, its body should appear
        assert len(system_msg["content"]) > 20
