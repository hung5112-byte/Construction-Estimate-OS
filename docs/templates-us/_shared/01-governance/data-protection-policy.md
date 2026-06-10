# PROMPT 18: Data Protection Policy

#### Description
A personal-data protection policy — aligned with the **Texas Data Privacy and Security Act (TDPSA)** and referencing the GDPR (for EU users). Governs collecting, processing, storing, sharing, and deleting personal data. General information only — not legal advice; confirm applicability with a licensed Texas attorney.

#### Information to collect (ask the user before generating)
1. What categories of personal data does the company collect? (customers, employees, partners)
2. Collection channels: website, app, store, phone, social media?
3. Where is data stored? (US servers / cloud)
4. Is data shared with third parties? (advertising, analytics, partners)
5. Is there a privacy lead / data-protection contact?
6. Any EU users / cross-border processing? (GDPR may apply)

#### Suggested template
Structure:
- **Part 1** — Purpose, scope, commitment
- **Part 2** — Definitions: personal data, sensitive data, consumer, controller, processor
- **Part 3** — Processing principles: lawful basis, transparency, purpose limitation, data minimization, accuracy, storage limitation, security
- **Part 4** — Collection: data categories, purpose, lawful basis, consent
- **Part 5** — Storage & security: retention, technical safeguards, access control
- **Part 6** — Third-party sharing: conditions, a data-processing agreement (DPA) template
- **Part 7** — Consumer rights (TDPSA): access, correction, deletion, portability, opt-out of sale/targeted ads
- **Part 8** — Breach response: notify affected consumers without unreasonable delay; notify the Texas Attorney General if 250+ Texans are affected [UNCERTAIN — verify thresholds/timing with attorney]
- **Part 9** — Roles & responsibilities: privacy lead, IT, HR, Marketing
- **Appendix**: consent form, data-mapping template, breach-notification template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Data Protection Policy.

CONTEXT:
- Company: [Name] — Industry: [industry]
- Data collected: [categories: customers, employees, partners]
- Channels: [website / app / offline / social]
- Storage: [US servers / cloud / hybrid]
- Third-party sharing: [Yes/No] — [list]
- Privacy lead: [Yes/No]
- Cross-border / EU users: [Yes/No]
- Legal basis: Texas Data Privacy and Security Act (TDPSA) + GDPR (if there are EU users) [UNCERTAIN — verify with attorney]

FORMAT:
- Clear sections with a table of contents
- Data-mapping table: data type | source | purpose | lawful basis | retention | sharing
- Consumer rights: a rights table + how to exercise + response SLA
- Breach-response flowchart: detect → assess → notify → remediate
- Appendix: consent form, DPA template, breach-report template

TONE: Compliance — serious, transparent, rights-protective.
LENGTH: 12-18 pages.

CROSS-REFERENCE: This is the legal data-protection policy. For the employee confidentiality policy, see bb-people/Information Confidentiality Policy. For the technical cybersecurity policy, see bb-product-tech/Cybersecurity Policy.

NOTE: General information, not legal advice. Confirm applicability with a licensed Texas attorney.
```

---
✍️ Author: Brian H. Doan
