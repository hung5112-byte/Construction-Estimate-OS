# PROMPT 19: License Renewal Calendar

#### Description
A calendar view of all licenses, certifications, insurance policies, and registrations that need periodic renewal. Alert system at 90/60/30/15 days ahead.

#### Information to collect (ask the user before generating)
1. Consolidate from which files? (Licenses & Permits Registry + Insurance Portfolio + entity registration)
2. Who receives alerts? (Admin / Legal / Owner)
3. Alert channel? (Email / Calendar / Slack / SMS)
4. Budget per renewal?

#### Suggested template
Structure:
- **12-month calendar**: month × items to renew
- **Detailed registry**: # | Item | Type | Expiration | Renewal lead time | Cost | Owner | Status
- **Alert rules**: 90 days (notify), 60 days (start paperwork), 30 days (submit), 15 days (escalate)
- **Renewal-process summary**: per license type
- **Dashboard**: total items | expiring | overdue | OK

Confirm the structure before generating.

#### File-generation prompt
```
Create a License Renewal Calendar.

CONTEXT:
- Data sources: [Licenses & Permits + Insurance + entity registration + contracts]
- Alert recipient: [title]
- Alert channel: [Email / Calendar / Slack / SMS]
- Budget tracking: [Yes/No]

FORMAT:
- Calendar view: 12 months, each cell lists items expiring that month
- Registry table: full columns, sorted by expiration ascending
- Color coding: 🟢 OK (>90 days) | 🟡 Attention (30-90 days) | 🟠 Urgent (15-30 days) | 🔴 Critical (<15 days) | ⚫ Expired
- Alert workflow: flowchart for the 4 milestones (90-60-30-15)
- Dashboard summary: KPI cards
- Auto-fill: from the related files in 01-bb-governance

TONE: Operational, action-oriented.
LENGTH: 3-5 pages.
```

---
✍️ Author: Brian H. Doan
