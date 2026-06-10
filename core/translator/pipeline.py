"""Compose: detect → simplify → TL;DR. Applied to the final output for the CEO."""
from __future__ import annotations
from pathlib import Path
from core.translator.glossary import Glossary
from core.translator.simplifier import Simplifier
from core.translator.tldr_generator import TLDRGenerator


class TranslatorPipeline:
    def __init__(self, llm, vault_glossary_path: Path | None = None):
        self.glossary = Glossary(vault_glossary_path=vault_glossary_path)
        self.simplifier = Simplifier(llm, glossary=self.glossary)
        self.tldr = TLDRGenerator(llm)

    def apply(self, raw_output: str) -> str:
        simplified = self.simplifier.simplify(raw_output)
        with_tldr = self.tldr.prepend(simplified)
        return with_tldr
