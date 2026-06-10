### PROMPT 12: Sales Pipeline Tracker

#### Description
A sales-pipeline tracking template — tracking each deal through the stages, value, close probability, revenue forecast, and conversion rates. A daily tool for the sales manager and a weekly report for leadership.

#### Information to collect (ask the user before generating)
1. Pipeline stages? (e.g. Lead → Qualified → Proposal → Negotiation → Closed Won/Lost)
2. Default probability per stage? (e.g. Lead 10%, Qualified 25%, Proposal 50%...)
3. Average deal value?
4. Average # deals in the pipeline?
5. Pipeline-review frequency? (daily / weekly)
6. Need a forecast? (monthly / quarterly / annual)
7. Track by rep / team / channel?

#### Suggested template
Structure:
- **Pipeline View**: Deal | Company | Contact | Value | Stage | Probability | Weighted | Age | Next Action | Owner | Close Date
- **Stage Summary**: table Stage | # Deals | Total Value | Weighted Value | Avg Age | Conversion %
- **Forecast View**: monthly / quarterly — Commit | Upside | Pipeline | Target | Gap
- **Rep Scorecard**: per rep — pipeline value | # deals | win rate | avg deal size | activity metrics
- **Conversion Funnel**: stage-to-stage conversion + trend
- **Stale Deals Alert**: deals > X days without moving stage
- **Weekly Review Template**: agenda + dashboard + action items

Confirm the structure before generating.

#### File-generation prompt
```
Create a Sales Pipeline Tracker.

CONTEXT:
- Company: [Name] — Stages: [list + probability %]
- Avg deal size: [amount] — Avg deals in pipeline: [number]
- Sales cycle: [days] — Review: [daily / weekly]
- Team size: [# reps] — Tracking: [per rep / team / channel]
- Forecast: [monthly / quarterly / annual]

FORMAT:
- Pipeline table: 12+ columns — Deal | Company | Value | Stage | Prob | Weighted | Age | Next Action | Owner | Close Date | Source | Notes (USD)
- Stage summary: table Stage | # Deals | $ Value | $ Weighted | Avg Age | Conv % → chart data
- Forecast: table Month | Commit | Best Case | Pipeline | Target | Gap | Gap %
- Rep scorecard: table Rep | Pipeline $ | # Deals | Win Rate | Avg Deal | Activities | Quota %
- Conversion waterfall: Lead → MQL → SQL → Proposal → Won — % each step
- Stale alert: rules — IF stage_age > [X days] THEN flag 🔴
- Weekly review template: 5 sections — Wins | Lost | Moved | Stuck | Actions

TONE: Operational — tracking, analytical, action-oriented.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
