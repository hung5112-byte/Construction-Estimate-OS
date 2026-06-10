# PROMPT 18: Scenario Planning

#### Description
Three strategic scenarios: Best Case, Base Case, Worst Case. Each has assumptions, impact, an action plan, and a financial projection. Helps the company prepare for several possible futures.

#### Information to collect (ask the user before generating)
1. The key variables that most affect the company? (market, regulation, technology, competition, macroeconomy)
2. Current financial projections (base case)?
3. What's your best case? (what if everything goes right)
4. Worst case? (what keeps you up at night)
5. Trigger points: what signals tell you which scenario you're entering?
6. Any pivot options? (if the bad scenario hits, how could the company change course?)

#### Suggested template
Structure:
- **Key Uncertainties** — 3-5 key variables, each with a range (high/base/low)
- **3 Scenarios** — 2-3 pages each:
  - Narrative: a written description — "In 2028, the market..."
  - Assumptions: table variable × value
  - Impact on business: revenue, cost, market share, headcount
  - Financial projection: P&L summary
  - Strategic response: specific actions
  - Trigger indicators: signs you're entering this scenario
- **Comparison Dashboard** — 3 scenarios side-by-side: key metrics × Best/Base/Worst
- **Decision Framework** — "If [trigger], then [action]" rules
- **Review Cadence** — quarterly update assumptions + check triggers

Confirm the structure before generating.

#### File-generation prompt
```
Create a Scenario Planning document.

CONTEXT:
- Company: [Name] — Industry: [industry]
- Key variables: [list 3-5: e.g. market growth, regulation, competition, technology, economy]
- Base-case projections: Revenue [number] | EBITDA [number] | Headcount [number]
- Best-case vision: [describe]
- Worst-case fear: [describe]
- Pivot options: [list]
- Time horizon: [1-3 years]

FORMAT:
- Scenario matrix: variable × Best/Base/Worst values
- 3 scenario narratives: 1-2 pages each, storytelling format
- Financial comparison: 3-column table — Revenue, EBITDA, Cash, Headcount, Market Share
- Trigger dashboard: Indicator | Best trigger | Worst trigger | Current | Trend
- Decision rules: "IF indicator > X THEN activate Plan B"
- Quarterly review checklist: 10 items to re-evaluate

TONE: Strategic foresight — thoughtful, balanced, preparing not predicting.
LENGTH: 10-15 pages.
```

---
✍️ Author: Brian H. Doan
