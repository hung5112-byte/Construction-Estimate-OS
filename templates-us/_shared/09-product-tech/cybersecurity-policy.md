### PROMPT 08: Cybersecurity Policy

#### Description
An information-security and cybersecurity policy — passwords, access control, encryption, incident response, and compliance. Protects the business from data loss, cyberattacks, and violations of personal-data law. General information only — not legal advice; confirm data-privacy obligations with an attorney.

#### Information to collect (ask the user before generating)
1. Do you store customer data? What kind? (PII, payment, health...)
2. MFA (two-factor) in place? For which systems?
3. Ever been attacked / had a data breach?
4. A dedicated IT-security person?
5. Compliance requirements? (TDPSA / HIPAA / GLBA / PCI-DSS / ISO 27001)
6. Use cloud services? (AWS / GCP / Azure)

#### Suggested template
Structure:
- **Part 1** — Purpose, scope, glossary, references (NIST Cybersecurity Framework, ISO 27001)
- **Part 2** — Password policy: complexity, rotation, password manager
- **Part 3** — Access control: least privilege, role-based access, review cycle
- **Part 4** — Data protection: encryption at rest/in transit, data retention, deletion
- **Part 5** — Network security: firewall, VPN, Wi-Fi, segmentation
- **Part 6** — Endpoint security: antivirus, patching, device encryption
- **Part 7** — Incident response plan: Detection → Containment → Eradication → Recovery → Lessons learned (include breach-notification check under Tex. Bus. & Com. Code ch. 521)
- **Part 8** — Awareness & training: phishing tests, security-training frequency
- **Part 9** — Compliance: Texas Data Privacy and Security Act (TDPSA) [verify effective scope]; Tex. Bus. & Com. Code ch. 521 (breach notice); HIPAA (if health data); GLBA (if financial data); PCI-DSS (if card data)
- **Appendix**: incident-response checklist, security-awareness quiz, vendor security assessment

Confirm the structure before generating.

#### File-generation prompt
```
Create a Cybersecurity Policy.

CONTEXT:
- Company: [Name] — Customer data: [type] — Cloud: [provider]
- MFA: [Yes/No] — Systems: [list]
- IT Security: [dedicated / shared / outsourced]
- Compliance: [TDPSA / HIPAA / GLBA / PCI-DSS / ISO 27001]
- Incident history: [Yes/No]
- Authority/standards: NIST Cybersecurity Framework; ISO 27001; TDPSA; Tex. Bus. & Com. Code ch. 521 (breach notice); HIPAA/GLBA/PCI-DSS as applicable

FORMAT:
- Password matrix: System | Min length | Complexity | Rotation | MFA
- Access control matrix: Role | System A | System B | System C → CRUD permissions
- Incident response flowchart: Mermaid — 5 phases + timeline + breach-notice check (ch. 521)
- Data classification × Handling: matrix 4 levels × encryption/storage/sharing/disposal
- Security checklist: Monthly ☐ + Quarterly ☐ + Annual ☐ review items
- Compliance mapping: Requirement | Law/Standard | Current status | Gap | Action
- Training calendar: Topic | Audience | Frequency | Format | Owner

TONE: Professional, security-minded, with specific US law + international standards.
LENGTH: 8-12 pages.

NOTE: General information, not legal advice. Confirm data-privacy/breach obligations with a licensed attorney.

CROSS-REFERENCE: This is the technical cybersecurity policy. For the legal data-protection policy, see bb-governance/Data Protection Policy. For the staff information-security rulebook, see bb-people/Information Security Policy.
```

---
✍️ Author: Brian H. Doan
