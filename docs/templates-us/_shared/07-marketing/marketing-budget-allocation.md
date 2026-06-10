### PROMPT 05: Marketing Budget Allocation

#### Description
A marketing-budget allocation document — split by channel, by campaign, by quarter. Includes ROI benchmarks per channel, triggers to reallocate budget, and the marketing-spend approval process.

#### Information to collect (ask the user before generating)
1. Total annual marketing budget? (USD or % of revenue?)
2. Current allocation? (% to online vs. offline vs. tools?)
3. Which channel gives the best ROI? Which is worst?
4. Any seasonal peaks? (Black Friday, Cyber Monday, holidays, back-to-school, industry peak season?)
5. Spend-approval process? (< $X: Marketing Manager | > $X: CMO | > $Y: CEO?)
6. A contingency fund? (% reserve?)

#### Suggested template
Structure:
- **Budget Overview**: total budget, % of revenue, YoY comparison
- **Channel Allocation**: breakdown by channel — paid, organic, content, tools, events, headcount
- **Campaign Budget**: breakdown by major campaign for the year
- **Quarterly Breakdown**: Q1-Q4 allocation by season
- **ROI Benchmarks**: target ROI/ROAS per channel
- **Reallocation Triggers**: conditions to move budget between channels
- **Approval Process**: spend-approval workflow by limit

Confirm the structure before generating.

#### File-generation prompt
```
Create a Marketing Budget Allocation.

CONTEXT:
- Company: [Name] — Total marketing budget: [$ / % of revenue]
- Current allocation: Online [%] | Offline [%] | Tools [%]
- Best-ROI channel: [channel] — Worst-ROI channel: [channel]
- Seasonal peaks: [list months/events — e.g. Black Friday, holidays]
- Approval: < $[X] (Marketing Manager) | > $[X] (CMO) | > $[Y] (CEO)
- Contingency: [%]

FORMAT:
- Budget summary: 1-page table — Total | Online | Offline | Content | Tools | Events | Contingency (USD)
- Channel breakdown: table Channel | Budget Q1 | Q2 | Q3 | Q4 | Total | % | Target ROI
- Campaign budget: table Campaign | Timing | Budget | Channels | Expected ROI | Owner
- Monthly cash flow: table Month × Channel — planned spend
- ROI benchmarks: table Channel | Industry Avg ROI | Our Target | Min Acceptable | Action if Below
- Reallocation rules: decision tree — Performance < X% → Review → Reallocate → To where
- Approval matrix: Value | Approver | Timeline | Documentation needed

TONE: Financial, data-driven, ROI-focused.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
