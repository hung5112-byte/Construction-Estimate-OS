---
type: meeting_r3
---
# Round 3 — Perspective Debate

GROWTH: # GROWTH POSITION — AMG-100 Program Review
## 06/11/2026 | Round 1

---

## Opening Frame

Our 2030 vision is unambiguous: **#1 hardware platform for in-venue guest engagement in US casual dining, every table running an LSI device, >99.5% fleet uptime.** The AMG-100 at $329 ASP and 42% gross margin is the product that gets us there. The TS-90 at $289 and 35% margin is holding ground, not gaining it.

The Con Advocate has raised five structural objections. I will address each directly. But first, let me reframe what is actually at stake.

**The asymmetry of this decision is not about $263K versus $118K. It is about what happens to the casual dining market window if we are not in September beta.**

Our ICP — VP of Operations and CIO buyers at 50–1,200 location chains — is actively purchasing now. Labor shortage is not a 2027 problem; it is a 2026 problem. Every server covering more tables because guests cannot self-pay at a working device is lost revenue *today*. If we are not in beta in September, we are not in commercial deployment in Q1 2027. If we are not in Q1 2027, we are watching a competitor occupy the table. That competitor does not give it back.

**With that stakes context established, here is my prioritized plan.**

---

## Where Con and I Actually Agree (Intellectual Honesty First)

Before I defend the bold position, I will confirm where Con is right, because credibility matters:

1. **QSA gap review must move to 06/18, not 06/25.** Con is correct. Seven days of earlier visibility on hardware-level PCI gaps could save a DVT respin. I am adopting this.

2. **RF contractor search starts today, 06/11.** Con is correct that nine days is optimistic for specialist placement. Search initiates immediately; realistic onboard target is 06/25. Documentation starts with the incumbent today.

3. **Tet pre-build authorization belongs in a capital inventory line, not contingency.** Con is correct on budget hygiene. I am separating it.

4. **Battery D7 completion plan must be written and dated by 06/13.** If Hardware Engineering (Dept 01) cannot produce a credible D7 completion plan in 48 hours, we have a bigger problem than scheduling.

These are not concessions that weaken the growth position. They are precision corrections that make the plan more executable. Now here is where Con is wrong, and why it matters.

---

## Where Con Is Wrong: The Five-Flaw Rebuttal

---

### Con's Flaw 1 — "Pareto Is Not Root Cause Closure"

Con argues that completing a Pareto by 06/18 leaves only four days to implement process corrections, run a verification lot, and confirm the fix — and that four days is not credible.

**Con is right about the definition. Con is wrong about the implication.**

Root cause closure for a yield problem does not always require a new verification lot before DVT build start. Here is why:

DVT *is* the verification lot for process corrections that have been implemented but not yet run at build scale. The entire function of DVT yield monitoring — including the 84% pause gate I proposed — is to confirm whether process corrections hold at build. If we require a full verification lot before DVT build authorization, we are requiring what is functionally a third EVT run. That is not how the NPI process works at any company running hardware at this cadence.

**What is required before 06/22 is not a verification lot. It is:**
- Confirmed failure mechanism (not just a Pareto — actual root cause)
- Process correction specified and implemented in the DVT build instructions
- DVT build instructions reviewed and approved by Quality (Dept 03) before build start

The 84% pause gate after the first 50 units is precisely the verification mechanism. If process corrections are wrong, we find out at unit 50, not unit 200. That is risk-controlled, not reckless.

**My action:** Hardware Engineering (Dept 01) and MSQ (Dept 04) must deliver confirmed failure mechanism and specified process correction — not just a Pareto — by 06/19. DVT build instructions incorporating those corrections must be approved by Quality (Dept 03) before 06/22 build authorization. The 84% pause gate is the in-build verification.

**This is tighter than baseline, not looser.**

---

### Con's Flaw 2 — "The Budget Math Is Broken"

Con's critique: $263K against $111.6K contingency is a $151K overrun, and reallocating from already-spent dollars is an accounting shell game.

**Con is correct that spent dollars cannot be reallocated. Con is wrong about what the $263K actually represents.**

Let me disaggregate the $263K:

| Item | Amount | Category |
|---|---|---|
| P1 DVT build protection | $35K | Operating — contingency eligible |
| P2 Yield engineering | $24K | Operating — contingency eligible |
| P3 RF contractor | $45K | Operating — contingency eligible |
| P4 PCI pre-assessment | $14K | Operating — contingency eligible |
| P5 eMMC buffer inventory | $26K | Supply chain inventory — separate line |
| P6 Battery 8D testing | $9K | Operating — contingency eligible |
| P7 Tet pre-build | $95K | Capital inventory — separate authorization |
| P7 Second-site qualification | $15K | Supply chain — separate line |
| **Operating contingency draw** | **$127K** | |
| **Separate capital/supply chain** | **$136K** | |

**Contingency draw is $127K, not $263K.** Against $111.6K remaining contingency, the overage is $15.4K — not $151K. That $15.4K requires one formal reallocation request from the program's remaining $1,128K budget. This is not a shell game; it is standard NPI program accounting.

**The capital and supply chain items ($136K) require separate authorization, which I explicitly support.** Con's $118K contingency plan and my $127K contingency plan differ by $9K (the battery D7 test cost that Con marks as "TBD"). When Con's "TBD" resolves, our numbers converge.

