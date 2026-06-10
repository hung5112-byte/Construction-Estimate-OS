from unittest.mock import patch, MagicMock
from core.tools.us_local_regulation import USLocalRegulation


def test_local_reg_searches_government_sites(tmp_path):
    fake = {"results": [{"url": "https://comptroller.texas.gov/taxes/sales/",
                         "title": "Sales tax", "content": "..."}],
            "answer": "..."}
    with patch("tavily.TavilyClient") as M:
        c = MagicMock()
        c.search.return_value = fake
        M.return_value = c
        tool = USLocalRegulation(api_key="x", cache_path=tmp_path / "c.db")
        r = tool.run("sales tax permit", jurisdiction="Texas")
    assert "comptroller.texas.gov" in r.sources[0]
