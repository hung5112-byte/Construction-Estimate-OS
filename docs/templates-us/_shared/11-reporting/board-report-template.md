### PROMPT 07: Board Report Template

#### Description
A report template for the Board of Directors / Advisory Board — a strategic-level summary of the business, covering financial performance, strategic progress, key risks, and decisions needing Board approval. Concise, strategic, focused on governance and oversight.

#### Information to collect (ask the user before generating)
1. Board structure? (# members, independent directors, committees)
2. Board meeting frequency? (quarterly / semi-annual / annual)
3. Board's main interest: financial performance / strategy / risk / compliance / ESG?
4. Any board committees? (Audit / Compensation / Nomination / Risk)
5. Which decisions need Board approval? (investment > X / hiring C-level / M&A)
6. Current format? Presentation length?

#### Suggested template
Structure:
- **Cover Page** — meeting details, agenda, attendance
- **CEO Report** — 1-2 pages: strategic highlights, key achievements, challenges
- **Financial Summary** — 1 page: P&L, balance-sheet highlights, cash position, forecast
- **Strategic Initiatives Update** — progress vs. plan, milestones, pivots
- **Risk Dashboard** — top 5 risks, status changes, new risks, mitigation progress
- **Compliance & Governance** — regulatory updates, audit findings, compliance status
- **Decisions Required** — clear ask: What, Why, Options, Recommendation
- **Appendix** — detailed financials, committee reports

Confirm the structure before generating.

#### File-generation prompt
```
Create a Board Report Template.

CONTEXT:
- Company: [Name] — Board: [# members] — Meeting frequency: [quarterly / semi-annual]
- Committees: [Audit / Compensation / Risk / None]
- Focus: [financial / strategy / risk / compliance / ESG]
- Approval thresholds: [investment > X / C-level hiring / M&A]
- Length: [X min presentation + X min Q&A]

FORMAT:
- Cover page: Company name | Board Meeting # | Date | Location | Time | Quorum status
- Agenda: # | Item | Presenter | Time | Type (Information/Discussion/Decision)
- CEO Report (1-2 pages):
  - Period highlights: 3-5 bullets — standout results
  - Strategic scorecard: Initiative | Status (🟢🟡🔴) | Commentary | Next milestone
  - Market & competitive update: key trends, competitive moves, market position
  - Outlook: next-quarter priorities, opportunities, concerns
- Financial Summary (1 page):
  - Key metrics: Revenue | EBITDA | Net Income | Cash — Actual vs. Budget vs. YoY (USD)
  - P&L waterfall: Revenue → Gross Profit → EBITDA → Net Income — highlight variances
  - Cash position: runway, burn rate, upcoming major payments
  - Forecast: revised full-year estimate vs. original budget
- Risk Dashboard:
  - Top 5 risks: Risk | Category | Likelihood | Impact | Trend (↑↓→) | Mitigation | Owner
  - New risks since last meeting
  - Closed/downgraded risks
  - Risk heat map: 5×5 matrix — Likelihood × Impact
- Compliance section:
  - Regulatory update: New regulations | Impact | Action taken | Status
  - Audit findings: Finding | Severity | Remediation | Due date | Status
  - Litigation: Case | Status | Exposure | Counsel recommendation
- Decisions Required:
  - For each decision: Background (2-3 sentences) | Options (2-3) | Recommendation | Financial impact | Risk
  - Resolution template: "RESOLVED, that the Board hereby approves..."
- Committee Reports (if applicable): 1-paragraph summary per committee
- Minutes template: Attendees | Decisions | Action items | Next meeting

TONE: Board-level, concise, decision-focused, governance-oriented.
LENGTH: 6-10 pages (excl. appendix).
```

---
✍️ Author: Brian H. Doan
