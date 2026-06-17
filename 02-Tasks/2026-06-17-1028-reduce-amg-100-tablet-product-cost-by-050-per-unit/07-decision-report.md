---
type: decision_report
stop: 1
---
## 📌 Bottom line (30-second read)
- We can save $0.50 per unit by switching to a different internal cable—no performance impact, no chip changes needed.
- But changing anything now is risky: the design isn't fully proven yet, the factory line is unstable, and there's no budget allocated.
- Smart move: spend $10K–$15K now to get supplier quotes and a timeline, but don't commit to full testing until the current design passes validation and the factory hits its quality targets.
- This protects the launch date and reliability promise while keeping the savings opportunity alive.

---

# Decision Report: AMG-100 $0.50 Component Cost Reduction

## Bottom Line (30-Second Read)

We've found a way to save $0.50 per unit by switching to an alternative flexible cable — a thin, flat wire that connects internal components (think of it as the ribbon-like wiring inside the device). This change doesn't touch the main processing chip, so there's no risk of slowing the device down.

However, making this change right now is risky because:
- We're in the middle of **DVT** — Design Validation Testing, the phase where we prove the product works as intended before ramping up production
- We have no money set aside for this work
- Our factory line isn't stable enough yet to handle a change safely

**The sensible approach:** Spend a small amount now ($10,000–$15,000) to get firm quotes and a timetable from cable suppliers. But don't commit to full testing until our current design passes validation and the factory is running smoothly. This protects our launch date and our promise of 99.5% device reliability while still chasing the savings before component choices are locked in.

## My Recommendation

**GO with conditions:** Approve a tightly controlled planning phase now. Only commit to full testing and rollout once the current design is proven stable and factory quality data looks solid.

## How This Differs from the Original Plan

| What Changed | Original Plan | My Recommendation | Why |
|-------------|---------------|-------------------|-----|
| Timing | Make the change during current validation testing | Wait until validation is successfully completed | We don't yet have enough real-world performance data or a stable production line. Changing things now purely risks delays. |
| Budget | Use existing funds (no dedicated allocation) | Require a specific **PO** — a Purchase Order, the formal document that commits money to a supplier — for the planning work | Finance tells us there's literally no money earmarked for this. Spending without a proper purchase order is financially irresponsible. |
| What to change | Find $0.50 of savings anywhere in the product | Focus only on switching to an alternative flexible cable | Engineering and manufacturing say this is the only option that's electrically identical, requires no new tooling, and avoids messing with the main chip, power, or wireless performance (**RF** — Radio Frequency, how the device communicates wirelessly). |

## What Each Department Told Us

- **Hardware Engineering:** There's $0.89 of potential savings across various passive components (parts that don't actively control the device). The safest route is bundling changes that don't touch the main chip and need no new manufacturing tools. An alternative flexible cable is electrically identical. Their most urgent priority is passing the **EMC** pre-scan — Electromagnetic Compatibility testing, which checks that the device doesn't interfere with other electronics and vice versa.

- **NPI Program Management** — the team that coordinates new product launches: Making changes during validation testing is a scheduling risk, not a savings win. The only safe approach is component swaps that don't touch the main chip or the **PCB** — Printed Circuit Board, the green board everything sits on. We must define what "no performance loss" actually means before allowing any change.

- **Quality & Reliability:** They want to pause this. We have zero history of how the device performs in real-world use. Swapping any component without a structured comparison test and a full software regression check (making sure existing features still work) creates traceability and audit problems. A bad change could make devices fail in the field.

- **Manufacturing & Supplier Quality:** The alternative flexible cable saves $0.40–$0.50 with "near-zero quality risk" — it's the only realistic option. But first we must fix the factory line. Their **OQC** pass rate — Outgoing Quality Control, the final inspection before products ship — is 94.2%, short of the required 97%. Their **FPY** — First Pass Yield, the percentage of units built correctly on the first attempt without rework — is 91.3%. We can't change components until the line is stable.

- **Finance:** There is exactly $0 budgeted for this. A formal purchase order is required before anyone does anything. If we sell fewer than 50,000 units, the return on this investment is negative. They'll conditionally approve the small planning phase but want volume commitments and test-pass triggers before any bigger spending.

## The Arguments For and Against

**FOR:** The flexible cable is a clear, low-risk way to improve profit margin on every single unit sold. Delaying leaves money on the table and means doing a messy mid-production change later.

**AGAINST:** "Near-zero risk" is not zero. Chasing $0.50 (just 0.15% of the $329 **ASP** — Average Selling Price, what customers typically pay) during validation testing, with no money allocated, risks derailing the entire product launch and breaking our uptime promise. It's a gamble with resources we don't have.

## Three Ways to Look at This

- **GROWTH view:** Do it now. The flexible cable swap has no performance downside. Fund the testing immediately, run it alongside current validation work, and lock in the savings before component choices are frozen (the **BOM** — Bill of Materials, the complete list of every part in the product — gets locked at a certain point and becomes hard to change).

- **CAUTIOUS view:** Reject this entirely for now. We have no budget, no real-world data, and we're gambling a high-margin product launch to save pennies. Make this a formal project for after the **PVT** phase — Production Validation Testing, the later stage where we prove the manufacturing process can build the product consistently.

- **BALANCED view:** The right answer sits in the middle. The flexible cable opportunity is real and shouldn't be abandoned. Fund the planning work now, but make any bigger commitment dependent on clean validation data and a secured budget. This protects the schedule while keeping the door open.

## What Must Happen Before Launch (Blockers)

