"""Auto-grow the glossary from outputs + look up terms from terms_dictionary."""
from __future__ import annotations
from pathlib import Path
import yaml
import re


DICT_PATH = Path(__file__).parent / "terms_dictionary.yaml"


class Glossary:
    def __init__(self, vault_glossary_path: Path | None = None):
        self.dict_data = yaml.safe_load(DICT_PATH.read_text(encoding="utf-8"))
        self.vault_path = vault_glossary_path
        self.vault_terms = self._load_vault() if vault_glossary_path else {}

    def _load_vault(self) -> dict[str, str]:
        if not self.vault_path.exists():
            return {}
        content = self.vault_path.read_text(encoding="utf-8")
        terms = re.findall(r"^-\s+\*\*(.+?)\*\*:\s*(.+)$", content, re.MULTILINE)
        return dict(terms)

    def lookup(self, term: str) -> str | None:
        if term in self.vault_terms:
            return self.vault_terms[term]
        for category, items in self.dict_data.items():
            if term in items:
                meta = items[term]
                if isinstance(meta, dict) and "en" in meta:
                    return meta["en"]
        return None

    def add_term(self, term: str, definition: str, category: str = "auto") -> None:
        self.vault_terms[term] = definition
        if self.vault_path:
            self._persist_vault(category)

    def _persist_vault(self, category: str):
        content = "---\ntype: brain\nsection: glossary\n---\n# Glossary\n\n"
        for term, defn in self.vault_terms.items():
            content += f"- **{term}**: {defn}\n"
        self.vault_path.write_text(content, encoding="utf-8")
