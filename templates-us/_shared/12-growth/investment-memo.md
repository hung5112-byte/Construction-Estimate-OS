### PROMPT 03: Investment Memo

#### Description
A detailed 8-15 page document for investors — deeper than a pitch deck. Covers the investment thesis, detailed market analysis, competitive landscape, financial analysis, risks & mitigations, and proposed terms. Sent after a pitch deck creates interest. General information only — raising capital is a securities offering; consult a securities attorney.

#### Information to collect (ask the user before generating)
1. A pitch deck already? (the memo builds on it)
2. Target investors? (VC / Angel / PE / Strategic / Institutional)
3. Due-diligence materials ready? (legal, financial, technical)
4. Key risks investors will ask about? (market, execution, regulatory, team)
5. Proposed terms: round size, valuation, instrument (equity/SAFE/convertible note)?

> US securities note: soliciting investment is the offer/sale of a security. Most private raises use a Regulation D exemption (Rule 506(b) or 506(c), 17 CFR §230.506) with a Form D filing and state notice filings. 506(b) prohibits general solicitation; 506(c) allows it but requires verifying accredited-investor status. [verify with a securities attorney]

#### Suggested template
Structure:
- **Executive Summary** — 1 page: thesis, opportunity, ask
- **Company Overview** — history, mission, milestones, current state
- **Market Opportunity** — TAM/SAM/SOM, trends, tailwinds, timing
- **Product & Technology** — product deep-dive, tech stack, IP, moat
- **Business Model & Unit Economics** — how you make money, at what margins
- **Traction & Metrics** — historical performance, cohort analysis, growth
- **Competitive Analysis** — landscape, differentiation, barriers to entry
- **Go-to-Market Strategy** — customer acquisition, channels, partnerships
- **Team & Organization** — leadership bios, org chart, key hires planned
- **Financial Projections** — 3-5 year, key assumptions, path to profitability
- **Risk Factors & Mitigations** — top 10 risks + mitigation strategies
- **Investment Terms** — amount, valuation, structure, use of proceeds, milestones
- **Appendix** — detailed financials, customer list, press, patents

Confirm the structure before generating.

#### File-generation prompt
```
Create an Investment Memo.

CONTEXT:
- Company: [Name] — Stage: [stage] — Raise: [amount] (USD)
- Investor target: [VC / Angel / PE / Strategic]
- Traction: [key metrics]
- Key risks: [top 5]
- Terms: [valuation, instrument]
- Authority: Securities Act of 1933; Reg D Rule 506(b)/(c) + Form D

FORMAT:
- Executive summary: 1 page — Problem | Solution | Market | Traction | Team | Ask — bullets
- Market analysis: TAM/SAM/SOM + market map + trend data + timing argument
- Competitive matrix: feature comparison + positioning + moat analysis
- Unit economics: detailed breakdown with cohort data (USD)
- Financial projections: summary table — Y1-Y5 — Revenue | EBITDA | Cash | Headcount
- Risk matrix: Risk | Probability (H/M/L) | Impact (H/M/L) | Mitigation | Status
- Team bios: Photo | Name | Title | Background | Why this person (2-3 sentences each)
- Use of funds: detailed breakdown — Category | Amount | % | Timeline | Milestone unlocked
- Terms page: Valuation | Instrument | Board seats | Rights | Vesting | Key provisions + securities-exemption note (Reg D)

TONE: Professional, balanced (honest about risks), compelling — investor-grade.
LENGTH: 10-15 pages.

NOTE: General information, not legal/financial advice. The raise must comply with securities law (typically Reg D).
```

---
✍️ Author: Brian H. Doan
