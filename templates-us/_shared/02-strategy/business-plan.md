# PROMPT 10: Business Plan

#### Description
A comprehensive business plan — the most important strategic document, pulling together every dimension: market, product, marketing, operations, finance, people. Used for internal management, fundraising, and bank loans.

#### Information to collect (ask the user before generating)
1. Main purpose: internal / fundraising / bank loan / partner?
2. Time horizon: 1 year / 3 years / 5 years?
3. Market overview: TAM/SAM/SOM (estimate)?
4. Financial projections: ready, or need to create?
5. Go-to-market strategy already in place?
6. Any data from earlier files? (SWOT, BMC, ICP, Competitive)

#### Suggested template
Structure (20-40 pages):
- **Executive Summary** — 2 pages, BLUF, standalone readable
- **Company Overview** — references the Company Profile
- **Market Analysis** — TAM/SAM/SOM, trends, customer segments
- **Products & Services** — description, roadmap, USP
- **Competitive Analysis** — references the Competitive Landscape
- **Marketing & Sales Strategy** — go-to-market, pricing, channels, customer acquisition
- **Operations Plan** — processes, supply chain, technology
- **Management Team** — key people, org chart, hiring plan
- **Financial Plan** — 3-5 year P&L, cash flow, break-even, funding requirements
- **Risk Analysis** — top 5 risks + mitigation
- **Milestones & Timeline** — key milestones, Gantt chart
- **Appendix** — financial model detail, market research data, key-people resumes

Confirm the structure before generating.

#### File-generation prompt
```
Create a Business Plan.

CONTEXT:
- Company: [Name] — Industry: [industry] — Stage: [startup/growth/mature]
- Purpose: [internal / fundraising / loan / partner]
- Time horizon: [1/3/5 years]
- Market: TAM [number] | SAM [number] | SOM [number]
- Financial data: [ready / need to create projection]
- Data from earlier files: [list files created in 02-strategy]

FORMAT:
- Executive Summary: 2 pages, standalone, highlight key numbers
- Each section: Key insight → Supporting data → Implications → Actions
- Financial tables: P&L, Cash Flow, Balance Sheet — 3 scenarios (Base/Optimistic/Conservative)
- Visuals: market-size pie chart, growth-projection line chart, org chart, timeline Gantt
- Cross-reference: link to detailed files (SWOT, BMC, ICP, Competitive)
- Appendix: detailed financial-model assumptions

TONE: Professional, persuasive (if fundraising), evidence-based.
LENGTH: 20-40 pages.
```

---
✍️ Author: Brian H. Doan
