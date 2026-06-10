# PROMPT 08: Master Glossary

#### Description
A unified glossary for the entire 200+ document system. Ensures every sub-skill uses the same terms, the same abbreviations, and the same definitions — so "KPI" in file A doesn't mean something different in file B.

#### Information to collect (ask the user before generating)
1. Does the company have its own internal terms? (e.g. calling employees "partners", customers "members")
2. Document language: English (with any specialized terms defined)?
3. Any internal acronyms to include?
4. Organize by topic or alphabetically?

#### Suggested template
Structure:
- **Usage rules** — how to use the glossary, when to reference it
- **Main glossary table** — Term | Abbreviation | Definition | Example | Used in skill #
- **By topic** — 9 groups for the 9 business dimensions
- **Company-internal terms** — a separate section for company-specific terms
- **Abbreviation list** — A-Z quick reference
- **Version log** — who changed what, when

Confirm the structure before generating.

#### File-generation prompt
```
Create a Master Glossary for the Business Packaging system.

CONTEXT:
- A system of 200+ documents, 12 sub-skills, 9 business dimensions
- Language: English (specialized terms defined on first use)
- Company: [Company name] — internal terms: [list if any]

FORMAT:
- Main table: # | Term | Abbreviation | Definition | Usage example | Appears in skill
- Grouped by the 9 dimensions + 1 "General" group
- Quick Reference Card: 1 page, abbreviations + short meaning only
- Initial base terms: ~100-150 common business terms
- Leave the "Company-internal terms" section blank for the owner to fill in

TONE: Reference material — concise, precise, easy to look up.
LENGTH: 10-15 pages (including ~150 starter terms).
```

---
✍️ Author: Brian H. Doan
