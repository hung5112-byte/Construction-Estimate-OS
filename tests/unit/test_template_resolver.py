from core.obsidian.template_resolver import TemplateResolver


def test_priority_custom_first(tmp_path):
    vault = tmp_path / "vault"
    repo = tmp_path / "repo"

    (repo / "templates-us" / "03-quality-reliability").mkdir(parents=True)
    (repo / "templates-us" / "03-quality-reliability" / "workplace-rules.md").write_text("DEFAULT", encoding="utf-8")

    (vault / "01-Departments" / "03-quality-reliability" / "refs").mkdir(parents=True)
    (vault / "01-Departments" / "03-quality-reliability" / "refs" / "workplace-rules.md").write_text("PACK", encoding="utf-8")

    (vault / "00-Templates-Custom" / "03-quality-reliability").mkdir(parents=True)
    (vault / "00-Templates-Custom" / "03-quality-reliability" / "workplace-rules.md").write_text("CUSTOM", encoding="utf-8")

    resolver = TemplateResolver(vault_root=vault, repo_templates=repo / "templates-us")
    path = resolver.resolve("workplace-rules", dept_code="03-quality-reliability")
    assert path.read_text(encoding="utf-8") == "CUSTOM"


def test_falls_back_to_repo_default(tmp_path):
    vault = tmp_path / "vault"
    repo = tmp_path / "repo"
    (repo / "templates-us" / "05-service-operations").mkdir(parents=True)
    (repo / "templates-us" / "05-service-operations" / "deployment-plan.md").write_text("DEFAULT", encoding="utf-8")
    vault.mkdir()

    resolver = TemplateResolver(vault_root=vault, repo_templates=repo / "templates-us")
    path = resolver.resolve("deployment-plan", dept_code="05-service-operations")
    assert "DEFAULT" in path.read_text(encoding="utf-8")


def test_returns_none_when_template_missing(tmp_path):
    resolver = TemplateResolver(vault_root=tmp_path, repo_templates=tmp_path / "fake")
    assert resolver.resolve("xyz", "05-service-operations") is None
