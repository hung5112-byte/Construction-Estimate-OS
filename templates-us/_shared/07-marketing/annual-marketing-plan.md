### PROMPT 01: Annual Marketing Plan

#### Description
A full-year marketing plan — marketing goals, target-audience analysis, brand positioning, channel strategy, budget allocation, KPIs, and a quarterly rollout timeline. The "battle map" the whole marketing team aligns and executes against.

#### Information to collect (ask the user before generating)
1. This year's business goals? (revenue, growth %, market share?)
2. Main target audience? (B2B/B2C, demographics, psychographics, pain points?)
3. Marketing channels in use? (Online: Facebook, Google, SEO, Email. Offline: events, PR, print?)
4. Annual marketing budget? (% of revenue or a specific number?)
5. Main competitors? (3-5 competitors and their current positioning?)
6. USP / core differentiator?

#### Suggested template
Structure:
- **Executive Summary**: a 1-page summary — goals, key strategy, budget, KPIs
- **Situation Analysis**: marketing SWOT, market overview, competitive landscape
- **Target Audience**: persona(s), customer segments, demographics + psychographics
- **Positioning & Messaging**: brand-positioning statement, key messages, tone of voice
- **Channel Strategy**: matrix channel × objective × budget × KPIs
- **Campaign Calendar**: Q1-Q4 timeline — main campaigns, seasonal events, launches
- **Budget Allocation**: by channel, by quarter, contingency fund
- **KPIs & Measurement**: table KPI × Target × Frequency × Measurement tool

Confirm the structure before generating.

#### File-generation prompt
```
Create an Annual Marketing Plan.

CONTEXT:
- Company: [Name] — Industry: [industry] — Revenue target: [amount]
- Target audience: [B2B/B2C] — Persona: [describe]
- Current channels: [list]
- Marketing budget: [amount / % of revenue]
- Main competitors: [3-5 names]
- USP: [differentiator]

FORMAT:
- Executive summary: 1 page — BLUF, 5 key bullet points
- Marketing SWOT: 2×2 matrix + SO/ST/WO/WT strategies
- Persona cards: 2-3 personas — Name | Age | Job | Pain points | Goals | Preferred channels
- Channel matrix: table Channel | Objective | Budget | KPI | Owner | Priority (USD)
- Campaign calendar: Gantt-style Q1-Q4 — Campaign | Channel | Budget | Timeline | KPI
- Budget breakdown: pie chart placeholder — Online [%] | Offline [%] | Content [%] | Tools [%] | Contingency [%]
- KPI dashboard: table KPI | Target Q1 | Q2 | Q3 | Q4 | YTD | Measurement tool

TONE: Executive, strategic, actionable.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
