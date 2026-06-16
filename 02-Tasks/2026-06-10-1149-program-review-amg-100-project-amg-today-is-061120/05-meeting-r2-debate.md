---
type: meeting_r2
---
# Round 2 — Pro/Con Debate

PRO: I’ll address this directly from the Pro Advocate seat, incorporating the department head’s cost reframe while holding the schedule and quality gates inviolable.

## Position: We Ship DVT on 06/22 with Zero Quality Gate Erosion and Minimal Committed Cash

The Brain tells me we have an $111.6k remaining contingency against a total $2M budget, with $872k already spent. We’re 11 days from the DVT build date of 06/22, with a hard certification gate on 08/18. The department perspectives confirm schedule is tight but achievable — three days of buffer on the antenna rework parts (ISS-014) is our single-point risk, with zero slack beyond 08/18 for PCI/EMV certification.

My recommendation is a prioritized improvement plan that meets the department head’s directive: **hold the speed, minimize committed cash, quality gates inviolable.** Every de-risk action below is restructured as trigger-based unless committing now is the only path to 06/22.

---

## Prioritized Improvement Plan

### 1. Antenna Rework Parts (ISS-014) — DG courier: **Trigger-Based**
**Risk:** ISS-014 ETA of 06/16 with only three working days of buffer is the single schedule driver for the DVT build. If the shipment slips past 06/17, we burn the 06/22 build date and cascade into the 08/18 cert gate with zero slack (strategy: fleet uptime >99.5% requires cert integrity — per Brain, cert path has zero slack after 08/18).

**Action:** Authorize DG courier/personal-carriage retrieval of the antenna rework parts shipment **only on a written trigger.**  
- **Trigger:** Supplier ETA confirmation slips past 06/17 12:00 CT.  
- **Cost if fired:** $3,200 (DG next-flight-out estimated for small-package freight from Shenzhen to Austin).  
- **Probability of firing:** ~25% (supplier is tracking to 06/16; the 3-day buffer is tight but real).  
- **Expected cash:** $800.  
- **Owner:** 04-Mfg-Supplier-Quality, decision by 06/16 09:00 CT.  

**Confirmation:** No quality gate is weakened — this is a logistics expedite, not a design change. PRT coverage and cert audit trail are unaffected.

---

### 2. CM build-team standby hold: **$0 Action FIRST, then Trigger-Based**
**Risk:** If parts arrive 06/17–06/18, the CM needs confirmed line capacity and technician staffing to complete the DVT build by 06/22. A paid standby hold was proposed at $8k.

**Action:**  
- **$0 first:** Negotiate a *no-cost priority-reservation letter* with the CM — commit a future PO for the MP ramp in exchange for guaranteed DVT-build capacity 06/17–06/22. This is standard practice per MSQ team’s supplier-negotiation approach (Brain: two-qualified-sources rule still applies — this is a capacity agreement, not a single-source commitment).  
- **Trigger-based backup:** If no-cost reservation fails by 06/13, authorize a paid standby hold **only on a written trigger.**  
  - **Trigger:** No-cost capacity agreement not secured by 06/13 17:00 CT.  
  - **Cost if fired:** $8,000 (one-week standby labor reservation).  
  - **Probability:** 15% (CM has open capacity per MSQ; the no-cost option is likely to succeed).  
  - **Expected cash:** $1,200.  
- **Owner:** 04-Mfg-Supplier-Quality, negotiation by 06/12; decision gate 06/13.  

**Confirmation:** No quality gate is weakened. This is a capacity-reservation action; PRT coverage and build processes remain per the DVT plan (strategy: DVT yield target 88%, per factory-yield-EVT baseline of 78% — no process shortcuts).

---

### 3. Air-freight backup for DVT parts: **Trigger-Based**
**Risk:** Any secondary part shortage (beyond ISS-014) could delay the DVT build if standard freight misses the 06/22 window. An air-freight expedite was proposed at $14k.

**Action:**  
- **Trigger:** Any DVT bill-of-materials line item supplier-confirmed ETA slips past 06/18 12:00 CT.  
- **Cost if fired:** $14,000 (air freight for remaining parts consolidation from Asia to Austin).  
- **Probability:** 10% (ISS-014 is the only known at-risk part; all other BOM items are tracking on schedule per MSQ position).  
- **Expected cash:** $1,400.  
- **Owner:** 04-Mfg-Supplier-Quality, monitor supplier ETAs daily from 06/12; trigger gate 06/18.  

**Confirmation:** No quality gate weakened — this is a freight-mode change, not a part substitution. Two-qualified-sources rule and PRT coverage unchanged.

