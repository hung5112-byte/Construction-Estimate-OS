### PROMPT 01: Sales Strategy & Target

#### Description
The top-level sales strategy document. Defines the revenue target, priority market segments, key sales channels, and measurement KPIs. The "north star" that aligns the whole sales team's actions with company goals.

#### Information to collect (ask the user before generating)
1. Annual revenue target? (total + quarterly/monthly breakdown)
2. Target market segments? (B2B / B2C / B2B2C? Which industry? Customer size?)
3. Best-selling products/services now? Top 3 by revenue?
4. Current sales channels? (direct sales, inside sales, online, agents, affiliate?)
5. Current sales team: how many? Split by channel/region?
6. Sales KPIs tracked? (revenue, deals, conversion rate, average deal size?)
7. Main competitors? Your differentiation?
8. Biggest current sales challenge?

#### Suggested template
Structure:
- **Part 1** — Strategy overview: sales vision, 1-3 year goals, North Star Metric
- **Part 2** — Market analysis: TAM/SAM/SOM, priority segments, buyer persona
- **Part 3** — Revenue targets: total → by product → by channel → by region × 12 months
- **Part 4** — Channel strategy: which channels to prioritize, resource allocation, target per channel
- **Part 5** — Go-to-Market: approach per segment, messaging, positioning
- **Part 6** — Sales-team org: structure, roles & responsibilities, territory mapping
- **Part 7** — KPIs & scorecard: leading + lagging indicators + weekly scorecard
- **Part 8** — Action plan: first 90 days, quarterly milestones
- **Appendix**: competitive landscape, quota-allocation template, territory map

Confirm the structure before generating.

#### File-generation prompt
```
Create a Sales Strategy & Target.

CONTEXT:
- Company: [Name] — Industry: [industry] — Current revenue: [amount/year]
- Revenue target: [amount/year] — Growth: [%]
- Segments: [B2B / B2C / B2B2C] — Target customer: [describe]
- Main products/services: [top 3 + % revenue]
- Channels: [direct / inside sales / online / agents / affiliate]
- Sales team: [headcount] — Split: [by channel / region]
- Competitors: [top 3]

FORMAT:
- Targets: table Total | Per product | Per channel | Per region × Q1-Q4 (USD)
- TAM/SAM/SOM: funnel-chart data + estimates
- Buyer persona: 2-3 persona cards (demographics, pain points, decision process, channels)
- Channel priority matrix: Channel | Revenue target | CAC | LTV | Priority | Resource %
- Scorecard: table KPI | Target | Weekly pace | Owner | Status
- 90-day action plan: Week 1-4 | Week 5-8 | Week 9-12 — specific milestones
- Territory map: Region/Segment × Sales Rep × Quota

TONE: Strategic, executive-level, action-oriented.
LENGTH: 8-12 pages.
```

---
✍️ Author: Brian H. Doan
