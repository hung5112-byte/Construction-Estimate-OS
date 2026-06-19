---
type: decision_report
stop: 1
---
## 📌 Bottom line (30-second read)

- Kioxia, our sole supplier for a critical AMG-100 storage chip, has cut Q4 deliveries by 40%, putting $166,000 in profit at risk.
- We recommend a controlled approach: run a 10-day engineering test now to confirm an alternative chip works, but only release the $75,000 emergency fund if the test succeeds.
- If the alternative chip passes, we build 500 temporary units to keep Q4 on track; if it fails, we shift to a Q1 backup plan without spending the money.
- A key concern is that any new chip needs 8 weeks of payment security recertification, and our factory has a history of using unapproved parts under pressure.

---

# Decision Report: AMG-100 Q4 Storage Chip Shortage — Keeping the Build Plan on Track

## Bottom Line

Kioxia, our only supplier for a critical storage chip in the AMG-100 tablet, has cut our Q4 delivery by 40%. The AMG-100 is our next-generation flagship product ($329 per unit, 42% profit margin) — currently in the final testing and validation phase before mass production.

We can't work around this shortage through extra effort: we have no spare AMG-100 units, and our older TS-90R tablet doesn't meet the new requirements.

We have three practical options. The best is a controlled, checkpoint-based approach: approve Finance's $75,000 emergency fund now (ready but not spent), run a 10-day engineering test to confirm an alternative chip works, and only spend the money if the test succeeds.

If the alternative chip passes, we build 500 temporary units and keep Q4 alive. If it fails, we shift to a Q1 qualification of a second supplier without spending the money, and we inform our test customer.

The biggest risks are real and recorded: any alternative chip may require 8 weeks of payment security re-certification, and our Shenzhen factory has a history of using unapproved parts when under pressure.

## Recommendation

**Approve with conditions** — Start the checkpoint-based sequence: launch the 10-day engineering test immediately, approve the $75,000 emergency fund in principle, but release money only if Engineering confirms by Day 10 that an alternative chip works physically and has a believable path through payment security re-certification.

## Changes From the Original Proposal

| Item | Original Proposal | Final Recommendation | Why |
|------|------------------|---------------------|-----|
| Decision trigger | Present options and risk/cost | Checkpoint-based approval with Day-10 go/no-go decision | Finance required the $75k to be conditional on a 10-day test; the payment security re-certification takes 8 weeks, so we must confirm a feasible path exists before committing money |
| Scope of temporary build | Protect the full Q4 build plan | 500-unit temporary build | A 500-unit partial build at 42% profit margin generates $69,000 in contribution — enough to cover the emergency chip purchase even at double the usual price — and avoids over-committing to an untested part |
| Spending authorization | Not specified | $45,000 initial limit, $75,000 total emergency authority | Keeps Finance's initial purchase order under the $50,000 approval threshold; only escalates if spot-market prices exceed double standard cost |

## Detailed Analysis

### What Each Department Told Us

- **Hardware Engineering:** Swapping the storage chip affects the circuit board layout, physical housing, heat management, internal software, and regulatory certification. They want to test a Samsung alternative chip that fits the same connection points, aiming to qualify it in 2 weeks. The internal software team strongly opposes mixing two different chip types before production — they want one single software version for all units.

- **New Product Introduction (NPI) Program Management:** The storage chip is the critical path from final product testing to mass production. The certification team warns that any alternative chip triggers a full payment security re-evaluation: 8–12 weeks, costing $30,000–$37,000. The bill-of-materials and engineering-change teams confirm no pre-approved alternative exists. Buying from unofficial sources risks traceability failure and voiding certifications. Their recommendation: build partially with whatever Kioxia delivers (60% of Q4 needs), and qualify a second supplier for Q1.

- **Manufacturing & Supplier Quality (MSQ):** A single-sourced chip with a 40% shortage means the production line goes idle. The biggest risk is unauthorized purchasing from brokers causing quality failures — a documented pattern from our Shenzhen factory. Qualifying any alternative part takes supplier-quality 6–8 weeks; production-line re-qualification takes 4–6 weeks. The test team warns that switching chip quality tiers without re-calibration adds 400–800 extra defects per million units.

- **Service Operations:** We have zero spare AMG-100 units — we're still in pre-production testing, so no refurbished pool exists. Even 10–15 component repair kits would prevent dead-end returns from the field. Our older tablet fleet already takes 8.2 days for turnaround versus the 5-day service commitment. They recommend locking the 60% allocation to the three confirmed test sites and staging spares before the first wave of installations.

