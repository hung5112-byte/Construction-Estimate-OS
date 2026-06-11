---
type: meeting_r2
---
# Round 2 — Pro/Con Debate

PRO: # Pro Advocate — Round 1 Position
## AMG-100 Program Review | 06/11/2026

---

**Pro position:** AMG-100 is 11 days from DVT build in a challenging but absolutely executable state. Every open issue has a closure path. The question is not *whether* to proceed — it is *how much to spend* to buy down risk and protect the 08/18 certification critical path. Our strategy is unambiguous: be the #1 hardware platform for in-venue guest engagement by 2030, >99.5% fleet uptime, every table running an LSI device. AMG-100 is the product that gets us there. Delaying DVT does not protect quality — it destroys schedule margin we cannot recover.

Here is my prioritized improvement plan.

---

## PRIORITY 1 — Protect DVT Build Date: 06/22 (ISS-014, ISS-019, ISS-021)

**The antenna rework parts (ISS-014) arrive 06/16 — 3 days before build.** That is tight but real. The action is not to wait and hope; it is to pre-position everything else so the moment parts land, build starts without friction.

**Concrete actions:**

| Action                                                                                                  | Owner                          | Date  | Cost Delta                |
| ------------------------------------------------------------------------------------------------------- | ------------------------------ | ----- | ------------------------- |
| Pre-kit all non-antenna BOM at contract manufacturer — 100% staged by 06/15                             | NPI Program Mgmt (Dept 02)     | 06/15 | +$8K expedite labor       |
| Confirm antenna parts ETA with supplier in writing; arrange air freight upgrade if ETA slips past 06/17 | MFG/Supplier Quality (Dept 04) | 06/13 | +$12K freight contingency |
| Assign dedicated CM build team on standby 06/16–06/22 — no line reassignment                            | NPI Program Mgmt (Dept 02)     | 06/16 | +$15K labor hold fee      |
| Complete rework qualification documentation for antenna assembly before 06/19                           | Hardware Engineering (Dept 01) | 06/19 | $0 (internal)             |

**Total incremental spend: ~$35K.** Against a $2.0M DVT budget with $111.6K contingency remaining, this is a 31% draw on contingency that buys the single most valuable thing we have: an uncompromised 06/22 start.

**Quality gate confirmation:** Rework qualification must be *complete and documented* before build authorization — this action accelerates documentation, it does not bypass it. No gate is weakened.

---

## PRIORITY 2 — Yield: From EVT 78% to DVT 88% Target (ISS-023, ISS-025)

**EVT yield at 78% is 10 points below DVT target (88%) and 17 points below MP target (95%).** At our ICP's deployment scale — 20–60 devices per site, 50–1,200 locations — a 12% scrap rate at MP volume is commercially fatal. The AMG-100 at $329 ASP and 42% margin (per products.md) means every scrapped unit costs $139 in lost gross profit. At a modest 10,000-unit first production run, closing 10 yield points saves $139,000 in direct margin.

**Root cause must be closed before DVT build start, not during.** The fact that yield root cause is described as "open" is the most dangerous single data point in this review.

**Concrete actions:**

| Action | Owner | Date | Cost Delta |
|---|---|---|---|
| Dedicate NPI yield engineer full-time to EVT failure analysis; complete Pareto of top 3 failure modes by 06/18 | Hardware Engineering (Dept 01) + MFG/Supplier Quality (Dept 04) | 06/18 | +$6K contractor support if needed |
| Issue DVT build instructions with specific process controls targeting top failure modes | Hardware Engineering (Dept 01) | 06/20 | $0 |
| Increase DVT build sample size by 15 units (from baseline) to generate statistically meaningful yield signal | NPI Program Mgmt (Dept 02) | 06/22 | +$18K material + build cost |
| Set explicit DVT yield gate: if <84% after first 50 units, build pauses for 48-hour analysis — not cancellation, analysis | Quality & Reliability (Dept 03) | 06/22 | $0 |

