# P-HWE-13: EMC Pre-Compliance Test Plan (EE)

#### Description
A pre-compliance EMC plan (radiated/conducted emissions, immunity, ESD) run before the accredited-lab visit so the certification slot is not wasted on a failing unit.

#### Information to collect (ask the user before generating)
1. Product, radios, and target markets (FCC Part 15, CE/EN, etc.)?
2. Applicable standards/classes (Part 15B/C, 62368-1, ESD 61000-4-2)?
3. Test sample config (cables, peripherals, firmware mode)?
4. In-house vs. third-party pre-scan capability?
5. Known risk areas (switchers, clocks, antennas)?

#### Suggested template
Structure:
- Standards matrix: test, limit, class, market
- Sample configuration + operating modes under test
- Test list: radiated/conducted emissions, ESD, surge/EFT as applicable
- Pass/fail margins target (e.g. 6 dB below limit at pre-scan)
- Risk mitigations staged (filtering, shielding, firmware) + lab booking gate

Confirm the structure before generating.

#### File-generation prompt
```
Create a EMC Pre-Compliance Test Plan (EE).

CONTEXT:
- Product: [model] — Radios: [Wi-Fi/BT/NFC/LTE] — Markets: [US/EU/...]
- Standards: [Part 15B/C, 62368-1, ...] — Sample: [config]

FORMAT:
- Standards/limits matrix; test list with method + margin target
- Sample/setup description
- Risk + mitigation table; gate to book the accredited lab

RULES: cite each standard and class explicitly [verify with lab]; do not book the accredited slot until pre-scan margin target is met or a mitigation plan is committed.
```

---
✍️ Author: Brian H. Doan
