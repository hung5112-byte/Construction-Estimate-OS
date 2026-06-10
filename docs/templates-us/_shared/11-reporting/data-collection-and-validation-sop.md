### PROMPT 06: Data Collection & Validation SOP

#### Description
A standardized process to collect, check, and validate data before it goes into reports. Ensures "garbage in, garbage out" doesn't happen. Includes data ownership, input standards, validation rules, reconciliation, and error handling.

#### Information to collect (ask the user before generating)
1. Main data sources? (ERP / CRM / spreadsheet / manual input / external)
2. Who enters data? (employees / managers / accounting / automated)
3. Common data problems? (duplicates / missing / wrong format / late / mismatched)
4. A data dictionary / data standards?
5. Current reconciliation process? (cross-check between systems)
6. Data-quality review frequency?

#### Suggested template
Structure:
- **Purpose & scope**
- **Data Ownership**: RACI per data type
- **Collection Standards**: format, units, naming convention, input deadline
- **Validation Rules**: automated checks, manual review, cross-system reconciliation
- **Error Handling**: detect → log → fix → verify → root cause → prevent
- **Data Quality Metrics**: accuracy, completeness, timeliness, consistency — KPIs
- **Review Process**: frequency, checklist, sign-off
- **Appendix**: data dictionary template, validation checklist, error-log template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Data Collection & Validation SOP.

CONTEXT:
- Company: [Name] — Data sources: [ERP / CRM / spreadsheet / manual]
- Entered by: [employees / managers / accounting / automated]
- Main problems: [duplicates / missing / wrong format / late / mismatched]
- Data dictionary: [Yes/No]
- Reconciliation: [current cross-check]

FORMAT:
- Data ownership matrix: table Data domain | Source system | Data owner | Data steward | Input by | Validate by
- Collection standards per data type:
  - Format: Date (MM/DD/YYYY) | Currency (USD, comma thousands, e.g. 1,250.00) | Text (Title Case) | Phone ((xxx) xxx-xxxx)
  - Naming convention: entity naming rules + examples
  - Input deadline: Data type | Source | Deadline | Frequency | Responsible
- Validation rules engine:
  - Automated: Rule | Check type (Range/Format/Uniqueness/Referential) | System | Action if fail
  - Manual: checklist ☐ per report — 10-15 items: Completeness | Accuracy | Consistency | Timeliness
  - Reconciliation: System A vs. System B | Metric | Tolerance | Frequency | Investigator
- Error-handling flowchart: Mermaid — Detect → Log → Classify (Critical/Major/Minor) → Fix → Verify → Root cause → Preventive action
- Error-log template: Date | Data domain | Error type | Description | Impact | Root cause | Fix | Fixed by | Verified by
- Data-quality scorecard: Dimension | Definition | Measurement | Target | Current | Status
  - Accuracy: % records without errors
  - Completeness: % required fields filled
  - Timeliness: % data submitted by deadline
  - Consistency: % cross-system matches
  - Uniqueness: % duplicate-free records
- Review calendar: monthly data-quality review | quarterly deep audit | annual data-governance review
- RACI per activity: Collect | Validate | Reconcile | Report | Fix errors | Set standards

TONE: Detailed SOP, data-governance-oriented.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