**Total incremental spend: ~$24K.** This is yield insurance — you cannot certify a product you cannot build at yield.

**Quality gate confirmation:** The 84% pause gate is a *tighter* interim gate than current plan, not a looser one.

---

## PRIORITY 3 — Eliminate the Single RF Engineer Bus-Factor (R-09)

**This is the risk that can kill certification with zero warning.** One engineer holds the RF/antenna expertise. The 08/18 cert critical path has zero slack. If that engineer is unavailable for any reason — illness, departure, family emergency — we miss FCC Part 15 authorization and the entire launch slips. Our strategy requires >99.5% fleet uptime; we cannot promise that to a VP of Operations buyer if we cannot even guarantee our own certification timeline.

**Concrete actions:**

| Action | Owner | Date | Cost Delta |
|---|---|---|---|
| Hire one RF/antenna contract engineer through a specialist firm (e.g., Robson Forensic, IEC Electronics engineering services); 3-month engagement covering DVT through cert submission | Hardware Engineering (Dept 01) | 06/20 | +$45K (3 months @ $15K/mo) |
| RF engineer documents all antenna tuning decisions, test setups, and pre-compliance data in a living technical file by 06/25 | Hardware Engineering (Dept 01) | 06/25 | $0 |
| Cross-train one existing hardware engineer on antenna test procedures — not to replace, to backstop | Hardware Engineering (Dept 01) | 07/01 | $0 |

**Total incremental spend: ~$45K.** This is the cheapest insurance policy in the program. One engineer departure does not cost $45K — it costs the entire September beta trial and potentially the 2026 launch.

**Quality gate confirmation:** No gate is changed. We are adding human redundancy to *execute* existing gates, not modify them.

---

## PRIORITY 4 — PCI PTS Pre-Assessment 07/06: Protect With Resource (R-01, ISS-027, ISS-028)

**The PCI PTS pre-assessment on 07/06 is 25 days away with zero described slack between it and the 08/18 hard stop.** Our ICP — VP of Operations / CIO buyers — explicitly values payment security (PCI) per strategy.md. A failed pre-assessment does not just delay cert; it signals to the market that our payment security posture is weak. That is brand damage in our most sensitive buyer dimension.

**Concrete actions:**

| Action | Owner | Date | Cost Delta |
|---|---|---|---|
| Engage PCI QSA (Qualified Security Assessor) firm for a pre-pre-assessment gap review — one day on-site before 06/25 | NPI Program Mgmt (Dept 02) | 06/25 | +$8K |
| Complete all PCI-related firmware hardening (tamper response, key injection, secure boot) and freeze firmware build for assessment | Hardware Engineering (Dept 01) | 07/01 | $0 (must-do regardless) |
| Assign dedicated internal PCI lead — single throat to choke — accountable for 07/06 readiness | NPI Program Mgmt (Dept 02) | 06/13 | $0 |
| Pre-book remediation window at PCI lab 07/07–07/14 in case first-pass gaps require hardware or firmware iteration | NPI Program Mgmt (Dept 02) | 06/20 | +$6K lab reservation fee |

**Total incremental spend: ~$14K.** PCI/EMV certification rigor is explicitly inviolable per this review's terms. Spending $14K to ensure we walk into 07/06 with no surprises is non-negotiable.

**Quality gate confirmation:** PCI/EMV rigor is strengthened, not compromised.

---

## PRIORITY 5 — eMMC Dual-Source: Close the Single-Source Risk Before MP (ISS-030, ISS-031)

**eMMC dual-source qualification is described as "in flight."** Our strategy vision requires >99.5% fleet uptime across the installed base. A single-source eMMC is a supply chain dependency that can halt production or create field quality inconsistency. The two-qualified-sources rule is inviolable per this review's terms.

**Concrete actions:**

