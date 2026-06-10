from unittest.mock import patch, MagicMock
from core.tools.us_law_search import USLawSearch


def test_us_law_search_filters_by_trusted_sites(tmp_path):
    fake_results = {
        "results": [
            {"url": "https://www.irs.gov/businesses/small-businesses-self-employed",
             "title": "Self-employed tax", "content": "..."},
            {"url": "https://statutes.capitol.texas.gov/Docs/BO/htm/BO.101.htm",
             "title": "Texas Business Organizations Code", "content": "..."},
        ],
        "answer": "Formation rules...",
    }
    with patch("tavily.TavilyClient") as M:
        c = MagicMock()
        c.search.return_value = fake_results
        M.return_value = c

        tool = USLawSearch(api_key="fake", cache_path=tmp_path / "c.db")
        result = tool.run("texas single member llc formation")

    assert all("irs.gov" in u or "texas.gov" in u or "uscode" in u
               for u in result.sources)
    assert result.data["answer"]
