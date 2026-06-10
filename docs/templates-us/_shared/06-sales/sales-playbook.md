### PROMPT 11: Sales Playbook

#### Description
A consolidated sales playbook — the "bible" for the sales team. Includes detailed buyer personas, competitive battlecards, value proposition, qualification criteria, and everything a rep needs to sell effectively. Every new rep must read it before they start.

#### Information to collect (ask the user before generating)
1. Products/services: short description, USP, price?
2. Buyer personas: how many main personas? Describe each?
3. Top 3-5 competitors? Strengths/weaknesses vs. you?
4. Value proposition: why should the customer choose you?
5. Qualification criteria: the ideal customer's criteria?
6. Average sales cycle?
7. Current win rate? Top win/lose reasons?

#### Suggested template
Structure:
- **Part 1** — Company & product overview: mission, USP, product portfolio
- **Part 2** — Ideal Customer Profile (ICP): industry, size, pain points, buying signals
- **Part 3** — Buyer personas: 2-4 detailed persona cards
- **Part 4** — Value Proposition Canvas: pains, gains, jobs-to-be-done → our solution
- **Part 5** — Competitive battlecards: per competitor — overview, strengths, weaknesses, how to win
- **Part 6** — Qualification criteria: BANT/MEDDIC scorecard
- **Part 7** — Sales messaging: elevator pitch, email templates, LinkedIn outreach
- **Part 8** — Win/Loss analysis: top reasons, patterns, lessons
- **Part 9** — FAQ: top 20 customer questions + answers
- **Appendix**: product cheat sheet, price card, case-study summaries

Confirm the structure before generating.

#### File-generation prompt
```
Create a Sales Playbook.

CONTEXT:
- Company: [Name] — Products/services: [list + USP]
- Personas: [number] — Description: [each persona]
- Competitors: [top 3-5 + strengths/weaknesses]
- Value prop: [why choose you]
- Qualification: [BANT / MEDDIC / Custom]
- Win rate: [%] — Top win reasons: [3] — Top lose reasons: [3]
- Sales cycle: [days]

FORMAT:
- ICP card: Industry | Size | Revenue | Pain Points | Buying Signals | Decision Makers
- Persona cards: 2-4 cards — photo placeholder, demographics, goals, pains, objections, preferred channels
- Value Prop Canvas: table Customer Jobs | Pains | Gains → Our Products | Pain Relievers | Gain Creators
- Battlecards per competitor: 1 page/competitor — Overview | They say | We say | When they win | How we win
- Qualification scorecard: table criterion | weight | score 1-5 | verdict (Go/No-go)
- Messaging library: elevator pitch (30s/60s) + email (cold/warm/follow-up) + LinkedIn message
- FAQ: 20 Q&A pairs, grouped by topic
- Win/Loss: table Reason | Win % | Lose % | Action

TONE: Sales enablement — energizing, practical, reference-worthy.
LENGTH: 12-18 pages.
```

---
✍️ Author: Brian H. Doan