- **Finance:** The storage chip has zero committed purchase orders — no money is already sunk, but other AMG-100 orders (screens, casings) are non-refundable. Revenue at risk: $395,000 in total sales, roughly $166,000 in profit if Q4 is completely lost. Their recommendation: make the $75,000 emergency fund conditional on NPI confirming a 500-unit temporary build and Engineering validating the alternative chip in 10 days. The return on investment: 4 to 8 times the emergency spend if the temporary build succeeds.

### Discussion of Options

- **For (Checkpoint-based approval, immediate engineering test):** Approve the $75,000 emergency fund in principle on Day 1 so the mechanism is ready, Manufacturing can prepare the Shenzhen production line, and Engineering launches the 10-day alternative chip test immediately. Money only releases if the physical and software qualification passes and a believable path through payment security re-certification exists. If validation fails, we keep the money and shift plans — but we haven't lost 10 days of testing time.

- **Against (Immediate $75,000 spend):** Finance made the spend conditional on a 10-day test, but the data shows payment security re-certification takes 8 weeks. Spending before the condition is met risks $75,000 on a build that may be unshippable. Manufacturing's documented quality-failure pattern shows that approving a build before qualification creates exactly the pressure that leads to unapproved substitutions. A checkpoint approach isn't delay — it's managing risk in the right order.

- **Result:** The checkpoint sequence is the middle path. It respects Finance's conditions, protects the schedule (no idle engineering days), and prevents the quality-failure pattern by locking the alternative only after qualification.

### Three Perspectives

- **Growth:** Authorize the $75,000 now and run the test. The competitive window for becoming the number one hardware platform by 2030 can't tolerate a quarter's delay. Finance already built the condition in — if the test fails, the money isn't spent. Delay costs 10 days of build time we can't recover.

- **Cautious:** The data — single-sourced part, 8-week payment security re-certification timeline, documented quality-failure pattern, zero repair pool — tells us this is a qualification-gated problem, not a spend-gated problem. Don't authorize a dollar until Engineering proves the alternative works. Protecting our ideal customer's trust ("predictable supply, fleet reliability") is permanent; a 10-day acceleration that ships untested storage on a payment terminal is reckless.

- **Balanced (recommended):** Checkpoint the authorization — approve the $75,000 on Day 1 but release only at Day 10 if testing confirms the alternative works. Run the engineering test immediately (no idle days). This protects both the schedule and our customer's trust. If the alternative fails, we shift plans with $75,000 saved and complete information.

## Actions Required Before Launch (Blockers)

These items must be completed before we can proceed:

- [ ] **Hardware Engineering (Electrical team):** Complete signal and power testing on the Samsung alternative chip within 10 days. Verify it fits the same connection points — any physical design difference forces a circuit board redesign (6-week delay, roughly $28,000).

- [ ] **Hardware Engineering (Mechanical team):** Confirm the alternative chip's physical height fits within the product's internal spacing (0.5mm margin required). Any height difference greater than 0.3mm triggers housing tooling changes (4–6 weeks, $15,000–$25,000).

- [ ] **Hardware Engineering (Software team):** Assess whether the alternative chip can run on a single software version. If mixing two different chip types is required, escalate to Department Head before committing — managing two software versions consumes 6–8 engineering weeks.

- [ ] **NPI Program Management (Certification):** Determine within 10 days whether the payment security body offers a conditional path that allows a controlled 500-unit temporary build while the full 8-week re-evaluation runs in parallel. If no conditional path exists, stop — do not build.

- [ ] **NPI Program Management (Bill of Materials/Engineering Change):** Open an engineering change order to qualify the alternative chip as a second source. No purchases from unofficial sources or brokers without traceability controls approved by the bill-of-materials and certification teams.

- [ ] **Manufacturing & Supplier Quality (Supplier Quality):** Identify and lock the qualified alternative candidate — golden-sample audit, outgoing quality check hold criteria, and production-line re-qualification plan ready by Day 7. Freeze flash test limits and map acceptable Kioxia quality tiers to the top two yield-friendly tiers.

- [ ] **Manufacturing & Supplier Quality (Factory Test):** Run a 200-unit comparison study on any substitute chip before accepting it for production — budget 1–2 weeks into the insertion schedule.

- [ ] **Service Operations (Repair):** Stage 10–15 storage chip repair kits for the repair bench now, so first field returns on test installations aren't dead ends.

- [ ] **Service Operations (Logistics):** Confirm USMCA trade paperwork filed this week if the Mexico shipping route is preferred ($3.80 per unit savings versus China). Vietnam air-freight fallback at roughly $36 per unit requires CFO sign-off.

- [ ] **Finance (Controller):** Open $45,000 initial emergency authority (under the $50,000 approval threshold); escalate only if spot-market prices exceed double standard cost. Track Kioxia allocation signals weekly — if partial recovery occurs by week 4, cancel unspent authority.

