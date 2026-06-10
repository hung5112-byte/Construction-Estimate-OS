### PROMPT 10: Sales Contract Template

#### Description
A standard sales / service contract template — basic legal terms, an exhibit describing the product/service, and an acceptance record. Protects both parties and reduces dispute risk. General information only — not legal advice; have a licensed Texas attorney review before use.

> US legal note: US contracts are governed by state law. A sale of goods is governed by the Uniform Commercial Code Article 2 as adopted in Texas (Tex. Bus. & Com. Code ch. 2); services are governed by Texas common law. Sales tax (not VAT) is added where the sale is taxable. Note: courts generally enforce **liquidated damages** that are a reasonable estimate of likely harm but will not enforce a clause that is a **penalty** — draft the breach clause accordingly [verify with an attorney].

#### Information to collect (ask the user before generating)
1. Contract type? (sale of goods / services / subscription)
2. Default payment terms? (deposit, milestone payments, COD, Net X)
3. Warranty? (term, conditions, scope)
4. Breach remedy? (liquidated damages — a reasonable estimate, not a penalty)
5. Dispute resolution? (negotiation → mediation/arbitration → Texas courts)
6. Need a technical exhibit / SLA?
7. Who signs? (individual / company — representative, title)

#### Suggested template
Structure:
- **Preamble**: parties (Party A – Seller, Party B – Buyer), recitals
- **Section 1** — Subject: product/service description
- **Section 2** — Contract value & payment
- **Section 3** — Time & place of performance
- **Section 4** — Seller's rights & obligations
- **Section 5** — Buyer's rights & obligations
- **Section 6** — Warranty & support
- **Section 7** — Confidentiality
- **Section 8** — Breach & liquidated damages (reasonable estimate, not a penalty)
- **Section 9** — Force majeure
- **Section 10** — Termination
- **Section 11** — Dispute resolution & governing law (Texas)
- **Section 12** — General provisions
- **Exhibit 1**: product/service detail + price
- **Exhibit 2**: SLA (if any)
- **Acceptance / delivery record**

Confirm the structure before generating.

#### File-generation prompt
```
Create a Sales Contract Template.

CONTEXT:
- Company: [Name] — EIN: [number] — Representative: [name + title]
- Contract type: [sale of goods / services / subscription]
- Payment: [deposit % + milestones / COD / Net X]
- Warranty: [term] — Scope: [describe]
- Breach: liquidated damages [reasonable estimate]
- Disputes: [negotiation → mediation/arbitration / Texas courts]
- SLA exhibit: [Yes/No]
- Authority: Texas contract law; UCC Art. 2 (Tex. Bus. & Com. Code ch. 2) for goods; governing law: Texas

FORMAT:
- Clear sections, continuously numbered
- Party info: table Party A | Party B — Name, EIN, Address, Representative, Title, Phone, Email
- Price exhibit: # | Item | Unit | Qty | Unit price | Amount | Sales tax | Total (USD)
- Payment schedule: Installment | % | Amount | Condition | Deadline
- SLA (if any): table Metric | Target | Measurement | Remedy
- Acceptance record: header + delivery content + inspection result + signatures
- Placeholders: [___] for all variable info

TONE: Legal — precise, tight, balanced between the parties.
LENGTH: 6-10 pages (contract + exhibits + record).

NOTE: General information, not legal advice. Have a licensed Texas attorney review. Avoid penalty clauses; use enforceable liquidated damages.
```

---
✍️ Author: Brian H. Doan
