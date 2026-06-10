import pytest
from core.agents.agent_loader import AgentLoader


def test_load_agent_from_md(tmp_path):
    agent_path = tmp_path / "ads-specialist.md"
    agent_path.write_text("""---
id: ads-specialist
name_vn: "Ad Specialist"
department: 05-service-operations
expertise: ["FB Ads", "Google Ads"]
required_tools: [us_law_search]
temperature: 0.3
---
# Ad Specialist

You are a US digital advertising specialist.
""", encoding="utf-8")

    loader = AgentLoader()
    agent = loader.load(agent_path)

    assert agent.id == "ads-specialist"
    assert agent.name_vn == "Ad Specialist"
    assert "FB Ads" in agent.expertise
    assert "us_law_search" in agent.required_tools
    assert agent.temperature == 0.3
    assert "advertising specialist" in agent.system_prompt.lower()


def test_missing_required_field_raises(tmp_path):
    agent_path = tmp_path / "bad.md"
    agent_path.write_text("---\n---\n# x\n", encoding="utf-8")
    with pytest.raises(ValueError):
        AgentLoader().load(agent_path)