## Key Checkpoint Gates

- **Day 10 Go/No-Go Gate:** If Hardware Engineering cannot confirm (a) physical and software qualification of the alternative chip and (b) a believable payment security conditional path, **do not draw the $75,000 emergency fund**. Shift to Q1 second-supplier qualification and communicate the delay to the test customer.

- **Week 4 Allocation Check:** If Kioxia restores 20% or more of the cut allocation by week 4, Finance may cancel or reduce unspent emergency authority.

- **Post-Bridge Quality Gate (first 200 field units):** If field defects on the alternative chip exceed 2,000 per million units (compared to Kioxia's baseline of 12 and Manufacturing's estimated 400–800 additional), **pause further AMG-100 shipments** and escalate to Quality for root cause.

- **Q4 Mass Production Entry Gate (if temporary build succeeds):** All six new product launch checklist gates must close with the qualified alternative part locked — no exceptions.

## Decisions the Department Head Must Make

**A) Authorize the checkpoint sequence (recommended):** Launch the 10-day engineering test immediately. Approve the $75,000 Finance emergency fund now — but release money only at Day 10 if Engineering confirms the physical and software qualification and a believable payment security conditional path. If Day 10 fails, shift to Q1 second-supplier qualification without spending the emergency fund.

**B) Authorize the $75,000 temporary build spend immediately (Growth position):** Draw the emergency fund now, commit Manufacturing to the qualified alternative, and run the test. Higher risk of spending $75,000 on an unshippable build if payment security blocks the conditional path (data shows 8-week timeline). But zero delay in build preparation if testing succeeds.

**C) Defer all spend until Q1 second-supplier qualification (Cautious fallback):** Accept the Q4-to-Q1 delay now. Communicate to the test customer. Run a full, unrushed second-supplier qualification. Preserves the $75,000 and eliminates risk of shipping untested components, but loses Q4 revenue (roughly $166,000 profit at risk) and competitive momentum.

**D) Attempt Kioxia allocation renegotiation only:** Push for a partial allocation reversal. Data confirms Kioxia already cut production (single-sourced, we have no leverage). This is a lottery ticket — not recommended as a standalone strategy, but may supplement any chosen path if Kioxia signals flexibility by week 4.

---

## ⚠️ Warning: claims missing a source

The following sentences contain figures or legal references but no clear citation was found. The Department Head should verify them before proceeding:

