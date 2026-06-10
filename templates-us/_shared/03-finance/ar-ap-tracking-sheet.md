# P-FIN-14: AR/AP Tracking Sheet

#### Description
A tracking sheet for accounts receivable (AR) and accounts payable (AP) — an aging report. Tracks each customer/vendor, classifies by age of the balance, and alerts on overdue items.

#### Information to collect (ask the user before generating)
1. Track AR, AP, or both?
2. Does your accounting software already have an aging report? (supplement or replace?)
3. Aging buckets: 30/60/90/120+ or custom?
4. Any extra columns needed? (e.g. owner, credit limit, follow-up notes)
5. Update frequency? (daily / weekly / monthly)

#### Suggested template
Structure:
- **AR Aging Report**: Customer | Total | Current | 1-30 | 31-60 | 61-90 | >90 | Credit limit | Status | Owner | Next action
- **AP Aging Report**: Vendor | Total | Current | 1-30 | 31-60 | 61-90 | >90 | Due date | Priority | Owner
- **Summary Dashboard**: Total AR | Total AP | Net | Overdue % | DSO | DPO
- **Alert Rules**: color + action per aging bucket
- **Follow-up Log**: Customer/Vendor | Date | Action | Result | Next step

Confirm the structure before generating.

#### File-generation prompt
```
Create an AR/AP Tracking Sheet.

CONTEXT:
- Company: [Name] — Track: [AR / AP / Both]
- # customers: [number] — # vendors: [number]
- Aging buckets: [30/60/90/120+ or custom]
- Update: [daily / weekly / monthly]
- Supplement software: [Yes/No]

FORMAT:
- AR table: 12+ columns, sort by overdue desc
- AP table: 12+ columns, sort by due date asc
- Color coding: 🟢 Current | 🟡 1-30 | 🟠 31-60 | 🔴 61-90 | ⚫ >90
- Summary KPIs: Total AR | Total AP | DSO | DPO | Overdue ratio
- Follow-up log template: a collections action-tracking table
- Top 10 Overdue: highlight the largest customer/vendor balances
- Trend: MoM comparison data

TONE: Operational, tracking-focused.
LENGTH: 3-5 pages.
```

---
✍️ Author: Brian H. Doan
