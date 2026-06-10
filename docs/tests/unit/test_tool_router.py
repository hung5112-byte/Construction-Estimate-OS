from unittest.mock import MagicMock
import json
from core.tools.tool_router import ToolRouter


def test_decides_tools_from_brief():
    fake = json.dumps({
        "tools": [
            {"tool": "us_law_search", "queries": ["advertising law"]},
            {"tool": "competitor_research", "queries": ["SaaS competitors"]},
            {"tool": "industry_benchmark", "queries": ["saas_b2b cac"]},
        ]
    })
    llm = MagicMock(complete=MagicMock(return_value=fake))

    router = ToolRouter(llm=llm)
    plan = router.plan(brief="Create a B2B SaaS ad campaign", brain_summary="...")

    tools = [p["tool"] for p in plan]
    assert "us_law_search" in tools
    assert "competitor_research" in tools
