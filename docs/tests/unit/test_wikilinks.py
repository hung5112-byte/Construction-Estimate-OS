"""Test core.wikilinks — Brain hub + Dept hubs + agent cross-linking."""
from __future__ import annotations

from core.onboard import onboard_vault
from core.wikilinks import LINK_MARKER, generate_wikilinks


def _bootstrap(tmp_path, packs=None):
    vault = tmp_path / "v"
    onboard_vault(vault_path=vault, packs=packs or [], init_git=False)
    return vault


def test_onboard_creates_brain_hub(tmp_path):
    vault = _bootstrap(tmp_path)
    hub = vault / "00-Brain" / "index.md"
    assert hub.exists()
    text = hub.read_text(encoding="utf-8")
    # Links to all 8 Brain files
    for stem in ("strategy", "products", "budget", "headcount", "state", "laws"):
        assert f"[[{stem}]]" in text
    # Links to departments via path
    assert "[[01-Departments/01-hardware-engineering/index" in text


def test_onboard_creates_dept_hub_with_org_chart(tmp_path):
    vault = _bootstrap(tmp_path)
    hub = vault / "01-Departments" / "01-hardware-engineering" / "index.md"
    assert hub.exists()
    text = hub.read_text(encoding="utf-8")
    assert "[[../../00-Brain/index" in text
    # V2: manager listed first with the star, teams below
    assert "**Manager:** [[hw-engineering-manager]]" in text
    assert "[[me-team]]" in text
    assert "[[ee-team]]" in text
    # Brain reference present
    assert "[[strategy]]" in text


def test_dept_hub_works_with_links_depends_on(tmp_path):
    """V2: depends_on renders as 'Works with' links with display names."""
    vault = _bootstrap(tmp_path)
    hub = (vault / "01-Departments" / "05-service-operations" / "index.md").read_text(
        encoding="utf-8"
    )
    assert "## Works with" in hub
    assert "[[../04-mfg-supplier-quality/index|Manufacturing & Supplier Quality]]" in hub


def test_onboard_appends_wikilinks_to_agent_files(tmp_path):
    vault = _bootstrap(tmp_path)
    agent = vault / "01-Departments" / "01-hardware-engineering" / "agents" / "me-team.md"
    text = agent.read_text(encoding="utf-8")
    assert LINK_MARKER in text
    assert "[[../index|🏢" in text
    assert "[[../../../00-Brain/index" in text
    # V2: team agents link to their manager
    assert "- Manager: [[hw-engineering-manager]]" in text


def test_manager_agent_has_no_self_manager_link(tmp_path):
    vault = _bootstrap(tmp_path)
    mgr = vault / "01-Departments" / "01-hardware-engineering" / "agents" / "hw-engineering-manager.md"
    links_block = mgr.read_text(encoding="utf-8").split(LINK_MARKER)[-1]
    assert "- Manager:" not in links_block


def test_wikilinks_idempotent(tmp_path):
    """Re-run generate_wikilinks: agent files don't get duplicate Links blocks."""
    vault = _bootstrap(tmp_path)
    agent = vault / "01-Departments" / "01-hardware-engineering" / "agents" / "me-team.md"
    first = agent.read_text(encoding="utf-8")

    summary = generate_wikilinks(vault)
    # Second run: nothing new should be added
    assert summary == {"brain_hub": False, "dept_hubs": 0, "agents_linked": 0}

    second = agent.read_text(encoding="utf-8")
    assert first == second
    # Marker only appears once
    assert second.count(LINK_MARKER) == 1


def test_wikilinks_with_pack_covers_pack_dept(tmp_path):
    """A pack's added departments get hubs + agent links (pack mechanism kept)."""
    import yaml

    # Verify generate_wikilinks covers any extra department folder present in
    # the vault (which is how pack departments arrive).
    vault = _bootstrap(tmp_path)
    extra = vault / "01-Departments" / "06-test-pack-dept"
    (extra / "agents").mkdir(parents=True)
    (extra / "department.yaml").write_text(
        yaml.safe_dump({
            "code": "06-test-pack-dept",
            "name_vn": "Test Pack Dept",
            "tier": 3,
            "agents": ["test-agent"],
            "default_speaker": "test-agent",
        }),
        encoding="utf-8",
    )
    (extra / "agents" / "test-agent.md").write_text(
        "---\nid: test-agent\nname_vn: Test Agent\ndepartment: 06-test-pack-dept\n---\n# Test Agent\n",
        encoding="utf-8",
    )

    generate_wikilinks(vault)
    hub = extra / "index.md"
    assert hub.exists()
    assert LINK_MARKER in (extra / "agents" / "test-agent.md").read_text(encoding="utf-8")


def test_brain_hub_skipped_if_already_exists(tmp_path):
    vault = _bootstrap(tmp_path)
    hub = vault / "00-Brain" / "index.md"
    custom = "# Custom Brain Hub\n"
    hub.write_text(custom, encoding="utf-8")

    summary = generate_wikilinks(vault)
    assert summary["brain_hub"] is False
    assert hub.read_text(encoding="utf-8") == custom
