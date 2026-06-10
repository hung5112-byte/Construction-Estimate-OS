# P-FIN-01: General Financial Policy

#### Description
The top-level policy document for financial management. Sets principles, approval levels, internal controls, and financial accountability. It's the "financial constitution" every other finance process must follow.

#### Information to collect (ask the user before generating)
1. Annual revenue? (sets the complexity of internal controls)
2. Current finance org? (a dedicated CFO, or a controller, or outsourced bookkeeping?)
3. Current approval levels? (does the Department Head approve everything, or is it delegated?)
4. Primary bank? Online banking / authorized signers?
5. Accounting software? (QuickBooks, Xero, NetSuite, Excel...)
6. Internal audit / annual external CPA review?

#### Suggested template
Structure:
- **Article I** — Purpose, scope, who it applies to
- **Article II** — Financial-management principles: transparency, thrift, efficiency, legal compliance
- **Article III** — Finance/accounting org: structure, functions, duties
- **Article IV** — Financial approval levels: a limit table by level (Staff → Manager → CFO → Owner/Board)
- **Article V** — Internal controls: four-eyes principle, segregation of duties, cross-checks
- **Article VI** — Asset & cash management: cash, bank, fixed assets, investments
- **Article VII** — Reporting: report types, frequency, recipients
- **Article VIII** — Audit & oversight
- **Appendix**: detailed approval-limit table, finance org chart

Confirm the structure before generating.

#### File-generation prompt
```
Create a General Financial Policy for the business.

CONTEXT:
- Company: [Name] — Industry: [industry] — Revenue: [amount/year] — Headcount: [number]
- Finance org: [dedicated CFO / controller / outsourced]
- Accounting software: [QuickBooks / Xero / NetSuite / Excel / other]
- Current approval levels: [describe]
- Audit: [internal / external CPA / none]
- Basis: US GAAP (FASB)

FORMAT:
- Articles with numbered sections
- Approval-limit table: cost type | Staff | Manager | CFO/Controller | Owner | Board + USD limit
- Finance org chart: Mermaid
- Internal-control principles: an applied checklist
- Reporting: table Report type | Frequency | Prepared by | Recipient | Deadline

TONE: Formal, standard, US-aligned.
LENGTH: 10-15 pages.
```

---
✍️ Author: Brian H. Doan
