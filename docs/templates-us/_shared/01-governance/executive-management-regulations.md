# PROMPT 08: Executive Management Regulations

#### Description
The operating rules for the executive team (Department Head, VPs, functional directors). Governs assignments, delegation, decision limits, and coordination among executives.

#### Information to collect (ask the user before generating)
1. How many executives? Specific titles?
2. Does the Department Head also chair the board? (combined roles?)
3. Each VP's area of responsibility?
4. Financial sign-off limit for each executive level?
5. Delegation process when someone is absent?

#### Suggested template
Structure:
- **Sections 1-3** — Scope, purpose, terms
- **Sections 4-6** — Executive structure: composition, appointment, removal
- **Sections 7-10** — Rights & responsibilities: Department Head, VPs, functional directors — one section each
- **Sections 11-13** — Decision authority: a detailed table by decision type × executive level
- **Sections 14-15** — Executive meetings: frequency, agenda, minutes
- **Sections 16-17** — Delegation & cover when absent
- **Section 18** — Reporting to the board
- **Appendix**: a sign-off authority table

Confirm the structure before generating.

#### File-generation prompt
```
Create Executive Management Regulations.

CONTEXT:
- Executives: [list titles + names]
- Department Head also chairs the board: [Yes/No]
- Assignments: [e.g. VP Sales owns Sales+Marketing, VP Operations owns Ops+HR]
- Sign-off limits: Department Head [amount] | VP [amount] | functional director [amount]

FORMAT:
- Continuously numbered sections
- Authority table: decision type | functional director | VP | Department Head | Board
- Delegation table: delegator | delegate | scope | duration
- Reporting diagram: Mermaid org chart

TONE: Internal, formal.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
