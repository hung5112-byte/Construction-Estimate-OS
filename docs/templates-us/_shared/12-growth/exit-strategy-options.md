### PROMPT 10: Exit Strategy Options

#### Description
A document analyzing exit options for the founder/shareholders — IPO, M&A, MBO, succession, liquidation. Each option is assessed on feasibility, timeline, valuation impact, and readiness. Gives the founder a "map" for the endgame. General information only — confirm tax consequences with a CPA and deal terms with an attorney.

#### Information to collect (ask the user before generating)
1. Desired exit timeline? (3 years / 5 years / 10 years / unclear)
2. Exit goal? (maximize value / retire / pursue a new venture / health/personal)
3. The business now: profitable? Scalable? Has IP?
4. Do shareholders share the exit view?
5. Any potential acquirer / strategic partner?
6. A succession plan already?

#### Suggested template
Structure:
- **Part 1** — Why exit planning matters: stats, why to plan early
- **Part 2** — Exit readiness assessment: 20-item checklist — Financial | Legal | Operational | Team
- **Part 3** — Option 1: IPO — requirements (SEC registration), timeline, costs, pros/cons, readiness gap
- **Part 4** — Option 2: M&A (trade sale) — process, valuation multiples, buyer types, negotiation
- **Part 5** — Option 3: MBO (management buyout) — structure, financing, transition
- **Part 6** — Option 4: family/succession — transfer to next generation, governance
- **Part 7** — Option 5: liquidation — when appropriate, process, tax implications
- **Part 8** — Comparison matrix: all options × criteria → recommendation
- **Part 9** — Exit-preparation roadmap: 3-5 year prep plan
- **Appendix**: exit-readiness scorecard, valuation checklist, due-diligence prep list

Confirm the structure before generating.

#### File-generation prompt
```
Create an Exit Strategy Options document.

CONTEXT:
- Company: [Name] — Revenue: [amount] — Profit: [amount] — Growth: [%] (USD)
- Timeline: [3/5/10 years]
- Goal: [maximize value / retire / new venture]
- Profitable: [Yes/No] — IP: [Yes/No] — Scalable: [Yes/No]
- Potential acquirers: [list or "not yet identified"]

FORMAT:
- Exit-readiness scorecard: 20 items ☐ — Category | Item | Ready | Gap | Action needed → Total score /100
- Per exit option: 1 page each — Description | Requirements | Timeline | Costs | Valuation impact | Pros | Cons | Readiness gap
- Comparison matrix: Option | Valuation multiplier | Timeline | Founder control | Tax efficiency | Feasibility | Score → Rank
- IPO readiness: 30-item checklist — Governance | Financial | Legal | IR | Audit (SEC registration)
- M&A process: flowchart — Preparation → Marketing → LOI → Due Diligence → Negotiation → Close → Integration
- Preparation roadmap: Gantt — Year 1-5 × workstreams (financial cleanup, legal, operations, team, market position)
- Value drivers: table Driver | Current state | Target state | Impact on valuation | Action
- Tax consideration: per option — summary of US tax implications (federal capital gains tax, IRC; possible QSBS §1202 exclusion for qualifying C-corp stock; no Texas personal income tax) — confirm with a CPA [verify]

TONE: Strategic, long-term, wealth-planning oriented.
LENGTH: 8-12 pages.

NOTE: General information, not legal/tax advice. Confirm tax with a CPA and deal terms with an attorney.
```

---
✍️ Author: Brian H. Doan
