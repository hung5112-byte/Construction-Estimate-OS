# P-NPI-07: Factory Build Commit

#### Description
The written build commitment from an ODM/CM — quantities, dates, line allocation, and the conditions on both sides. Demand without a written factory commit is a wish; this turns wishes into commitments.

#### Information to collect (ask the user before generating)
1. Factory/site and the build(s) being committed?
2. Quantities and ship-date requirements?
3. Conditions the factory needs from us? (material arrival, frozen BOM date, test firmware, deposits)
4. The frozen window policy? (changes inside N weeks need mutual sign-off)
5. What happens on a miss? (escalation, capacity recovery, cost responsibility)

#### Suggested template
Structure:
- **Header**: factory/site, product + BOM revision, commit date, our PM + their PM
- **Commit table**: build/lot, quantity, line, start date, output rate, complete date, ship date
- **Our obligations**: material clear-to-build dates, frozen BOM by, test firmware version by, approvals owed
- **Their obligations**: line allocation, staffing, FAI timing, daily output reporting
- **Frozen window**: the date after which changes require mutual written agreement; change-request path
- **Miss handling**: notification timing (early, with options), recovery capacity rules, cost responsibility per cause [commercial terms — align with the MSA; verify with attorney]
- **Signatures**: both program managers

Confirm the structure before generating.

#### File-generation prompt
```
Create a Factory Build Commit document.

CONTEXT:
- Factory: [site] — Product: [model, BOM rev] — Builds: [qty/dates]
- Our obligations: [material/firmware dates] — Frozen window: [N weeks]

FORMAT:
- Header; commit table; mutual obligations sections
- Frozen-window clause; miss-handling rules referencing the MSA
- Dual signature block

RULES: both sides' obligations are dated; the frozen window is explicit;
a commit without their signature is still a wish.
```

---
✍️ Author: Brian H. Doan
