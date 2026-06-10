# PROMPT 11: OGSM Framework

#### Description
OGSM (Objectives-Goals-Strategies-Measures) — a one-page strategy tool connecting the long-term vision to specific actions. Simpler than a business plan, easy to communicate to the whole team.

#### Information to collect (ask the user before generating)
1. Objective (the big goal): what does the company want to achieve in the next 3-5 years?
2. Goals (measurable goals): specific KPIs with targets?
3. Strategies: 3-5 main approaches?
4. Time period: which fiscal year?
5. Do you already have OKRs? (OGSM sits a level above OKR)

#### Suggested template
Structure (1-2 pages):
- **Objective** — one sentence, qualitative, inspiring (e.g. "Become the #1 marketing platform for US small businesses")
- **Goals** — 3-5 metrics, quantitative, time-bound (e.g. "$100M revenue by 2027", "50,000 active customers")
- **Strategies** — 3-5 major strategies, each with a short description
- **Measures** — each strategy has 2-3 specific KPIs + target + measurement frequency
- **OGSM Map** — 1-page visual: O → G1,G2,G3 → S1,S2,S3 → M1.1, M1.2...

Confirm the structure before generating.

#### File-generation prompt
```
Create an OGSM Framework.

CONTEXT:
- Company: [Name] — Objective: [describe the big goal]
- Goals: [list KPIs + targets]
- Strategies: [list 3-5 strategies]
- Period: [year/phase]
- Existing OKR: [Yes/No]

FORMAT:
- OGSM table: 4 columns (O|G|S|M), clear cascade
- 1-page overview: fits on 1 page, landscape orientation
- Detail page: each Strategy → Measures → action items → owner → timeline
- Alignment check: each Measure links up to a Goal, each Goal links up to the Objective
- Quarterly review template: a progress-review table

TONE: Strategic, concise, executive-friendly.
LENGTH: 2-4 pages (1 page OGSM + 1-3 pages detail).
```

---
✍️ Author: Brian H. Doan
