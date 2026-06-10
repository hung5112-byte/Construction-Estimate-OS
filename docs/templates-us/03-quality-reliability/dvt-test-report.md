# P-HPD-03: DVT Test Plan & Report

#### Description
A design-verification test (DVT) plan and report for an electronic device — what is tested, against which spec limits, with what sample size, and an explicit gate verdict. The same skeleton serves EVT (early, reduced scope) and PVT (process-focused).

#### Information to collect (ask the user before generating)
1. Which phase? (EVT / DVT / PVT)
2. Product and hardware/firmware revision under test?
3. Test categories in scope? (electrical, thermal, environmental, mechanical, RF, battery, reliability)
4. Sample size and build source? (which build, which factory)
5. Gate decision needed by when?

#### Suggested template
Structure:
- **Header**: product, HW/FW revision, phase, build/lot, sample size, dates
- **Test matrix**: test ID, category, method/standard reference, spec limit,
  sample size, result (pass/fail/marginal), evidence link
- **Failures**: each failure → severity, root-cause status, fix plan, retest result
- **Compliance pre-scans**: EMC/safety pre-scan results (informal, before the lab)
- **Gate verdict**: PASS / CONDITIONAL (open items with owners + dates) / FAIL
  (recovery plan) — criteria stated, not vibes
- **Sign-off**: engineering, quality, NPI

Confirm the structure before generating.

#### File-generation prompt
```
Create a [EVT/DVT/PVT] test plan & report document.

CONTEXT:
- Product: [model] HW rev [X] / FW [version] — Build: [lot/factory]
- Categories: [electrical, thermal, environmental, mechanical, RF, battery]
- Gate date: [date]

FORMAT:
- Header block; test matrix table (ID, category, method, limit, n, result, evidence)
- Failure log with root-cause status and retest results
- Gate verdict section with explicit criteria and open-item table (owner, date)
- Sign-off block (engineering / quality / NPI)

RULES: every marginal result gets a disposition; a gate pass with open
criticals is recorded as CONDITIONAL, never as PASS.
```

---
✍️ Author: Brian H. Doan
