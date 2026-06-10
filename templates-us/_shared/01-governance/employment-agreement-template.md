# PROMPT 12: Employment Agreement Template (Offer Letter / At-Will Employment)

#### Description
A standard US employment-agreement template. **Texas is an at-will employment state** — either party may end the employment relationship at any time, with limited exceptions. The federal **FLSA** governs minimum wage and overtime, and the **Texas Payday Law** (Texas Workforce Commission) governs wage payment. The document is structured as an at-will offer/agreement; any probation or severance terms are contractual, not statutory. General information only — not legal advice.

#### Information to collect (ask the user before generating)
1. Document type? (offer letter / full employment agreement / both)
2. Exempt or non-exempt under the FLSA? (affects overtime eligibility)
3. Any benefits beyond the legal minimum? (e.g. private health insurance, equity/options, remote work, PTO)
4. A non-compete or non-solicitation clause after separation?
5. Is the pay scale / compensation already set?

#### Suggested template
Structure (offer letter / agreement):
- **Section 1** — Parties: employer + employee
- **Section 2** — Position, start date, at-will statement
- **Section 3** — Duties, location, title
- **Section 4** — Compensation: pay rate, bonus, pay schedule, exempt/non-exempt status
- **Section 5** — Hours, PTO/leave (note any FMLA eligibility for larger employers)
- **Section 6** — Benefits (health, retirement); payroll taxes (FICA/FUTA/SUTA) withheld/paid
- **Section 7** — Training
- **Section 8** — Confidentiality, IP assignment, non-compete/non-solicit
- **Section 9** — At-will employment & separation (no fixed notice required, but state any agreed notice)
- **Section 10** — Policies (reference the employee handbook)
- **Section 11** — Dispute resolution & governing law (Texas)
- **Signature block**: both parties, each keeps a copy

Confirm the structure before generating.

#### File-generation prompt
```
Create an employment-agreement template (offer letter / at-will employment).

CONTEXT:
- Company: [Name] — Industry: [industry] — Size: [headcount]
- Document type: [offer letter / full agreement / both]
- Exempt or non-exempt (FLSA): [exempt / non-exempt]
- Benefits: [list]
- Non-compete: [Yes/No] — Duration: [months] — Geographic scope: [...]
- Legal basis: at-will employment (Texas); FLSA (29 U.S.C. § 201); Texas Payday Law (TWC).
  Texas enforces a reasonable non-compete under Tex. Bus. & Com. Code § 15.50 [UNCERTAIN — verify with attorney].

FORMAT:
- Template form: fill-in fields = [___], checkboxes = ☐
- Clear AT-WILL statement near the top
- A reference table: clause → governing law/agency (FLSA / TWC / Texas common law)
- Appendix: Job Description template, benefits summary, employee NDA
- Highlight clauses that MUST be customized to the company (don't use the template verbatim)

TONE: Legal, standard, easy to fill in.
LENGTH: 4-6 pages.

NOTE: Reference template — MUST be reviewed by a licensed Texas employment attorney before use.
General information, not legal advice.
```

---
✍️ Author: Brian H. Doan
