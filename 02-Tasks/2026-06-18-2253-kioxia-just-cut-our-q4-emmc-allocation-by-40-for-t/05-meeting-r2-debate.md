---
type: meeting_r2
---
# Round 2 — Pro/Con Debate

PRO: As the Pro Advocate, I’m pushing for decisive, funded action to protect the AMG-100 Q4 build plan. The Brain is clear: Kioxia’s 40% cut isn’t an abstraction — it’s a direct threat to a $329/unit product with 42% margin, currently in DVT and headed for PVT. If we lose the quarter, that margin is trapped in engineering, not revenue.

Here are our three concrete options, ranked by risk and urgency:

---

### Option 1 (My Recommendation): Authorize the $75k Finance Contingency NOW for Bridge Sourcing, Paired with Fast-Track Qualification
**What we do:**  
- Immediately draw the $75k contingency Finance has already offered (Brain: budget contingency, conditioned on NPI PM confirming a 500-unit bridge build and Engineering validating the alternate component in 10 days).  
- NPI Program Management triggers the alternate eMMC qualification sprint Engineering says is required: PCB layout, thermal, firmware, and PCI/EMVCo re-evaluation.  
- Manufacturing & Supplier Quality (MSQ) locks the Shenzhen factory to the qualified alternate ONLY, preventing unqualified substitutions that historically lead to quality escapes (Brain: MSQ warns of this exact pattern).

**Cost/Risk:**  
- **Cost:** $75k draw + potential 6–8 week schedule slip if the alternate fails (Brain: Hardware PM flagged this).  
- **Risk:** If Engineering can’t validate in 10 days, we lose the bridge window and the Q4 gate slips to Q1. But Finance already tied the spend to that exact validation — so the money is only at risk if we fail the test.  
- **Upside:** Preserves Q4 build for 500 units, keeping DVT→PVT on track and protecting the full 13.3" tablet launch. We avoid fleet fragmentation because we never mix components in production.

**Why this aligns with strategy:** Our ICP (casual-dining chains deploying 20–60 devices per site) demands predictable supply and fleet uptime. A Q4 miss directly hits the “fast RMA turnaround, predictable supply” pain point. The $75k is a rounding error compared to losing the #1 hardware platform trajectory by 2030.

---

### Option 2: Negotiate With Kioxia for Emergency Partial Allocation (No Spend, High Risk)
**What we do:**  
- Have Supply Chain push Kioxia for a preferential allocation to cover the 40% gap, arguing our volume is strategic for their long-term business.  
- Ramp refurbished TS-90R devices as a stopgap for any remaining gap (Brain: TS-90R, $145, 22% margin, Active status).

**Cost/Risk:**  
- **Cost:** $0 upfront, but high opportunity cost.  
- **Risk:** Kioxia has already cut — this is wishcasting. Engineering’s eMMC is single-sourced (Brain: MSQ confirms). If Kioxia doesn’t reverse, we have no Q4 AMG-100 units and must explain to chains why we can’t deliver Gen 3. The TS-90R is a legacy product; it doesn’t meet the AMG-100 spec and fragments our install base. Service Ops (Brain) says they can’t absorb the gap — legacy fleets are already “running hot.”  
- **Upside:** None real; this is a lottery ticket, not a plan.

---

### Option 3: Authorize a Second Source Qualification but Defer the Bridge Build (Mid-Risk, Delays Revenue)
**What we do:**  
- Qualify the alternate eMMC (as in Option 1) but do NOT authorize the $75k bridge build until qualification passes.  
- Accept that Q4 DVT→PVT gate slips to Q1 and communicate the delay to the one customer likely testing AMG-100.

**Cost/Risk:**  
- **Cost:** $0 upfront, but we lose Q4 revenue on the 42% margin product.  
- **Risk:** Service Ops flags that AMG-100 hasn’t built its safety net — a Q1 slip means zero field units generating data, zero revenue, and a perception of instability to our ICP. Competitors with supply chain maturity will eat our lunch.  
- **Upside:** Avoids the $75k draw, but since Finance already conditioned it on validation, Option 1 has the same constraint without the delay.

---

## My Pushback Against Any “Wait and See” Con Argument
The Con Advocate may argue we should absorb the gap with refurbished legacy products and not risk the $75k. But Service Ops’s own position (Brain) kills that: “We cannot absorb a 40% part shortfall through ops heroics.” The TS-90R is not a Gen 3 tablet; it doesn’t solve the labor-shortage pain point (faster payment, upsell, games). Our ICP is buying AMG-100 because the legacy fleet can’t keep up. Delaying just swaps the $75k risk for a much larger, unquantified risk of losing the platform’s launch momentum and chain commitments.

**The Path to Winning:** We draw the contingency, hold Engineering to the 10-day validation, and MSQ to the qualified alternate. That keeps Q4 alive and proves to Finance and the exec team that we can manage supply shocks without losing the strategic plot. The #1 hardware platform by 2030 doesn’t get built by standing still when a single-source part is cut 40%.

CON: Here’s my read, and I’ll be direct because that 40% cut deserves directness.

---

The Pro Advocate laid out three options. I’m not arguing for doing nothing — I’m arguing we don’t authorize a dollar or commit to a path until we answer the two questions that every department in the Brain is screaming at us:

