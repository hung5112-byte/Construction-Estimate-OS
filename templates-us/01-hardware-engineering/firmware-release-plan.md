# P-HWE-05: Firmware Release Plan

#### Description
The plan for one firmware release — scope, gates, factory impact, and rollback strategy. Written by the FW/Embedded team, gated by Firmware QA. A release without a tested rollback path is not a release.

#### Information to collect (ask the user before generating)
1. Release version and products/hardware revisions it targets?
2. Scope? (features, fixes — with the field issues they close, if any)
3. Fleet reality: which from-versions exist in the field?
4. Factory impact? (new production firmware, provisioning changes)
5. Security relevance? (anything touching boot, keys, payment paths → certification check)

#### Suggested template
Structure:
- **Header**: version, target HW revisions, owner, target date
- **Scope table**: change, type (feature/fix), linked issue/8D, risk
- **Compatibility**: supported update paths (from-version × to-version), migration steps
- **Gates**: regression scope, soak duration, OTA-path test incl. power-loss + rollback — pass criteria per gate [owned by firmware-qa]
- **Factory plan**: production firmware cut-in (build/lot), provisioning changes, golden unit update
- **Rollout**: canary wave size/duration, full-fleet criteria, abort criteria, rollback procedure
- **Certification check**: security-relevant? written verdict [from certification]
- **Handoffs**: gate report (firmware-qa), cut-in (odm-program-mgmt + bom-eco-plm), fleet staging (deployment-support)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Firmware Release Plan.

CONTEXT:
- Version: [x.y.z] — Targets: [HW revs] — Fleet from-versions: [list]
- Scope: [changes] — Factory impact: [yes/no detail] — Security-relevant: [yes/no]

FORMAT:
- Header; scope table with linked issues; compatibility matrix
- Gate table (gate, scope, pass criteria, owner)
- Factory cut-in plan; staged rollout with canary/abort/rollback
- Certification verdict line; handoff list

RULES: every fleet from-version appears in the update-path test matrix;
no fleet-wide rollout without a completed canary wave.
```

---
✍️ Author: Brian H. Doan
