# P-NPI-04: Certification Project Plan

#### Description
The execution plan for one certification program (PCI PTS, EMVCo L1/L2, FCC, UL/IEC, CE) — lab engagement, samples, schedule, cost, and the dependencies that put certification on the NPI critical path from day one. [Scheme requirements change — verify current versions with the lab.]

#### Information to collect (ask the user before generating)
1. Which certification/scheme and version? Target market?
2. Product and hardware/firmware configuration to be evaluated?
3. Lab selected or candidates? Prior quotes?
4. Sample requirements? (count, configuration, who builds them, by when)
5. The launch date this certification gates?

#### Suggested template
Structure:
- **Header**: scheme + version [verify with lab], product/config, lab, owner
- **Scope**: what is evaluated; reuse from prior approvals (deltas only?)
- **Schedule table**: milestone (pre-scan, sample delivery, evaluation start, report, approval), date, dependency — mapped against the NPI plan
- **Samples plan**: count, exact configuration (HW rev + FW version + keys), build source, delivery date
- **Cost**: lab fees, samples, travel/witnessing [quote-based]
- **Risk table**: failure modes (pre-scan fail, queue slip, change during evaluation) with mitigations
- **Change freeze**: what cannot change during evaluation without restart — communicated to BOM/ECO/PLM
- **Evidence handling**: where reports/certificates land (QMS), renewal entry in the certification tracker

Confirm the structure before generating.

#### File-generation prompt
```
Create a Certification Project Plan.

CONTEXT:
- Scheme: [PCI PTS x.x / EMVCo / FCC / UL] [verify version] — Product: [model + config]
- Lab: [name/candidates] — Launch gated: [date] — Samples: [n, config]

FORMAT:
- Header; scope incl. reuse; milestone table tied to NPI dates
- Samples plan; cost table; risk table; change-freeze notice;
  evidence/renewal handoffs

RULES: the schedule shows the lab queue as a real dependency; the change freeze
is explicit and sent to change control; sample configurations are exact, not "latest".
```

---
✍️ Author: Brian H. Doan
