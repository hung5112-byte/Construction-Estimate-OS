"""Test env loading + tool availability + ToolRouter filter — no real keys used."""
from __future__ import annotations
import os

from core.utils.config import load_vault_env, save_vault_env, apply_vault_env_to_os
from core.tools.web_search import WebSearch
from core.tools.us_law_search import USLawSearch
from core.tools.industry_benchmark import IndustryBenchmark
from core.tools.tax_calculator import TaxCalculator
from core.tools.tool_router import ToolRouter


def test_save_and_load_vault_env(tmp_path):
    save_vault_env(tmp_path, {"TAVILY_API_KEY": "abc123", "EMPTY_KEY": ""})
    env = tmp_path / ".env"
    assert env.exists()
    loaded = load_vault_env(tmp_path)
    assert loaded["TAVILY_API_KEY"] == "abc123"
    assert "EMPTY_KEY" not in loaded


def test_save_vault_env_adds_gitignore_entry(tmp_path):
    save_vault_env(tmp_path, {"TAVILY_API_KEY": "x"})
    gitignore = (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore


def test_save_vault_env_idempotent_merge(tmp_path):
    save_vault_env(tmp_path, {"TAVILY_API_KEY": "k1"})
    save_vault_env(tmp_path, {"GOOGLE_API_KEY": "k2"})
    loaded = load_vault_env(tmp_path)
    assert loaded["TAVILY_API_KEY"] == "k1"
    assert loaded["GOOGLE_API_KEY"] == "k2"


def test_apply_vault_env_to_os(tmp_path, monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    save_vault_env(tmp_path, {"TAVILY_API_KEY": "from-vault"})
    apply_vault_env_to_os(tmp_path)
    assert os.environ.get("TAVILY_API_KEY") == "from-vault"


def test_tool_skips_when_no_api_key(monkeypatch, tmp_path):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    tool = WebSearch(cache_path=tmp_path / "cache.db")
    assert tool.is_available() is False
    result = tool.run("hello")
    assert result.data["skipped"] is True
    assert "TAVILY_API_KEY" in result.notes


def test_tool_available_with_explicit_key(tmp_path):
    tool = USLawSearch(api_key="x", cache_path=tmp_path / "cache.db")
    assert tool.is_available() is True


def test_industry_benchmark_always_available():
    tool = IndustryBenchmark()
    assert tool.is_available() is True


def test_tax_calculator_always_available():
    tool = TaxCalculator()
    assert tool.is_available() is True


def test_tool_router_filters_by_available_tools(monkeypatch):
    """Router with available_tools=['industry_benchmark', 'tax_calculator']
    must not plan tools outside the list even if the LLM returns them."""
    class MockLLM:
        def complete(self, messages, model=None):
            return (
                '{"tools": ['
                '{"tool": "web_search", "queries": ["x"]},'
                '{"tool": "industry_benchmark", "queries": ["y"]}'
                ']}'
            )

    router = ToolRouter(
        MockLLM(), available_tools=["industry_benchmark", "tax_calculator"]
    )
    plan = router.plan("brief", "brain")
    names = [c["tool"] for c in plan]
    assert "web_search" not in names
    assert "industry_benchmark" in names


def test_tool_router_empty_available_returns_empty_plan():
    """No credentialed tools → no LLM call, return []."""
    class FailLLM:
        def complete(self, *_args, **_kw):
            raise AssertionError("LLM should NOT be called when available is empty")

    router = ToolRouter(FailLLM(), available_tools=[])
    assert router.plan("brief", "brain") == []


def test_research_phase_lists_available_and_skipped(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    from core.orchestrator.research_phase import (
        list_available_tools, list_skipped_tools,
    )
    available = list_available_tools()
    skipped = list_skipped_tools()
    skipped_names = [s["name"] for s in skipped]
    assert "industry_benchmark" in available
    assert "tax_calculator" in available
    assert "web_search" in skipped_names
    assert "us_law_search" in skipped_names