**The material difference between Con's plan and mine is not the contingency math. It is that Con defers $136K of supply chain and inventory action to separate processes with no committed dates, while I am committing to parallel execution.**

---

### Con's Flaw 3 — "Battery D7 Is a Hard Build Stop"

Con argues that D6 → D7 completion by 06/21 is not a $0 action and may not be achievable on that timeline.

**Con is 100% correct that D7 is a hard build stop. Con is 100% correct that it is not $0.** I acknowledge the Pro position understated this.

Here is the growth-side position: **we need to know the D7 completion cost and date in 48 hours, not in two weeks.**

If Hardware Engineering (Dept 01) delivers a D7 completion plan by 06/13 that says "D7 achievable by 06/20 with $18K in accelerated validation testing," we fund it immediately and build starts 06/22.

If the plan says "D7 requires hardware iteration, achievable by 06/28 with $35K," we slip DVT to 06/29 — a 7-day slip — and we still have a defensible cert path if the 08/18 window has any give.

**What the growth position refuses to accept is using "we don't know the D7 cost yet" as a reason to not start the clock.** The clock started today. D7 plan is due 06/13. Fund it from contingency when we know the number. Do not let uncertainty become delay.

**The battery risk is real. The answer is acceleration, not postponement.**

---

### Con's Flaw 4 — "PCI Timing Has a Structural Gap"

Con argues the QSA gap review on 06/25 is too late because hardware-level PCI gaps discovered after DVT build authorization cannot be corrected without a respin.

**Con is right. I am moving the QSA gap review to 06/18.** I said so in the agreement section above.

But I want to be precise about what Con is implicitly arguing: that PCI hardware gaps are likely. That is not established. ISS-027 and ISS-028 are open, but their severity is not described in the Brain as hardware-level architectural failures. If they were, our internal PCI lead would have escalated before now.

The 06/18 QSA gap review is worth $8K regardless of severity assessment, because the cost of being wrong is a DVT respin. This is not a close call. We spend $8K, we learn by 06/18, we have four days to respond before build start if something surfaces.

**Growth position: spend the $8K, move the date, stop treating this as a Con victory. It is just good program management.**

---

### Con's Flaw 5 — "RF Hire Timeline Is Wishful"

Con argues that a specialist RF/antenna contractor cannot be placed in nine days and that the realistic timeline is 06/25, not 06/20.

**Con is probably right on the timeline. I am adjusting to 06/25 as the realistic onboard target.**

But here is what Con misses: the most important R-09 mitigation action is not hiring the contractor. It is getting the incumbent RF engineer to start the technical documentation file **today**. If the contractor arrives 06/25 and finds a complete antenna tuning decision log, pre-compliance data summary, and test setup documentation, that contractor can be productive on day one. If the contractor arrives 06/25 and finds nothing documented, we have lost two weeks.

**My action, effective 06/11:** Incumbent RF engineer begins technical documentation file today. Contractor search initiates today. Target onboard 06/25. The $45K spend is unchanged; the sequence is corrected.

---

## The Prioritized Plan (Growth Version, Precision-Corrected)

### PRIORITY 1 — DVT Build Date: 06/22 (Non-Negotiable Unless Conditions Force Slip)

