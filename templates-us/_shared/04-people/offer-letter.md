# P-PPL-14: Offer Letter

#### Description
A professional offer-letter template — sent to the selected candidate. Includes title, pay, benefits, start date, contingencies, and a response deadline. This is the first formal impression for a future employee. General information only — not legal advice; have an employment attorney review the at-will and contingency language.

#### Information to collect (ask the user before generating)
1. Standard letterhead/branding?
2. Required elements? (pay, start date, who they report to)
3. Any contingencies? (background check, references, drug test if applicable, employment-eligibility verification)
4. Offer response deadline: how many days?
5. Who signs the offer? (Owner / HR Manager)

> US legal note: a US offer letter should (1) state the position is **at-will** (either party may end employment at any time, with or without cause — Texas default), (2) state whether the role is **exempt or non-exempt** under the FLSA, (3) note the offer is **contingent on employment-eligibility verification (Form I-9)** under 8 U.S.C. §1324a, and (4) make clear the letter is not an employment contract for a fixed term. US pay is typically stated as an annual salary or hourly rate (not "gross/net").

#### Suggested template
Structure:
- **Header**: Logo + "OFFER OF EMPLOYMENT"
- **Welcome**: a personalized congratulations
- **Position details**: title, department, reports to, start date, exempt/non-exempt status
- **Compensation**: annual salary or hourly rate, pay frequency, variable/bonus if any
- **Benefits summary**: top benefits offered
- **Contingencies**: background check, references, Form I-9 employment eligibility
- **At-will statement**: clear at-will language; letter is not a fixed-term contract
- **Response deadline**: a specific date
- **Signatures**: Owner/HR Manager + candidate acceptance
- **Appendix**: documents to bring day one (I-9 documentation), handbook acknowledgment, NDA

Confirm the structure before generating.

#### File-generation prompt
```
Create an Offer Letter template.

CONTEXT:
- Company: [Name]
- Signer: [Owner / HR Manager]
- Contingencies: [background check / references / I-9 / drug test]
- Response deadline: [days]
- Attachments: [Handbook acknowledgment / JD / NDA]
- Authority: at-will employment (Texas); FLSA exempt/non-exempt (29 U.S.C. §213); Form I-9 employment eligibility (8 U.S.C. §1324a)

FORMAT:
- Header: Logo + company info + "OFFER OF EMPLOYMENT"
- Body: Congratulations → Position & department → Start date → Exempt/non-exempt → Compensation (annual salary or hourly rate, pay frequency) → Benefits highlights → Contingencies → At-will statement → Response deadline
- Attachment checklist: documents to bring day one (including I-9 documents)
- Acceptance section: "I accept the position of..." + candidate signature + date
- Signature: Name + Title + Company

TONE: Professional yet warm — make the new hire excited.
LENGTH: 2 pages.

NOTE: General information, not legal advice. Have a licensed Texas employment attorney review the at-will and contingency language.
```

---
✍️ Author: Brian H. Doan
