"""Load 00-Brain/*.md → BrainContext."""
# Section headings below must match the English headings in the Brain templates
# (vault-template/00-Brain/ and test fixtures). Keep them in sync.
from __future__ import annotations
import re
from pathlib import Path
from core.obsidian.frontmatter import parse as parse_frontmatter
from core.brain.schema import (
    Strategy, Product, Budget, Headcount,
    LawReference, DecisionEntry, BrainContext,
)

class BrainReader:
    # Maps raw state strings from markdown to valid BusinessStage literals
    _STAGE_MAP: dict[str, str] = {
        "pre-seed": "pre-seed",
        "seed": "seed",
        "growth": "growth",
        "mature": "mature",
        "pivot": "pivot",
    }

    def __init__(self, vault_root: Path):
        self.vault = Path(vault_root)
        self.brain_dir = self.vault / "00-Brain"

    def load(self, include_decisions: bool = False) -> BrainContext:
        """include_decisions defaults to False — ADR-004 §5 (judge-only):
        BrainContext flows into MANY non-judge LLM prompts (gap analyzer,
        document executor, every debater), so episodic ledger entries must be
        opted into explicitly. Step 3's Synthesizer injection reads the ledger
        directly via DecisionLedger, not through this dump."""
        if not self.brain_dir.exists():
            raise FileNotFoundError(f"Brain dir not found: {self.brain_dir}")
        return BrainContext(
            strategy=self._read_strategy(),
            products=self._read_products(),
            budget=self._read_budget(),
            headcount=self._read_headcount(),
            laws=self._read_laws(),
            decisions=self._read_decisions() if include_decisions else [],
            state=self._read_state(),
            glossary=self._read_glossary(),
        )

    # ------------------------------------------------------------------ helpers

    def _read_file(self, name: str) -> tuple[dict, str]:
        path = self.brain_dir / name
        if not path.exists():
            return {}, ""
        return parse_frontmatter(path.read_text(encoding="utf-8"))

    def _extract_section(self, body: str, heading: str) -> str:
        """Return content after `## heading` until next ## or EOF."""
        pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)"
        m = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
        return m.group(1).strip() if m else ""

    # ------------------------------------------------------------------ parsers

    def _read_strategy(self) -> Strategy:
        _, body = self._read_file("strategy.md")
        vision = self._extract_section(body, "Vision") or "(not filled in)"
        icp = self._extract_section(body, "Target Customer (ICP)") or "(not filled in)"
        return Strategy(vision=vision, icp=icp)

    def _read_products(self) -> list[Product]:
        _, body = self._read_file("products.md")
        # Parse markdown table rows: | CODE | Name | price | margin | status |
        rows = re.findall(
            r"\|\s*([A-Z][A-Z0-9]*)\s*\|\s*([^|]+?)\s*\|\s*\$?([\d_,.]+)\s*\|\s*(\d+(?:\.\d+)?)\s*\|\s*(\w+)\s*\|",
            body,
        )
        return [
            Product(
                code=r[0],
                name=r[1].strip(),
                price_usd=int(re.sub(r"[_,.]", "", r[2])),
                margin_pct=float(r[3]),
                status=r[4],
            )
            for r in rows
        ]

    def _read_budget(self) -> Budget:
        _, body = self._read_file("budget.md")
        total_match = re.search(r"Total budget:\s*\$?([\d_,.]+)", body)
        total = int(re.sub(r"[_,.]", "", total_match.group(1))) if total_match else 0
        return Budget(total_year_usd=total)

    def _read_headcount(self) -> Headcount:
        _, body = self._read_file("headcount.md")
        depts = re.findall(r"^-\s+(\d{2}-[\w-]+)", body, re.MULTILINE)
        return Headcount(active_departments=depts)

    def _read_laws(self) -> list[LawReference]:
        _, body = self._read_file("laws.md")
        # Match "- Law name (citation)" where the citation is any parenthetical,
        # e.g. "(26 U.S.C. § 11)" or "(Tex. Bus. Orgs. Code)".
        rows = re.findall(r"-\s+(.+?)\s*\(([^)]+)\)", body)
        return [LawReference(name=r[0], code=r[1]) for r in rows]

    def _read_decisions(self) -> list[DecisionEntry]:
        # Structured entries come from decision-ledger.md (ADR-004 §1); the
        # prose decisions-log.md is frozen history and stays unparsed.
        from core.brain.ledger import DecisionLedger, LEDGER_FILENAME

        return DecisionLedger(self.brain_dir / LEDGER_FILENAME).entries()

    def _read_state(self) -> str:
        _, body = self._read_file("state.md")
        section = self._extract_section(body, "Stage")
        if not section:
            return "unknown"
        m = re.search(r"\[(\w[\w\s/-]+)\]", section)
        raw = m.group(1) if m else "unknown"
        return self._STAGE_MAP.get(raw.lower().strip(), "unknown")

    def _read_glossary(self) -> dict[str, str]:
        _, body = self._read_file("glossary.md")
        terms = re.findall(r"^-\s+\*\*(.+?)\*\*:\s*(.+)$", body, re.MULTILINE)
        return dict(terms)