| Action | Owner | Date | Cost Delta |
|---|---|---|---|
| Confirm second-source eMMC vendor qualification timeline — must be complete before MP ramp gate | MFG/Supplier Quality (Dept 04) | 06/18 | $0 |
| If second-source qualification cannot complete before MP ramp gate, place a 90-day buffer inventory order on primary source eMMC now — cover first 3 months of MP volume | MFG/Supplier Quality (Dept 04) | 06/20 | +$22K inventory carry cost |
| Accelerate second-source DVT validation samples — include second-source eMMC in 15% of DVT units | Hardware Engineering (Dept 01) + MFG/Supplier Quality (Dept 04) | 06/22 | +$4K sample cost |

**Total incremental spend: ~$26K (worst case).** The two-qualified-sources rule cannot be waived. This spend ensures we are never in a position of choosing between shipping product and violating supply chain policy.

**Quality gate confirmation:** Dual-source rule is upheld. Buffer inventory is a *contingency*, not a workaround — qualification still completes before MP.

---

## PRIORITY 6 — Battery 8D at D6 and MTBF Gap (ISS-032, Reliability)

**MTBF at 62,000 hours against a 2.0% AFR target is a gap.** To put this in field terms: our ICP deploys 20–60 devices per site. At 2.0% AFR, a 500-site chain running 30 devices each (15,000 units) expects 300 failures per year — that is a manageable RMA pool. If MTBF does not improve, AFR worsens, RMA volume exceeds depot capacity, and we breach the uptime promise that is *central to our positioning*.

**The battery 8D at D6 of 8 means root cause is identified but corrective action is not yet validated.** This cannot enter DVT unresolved — battery failures in the harsh restaurant environment (spills, 24/7 duty cycle, sanitizer chemicals — per strategy.md ICP pain points) are the most likely field failure mode.

**Concrete actions:**

| Action | Owner | Date | Cost Delta |
|---|---|---|---|
| Battery 8D must reach D7 (corrective action implemented and validated) before DVT build start 06/22 | Hardware Engineering (Dept 01) + Quality & Reliability (Dept 03) | 06/21 | $0 (in-progress) |
| Include battery thermal/stress validation in DVT PRT plan — minimum 50-cycle accelerated test at operating temp range | Quality & Reliability (Dept 03) | 06/22 | +$9K test cost |
| MTBF prediction model update: incorporate EVT failure data and revised component selections — publish updated prediction before 07/15 | Quality & Reliability (Dept 03) | 07/15 | $0 |
| Alpha trial uptime at 99.1% vs 99.5% target: conduct root cause analysis of alpha downtime events; findings must feed DVT design checklist | Service Operations (Dept 05) | 06/20 | $0 |

**Total incremental spend: ~$9K.**

**Quality gate confirmation:** Battery 8D D7 is a *prerequisite* for build authorization, not a parallel activity.

---

## PRIORITY 7 — BrightPath Single-Site Risk and Tet Pre-Build

**BrightPath single-site manufacturing risk is a concentration risk that compounds every other supply chain issue.** Combined with Tet (Lunar New Year) factory shutdown windows, the pre-build strategy must be explicit and funded.

**Concrete actions:**

| Action | Owner | Date | Cost Delta |
|---|---|---|---|
| Quantify Tet exposure: identify exact shutdown window and required pre-build volume to maintain beta trial supply (Sept) and MP ramp | NPI Program Mgmt (Dept 02) + MFG/Supplier Quality (Dept 04) | 06/18 | $0 |
| Authorize pre-build inventory funding in budget plan — estimated 500-unit pre-build at $191 COGS (329 × 58%) = ~$95K inventory | NPI Program Mgmt (Dept 02) | 06/20 | +$95K inventory (recoverable) |
| Initiate second-site qualification at BrightPath or alternate CM — not required for DVT, required as risk mitigation before MP | MFG/Supplier Quality (Dept 04) | 07/01 | +$15K qualification cost |

**Total incremental spend: ~$110K (largely inventory, which is recoverable revenue).** Note: $95K of this is inventory that becomes revenue — it is not a sunk cost.

**Quality gate confirmation:** Pre-build units must pass all DVT-equivalent quality gates before inventory commitment.

