---
type: clarification
answered: true
---

# 🤖 Questions from the system (Brain-first)

> Tick `[x]` for the Department Head's choice, or fill in free text. Save the file.

## Q1 [CRITICAL]
_Cite: 00-Brain/products.json: AMG100.status = 'DVT'_

The Brain lists AMG-100 in DVT phase. In what program phase does the Q4 build plan assume these units ship — DVT samples, PVT pilot, or full MP mass production?

- [ ] DVT samples only (engineering builds)
- [ ] PVT pilot (limited production for validation)
- [x] Full MP ramp (commercial shipment to customers)
- [ ] Mixed — some PVT, some MP

## Q2 [CRITICAL]
_Cite: 00-Brain/products.json: no alt BOM; 00-Brain/laws.json: 47 CFR Part 15, UL/IEC 62368-1_

The Brain shows no second-source NAND IC and no alternate approved BOM for AMG-100. If you plan a partial eMMC supplier swap as a mitigation, what qualification timeline and regulatory recertification delta do you estimate for FCC Part 15 / UL 62368-1?

- [ ] No recertification needed — drop-in compatible part
- [ ] FCC/UL delta < 4 weeks, can start within Q4
- [x] FCC/UL delta 4–8 weeks, start pushes past Q4
- [ ] Significant redesign required — not Q4 feasible

## Q3 [CRITICAL]
_Cite: 00-Brain/budget.json: total_year_usd = 6800000, spent_year_usd = 0_

The total annual hardware budget in the Brain is $6.8M with $0 spent recorded and no Q4-specific allocation. What is the Q4 spend ceiling available for spot-buy eMMC premiums, line-down charges, or emergency NRE?

- [ ] We have full $6.8M unencumbered; no Q4 cap
- [x] Approximately 25% ($1.7M) allocated for Q4
- [ ] Less than $500K discretionary remaining for Q4
- [ ] No committed Q4 hardware budget — needs new approval

## Q4 [WARN]
_Cite: 00-Brain/products.json: no BOM / features array for AMG100_

The Brain contains no BOM for AMG-100. Is the impacted eMMC soldered-down or socketed, and is it shared with TS-90 or CY-80L? This determines rework cost, board scrap risk, and potential to cannibalize from other programs.

- [x] Soldered-down; unique to AMG-100
- [ ] Soldered-down; shared with TS-90 or CY-80L
- [ ] Socketed/module; unique to AMG-100
- [ ] Socketed/module; shared with TS-90 or CY-80L

## Q5 [WARN]
_Cite: 00-Brain/products.json: no inventory fields; 00-Brain/headcount.json: department '04-mfg-supplier-quality' active_

No on-hand, in-transit, or safety-stock inventory data exists in the Brain for this eMMC part. What is your current inventory position in weeks-of-supply (at Q4 build rate), including pipe?

- [ ] Less than 2 weeks — critical exposure now
- [x] 2–6 weeks — partial buffer, Q4 gap remains
- [ ] 6–12 weeks — covers most of Q4
- [ ] More than 12 weeks — sufficient to absorb 40% cut

## Q6 [WARN]
_Cite: 00-Brain/products.json: TS90.status = 'MP', TS90R.status = 'Active', AMG100.margin_pct = 42.0_

The Brain shows TS-90 in MP and TS-90R (refurb) Active. Is a short-term bridge substituting or supplementing AMG-100 shipments with TS-90R or CY-80L units viable — factoring in customer acceptance, certification scope, and the 42% target margin?

- [ ] Yes — customer already approves TS-90R as equivalent
- [x] Maybe — requires limited customer waiver; margin risk < 5 pts
- [ ] No — different form factor / certification blocks substitution
- [ ] Not evaluated yet — need customer & cert input
