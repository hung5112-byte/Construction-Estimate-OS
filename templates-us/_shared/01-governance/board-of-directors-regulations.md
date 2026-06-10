# PROMPT 07: Board of Directors Regulations

#### Description
Internal regulations governing how the board of directors (or LLC managers/members) operates, its authority, and its decision process. Supplements the formation documents for day-to-day governance. Based on the Texas Business Organizations Code (TBOC). General information only — not legal advice.

#### Information to collect (ask the user before generating)
1. Entity type & governance structure?
2. How many directors/managers? Any independent members?
3. Meeting frequency: monthly / quarterly?
4. Any standing committees? (Audit, Compensation, Strategy)
5. Financial decision limit: how much can the CEO decide before the board must approve?

#### Suggested template
Structure:
- **Article I** — Scope & purpose
- **Article II** — Board composition: number, term, qualifications, election/removal
- **Article III** — Authority & responsibilities: list of powers, limits, reserved matters
- **Article IV** — Meetings: notice, agenda, quorum, voting, online meetings
- **Article V** — Standing committees: formation, duties, reporting
- **Article VI** — Relationship with executives: oversight, delegation, financial limits
- **Article VII** — Disclosure & conflicts of interest
- **Appendix**: a financial-authority table

Confirm the structure before generating.

#### File-generation prompt
```
Create Board of Directors Regulations.

CONTEXT:
- Entity type: [type] — Number of directors: [number] — Independent members: [Yes/No]
- Meeting frequency: [monthly/quarterly]
- Committees: [list if any]
- CEO financial limit: [amount]
- Basis: Texas Business Organizations Code (TBOC) + the company's formation documents

FORMAT:
- Articles with numbered sections
- Financial-authority table: decision type | CEO | CFO | Board | Members/Shareholders + dollar amount
- Reserved-matters list: decisions that MUST go to the board
- Decision workflow: Mermaid flowchart

TONE: Formal, internal, clear.
LENGTH: 8-12 pages.

NOTE: General information, not legal advice.
```

---
✍️ Author: Brian H. Doan
