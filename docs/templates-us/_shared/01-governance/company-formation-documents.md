# PROMPT 01: Company Formation Documents (Certificate of Formation + Company Agreement / Bylaws)

#### Description
The foundational legal documents that govern how the company is organized and operated. Under the **Texas Business Organizations Code (TBOC)**, a domestic entity is created by filing a **Certificate of Formation** with the Texas Secretary of State; internal governance is set by a **Company Agreement** (LLC) or **Bylaws** (corporation). This file produces a standard set, customized to the entity type and the company's specifics. General information only — not legal advice.

#### Information to collect (ask the user before generating)
1. Entity type? (single-member LLC / multi-member LLC / corporation / partnership / sole proprietorship + DBA)
2. Ownership? (LLC membership interests / corporate shares — and each owner's percentage)
3. Primary line of business? (NAICS code)
4. Management structure? (member-managed vs. manager-managed LLC / board of directors + officers for a corporation)
5. Any special provisions? (e.g. equity vesting, veto rights, transfer restrictions / buy-sell)
6. Does the company have existing documents to update, or is this a brand-new formation?

#### Suggested template
Standard structure under the TBOC:
- **Article I** — General provisions: name, registered office/agent, purpose, NAICS line of business
- **Article II** — Members/Shareholders: rights, obligations, capital contributions, transfer restrictions
- **Article III** — Management: member/manager (LLC) or board of directors + officers (corporation)
- **Article IV** — Meetings & decisions: notice, quorum, voting *(note: a single-member LLC has no meeting requirement)*
- **Article V** — Finances: fiscal year, profit distributions, reserves
- **Article VI** — Dissolution, winding up, reorganization
- **Article VII** — Miscellaneous / execution

Confirm the structure before generating.

#### File-generation prompt
```
Create company formation documents for the business.

CONTEXT:
- Entity type: [single-member LLC / multi-member LLC / corporation / partnership]
- Ownership: [each owner's % — LLC membership interest or corporate shares]
- Line of business: [NAICS code + description]
- Management: [member-managed / manager-managed / board + officers]
- Special provisions: [list]
- Legal basis: Texas Business Organizations Code (TBOC); filed with the Texas Secretary of State

FORMAT:
- Clear articles, continuously numbered sections (Section 1, 2, 3...)
- Standard but readable legal language
- Highlight customized (non-standard) provisions with [NOTE]
- Footer: "These documents are effective as of the date of execution"
- Signature block: all founding members/shareholders

TONE: Formal, legal, serious.
LENGTH: 10-20 pages depending on entity type.

NOTE: This is a reference template only. The company MUST have a licensed Texas attorney review it
before official use. General information, not legal advice.
```

---
✍️ Author: Brian H. Doan
