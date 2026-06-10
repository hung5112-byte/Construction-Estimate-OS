# P-PPL-04: Headcount Plan

#### Description
An overall headcount plan — how many you have now, how many you need to hire, when, and the budget. Tied directly to the business strategy and budget.

#### Information to collect (ask the user before generating)
1. Current headcount by department?
2. Business plan for the next 12 months? (revenue growth → more staff needed?)
3. Current turnover rate?
4. Current payroll budget as % of revenue?
5. Plans to open a branch / launch a new product needing a new team?

#### Suggested template
Structure:
- **Current State**: table department × current HC × cost
- **Gap Analysis**: compare current HC vs. HC needed by strategy
- **Hiring Plan**: hiring timeline by quarter — role | dept | Q1 | Q2 | Q3 | Q4 | Priority
- **Budget Impact**: payroll forecast — current + incremental + total
- **Turnover Forecast**: expected exits + replacement plan
- **Ratios**: revenue per employee, cost per hire, time to fill

Confirm the structure before generating.

#### File-generation prompt
```
Create a Headcount Plan.

CONTEXT:
- Company: [Name] — Current HC: [number] — Per dept: [detail]
- Growth plan: [describe]
- Turnover: [%/year]
- Payroll/Revenue ratio: [%]
- Expansion: [branch / new product if any]

FORMAT:
- Current state: Dept | Current HC | Avg Salary | Total Cost | Revenue/employee (USD)
- Gap analysis: Dept | Current | Needed | Gap | Priority | Justification
- Hiring timeline: Gantt-style Q1-Q4 × role
- Budget forecast: monthly payroll × 12 months → total + YoY change
- Turnover model: Dept | Rate | Expected exits | Replacement cost
- Summary KPIs: Total HC plan | New hires | Budget impact | Cost per hire

TONE: Strategic, data-driven, tied to the business plan.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
