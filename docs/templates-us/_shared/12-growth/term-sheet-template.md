### PROMPT 05: Term Sheet Template

#### Description
An investment term-sheet template — a (mostly) non-binding document summarizing terms & conditions before the definitive agreements. Covers valuation, investment amount, instrument type, investor rights, governance, and protective provisions. General information only — raising investment is a securities transaction; have a securities attorney review.

> US securities note: offering equity, SAFEs, or convertible notes is the sale of a **security**. It must be registered or exempt — most startups rely on a **Regulation D** exemption (SEC Rule 506(b) or 506(c), 17 CFR §230.506) with a **Form D** filing, plus state "blue-sky"/Texas notice filings. 506(c) allows general solicitation but requires verifying accredited-investor status. [verify all specifics with a securities attorney]

#### Information to collect (ask the user before generating)
1. Instrument type? (Equity / Convertible Note / SAFE / Hybrid)
2. Pre-money valuation range?
3. Desired board composition?
4. Which investor rights are acceptable / not?
5. Founder vesting: existing or to be added?
6. Governing law? (Delaware / Texas)

#### Suggested template
Structure:
- **Preamble** — parties, date, non-binding notice (except confidentiality/exclusivity)
- **Investment Terms** — amount, valuation, price per share, type of security
- **Capitalization** — pre- & post-money cap table
- **Investor Rights** — information rights, pro-rata, anti-dilution, registration
- **Governance** — board composition, observer rights, protective provisions
- **Founder Terms** — vesting, non-compete, key-person insurance
- **Closing Conditions** — due diligence, legal, regulatory (Reg D / Form D)
- **Other** — exclusivity period, expenses, confidentiality, governing law

Confirm the structure before generating.

#### File-generation prompt
```
Create a Term Sheet Template.

CONTEXT:
- Company: [Name] — Instrument: [Equity / Note / SAFE]
- Valuation: [pre-money] — Raise: [amount] (USD)
- Board: [current + proposed]
- Governing law: [Delaware / Texas]
- Authority: Securities Act of 1933; Reg D Rule 506(b)/(c) (17 CFR §230.506) + Form D; state blue-sky filings

FORMAT:
- Investment terms: summary table — Item | Term | Notes
  - Security type, Price/share, Amount, Pre-money, Post-money, Shares issued (USD)
- Cap-table impact: Before | After — per shareholder
- Investor rights: checklist ☐ — Information | Pro-rata | Anti-dilution (type) | Registration | Tag-along | Drag-along
- Governance: board seats | observer | protective provisions (veto list)
- Founder: vesting schedule | non-compete | ESOP commitment | key person
- Conditions: due-diligence scope | timeline | exclusivity period | securities-exemption compliance (Reg D)
- Definitions: key terms — liquidation event, qualified financing, material adverse change
- Signature block: Company | Investor | Date

⚠️ LEGAL NOTE: This term sheet MUST be reviewed by a securities attorney. The financing must comply with federal/state securities law (typically a Reg D exemption + Form D).

TONE: Legal-lite — clear, balanced, professional.
LENGTH: 4-6 pages.

NOTE: General information, not legal advice.
```

---
✍️ Author: Brian H. Doan
