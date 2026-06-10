# PROMPT 05: Quality Checklist

#### Description
A checklist form to verify each sub-skill produced the expected output, in the right format, with the right content. Used after finishing each skill and after finishing the whole system.

#### Information to collect (ask the user before generating)
1. Which quality standard applies? (ISO 9001 / internal standard / custom)
2. Who checks? (AI auto-check / coach / both)
3. Pass/fail level: minimum % complete to count as "done"?
4. Need scoring, or just pass/fail per item?

#### Suggested template
Structure:
- **Per-Skill Checklist** — 12 tables, each listing expected files + criteria
- **Cross-Skill Checklist** — consistency check: terms, format, cross-references
- **Completeness Score** — files created / files expected × 100%
- **Quality Score** — based on criteria: accuracy, completeness, consistency, usability
- **Issues Log** — a table of issues + severity + action required

Confirm the structure before generating.

#### File-generation prompt
```
Create a Quality Checklist for the Business Packaging system.

CONTEXT:
- 12 sub-skills, each producing 5-20 files
- Total: 200+ files to check
- Standard: [ISO 9001 / internal / custom]
- Checker: [AI / coach / both]
- Pass threshold: [minimum %]

FORMAT:
- Per-skill checklist: table | File | Present? | Correct format | Complete content | Notes
- Cross-skill checklist: consistent terms | correct cross-refs | naming convention | version
- Summary scorecard: Skill × 4 criteria = score matrix
- Issues log template: # | Skill | File | Issue | Severity | Action | Owner | Due
- Final sign-off section: coach signature + owner signature + date

TONE: Serious, standards-based, audit-style.
LENGTH: 8-10 pages (including 12 per-skill tables).
```

---
✍️ Author: Brian H. Doan
