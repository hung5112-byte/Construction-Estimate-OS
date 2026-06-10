# P-HWE-06: OTA Rollout Plan

#### Description
The execution plan for pushing a released firmware to the installed fleet — wave design, monitoring, abort criteria, and customer communication. The update path is the most dangerous code path; this plan treats it that way.

#### Information to collect (ask the user before generating)
1. Release version (must have a passed gate report) and fleet size?
2. Fleet segmentation? (by customer, site, hardware rev, current version)
3. Canary selection — which devices/sites and why them?
4. Monitoring signals? (check-in rate, failure codes, DOA reports, support tickets)
5. Customer notification requirements? (managed sites vs. silent update policy)

#### Suggested template
Structure:
- **Preconditions**: gate report passed [link], rollback tested, support briefed
- **Wave plan table**: wave, population (count/segment), start, soak time, advance criteria
- **Monitoring**: signal, source, healthy threshold, who watches, check frequency
- **Abort criteria**: explicit numbers (e.g. update-failure rate > X%, new fault code spike) → halt + rollback decision owner
- **Rollback procedure**: how, how long, device-state implications
- **Communication**: who is told what, before and after (customers, support, deployment)
- **Completion**: fleet coverage target, stragglers plan (offline devices), closure report

Confirm the structure before generating.

#### File-generation prompt
```
Create an OTA Rollout Plan.

CONTEXT:
- Version: [x.y.z] — Fleet: [n devices, segments] — Canary: [selection]
- Monitoring sources: [list] — Notification policy: [managed/silent]

FORMAT:
- Preconditions checklist; wave table with advance criteria
- Monitoring table; numeric abort criteria with decision owner
- Rollback procedure; communication matrix; completion criteria

RULES: abort criteria are numbers decided before wave 1, not judgment calls
during it; the rollback owner is named; offline-device stragglers get a plan.
```

---
✍️ Author: Brian H. Doan
