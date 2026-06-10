### PROMPT 15: Incident Management SOP

#### Description
A process to handle every kind of incident — from IT down, power loss, or an accident, to a serious customer complaint. Severity classification, escalation path, handling, reporting, and root-cause analysis.

#### Information to collect (ask the user before generating)
1. Most common incident type? (IT / safety / customer / operations / finance)
2. How many escalation levels currently?
3. An on-call / shift-coverage team?
4. Desired response time for a serious incident? (15 min / 1 hour / 4 hours)
5. Ever had a major incident? Lessons learned?
6. An incident-management tool? (Jira, Freshdesk, Excel...)
7. Who is the final decision-maker for a serious incident?

#### Suggested template
Structure:
- **Severity classification**: Severity 1 (Critical) → 2 (High) → 3 (Medium) → 4 (Low) + examples
- **Escalation matrix**: severity × response time × resolver × escalate to × notify
- **Handling process**: detect → classify → notify → handle → remediate → report
- **Incident report template**: a standard incident report form
- **Root Cause Analysis**: 5 Whys + Fishbone diagram guide
- **Post-incident review**: a post-incident review checklist
- **Preventive actions**: a preventive-action register

Confirm the structure before generating.

#### File-generation prompt
```
Create an Incident Management SOP.

CONTEXT:
- Company: [Name] — Common incident type: [IT / safety / customer / operations]
- # escalation levels: [3-4]
- On-call: [Yes/No]
- Response-time target: [time]

FORMAT:
- Severity classification: Severity 1-4 + examples
- Escalation matrix: Severity | Response time | Resolver | Escalate to | Notify
- Flowchart: Mermaid — Detect → Classify → Handle → Remediate → RCA → Preventive
- Incident report template: Time | Description | Severity | Impact | Root Cause | Action | Owner | Status
- RCA template: 5 Whys + Fishbone diagram guide
- Post-incident review: 8-question checklist
- Preventive-action log: Action | Owner | Due | Status

TONE: Urgent, clear, action-oriented.
LENGTH: 5-7 pages.
```

---
✍️ Author: Brian H. Doan
