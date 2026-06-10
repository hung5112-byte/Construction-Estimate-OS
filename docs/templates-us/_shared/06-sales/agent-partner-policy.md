### PROMPT 15: Agent / Partner Policy

#### Description
A comprehensive policy for agents and distribution partners — defining how to become a partner, the rights and obligations, commission structure, territory, KPIs, and the evaluation process. The clear "rules of the game" for the partner relationship.

#### Information to collect (ask the user before generating)
1. Partner type? (sales agent / distributor / reseller / affiliate / referral partner)
2. Criteria to become a partner? (capital, experience, headcount, region)
3. Commission structure? (% of revenue / volume discount / tiered commission)
4. Territory? (exclusive / non-exclusive)
5. Partner KPIs? (minimum sales / month, quarter)
6. Support? (marketing, training, co-branding, tools)
7. Evaluation cadence? Termination conditions?
8. Partner tiers? (Silver / Gold / Platinum?)

#### Suggested template
Structure:
- **Sections 1-3** — Purpose, scope, partner-type definitions
- **Section 4** — Conditions & process to become a partner
- **Section 5** — Partner tiers: table of tiers + conditions + benefits
- **Section 6** — Partner benefits: commission, marketing support, training, tools, co-branding
- **Section 7** — Partner obligations: minimum sales, reporting, brand compliance, customer care
- **Section 8** — Commission structure: detailed table tier × product × %
- **Section 9** — Territory & exclusivity: territory rules, conflict handling
- **Section 10** — Evaluation & ranking: KPIs, frequency, rewards/penalties
- **Section 11** — Termination & wind-down: conditions, process, post-termination obligations
- **Appendix**: partner application, detailed commission table, KPI scorecard

Confirm the structure before generating.

#### File-generation prompt
```
Create an Agent / Partner Policy.

CONTEXT:
- Company: [Name] — Industry: [industry]
- Partner type: [agent / distributor / reseller / affiliate / referral]
- Criteria: [capital / experience / headcount / region]
- Commission: [% / tiered / hybrid]
- Territory: [exclusive / non-exclusive] — Regions: [list]
- KPIs: [min sales / month, quarter]
- Tiers: [Silver / Gold / Platinum or custom]
- Support: [marketing / training / tools / co-brand]

FORMAT:
- Continuously numbered sections, clear language
- Tier matrix: table Tier | Conditions | Commission % | Marketing support | Training | Territory
- Commission table: Product | Tier 1 % | Tier 2 % | Tier 3 % | Bonus condition
- KPI scorecard: KPI | Target | Weight | Measurement | Frequency
- Territory map: Region | Partner | Exclusive? | Population | Market size
- Evaluation timeline: Q1 review | mid-year | annual | re-certification
- Termination flowchart: Mermaid — Warning → Probation → Termination → Settlement
- Application: a 1-page form

TONE: Professional, clear, fair, attractive to prospective partners.
LENGTH: 8-12 pages.

NOTE: Commission and termination terms become contractual in the Partner Agreement — have an attorney review that contract.
```

---
✍️ Author: Brian H. Doan
