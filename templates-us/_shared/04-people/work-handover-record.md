# P-PPL-19: Work Handover Record

#### Description
A handover-record template for when an employee leaves or changes roles — fully documenting: work in progress, assets, accounts, documents, receivables, and customers managed. Signed by three parties: the departing employee + the receiver + the manager.

#### Information to collect (ask the user before generating)
1. Required handover items? (role-dependent: Sales hands over customers, Accounting hands over the books)
2. Asset handover: laptop, phone, vehicle, badge — inspection process?
3. Account handover: email, CRM, software, company social — who takes over?
4. Need to hand over receivables / customers being managed?
5. Who signs off? (3 parties, or add HR?)

#### Suggested template
Structure:
- **Header**: departing employee + receiver + date
- **Part 1** — Work in progress: Task | Status | Deadline | Notes
- **Part 2** — Assets: Asset ID | Name | Condition | Notes
- **Part 3** — Accounts & passwords: System | Account | Access transferred ☐
- **Part 4** — Documents: List | Storage location | Handed over ☐
- **Part 5** — Receivables & customers: Customer | Balance | Status | Receiver
- **Signatures**: departing employee | receiver | manager | HR (if needed)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Work Handover Record.

CONTEXT:
- Company: [Name]
- Required items: [Work / Assets / Accounts / Documents / Receivables-Customers]
- Sign-off: [3 parties / 4 parties (add HR)]

FORMAT:
- One template form, 2-3 pages
- Header: company info | departing employee (name, title, dept, last day) | receiver (name, title)
- Work table: # | Task | Status (Done/In progress/Pending) | Deadline | Notes for receiver
- Asset table: # | Asset ID | Name | Serial# | Condition | Recovered ☐
- Account table: # | System | Username | Password reset ☐ | Access transferred ☐
- Document table: # | Document | Storage (folder/drive) | Handed over ☐
- Customer/receivables table: # | Customer | Balance | Status | Receiver | Notes
- Signature footer: 3-4 boxes — Departing | Receiver | Manager | HR
- Notes: open items + resolution timeline

TONE: Formal, complete, avoids post-departure disputes.
LENGTH: 2-3 pages.
```

---
✍️ Author: Brian H. Doan
