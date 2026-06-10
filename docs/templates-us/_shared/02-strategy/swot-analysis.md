# PROMPT 05: SWOT Analysis

#### Description
A comprehensive Strengths-Weaknesses-Opportunities-Threats analysis, with the combined strategies SO (use strengths to seize opportunities), ST (use strengths to counter threats), WO (fix weaknesses via opportunities), WT (defend).

#### Information to collect (ask the user before generating)
1. Scope of analysis? (whole company / one product / one market)
2. Main competitors? (2-3 names)
3. Strengths you'd claim? (where do you think you're best?)
4. Biggest weakness? (where do you know you're weak?)
5. Market/industry trends you see? (opportunities)
6. The risks/threats you worry about most?
7. Any supporting data? (revenue, market share, customer survey, NPS)

#### Suggested template
Structure:
- **Executive Summary** — 5 lines: top 3 insights from the SWOT
- **SWOT Matrix** — standard 2×2 table, 5-8 items per cell
- **Detail per cell** — each item: description + evidence + impact (High/Medium/Low)
- **TOWS Matrix** — 4 combined strategies: SO, ST, WO, WT
- **Priority Actions** — top 5 priority actions based on the SWOT
- **Data Sources** — the information sources used

Confirm the structure before generating.

#### File-generation prompt
```
Create a SWOT Analysis for the business.

CONTEXT:
- Company: [Name] — Industry: [industry] — Size: [revenue, headcount]
- Scope: [whole company / product X / market Y]
- Competitors: [list 2-3]
- Strengths (owner's view): [list]
- Weaknesses (owner's view): [list]
- Opportunities (market): [list]
- Threats (concerns): [list]
- Supporting data: [if any]

FORMAT:
- SWOT 2×2 matrix: 5-8 short items per cell
- Detail table: each item = description (1-2 sentences) + evidence + impact (H/M/L)
- TOWS Matrix: 4 strategy cells, 3-5 specific strategies each
- Priority Actions: top 5, ranked, each with Owner + Timeline + Expected Impact
- Visualization data: radar chart / impact-matrix data

TONE: Analytical, evidence-based, actionable.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
