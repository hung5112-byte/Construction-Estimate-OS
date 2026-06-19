# P-HWE-23: Firmware Test Plan (FW)

#### Description
A structured firmware test plan — unit, integration, HIL, regression, and field-failure reproduction — mapped to requirements and release gates.

#### Information to collect (ask the user before generating)
1. Firmware version and scope of changes?
2. Test levels available (unit, HIL rig, on-device, field)?
3. Critical functions (payment, OTA, power management, radios)?
4. Coverage targets and regression suite?
5. Known field failures to reproduce (e.g. battery-connector intermittency)?

#### Suggested template
Structure:
- Test matrix: requirement -> test case -> level -> pass criteria
- Critical-path tests: payment, OTA + rollback, power/sleep, radios
- Regression scope + automation status
- HIL/on-device setup + instrumentation
- Defect triage + release-gate exit criteria

Confirm the structure before generating.

#### File-generation prompt
```
Create a Firmware Test Plan (FW).

CONTEXT:
- FW: [version] — Changes: [...] — Critical funcs: [payment/OTA/power]
- Levels: [unit/HIL/device] — Coverage target: [%]

FORMAT:
- Requirement-to-test traceability table
- Critical-path + regression test lists
- Exit criteria for the release gate

RULES: payment, OTA-with-rollback, and power-management paths are mandatory test cases for any release; each test maps to a requirement ID.
```

---
✍️ Author: Brian H. Doan
