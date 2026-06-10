# P-FIN-12: Month-End Closing SOP (Monthly Close)

#### Description
The monthly-close accounting process — a checklist of all accounting work to finish before "closing the books" each month. Covers recording, reconciliation, adjusting entries, and reporting.

#### Information to collect (ask the user before generating)
1. Close timeline: by which day each month must it be done? (e.g. the 5th of the following month)
2. How many accountants work the close?
3. Accounting software? How much is automated?
4. Common adjusting entries? (depreciation, allocations, accruals, reserves)
5. What reports are due after close? (internal / tax / bank)

#### Suggested template
Structure:
- **Close timeline** — Gantt: Day 1 → Day 5 (or custom), what happens each day
- **Pre-close checklist** — before close: bank reconciliation, cash count, cut-off
- **Close checklist** — during close: adjusting entries, depreciation, allocations, reserves
- **Post-close checklist** — after close: review, prepare reports, file taxes
- **Reconciliation** — GL vs. subledger, bank vs. books, inventory vs. books
- **Reporting** — list of reports due + deadline + recipient
- **Sign-off** — Accountant → Controller → CFO/Owner

Confirm the structure before generating.

#### File-generation prompt
```
Create a Monthly Close SOP.

CONTEXT:
- Company: [Name] — Close timeline: day [X] each month
- Number of accountants: [number] — Software: [name]
- Main adjusting entries: [list]
- Reports due: [internal / sales tax / payroll tax / bank]

FORMAT:
- Gantt chart: Day 1-5 × Tasks × Owner — Mermaid or table
- Pre-close checklist: 10-15 items ☐ + Owner + Deadline
- Close checklist: 15-20 items ☐ + sample journal entries
- Post-close checklist: 8-10 items ☐ + Report + Deadline
- Reconciliation template: GL vs. subledger vs. source → variance → resolution
- Sign-off sheet: Task | Done by | Reviewed by | Date | Notes
- Common errors: table of common mistakes + how to prevent them

TONE: Standard SOP, operational, checklist-oriented.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
