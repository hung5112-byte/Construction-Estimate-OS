# P-FIN-10: Cash Receipt & Disbursement SOP

#### Description
A standardized process for every cash receipt and disbursement — from incurrence, documentation, and approval, through execution, recording, and filing. Ensures no transaction "escapes" the control system.

#### Information to collect (ask the user before generating)
1. Common payment methods? (cash / bank transfer (ACH/wire) / digital wallet / card)
2. Accounting software? (auto-posting or manual?)
3. # disbursement approval levels? (1 / 2 / 3)
4. Is there petty cash on site? Cash-on-hand limit?
5. How often are deposits made to the bank?

#### Suggested template
Structure:
- **Purpose & scope**
- **Glossary & abbreviations**
- **RECEIPT process**: 6-step flowchart — incur → issue receipt → confirm → collect → record → file
- **DISBURSEMENT process**: 8-step flowchart — request → approve → issue voucher → pay → source document → record → reconcile → file
- **Petty-cash rules**: limit, cash count, bank deposit
- **Required documents**: list per transaction type
- **Retention**: how long, how to organize, digitization

Confirm the structure before generating.

#### File-generation prompt
```
Create a Cash Receipt & Disbursement SOP.

CONTEXT:
- Company: [Name] — Payment methods: [cash / ACH / wallet / card]
- Software: [QuickBooks / Xero / NetSuite / Excel]
- # disbursement approval levels: [number]
- Petty cash: [Yes/No] — Limit: [amount]
- Control basis: internal controls (segregation of duties, four-eyes principle); US GAAP for recording

FORMAT:
- RECEIPT flowchart: Mermaid — 6 clear steps
- DISBURSEMENT flowchart: Mermaid — 8 clear steps, highlight control points
- Document table: transaction type | required documents | who prepares | who approves | # copies
- Petty-cash rules: limit | count frequency | bank-deposit process
- End-of-day checklist: 5 items for the bookkeeper
- Error handling: table common errors | resolution | escalation

TONE: Standard SOP — clear, step-by-step, unambiguous.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
