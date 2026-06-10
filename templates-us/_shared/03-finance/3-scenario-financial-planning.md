# P-FIN-08: 3-Scenario Financial Planning

#### Description
A financial analysis across 3 scenarios: Best Case (optimistic), Base Case (realistic), Worst Case (pessimistic). Each scenario has its own assumptions, projected P&L, cashflow impact, and a specific action plan.

#### Information to collect (ask the user before generating)
1. Key variables driving revenue? (e.g. new customers, price, conversion rate)
2. Key variables driving costs? (e.g. material cost, payroll, rent)
3. Biggest current risk? (market, competitor, legal, staffing)
4. Have you ever hit the worst case? How did it play out?
5. KPI trigger: when do you switch from the Base to the Worst-case plan?

#### Suggested template
Structure:
- **Executive Summary** — 3 scenarios summarized in one table
- **Assumptions Matrix** — variables × 3 scenarios
- **Best Case** — assumptions, P&L, cashflow, headcount, investment
- **Base Case** — assumptions, P&L, cashflow, headcount, investment
- **Worst Case** — assumptions, P&L, cashflow, headcount, cost-cutting plan
- **Trigger Points** — which KPI → switch scenario
- **Action Plan per Scenario** — a specific action table
- **Dashboard** — compare all 3 scenarios on one page

Confirm the structure before generating.

#### File-generation prompt
```
Create a 3-scenario financial plan.

CONTEXT:
- Company: [Name] — Current revenue: [amount/year]
- Revenue variables: [list + range]
- Cost variables: [list + range]
- Key risks: [list]
- Forecast horizon: [12 months / 3 years]

FORMAT:
- Comparison table: KPI | Best | Base | Worst — for 10+ KPIs
- Assumptions matrix: variable | Best | Base | Worst + Probability %
- Mini P&L per scenario: Revenue → COGS → GP → SG&A → EBITDA → NI
- Cashflow summary per scenario: 12 months × 3 scenarios
- Trigger dashboard: table KPI | Threshold Best→Base | Threshold Base→Worst | Current
- Action cards: 5-7 specific actions per scenario
- Waterfall: revenue-difference breakdown Best vs. Worst

TONE: Strategic, analytical, decision-oriented.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
