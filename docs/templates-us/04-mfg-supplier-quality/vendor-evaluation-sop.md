### PROMPT 06: Vendor Evaluation SOP

#### Description
A process to evaluate and select vendors — evaluation criteria, the approval process, periodic re-evaluation, and blacklisting. Ensures the company works with reliable, quality vendors at fair prices.

#### Information to collect (ask the user before generating)
1. How many vendors do you work with? Main categories?
2. Most important criteria? (price / quality / delivery / service?)
3. Re-evaluation frequency? (6 months / 1 year)
4. Who decides on a vendor? (Procurement / Committee / Owner)
5. Any single-source vendors (only one vendor for a given item)?
6. Do you require vendors to hold ISO or special certifications?

#### Suggested template
Structure:
- **Step 1** — Define the need: category, specs, volume
- **Step 2** — Source vendors: sources, longlist
- **Step 3** — Pre-qualify: basic criteria, shortlist
- **Step 4** — Detailed evaluation: scorecard, site visit, sample test
- **Step 5** — Negotiate & select: master agreement, terms
- **Step 6** — Vendor onboarding: system setup, test order
- **Step 7** — Re-evaluation: periodic review, adjust or replace
- **Blacklist**: criteria to blacklist, process

Confirm the structure before generating.

#### File-generation prompt
```
Create a Vendor Evaluation SOP.

CONTEXT:
- Company: [Name] — # vendors: [number] — Categories: [list]
- Priority criteria: [price / quality / delivery / service]
- Re-evaluate: [6 months / 1 year]
- Approver: [Procurement / Committee / Owner]
- Single-source: [Yes/No]
- ISO requirement: [Yes/No]

FORMAT:
- 7-step flowchart: Mermaid — need to re-evaluation
- Pre-qualification checklist: 10 Go/No-Go criteria
- Scorecard reference: link to frm-scorecard-ncc.md
- Decision matrix: score range → Approved / Conditional / Rejected
- Re-evaluation schedule: 12-month calendar × main vendors
- Blacklist criteria: 5-7 conditions → blacklist + appeal process

TONE: Professional procurement, objective, data-driven.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
