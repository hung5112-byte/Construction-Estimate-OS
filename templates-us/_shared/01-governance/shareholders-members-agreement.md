# PROMPT 04: Shareholders / Members Agreement

#### Description
A legal document supplementing the formation documents, governing the relationship among shareholders/members in detail: vesting, exit mechanism, anti-dilution, drag-along, tag-along, deadlock resolution. Especially important for startups and companies with multiple owners. General information only — not legal advice.

#### Information to collect (ask the user before generating)
1. How many shareholders/members? Each one's ownership %?
2. Is any owner a financial investor (non-operating)?
3. A vesting schedule for founders/key people? (e.g. 4 years, 1-year cliff)
4. Plans to raise more capital? (affects the anti-dilution clause)
5. Deadlock resolution: which mechanism? (Russian roulette / Texas shoot-out / mediation)
6. Is there an existing shareholders agreement?

#### Suggested template
Structure:
- **Part 1** — Parties, definitions, term glossary
- **Part 2** — Contributions & equity: percentages, schedule, vesting
- **Part 3** — Governance & decisions: members/shareholders, board, veto rights, reserved matters
- **Part 4** — Transfers: ROFR, tag-along, drag-along, lock-up period
- **Part 5** — Anti-dilution: full ratchet / weighted average
- **Part 6** — Exit & deadlock: buy-out, IPO, dissolution, deadlock resolution
- **Part 7** — Non-compete, non-solicitation, confidentiality
- **Part 8** — General: governing law (Texas), dispute resolution, effectiveness

Confirm the structure before generating.

#### File-generation prompt
```
Create a Shareholders / Members Agreement.

CONTEXT:
- Company: [Name] — Entity type: [type]
- Shareholders/members: [Name - % - role (operating/financial)]
- Vesting: [Yes/No] — Schedule: [detail]
- Capital-raise plans: [Yes/No]
- Deadlock mechanism: [Russian roulette / Texas shoot-out / mediation]

FORMAT:
- Clear parts, continuously numbered sections
- Owner summary table: name | % | equity class | role | vesting status
- Plain English for important terms (define on first use)
- Appendix: vesting schedule, reserved-matters list, cap-table template

TONE: Formal, legal, tight.
LENGTH: 12-20 pages.

NOTE: Reference template — MUST be reviewed by a licensed Texas attorney before signing. Not legal advice.
```

---
✍️ Author: Brian H. Doan
