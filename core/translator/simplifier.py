"""Rewrite output to inject term definitions (RULE 4)."""
from __future__ import annotations
from core.translator.jargon_detector import JargonDetector
from core.translator.glossary import Glossary


SIMPLIFIER_PROMPT = """You are a business editor. Rewrite the text below so a non-technical CEO can easily understand it.

## Requirements
- Define EVERY domain term the first time it appears, format:
  **Term** (simple explanation — a concrete example for this company)
- Replace hard words with everyday words when equivalent (lead → interested customer, churn → customers leaving)
- Short, readable sentences
- Do NOT change meaning, do not add or remove information
- Plain English

## Existing glossary (use as reference)
{glossary_subset}
"""


class Simplifier:
    def __init__(self, llm, glossary: Glossary | None = None):
        self.llm = llm
        self.glossary = glossary or Glossary()
        self.detector = JargonDetector(self.glossary)

    def simplify(self, text: str) -> str:
        terms = self.detector.detect(text)
        if not terms:
            return text

        glossary_text = "\n".join(
            f"- **{t}**: {defn or '(not yet defined, please explain in plain English)'}"
            for t, defn in terms
        )

        messages = [
            {"role": "system", "content": SIMPLIFIER_PROMPT.format(glossary_subset=glossary_text)},
            {"role": "user", "content": text},
        ]
        return self.llm.complete(messages)
