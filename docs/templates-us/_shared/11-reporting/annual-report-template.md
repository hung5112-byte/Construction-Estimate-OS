### PROMPT 10: Annual Report Template

#### Description
A consolidated annual report — for shareholders, partners, banks, and media. Summarizes the year: mission, strategy, financial results, business operations, people, CSR, and next-year plan.

#### Information to collect (ask the user before generating)
1. Public or private company? (disclosure rules differ — a public company has SEC reporting obligations)
2. Main audience: shareholders / bank / partners / media / internal?
3. Include a CSR/ESG section?
4. Independent audit?
5. Format: document / designed PDF / web / presentation?
6. Main message to convey? (growth / stability / transformation / expansion)

#### Suggested template
Structure:
- **Cover** — company name, year, tagline, visual
- **Letter from the Chairman/Department Head** — 1-2 pages: vision, highlights, thanks
- **Company intro** — mission, vision, values, history, milestones
- **Market overview** — economic context, industry, opportunities, challenges
- **Business results** — revenue, profit, market share, customers, products
- **Financial statements** — P&L, Balance Sheet, Cash Flow + notes
- **People** — team growth, culture, development, diversity
- **Social responsibility** — CSR, ESG, community, environment
- **Strategy & plan** — next year, 3-5 year vision
- **Appendix**: corporate governance, org chart, glossary

Confirm the structure before generating.

#### File-generation prompt
```
Create an Annual Report Template.

CONTEXT:
- Company: [Name] — Public/Private: [type]
- Reporting year: [year]
- Audience: [shareholders / bank / partners / media]
- CSR/ESG: [Yes/No]
- Audit: [Yes/No] — Firm: [name]
- Message: [growth / stability / transformation]
- Format: [document / designed PDF / web]

FORMAT:
- Cover page: Company name | "Annual Report [Year]" | Visual/Image | Tagline
- Table of Contents: hyperlinked sections
- Chairman/Department Head letter (1-2 pages):
  - Opening: context of the past year
  - Highlights: 5-7 standout achievements
  - Challenges: difficulties and how they were overcome
  - Gratitude: thanks to shareholders, team, customers, partners
  - Outlook: direction for next year
- Company intro (2-3 pages):
  - At a glance: infographic — Founded | Revenue | Employees | Customers | Locations | Products
  - Mission, Vision, Core Values
  - Milestone timeline: key events since founding
- Market overview (1-2 pages):
  - GDP, industry growth, trends
  - Market size, company market share
  - Competitive landscape
  - Opportunities & threats
- Business results (3-5 pages):
  - Key metrics: Revenue | Growth % | Market share | New customers | Retention rate (USD)
  - Revenue breakdown: by product/segment/region — chart + table
  - Customer highlights: case studies, testimonials, key wins
  - Product/service developments: launches, improvements, awards
- Financial statements (3-5 pages):
  - Financial highlights: 5-year summary — Revenue | EBITDA | Net Income | Total Assets | Equity
  - P&L | Balance Sheet | Cash Flow — comparative 2 years (US GAAP)
  - Key ratios: profitability | liquidity | leverage
  - Auditor's report summary (if applicable)
- People & culture (1-2 pages):
  - Headcount: growth | breakdown by dept/level
  - Training: hours | programs | investment
  - Engagement: score | highlights
  - Culture initiatives: events, awards, recognition
- CSR/ESG (1-2 pages, if applicable):
  - Environmental: carbon footprint, green initiatives
  - Social: community programs, donations, volunteer hours
  - Governance: board composition, ethics, transparency
- Strategy & plan (1-2 pages):
  - Strategic priorities for next year: 3-5 pillars
  - Investment plans: capex, R&D, market expansion
  - 3-5 year vision: where we're heading
- Corporate Governance: board members, committees, meeting attendance, remuneration
- Appendix: org chart, glossary, contact information

TONE: Professional, inspirational, transparent — balance achievements with honesty.
LENGTH: 20-30 pages.
```

---
✍️ Author: Brian H. Doan
