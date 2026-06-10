from core.tools.industry_benchmark import IndustryBenchmark


def test_lookup_saas_cac():
    tool = IndustryBenchmark()
    r = tool.run("saas_b2b cac")
    assert r.data["median"] == 320


def test_lookup_unknown_returns_empty():
    tool = IndustryBenchmark()
    r = tool.run("madeup_industry blah")
    assert r.data == {} or r.data.get("not_found")
