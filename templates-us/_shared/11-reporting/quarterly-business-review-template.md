### PROMPT 08: Quarterly Business Review Template

#### Description
A Quarterly Business Review (QBR) template — a comprehensive quarterly performance review, comparing actual vs. plan, analyzing causes, capturing lessons, and adjusting the next quarter's plan. The QBR is the most important "course correction" mechanism, combining backward-looking (review) with forward-looking (planning).

#### Information to collect (ask the user before generating)
1. Who attends the QBR? (leadership only / + department heads / whole company)
2. QBR length? (half-day / full-day / 2 hours)
3. Each department presents separately, or just a roll-up?
4. Scoring/rating per objective?
5. OKR system: OKR or KPI-based?
6. QBR output: action plan / updated forecast / revised priorities?

#### Suggested template
Structure:
- **Part 1** — Quarter summary: headline results, key achievements, key misses
- **Part 2** — Financial review: revenue, P&L, cash flow vs. plan + variance analysis
- **Part 3** — OKR/KPI scorecard: Objective × Key Result → score + commentary
- **Part 4** — Department reviews: each dept 1-2 pages — wins, misses, lessons, asks
- **Part 5** — Customer & market: NPS, churn, market trends, competitive moves
- **Part 6** — Lessons learned: Start / Stop / Continue
- **Part 7** — Next-quarter plan: priorities, OKRs, resource needs, risks
- **Appendix**: detailed department data, customer-feedback summary

Confirm the structure before generating.

#### File-generation prompt
```
Create a Quarterly Business Review Template (QBR).

CONTEXT:
- Company: [Name] — QBR participants: [leadership / + dept heads / whole company]
- Length: [X hours] — Format: [presentation / workshop / hybrid]
- OKR/KPI system: [OKR / KPI / hybrid]
- Dept presentations: [Yes/No]
- Output: [action plan / updated forecast / revised priorities]

FORMAT:
- Quarter headline: 1 slide — Q[X] [Year] | Revenue: [actual vs target] | Key metric 1-3 | Overall rating (🟢🟡🔴)
- Financial review:
  - Revenue: Actual | Target | % | vs Prior Q | vs YoY — by product/segment (USD)
  - P&L: Revenue → Gross Profit → EBITDA → Net Income — variance waterfall
  - Cash flow: Opening → Operating → Investing → Financing → Closing
  - Unit economics: CAC | CLV | LTV:CAC | Payback period — trend
- OKR/KPI Scorecard:
  - Company OKRs: Objective | KR1 score | KR2 score | KR3 score | Overall | Commentary
  - Scoring: 0-0.3 (🔴 Miss) | 0.4-0.6 (🟡 Progress) | 0.7-1.0 (🟢 Achieved)
  - Quarter-over-quarter trend per OKR
- Department review template (per dept):
  - Dept KPIs: 5-8 metrics — Actual vs. Target | Status
  - Top 3 wins: What | Impact | Replicable?
  - Top 3 misses: What | Root cause | Action
  - Resource needs: Ask | Justification | Priority
- Customer & Market:
  - NPS/CSAT trend: Score | Trend | Top feedback themes
  - Churn analysis: Rate | Revenue impact | Reasons | Save rate
  - Market intel: competitive moves | industry trends | regulatory changes
- Lessons Learned:
  - Start doing: Activity | Expected impact | Owner
  - Stop doing: Activity | Why | Alternative
  - Continue doing: Activity | Why working | How to amplify
- Next Quarter Plan:
  - Updated OKRs/priorities: Objective | Key Results | Owner | Dependencies
  - Resource allocation: Dept | Headcount | Budget | Key initiatives
  - Risk register: Risk | Probability | Impact | Mitigation | Owner
  - Key dates/milestones: Date | Event | Owner | Dependencies

TONE: Strategic, honest (celebrate wins AND confront misses), action-oriented.
LENGTH: 10-15 pages.
```

---
✍️ Author: Brian H. Doan
