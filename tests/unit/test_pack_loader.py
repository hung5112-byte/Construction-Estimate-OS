from core.agents.pack_loader import PackLoader


def test_load_pack_yaml(tmp_path):
    pack_dir = tmp_path / "testpack"
    pack_dir.mkdir()
    (pack_dir / "pack.yaml").write_text("""
name: Test Pack
code: testpack
version: 1.0.0
description: Example overlay pack
adds_departments: [06-test-dept]
extends_departments:
  - target: 05-service-operations
    add_agents: [extra-agent]
brain_template: brain-template/
compliance_refs: ["Example Regulation"]
""", encoding="utf-8")

    loader = PackLoader(tmp_path)
    pack = loader.load("testpack")
    assert pack.code == "testpack"
    assert "06-test-dept" in pack.adds_departments
    # extends_departments is parsed for forward compatibility (not applied by onboarding)
    assert pack.extends_departments[0].target == "05-service-operations"
