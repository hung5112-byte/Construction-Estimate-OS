# PROMPT 15: Risk Register

#### Description
A strategic risk register — a consolidated catalog to assess and track all company-level risks. Unlike the Risk Management Policy (01-governance), which is the framework/policy, this is the ACTUAL table listing specific risks.

#### Information to collect (ask the user before generating)
1. Do you already have a risk list from the Risk Management Policy?
2. Top 5 risks the company worries about most?
3. Who will be the Risk Owner for each risk?
4. Review frequency: monthly / quarterly?
5. Any KRIs (Key Risk Indicators) already tracked?

#### Suggested template
Structure:
- **Risk Register Table**: ID | Category | Description | Likelihood (1-5) | Impact (1-5) | Score | Strategy | Mitigation Actions | Owner | KRI | Status | Last Review
- **Heat Map Data**: a 5×5 grid with the number of risks per cell
- **Top 10 Risks**: card format — detailed analysis for the top 10
- **KRI Dashboard**: Metric | Threshold | Current | Trend (↑↓→)
- **Review Log**: Date | Reviewed by | Changes | New risks | Closed risks

Confirm the structure before generating.

#### File-generation prompt
```
Create a Risk Register.

CONTEXT:
- Company: [Name] — Industry: [industry]
- Risk categories: [Strategy / Finance / Operations / Compliance / Reputation / Technology]
- Top 5 risks: [list]
- Risk Owners: [mapping]
- Review frequency: [monthly/quarterly]
- Existing KRIs: [list or "none"]

FORMAT:
- Main table: full register with all columns (12+ columns)
- Heat Map: 5×5 data grid, color-coded
- Top 10 Risk Cards: each risk = half a page detail — root cause, current controls, residual risk, action plan
- KRI tracking: table of indicators + trend arrows
- Review log: a template for the monthly/quarterly review
- Starter risks: pre-populate 15-20 common risks per industry

TONE: Risk management — objective, vigilant, actionable.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
