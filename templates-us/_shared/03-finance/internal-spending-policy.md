# P-FIN-02: Internal Spending Policy

#### Description
A detailed policy on spending limits, approval workflow, allowed expense categories, and day-to-day spending controls. This file is used by EVERY employee — it must be clear, easy to understand, and easy to look up.

#### Information to collect (ask the user before generating)
1. No-approval-needed spending limit per level? (e.g. Staff < $500, Manager < $5,000, Owner < $50,000)
2. Common expense categories? (e.g. office supplies, travel, client meals, conferences...)
3. Which expenses need special approval? (e.g. advertising > $X, asset purchase > $Y)
4. Approval process: email / software / paper? How many approval levels?
5. Advances allowed? How soon must they be reconciled?
6. Out-of-category spend — what's the special-approval process?

#### Suggested template
Structure:
- **Article 1-3** — Purpose, scope, glossary
- **Article 4** — Spending principles: in budget, on purpose, fully documented, pre-approved
- **Article 5** — Approval levels: a detailed limit table by level × expense type
- **Article 6** — Expense categories: list + per-item limits (e.g. client meals max $X/instance)
- **Article 7** — Spending process: flowchart from incurrence → approval → payment → documentation
- **Article 8** — Advances & reconciliation: limits, deadlines, handling unreconciled advances
- **Article 9** — Special spending: out-of-category, over-limit, emergency
- **Article 10** — Violations: consequences, reimbursement responsibility
- **Appendix**: expense-limit table, payment-request form

Confirm the structure before generating.

#### File-generation prompt
```
Create an Internal Spending Policy.

CONTEXT:
- Company: [Name] — Size: [headcount] — Revenue: [amount/year]
- Approval limits: Staff [___] | Manager [___] | Owner [___] | Board [___]
- Approval process: [email / software / paper]
- # approval levels: [number]
- Advances: [Yes/No] — Reconciliation deadline: [days]

FORMAT:
- Continuously numbered articles, clear language for all levels of staff
- Approval table: Expense type | < $X (Staff) | < $Y (Manager) | < $Z (Owner) | > $Z (Board)
- Limit table: Type | Limit/instance | Limit/month | Notes (USD)
- Approval flowchart: Mermaid — Incur → Request → Approve → Pay → Document → Record
- FAQ: 10 common situations (e.g. late-night taxi, client meals over the limit...)

TONE: Clear, easy, practical — readable by anyone.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
