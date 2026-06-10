### PROMPT 01: Pitch Deck (Fundraising Slide Deck)

#### Description
A 12-15 slide fundraising deck — story-driven, data-backed. Follows the standard VC format: Problem → Solution → Market → Product → Traction → Business Model → Competition → Team → Financials → Ask. The single most important "weapon" in fundraising.

#### Information to collect (ask the user before generating)
1. Funding stage? (Pre-seed / Seed / Series A / Series B+)
2. Amount to raise? Expected valuation?
3. Current traction? (revenue, users, growth rate, key milestones)
4. TAM/SAM/SOM? Market data?
5. Team highlights? (founder background, key hires)
6. Competitive landscape? Moat/USP?
7. Use of funds? Current runway?

#### Suggested template
Structure — 15 slides:
- **Slide 1** — Cover: logo, tagline, round info
- **Slide 2** — Problem: clear pain point, data-backed
- **Slide 3** — Solution: how you solve it, the "aha" moment
- **Slide 4** — Product: demo/screenshots, key features
- **Slide 5** — Market size: TAM → SAM → SOM with sources
- **Slide 6** — Business model: revenue model, unit economics
- **Slide 7** — Traction: hockey-stick metrics, key milestones
- **Slide 8** — Customer/case study: social proof, testimonials
- **Slide 9** — Competition: 2×2 matrix or feature comparison (position top-right)
- **Slide 10** — Go-to-market: growth strategy, channels, partnerships
- **Slide 11** — Team: founders + key hires + advisors, relevant experience
- **Slide 12** — Financials: 3-5 year revenue projection, key assumptions
- **Slide 13** — Use of funds: pie chart — how the money will be spent
- **Slide 14** — The ask: amount, instrument, timeline, milestones
- **Slide 15** — Contact/appendix

Confirm the structure before generating.

#### File-generation prompt
```
Create Pitch Deck content (text + slide structure).

CONTEXT:
- Company: [Name] — Industry: [industry] — Stage: [Pre-seed/Seed/A/B]
- Raise: [amount] — Valuation: [pre-money] (USD)
- Traction: [revenue/users/growth]
- TAM: [number] — SAM: [number] — SOM: [number]
- Team: [founders + key hires]
- Moat: [competitive advantage]
- Use of funds: [breakdown]

FORMAT:
- 15 slides — each slide: Title | Key message (1 sentence) | Content outline | Data/visuals needed
- Slide 2 (Problem): statistic + story — "X% of [market] struggles with [problem]"
- Slide 5 (Market): TAM/SAM/SOM nested circles + sources
- Slide 7 (Traction): chart data — MoM or QoQ growth trajectory
- Slide 9 (Competition): 2×2 positioning matrix — axes labeled
- Slide 12 (Financials): revenue table — Year 1-5, Revenue, COGS, GP, EBITDA, headcount
- Slide 13 (Use of Funds): pie chart — Product X% | Sales X% | Marketing X% | Ops X% | Buffer X%
- Design notes per slide: color palette, font, visual style
- Speaker notes: 30-second talking points per slide

TONE: Confident, data-driven, story-first — inspire but don't oversell.
LENGTH: 15 slides content + speaker notes (8-12 pages text).

NOTE: A fundraise is a securities offering — keep claims accurate and consult a securities attorney on the offering structure (Reg D).
```

---
✍️ Author: Brian H. Doan
