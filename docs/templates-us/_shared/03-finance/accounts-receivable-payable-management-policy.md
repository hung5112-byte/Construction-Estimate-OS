# P-FIN-03: Accounts Receivable / Payable Management Policy

#### Description
A comprehensive policy for managing accounts receivable (AR) and accounts payable (AP). Sets payment terms, customer credit limits, collections process, the allowance for doubtful accounts, and vendor-payment management. General information only — not legal/accounting advice; confirm collections practices and the allowance method with a licensed CPA/attorney.

#### Information to collect (ask the user before generating)
1. Business model? (B2B with long terms / B2C paid up front / hybrid)
2. Common payment terms? (COD, Net 15, Net 30, Net 60?)
3. Current AR status? (% past due, bad debt)
4. Do you have a dedicated collections function?
5. Customer credit criteria? (revenue, history, guarantee...)
6. Early-payment discount policy?

#### Suggested template
Structure:
- **Part 1** — Purpose, scope, glossary
- **Part 2** — AR management: granting credit, limits, terms, discounts
- **Part 3** — Collections: a 4-step process (reminder → follow-up → warning → legal/collections referral)
- **Part 4** — Allowance for doubtful accounts: criteria, rates, write-off process (US GAAP allowance for credit losses, ASC 326 / CECL — method and applicability vary by entity [verify with CPA])
- **Part 5** — AP management: payment priority, capturing discounts, cashflow management
- **Part 6** — Reconciliation: frequency, process, handling discrepancies
- **Part 7** — Roles & responsibilities
- **Appendix**: aging-analysis template, demand-letter sample, credit-application form

Confirm the structure before generating.

#### File-generation prompt
```
Create an AR/AP Management Policy.

CONTEXT:
- Company: [Name] — Model: [B2B / B2C / Hybrid]
- Payment terms: [COD / Net 15 / Net 30 / Net 60]
- AR status: [% past due] — Bad debt: [% or amount]
- Collections function: [Yes/No]
- Early-payment discount: [Yes/No] — [detail]

FORMAT:
- Clear parts, with a table of contents
- Credit scoring: table Criterion | Weight | Score → credit limit
- Aging buckets: Current | 1-30 | 31-60 | 61-90 | 91-120 | >120 days
- Collections escalation: 4-step flowchart + timeline + owner
- Allowance for doubtful accounts: table aging × % allowance (US GAAP / ASC 326 — confirm method with CPA)
- AP payment-priority matrix: strategic vendors > regular vendors > other

TONE: Professional, financial, tight.
LENGTH: 8-12 pages.

NOTE: General information, not legal/accounting advice. Confirm collections practices and the allowance method with a licensed CPA/attorney.
```

---
✍️ Author: Brian H. Doan
