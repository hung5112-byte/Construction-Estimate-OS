# PROMPT 05: Board Meeting Minutes Template

#### Description
A standardized template for board / member meeting minutes. Ensures every meeting is recorded in the proper format with the required content under the Texas Business Organizations Code (TBOC). (A single-member LLC generally has no meeting requirement, but minutes are still good governance.) General information only — not legal advice.

#### Information to collect (ask the user before generating)
1. Entity type? (corporation vs. LLC have different minute rules)
2. Number of directors / managers / members?
3. Is there a dedicated corporate secretary?
4. How many items/decisions per meeting typically?
5. Need bilingual minutes? (for a company with foreign owners)

#### Suggested template
Structure:
- **Header**: Logo, company name, EIN, "MINUTES OF THE [BOARD / MEMBERS] MEETING"
- **Meeting info**: minutes #, date/time, location (or online), chair, secretary
- **Attendance**: table: Name | Title | Ownership/voting % | Present ☐
- **Agenda items**: each with: presentation | discussion | vote | result
- **Resolutions**: numbered, clearly worded, % in favor
- **Dissents** (if any)
- **Signatures**: chair + secretary + attendees (if required)

Confirm the structure before generating.

#### File-generation prompt
```
Create a board / member meeting minutes template.

CONTEXT:
- Entity type: [type] — Meeting type: [board / members / shareholders]
- Number of directors/members: [number]
- Bilingual: [Yes/No]
- Legal basis: Texas Business Organizations Code (TBOC), Section [applicable section] [UNCERTAIN — verify]

FORMAT:
- Form template: fill-in fields marked [___]
- Professional header: logo placeholder, company info, EIN
- Attendance table: Name | Title | voting % | Present/Proxy
- Each item: # | Item | Presenter | Vote result (For __ / Against __ / Abstain __)
- Footer: chair & secretary signatures, a legal-confirmation line
- Appendix: checklist of required content

TONE: Legal-administrative, formal.
LENGTH: 3-4 pages.

NOTE: General information, not legal advice.
```

---
✍️ Author: Brian H. Doan
