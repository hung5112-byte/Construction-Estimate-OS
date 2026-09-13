from core.agents.registry import Registry


def test_registry_loads_dept_with_agents(tmp_path):
    (tmp_path / "05-service-operations" / "agents").mkdir(parents=True)
    (tmp_path / "05-service-operations" / "department.yaml").write_text(
        "code: '05-service-operations'\nname_local: Ops\ntier: 3\nagents: [test-agent]\ndefault_speaker: test-agent\n",
        encoding="utf-8",
    )
    (tmp_path / "05-service-operations" / "agents" / "test-agent.md").write_text(
        "---\nid: test-agent\nname_local: Test\ndepartment: 05-service-operations\n---\n# Test\n",
        encoding="utf-8",
    )

    reg = Registry(tmp_path)
    dept = reg.get("05-service-operations")
    assert dept.code == "05-service-operations"
    assert "test-agent" in dept.agents_by_id
    assert dept.select_agent_for_brief("anything").id == "test-agent"
