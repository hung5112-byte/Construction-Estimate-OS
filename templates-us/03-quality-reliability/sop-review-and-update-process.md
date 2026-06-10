### PROMPT 13: SOP Review & Update Process

#### Description
A meta-SOP — the process to manage, review, and update all SOPs in the company. Ensures SOPs stay current, reflect real operations, have version control, and are reviewed periodically.

#### Information to collect (ask the user before generating)
1. How many SOPs currently? Stored where? (Notion / Drive / SharePoint / hard copy)
2. SOP-review frequency? (6 months / 1 year / on change)
3. Who can edit an SOP? Change-approval process?
4. A version-control system? (v1.0, v1.1...)
5. An audit trail for changes?
6. When does an SOP get retired/archived?

#### Suggested template
Structure:
- **Purpose & scope** — applies to EVERY SOP, POL, MAN, FRM in the company
- **SOP Inventory**: a list of all SOPs — ID, name, owner, version, last review, next review
- **Review Schedule**: review calendar — which SOP is reviewed when
- **Trigger-based Review**: what events trigger an off-schedule review? (incident, audit finding, law change)
- **Review & Update Process**: flowchart — Trigger → Draft changes → Review → Approve → Publish → Train → Archive old
- **Version Control**: versioning rules, changelog format
- **Distribution & Training**: how to announce new/updated SOPs, train affected staff
- **Retirement**: when to retire, archive process, retention period

Confirm the structure before generating.

#### File-generation prompt
```
Create an SOP Review & Update Process.

CONTEXT:
- Company: [Name] — # SOPs: [number] — Storage: [platform]
- Review frequency: [6 months / 1 year]
- Who edits SOPs: [SOP owner / centralized team]
- Version control: [Yes/No]

FORMAT:
- SOP inventory template: SOP ID | Name | Category | Owner | Version | Effective date | Last review | Next review | Status
- Review calendar: 12 months × SOP list → highlight review months
- Review trigger list: Event | Type (Scheduled/Triggered) | Action | Owner
- Update flowchart: Mermaid — Trigger → Draft → Peer Review → Approve → Publish → Notify → Train → Archive
- Version control rules: Major (v1→v2) vs. Minor (v1.0→v1.1) | changelog format
- Change log template: Version | Date | Section | Change description | Changed by | Approved by
- Distribution checklist: ☐ Update master | ☐ Notify users | ☐ Remove old version | ☐ Train if needed | ☐ Update training materials
- Retirement criteria: Conditions | Archive location | Retention period | Approver

TONE: Meta-SOP — structured, governance-focused.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