- **[Line 7] Figure:** - Kioxia, our sole supplier for a critical AMG-100 storage chip, has cut Q4 deliveries by 40%, putting $166,000 in profit at risk.
- **[Line 8] Figure:** - We recommend a controlled approach: run a 10-day engineering test now to confirm an alternative chip works, but only release the $75,000 emergency fund if the test succeeds.
- **[Line 9] Figure:** - If the alternative chip passes, we build 500 temporary units to keep Q4 on track; if it fails, we shift to a Q1 backup plan without spending the money.
- **[Line 10] Figure:** - A key concern is that any new chip needs 8 weeks of payment security recertification, and our factory has a history of using unapproved parts under pressure.
- **[Line 18] Figure:** Kioxia, our only supplier for a critical storage chip in the AMG-100 tablet, has cut our Q4 delivery by 40%.
- **[Line 18] Figure:** The AMG-100 is our next-generation flagship product ($329 per unit, 42% profit margin) — currently in the final testing and validation phase before mass production.
- **[Line 22] Figure:** The best is a controlled, checkpoint-based approach: approve Finance's $75,000 emergency fund now (ready but not spent), run a 10-day engineering test to confirm an alternative chip works, and only sp
- **[Line 26] Figure:** The biggest risks are real and recorded: any alternative chip may require 8 weeks of payment security re-certification, and our Shenzhen factory has a history of using unapproved parts when under pres
- **[Line 30] Figure:** **Approve with conditions** — Start the checkpoint-based sequence: launch the 10-day engineering test immediately, approve the $75,000 emergency fund in principle, but release money only if Engineerin
- **[Line 44] Figure:** They want to test a Samsung alternative chip that fits the same connection points, aiming to qualify it in 2 weeks.
- **[Line 46] Figure:** The certification team warns that any alternative chip triggers a full payment security re-evaluation: 8–12 weeks, costing $30,000–$37,000.
- **[Line 46] Figure:** Their recommendation: build partially with whatever Kioxia delivers (60% of Q4 needs), and qualify a second supplier for Q1.
- **[Line 48] Figure:** - **Manufacturing & Supplier Quality (MSQ):** A single-sourced chip with a 40% shortage means the production line goes idle.
- **[Line 48] Figure:** Qualifying any alternative part takes supplier-quality 6–8 weeks; production-line re-qualification takes 4–6 weeks.
- **[Line 50] Figure:** Our older tablet fleet already takes 8.2 days for turnaround versus the 5-day service commitment.
- **[Line 50] Figure:** They recommend locking the 60% allocation to the three confirmed test sites and staging spares before the first wave of installations.
- **[Line 52] Figure:** Revenue at risk: $395,000 in total sales, roughly $166,000 in profit if Q4 is completely lost.
- **[Line 52] Figure:** Their recommendation: make the $75,000 emergency fund conditional on NPI confirming a 500-unit temporary build and Engineering validating the alternative chip in 10 days.
- **[Line 56] Figure:** - **For (Checkpoint-based approval, immediate engineering test):** Approve the $75,000 emergency fund in principle on Day 1 so the mechanism is ready, Manufacturing can prepare the Shenzhen production
- **[Line 56] Figure:** If validation fails, we keep the money and shift plans — but we haven't lost 10 days of testing time.
- **[Line 58] Figure:** - **Against (Immediate $75,000 spend):** Finance made the spend conditional on a 10-day test, but the data shows payment security re-certification takes 8 weeks.
- **[Line 58] Figure:** Spending before the condition is met risks $75,000 on a build that may be unshippable.
- **[Line 64] Figure:** - **Growth:** Authorize the $75,000 now and run the test.
- **[Line 64] Figure:** Delay costs 10 days of build time we can't recover.
- **[Line 68] Figure:** - **Balanced (recommended):** Checkpoint the authorization — approve the $75,000 on Day 1 but release only at Day 10 if testing confirms the alternative works.
- **[Line 68] Figure:** If the alternative fails, we shift plans with $75,000 saved and complete information.
- **[Line 74] Figure:** - [ ] **Hardware Engineering (Electrical team):** Complete signal and power testing on the Samsung alternative chip within 10 days.
- **[Line 74] Figure:** Verify it fits the same connection points — any physical design difference forces a circuit board redesign (6-week delay, roughly $28,000).
- **[Line 76] Figure:** - [ ] **Hardware Engineering (Mechanical team):** Confirm the alternative chip's physical height fits within the product's internal spacing (0.5mm margin required).
- **[Line 76] Figure:** Any height difference greater than 0.3mm triggers housing tooling changes (4–6 weeks, $15,000–$25,000).
- **[Line 80] Figure:** - [ ] **NPI Program Management (Certification):** Determine within 10 days whether the payment security body offers a conditional path that allows a controlled 500-unit temporary build while the full 
- **[Line 86] Figure:** - [ ] **Manufacturing & Supplier Quality (Factory Test):** Run a 200-unit comparison study on any substitute chip before accepting it for production — budget 1–2 weeks into the insertion schedule.
- **[Line 90] Figure:** - [ ] **Service Operations (Logistics):** Confirm USMCA trade paperwork filed this week if the Mexico shipping route is preferred ($3.80 per unit savings versus China).
- **[Line 90] Figure:** Vietnam air-freight fallback at roughly $36 per unit requires CFO sign-off.
- **[Line 92] Figure:** - [ ] **Finance (Controller):** Open $45,000 initial emergency authority (under the $50,000 approval threshold); escalate only if spot-market prices exceed double standard cost.
- **[Line 96] Figure:** - **Day 10 Go/No-Go Gate:** If Hardware Engineering cannot confirm (a) physical and software qualification of the alternative chip and (b) a believable payment security conditional path, **do not draw
- **[Line 98] Figure:** - **Week 4 Allocation Check:** If Kioxia restores 20% or more of the cut allocation by week 4, Finance may cancel or reduce unspent emergency authority.
- **[Line 100] Figure:** - **Post-Bridge Quality Gate (first 200 field units):** If field defects on the alternative chip exceed 2,000 per million units (compared to Kioxia's baseline of 12 and Manufacturing's estimated 400–8
- **[Line 102] Figure:** - **Q4 Mass Production Entry Gate (if temporary build succeeds):** All six new product launch checklist gates must close with the qualified alternative part locked — no exceptions.
- **[Line 106] Figure:** Approve the $75,000 Finance emergency fund now — but release money only at Day 10 if Engineering confirms the physical and software qualification and a believable payment security conditional path.
- **[Line 108] Figure:** **B) Authorize the $75,000 temporary build spend immediately (Growth position):** Draw the emergency fund now, commit Manufacturing to the qualified alternative, and run the test.
- **[Line 108] Figure:** Higher risk of spending $75,000 on an unshippable build if payment security blocks the conditional path (data shows 8-week timeline).
- **[Line 110] Figure:** Preserves the $75,000 and eliminates risk of shipping untested components, but loses Q4 revenue (roughly $166,000 profit at risk) and competitive momentum.
