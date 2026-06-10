# PROMPT 14: NDA Template (Non-Disclosure Agreement)

#### Description
A Non-Disclosure Agreement (NDA) template — two versions: one-way and mutual. Used for employees, partners, vendors, and investors. Governed by Texas contract law. General information only — not legal advice.

#### Information to collect (ask the user before generating)
1. Which NDA type? (one-way / mutual / both)
2. Who signs: employee / business partner / investor / freelancer?
3. Confidentiality term after the relationship ends? (1 year / 2 years / indefinite for trade secrets)
4. Scope of confidential information: everything, or only specific categories?
5. Remedy for breach: injunctive relief and/or liquidated damages (a reasonable estimate of harm, not a penalty)?

#### Suggested template
Structure:
- **Section 1** — Parties, purpose of the NDA
- **Section 2** — Definition of "Confidential Information" — list clearly: business, technical, financial, customer, personnel
- **Section 3** — Confidentiality obligations: no disclosure, no use, reasonable safeguards
- **Section 4** — Exclusions: already public, previously known, lawfully from a third party, legally required
- **Section 5** — Term: during and after the relationship (trade secrets may be protected indefinitely)
- **Section 6** — Return/destroy materials
- **Section 7** — Remedies: injunctive relief + liquidated damages (reasonable, not a penalty — Texas common law)
- **Section 8** — Governing law (Texas) & dispute resolution

Confirm the structure before generating.

#### File-generation prompt
```
Create an NDA template (Non-Disclosure Agreement).

CONTEXT:
- Company: [Name]
- Type: [one-way / mutual / both]
- Signer: [employee / partner / investor / freelancer]
- Confidentiality term: [time after the relationship ends]
- Remedy: [injunctive relief / liquidated damages in USD as a reasonable estimate of harm]

FORMAT:
- Two separate versions: one-way + mutual (if both selected)
- Concise and to the point — an NDA need not be long
- Highlight: the definition of "Confidential Information" must be VERY SPECIFIC
- Appendix: list of confidential-information categories by department

TONE: Legal, tight, concise.
LENGTH: 3-4 pages per version.

NOTE: Reference template — have a licensed Texas attorney review it before use. Not legal advice.
```

---
✍️ Author: Brian H. Doan
