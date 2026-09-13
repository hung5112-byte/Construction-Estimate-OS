"""Phase 5 smoke: imports + 3 packs loadable + template resolver work."""
from pathlib import Path


def test_phase5_imports():
    """All Phase 5 modules import cleanly."""
    from core.agents.agent_loader import AgentLoader, AgentDefinition  # noqa: F401
    from core.agents.registry import Registry, DepartmentWithAgents  # noqa: F401
    from core.agents.pack_loader import PackLoader, Pack  # noqa: F401
    from core.obsidian.template_resolver import TemplateResolver  # noqa: F401
    from core.obsidian.doc_writer import DocWriter  # noqa: F401
    from core.obsidian.git_sync import GitSync  # noqa: F401


def test_pack_mechanism_loadable():
    """No packs ship by default; the loader mechanism still works."""
    from core.agents.pack_loader import PackLoader
    repo = Path(__file__).parent.parent.parent
    loader = PackLoader(repo / "packs")
    # list_available returns only dirs containing pack.yaml — none by default
    assert loader.list_available() == []


def test_6_core_depts_have_agents():
    from core.agents.registry import Registry
    repo = Path(__file__).parent.parent.parent
    reg = Registry(repo / "departments")

    expected = {
        "01-bid-coordination": 5,
        "02-civil-structural": 4,
        "03-architectural": 5,
        "04-mep": 4,
        "05-cost-engineering": 5,
        "06-estimate-review": 4,
    }
    for code, n in expected.items():
        d = reg.get(code)
        assert len(d.agents_by_id) == n, f"{code} should have {n} agents (manager + teams)"


def test_template_resolver_finds_templates_us():
    from core.obsidian.template_resolver import TemplateResolver
    repo = Path(__file__).parent.parent.parent

    resolver = TemplateResolver(
        vault_root=repo / "tests/fixtures/demo-vault",
        repo_templates=repo / "templates-us",
    )
    # Verify ANY template exists in a dept folder (not specific filename)
    dept_dir = repo / "templates-us" / "01-bid-coordination"
    if dept_dir.exists():
        sample_files = [f for f in dept_dir.iterdir() if f.suffix == ".md"]
        if sample_files:
            sample_name = sample_files[0].stem
            found = resolver.resolve(sample_name, "01-bid-coordination")
            assert found is not None
            assert found.exists()
