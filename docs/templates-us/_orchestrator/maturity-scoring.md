# PROMPT 07: Maturity Scoring

#### Description
A form to score the business's maturity level across 9 dimensions. Used in the Scope Assessment step to set priorities, and in the Handover Report to compare before/after.

#### Information to collect (ask the user before generating)
1. Customize the 9 dimensions or use the standard? (Strategy, Finance, Marketing, Sales, Operations, People, Technology, Governance, Training)
2. Scale: 0-5 or 1-10?
3. Need a detailed rubric per level?
4. Need an industry benchmark?

#### Suggested template
Structure:
- **Scoring Matrix** — 9 dimensions × 6 levels (0-5), each cell with a specific description
- **Level Definitions** — Level 0 (Ad-hoc) → 1 (Initial) → 2 (Defined) → 3 (Managed) → 4 (Optimized) → 5 (World-class)
- **Scoring Guide** — how to score: evidence-based, concrete examples
- **Summary Spider Chart** — data template for a radar chart
- **Benchmark Reference** — comparison to the industry average (if available)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Maturity Scoring Framework for the Business Packaging system.

CONTEXT:
- 9 dimensions: [list or use the standard]
- Scale: [0-5 / 1-10]
- Purpose: assess before packaging (baseline) and after completion (progress)

FORMAT:
- Overview table: 9 dimensions × Score × Evidence × Notes
- Detailed rubric: each dimension × each level = a 2-3 line description + a concrete example
  - e.g. Marketing Level 2 = "Has a page, posts irregularly, no content calendar yet"
- Spider-chart data template: a data table to draw the radar chart
- Interpretation guide: total score → recommended action
  - 0-15: "Startup mode — build from the foundation"
  - 16-30: "Growing — needs systematization"
  - 31-45: "Mature — optimize & automate"

TONE: Objective, evidence-based, non-judgmental.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
