### PROMPT 09: Data Backup SOP

#### Description
A data backup and recovery process — backup schedule, method (full/incremental/differential), storage location, periodic restore testing, and RPO/RTO per system.

#### Information to collect (ask the user before generating)
1. Which systems/data need backup? (database, files, email, code, configs)
2. Current backup: automated or manual? What tool?
3. Storage: local / cloud / both? Capacity?
4. Ever needed a restore? Result?
5. Desired RPO? (max data loss: 1 hour / 1 day)
6. Desired RTO? (recover within: 1 hour / 4 hours / 1 day)

#### Suggested template
Structure:
- **Purpose & scope**
- **Data classification**: criticality levels — Critical / Important / Normal
- **Backup Schedule**: table system × frequency × method × retention
- **Backup Procedure**: step-by-step per backup type
- **Storage & Rotation**: Primary / Secondary / Offsite — 3-2-1 rule
- **Restore Procedure**: step-by-step recovery + timeline
- **Disaster Recovery Test**: test frequency, checklist, results report
- **RPO/RTO Matrix**: system × RPO × RTO × current capability × gap
- **Appendix**: backup-log template, restore-test report template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Data Backup SOP.

CONTEXT:
- Company: [Name] — Systems to back up: [list]
- Backup tool: [name]
- Storage: [local / cloud / hybrid] — Capacity: [GB/TB]
- RPO target: [time] — RTO target: [time]
- Restore history: [Yes/No]

FORMAT:
- Data classification: table System | Data type | Criticality | RPO | RTO
- Backup schedule: System | Method (Full/Incr/Diff) | Frequency | Time | Retention | Storage
- 3-2-1 rule diagram: 3 copies × 2 media × 1 offsite
- Backup procedure: step-by-step per system — numbered steps
- Restore procedure: step-by-step — numbered steps + estimated time
- DR test checklist: 10-15 items ☐ + Scenario | Expected | Actual | Pass/Fail
- RPO/RTO dashboard: System | Target RPO | Actual RPO | Target RTO | Actual RTO | Status 🟢🟡🔴
- Backup log: Date | System | Type | Size | Duration | Status | Operator

TONE: Technical SOP, clear, testable.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
