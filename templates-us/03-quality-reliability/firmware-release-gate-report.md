# P-QR-04: Firmware Release Gate Report

#### Description
Firmware QA's verdict on a release candidate — regression results, OTA-path testing including power-loss and rollback, defect list with honest severities, and a pass/conditional/fail gate. The release plan proposes; this report disposes.

#### Information to collect (ask the user before generating)
1. Release version and the release plan it gates? (link)
2. Regression scope executed? (suites, platforms, from-versions)
3. OTA-path results? (every fleet from-version, power-loss-mid-update, rollback)
4. Open defects with severities?
5. Soak status? (duration, units, anomalies)

#### Suggested template
Structure:
- **Header**: version, candidate build, gate date, tester(s), release-plan link
- **Coverage table**: suite, platform/HW rev, from-version, result, evidence link
- **OTA-path table**: from→to per fleet version, normal update, power-loss test, rollback test — all explicit
- **Soak**: units, duration, anomalies with disposition
- **Defects**: ID, severity (honest — a severity downgraded for schedule is a field incident scheduled), disposition (fix-before-ship / ship-with / reject)
- **Verdict**: PASS / CONDITIONAL (dated conditions) / FAIL (required fixes)
- **Escape clause**: every field escape from this release becomes a permanent regression test

Confirm the structure before generating.

#### File-generation prompt
```
Create a Firmware Release Gate Report.

CONTEXT:
- Version: [x.y.z] — Plan: [link] — Regression: [scope run]
- Fleet from-versions: [list] — Defects: [list w/ severity] — Soak: [status]

FORMAT:
- Header; coverage table; OTA-path matrix (incl. power-loss + rollback columns);
  soak summary; defect disposition table; verdict block; escape clause

RULES: an untested fleet from-version fails the gate by definition;
ship-with defects are listed in the verdict, not buried; rollback untested = FAIL.
```

---
✍️ Author: Brian H. Doan
