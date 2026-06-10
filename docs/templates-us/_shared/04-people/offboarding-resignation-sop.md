# P-PPL-18: Offboarding / Resignation SOP

#### Description
The process when an employee leaves — from receiving notice, through handover and final pay, to the exit interview. Reflects US/Texas rules on at-will employment and final-pay timing. Keeps the business running and lets the employee leave cleanly. General information only — not legal advice; confirm final-pay and COBRA obligations with an attorney/CPA.

> US legal note: US employment is **at-will**, so there is generally **no statutory advance-notice requirement** (the common "two weeks' notice" is custom, not law). For final pay, the **Texas Payday Law** (Tex. Lab. Code §61.014) requires: if the employee is **discharged**, final wages within **6 calendar days**; if the employee **quits**, by the **next regular payday** [verify]. **COBRA** continuation of group health coverage applies to employers with **20+ employees** (29 U.S.C. §1161) [verify].

#### Information to collect (ask the user before generating)
1. Notice period expectation? (customary 2 weeks — not legally required at-will)
2. Who receives the resignation? (manager first or HR first?)
3. Handover process: how many days? Who supervises?
4. Final pay: accrued PTO (if your policy pays it out), wages, bonus — timeline per Texas Payday Law?
5. Exit interview? Who conducts it?
6. Asset/access recovery: IT revoke, badge, keys — timeline?

#### Suggested template
Structure:
- **Step 1** — Receive resignation: form, notice, acknowledgment
- **Step 2** — Internal notification: who needs to know, when, how
- **Step 3** — Work handover: list, recipient, timeline, sign-off
- **Step 4** — Asset & access recovery: IT, admin, badge, keys, documents
- **Step 5** — Final pay: wages, accrued PTO payout (per policy), bonus — within Texas Payday Law timing
- **Step 6** — Exit interview: questions, conductor, report
- **Step 7** — System updates: HR records, payroll, org chart; COBRA notice if applicable

Confirm the structure before generating.

#### File-generation prompt
```
Create an Offboarding / Resignation SOP.

CONTEXT:
- Company: [Name] — Notice expectation: [e.g. 2 weeks, customary]
- Receives resignation: [Manager / HR]
- Handover: [days]
- Exit interview: [Yes/No] — Conductor: [HR / Manager]
- Authority: at-will employment (Texas); Texas Payday Law final-pay timing (Tex. Lab. Code §61.014); COBRA (29 U.S.C. §1161, 20+ employees)

FORMAT:
- Overall flowchart: Mermaid — Notice → Acknowledge → Handover → Recover assets → Final pay → Exit interview → Close
- Timeline: notice date (D0) → handover (D+X) → last day → final pay (per Texas Payday Law)
- Handover checklist: Tasks | Assets | Accounts/passwords | Documents | Receivables/customers
- IT revoke checklist: Email | Laptop | Access | Cloud | VPN | Badge — ☐ + Owner + Deadline
- Final-pay checklist: Wages | Accrued PTO (if policy pays out) | Bonus | COBRA notice (if 20+)
- Exit interview: 10 questions + report template → HR summary for management
- Legal notes: final-pay timing (Texas Payday Law), COBRA election notice

TONE: Standard SOP, compliant, respectful of the departing employee.
LENGTH: 5-7 pages.

NOTE: General information, not legal advice. Confirm final-pay timing and COBRA with an attorney/CPA.
```

---
✍️ Author: Brian H. Doan