---

## BUDGET SUMMARY

| Priority | Incremental Spend | Category |
|---|---|---|
| P1 — DVT Build Date Protection | $35K | Schedule insurance |
| P2 — Yield Root Cause + Sample Increase | $24K | Quality / yield |
| P3 — RF Engineer Bus-Factor | $45K | Risk mitigation |
| P4 — PCI Pre-Assessment Support | $14K | Certification rigor |
| P5 — eMMC Dual-Source Buffer | $26K | Supply chain |
| P6 — Battery 8D + MTBF | $9K | Reliability |
| P7 — Tet Pre-Build + BrightPath | $110K | Supply chain / inventory |
| **TOTAL INCREMENTAL** | **$263K** | |

**Current contingency remaining: $111.6K.** The full $263K plan exceeds contingency by $151K. My recommendation: fund P1 through P5 immediately from contingency ($144K — slightly over, requires $32K budget reallocation from the $872K already-spent baseline or a contingency top-up request). P6 and P7 fund from a separate inventory/supply chain budget line given the recoverable nature of pre-build inventory.

**Against a $2.0M program budget, $263K in de-risking spend protects a product that generates $139 gross margin per unit** (AMG-100: $329 × 42%). A 10,000-unit first year recovers this entire incremental investment in **1,900 units sold** — less than two average-size chain deployments.

---

## WHAT DOES NOT MOVE

To be explicit: the following are inviolable and no action above touches them:

1. **PCI/EMV certification rigor** — P4 adds resources, does not reduce scope
2. **Two-qualified-sources rule** — P5 funds acceleration, does not grant a waiver
3. **Battery 8D D7 before build** — P6 sets it as a hard prerequisite
4. **DVT yield gate at 84%** — P2 sets a tighter interim gate than baseline
5. **FCC Part 15 / UL/IEC 62368-1 certification** (per laws.md) — R-09 mitigation adds capacity, not shortcuts

---

## CLOSING ARGUMENT

Every department has raised legitimate concerns. But concern is not a strategy. Our 2030 vision is to be the #1 hardware platform in US casual dining. The chains we are selling to — VP of Operations buyers who are hemorrhaging labor costs and losing revenue at every dead table — need this product in September beta. AMG-100 at $329 with 42% margin is the highest-margin product in our lineup. Every week of delay is a week a competitor occupies a table we should own.

**The path is clear: spend $263K, close the eight open issues on the dates above, and build on 06/22. The alternative — delaying DVT — does not eliminate risk. It just moves it to a place where we have even less time to respond.**

CON: # Con Advocate — Round 1 Position
## AMG-100 Program Review | 06/11/2026

---

**Con position:** The Pro Advocate has produced a competent spend plan, but it contains five structural flaws that individually could kill the program and collectively represent a pattern of wishful thinking dressed up as risk management. I am not arguing for indefinite delay. I am arguing that three specific conditions must be satisfied *before* 06/22 build authorization, that the budget math is broken, and that Pro's plan has a dangerous blind spot on what "quality gate" actually means in this context.

Let me be precise.

---

## FLAW 1 — The Yield Root Cause is Open and Pro's Plan Does Not Actually Close It Before Build

**Pro says:** "Root cause must be closed before DVT build start, not during." Then Pro's own action table says: *"Complete Pareto of top 3 failure modes by 06/18."*

A Pareto is not root cause closure. A Pareto tells you which failure modes are most frequent. Root cause closure requires: (1) confirmed mechanism, (2) corrective action implemented in the build process, (3) at least one verification lot demonstrating the correction works.

**The Brain is explicit on yield:** EVT yield was 78% against a DVT target of 88% and MP target of 95%. MSQ (Dept 04) states: *"yield root cause open, rework qualification incomplete."* Quality & Reliability (Dept 03) lists yield root cause as one of four conditions for build-start authorization.

