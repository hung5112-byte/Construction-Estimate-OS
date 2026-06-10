### PROMPT 07: Complaint Log & Tracker

#### Description
A template to track all complaints — ticket ID, severity, category, status, SLA compliance, resolution, root cause. Used for real-time tracking and monthly/quarterly trend analysis.

#### Information to collect (ask the user before generating)
1. How do you categorize complaints? (product, delivery, service, payment, staff attitude)
2. How many severity levels? (3 or 4)
3. SLA target by severity?
4. Integrate with a CRM/helpdesk?
5. Who reviews the log weekly?

#### Suggested template
Structure:
- **Complaint Log**: Ticket ID | Date | Customer | Channel | Category | Severity | Description | Assigned to | Status | SLA deadline | Resolution | Root cause
- **Dashboard summary**: total tickets | open | in progress | resolved | overdue SLA | avg resolution time
- **Trend analysis**: monthly — category breakdown, severity breakdown, SLA compliance rate
- **Root cause analysis**: Pareto chart — top 5 causes, frequency, corrective actions

Confirm the structure before generating.

#### File-generation prompt
```
Create a Complaint Log & Tracker.

CONTEXT:
- Company: [Name] — Categories: [list]
- Severity levels: [3/4] — SLA: [detail per level]
- CRM/Helpdesk: [name / none]
- Reviewer: [who] — Review frequency: [weekly/monthly]

FORMAT:
- Master log: 15+ column table — Ticket# | Date | Customer | Channel | Category | Severity | Description | Assigned | Status | SLA deadline | SLA met? | Resolution date | Resolution | Root cause | Follow-up
- Status definitions: New 🔵 | In Progress 🟡 | Escalated 🟠 | Resolved 🟢 | Closed ⚫ | Reopened 🔴
- SLA dashboard: table Severity | SLA target | Avg actual | Compliance % | Trend
- Weekly summary: template — Total | New | Resolved | Open | Overdue | Top category | Top root cause
- Monthly report: category pie-chart guide | severity distribution | SLA trend | action items
- Escalation alert: trigger conditions — auto-escalate when past SLA or severity = Critical

TONE: Tracking, analytical, data-driven.
LENGTH: 4-5 pages.
```

---
✍️ Author: Brian H. Doan
