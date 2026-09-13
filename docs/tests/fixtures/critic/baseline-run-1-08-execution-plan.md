---
type: execution_plan
stop: 2
---
## 📌 Bottom line (30-second read)

- We have a faulty chip in our main product (CY-80L) and need to place a large bulk order fast — the purchase order must be signed by Week 4 to keep production and refurbishments running for up to 44 weeks.
- Before we can order, we need real sales numbers, confirmed pricing, and Engineering's written answer on whether to swap the chip or rebuild the product from scratch — all due Week 1.
- Total spend could exceed $1.02M, which requires Vice President approval; if it goes above $1.36M, the plan is cancelled.
- We do not yet have a confirmed replacement chip — we need at least two viable options identified by Week 6, or we stop the chip-swap work and start a full redesign instead.
- The next-generation product (AMG-100) is not available as a backup — anyone assuming otherwise needs to be corrected immediately.

---

---
type: execution_plan
stop: 2
---
# Execution Plan

## Tasks

| # | Task | Owner dept | Due | Deliverable |
|---|------|-----------|-----|-------------|
| 1 | Pull verified CY-80L (our current main product model) monthly sales figures — minimum last 6 months — from the business system and load them into the financial model | 02-npi-program-management | Week 1 | Confirmed monthly unit volume figure, signed off by Department Head |
| 2 | Get Engineering's formal written position: chip swap (replacing only the faulty chip, keeping the rest of the product the same) or full redesign (rebuilding the product from scratch) as the intended long-term solution | 02-npi-program-management (coordinating with 01-hardware-engineering) | Week 1 | Signed written statement from Engineering lead; shared with all department heads |
| 3 | Pull CY-80R (our current refurbishment model) chip usage separately from CY-80L production demand | 05-service-operations | Week 1 | Standalone chip consumption figure for the refurbishment programme |
| 4 | Freeze reference ("golden") samples (the agreed physical standard that all production units are measured against) and production test limits (the pass/fail boundaries used on the production line) with the **contract manufacturer** (the external factory that builds our products on our behalf) before any stock ships | 04-mfg-supplier-quality | Week 1 | Frozen test limits document, countersigned by the contract manufacturer's quality team |
| 5 | Obtain firm bulk-purchase unit pricing and **MOQ** (**Minimum Order Quantity** — the smallest number of units the supplier will sell in one order, e.g. the supplier may refuse to sell fewer than 10,000 chips at a time) from the chip supplier — authorised manufacturer only, no third-party brokers; require a **COC** (**Certificate of Conformance** — a supplier's written guarantee that the parts meet our agreed specification, e.g. confirming the chips are genuine and built to the correct standard) and manufacture date stamps | 04-mfg-supplier-quality | Week 2 | Signed supplier quotation with COC terms and MOQ confirmed |
| 6 | Model the required order quantity across three chip-swap timeline scenarios (best case 28 weeks / mid case 34 weeks / worst case 44 weeks), including CY-80R refurbishment demand, using the verified sales figures from Task 1 | 02-npi-program-management + 06-finance | Week 2 | Three-scenario order-size model with recommended quantity |
| 7 | Produce a departmental budget breakdown for the $6.8M annual budget and assign a named budget owner for this programme | 06-finance | Week 2 | Departmental budget split document with named owner |
| 8 | Check total committed spend against the $1.02M escalation threshold; escalate to **VP** (**Vice President** — the senior executive with authority to approve spending above this level) if the modelled order exceeds that figure | 06-finance | Week 2 | Written escalation memo to VP if threshold is breached, or written clearance if it is not |
| 9 | Write incoming inspection standards for bulk-purchase stock — including the rule that the first three deliveries of any replacement chip are inspected at the highest level or 100% electrical screen (testing every single chip electrically, rather than testing only a sample) | 03-quality-reliability | Week 3 | Approved incoming inspection plan, ready before first delivery arrives |
| 10 | Sign the bulk purchase order, sized to the worst-case chip-swap timeline (44 weeks) plus a 15% safety cushion, covering both CY-80L production and CY-80R refurbishment demand | 02-npi-program-management + 06-finance (VP sign-off required as order exceeds $50,000) | Week 4 | Countersigned purchase order on file |
| 11 | Identify at least 2 replacement chip candidates with confirmed technical compatibility (matching pin layout — meaning the physical connection points line up — and communication protocol — meaning the chip speaks the same electronic language as the rest of the product) | 04-mfg-supplier-quality + 01-hardware-engineering | Week 5 | Candidate shortlist with technical compatibility confirmation for each |
| 12 | Produce an itemised chip-swap engineering cost estimate broken out by area: chip integration, software update, **payment security re-certification** (re-obtaining the industry approval that confirms our product safely handles card payments — e.g. **PCI** (**Payment Card Industry** compliance — the mandatory security standard required before any device can process credit or debit card payments)), government radio approval lab fees, product safety lab fees, and software labour | 01-hardware-engineering | Week 5 | Line-by-line cost estimate (the current $150,000–$300,000 range is not sufficient for budget approval) |
| 13 | Confirm the import tariff classification (the official tax category assigned by customs that determines how much import duty we pay) for any replacement chip before freight is booked | 05-service-operations | Week 5 | Written tariff classification confirmation on file before any replacement chip material ships |
| 14 | Gate review: if 2 or more replacement chip candidates are confirmed and the itemised cost estimate is approved, issue the engineering spending order for the chip-swap route; if fewer than 2 candidates are found, pause chip-swap spending and formally open a redesign programme | 02-npi-program-management | Week 6 | Written gate decision (proceed with chip swap or redirect to redesign), signed by Department Head |
| 15 | Commit engineering spend on chip-swap route (conditional on a positive Week 6 gate) | 01-hardware-engineering | Week 8 | Approved engineering spending order issued |
| 16 | Complete replacement chip technical integration and start software update | 01-hardware-engineering | Week 20 | Integration milestone report; if missed, assess whether bulk-purchase quantity needs topping up |

---

## Resources

- **Estimated budget:** Up to $1.02M for the bulk purchase order before VP escalation is required; escalate to VP if committed spend exceeds $1.02M, and cancel if it exceeds $1.36M (20% of the $6.8M annual budget). Chip-swap engineering spend of $150,000–$300,000 (exact figure to be confirmed by the itemised estimate in Task 12). Unplanned air freight exposure of $40,000–$80,000 if the chip-swap timeline slips — no freight line item currently exists in the budget and one must be added. Any draw on contingency funds above $25,000 requires a written **Change Control Board** (a small group of decision-makers with the authority to approve unplanned budget changes — for example, approving an emergency freight cost that was not in the original plan) decision log entry.
- **Additional headcount:** No new permanent headcount recommended at this stage. **NPI Programme Management** (**New Product Introduction** — the team responsible for bringing a new or changed product through development and into production, e.g. managing the chip-swap process from engineering through to the factory) will need to coordinate across all six departments at the same time through at least Week 8. Consider whether a dedicated programme coordinator is needed to keep the weekly checkpoint schedule on track.

---

## Risks and mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| The purchase order is sized on unverified sales numbers, resulting in either a supply gap (too small an order) or too much cash tied up in stock that cannot easily be sold (too large an order) | High | Task 1 must be completed in Week 1; no order quantity is finalised until real figures are pulled from the business system |
| Engineering insists on a full redesign while all other departments fund a chip-swap route — wasting money on a path Engineering will not support | High | Task 2 forces a written position from Engineering by Week 1; all engineering budget is blocked until this is resolved in writing |
| CY-80R refurbishment demand is not counted in the order, leaving the refurbishment programme without chips part-way through the window | High | Task 3 separates refurbishment chip usage before the order model is built; Task 6 explicitly includes refurbishment demand in all three scenarios |
| Total committed spend exceeds $1.02M without VP approval, creating a policy breach | High | Task 8 checks the modelled order against the threshold in Week 2, before the order is signed in Week 4 |
| The chip supplier sells end-of-life stock at a large premium, making the order unaffordable or pushing spend past the $1.36M cancellation trigger | High | Task 5 locks firm pricing by Week 2, giving two weeks to reassess quantity before the Week 4 signing deadline |
| Bulk-purchase stock ships before inspection standards exist, allowing subtly faulty chips into inventory (raising the risk of "no fault found" returns — products sent back by customers where no obvious fault can be identified — on both CY-80L and CY-80R) | High | Task 9 requires the incoming inspection plan to be approved before the first delivery arrives, not after |
| Test limits are not frozen before stock ships, creating two subtly different versions of the CY-80L in the field and risking PCI compliance failure | High | Task 4 freezes golden samples and test limits in Week 1, before any stock ships |
| Fewer than 2 replacement chip candidates are found by Week 6, leaving the chip-swap route without a viable source | Medium | Task 14 includes an explicit gate: if the candidate count is below 2, chip-swap spending is paused and a redesign programme is formally opened |
| The chip-swap engineering cost estimate remains a wide range ($150,000–$300,000), preventing formal budget approval | Medium | Task 12 requires a line-by-line breakdown by Week 5; engineering spend is blocked until the itemised estimate exists |
| Unplanned air freight costs ($40,000–$80,000) hit a budget with no freight line item | Medium | Finance must add a freight line item when producing the departmental budget breakdown in Task 7; Service Operations to confirm the tariff classification in Task 13 |
| The **AMG-100** (our next-generation product model — currently **not** in production and therefore not available as a substitute for the CY-80L) is assumed by some people in the business to be available as a replacement. It is not, and cannot fill a CY-80L supply gap | Medium | All internal communications and status reports must clearly state the AMG-100 is not a substitute; NPI Programme Management to include this statement in every programme status update |
| Stock purchased from third-party brokers lacks a COC, introducing counterfeit or out-of-specification chips | Medium | Task 5 makes COC and manufacture date stamps a non-negotiable condition of the purchase order |

---

## Success metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Engineering's written position on chip swap vs. redesign confirmed | Signed statement exists and has been shared | Week 1 |
| Verified CY-80L monthly sales figure pulled from business system | Actual figure in the financial model (not an assumed number) | Week 1 |
| Golden samples and test limits frozen with contract manufacturer | Signed-off document on file | Week 1 |
| Firm supplier pricing and MOQ confirmed | Written quotation with COC terms received | Week 2 |
| Three-scenario order-size model completed including CY-80R refurbishment demand | Model signed off by NPI and Finance | Week 2 |
| Purchase order signed on time | Order placed by end of Week 4 | Week 4 |
| Purchase order spend within approved threshold | Total committed spend at or below $1.02M without VP escalation, or VP approval obtained if above | Week 4 |
| Incoming inspection standards approved before first delivery | Plan signed off and in use | Before first delivery |
| Replacement chip candidates identified | Minimum 2 candidates with confirmed technical compatibility | Week 6 |
| Itemised chip-swap engineering cost estimate produced | Line-by-line breakdown, not a range | Week 6 |
| Engineering spend committed (if gate passed) | Spending order issued | Week 8 |
| Replacement chip technical integration complete | Milestone achieved; software update started | Week 20 |
| CY-80L and CY-80R supply continuity maintained | Zero weeks where either product runs out of stock during the bulk-purchase window | Ongoing through Week 44 |

---

## Templates to create

| Template name | Dept | Notes |
|---------------|------|-------|
| engineering-change-order | 02-npi-program-management | Use to record and control any change to the chip specification or test limits, and to record the formal gate decision at Week 6 |
| incoming-inspection-plan | 03-quality-reliability | Use to define inspection standards for bulk-purchase stock before the first delivery; must include the 100% electrical screen rule for the first three deliveries — note: map to `reliability-test-plan` from the catalogue |
| supplier-corrective-action-request | 04-mfg-supplier-quality | Use if any bulk-purchase delivery fails the incoming inspection or arrives without a valid COC |
| rma-process-sop | 05-service-operations | Use to handle "no fault found" returns from the field on both CY-80L and CY-80R; must refer to the chip variation risk identified by Quality & Reliability |
| shortage-escalation-plan | 02-npi-program-management | Use to define the trigger, escalation path, and VP notification process if the purchase order falls below the minimum required quantity or if fewer than 2 replacement chip candidates are confirmed by Week 6 |