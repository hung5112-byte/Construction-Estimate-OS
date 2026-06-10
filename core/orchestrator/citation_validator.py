"""P1.8 — Citation validator post-Synthesizer.

Parse the decision-report markdown, find claims with facts/numbers/regulations
that have no citation, and append a warning at the end of the report.

Heuristics (not too strict):
- Claim = a sentence with a concrete figure (e.g. "up 20%", "$5,000", "30 days")
  OR a law/code reference (e.g. "26 U.S.C. § 11", "Tex. Tax Code", "FLSA")
- Citation = a sentence/block containing [source: ...] or a Brain file cite (strategy.md, laws.md, ...)
  or a URL (http/https)
- Common-knowledge phrases are exempt (no cite needed)
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


# ────────────────────────────── Patterns ─────────────────────────────── #

# Concrete figures: percent, USD currency, durations.
# NOTE: the outer \b is omitted intentionally — % and $ are non-word chars, so a \b
# next to them creates an impossible boundary. The patterns are specific enough.
_RE_NUMERIC_CLAIM = re.compile(
    r"""
    (?:
        \d+[\.,]?\d*\s*%                                                  # percent: 20%, 3.5%
      | \$\s*\d[\d,]*(?:\.\d+)?\s*(?:K|M|B|thousand|million|billion)?     # USD: $5,000, $1.2M
      | \d+[\.,]?\d*\s*(?:K|M|B|thousand|million|billion)\s*(?:USD|dollars)?  # 5 million USD
      | \d+[\.,]?\d*\s*(?:USD|EUR|dollars)                                # other currency
      | \d+\s*(?:day|days|week|weeks|month|months|year|years|hour|hours|minute|minutes)  # durations
      | \d{1,3}(?:,\d{3})+                                                # large numbers: 1,000,000
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Law / code / statute references (US).
_RE_LEGAL_CLAIM = re.compile(
    r"""
    (?:
        \d+\s*U\.?\s*S\.?\s*C\.?\s*(?:§\s*)?\d*       # 26 U.S.C. § 11
      | \d+\s*C\.?\s*F\.?\s*R\.?\s*\d*                # 12 C.F.R. 1005
      | Tex\.\s*[\w.]+\s*Code                          # Tex. Tax Code
      | (?:Section|§)\s*\d+                            # Section 171, § 521
      | \b(?:IRC|TBOC|TDPSA|FLSA|FTC|HIPAA|GLBA|FICA|FUTA|SUTA)\b   # named codes/acts
      | \b[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*\s+Act\b   # Fair Labor Standards Act
    )
    """,
    re.VERBOSE,
)

# Accepted citation markers
_RE_CITATION = re.compile(
    r"""
    (?:
        \[source\s*:\s*[^\]]+\]          # [source: ...]
      | \[[^\]]+\.md[^\]]*\]             # [strategy.md], [finance.md:12], etc.
      | \[[^\]]+\]\(https?://[^\)]+\)    # markdown link with a URL
      | https?://\S+                     # bare URL
      | \*\s*Source\s*:                  # * Source:
      | Brain\s*reference\s*:            # "Brain reference:"
      | cite\s*[:：]                     # "cite:"
      | \(Brain\s*[^)]+\)                # (Brain strategy.md)
      | \[[^\]]*(?:strategy|products|budget|headcount|laws|decisions-log|state|glossary)\.md[^\]]*\]
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Brain file names (the real 8 sections) — if a sentence mentions one, treat it as cited
_RE_BRAIN_FILE = re.compile(
    r"\b(?:strategy|products|budget|headcount|laws|decisions-log|state|glossary)\.md\b",
    re.IGNORECASE,
)

# Common-knowledge phrases — exempt, no citation needed
_COMMON_KNOWLEDGE_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r"holiday\s+season",
        r"cultural\s+tradition",
        r"common\s+practice",
        r"as\s+a\s+rule\s+of\s+thumb",
        r"rule\s+of\s+thumb",
        r"typically",
        r"generally",
        r"commonly",
        r"industry\s+norm",
    ]
]

# Skip section headings and frontmatter lines
_RE_HEADING = re.compile(r"^#{1,6}\s+|^---|^\*\*\*|^---$")
# Sentences too short (< 20 chars) — not enough context to be a claim
_MIN_SENTENCE_LEN = 20


# ────────────────────────────── Data model ─────────────────────────────── #


@dataclass
class CitationFlag:
    """A claim missing a citation."""
    line_no: int
    sentence: str
    reason: str  # "numeric_claim" | "legal_claim"


# ────────────────────────────── Validator ─────────────────────────────── #


class CitationValidator:
    """Validate the decision report, flag claims missing a citation, append a warning section."""

    # Warning section header injected at the end of the report
    WARNING_HEADER = "\n\n---\n\n## ⚠️ Warning: claims missing a source\n\n"
    WARNING_INTRO = (
        "The following sentences contain figures or legal references but no clear "
        "citation was found. The CEO should verify them before proceeding:\n\n"
    )

    def validate(self, report_path: Path) -> list[CitationFlag]:
        """Read the report, flag claims missing a citation, write the warning section to the file.

        Returns:
            A list of CitationFlag (may be empty if there are no issues).
        """
        path = Path(report_path)
        if not path.exists():
            return []

        content = path.read_text(encoding="utf-8")
        flags = self._find_uncited_claims(content)

        if flags:
            warning = self._build_warning_section(flags)
            # Append the warning — only if not already present (avoid double-append on re-validate)
            if self.WARNING_HEADER.strip() not in content:
                path.write_text(content + warning, encoding="utf-8")

        return flags

    def _find_uncited_claims(self, content: str) -> list[CitationFlag]:
        """Parse each sentence in the content, return the list of flags."""
        flags: list[CitationFlag] = []
        lines = content.splitlines()

        for line_no, line in enumerate(lines, start=1):
            # Skip headings, frontmatter, blank lines
            stripped = line.strip()
            if not stripped or _RE_HEADING.match(stripped):
                continue
            # Skip code blocks (don't validate code/yaml content)
            if stripped.startswith("```") or stripped.startswith("|"):
                continue

            # A citation marker may appear after a period on the same line (e.g.
            # "Revenue up 25%. [source: finance.md]"). Check the whole line;
            # if it has a citation, skip every sentence on that line.
            line_has_cite = bool(
                _RE_CITATION.search(stripped) or _RE_BRAIN_FILE.search(stripped)
            )

            # Split sentences within the line (by period/question/exclamation mark)
            sentences = _split_sentences(stripped)

            for sentence in sentences:
                if len(sentence) < _MIN_SENTENCE_LEN:
                    continue
                if _is_common_knowledge(sentence):
                    continue

                # Check for a citation in the sentence or elsewhere on the line
                has_cite = line_has_cite or bool(
                    _RE_CITATION.search(sentence) or _RE_BRAIN_FILE.search(sentence)
                )
                if has_cite:
                    continue

                # Flag if there is a numeric claim
                if _RE_NUMERIC_CLAIM.search(sentence):
                    flags.append(CitationFlag(
                        line_no=line_no,
                        sentence=sentence[:200],
                        reason="numeric_claim",
                    ))
                # Flag if it mentions a law/code with no citation
                elif _RE_LEGAL_CLAIM.search(sentence):
                    flags.append(CitationFlag(
                        line_no=line_no,
                        sentence=sentence[:200],
                        reason="legal_claim",
                    ))

        return flags

    def _build_warning_section(self, flags: list[CitationFlag]) -> str:
        """Build the markdown warning section from the list of flags."""
        lines = [self.WARNING_HEADER, self.WARNING_INTRO]
        for f in flags:
            label = "Figure" if f.reason == "numeric_claim" else "Legal"
            lines.append(f"- **[Line {f.line_no}] {label}:** {f.sentence}\n")
        return "".join(lines)


# ────────────────────────────── Helpers ─────────────────────────────── #


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences by sentence-ending punctuation.

    No complex regex — a simple split is enough for this heuristic validator.
    """
    # Split at period/question/exclamation marks, keeping the boundary
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def _is_common_knowledge(sentence: str) -> bool:
    """Return True if the sentence is common knowledge that needs no cite."""
    return any(p.search(sentence) for p in _COMMON_KNOWLEDGE_PATTERNS)
