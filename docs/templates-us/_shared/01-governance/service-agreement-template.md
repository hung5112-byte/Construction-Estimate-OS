# PROMPT 13: Service Agreement Template

#### Description
A B2B service-agreement template, used for buying/selling services, hiring freelancers, and outsourcing. Customized to the service type and industry. Governed by Texas contract law. General information only — not legal advice.

#### Information to collect (ask the user before generating)
1. Is the company the provider or the client? (or both?)
2. Most common service type? (consulting, IT, marketing, logistics...)
3. Payment: milestone, monthly, on completion?
4. Need an SLA (Service Level Agreement)?
5. Any international element? (governing law, currency, time zone)

#### Suggested template
Structure:
- **Section 1** — Parties, representatives
- **Section 2** — Scope of services (SOW / Scope of Work)
- **Section 3** — Term, schedule, milestones
- **Section 4** — Contract value, payment method, taxes (sales tax if applicable)
- **Section 5** — Obligations of the parties
- **Section 6** — SLA & KPIs (if any)
- **Section 7** — Confidentiality & intellectual property
- **Section 8** — Indemnification & limitation of liability
- **Section 9** — Termination
- **Section 10** — Force majeure
- **Section 11** — Governing law (Texas) & dispute resolution
- **Appendix**: SOW template, SLA template, rate sheet

Confirm the structure before generating.

#### File-generation prompt
```
Create a service-agreement template.

CONTEXT:
- Company: [Name] — Role: [provider / client / both]
- Service type: [consulting / IT / marketing / logistics / other]
- Payment: [milestone / monthly / on completion]
- SLA: [Yes/No]
- International: [Yes/No] — Governing law: [Texas / other]

FORMAT:
- Template form: fill-in fields = [___]
- A separate SOW attachment template
- SLA template (if any): metric | target | measurement | remedy
- Rate sheet: service | unit | unit price | notes
- Payment-schedule template: milestone | deliverable | % | amount | due date

TONE: Professional, balanced between the two parties.
LENGTH: 6-8 pages + appendices.

NOTE: General information, not legal advice. Have a Texas attorney review before use.
```

---
✍️ Author: Brian H. Doan
