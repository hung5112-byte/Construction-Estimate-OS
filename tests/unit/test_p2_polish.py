"""Test P2 polish: slugify with diacritics, robust JSON parse, brain filter, cache per-vault."""
from __future__ import annotations


from core.orchestrator.flow_controller import _slugify
from core.orchestrator.router import Router
from core.tools.tool_router import ToolRouter
from core.agents.base_agent import BaseAgent


# ─────────────────────────────────── P2.6: Slugify diacritics ─────────────────


class TestSlugify:
    def test_strips_accents(self):
        assert _slugify("Café Señor") == "cafe-senor"

    def test_diacritics_normalized(self):
        assert _slugify("Résumé Review") == "resume-review"
        assert _slugify("Piñata") == "pinata"

    def test_full_brief_compound(self):
        result = _slugify("Create capability profile Andy Tech Marketing")
        assert result == "create-capability-profile-andy-tech-marketing"

    def test_keeps_alphanumeric(self):
        assert _slugify("Q2 Analysis") == "q2-analysis"

    def test_empty_falls_back_to_task(self):
        assert _slugify("!!!") == "task"

    def test_max_len_respected(self):
        long = "x" * 100
        assert len(_slugify(long, max_len=50)) <= 50


# ─────────────────────────────────── P2.2: JSON parse ─────────────────────────


class _MockLLM:
    def __init__(self, response):
        self.response = response

    def complete(self, messages, model=None):
        return self.response


class TestRouterJSONParse:
    def _classify(self, raw):
        from core.brain.schema import (
            BrainContext, Strategy, Budget, Headcount,
        )
        brain = BrainContext(
            strategy=Strategy(vision="x", icp="x"),
            products=[],
            budget=Budget(total_year_usd=0),
            headcount=Headcount(active_departments=[]),
            laws=[], decisions=[], state="seed", glossary={},
        )
        router = Router(_MockLLM(raw))
        return router.classify("brief", brain)

    def test_clean_json(self):
        raw = '{"class": "SIMPLE", "departments": ["03-quality-reliability"], "reasoning": "ok"}'
        result = self._classify(raw)
        assert result.class_.value == "SIMPLE"

    def test_code_fence(self):
        raw = '```json\n{"class": "COMPLEX", "departments": ["01-hardware-engineering"], "reasoning": "x"}\n```'
        result = self._classify(raw)
        assert result.class_.value == "COMPLEX"

    def test_prose_then_json(self):
        raw = 'Here is the answer:\n{"class": "STRATEGIC", "departments": ["02-npi-program-management"], "reasoning": "y"}\nDone.'
        result = self._classify(raw)
        assert result.class_.value == "STRATEGIC"

    def test_nested_object_not_merged(self):
        """Ensure nested {} does not break parsing — strategy 3 (balanced) handles it."""
        raw = '{"class": "SIMPLE", "departments": [], "reasoning": "a", "extra": {"k": "v"}}'
        result = self._classify(raw)
        assert result.class_.value == "SIMPLE"


class TestToolRouterJSONParse:
    def test_extracts_json_from_fence(self):
        raw = '```json\n{"tools": [{"tool": "industry_benchmark", "queries": ["x"]}]}\n```'
        router = ToolRouter(_MockLLM(raw), available_tools=["industry_benchmark"])
        plan = router.plan("brief", "brain")
        assert len(plan) == 1
        assert plan[0]["tool"] == "industry_benchmark"

    def test_returns_empty_on_unparseable(self):
        router = ToolRouter(_MockLLM("Sorry I cannot help"), available_tools=["x"])
        assert router.plan("b", "br") == []


# ─────────────────────────────────── P2.7: Brain filter ───────────────────────


class TestBrainContextFilter:
    def _make_agent(self, refs):
        return BaseAgent(
            name_vn="X", role="X", system_prompt="X",
            llm=_MockLLM(""), required_refs=refs,
        )

    def test_filter_by_required_refs(self):
        agent = self._make_agent(["strategy", "laws"])
        ctx = {
            "strategy": {"vision": "v"},
            "laws": [{"name": "Texas Business Organizations Code"}],
            "budget": {"total": 1000},
            "headcount": {},
            "products": [],
            "decisions": [],
            "state": "seed",
            "glossary": {"sales tax": "Texas sales-and-use tax"},
        }
        filtered = agent._filter_brain(ctx)
        assert "strategy" in filtered
        assert "laws" in filtered
        assert "budget" not in filtered
        # glossary always included
        assert "glossary" in filtered

    def test_no_required_refs_returns_full(self):
        agent = self._make_agent([])
        ctx = {"strategy": {}, "budget": {}}
        assert agent._filter_brain(ctx) == ctx

    def test_md_extension_stripped(self):
        agent = self._make_agent(["strategy.md"])
        ctx = {"strategy": "s", "budget": "b", "glossary": {}}
        filtered = agent._filter_brain(ctx)
        assert "strategy" in filtered

    def test_alias_finance_to_budget(self):
        agent = self._make_agent(["finance"])
        ctx = {"budget": "b", "strategy": "s", "glossary": {}}
        filtered = agent._filter_brain(ctx)
        assert "budget" in filtered


# ─────────────────────────────────── P2.3: Cache per-vault ────────────────────


class TestCachePerVault:
    def test_research_phase_uses_vault_cache_path(self, tmp_path):
        from core.orchestrator.research_phase import ResearchPhase

        rp = ResearchPhase(_MockLLM(""), vault_root=tmp_path)
        cache_path = rp._cache_path()
        assert cache_path is not None
        assert tmp_path in cache_path.parents
        assert cache_path.parent.exists()

    def test_research_phase_no_vault_returns_none(self):
        from core.orchestrator.research_phase import ResearchPhase

        rp = ResearchPhase(_MockLLM(""))
        assert rp._cache_path() is None
