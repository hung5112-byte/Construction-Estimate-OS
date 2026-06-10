from unittest.mock import MagicMock
from core.translator.pipeline import TranslatorPipeline


def test_pipeline_simplifies_and_prepends_tldr():
    llm = MagicMock()
    llm.complete.side_effect = [
        "rewritten with **CAC** (cost per customer)",
        "## 📌 Bottom line\n- key1\n- key2\n- key3",
    ]

    p = TranslatorPipeline(llm=llm)
    out = p.apply("CAC up 30%, action needed now")

    assert out.startswith("## 📌 Bottom line")
    assert "**CAC**" in out
