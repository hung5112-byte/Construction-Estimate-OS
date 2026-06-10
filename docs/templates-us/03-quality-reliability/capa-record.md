# P-QR-01: CAPA Record

#### Description
A corrective/preventive action record — from problem statement through root cause to verified closure. A CAPA closed without before/after data will reopen; this record makes that impossible to hide.

#### Information to collect (ask the user before generating)
1. The trigger? (audit finding, escape, field trend, SCAR escalation, gate failure)
2. Problem statement with data? (what, where, how many, rate)
3. Containment already in place?
4. Suspected ownership? (design / process / supplier / documentation / training)
5. Verification metric — what number must move to prove closure?

#### Suggested template
Structure:
- **Header**: CAPA ID, source/trigger reference, owner, open date, due dates per phase
- **Problem statement**: condition → consequence, with the data (counts AND rates)
- **Containment**: immediate actions, scope covered (WIP/transit/stock/field), effectivity
- **Root cause**: method used (5-Why/fishbone/8D ref), the process-level cause —
  "operator error" and "retrained" are not root causes
- **Corrective action**: the process/design/document change, implementation evidence
- **Preventive action**: where else this cause lives; systemic fix
- **Verification**: the metric, baseline, target, observation window, actual result
- **Closure**: verified-by, date; recurrence rule (same cause reopens at higher severity)

Confirm the structure before generating.

#### File-generation prompt
```
Create a CAPA Record.

CONTEXT:
- Trigger: [source + reference] — Problem: [statement w/ data]
- Containment: [state] — Verification metric: [number that must move]

FORMAT:
- Header with phase due dates; problem statement (rates, not just counts)
- Containment scope table; root cause with method and escape analysis
- Corrective + preventive actions with evidence; verification table
  (baseline → target → actual); closure + recurrence rule

RULES: no closure without verification data over the stated window;
root cause must be at process level; recurrence reopens, never re-files.
```

---
✍️ Author: Brian H. Doan
