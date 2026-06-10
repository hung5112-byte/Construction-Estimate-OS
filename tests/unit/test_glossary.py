from core.translator.glossary import Glossary


def test_lookup_known_term():
    g = Glossary()
    assert "customer" in g.lookup("CAC").lower()


def test_lookup_unknown_returns_none():
    g = Glossary()
    assert g.lookup("XYZ_ABC") is None


def test_add_term_persists(tmp_path):
    p = tmp_path / "glossary.md"
    p.write_text("---\n---\n# G\n", encoding="utf-8")
    g = Glossary(vault_glossary_path=p)
    g.add_term("FOOBAR", "a definition")
    assert "FOOBAR" in p.read_text(encoding="utf-8")
