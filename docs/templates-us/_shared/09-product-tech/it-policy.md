### PROMPT 07: IT Policy

#### Description
A policy governing the use of technology devices, software, email, internet, and data in the business. Includes BYOD, acceptable use, data classification, and employee responsibilities. The foundation for information security and compliance.

#### Information to collect (ask the user before generating)
1. Does the company issue devices, or BYOD (employees use personal machines)?
2. A dedicated email domain? Email-use rules?
3. Internet policy? (filter / monitor / open)
4. Sensitive data? (customer, financial, HR — needs classifying)
5. Remote work? Remote-access policy?
6. Software: free to install, or must go through IT approval?

#### Suggested template
Structure:
- **Articles 1-3** — Purpose, scope, glossary
- **Article 4** — Devices & hardware: issuance, care, return on exit, BYOD
- **Article 5** — Software: allowed list, installation, license, no cracked/pirated software
- **Article 6** — Email & communication: company email use, email signature, retention
- **Article 7** — Internet: acceptable use, restricted sites, monitoring notice
- **Article 8** — Data classification: Public / Internal / Confidential / Restricted
- **Article 9** — Remote access: VPN, MFA, approved devices
- **Article 10** — Incident reporting: IT incidents, lost devices, data breach
- **Article 11** — Violations
- **Appendix**: IT-use acknowledgment, approved-software list

Confirm the structure before generating.

#### File-generation prompt
```
Create an IT Policy.

CONTEXT:
- Company: [Name] — Headcount: [number] — Remote: [Yes/No]
- Devices: [Company-issued / BYOD / Hybrid]
- Email domain: [Yes/No] — Provider: [Google Workspace / M365 / other]
- Sensitive data: [type]
- Internet: [filter / monitor / open]

FORMAT:
- Continuously numbered articles, clear language for all employees
- Data classification matrix: Level | Definition | Examples | Handling | Storage | Sharing
- BYOD requirements: table device standard | OS version | Security apps | Enrollment
- Software whitelist: table Category | Approved tools | Banned alternatives
- Email signature template: standardized format
- Incident reporting flowchart: Mermaid — Detect → Report → Classify → Handle → Review
- Acknowledgment form: signed by each employee

TONE: Clear, readable for non-tech, with concrete examples.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