**Pro's plan delivers a Pareto by 06/18 — that leaves exactly four days (06/18 to 06/22) to implement process corrections, run a verification lot, and confirm the fix works before build authorization.** Four days is not enough time to do that credibly. If DVT begins with yield root cause unconfirmed, we will discover at DVT build whether the fix worked. That is not DVT — that is a second EVT run at DVT cost.

**The risk scenario Pro ignores:** DVT yield comes in at 79–82%. We are now past 06/22, inside the 08/18 cert window with zero slack, and we have just consumed 2–3 weeks of build time discovering what EVT already told us. The 08/18 hard stop does not move. The cert path does not extend. We miss FCC and PCI simultaneously.

**My requirement:** Yield root cause must be confirmed (mechanism identified, process correction specified) *before* 06/22, not on 06/18. If that requires a 5–7 day DVT slip to 06/27–06/29, that is a better outcome than discovering yield is still broken during the DVT build itself. A short slip now is recoverable. A yield failure during DVT is not.

---

## FLAW 2 — The Budget Math Is Broken and Pro Buries the Overrun

Pro's own table shows **$263K total incremental spend against $111.6K contingency remaining** — a $151.4K overrun. Pro's proposed resolution: "fund from contingency plus $32K reallocation from the $872K already-spent baseline."

**That is not a resolution. That is an accounting shell game.** The $872K already-spent baseline is *spent*. You cannot reallocate spent dollars. The program budget is $2.0M total; $872K spent leaves $1,128K remaining for the entire remainder of the program — DVT build, certification, PRT, beta trial support, ramp preparation. Pro is proposing to consume an additional $263K of that $1,128K (23.3%) in the next 11 days on de-risking, leaving $865K for everything that comes after.

**Specific numbers from the Brain:** budget_tracker shows total_year_usd: $6,800,000 at the company level, but the program budget ceiling referenced in this review is $2.0M with $111.6K contingency. Pro's P7 alone — the Tet pre-build — is $110K, of which Pro claims $95K is "recoverable inventory." Recoverable inventory is still a cash outlay today. At current contingency of $111.6K, P7 alone consumes 99% of remaining contingency *before* any other priority is funded.

**Pro's sequencing is wrong:** P7 (BrightPath/Tet pre-build) should not be funded from contingency at all. It is an inventory investment decision that belongs in a separate capital authorization, not jammed into a DVT contingency draw.

**My requirement:** Before any contingency draw is authorized, Finance must confirm the remaining $1,128K is sufficient to cover DVT build, cert lab fees, PRT execution, and beta trial support through September. If it is not, the $263K de-risking plan requires a formal budget reallocation request — not a verbal "we'll figure it out." Pro skips this step entirely.

---

## FLAW 3 — Battery 8D at D6 Is a Hard Build Stop, Not a "Prerequisite" You Can Assert Into Existence

**Pro says:** "Battery 8D must reach D7 before DVT build start 06/22" — and assigns this a cost delta of $0, treating it as "in-progress."

**ISS-032 is not $0 and it is not merely in-progress.** MSQ (Dept 04) flags battery single-source risk and the 8D at D6 as independent blocking conditions. Quality & Reliability (Dept 03) lists battery corrective action validation as a build-start condition. D6 in the 8D methodology means: *root cause confirmed, but corrective action not yet implemented or validated.* D7 requires: corrective action implemented AND verified effective.

**The Brain's ICP context makes this worse, not better.** Strategy.md explicitly identifies *"harsh environment: spills, sanitizer chemicals, 24/7 duty cycle"* as the ICP's operating reality. A battery that has not completed D7 corrective action validation going into a 24/7 harsh-environment device is not a scheduling inconvenience — it is a field safety risk and a Lithium battery transport compliance issue (49 CFR / IATA DG per laws.md). If a DVT unit with an unvalidated battery correction fails thermally in the field during the September beta trial, we are not looking at an RMA. We are looking at an incident report and potential regulatory scrutiny.

