from core.translator.jargon_detector import JargonDetector


def test_detects_marketing_jargon():
    jd = JargonDetector()
    found = jd.detect("Target CAC $300, ROAS >= 3.2x")
    terms = [t for t, _ in found]
    assert "CAC" in terms
    assert "ROAS" in terms


def test_filters_out_common_acronyms():
    jd = JargonDetector()
    found = jd.detect("Your LLC in the US, met the Department Head on Mon")
    terms = [t for t, _ in found]
    assert "LLC" not in terms
    assert "US" not in terms