---

### 4. Expedited pre-stage labor (DG receipt to CM intake): **Trigger-Based**
**Risk:** If DG courier fires (Action 1), the parts arrive at DG hub Austin ~4–6 hours before CM cutoff. Pre-staging labor (customs clearance prep, dedicated intake runner) was proposed at $1.8k committed.

**Action:**  
- **Trigger:** DG courier is fired (Action 1 trigger met). This is a *dependent trigger* — it only fires if Action 1 fires.  
- **Cost if fired:** $1,800 (dedicated customs broker pre-clearance + on-call courier from DG hub to CM).  
- **Probability:** Same as Action 1 — 25% conditional on Action 1 firing, so 25% overall.  
- **Expected cash:** $450.  
- **Owner:** 05-Service-Operations (logistics coordination); dependent on Action 1 trigger.  

**Confirmation:** No quality gate weakened — this is intake logistics, not a build or test process change.

---

### 5. Tet/BrightPath pre-build inventory: **Recoverable Working Capital — Move Off Contingency**
**Risk:** BrightPath single-site risk (R-09 — bus factor, sole RF engineer) could disrupt the ramp if BrightPath capacity is constrained during beta trial (Sept) or early MP. The earlier plan proposed $15k in contingency for pre-build inventory to buffer against single-site disruption.

**Department Head’s Re-Cost:** This is **recoverable working capital**, not NRE burn. The Brain shows the AMG-100 at $329/unit (42% margin) and AMG-D10 at $89/unit (38% margin). Pre-built Tet/BrightPath subassemblies can be consumed against actual ramp orders — they inventory as assets, not expense.

**Action:**  
- **Move the $15k from program contingency to a separate capital line** (inventory pre-build authorization, tied to ramp demand per the Brain’s ramp-plan). Right-size the pre-build to 30 units (covers first 60 days of beta trial spares demand, per Service Ops position on spares burn rate).  
- **Cost to contingency:** $0 (reclassified as capital, not program expense).  
- **Owner:** 04-Mfg-Supplier-Quality + Finance (capital authorization by 06/20).  

**Confirmation:** No quality gate weakened — two-qualified-sources rule still applies for MP; this is a tactical buffer build, not a single-source commitment. R-09 bus-factor risk is mitigated by the RF-engineer documentation file (see Action 6).

---

### 6. RF-engineer bus-factor (R-09): **$0 Action**
**Risk:** Single RF engineer (BrightPath, R-09) creates key-person risk for antenna coexistence and cert support. A paid contractor search ($4k placeholder) was proposed.

**Action:**  
- **$0 first:** Require the RF engineer to produce a **detailed documentation file** (tuning procedures, test fixtures, calibration data, cert submission package) by 06/30, reviewed by the engineering manager. This buys the same schedule protection as a contractor search — a qualified RF contractor can ramp from documentation, not from scratch, if the key person becomes unavailable.  
- **Trigger-based backup:** If documentation review fails completeness by 06/30, initiate contractor search ($4k) on trigger — but probability is <10% given the engineer’s track record on EVT (Brain: ISS-019/021/023 closed; R-09 is a bus-factor risk, not a performance risk).  
- **Expected cash:** $400 (trigger probability ~10% × $4k, only if documentation fails).  
- **Owner:** 01-Hardware-Engineering, documentation by 06/30; review 07/02.  

**Confirmation:** No quality gate weakened — cert path (08/18) and antenna coexistence validation (ISS-023, PRT coverage) are strengthened by the documentation artifact, not weakened.

---

### 7. Battery 8D D6–D8 acceleration: **$0 Action (reprioritization)**
**Risk:** Battery 8D is at D6 — root cause identified, permanent corrective action in validation. The alpha trial uptime gap (99.1% vs. 99.5% target, per Brain: field-trial-report) is driven partly by battery-related spares burn (Service Ops position). Any delay in closing the 8D to D8 risks repeating the gap in beta trial (Sept).

**Action:**  
- Assign dedicated quality engineer to battery 8D D7–D8 closure **this sprint** (no added cost — reprioritize within existing headcount per Brain: active departments include 03-Quality-Reliability and 05-Service-Operations).  
- **Cost:** $0 (internal reprioritization).  
- **Owner:** 03-Quality-Reliability, D8 closure by 07/01 to support beta trial readiness (Sept per Brain: ramp-plan).  

**Confirmation:** No quality gate weakened — battery validation is an inviolable gate per the department head directive and Brain’s cert-plan (PCI/EMV rigor, safety listing UL/IEC 62368-1). This action hardens the gate, not weakens it.

