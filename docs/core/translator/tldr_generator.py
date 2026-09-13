"""Generate a TL;DR (3-5 plain-language lines) for long output."""
from __future__ import annotations


TLDR_PROMPT = """Summarize the report below into 3-5 plain-language lines a Department Head can read in 30 seconds.

## Requirements
- 3-5 lines (NO more)
- Bullet points (- ...)
- Each line: one key fact the Department Head needs to know
- Plain English, NO jargon
- CITATIONS: when a bullet repeats a figure ($, %, weeks, ...) from the body,
  carry the body's citation marker (`[[...]]`, `(ref: Q<n>)`, `<file>.md`, URL)
  onto the bullet verbatim. Never introduce a figure the body does not state —
  a scanner rejects uncited figures.
- Format:
```
## 📌 Bottom line (30-second read)
- ...
- ...
```
"""


class TLDRGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate(self, full_text: str) -> str:
        messages = [
            {"role": "system", "content": TLDR_PROMPT},
            {"role": "user", "content": full_text},
        ]
        return self.llm.complete(messages)

    def prepend(self, full_text: str) -> str:
        if "## 📌 Bottom line" in full_text:
            return full_text
        tldr = self.generate(full_text)
        return tldr + "\n\n---\n\n" + full_text
