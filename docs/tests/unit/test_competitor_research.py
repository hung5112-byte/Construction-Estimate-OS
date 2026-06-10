from unittest.mock import patch, MagicMock
from core.tools.competitor_research import CompetitorResearch


def test_extracts_competitors_from_query(tmp_path):
    fake = {"results": [
        {"url": "https://quickbooks.com", "title": "QuickBooks", "content": "..."},
        {"url": "https://gusto.com", "title": "Gusto", "content": "..."},
    ], "answer": "Top SME management SaaS in the US..."}
    with patch("tavily.TavilyClient") as M:
        c = MagicMock()
        c.search.return_value = fake
        M.return_value = c
        tool = CompetitorResearch(api_key="x", cache_path=tmp_path / "c.db")
        r = tool.run("US SME management SaaS")

    assert len(r.sources) == 2
    assert "quickbooks.com" in r.sources[0]
