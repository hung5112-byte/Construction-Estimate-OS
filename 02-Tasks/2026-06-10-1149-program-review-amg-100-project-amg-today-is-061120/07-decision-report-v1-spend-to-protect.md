---
type: decision_report
stop: 1
---
## 📌 Bottom line (30-second read)

- **Do not start the build on June 22** — three things must happen first: prove the battery fix actually works, confirm why the production pass rate is low and write the fix into official build instructions, and complete a payment-security hardware review by June 18.
- **A short 5–7 day delay (to June 27–29) is recoverable** — but if the build starts June 22 and then fails on quality or battery safety, the August 18 certification deadline will be missed with no time left to recover.
- **Approve ~$127K from the contingency reserve** — this requires a formal $15K reallocation since only $111.6K is currently available; a separate $136K for parts and supply chain must go through the capital budget, not contingency.
- **Start two free actions today:** have the sole antenna engineer begin writing down all technical decisions, and launch a search for a backup specialist — both protect the program from depending entirely on one person.
- **One more flag for later:** the device's predicted failure rate is seven times worse than the target — this must be fixed before the September beta trial is approved, or large customers will see far more broken devices than promised.

---

# Decision Report: AMG-100 First Verification Build Readiness & Program Improvement Plan

---

## 📌 Summary (30-second read)

- **Do not approve the start of the first verification build on 06/22 until three firm conditions are met.** All five departments and every analytical view reached the same conclusion independently: the program can be saved, but it is not ready to move forward as it stands.

- The three conditions blocking progress are: (1) the battery fix must be fully tested and proven (right now, we know what is wrong but have not yet proven the fix works), (2) the reason our production pass rate is low must be fully confirmed and the fix written into the approved build instructions — a frequency chart alone is not enough, and (3) a review of payment-security gaps in the hardware must be completed by 06/18.

- A **deliberate 5–7 day delay** to around 06/27–06/29, decided today with full awareness, can still be recovered within the certification deadline. Starting the build on 06/22 and then failing on production quality or battery safety will use up every remaining day of schedule buffer and cause us to miss the 08/18 certification hard deadline.

- **Spend approximately $127K from our contingency reserve** (the set-aside budget for unexpected problems). We currently have $111.6K available, so this requires a formal $15K reallocation. A further $136K for parts inventory and supply-chain items should go through separate capital budget approvals, not the contingency reserve.

- **Start two no-cost actions today:** our current radio-frequency engineer begins writing down all antenna decisions, and we launch a search for a specialist contractor. Both actions protect the certification path from the risk of depending entirely on one person — at no immediate cost.

---

## Recommendation

**Approve with conditions** — authorize the first verification build, but only after the three firm conditions below are met. The program is technically recoverable. The commercial window is still intact if those conditions are closed by 06/19–06/21.

---

## Changes from the original plan

| Item | Original plan | Recommendation | Reason |
|---|---|---|---|
| Verification build start date | 06/22 (fixed) | 06/22 **if** three firm conditions are met on time; otherwise slip to approximately 06/27–06/29 | The battery fix and production pass-rate root cause cannot be skipped. A failed build costs more time than a short, planned delay. |
| Payment-security review date | 06/25 (implied) | **06/18 — moved 7 days earlier** | Hardware-level payment-security gaps found after build approval would require a complete rebuild of the circuit board. Spending $8K now avoids a program-restructuring cost later. |
| Radio-frequency contractor hire target | 06/20 | **06/25** (realistic for specialist placement) | Specialist contractors typically take 2–4 weeks to place. Our current engineer begins documentation today to cover the gap. |
| Pre-production parts inventory for Tet market / BrightPath ***(BrightPath — our contract manufacturer, the outside company that builds our devices)*** | Treated as contingency spend | **Separate capital budget approval** | $95K in inventory is recoverable through revenue, but it is still a cash outlay. It must not be mixed into the $111.6K contingency reserve. |
| **MTBF** (Mean Time Between Failures — a measure of how long a device is expected to run before breaking down; for example, a figure of 62,000 hours means the device is predicted to run about 7 years before a failure) gap | Treated as a minor reliability note | **Condition for approving the beta trial** (not a condition for the build) | Our current MTBF figure implies a 14.1% annual failure rate against a 2.0% target — seven times worse. This must be on record. An updated prediction is required before beta trial approval. |

