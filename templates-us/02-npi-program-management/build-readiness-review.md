# P-NPI-03: Build Readiness Review

#### Description
The go/no-go check before committing a build at the factory — material coverage, test readiness, documentation currency, and line booking, verified with evidence days before materials are consumed. A build without pass criteria is a party, not a build.

#### Information to collect (ask the user before generating)
1. Build purpose and phase? (EVT-2, DVT-1, PVT, production change validation)
2. Quantity, factory/site, and target start date?
3. BOM revision the build must use — any in-flight ECOs?
4. Test plan for the build (stations, coverage, who correlates)?
5. Material status source? (factory clear-to-build report, buyer coverage report)

#### Suggested template
Structure:
- **Header**: build name, purpose, qty, site, target dates, BOM revision (frozen)
- **Purpose & pass criteria**: what this build must prove; numeric criteria
- **Material readiness**: clear-to-build % , shortages with ETAs, substitutions (approved alternates only — with ECO refs)
- **Documentation readiness**: work instructions at correct revision, FAI requirements, deviation list
- **Test readiness**: stations available, fixtures correlated, test firmware version
- **Line & schedule**: booked window, changeover, daily output assumption
- **Risk & fallback**: top 3 things that stop the build; partial-build decision rules
- **Verdict**: GO / GO with conditions (dated) / HOLD — signed by NPI PM + MSQ + quality

Confirm the structure before generating.

#### File-generation prompt
```
Create a Build Readiness Review document.

CONTEXT:
- Build: [name/purpose] — Qty: [n] — Site: [factory] — Start: [date]
- BOM rev: [X] — Open ECOs: [list] — Test plan: [summary]

FORMAT:
- Header; purpose + numeric pass criteria; material/documentation/test
  readiness tables with evidence; line booking; risk & fallback rules
- Verdict block with three signatures

RULES: substitutions only from approved alternates with ECO references;
an unfrozen BOM is an automatic HOLD; pass criteria precede the build.
```

---
✍️ Author: Brian H. Doan