---

## Committed Cash vs. Expected Cash Summary

| Action | Type | Cost if Fired | Firing Probability | Expected Cash | Committed Now |
|--------|------|---------------|--------------------|---------------|---------------|
| 1. DG courier (ISS-014) | Trigger | $3,200 | 25% | $800 | $0 |
| 2. CM standby (backup) | Trigger | $8,000 | 15% | $1,200 | $0 |
| 3. Air-freight backup | Trigger | $14,000 | 10% | $1,400 | $0 |
| 4. Pre-stage labor | Trigger (dependent on #1) | $1,800 | 25% | $450 | $0 |
| 5. Tet/BrightPath pre-build | Capital reclass | $0 | — | $0 | $0 |
| 6. RF eng. documentation | $0 first, trigger backup | $4,000 | 10% | $400 | $0 |
| 7. Battery 8D acceleration | $0 (reprioritize) | $0 | — | $0 | $0 |
| **Totals** | — | **$31,000** (worst-case) | — | **$4,250** | **$0** |

- **Committed cash:** $0.  
- **Expected cash:** $4,250.  
- **Worst-case cash:** $31,000 (all triggers fire simultaneously — requires ISS-014 slip past 06/17, CM capacity failure, and BOM slip, a compound probability ~0.4%).  

This leaves $107,350 of the $111.6k contingency untouched (or $80,600 if worst-case fires, still within budget per Brain: budget-tracker showing $2M total).

---

## Schedule and Quality Gate Confirmation

**06/22 DVT build date:** Held. The DG courier trigger (Action 1) is the schedule backstop — if the 06/16 ETA slips, the courier is authorized with a 24-hour retrieval window (06/18 → 06/19 intake → 06/20–06/22 build). The CM standby trigger (Action 2) ensures capacity alignment. The air-freight trigger (Action 3) catches any secondary BOM slip. Actions 1–4 together provide layered defense with zero committed cash unless a trigger fires.

**08/18 certification hard gate:** Held with zero slack erosion. The Brain’s cert-plan shows PCI PTS pre-assessment 07/06 (R-01) and the 08/18 final gate with no slack. None of the above actions alter the cert critical path — they protect the DVT build that feeds the cert units. The RF documentation file (Action 6) hardens cert support, not weakens it.

**Quality gates inviolable:**  
- **PRT coverage:** Unchanged — we are not reducing test coverage; the DVT build follows the same PRT plan (Brain: prt-plan).  
- **Two-qualified-sources rule:** Unchanged — the Tet pre-build (Action 5) is a tactical buffer, not a single-source commitment. BrightPath remains one of two qualified sources; R-09 is mitigated by documentation.  
- **PCI/EMV rigor:** Strengthened — the 08/18 cert gate is protected by the schedule actions; battery 8D closure (Action 7) hardens field reliability data for cert submission.  
- **Battery validation:** Harden by Action 7’s D8 closure, not weakened — the 8D process is quality’s own gate (Brain: Lithium battery transport, 49 CFR/IATA DG; safety listing UL/IEC 62368-1).  

---

## Yield and Reliability Path (Not Cost-Dependent, Confirmed)

The Brain’s factory-yield-EVT shows 78% yield with a target path to 88% at DVT and 95% at MP. The actions above do not directly spend on yield improvement — that’s an engineering-process workstream already in the base plan ($1,978k of $2M allocated, per the department head’s directive: no base-workstream cuts). The CM capacity action (Action 2) and MSQ’s supplier-quality gates (ISS-027/028) are the process enablers — they’re in the base plan, not the de-risk bundle.

MTBF of 62k hours vs. 2.0% AFR target (per Brain: mtbf-prediction) is a design-intent metric — DVT testing will validate or disprove it. The alpha trial uptime gap (99.1% vs. 99.5%) is addressed by battery 8D closure (Action 7) and the depot-readiness workstream already in Service Ops’ base plan. The depot readiness for AMG-100 (Brain: field-trial-report) is not a cost-add in this plan — it’s base-plan workstream, per the directive.

---

## Summary

This plan holds 06/22 and 08/18 with **zero committed cash** and $4,250 expected cash, leaving $107k–$80k of contingency intact. Every quality gate is confirmed inviolable — six explicit confirmations above, each cross-referenced to Brain data (cert-plan, prt-plan, factory-yield-EVT, mtbf-prediction, field-trial-report, ramp-plan, and the department head’s directive). The department head’s reframe is fully met: speed is held, committed budget is minimized to $0, recoverable capital is reclassified, $0 actions are used first, and base workstreams are untouched.

CON: Here is the Con Advocate's rebuttal, incorporating the department head's cost reframe and directly challenging the Pro Advocate's proposal.

## Con Advocate Position: The Pro’s Plan is a Fragile Bet Dressed as a Prudent Hedge

The Pro Advocate’s plan is elegant, but it fails on three critical fronts: it overestimates trigger speed against a known threat, treats a catastrophic supplier risk with a logistics band-aid, and dangerously optimizes for cost at the expense of hard-won quality data. The Brain data, when read without optimism, shows a program balanced on a knife’s edge with unacceptable technical debt.

My position is that we must spend *some* committed money now to transform a reactive, trigger-based defense into a robust, pre-planned schedule margin. We cannot treat a 3-day buffer as a risk; it is a near-certainty of slip.

---

## Rebuttal of Pro Advocate’s Prioritized Plan

### 1. Antenna DG Courier: A Trigger is Too Slow for a Single Point of Failure
The Pro plan treats ISS-014’s 06/16 ETA as a logistics problem solvable by a next-flight-out courier. This is a critical error in reading the Brain’s Department Perspectives.

- **Brain citation:** 01-Hardware-Engineering states the 06/16 shipment is a "single-point schedule risk." 02-NPI states it’s an "11-day[s] from DVT build" schedule with a "hard certification gate at 08/18 with zero slack."
- **Rebuttal:** A trigger activated on 06/17, when a factory in Shenzhen confirms a slip, does not magically produce parts in Austin by 06/19. The Pro's math assumes a 24-hour global courier miracle from supplier-slip-confirmation to parts-on-bench. We’ve seen this movie before. A customs hold, a DG paperwork error on a lithium battery component (Brain: 49 CFR / IATA DG), or a simple missed connection burns the entire DVT build window. If we wait for the slip to *happen* before acting, we have already lost 08/18, because the Brain confirms "zero slack" after that date. **We must build schedule margin, not just react to its absence.**

### 2. Recoverable Capital: Misclassifying a Strategic Necessity
The Pro plan rightfully moves the Tet/BrightPath pre-build off the contingency line, calling it "recoverable working capital." I agree with the accounting, but the problem is the *quantity*.

- **Brain citation:** 05-Service-Operations states the "alpha trial uptime gap (99.1% vs. 99.5%)... means beta deployment burns spares faster than planned." The strategy demands a "99.5% fleet uptime."
- **Rebuttal:** Right-sizing it to "30 units" for "60 days" is a gamble that our alpha trial data is an outlier, not a trend. The Service Ops position explicitly warns against this optimism. If deploy spares are burned faster, a 30-unit pre-build is a burnt match before the beta trial even generates momentum, risking field failures that directly violate the company’s strategic goal. This isn’t a buffer; it's a symbolic gesture.

### 3. $0 Actions: A Documentation File Doesn't Replace an Engineer
The Pro plan’s treatment of the BrightPath single RF engineer risk (R-09) is the most dangerous cost-avoidance move in the deck.

- **Brain citation:** 04-Mfg-Supplier-Quality flags "single RF engineer bus-factor R-09, BrightPath single-site risk." The 08/18 cert path is locked and relies on RF coexistence validation (ISS-023).
- **Rebuttal:** Pro suggests an "RF-engineer documentation file" as a $0 replacement for a paid contractor. If the bus factor hits—if that single engineer gets sick, leaves, or is hit by the proverbial bus on 07/15—a "documentation file" cannot execute antenna tuning, debug coexistence interference in the EMV chamber, or answer an 11th-hour question from the PCI PTS lab (07/06 pre-assessment, R-01). A static document is not a dynamic, qualified human. We are betting the company’s #1 strategic goal on one person's health. A $4k contractor retainer is the cheapest insurance policy we will ever buy.

### 4. Battery 8D: Reprioritization Masks a Resource Conflict
The Pro plan assigns a "dedicated quality engineer" to close the battery 8D to D8 by 07/01 with "no added cost."

- **Brain citation:** 03-Quality-Reliability states three gates are "soft — battery validation, antenna coexistence, and document control." The Pro plan itself lists ISS-027/028 as open quality gates.
- **Rebuttal:** You cannot reprioritize a quality engineer from soft gates (ISS-027/028) to harden the battery 8D and call it a "$0 action." That is a direct trade-off that weakens DVT readiness in one area to fix another. We are not creating capacity; we are borrowing it from an equally critical, inviolable quality gate. This risks a cascading failure where battery validation passes, but DVT process validation fails.

---

## The Con Advocate's Revised Improvement Plan: Spend Early, Build Margin

We must follow the department head’s directive to hold the schedule with minimal *committed* cash, but "minimal" is not "zero" when "zero" creates existential schedule risk. We will spend a small amount of committed cash now to ensure our triggers are fast enough to matter.

| Priority | Action | Owner | Date | Cost Delta & Type | Quality Gate Confirmation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **ISS-014: Commit to Pre-Staged Courier Path Now.** Do not wait for a slip. Immediately book and pay for the DG-capable courier to be standing by in Shenzhen on 06/16 to receive the parts the moment they are ready. This buys 1–2 days vs. a trigger-fired emergency call. We commit the courier fee, not the flight cost, yet. | 04-Mfg-Supplier-Quality | 06/12/2026 | **Committed-Now: $1,500** (courier standby). **Trigger-Based**: Air freight cost ($3,200) only paid upon successful pickup. | No quality gate weakened. This hardens the DVT build schedule, protecting the samples needed for PRT coverage and cert audit trail. |
| **2** | **CM Capacity: Trigger-Based Reservation.** We accept the Pro's trigger for the $8k standby hold, but only if the no-cost letter fails. This is a pure insurance policy. | 04-Mfg-Supplier-Quality | 06/13/2026 | **Committed-Now: $0. Trigger-Based ($8,000)** if no-cost agreement fails. | No quality gate weakened. A capacity guarantee ensures we do not rush the DVT 88% yield target (Brain: factory-yield-evt). |
| **3** | **Air-Freight Backup: Trigger-Based.** This remains a reasonable, low-probability trigger for secondary BOM slips. We accept the Pro's structure here. | 04-Mfg-Supplier-Quality | 06/18/2026 | **Committed-Now: $0. Trigger-Based ($14,000)** if any line item ETA slips. | No quality gate weakened. |
| **4** | **Tet Pre-Build: Right-Size to Beta Burn Rate.** We accept the capital reclassification but must right-size the pre-build to 75 units, not 30. | 04-Mfg-Supplier-Quality, Finance | 06/20/2026 | **Committed-Now: $0 against contingency.** Moved to a separate capital line with an incremental $22.5k authorization. This directly reflects the higher spares burn rate confirmed by Service Ops and the 99.5% uptime goal. | No quality gate weakened. This action directly supports meeting the strategic fleet uptime requirement without committing a single source (Brain: two-qualified-sources rule). |
| **5** | **RF Bus-Factor (R-09): Commit to a Part-Time Contractor Retainer.** A documentation file is a helpful artifact, but it is not a mitigation for a single point of failure on a cert-critical path. | 01-Hardware-Engineering, HR | 06/18/2026 | **Committed-Now: $4,000.** Retainer for a qualified RF contractor to review the documentation file, be familiar with our design, and be on standby for the 08/18 cert push. | No quality gate weakened. It directly hardens the cert critical path by ensuring a qualified backup, protecting PCI/EMV and antenna coexistence validation (ISS-023). |
| **6** | **Battery 8D: Fund Dedicated Overtime.** Do not borrow from quality resources (ISS-027/028). Authorize a focused overtime budget for the existing quality engineer to close the D7/D8 validation sprint without sacrificing other DVT readiness gates. | 03-Quality-Reliability | 06/12/2026 | **Committed-Now: $2,800.** (2 weeks of dedicated overtime). | No quality gate weakened. This hardens the inviolable battery validation gate (Brain: safety listing UL/IEC 62368-1) without depleting resources for other soft gates. |

---

## Committed Cash vs. Expected Cash: The Con Advocate’s View

We spend a small, prudent amount now to eliminate the catastrophic risk. The Pro’s plan shows $0 committed but a 0.4% chance of a $31,000 catastrophe—that’s a skewed statistic when the probability of the single ISS-014 slip is much higher at 25%, triggering a chain of events that kills our schedule even if all the money is eventually spent.

| | Pro Advocate | Con Advocate |
| :--- | :--- | :--- |
| **Committed Cash** | **$0** | **$8,300** |
| **Expected Cash** | $4,250 | **$7,600** (approx) |
| **Worst-Case Cash** | $31,000 | $28,300 |
| **Remaining Contingency (worst case)** | $80,600 | $83,300 |

My plan leaves $83,300 in contingency in the absolute worst case, a trivial difference from the Pro’s plan. But the cost of the Pro’s plan failing is a missed 08/18 cert gate, which costs us the #1 strategic objective. **The Brain’s strategy is our fiduciary duty, and my proposal spends a fraction of our remaining contingency to actually guarantee it.**