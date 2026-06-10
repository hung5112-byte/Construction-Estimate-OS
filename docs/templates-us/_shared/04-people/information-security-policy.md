# P-PPL-10: Information Security Policy

#### Description
A policy for information classification, security rules, access rights, and handling security incidents. Complements the NDA in 01-Governance — the NDA is the legal commitment; this is the daily behavioral rulebook for security.

#### Information to collect (ask the user before generating)
1. Information classification: how many levels? (e.g. Public / Internal / Confidential / Secret)
2. Sensitive data: customer, financial, technology, HR — which matters most?
3. BYOD (Bring Your Own Device) policy: allowed?
4. Social media: can employees post about the company? Rules?
5. Process when a leak/breach is discovered?
6. A DPO (Data Protection Officer) or dedicated IT security?

#### Suggested template
Structure:
- **Part 1** — Purpose, scope, definitions
- **Part 2** — Information classification: 4 levels + examples + handling for each
- **Part 3** — Access rights: a Role × Information-type matrix → access level
- **Part 4** — Daily security rules: passwords, lock screen, clean desk, file sharing
- **Part 5** — BYOD & personal devices: allowed/not, conditions
- **Part 6** — Social media: what can / can't be said about the company
- **Part 7** — Security incident response: detect → report → contain → investigate → remediate (note: a breach of personal data may trigger notification under Texas Business & Commerce Code ch. 521 [verify])
- **Part 8** — Violations & consequences: warning → discipline → termination → legal

Confirm the structure before generating.

#### File-generation prompt
```
Create an Information Security Policy.

CONTEXT:
- Company: [Name] — Industry: [industry] — Headcount: [number]
- Classification: [Public / Internal / Confidential / Secret]
- Most sensitive data: [Customer / Financial / Technology / HR]
- BYOD: [Allowed / Not / Conditional]
- DPO/IT Security: [Yes/No]
- Linked to: the NDA in 01-Governance

FORMAT:
- Classification matrix: Level | Definition | Examples | Who can access | Storage | Sharing | Disposal
- Access control: Role × Info type = Read/Write/None — matrix table
- Daily security rules: 10 rules — poster-friendly
- BYOD rules: Device | Allowed | Conditions | MDM required
- Social media dos/don'ts: 5 do + 5 don't
- Incident response flowchart: Mermaid — Detect → Notify IT → Contain → Owner → Investigate → Report (+ Texas ch. 521 breach-notice check)
- Violation penalties: table Violation | Level 1 (warn) | Level 2 (discipline) | Level 3 (termination/legal)

TONE: Serious, security-minded, but readable for non-tech staff.
LENGTH: 6-8 pages.

CROSS-REFERENCE: This is the security rulebook for staff. For the legal data-protection policy see bb-governance/Data Protection Policy (TDPSA). For technical cybersecurity see bb-product-tech/Cybersecurity Policy.
```

---
✍️ Author: Brian H. Doan
