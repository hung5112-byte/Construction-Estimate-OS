# P-SVC-05: Field Escalation Log

#### Description
The tracked log of field issues escalated from deployed sites — triage lane, resolution time, and the pattern detection that turns repeated site pain into a quality signal. Every escalation lands in exactly one lane: swap, repair, firmware, or site-environment.

#### Information to collect (ask the user before generating)
1. Intake channels? (customer calls, monitoring alerts, deployment techs)
2. Triage lanes and their owners? (swap from spares / RMA repair / firmware investigation / site issue)
3. Response/resolution targets per severity?
4. Fleet monitoring available? (device logs/telemetry pullable remotely)
5. Output format? (.xlsx log + a weekly summary recommended)

#### Suggested template
Structure (.xlsx):
- **Sheet "Log"**: ID, date, site/customer, device serial(s), symptom, severity
  (site-down / degraded / single-device / cosmetic), evidence pulled (logs? fault codes?),
  triage lane, owner, response time, resolution, closed date
- **Sheet "Patterns"**: repeat offenders — by site (environment issue?), by device cohort
  (escalate to field-quality), by symptom (firmware candidate?)
- **Sheet "SLA"**: response/resolution vs. targets per severity
- **Weekly summary block**: new/closed/aging, the one pattern worth a sentence, handoffs
  made (cohort signals → field-quality-rma-fa, firmware suspicions → firmware-qa)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Field Escalation Log workbook (.xlsx).

CONTEXT:
- Channels: [list] — Lanes/owners: [swap/repair/firmware/site → names]
- Severity targets: [response/resolution per level] — Telemetry: [available?]

FORMAT (.xlsx):
- "Log" with evidence and lane columns; "Patterns" (site/cohort/symptom repeats)
- "SLA" vs. targets; weekly summary block with handoffs

RULES: device evidence (logs/fault codes) is pulled before triage, not after;
three repeats of anything is a pattern with a handoff; site-down severity has
an hours-scale response target.
```

---
✍️ Author: Brian H. Doan