**Pro's $0 cost delta for D7 completion is implausible.** If D7 were achievable at $0 internal effort between now and 06/21, it would already be done. The fact that it is at D6 on 06/11 with 11 days to build start means either: (a) the corrective action requires physical hardware iteration — which takes time and money — or (b) the verification testing has not been run. Neither scenario is free.

**My requirement:** Hardware Engineering (Dept 01) must provide a written D7 completion plan with specific deliverables, test protocol, and a realistic date by 06/13. If D7 cannot be confirmed before 06/22, DVT does not start on 06/22. This is not a quality gate we negotiate.

---

## FLAW 4 — Pro's PCI Plan Has a Structural Timing Gap That Creates a Certification Cliff

**Pro's Priority 4 action:** Engage QSA for a "pre-pre-assessment" gap review by 06/25, freeze firmware by 07/01, pre-assessment on 07/06.

**The problem:** "Freeze firmware by 07/01" and "pre-assessment on 07/06" leaves five days between firmware freeze and assessment entry. PCI PTS (Payment Terminal Security) assessment under the PCI SSC framework is not a one-day event — it involves physical security evaluation, logical security testing, key management review, and tamper evidence inspection. If DVT hardware is not complete and stable before firmware freeze, you are assessing a configuration that does not match your DVT build.

**ISS-027 and ISS-028 are open.** The Brain does not describe their specific content, but the cert-plan document places both in the PCI critical path. Pro's plan assigns a "dedicated internal PCI lead" as an action — but does not identify who that person is, what their PCI background is, or whether they have prior PTS assessment experience. "Single throat to choke" is a management cliché, not a qualification.

**The zero-slack reality:** The 08/18 hard stop is described as a certification stop-ship boundary. If PCI PTS assessment on 07/06 reveals a hardware-level gap — tamper mesh, key injection architecture, secure element integration — hardware iteration could require 4–6 weeks. That blows past 08/18 with no recovery path. Pro's $8K "pre-pre-assessment" gap review on 06/25 is the right idea, but it is too late and too shallow.

**My requirement:** Move the QSA gap review to 06/18 — not 06/25. Seven additional days of lead time before DVT build could reveal hardware-level PCI gaps that must be designed into the DVT build, not retrofitted afterward. A hardware-level PCI gap discovered on 06/25 after DVT build authorization has already been granted cannot be corrected without a DVT respin. That is a program-ending scenario.

**Cost delta: +$8K is correct, but it needs to happen 07 days earlier.** This is one of the cheapest schedule insurance policies in the entire plan. Pro has it at the right price and the wrong date.

---

## FLAW 5 — The Single RF Engineer Bus-Factor (R-09) Plan Is Sound in Concept but the Timeline Is Wrong

**Pro is correct that R-09 is the risk that can kill certification with zero warning.** I will not argue against the $45K RF contract engineer. But Pro's plan says: "Hire one RF/antenna contract engineer... by 06/20."

