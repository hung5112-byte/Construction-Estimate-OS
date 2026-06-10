### PROMPT 11: Standard SOP Template

#### Description
A standardized format for EVERY SOP in the company. Ensures every process is written with the same structure — easy to read, update, and train on.

#### Information to collect (ask the user before generating)
1. SOP naming convention? (e.g. SOP-[Dept]-[###])
2. Versioning: v1.0 → v1.1 (minor) → v2.0 (major), or another convention?
3. Who approves an SOP? (Manager / Owner / both)
4. A company logo for the header?
5. SOP review frequency? (6 months / 1 year)

#### Suggested template
Structure (meta-template):
- **Page 1 — SOP Template**: Header (Logo, Name, ID, Version, Date, Owner, Approver) → 7 standard sections → Footer
- **Page 2 — Fill guide**: tips for writing an effective SOP, dos/don'ts, examples
- **7 standard sections for every SOP**:
  1. Purpose (1-2 sentences)
  2. Scope (who it applies to, when)
  3. Glossary & abbreviations (table)
  4. Responsibilities (RACI table)
  5. Procedure (flowchart + step detail)
  6. Related forms (links)
  7. Change history (version log)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Standard SOP Template.

CONTEXT:
- Company: [Name]
- Naming convention: [SOP-Dept-###]
- Versioning: [v1.0 → v1.1 → v2.0]
- Approver: [title]
- Review cycle: [6 months / 1 year]

FORMAT:
- 1 page template + 1 page fill guide
- Header: Logo | SOP name | ID | Version | Issue date | Review date | Owner | Approved by
- Body sections:
  1. Purpose (1-2 sentences)
  2. Scope (who it applies to, when)
  3. Glossary & abbreviations (table)
  4. Responsibilities (RACI table)
  5. Procedure (flowchart + step detail)
  6. Related forms (links)
  7. Change history (version log)
- Footer: "Internal document — do not copy" + page number
- Guide: tips for writing an effective SOP, dos/don'ts

TONE: Meta-template, standardization guide.
LENGTH: 2-3 pages.
```

---
✍️ Author: Brian H. Doan
