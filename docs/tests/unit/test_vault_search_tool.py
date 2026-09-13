"""Tests for the vault_search tool + registration (ADR-004 Addendum A, Step 1)."""
from __future__ import annotations

from pathlib import Path

import pytest

from core.retrieval.indexer import VaultIndexer
from core.tools.vault_search import NO_MATCH_SENTINEL, VaultSearchTool


@pytest.fixture()
def vault(tmp_path: Path) -> Path:
    root = tmp_path / "vault"
    brain = root / "00-Brain"
    brain.mkdir(parents=True)
    (brain / "products.md").write_text(
        "---\ntype: brain\nlabel: internal\n---\n"
        "# Products\n\n## Warranty\n\nThe CY80 carries a two-year limited warranty.\n",
        encoding="utf-8",
    )
    VaultIndexer(root).build()
    return root


def test_unavailable_without_index(tmp_path: Path):
    assert VaultSearchTool().is_available() is False
    assert VaultSearchTool(vault_root=tmp_path).is_available() is False


def test_available_after_index_build(vault: Path):
    assert VaultSearchTool(vault_root=vault).is_available() is True


def test_run_returns_sources_and_snippets(vault: Path):
    result = VaultSearchTool(vault_root=vault).run("CY80 warranty")
    assert result.sources == ["00-Brain/products.md#Warranty"]
    assert result.retrieved_at
    hits = result.data["hits"]
    assert hits[0]["source"] == "00-Brain/products.md#Warranty"
    assert "warranty" in hits[0]["snippet"].lower()


def test_run_no_match_returns_sentinel(vault: Path):
    result = VaultSearchTool(vault_root=vault).run("xylophone quasar nonsense")
    assert result.data["hits"] == []
    assert NO_MATCH_SENTINEL in result.notes
    assert result.sources == []


def test_vault_root_derived_from_cache_path(vault: Path):
    # ResearchPhase._instantiate_tool passes cache_path=<vault>/.cache/tool_cache.db
    tool = VaultSearchTool(cache_path=vault / ".cache" / "tool_cache.db")
    assert tool.is_available() is True
    assert tool.run("warranty").sources


def test_registered_in_tool_registry_and_descriptions():
    from core.orchestrator.research_phase import TOOL_REGISTRY
    from core.tools.tool_router import _FULL_TOOL_DESCRIPTIONS

    assert TOOL_REGISTRY["vault_search"] is VaultSearchTool
    assert "vault_search" in _FULL_TOOL_DESCRIPTIONS
    # No API key required — the description must not claim one
    assert "API_KEY" not in _FULL_TOOL_DESCRIPTIONS["vault_search"]


def test_list_available_tools_sees_vault_search_with_vault(vault: Path):
    from core.orchestrator.research_phase import list_available_tools

    assert "vault_search" in list_available_tools(vault_root=vault)
    assert "vault_search" not in list_available_tools()


# ------------------------------------------------- review-fleet regression fixes

def test_construct_tool_propagates_real_init_typeerror():
    import pytest

    from core.orchestrator.research_phase import _construct_tool

    class Boom:
        def __init__(self):
            raise TypeError("boom from inside __init__")

    with pytest.raises(TypeError, match="boom from inside"):
        _construct_tool(Boom)


def test_construct_tool_passes_only_accepted_kwargs(tmp_path):
    from core.orchestrator.research_phase import _construct_tool

    class CacheOnly:
        def __init__(self, cache_path=None):
            self.cache_path = cache_path

    t = _construct_tool(CacheOnly, cache_path=tmp_path / "c.db", vault_root=tmp_path)
    assert t.cache_path == tmp_path / "c.db"


def test_run_auto_syncs_stale_index(vault):
    (vault / "00-Brain" / "new-note.md").write_text(
        "---\nlabel: internal\ntrust_tier: brain\n---\n# New\n\nFresh gasket supplier shortlist.\n",
        encoding="utf-8",
    )
    # No manual `bd-os index` after the edit — the tool must sync before searching
    result = VaultSearchTool(vault_root=vault).run("gasket supplier shortlist")
    assert result.sources


def test_no_match_sentinel_lands_in_findings_file(vault, tmp_path):
    from core.orchestrator.research_phase import ResearchPhase

    rp = ResearchPhase(llm=None, vault_root=vault)
    tool = VaultSearchTool(vault_root=vault)
    r = tool.run("xylophone quasar nonsense")
    folder = tmp_path / "task"
    folder.mkdir()
    rp._write_findings(
        folder,
        [],
        {"vault_search": [{
            "query": "xylophone quasar nonsense", "data": r.data,
            "sources": r.sources, "retrieved_at": r.retrieved_at, "notes": r.notes,
        }]},
    )
    text = (folder / "03b-research-findings.md").read_text(encoding="utf-8")
    assert NO_MATCH_SENTINEL in text


def test_list_skipped_tools_reason_for_vault_search(tmp_path):
    from core.orchestrator.research_phase import list_skipped_tools

    skipped = {s["name"]: s["reason"] for s in list_skipped_tools(vault_root=tmp_path)}
    assert "vault_search" in skipped
    assert "TAVILY" not in skipped["vault_search"]
    assert "bd-os index" in skipped["vault_search"]
