### PROMPT 01: Training Policy

#### Description
The company's overall training policy — principles, goals, the company's and employees' rights & obligations in training, the training budget, post-training service commitment, the proposal & approval process, and evaluation. The internal foundation for all L&D activity. General information only — not legal advice; have an attorney review any repayment/clawback terms.

#### Information to collect (ask the user before generating)
1. A dedicated training budget? % of payroll or revenue?
2. Do employees sign a post-training service commitment? (e.g. training over $2,000 → 12-month commitment)
3. Training modes: in-house / external / online / blended?
4. Who can propose training? Approval process?
5. Support for self-directed learning? (tuition, time, certifications)
6. Industry-specific legal training requirements? (OSHA safety, professional licensing/CE...)

> US note: "training repayment agreement provisions" (TRAPs / clawbacks) are used in the US but are increasingly scrutinized and may be limited or unenforceable depending on amount, terms, and state law (and FTC attention). If you require repayment of training costs when an employee leaves early, have a licensed attorney draft/review it for enforceability. [verify]

#### Suggested template
Structure:
- **Articles 1-3** — Purpose, scope, glossary
- **Article 4** — Training principles: continuous, planned, strategy-linked, measurable
- **Article 5** — Training categories: mandatory (compliance) / job skills / personal development / leadership
- **Article 6** — Rights & obligations: what the company commits / what the employee commits
- **Article 7** — Budget: how it's set, approved, tracked
- **Article 8** — Training proposal & approval process
- **Article 9** — Post-training service commitment & cost repayment (subject to enforceability — see note)
- **Article 10** — Training-effectiveness evaluation (Kirkpatrick)
- **Article 11** — Training-record retention
- **Article 12** — Violations
- **Appendix**: training commitment form, training-proposal form

Confirm the structure before generating.

#### File-generation prompt
```
Create a Training Policy.

CONTEXT:
- Company: [Name] — Industry: [industry] — Headcount: [number]
- Training budget: [% of payroll or fixed amount]
- Service commitment: [yes/no] — Detail: [conditions]
- Modes: [in-house / external / online / blended]
- Mandatory industry training: [licenses/certifications]
- Self-learning support: [yes/no] — [detail]

FORMAT:
- Continuously numbered articles, clear language
- Training classification matrix: Type | Mandatory/Voluntary | Audience | Frequency | Budget | Example
- Budget allocation: Category | % Budget | Approval level | Cap per person (USD)
- Approval flowchart: Mermaid — Proposal → Line Manager → HR → Finance → CEO (by amount)
- Service commitment: table Training cost | Commitment period | Repayment if leaving early (note enforceability)
- Training-hours target: table Level | Min hours/year | Mandatory | Optional
- Record retention: table Record type | Retention period | Format | Storage
- Acknowledgment form: agreement to comply with the policy

TONE: Clear policy, balancing employee benefit and company interest.
LENGTH: 6-10 pages.

NOTE: General information, not legal advice. Have a licensed attorney review any training-repayment/clawback terms for enforceability.
```

---
✍️ Author: Brian H. Doan