**Hiring a specialist RF/antenna contractor in nine days is not realistic.** RF/antenna engineers with FCC Part 15 pre-compliance and antenna tuning experience are a thin market. Specialist engineering staffing firms (Pro cites firms like Robson Forensic and IEC Electronics engineering services) typically require 2–4 weeks to identify, screen, and onboard a qualified candidate. If the search starts on 06/11 and requires 2–4 weeks, the contractor is not on-site until 06/25–07/09. That means the RF documentation action (Pro's 06/25 date) begins without backup in place.

**The correct action sequence:** Start the contractor search *today, 06/11*, with a parallel action to have the incumbent RF engineer begin the technical documentation file *immediately* — not by 06/25. If the engineer is available today and documentation starts today, we have 25 days of documentation work before the 07/06 PCI assessment creates schedule pressure. If documentation starts 06/25, we have 11 days.

**My requirement:** RF contractor search initiates 06/11. Incumbent engineer begins technical documentation file 06/12. Revised hire target: 06/25 (realistic) rather than 06/20 (wishful). No change to Pro's cost estimate of $45K.

---

## WHAT PRO GETS RIGHT (to be intellectually honest)

1. **The eMMC dual-source buffer inventory** (P5, $26K) is correctly structured and correctly sequenced. The two-qualified-sources rule cannot be waived; a buffer inventory as a bridge to qualification completion is the right mechanism.

2. **The 84% DVT yield pause gate** (P2) is a tighter interim gate than baseline. I support this specifically — it is one of the few places where Pro's plan adds rigor rather than just spending.

3. **BrightPath/Tet pre-build quantification** (P7, $0 for the analysis) is correct. The $95K inventory authorization should not come from contingency, but the analysis must happen before 06/18.

4. **The $45K RF contract engineer** is correctly scoped in cost. My objection is timeline, not concept.

---

## MY COUNTER-PLAN: THREE HARD CONDITIONS BEFORE BUILD AUTHORIZATION

The Brain's own departments — Hardware Engineering (Dept 01), Quality & Reliability (Dept 03), and MSQ (Dept 04) — all independently concluded: *not ready to build on 06/22 as-is.* That is not one pessimistic department. That is three independent technical functions converging on the same signal.

**I propose the following hard conditions for build authorization, with dates:**

| Condition | Required By | Owner | If Not Met |
|---|---|---|---|
| Yield root cause confirmed (mechanism + process correction specified, not just Pareto) | 06/19 | HW Eng (01) + MSQ (04) | DVT slips to 06/27 — 5-day recovery, still within cert window if cert path has any give |
| Battery 8D reaches D7 with written verification test results | 06/21 | HW Eng (01) + Q&R (03) | Hard stop: DVT does not start |
| QSA gap review completed (moved to 06/18, not 06/25) | 06/18 | NPI (02) + HW Eng (01) | DVT does not start until any hardware-level PCI gaps are dispositioned |

**These three conditions are the difference between a DVT build that discovers problems and a DVT build that confirms solutions.**

---

## BUDGET COUNTER-POSITION

Pro's $263K plan requires a formal budget reallocation, not a contingency draw plus hand-waving about spent dollars. My revised priority stack, funded from contingency only:

| Priority | Spend | Source |
|---|---|---|
| QSA gap review (moved to 06/18) | $8K | Contingency |
| RF contractor search + onboarding | $45K | Contingency |
| DVT yield engineer + sample increase | $24K | Contingency |
| PCI lab reservation + dedicated lead | $6K | Contingency |
| DVT build date protection (P1) | $35K | Contingency |
| **Subtotal from contingency** | **$118K** | Slightly over $111.6K — requires $6.4K formal reallocation |
| Battery 8D D7 validation (actual cost TBD by 06/13) | TBD | Separate budget line |
| eMMC buffer inventory | $26K | Supply chain budget |
| Tet pre-build authorization | $95K | Capital inventory — separate authorization |
| BrightPath second-site qualification | $15K | Separate budget line |

**Total requiring contingency draw: $118K.** The $6.4K overage above $111.6K contingency requires a single formal reallocation request — a clean, auditable action. Everything else is separated into appropriate budget categories, not blended into contingency.

---

## CLOSING ARGUMENT

The Pro Advocate's framing is: *"Delaying DVT does not protect quality — it destroys schedule margin we cannot recover."*

**That framing inverts the actual risk.** A 5-day DVT slip to 06/27, taken deliberately today with three hard conditions satisfied, consumes 5 days of schedule. A DVT build that starts 06/22 with yield root cause unconfirmed and battery D7 incomplete, and then discovers both problems during the build, does not cost 5 days — it costs the entire remaining schedule margin and lands us at 08/18 with a product that has not passed its own quality gates.

The Brain's strategy vision — *"#1 hardware platform for in-venue guest engagement, >99.5% fleet uptime"* — is not served by shipping a product whose yield mechanism we do not understand and whose battery corrective action has not been validated. VP of Operations and CIO buyers (our ICP per strategy.md) who experience device failures in the first 90 days of a beta trial do not give second chances. They give the table to a competitor.

**Spend the money. Close the three hard conditions first. Then build.**