1. **Can Engineering actually validate an alternate eMMC in 10 days?**
2. **If they can’t, does the bridge build still make sense, or are we just burning $75k on a schedule slip we’ve already locked in?**

Here’s why I’m not rubber-stamping Option 1 yet.

---

## First, what the Brain actually says about the alternate component risk

**Hardware Engineering:** This isn’t a resistor swap. The eMMC sits at the intersection of PCB layout, mechanical enclosure, thermal budget, firmware qualification, *and* regulatory certification. A rushed swap risks “cascading tooling changes, fleet fragmentation, and certification rework.” That’s not language from a team that’s confident 10 days is realistic.

**NPI Program Management:** Certification explicitly warns that any alternate eMMC triggers PCI/EMVCo re-evaluation — an 8-week clock, minimum. Not 10 days. Eight weeks. That’s the actual regulatory gate, not an engineering ambition.

**MSQ:** The Shenzhen factory pattern is real and documented. Under pressure, they substitute without qualification. Last time that happened, we got quality escapes. If we authorize a bridge build and the alternate isn’t locked, we’re handing MSQ a fire they’ve already told us they can’t contain.

**Service Ops:** Even if we produce 500 units on the bridge, there is *zero* safety net. No RMA pool. No refurbished Gen 3 tablets. One field issue, and we’re swapping AMG-100s for TS-90R legacy units that don’t meet spec. That’s not a launch — that’s a beta test with customer money.

---

## My pushback on Option 1, point by point

**Pro says: “Draw the $75k now, pair with fast-track qualification.”**

The Brain says Finance conditioned that draw on Engineering validating the alternate in 10 days. But the Brain also says PCI/EMVCo re-evaluation takes 8 weeks. Those two facts are incompatible. If we draw the $75k today, we’re spending money before the condition precedent is met. That’s not protecting the quarter — that’s hoping the quarter protects itself.

**Pro says: “The $75k is a rounding error vs. losing the #1 hardware platform trajectory.”**

The $75k isn’t the issue. I’ll spend the $75k. What I won’t do is pretend it buys us a bridge when the Brain says the bridge’s foundation — a validated alternate — may not exist inside Q4 at all. A rounding error is still an error if it’s spent on a build plan that ships unqualified parts.

**Pro says: “MSQ locks the Shenzhen factory to the qualified alternate only.”**

Locking a factory to a part that hasn’t passed qualification is a contradiction. MSQ’s own position says the historical pattern is unqualified substitution under pressure. If we hand them a part that’s still in validation and say “build 500,” we’re creating the pressure, not solving it.

---

## Option 2 — Pro calls it a lottery ticket. I agree. Let’s move on.

The Brain confirms Kioxia already cut. MSQ confirms single-source. There is no leverage play here. Pro and I are aligned: this isn’t a plan.

---

## Option 3 — Pro dismisses it as “defer and lose the quarter.”

I don’t dismiss it. I want to *structure* it properly. Here’s what I propose:

**A gated decision sequence, not a blanket authorization:**

1. **Gate 1 (Days 1–10):** Engineering runs the alternate eMMC through PCB, thermal, firmware, and *preliminary* PCI/EMVCo assessment. Cost: internal resources only. The $75k is parked, not released.
2. **Gate 2 (Day 10):** If Engineering reports a *credible* 10-day validation path — meaning the physical and firmware qual passes and PCI/EMVCo has a conditional path that doesn’t require full 8-week re-evaluation — we release the $75k immediately for the 500-unit bridge build.
3. **Gate 3 (Day 10, parallel):** MSQ prepares the Shenzhen line for the qualified alternate *only if* Gate 2 passes. If it doesn’t, we accept the Q2 slip, communicate to the test customer, and run a proper second-source qualification on a normal timeline.

**Why this structure:**

- It respects Finance’s condition: the money only moves when validation proves viable.
- It respects Engineering and Certification’s real-world timelines: nothing in the Brain says 10 days is a lock. If it isn’t, we don’t pretend.
- It respects Service Ops: we don’t field 500 units with no RMA pool and an unqualified heart-transplant component.
- It protects the ICP: the worst outcome isn’t a quarter’s delay. The worst outcome is shipping AMG-100s that fail in the field because we swapped a single-sourced storage component under duress. That fractures the “predictable supply” value proposition permanently.

---

## My bottom line

I’m not the “wait and see” advocate. I’m the “don’t authorize the spend until the condition Finance wrote into the spend is met” advocate. The Brain says:

- eMMC qualification touches 5 engineering domains and one 8-week certification gate.
- MSQ has a documented quality-escape pattern under allocation pressure.
- Service Ops has no safety net for a Gen 3 launch.

I want Q4 protected as much as Pro does. But protecting Q4 means not shipping unvalidated tablets to chains that are betting their table-service experience on us. If we draw the $75k on Day 1 and the alternate fails on Day 10, we’ve lost the money *and* the quarter. If we gate it, we lose at most 10 days and keep the $75k for the actual solve — even if that solve lands in Q2.

**My recommendation:** Authorize the gated sequence. Park the $75k. Get Engineering’s real answer at Day 10. Then spend or pivot with full information, not with a schedule panic.