---

## Detailed analysis

### What each department said

**Hardware Engineering (Dept 01)** issued the sharpest warning of any single team. The antenna rework fix for issue ISS-014 has been tested on zero reworked units. Without **S-parameter** (a measurement of how efficiently radio signals move through the antenna — think of it as a signal efficiency score) data before 06/22, we would be committing more than 100 verification build circuit boards to an unproven fix. The team also noted that the root cause of our low production pass rate has not been broken down by individual component or connection, that the document defining how security keys are programmed into devices at the factory is still unsigned, and that our sole radio-frequency engineer (R-09) is a single point of failure for both our government radio certification and the next-generation product platform. Hardware Engineering recommended making four deliverables a firm condition for build entry, all due by 06/19.

**NPI Program Management** (**NPI** — New Product Introduction — the end-to-end process of taking a product from design to mass production; Dept 02) confirmed the exact schedule sequence: parts arrive 06/16 → inspection clears 06/17 → **BOM** (Bill of Materials — the master list of every part that goes into the device, like a recipe ingredient list) is frozen 06/18 → build starts 06/22 → payment-security pre-assessment 07/06 → hard deadline 08/18. Every step in that chain has zero spare time. Dept 02 approved approximately $25–50K in additional targeted spending to reduce risk on the critical path, and identified nine open issues that need to be checked for certification relevance before the build starts.

**Quality & Reliability (Dept 03)** placed a conditional hold on the build for four reasons: the battery **8D process** (Eight Disciplines — a structured eight-step problem-solving method; think of it as a formal checklist for diagnosing and fixing a serious defect) is stuck at **D6** (step six out of eight — the root cause is confirmed but the fix has not yet been proven to work), our production pass rate is 78% with no published **Pareto** (a frequency-ranked list of failures, showing which problems occur most often — named after the principle that a small number of causes drive most failures) analysis, there is no spare time in the certification path after 08/18, and engineer R-09 is a single point of failure for the radio section. Dept 03 stated clearly: a verification build without defined pass criteria is not a gate — it is a party.

**Manufacturing & Supplier Quality (Dept 04)** added three independent blocking conditions beyond those named by other departments: the re-test rate from our earlier **EVT** (Engineering Verification Test — the build round where engineering confirms that design corrections actually work, typically the second or third physical build before mass production) is unknown, meaning the 78% headline pass rate may itself be unreliable; the **golden sample** (the physical reference unit against which all production units are compared — the "master copy") for the antenna rework has not been signed off by the supplier's quality team; and the radio-frequency test station cannot be re-qualified after the antenna geometry change in just three days. Dept 04 also confirmed that having only one approved supplier for the **eMMC** (embedded flash storage — the built-in memory chip that stores the device's software and data, similar to the storage chip in a smartphone) is a hard violation of our **AVL** (Approved Vendor List — the official list of suppliers whose parts we are allowed to use; using a part from a supplier not on this list is a compliance violation), not merely a scheduling note.

**Service Operations (Dept 05)** flagged that the repair infrastructure — repair guides, fault-code categories, and spare-parts inventory sizing — does not yet exist for the AMG-100. At a 78% production pass rate, roughly one in every five units returned to the repair bench becomes undiagnosable noise without standardized diagnostics. Dept 05 also raised the most time-sensitive single logistics issue: customs clearance for the ISS-014 antenna parts must be confirmed with our broker **today** — not just assumed — because these parts fall under **49 CFR / IATA DG** (federal and international rules governing how lithium battery assemblies are classified, packaged, and transported through customs — non-compliance can result in shipments being held or destroyed) lithium battery transport regulations.

---

### The case for moving forward vs. the case for caution

