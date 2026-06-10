### PROMPT 19: Weekly Report Template

#### Description
A weekly report template for managers/employees — summarizing KPIs, done/doing/blocked, highlights, concerns, and next week's plan.

#### Information to collect (ask the user before generating)
1. Who uses this template? (manager reporting to owner / employee reporting to manager / both)
2. Which KPIs to report weekly? (revenue, SLA, quality, project progress...)
3. Submission deadline? (Friday afternoon / Monday morning)
4. Current format? (Email / Excel / Google Docs / verbal)
5. What does the owner/manager most want to see in a weekly report?
6. Max time to read one report? (2 min / 5 min)

#### Suggested template
Structure:
- **Header**: Week # | Date | Department | Reporter
- **KPI Snapshot**: table KPI × Target × Actual × % × Status (🟢🟡🔴)
- **Done this week**: 5-7 completed items
- **In progress**: 3-5 items + % progress
- **Blocked**: 1-3 items stuck + who needs to help
- **Highlights**: 1-2 wins/good news
- **Concerns**: 1-2 risks/issues to escalate
- **Next week plan**: top 5 priorities
- **Sign-off**: one page, readable in 2 minutes

Confirm the structure before generating.

#### File-generation prompt
```
Create a Weekly Report Template.

CONTEXT:
- Company: [Name] — Used for: [Manager→Owner / Employee→Manager / Both]
- KPIs tracked: [list]
- Deadline: [day/time]
- Format: [Excel / Docs / Email]

FORMAT:
- Header: Week [#] | [Date-Date] | Department | Reporter
- KPI Snapshot: table KPI | Weekly target | Actual | % | Status 🟢🟡🔴
- Done this week: 5-7 bullets — completed tasks
- In progress: 3-5 bullets — ongoing + % done
- Blocked: 1-3 bullets — obstacles + who needs to help
- Highlights: 1-2 wins
- Concerns: 1-2 risks/issues to escalate
- Next week plan: top 5 priorities
- Scannable in 2 minutes — one page

TONE: Executive, concise, status-focused.
LENGTH: 1 page.
```

---
✍️ Author: Brian H. Doan
