### PROMPT 01: Reporting Policy & Standards

#### Description
A policy governing the whole reporting system — report types, frequency, standard format, deadlines, each function's responsibility, the approval process, and data-quality standards. The "rules of the game" for reporting — ensuring information is correct, complete, on time, and to the right person.

#### Information to collect (ask the user before generating)
1. How many report types today? (daily / weekly / monthly / quarterly / annual)
2. Who receives reports? (CEO / leadership / Board / shareholders / regulators)
3. Current format: free-form or templated? What tool? (Excel / Google Sheets / BI tool / ERP)
4. Main problem: numbers don't match / late reports / inconsistent format / too many reports?
5. Audit requirements? (internal / external CPA / regulatory)
6. Report-data confidentiality policy?

#### Suggested template
Structure:
- **Articles 1-3** — Purpose, scope, glossary
- **Article 4** — Report classification: Operational / Financial / Strategic / Compliance / Ad-hoc
- **Article 5** — Reporting calendar: table type × frequency × deadline × owner × audience
- **Article 6** — Format & template standards: standardized header, structure, visualization
- **Article 7** — Data-quality standards: accuracy, completeness, timeliness, consistency
- **Article 8** — Review & approval process: who approves, approval timeline
- **Article 9** — Distribution & confidentiality: who receives, channel, classification
- **Article 10** — Archive & retention: storage, retention period, retrieval
- **Article 11** — Exception reporting: abnormal reports, triggers, escalation
- **Article 12** — Violations
- **Appendix**: reporting-calendar master, report cover-page template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Reporting Policy & Standards.

CONTEXT:
- Company: [Name] — Headcount: [number] — # departments: [number]
- Report types: [daily / weekly / monthly / quarterly / annual]
- Audience: [CEO / leadership / Board / shareholders / regulators]
- Tool: [Excel / Google Sheets / BI tool / ERP]
- Main problem: [wrong numbers / late / messy format / too many]
- Audit: [internal / external CPA / regulatory]

FORMAT:
- Continuously numbered articles
- Report classification: table Type | Description | Frequency | Deadline | Owner | Audience | Confidentiality
- Reporting calendar: 12-month master calendar — Type | Jan | Feb | ... | Dec — highlight deadlines
- Template standards:
  - Header: Logo | Report name | Period | Version | Author | Date | Classification
  - Structure: executive summary → KPIs → detail → variance analysis → action items
  - Visualization rules: chart types per data type, color coding, annotation standards
- Data-quality checklist: ☐ Accuracy | ☐ Completeness | ☐ Timeliness | ☐ Consistency | ☐ Source verified
- Approval workflow: Mermaid — Data owner → Reviewer → Approver → Distribution
- Exception reporting: Trigger | Threshold | Escalation path | Response time
- Archive matrix: Report type | Retention period | Storage | Access | Destruction method

TONE: Governance-level, clear, enforces compliance.
LENGTH: 6-10 pages.
```

---
✍️ Author: Brian H. Doan