**The case for moving forward:**
- The verification build is the right mechanism for confirming that process corrections work, **provided** that the failure causes are confirmed and the fixes are written into approved build instructions before the build starts. Requiring a separate standalone test lot would effectively be running a third engineering verification round — that is not standard practice for new product introduction. 
- The budget is $127K (not $263K) once parts inventory and supply-chain items are correctly moved to their own capital budget lines. The gap versus our $111.6K contingency reserve is only $15K, which requires one formal reallocation — not a financial workaround.
- On a 10,000-unit mass-production run at $138.18 gross profit per unit, every one percentage point recovered in production pass rate equals approximately $13,818 in recovered profit. Recovering 10 percentage points equals $138,180 in recovered margin — a 5.7× return on the de-risking spend.
- Every week of delay is a week a competitor occupies a market position we should own. **VP of Operations** (VP — Vice President of Operations — a senior buyer responsible for running a company's day-to-day facilities and purchasing decisions) buyers are purchasing now.

**The case for caution:**
- A frequency chart is not root cause closure. True root cause closure requires: confirmed failure mechanism, a specified process correction, and that correction written into the build instructions. The action plan delivers a frequency chart by 06/18 — just four days before the build — leaving no time to verify even the most basic fix.
- The original budget framing was broken: $263K was presented against $111.6K in contingency, with "reallocation from already-spent dollars" proposed as the solution. Money that has already been spent cannot be reallocated.
- The battery fix being unproven is not a minor paperwork item. In a device running continuously in a harsh environment, a battery with an unvalidated fix is a heat risk and a lithium battery regulatory risk under 49 CFR / IATA DG rules. If a unit fails thermally during the September beta trial, the consequence is not a standard **RMA** (Return Merchandise Authorization — the formal process for a customer to return a faulty unit for repair or replacement) — it is a regulatory incident.
- The payment-security review on 06/25 is too late. Hardware-level gaps in **PCI PTS** (Payment Card Industry — Payment Terminal Security — the hardware and software security standard that payment devices must meet to legally process card transactions; for example, it governs tamper-proof enclosures and how encryption keys are stored) — such as the tamper-detection mesh, the key-programming architecture, and the secure chip design — cannot be patched in software. They require a circuit-board redesign. A circuit-board issue found on 06/25, after build approval, means a full rebuild of the verification units and a missed 08/18 deadline.

**Conclusion:** The caution case wins on the three firm conditions (battery fix proven, production pass-rate root cause closed, payment-security review brought forward) and on budget discipline. The forward case wins on the question of whether a separate test lot is needed (it is not, if the conditions are met before build start) and on the commercial urgency. These two positions are not in conflict: spend the money, close the three conditions, then build — on 06/22 if the conditions are met on time, or on 06/27–06/29 if the battery fix requires more time.

---

### Three viewpoints

**Viewpoint 1 — Growth:** Spend $263K total (correctly split: $127K from contingency, $136K from separate capital approvals), start the build on 06/22, and protect the September beta window. The commercial advantage favors urgency. Every action adds rigor without removing a gate. The proposed 84% pass-rate pause gate during the build is tighter than our baseline.

**Viewpoint 2 — Caution:** The **MTBF** gap has been underweighted by both sides. At **ICP** (Ideal Customer Profile — the description of the type of customer most likely to buy and succeed with our product; in this case, large multi-site operators) scale — 500 locations × 30 devices = 15,000 units — a 14.1% annual failure rate means approximately 2,115 device failures per year against a target of 300. Shipping a device with this reliability profile to buyers who chose us specifically because we promised greater than 99.5% uptime across their fleet is not a quality problem — it is an existential commercial risk. The build is not delayed for MTBF alone, but beta trial approval must be conditioned on an updated reliability prediction that shows a credible path to 2.0% or lower annual failure rate.

**Viewpoint 3 — Balanced:** Both viewpoints are correct in their own areas. Three firm conditions must be met before build approval — non-negotiable. Six targeted contingency spends totalling approximately $127K should be authorized. Two no-cost actions start today (RF documentation and contractor search). Beta trial approval is separately conditioned on an updated reliability prediction. A deliberate 5–7 day slip, if the battery fix requires it, is decided today — not discovered mid-build.

---

## Actions required before launch (BLOCKERS)

All items are listed by date. Items marked 🔴 are hard stops — the build does not start without them.

---

**06/11 (TODAY):**
- [ ] 🔴 Current radio-frequency engineer (R-09) begins a technical documentation file covering all antenna tuning decisions, test setups, and pre-certification data — starts today, costs $0
- [ ] 🔴 Search for a specialist radio-frequency contractor is launched through a specialist placement firm — starts today, $0 until placement
- [ ] 🔴 ISS-014 antenna parts: confirm customs clearance with our broker today; authorize a dedicated **DG courier** (a carrier licensed to transport Dangerous Goods — in this case, lithium battery assemblies — under 49 CFR / IATA DG regulations) if there is any risk of a hold (~$8–15K, Service Operations)
- [ ] Request a full forward budget estimate (verification build through beta trial) from NPI Program Management (Dept 02) — confirms whether the remaining $1,016K non-contingency budget is sufficient before any contingency draw is approved

**06/13:**
- [ ] 🔴 Battery 8D **D7** (step seven of eight — this is where the fix is physically tested and proven to work under real conditions) completion plan delivered in writing by Hardware Engineering (Dept 01) and Quality (Dept 03): physical test protocol, a committed completion date of 06/21 or earlier, and actual cost difference. If the date is later than 06/21, the build start slips to the day after D7 is confirmed.
- [ ] A named internal **PCI** (Payment Card Industry — the set of security standards that any company handling card payments must meet) lead is assigned — must have prior PCI PTS assessment experience
- [ ] ISS-014 antenna parts **ETA** (Estimated Time of Arrival — the confirmed delivery date from the supplier) confirmed in writing from the supplier; air freight backup ($12K) authorized if there is any risk of the parts arriving after 06/17

**06/14:**
- [ ] Written inspection checklist for incoming antenna rework parts — acceptance criteria approved by Hardware Engineering (Dept 01) and Quality (Dept 03) before the parts arrive on 06/16, not upon receipt. Cost: $0

**06/15:**
- [ ] All non-antenna BOM parts pre-staged at the contract manufacturer — 100% ready (+$8K in expedited labor)
- [ ] Forward budget estimate delivered by NPI (Dept 02) — required before any contingency draw is approved

**06/16:**
- [ ] **CM** (Contract Manufacturer — **BrightPath**, the outside company that physically builds our devices) dedicated build team placed on standby, with no line reassignment ($15K labor hold)
- [ ] **EVT** production pass-rate frequency analysis (Pareto) published by Quality (Dept 03) and Manufacturing & Supplier Quality (Dept 04) — top three failure modes with named owners. *This is the input to root cause closure, not the closure itself.*

**06/17:**
- [ ] ISS-014 antenna parts received and inspected against the pre-defined checklist; written factory receiving confirmation provided
- [ ] **ECO** (Engineering Change Order — a formal document that officially records a design change and ensures it is reflected in all build instructions and specifications) for the antenna, signed, with the certification-relevance box completed
- [ ] **EVT** re-test rate audit completed by the Factory Test and Yield team — confirms whether the 78% headline pass rate is accurate or distorted by units being retested multiple times

**06/18:**
- [ ] 🔴 **QSA** (Qualified Security Assessor — a PCI-certified third party authorized to review whether our device meets payment-security hardware requirements) gap review completed — on-site hardware-level PCI PTS assessment (~$8K). Any hardware gaps must be resolved before build approval is given.
- [ ] DVT **BOM** (Bill of Materials — the master parts list) frozen at a locked revision

---

## ⚠️ Warning: claims missing a source

The following sentences contain figures or legal references but no clear citation was found. The Department Head should verify them before proceeding:

- **[Line 8] Figure:** - **A short 5–7 day delay (to June 27–29) is recoverable** — but if the build starts June 22 and then fails on quality or battery safety, the August 18 certification deadline will be missed with no ti
- **[Line 9] Figure:** - **Approve ~$127K from the contingency reserve** — this requires a formal $15K reallocation since only $111.6K is currently available; a separate $136K for parts and supply chain must go through the 
- **[Line 25] Figure:** - A **deliberate 5–7 day delay** to around 06/27–06/29, decided today with full awareness, can still be recovered within the certification deadline.
- **[Line 27] Figure:** - **Spend approximately $127K from our contingency reserve** (the set-aside budget for unexpected problems).
- **[Line 27] Figure:** We currently have $111.6K available, so this requires a formal $15K reallocation.
- **[Line 27] Figure:** A further $136K for parts inventory and supply-chain items should go through separate capital budget approvals, not the contingency reserve.
- **[Line 57] Figure:** Dept 02 approved approximately $25–50K in additional targeted spending to reduce risk on the critical path, and identified nine open issues that need to be checked for certification relevance before t
- **[Line 59] Figure:** **Quality & Reliability (Dept 03)** placed a conditional hold on the build for four reasons: the battery **8D process** (Eight Disciplines — a structured eight-step problem-solving method; think of it
- **[Line 63] Figure:** At a 78% production pass rate, roughly one in every five units returned to the repair bench becomes undiagnosable noise without standardized diagnostics.
- **[Line 63] Legal:** Dept 05 also raised the most time-sensitive single logistics issue: customs clearance for the ISS-014 antenna parts must be confirmed with our broker **today** — not just assumed — because these parts
- **[Line 71] Figure:** - The budget is $127K (not $263K) once parts inventory and supply-chain items are correctly moved to their own capital budget lines.
- **[Line 71] Figure:** The gap versus our $111.6K contingency reserve is only $15K, which requires one formal reallocation — not a financial workaround.
- **[Line 72] Figure:** - On a 10,000-unit mass-production run at $138.18 gross profit per unit, every one percentage point recovered in production pass rate equals approximately $13,818 in recovered profit.
- **[Line 72] Figure:** Recovering 10 percentage points equals $138,180 in recovered margin — a 5.7× return on the de-risking spend.
- **[Line 77] Figure:** - The original budget framing was broken: $263K was presented against $111.6K in contingency, with "reallocation from already-spent dollars" proposed as the solution.
- **[Line 78] Legal:** In a device running continuously in a harsh environment, a battery with an unvalidated fix is a heat risk and a lithium battery regulatory risk under 49 CFR / IATA DG rules.
- **[Line 87] Figure:** **Viewpoint 1 — Growth:** Spend $263K total (correctly split: $127K from contingency, $136K from separate capital approvals), start the build on 06/22, and protect the September beta window.
- **[Line 87] Figure:** The proposed 84% pass-rate pause gate during the build is tighter than our baseline.
- **[Line 89] Figure:** At **ICP** (Ideal Customer Profile — the description of the type of customer most likely to buy and succeed with our product; in this case, large multi-site operators) scale — 500 locations × 30 devic
- **[Line 89] Figure:** Shipping a device with this reliability profile to buyers who chose us specifically because we promised greater than 99.5% uptime across their fleet is not a quality problem — it is an existential com
- **[Line 89] Figure:** The build is not delayed for MTBF alone, but beta trial approval must be conditioned on an updated reliability prediction that shows a credible path to 2.0% or lower annual failure rate.
- **[Line 91] Figure:** Six targeted contingency spends totalling approximately $127K should be authorized.
- **[Line 91] Figure:** A deliberate 5–7 day slip, if the battery fix requires it, is decided today — not discovered mid-build.
- **[Line 102] Figure:** - [ ] 🔴 Current radio-frequency engineer (R-09) begins a technical documentation file covering all antenna tuning decisions, test setups, and pre-certification data — starts today, costs $0
- **[Line 103] Figure:** - [ ] 🔴 Search for a specialist radio-frequency contractor is launched through a specialist placement firm — starts today, $0 until placement
- **[Line 104] Figure:** - [ ] 🔴 ISS-014 antenna parts: confirm customs clearance with our broker today; authorize a dedicated **DG courier** (a carrier licensed to transport Dangerous Goods — in this case, lithium battery as
- **[Line 105] Figure:** - [ ] Request a full forward budget estimate (verification build through beta trial) from NPI Program Management (Dept 02) — confirms whether the remaining $1,016K non-contingency budget is sufficient
- **[Line 110] Figure:** - [ ] ISS-014 antenna parts **ETA** (Estimated Time of Arrival — the confirmed delivery date from the supplier) confirmed in writing from the supplier; air freight backup ($12K) authorized if there is
- **[Line 116] Figure:** - [ ] All non-antenna BOM parts pre-staged at the contract manufacturer — 100% ready (+$8K in expedited labor)
- **[Line 120] Figure:** - [ ] **CM** (Contract Manufacturer — **BrightPath**, the outside company that physically builds our devices) dedicated build team placed on standby, with no line reassignment ($15K labor hold)
- **[Line 126] Figure:** - [ ] **EVT** re-test rate audit completed by the Factory Test and Yield team — confirms whether the 78% headline pass rate is accurate or distorted by units being retested multiple times
- **[Line 129] Figure:** - [ ] 🔴 **QSA** (Qualified Security Assessor — a PCI-certified third party authorized to review whether our device meets payment-security hardware requirements) gap review completed — on-site hardware