- **Finance:** Approve a $10,000–$15,000 purchase order from the $6.8 million engineering budget to fund the planning phase.
- **NPI:** Define and get every department to sign off on specific "no performance loss" measurements (boot time, payment transaction speed, screen response time — what we call **UI** latency, or how fast the User Interface reacts).
- **Manufacturing & Supplier Quality:** Send out the **RFQ** package — Request for Quotation, the formal document asking suppliers to bid — for the alternative flexible cable. Get a formal quote covering the supplier's **NRE** costs — Non-Recurring Engineering, the one-time setup fees a supplier charges — and qualification costs.
- **Quality & Reliability:** Draft the structured comparison-testing plan (including an 85°C/85% humidity stress test and connector-plug endurance testing) and secure a commitment for lab time, dependent on validation data.
- **Manufacturing/ODM:** The **ODM** — Original Design Manufacturer, the contract factory that builds the product for us — must bring their line up to the 97% outgoing quality pass rate and resolve three open audit findings before any component change is introduced.

## Decision Gates (Key Performance Indicators, or KPIs)

- **Gate 1 (Planning → Full Testing):** Current validation must finish cleanly, with the factory's outgoing quality pass rate at or above 97%. NPI must confirm we expect to sell more than 50,000 units of the AMG-100 over its lifetime. **ROI** — Return on Investment, whether the savings exceed what we spend to achieve them — only works above this volume.

- **Gate 2 (Full Testing → Locking the Component List):** The alternative cable must pass Quality & Reliability's comparison testing (stress tests, connector endurance, real-world validation) with zero failures. If it fails, the cost-saving idea is dead immediately.

- **Gate 3 (Post-Launch Safety Net):** In the first 30 days of the initial production run, if any real-world failure rate linked to the flexible cable exceeds 0.1%, stop shipping immediately and switch back to the original cable.

## Decisions You Need to Make

- **A:** Approve the $10,000–$15,000 purchase order for the planning phase from the engineering budget? (Yes/No)
- **B:** Agree that full testing money can only be released after (1) clean validation results and (2) confirmation we'll sell more than 50,000 units? (Yes/No)
- **C:** Agree that full qualification cannot begin until the factory hits the 97% quality pass rate, as manufacturing requires? (Yes/No)
- **D:** Or, reject this stepped approach entirely and park the $0.50 flexible cable idea in a formal post-production-validation pipeline, to be revisited 90 days after launch (the CAUTIOUS proposal)? (Selecting this overrides decisions A, B, and C)

---

## ⚠️ Warning: claims missing a source

The following sentences contain figures or legal references but no clear citation was found. The Department Head should verify them before proceeding:

- **[Line 6] Figure:** - We can save $0.50 per unit by switching to a different internal cable—no performance impact, no chip changes needed.
- **[Line 8] Figure:** - Smart move: spend $10K–$15K now to get supplier quotes and a timeline, but don't commit to full testing until the current design passes validation and the factory hits its quality targets.
- **[Line 17] Figure:** We've found a way to save $0.50 per unit by switching to an alternative flexible cable — a thin, flat wire that connects internal components (think of it as the ribbon-like wiring inside the device).
- **[Line 24] Figure:** **The sensible approach:** Spend a small amount now ($10,000–$15,000) to get firm quotes and a timetable from cable suppliers.
- **[Line 24] Figure:** This protects our launch date and our promise of 99.5% device reliability while still chasing the savings before component choices are locked in.
- **[Line 40] Figure:** - **Hardware Engineering:** There's $0.89 of potential savings across various passive components (parts that don't actively control the device).
- **[Line 46] Figure:** - **Manufacturing & Supplier Quality:** The alternative flexible cable saves $0.40–$0.50 with "near-zero quality risk" — it's the only realistic option.
- **[Line 46] Figure:** Their **OQC** pass rate — Outgoing Quality Control, the final inspection before products ship — is 94.2%, short of the required 97%.
- **[Line 46] Figure:** Their **FPY** — First Pass Yield, the percentage of units built correctly on the first attempt without rework — is 91.3%.
- **[Line 48] Figure:** - **Finance:** There is exactly $0 budgeted for this.
- **[Line 48] Figure:** If we sell fewer than 50,000 units, the return on this investment is negative.
- **[Line 66] Figure:** - **Finance:** Approve a $10,000–$15,000 purchase order from the $6.8 million engineering budget to fund the planning phase.
- **[Line 69] Figure:** - **Quality & Reliability:** Draft the structured comparison-testing plan (including an 85°C/85% humidity stress test and connector-plug endurance testing) and secure a commitment for lab time, depend
- **[Line 70] Figure:** - **Manufacturing/ODM:** The **ODM** — Original Design Manufacturer, the contract factory that builds the product for us — must bring their line up to the 97% outgoing quality pass rate and resolve th
- **[Line 74] Figure:** - **Gate 1 (Planning → Full Testing):** Current validation must finish cleanly, with the factory's outgoing quality pass rate at or above 97%.
- **[Line 74] Figure:** NPI must confirm we expect to sell more than 50,000 units of the AMG-100 over its lifetime.
- **[Line 78] Figure:** - **Gate 3 (Post-Launch Safety Net):** In the first 30 days of the initial production run, if any real-world failure rate linked to the flexible cable exceeds 0.1%, stop shipping immediately and switc
- **[Line 82] Figure:** - **A:** Approve the $10,000–$15,000 purchase order for the planning phase from the engineering budget?
- **[Line 83] Figure:** - **B:** Agree that full testing money can only be released after (1) clean validation results and (2) confirmation we'll sell more than 50,000 units?
- **[Line 84] Figure:** - **C:** Agree that full qualification cannot begin until the factory hits the 97% quality pass rate, as manufacturing requires?
- **[Line 85] Figure:** - **D:** Or, reject this stepped approach entirely and park the $0.50 flexible cable idea in a formal post-production-validation pipeline, to be revisited 90 days after launch (the CAUTIOUS proposal)?
