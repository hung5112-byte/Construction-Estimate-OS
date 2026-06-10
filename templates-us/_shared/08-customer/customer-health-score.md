### PROMPT 10: Customer Health Score

#### Description
A template to measure the "health" of the customer relationship — scoring dimensions (usage, engagement, support, payment, NPS), weights, the formula, warning thresholds, and actions per score level. A proactive tool to spot at-risk customers before it's too late.

#### Information to collect (ask the user before generating)
1. What data do you have? (usage logs, login frequency, support tickets, payment history, NPS)
2. The earliest signal of an at-risk customer?
3. A CRM/CS platform that can track the health score?
4. How many customers to monitor? Score update frequency?
5. Who acts when the health score drops?

#### Suggested template
Structure:
- **Scoring Dimensions**: Usage (30%) | Engagement (20%) | Support (20%) | Payment (15%) | NPS/Feedback (15%)
- **Sub-metrics per dimension**: 3-5 metrics each, scored 1-10
- **Calculation**: weighted average → score 0-100
- **Thresholds**: Green (≥70) — Healthy | Yellow (50-69) — At Risk | Red (<50) — Critical
- **Actions per range**: Green → nurture/upsell | Yellow → proactive outreach | Red → save-team intervention

Confirm the structure before generating.

#### File-generation prompt
```
Create a Customer Health Score Template.

CONTEXT:
- Company: [Name] — Data available: [usage / engagement / support / payment / NPS]
- Churn signals: [describe]
- Platform: [CRM / CS tool / manual]
- # customers monitored: [number] — Update frequency: [daily / weekly / monthly]
- Action owner: [CS Manager / CSM / auto-alert]

FORMAT:
- Scoring model: table Dimension | Weight | Sub-metrics | Scoring rule (1-10) | Data source | Update freq
- Calculation example: walk through one specific customer — input → weighted score → final score
- Threshold matrix: Score range | Status | Color | Description | Required action | Timeline | Owner
- Dashboard view: Customer | Score | Trend (↑↓→) | Status | Last contact | Next action | CSM
- Alert system: auto-trigger when score drops ≥15 points/month or falls to Red
- Cohort analysis: score distribution per tier | average score by segment | trend over time
- Playbook per status: Green (3 actions) | Yellow (5 actions) | Red (7 actions) — scripts + offers

TONE: Analytical, proactive, early-warning focused.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