**Three hard conditions for build authorization (incorporating Con's valid points):**

| Condition | Owner | Due | Cost |
|---|---|---|---|
| Yield root cause confirmed: failure mechanism + process correction specified in DVT build instructions, approved by Quality (Dept 03) | HW Eng (01) + MSQ (04) + Q&R (03) | 06/19 | $6K contractor support |
| Battery 8D D7 completion plan delivered with committed date and cost | HW Eng (01) + Q&R (03) | 06/13 | $0 (if D7 ≤ 06/21) or slip DVT to D7+1 |
| QSA gap review complete, hardware-level PCI gaps dispositioned | NPI (02) + HW Eng (01) | 06/18 | $8K |
| Antenna parts confirmed in writing, air freight contingency reserved | MSQ (04) | 06/13 | $12K freight contingency |
| All non-antenna BOM pre-kitted at CM | NPI (02) | 06/15 | $8K expedite labor |
| CM build team on standby 06/16–06/22 | NPI (02) | 06/16 | $15K labor hold |

**Schedule logic:** If all three hard conditions are met by their dates, build starts 06/22. If battery D7 requires a slip, DVT moves to D7+1. A 7-day slip to 06/29 is recoverable; a failed DVT build because D7 was not complete is not.

---

### PRIORITY 2 — Yield: EVT 78% → DVT 88% Target

**The 84% pause gate after first 50 units is the verification mechanism for process corrections.** This is tighter than baseline.

| Action | Owner | Due | Cost |
|---|---|---|---|
| Failure mechanism confirmed + process correction in build instructions | HW Eng (01) + MSQ (04) | 06/19 | $6K |
| DVT sample size increased by 15 units for statistical signal | NPI (02) | 06/22 | $18K |
| 84% pause gate after first 50 units — hard stop for 48-hour analysis if triggered | Q&R (03) | 06/22 | $0 |

**P2 total: $24K**

At AMG-100's $329 ASP and 42% margin, the gross profit per unit is **$138.18**. Every percentage point of yield improvement at 10,000-unit MP scale = ~$13,818 in recovered gross profit. Closing 10 yield points = **$138,180 in margin recovery**. The $24K spend has a 5.7x return if it closes the gap.

---

### PRIORITY 3 — RF Bus-Factor Elimination (R-09)

| Action | Owner | Due | Cost |
|---|---|---|---|
| Incumbent RF engineer begins technical documentation file | HW Eng (01) | **06/11 (today)** | $0 |
| RF specialist contractor search initiated | HW Eng (01) | **06/11 (today)** | $0 |
| Contractor onboarded | HW Eng (01) | 06/25 | $45K (3 mo.) |
| Cross-train backup engineer on antenna test procedures | HW Eng (01) | 07/01 | $0 |

**P3 total: $45K**

This is the cheapest catastrophic-risk insurance in the program. One engineer unavailability without documentation costs the entire cert path. $45K eliminates that scenario.

---

### PRIORITY 4 — PCI Pre-Assessment: QSA Gap Review 06/18

| Action | Owner | Due | Cost |
|---|---|---|---|
| QSA gap review (moved from 06/25 to 06/18) | NPI (02) + HW Eng (01) | 06/18 | $8K |
| Dedicated internal PCI lead assigned (named individual, PTS experience required) | NPI (02) | 06/13 | $0 |
| PCI firmware hardening complete, firmware frozen | HW Eng (01) | 07/01 | $0 |
| Remediation window pre-booked at PCI lab 07/07–07/14 | NPI (02) | 06/20 | $6K |

**P4 total: $14K**

The 06/18 date is the correction that matters. If a hardware-level PCI gap surfaces on 06/18, we have four days before build start to disposition it. If it surfaces on 06/25, we have zero days. **$8K buys a week of decision time.** This is among the highest-ROI single actions in the entire plan.

---

### PRIORITY 5 — eMMC Dual-Source (Two-Sources Rule: Inviolable)

| Action | Owner | Due | Cost |
|---|---|---|---|
| Second-source qualification timeline confirmed — must complete before MP ramp gate | MSQ (04) | 06/18 | $0 |
| 15% of DVT units use second-source eMMC for accelerated validation | HW Eng (01) + MSQ (04) | 06/22 | $4K |
| If second-source qualification cannot complete before MP gate: 90-day buffer inventory on primary source | MSQ (04) | 06/20 | $22K inventory |

**P5 total: $26K (supply chain budget line, not contingency)**

The two-qualified-sources rule cannot be waived. The buffer inventory is a bridge to qualification completion, not a workaround. Separate capital authorization.

---

### PRIORITY 6 — Battery 8D D7 + MTBF

**Definition note:** *8D* is an eight-discipline problem-solving methodology. D6 = root cause confirmed. D7 = corrective action implemented and verified effective. D7 is required before DVT build start per Quality (Dept 03).

**Definition note:** *MTBF* (Mean Time Between Failures) at 62,000 hours implies an Annual Failure Rate of approximately 12.9% (AFR = 8,760/MTBF × 100). Target AFR is 2.0%, implying required MTBF ≥ 438,000 hours. **This is a significant gap that the Brain data flags but neither advocate has fully quantified.**

| Action | Owner | Due | Cost |
|---|---|---|---|
| D7 completion plan delivered (mechanism, test protocol, committed date) | HW Eng (01) + Q&R (03) | 06/13 | $0 |
| D7 corrective action validated — hard build prerequisite

CAUTIOUS: # CAUTIOUS POSITION — AMG-100 Program Review
## 06/11/2026 | Round 1

---

## Opening Statement

I am not here to kill AMG-100. I am here to make sure we do not spend $2.0M building toward a September beta trial and then discover in August that we have a product whose yield mechanism we never confirmed, whose battery corrective action was never validated, and whose PCI certification has a hardware-level gap we could have found in June for $8,000.

The Pro Advocate and Growth Advocate have produced aggressive plans. Several of their actions are correct. Several contain a structural pattern I will call **hope-based scheduling** — asserting that a condition will be met by a date without explaining *how* it gets met, then treating that assertion as a closed risk.

My job is to find the scenarios where this program fails and set concrete conditions that prevent us from discovering those scenarios at the worst possible moment.

Let me define terms I will use, then work through the evidence.

---

## Jargon Definitions (Plain English)

**DVT** — Design Validation Test. The build phase where a near-production design is assembled and tested to confirm it meets specifications. Failure here means redesign; schedule impact is severe.

**EVT** — Engineering Validation Test. Earlier build phase; establishes baseline performance. Our EVT yield was 78%.

**8D / D6 / D7** — Eight-Discipline problem-solving methodology. D6 = root cause identified and confirmed. D7 = corrective action *implemented and verified effective* with test evidence. D7 is not a paperwork step; it requires physical validation data.

**MTBF** — Mean Time Between Failures, in hours. At 62,000 hours, implied Annual Failure Rate = 8,760 ÷ 62,000 = **14.1% AFR**. Target AFR is 2.0%, implying required MTBF ≥ 438,000 hours. **This gap has not been adequately surfaced in this review.**

**AFR** — Annual Failure Rate. The percentage of deployed units expected to fail in a 12-month period.

**PCI PTS** — Payment Card Industry Payment Terminal Security. A hardware and software security standard mandatory for any device processing card payments. Hardware-level failures at assessment cannot be patched; they require physical redesign.

**FCC Part 15** — US Federal Communications Commission equipment authorization for unintentional radiators. Required before any commercial sale. Antenna design changes after authorization require re-testing.

**RMA** — Return Merchandise Authorization. A returned failed unit.

**Tet** — Lunar New Year. A multi-week factory shutdown period at Chinese/Vietnamese contract manufacturers. Missing the pre-build window creates a supply gap.

**BrightPath** — Our single contract manufacturer. "Single-site risk" means one fire, flood, labor action, or COVID-equivalent event at BrightPath stops all production.

**eMMC** — Embedded MultiMediaCard. Flash storage component. Single-source qualification means only one approved supplier; if that supplier has a shortage or quality event, production halts.

**QSA** — Qualified Security Assessor. A PCI-certified third party authorized to conduct PTS assessments.

**NPI** — New Product Introduction. The end-to-end process from design to mass production.

**PRT** — Product Reliability Test. A structured test program that validates field reliability before launch.

**ASP** — Average Selling Price. AMG-100 ASP: $329 (per products.md). Gross margin: 42%, meaning gross profit per unit = **$138.18**.

---

## THE MTBF PROBLEM NOBODY IS QUANTIFYING

Before I address the seven review areas, I need to surface a number that both advocates have treated as a footnote.

**MTBF at 62,000 hours implies a 14.1% AFR.** Target is 2.0% AFR.

At our ICP's scale — a 500-location chain running 30 devices per site = 15,000 deployed units — a 14.1% AFR means **2,115 field failures per year**. Our 2.0% target means 300. That is a 7x gap in RMA volume.

The Brain's strategy vision is explicit: **>99.5% fleet uptime**. The ICP pain point is explicit: **"device downtime kills revenue at the table."** A 14.1% AFR does not support 99.5% uptime under any reasonable repair-cycle assumption. Even if depot turns units in 48 hours, a chain with 2,115 annual failures is not experiencing 99.5% uptime — it is experiencing something closer to 94–96%, depending on fleet size and repair logistics.

**No action in either advocate's plan closes the MTBF gap before DVT build start.** I am not saying DVT should be delayed for MTBF alone. I am saying that if we enter DVT without a credible path to ≥438,000 hours MTBF, we should not be authorizing a September beta trial. Shipping a device with 14.1% AFR to VP of Operations buyers who explicitly selected us for uptime reliability is not a quality problem — it is an existential commercial risk.

**My requirement:** Quality & Reliability (Dept 03) must publish an updated MTBF prediction incorporating EVT failure data and identified improvement actions by 06/18 — before DVT build authorization, not after. If the updated prediction does not show a credible path to ≤2.0% AFR by MP ramp, that is a program-level decision that executive leadership must make with full information.

---

## AREA 1 — Schedule Risk: DVT Build Readiness

### Antenna Parts (ISS-014): The 3-Day Buffer Is Real Risk

Antenna rework parts arrive 06/16. DVT build is 06/22. That is six calendar days, not three — but realistically, 06/16 is a Monday delivery, parts must be inspected, rework qualification documentation must be complete, and build prep must happen. Effective working buffer: approximately 3 days of productive time.

**The risk scenario neither advocate fully models:** Parts arrive 06/16 with a quality nonconformance — wrong specification, wrong quantity, or incoming inspection failure. At that point, we have a re-order cycle on top of an already-tight schedule. Air freight contingency (Pro's $12K action) covers a known delay. It does not cover a quality failure on arrival.

**My addition to Pro's P1:** Incoming inspection criteria for antenna parts must be defined and documented *before* 06/16 arrival, not upon receipt. If parts arrive and inspection criteria are being written in real time, we will lose 12–24 hours we do not have.

**Concrete gate I am adding:** A written incoming inspection checklist for the antenna parts, approved by Hardware Engineering (Dept 01) and Quality & Reliability (Dept 03), must be complete by **06/14**. Cost: $0 — this is internal engineering work.

### The 08/18 Hard Stop: Zero Slack Is Not a Feature

Both advocates treat the 08/18 certification deadline as a constraint to schedule around. I want to be explicit about what zero slack actually means:

**If anything goes wrong between DVT build start (06/22) and cert submission, we have no recovery path.** Not a small path. None. A single unexpected PCI hardware gap, a yield failure that requires a process change and a re-run, a battery thermal event during PRT — any of these individually breaks the cert timeline.

**The correct response to zero slack is not to move faster. It is to eliminate every knowable source of surprise before 06/22.** That is the entire premise of my position.

---

## AREA 2 — Open Issues: Closure Plan Robustness

### ISS-023/025 — Yield Root Cause: The Critical Distinction

Both advocates cite "yield root cause closed before build" as a requirement. Both then describe actions that do not actually guarantee this.

**Let me be precise about what "closed" means:**
1. Failure mechanism confirmed — physical root cause identified with evidence (not hypothesis)
2. Process correction specified — a change to the build process that addresses the mechanism
3. Correction implemented in DVT build instructions, reviewed and approved by Quality (Dept 03)
4. At minimum, a small verification lot (even 10–15 units) demonstrating the correction holds

**Pro's plan delivers a Pareto by 06/18 and calls that closure. Growth's plan says "confirmed failure mechanism + process correction specified" by 06/19.** Growth is closer to correct on the definition, but 06/19 is three days before build start — not enough time for even a small verification lot.

**My position on the verification lot:** I am not requiring a full verification lot before 06/22. I am requiring that the DVT build itself be structured so the first 50 units serve as the verification lot, with the 84% pause gate as the decision point. This is acceptable *only if* the failure mechanism is confirmed and the process correction is specified before build start. A Pareto alone is not sufficient basis to authorize build.

**Concrete gate:** Hardware Engineering (Dept 01) and MSQ (Dept 04) must deliver a written yield root cause closure document — mechanism confirmed, process correction specified, correction incorporated in DVT build instructions — by **06/19**. Quality & Reliability (Dept 03) must sign off on that document before build authorization. If this document is not complete and signed by 06/19, DVT slips to the date it is complete. A 5–7 day slip now is preferable to discovering yield is still broken at unit 50 during DVT.

### ISS-032 — Battery 8D at D6: This Is Not Negotiable

**D6 means root cause is confirmed. D7 means corrective action is implemented and verified with test data.** These are not semantic distinctions — they are the difference between "we know what went wrong" and "we fixed it and proved the fix works."

The Brain's ICP context makes D7 completion before DVT build start non-negotiable on two independent grounds:

**Ground 1 — Field safety.** Strategy.md identifies "spills, sanitizer chemicals, 24/7 duty cycle" as the operating environment. A battery that has not had its corrective action validated going into that environment is a thermal risk. Lithium battery incidents in commercial food-service environments are not RMA events — they are regulatory events (49 CFR / IATA DG per laws.md) and potential liability events.

**Ground 2 — Certification integrity.** A battery with an unvalidated corrective action that fails during PRT testing — which is part of the cert path — does not just fail the test. It requires a redesign loop, which blows the 08/18 deadline entirely.

**The Pro plan assigns D7 completion a cost delta of $0 and calls it "in-progress."** Growth corrects this and requires a D7 completion plan by 06/13. I support Growth's requirement but want to be explicit about the consequence: **if Hardware Engineering (Dept 01) cannot deliver a credible D7 completion plan with a date ≤ 06/21 by 06/13, DVT does not start on 06/22.** Full stop. This is not a negotiating position — it is a quality gate.

**Concrete gate:** D7 completion plan due **06/13**. If plan date ≤ 06/21: build proceeds as planned. If plan date > 06/21: DVT start slips to D7 completion date + 1 day. No exceptions.

### ISS-027/028 — PCI: Hardware Gaps Discovered Late Are Program-Ending

Both advocates now agree the QSA gap review should move to 06/18. I want to explain precisely why, because the stakes need to be on record.

**PCI PTS assessment evaluates hardware-level security:** tamper mesh coverage, key injection architecture, secure element integration, physical attack resistance. These are not firmware patches. If the QSA gap review on 06/18 reveals that the tamper mesh design does not meet PTS requirements, that requires a PCB revision. A PCB revision at DVT stage is a minimum 4–6 week cycle. At 4 weeks from 06/18, we are at 07/16 — and we have not yet started DVT build. The 08/18 deadline is gone.

**This is the single scenario where a $8,000 expenditure prevents a program-ending outcome.** If the QSA review on 06/18 is clean, we have confirmation and proceed with confidence. If it reveals a hardware gap, we have four days before build authorization to decide: can we design around it in DVT, or do we need to restructure the program? Either way, we make the decision with information. A QSA review on 06/25 gives us the same possible outcomes with four fewer days to respond.

**Concrete gate:** QSA gap review complete by **06/18**. Any hardware-level PCI gaps must be dispositioned by Hardware Engineering (Dept 01) before build authorization on 06/22. Cost: $8K.

### ISS-030/031 — eMMC Dual-Source: The Two-Sources Rule Is Inviolable

Both advocates agree. The two-qualified-sources rule cannot be waived. Buffer inventory is an acceptable bridge to qualification completion, not a substitute for qualification.

**My addition:** The second-source qualification timeline must be confirmed in writing by **06/18**. "In flight" is not a status — it is an absence of commitment. If the second source cannot complete qualification before the MP ramp gate, we need to know that now, when we can plan around it, not at the MP gate, when we cannot.

---

## AREA 3 — Budget: Where Contingency Buys Real Risk Reduction

**Current position:** $2.0M total budget, $872K spent, $1,128K remaining. Of that $1,128K, the program has designated $111.6K as contingency. The remaining ~$1,016K must cover DVT build, cert lab fees, PRT execution, beta trial support, and ramp preparation.

**The accounting question both advocates have not fully answered:** Is $1,016K (ex-contingency) sufficient to cover DVT through beta? Before any contingency draw is authorized, someone in Finance or NPI Program Management (Dept 02) needs to confirm that the remaining non-contingency budget is sufficient for the planned program scope. If it is not, the $263K de-risking discussion is happening against an already-constrained budget, and we need a formal budget reallocation request — not informal reallocation from "already-spent" dollars.

**My required action:** NPI Program Management (Dept 02) delivers a forward budget estimate — DVT through beta trial — by **06/13**, before any contingency draws are authorized. If the forward spend exceeds remaining budget, this goes to executive leadership for reallocation decision. Cost: $0.

**Where contingency spend is justified (my priority order, from Brain data):**

| Rank | Action | Rationale | Amount | Source |
|---|---|---|---|---|
| 1 | QSA gap review — moved to 06/18 | Hardware PCI gap = program-ending; $8K prevents it | $8K | Contingency |
| 2 | RF contractor search + onboarding | Single engineer = cert path with zero redundancy | $45K | Contingency |
| 3 | Yield engineering + DVT sample increase | 10-point yield gap; $24K buys statistical confidence | $24K | Contingency |
| 4 | DVT build date protection (antenna parts, CM standby) | $35K buys uncompromised 06/22 start | $35K | Contingency |
| 5 | PCI lab remediation window pre-booking | $6K holds option value on 07/07–07/14 slot | $6K | Contingency |
| 6 | Battery D7 validation testing | Cost TBD 06/13; fund from contingency when known | TBD | Contingency |
| **Contingency subtotal** | | | **$118K + TBD battery** | |
| 7 | eMMC buffer inventory + second-source acceleration | Supply chain; separate budget line | $26K | Supply chain |
| 8 | Tet pre-build inventory | Capital inventory; separate authorization | $95K | Capital |
| 9 | BrightPath second-site qualification | Supply chain; separate budget line | $15K | Supply chain |

**The $118K contingency draw slightly exceeds $111.6K by $6.4K.** This requires one formal reallocation request. It is a clean, auditable action. The battery D7 cost, once known on 06/13, may push this higher — but we fund it when we know the number, not before.

**The P7 inventory items ($110K) must go through separate capital authorization.** They are recoverable as revenue but they are cash outflows today, and jamming them into contingency obscures the true program financial position.

---

## AREA 4 — EVT Yield 78%: The Path to 88% DVT and 95% MP

**Numbers from the Brain:**
- EVT yield: 78%
- DVT target: 88% (10-point gap)
- MP target: 95% (17-point gap from EVT)
- AMG-100 

BALANCED: # BALANCED POSITION — AMG-100 Program Review
## 06/11/2026 | Round 1

---

## Opening Frame

Both the Growth and Cautious advocates have produced technically serious positions. Growth's plan is directionally right on urgency and commercially grounded in the Brain's numbers. Cautious is right on the three conditions that, if not met, make a 06/22 build start actively harmful rather than merely risky.

My job is not to split the difference arithmetically. It is to identify which actions are load-bearing — meaning their absence creates genuine program failure risk — and sequence them against realistic timelines and the actual contingency budget.

Let me define terms clearly, then build the plan.

---

## Jargon Definitions (Plain English, Referenced to Brain Data)

**DVT** — Design Validation Test. The build phase where a near-final design is assembled and tested against specifications. A DVT failure typically requires redesign; schedule damage is severe.

**EVT** — Engineering Validation Test. Earlier phase. Our EVT yield was 78% (factory-yield-evt document). DVT target is 88%. MP (mass production) target is 95%.

**8D / D6 / D7** — Eight-Discipline problem-solving methodology. D6 = root cause confirmed. D7 = corrective action implemented *and* verified with physical test evidence. D7 is not a document — it is a test result.

**MTBF** — Mean Time Between Failures, in hours. At 62,000 hours (mtbf-prediction), implied Annual Failure Rate = 8,760 ÷ 62,000 = **14.1% AFR**. Target AFR is 2.0%, implying required MTBF ≥ 438,000 hours. This is a **7x reliability gap** that neither advocate has fully quantified in operational terms. At a 500-location chain running 30 devices per site (15,000 units), 14.1% AFR means approximately 2,115 field failures per year against a 300-unit target. This gap must be on record before DVT build authorization.

**AFR** — Annual Failure Rate. Percentage of deployed units expected to fail in 12 months.

**PCI PTS** — Payment Card Industry Payment Terminal Security. A hardware and software security certification mandatory for any device processing card payments. Hardware-level gaps at assessment cannot be patched — they require physical redesign, which at this stage is a program-restructuring event.

**QSA** — Qualified Security Assessor. A PCI-certified third party authorized to conduct PTS assessments.

**FCC Part 15** — US Federal Communications Commission equipment authorization for unintentional radiators (47 CFR Part 15, per laws.md). Required before commercial sale. Antenna design changes after authorization require re-testing.

**RMA** — Return Merchandise Authorization. A returned failed unit. Fleet uptime depends on RMA volume staying within depot capacity.

**eMMC** — Embedded MultiMediaCard. Flash storage. Single-source qualification means one approved supplier; a quality event or shortage at that supplier halts production.

**BrightPath** — Our sole contract manufacturer. Single-site concentration risk: one operational disruption stops all production.

**Tet** — Lunar New Year factory shutdown. Missing the pre-build window creates a supply gap that cannot be recovered until after the shutdown period ends.

**NPI** — New Product Introduction. The structured process from design completion to mass production readiness.

**PRT** — Product Reliability Test. Structured testing that validates field reliability before launch. Part of the certification path.

**ASP / Gross Profit** — AMG-100 ASP: $329 (products.md). Gross margin: 42%. Gross profit per unit: **$138.18**. At 10,000 units, every recovered percentage point of yield = approximately $13,818 in gross profit.

---

## What Growth Gets Right

1. The commercial window is real. VP of Operations and CIO buyers (ICP per strategy.md) are purchasing now. A missed September beta means no Q1 2027 commercial deployment. The asymmetry favors urgency when risks are genuinely manageable.

2. DVT *is* the verification mechanism for process corrections when the failure mechanism is confirmed and corrections are specified in build instructions before build start. Requiring a standalone verification lot before DVT would be a third EVT run — not standard NPI practice.

3. The contingency math, correctly disaggregated, shows a $127K contingency draw (not $263K), with $136K properly classified to separate capital and supply chain budget lines. The overrun against $111.6K is $15.4K — one formal reallocation request, not a shell game.

4. Pre-build inventory ($95K) is recoverable revenue, not sunk cost. It belongs in a capital authorization, not contingency, but it is not waste.

---

## What Cautious Gets Right

1. The MTBF gap — 14.1% AFR against a 2.0% target — has not been adequately surfaced. Shipping a device with a 7x reliability gap to buyers who selected us explicitly for uptime is an existential commercial risk, not a footnote.

2. The QSA gap review must be 06/18, not 06/25. Hardware-level PCI gaps discovered after DVT build authorization cannot be corrected without a DVT respin. Seven days of earlier visibility costs $8K. A DVT respin caused by a gap discoverable on 06/18 costs the entire cert timeline.

3. Battery D7 is a hard build stop, not an assertion. "In-progress" at D6 on 06/11 with 11 days to build start is not a schedule; it is a hope. A written D7 completion plan with a committed date and physical test protocol is due 06/13.

4. Incoming inspection criteria for antenna parts must be written before 06/16 arrival, not upon receipt. A quality nonconformance on arrival with no pre-defined acceptance criteria costs 12–24 hours the schedule cannot absorb.

---

## Where Both Advocates Have a Gap

**Neither plan resolves the MTBF/AFR gap with a concrete action before DVT.**

Growth mentions MTBF as a reliability item. Cautious surfaces the 14.1% AFR math. Neither requires a credible path to ≤2.0% AFR as a condition of DVT build authorization or beta trial authorization.

The Brain's strategy vision — *">99.5% fleet uptime, every table running an LSI device"* — is not a marketing claim. It is the explicit value proposition to VP of Operations and CIO buyers (strategy.md ICP) who are evaluating us against competitors for multi-year, multi-site deployments. A device with 14.1% AFR cannot deliver 99.5% uptime under any realistic repair-cycle model.

**This does not delay DVT.** DVT is the mechanism for generating the reliability data needed to update the MTBF prediction. But it does mean that beta trial authorization in September must be conditioned on an updated MTBF prediction — incorporating DVT failure data — showing a credible path to ≤2.0% AFR at MP configuration. Shipping a beta device whose reliability profile we cannot defend to a paying customer is not a quality gate we can waive.

---

## THE BALANCED PLAN

### Three Hard Conditions for 06/22 Build Authorization

These conditions are non-negotiable. If any is not met by its date, build start slips to the date it is met. A deliberate short slip is recoverable. A DVT build that starts with these unresolved is not.

| Condition | Due | Owner | Cost | Consequence If Missed |
|---|---|---|---|---|
| **Yield root cause closed:** failure mechanism confirmed (not Pareto alone), process correction specified, incorporated in DVT build instructions, signed off by Quality (Dept 03) | 06/19 | HW Eng (01) + MSQ (04) + Q&R (03) | $6K contractor support | DVT slips to date of closure. 5–7 day slip is recoverable; failed DVT yield is not. |
| **Battery 8D D7 completion plan** delivered with committed date ≤ 06/21 and written physical test protocol | 06/13 | HW Eng (01) + Q&R (03) | $0 to plan; cost funded when known | Hard stop: DVT does not start until D7 is complete with test evidence |
| **QSA gap review complete:** hardware-level PCI gaps dispositioned before build authorization | 06/18 | NPI (02) + HW Eng (01) | $8K | DVT does not start until gaps dispositioned; hardware gaps at this stage = program restructure |

**Schedule logic:** If all three conditions are met on time, build starts 06/22. If battery D7 requires a slip, DVT moves to D7+1. A 7-day slip to 06/29 is recoverable within the cert window if the cert path has any give at all. A yield failure or battery event during DVT is not recoverable before 08/18.

---

### PRIORITY 1 — DVT Build Date Protection (ISS-014, ISS-019, ISS-021)

**The 06/16 antenna parts arrival with a 3-day effective buffer is manageable with pre-positioning. The gap in both prior plans: no incoming inspection criteria defined before parts arrive.**

| Action | Owner | Due | Cost |
|---|---|---|---|
| Written incoming inspection checklist for antenna parts — acceptance criteria defined and approved by HW Eng (01) and Q&R (03) | HW Eng (01) + Q&R (03) | 06/14 | $0 (internal) |
| Confirm antenna parts ETA in writing from supplier; air freight upgrade contingency if ETA slips past 06/17 | MSQ (04) | 06/13 | $12K freight contingency |
| Pre-kit all non-antenna BOM at CM — 100% staged by 06/15 | NPI (02) | 06/15 | $8K expedite labor |
| CM dedicated build team on standby 06/16–06/22 — no line reassignment | NPI (02) | 06/16 | $15K labor hold |
| Rework qualification documentation for antenna assembly complete and approved before 06/19 | HW Eng (01) | 06/19 | $0 (internal) |

**P1 total: $35K**

The incoming inspection checklist is the Balanced addition. It costs nothing and eliminates the scenario where parts arrive 06/16 with a quality nonconformance and inspection criteria are being written in real time.

*Quality gate confirmation: no gate weakened. Rework qualification documentation is a prerequisite for build authorization, not a parallel activity.*

---

### PRIORITY 2 — Yield: EVT 78% → DVT 88% Target (ISS-023, ISS-025)

**The 10-point yield gap from EVT to DVT target is the most commercially consequential open issue in the program.** At AMG-100's $138.18 gross profit per unit, every percentage point of yield at 10,000-unit MP scale = $13,818 in recovered gross profit. Closing 10 points = $138,180.

**The Balanced position on verification:** DVT *is* the verification mechanism for process corrections — provided the failure mechanism is confirmed and corrections are in approved build instructions before 06/22. The 84% pause gate after the first 50 units is the in-build check. This is tighter than baseline, not looser.

| Action | Owner | Due | Cost |
|---|---|---|---|
| Yield root cause closure document: failure mechanism confirmed, process correction specified, incorporated in DVT build instructions | HW Eng (01) + MSQ (04) | 06/19 | $6K contractor support |
| Quality (Dept 03) sign-off on yield root cause closure document before build authorization | Q&R (03) | 06/20 | $0 |
| DVT sample size increased by 15 units for statistical signal | NPI (02) | 06/22 | $18K material + build |
| **84% pause gate after first 50 units:** if yield < 84%, 48-hour analysis hold — not cancellation, analysis | Q&R (03) | 06/22 | $0 |

**P2 total: $24K**

*Quality gate confirmation: the 84% pause gate is a tighter interim gate than baseline. The yield root cause closure document is a new prerequisite for build authorization. No existing gate is weakened.*

---

### PRIORITY 3 — RF Engineer Bus-Factor Elimination (R-09)

**One engineer holds FCC Part 15 antenna expertise on a cert path with zero slack after 08/18.** This is the risk that can kill certification with no warning. The Balanced position agrees with Growth on cost ($45K) and with Cautious on timeline (06/20 is not realistic for specialist placement; 06/25 is).

**The most important action is not hiring the contractor. It is starting documentation today.**

| Action | Owner | Due | Cost |
|---|---|---|---|
| Incumbent RF engineer begins technical documentation file: antenna tuning decisions, test setups, pre-compliance data summary | HW Eng (01) | **06/11 (today)** | $0 |
| RF specialist contractor search initiated through specialist firm | HW Eng (01) | **06/11 (today)** | $0 |
| Contractor onboarded (realistic target given 2–4 week specialist placement cycle) | HW Eng (01) | 06/25 | $45K (3 months) |
| Cross-train one existing hardware engineer on antenna test procedures | HW Eng (01) | 07/01 | $0 |

**P3 total: $45K**

The documentation action starting today means that when the contractor arrives 06/25, a complete technical record exists. Two weeks of documentation work at $0 cost is the highest-ROI action in the entire plan. Starting it on 06/25 — when the contractor arrives — wastes those two weeks.

*Quality gate confirmation: no gate is modified. Human redundancy is added to execute existing gates, not to replace them.*

---

### PRIORITY 4 — PCI Pre-Assessment: QSA Gap Review 06/18 (R-01, ISS-027, ISS-028)

**Both prior advocates now agree the QSA review must move to 06/18.** The Balanced position confirms this is correct and explains precisely why the seven-day difference matters.

A hardware-level PCI PTS gap discovered on 06/18 (four days before build start) can be dispositioned before build authorization — either designed around in the DVT build or escalated to executive leadership as a program-restructuring decision. The same gap discovered on 06/25 (three days after build authorization) requires a DVT respin. A DVT respin at that stage eliminates all cert path margin and breaks 08/18.

**The $8K cost is the cheapest catastrophic-risk insurance in the program after the RF documentation action that costs $0.**

| Action | Owner | Due | Cost |
|---|---|---|---|
| QSA gap review — one day on-site, hardware-level PCI PTS evaluation | NPI (02) + HW Eng (01) | 06/18 | $8K |
| Named internal PCI lead assigned — must have prior PTS assessment experience | NPI (02) | 06/13 | $0 |
| Any hardware-level PCI gaps dispositioned before build authorization | HW Eng (01) | 06/21 | Cost TBD if gaps found |
| PCI firmware hardening complete, firmware build frozen | HW Eng (01) | 07/01 | $0 (must-do regardless) |
| Remediation window pre-booked at PCI lab 07/07–07/14 | NPI (02) | 06/20 | $6K reservation |

**P4 total: $14K**

*Quality gate confirmation: PCI/EMV certification rigor is strengthened. The QSA gap review adds a pre-DVT hardware validation layer that does not exist in the baseline plan.*

---

### PRIORITY 5 — Battery 8D D7 + MTBF Transparency (ISS-032, Reliability)

**This is the area where both prior advocates understate the stakes.**

**On D7:** D6 means root cause is confirmed. D7 means corrective action implemented and verified with physical test evidence. "In-progress" at D6 on 06/11 with 11 days to build start is not a status — it is a gap with an unknown resolution date.

**On MTBF:** 62,000 hours implies 14.1% AFR against a 2.0% target. At ICP scale (500 locations × 30 devices = 15,000 units), the gap is 2,115 annual failures versus a 300-unit target. This is not a reliability footnote. It is the central commercial promise — >99.5% fleet uptime per strategy.md — measured against a current failure rate that cannot support that promise.

**The Balanced position:** DVT is not delayed for MTBF