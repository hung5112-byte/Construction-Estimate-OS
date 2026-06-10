# P-FIN-11: Accounts Reconciliation SOP

#### Description
A periodic process to reconcile balances between the company and its customers (AR) and vendors (AP). Ensures the books match what partners show, and catches discrepancies early.

#### Information to collect (ask the user before generating)
1. Reconciliation frequency? (monthly / quarterly / when a discrepancy arises)
2. How many customers/vendors need regular reconciliation?
3. Method: email / in person / signed statement?
4. Software support? (auto-generate the reconciliation, or manual?)
5. Are discrepancies currently common?

#### Suggested template
Structure:
- **Purpose & scope**
- **Reconciliation calendar**: who reconciles with whom, and when
- **AR reconciliation process**: 5 steps — export data → send confirmation → receive response → resolve discrepancy → sign statement
- **AP reconciliation process**: 5 similar steps
- **Discrepancy handling**: decision tree — type of discrepancy → cause → resolution
- **Reconciliation-statement template**
- **Escalation**: when the two sides don't agree

Confirm the structure before generating.

#### File-generation prompt
```
Create an Accounts Reconciliation SOP.

CONTEXT:
- Company: [Name] — # customers to reconcile: [number] — # vendors: [number]
- Frequency: [monthly / quarterly]
- Method: [email / in person / online]
- Software: [name]

FORMAT:
- Reconciliation calendar: table Week/Month × Counterparty
- AR flowchart: Mermaid — 5 steps + timeline
- AP flowchart: Mermaid — 5 steps + timeline
- Discrepancy handling: decision tree — timing / quantity / price / other → action
- Statement template: header + detail table + discrepancy + both signatures
- Aging-report template alongside reconciliation
- KPIs: % reconciliation complete / month, % discrepancy / total balance

TONE: Standard SOP, clear.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
