---
type: meeting_r1
---
# Round 1 — Perspectives

## [[01-Departments/01-hardware-engineering/index|01-hardware-engineering]]

### Team inputs

#### [[me-team]]

**ME take:**

1. **Thermal margin is the yield killer.** EVT 78% yield — I need to know how many failures were thermally driven before DVT locks the enclosure. At 24/7 duty cycle in a restaurant environment (ambient 35°C+), if we haven't characterized the 13.3" panel's heat path to the enclosure with a real TIM pad spec, we're discovering this at DVT, not designing around it.

2. **IP/sealing is a system — not a gasket.** Spill/sanitizer resistance is core to the ICP pain point. ISS-019/021/023 closure plans need to confirm sealing validation is part of DVT test matrix, not deferred.

3. **11 days to build, no tooling changes allowed.** Any open mechanical ECO (cosmetic or structural) hitting the tool now adds 4–6 weeks minimum. Freeze the steel today.

**Numbers:** DVT build 06/22 — zero tooling float. Restaurant ambient +35°C = thermal design must be validated before build.

**Recommendation:** Confirm thermal characterization data and IP sealing test plan are closed before 06/22 build release — no enclosure surprises at DVT.

**Brain references:** products.md — AMG100, DVT status; ICP: spill/sanitizer/24-7 duty cycle

#### [[ee-team]]

**EE take:**

1. **ISS-014 antenna rework — 3-day buffer is a design defect risk, not a schedule risk.** If the revised antenna placement or matching network hasn't been pre-validated on bench, we're committing DVT boards to an unverified RF fix. Need S11/TRP/TIS data on rework samples *before* 06/22, not after. EMC/RF cert is already on the zero-slack path post-08/18.

2. **eMMC single-source is a live BOM defect.** Until second source is qualified and on approved vendor list, we're one end-of-life notice from a respin. DVT should pull from *both* candidate vendors — splits the qualification work and gives yield data on both parts simultaneously.

3. **78% EVT yield → 88% DVT target requires knowing the dominant failure modes *by net/component*, not just by symptom.** If we don't have ICT/FCT coverage data confirming which failures were caught electrically vs. functionally, we're guessing at the fix.

**Numbers:** AMG-100 at $329 / 42% margin (products.md). Each yield point below 95% at MP scale erodes that margin directly. 111.6k contingency remaining — a PCB re-spin to fix a missed EMC issue post-cert would consume it entirely.

**Recommendation:** Gate DVT build entry on bench-confirmed antenna data (06/19 latest) and confirmed ICT test coverage report — no board touches the line without both.

**Brain references:** products.md — AMG100 DVT status, 42% margin target

#### [[fw-embedded-team]]

**FW take:**

1. **OTA + rollback before beta** — AMG-100 fleet uptime target is 99.5% (strategy). A bad OTA wave in the September beta trial with no tested rollback path will crater that number permanently. We need canary-wave infrastructure (5% → 20% → 100%) and a validated rollback tested at DVT, not bolted on at MP.

2. **Factory provisioning spec is a DVT gate** — provisioning keys, firmware version, and fault-code map must be locked and documented before the 06/22 build. If the ODM burns default or debug credentials at EVT units, we don't repeat that at DVT. This is a PCI-adjacent risk, not just a process preference.

3. **Diagnostics gap is blocking RMA triage** — EVT yield was 78%; without firmware fault codes distinguishing HW vs FW failures, Field Quality/RMA-FA is guessing. That inflates RMA costs and masks real MTBF data.

**Numbers:** DVT build 06/22 (11 days); 99.5% uptime target unmet at 99.1% alpha; MTBF 62k h vs target.

**Recommendation:** Gate DVT build on: signed provisioning spec, OTA rollback test plan, and fault-code map delivered to Firmware QA.

**Brain references:** products.md (AMG100, DVT status); strategy (99.5% fleet uptime, PCI)

#### [[system-architecture]]

**Architecture take:** Three decisions are live and irreversible if we miss them in the next 11 days — antenna partition, eMMC platform lock, and RF bus-factor single-point-of-failure. All three affect the AMG-100 *and* any Gen 4 that follows.

**Flags:**

1. **ISS-014 antenna rework (3-day buffer):** If the 06/16 parts slip even 48 hours, DVT builds without validated RF. That's not a buffer — that's a cliff. The antenna layout decision made here locks the PCB stackup for the platform family.

2. **Single RF engineer (R-09):** Strategy demands >99.5% fleet uptime. One person owns FCC 47 CFR Part 15 compliance knowledge for the product. That's an architectural bus-factor embedded in a human.

3. **eMMC dual-source:** Component standardization here has platform-wide implications — wrong bet locks three future products.

**Recommendation:** Spend contingency on antenna: parallel a backup supplier now, not after 06/16 slips.

**Brain refs:** strategy.md (>99.5% fleet uptime), products.md (AMG100 DVT status)

### Department synthesis

# Hardware Engineering — Round 1 Position
## AMG-100 DVT Readiness Review | 06/11/2026

---

**Engineering position:** We are not ready to build DVT on 06/22 as-is. Four hard gates are currently open, and three of them have no confirmed closure data. We can get there — but we need decisions and deliverables in the next five days, not eleven.

---

**Team signals:**

**EE team** raised the sharpest single risk: ISS-014 antenna rework has a 3-day buffer after parts land 06/16, but there is zero bench-validation data on the revised antenna placement or matching network. "Matching network" = the small passive components that tune how efficiently the antenna transmits and receives. Without S-parameter (RF reflection/efficiency) data on reworked samples *before* 06/22, we are committing 100+ DVT boards to an unverified fix. EMC/RF certification after 08/18 already has zero schedule slack per the cert plan. A missed antenna fix discovered at certification is a respin — and per the EE team, a PCB respin would consume the entire $111.6k contingency.

**System Architecture** escalated this further: the antenna layout decision made in this build locks the PCB stackup for the platform family, affecting Gen 4 as well. The buffer isn't a buffer — it's a cliff. I am siding with the EE and Architecture teams here over any impulse to hold the date: **06/22 does not move unless antenna bench data is confirmed by 06/19.**

**ME team** flagged thermal and sealing as a yield trap. EVT yield was 78% and we do not yet have a causal breakdown of how many failures were thermally driven vs. electrical vs. mechanical. At 24/7 restaurant duty cycle with ambient temperatures at 35°C+, if the thermal interface material (TIM pad — the heat-conducting layer between chip and enclosure) specification is not locked and validated before the build, we are discovering a thermal problem during DVT, not designing around it. ME is also correct that the enclosure tooling is frozen: any open mechanical ECO (engineering change order — a formal design change) hitting the mold tools now adds 4–6 weeks minimum. **Sealing validation (ISS-019/021/023) must be confirmed in the DVT test matrix before 06/22, not deferred post-build.**

**FW team** identified a PCI-adjacent risk that I will not let slide: if factory provisioning keys and firmware version are not locked in a signed spec before 06/22, we risk repeating the EVT credential error at DVT. PCI PTS pre-assessment is 07/06 — 14 days after the build. Burned-in debug credentials on DVT units arriving at a PCI assessment is not a recoverable situation. **Provisioning spec must be signed before boards are released to the line.** The FW team also correctly ties the 99.1% alpha uptime gap directly to the absence of a validated OTA rollback path — this is a September beta risk, not a post-MP nice-to-have.

**Disagreement to name explicitly:** There is an implicit tension between the Architecture team's recommendation to spend contingency on a parallel antenna supplier *now* and the EE team's position that bench validation of the existing rework fix is the priority. I am siding with EE: parallel sourcing takes weeks to qualify; we need bench data in eight days. The supplier hedge is a right call for Gen 4 platform planning, but it does not solve the 06/16 parts risk. The near-term spend should go to accelerating antenna bench validation (rework labor, RF lab time), not a second supplier that cannot qualify before DVT.

---

**Risks — ranked:**

1. **Antenna rework unvalidated (ISS-014)** — no bench data, 3-day buffer, zero cert slack post-08/18. Owner: EE team. *Critical path constraint.*
2. **EVT yield 78% — failure modes not decomposed by net/component** — if we don't know what failed, DVT's 88% target is a wish. Owner: EE + ME jointly.
3. **Provisioning spec unsigned** — PCI pre-assessment 07/06, 14 days post-build. Owner: FW team.
4. **Thermal characterization not confirmed** — enclosure is frozen; thermal failure found at DVT has no tooling escape. Owner: ME team.
5. **eMMC single-source** — one end-of-life notice away from a respin. Owner: EE + System Architecture.
6. **Single RF engineer (R-09)** — one person owns FCC 47 CFR Part 15 knowledge for the platform. Bus-factor risk for cert and Gen 4. Owner: me to escalate to NPI-PM.

---

**Recommendation:**

Gate DVT build entry on four deliverables, all due **06/19**:

1. Antenna bench validation data (S11/TRP/TIS) on reworked samples — EE team
2. Signed factory provisioning spec — FW team
3. Thermal characterization report with TIM pad spec confirmed — ME team
4. EVT yield failure-mode breakdown by net/component (not symptom) — EE + ME

Spending more to hit these gates is justified. RF lab time, contract rework labor, accelerated thermal testing — all of this is cheaper than a cert respin on the zero-slack path. I will engage [[docs/departments/02-npi-program-management/agents/npi-pm-manager]] on the gate hold and [[docs/departments/03-quality-reliability/agents/quality-manager]] on formalizing these four items as DVT entry criteria. eMMC dual-source qualification should run in parallel as a DVT *exit* gate, not an entry gate — that is the right risk sequencing given the 11-day window.

---

**Brain references:** products.md — AMG100 (DVT status, $329/$, 42% margin); strategy.md — 99.5% fleet uptime, PCI requirement, US casual-dining ICP (spill/sanitizer/24-7 duty cycle); budget.md — $111.6k contingency remaining.

## [[01-Departments/02-npi-program-management/index|02-npi-program-management]]

### Team inputs

#### [[hardware-pm]]

**Program take:** DVT build 06/22, 11 days out. Phase is late-DVT prep. Three things binding this program right now:

**1. ISS-014 antenna parts land 06/16 — 3-day buffer to build start.** Any customs or yield hit on that shipment pushes DVT right, which collapses the cert critical path that already has zero slack after 08/18. This is the single highest-urgency item. Owner and daily status needed today.

**2. MTBF 62k hours is below the trajectory needed for 2.0% AFR.** With alpha uptime at 99.1% vs. 99.5% target and battery 8D still at D6, DVT reliability test coverage must be defined and locked before build — not after. A build without pass criteria is a party (see Principles).

**3. Single RF engineer (R-09) owns the antenna closure.** If ISS-014 resolution requires design judgment at build, that bus-factor is a program risk, not just an HR note.

**Numbers:** 11 days to build. Contingency 111.6k of 2.0M remaining. EVT yield 78% — need +10pp to DVT gate.

**Recommendation:** Confirm ISS-014 parts receipt and inspection plan by 06/13; without that, DVT slip probability is >50%.

**Brain references:** products.md — AMG100, status: DVT

#### [[certification]]

**Cert take:** AMG-100 is a payment-capable tabletop device (PCI PTS required) with Wi-Fi/BT (FCC Part 15 required) and a safety listing obligation (UL/IEC 62368-1 via NRTL). Per laws.md, all three are mandatory for US deployment. The cert plan references a PCI PTS pre-assessment on 07/06 — that's **35 days from today with zero identified lab buffer**, and the cert critical path goes to zero slack after 08/18. That is a stop-ship risk, not a schedule risk.

**Three flags:**

1. **PCI PTS pre-assessment 07/06 is the cert throat.** Any DVT hardware change between 06/22 build and lab submission — mechanical, firmware, RF — can push that date. The antenna rework (ISS-014, parts ETA 06/16, 3-day buffer) is exactly the kind of last-minute change that arrives at DVT build and then gets quietly carried into the lab sample. Lab needs a **frozen, rework-free sample** — if ISS-014 isn't closed clean before 06/22, we should build a cert-dedicated unit with the rework already incorporated, not retrofitted.

2. **Single RF engineer (R-09 bus factor) directly threatens FCC path.** FCC Part 15 authorization for a Wi-Fi/BT device requires antenna characterization, SAR/MPE analysis, and test report preparation — work that lives entirely with one person. If that engineer is consumed by the antenna rework through DVT, FCC submission slips. FCC TCB labs are running 6–8 week queues right now. A 2-week slip in submission = a 2-week slip in authorization = launch at risk. Spend to bring in a contract RF/EMC consultant now; cost is ~$15–25K and it buys parallelism.

3. **No cert-impact verdicts are documented for ISS-019/021/023/025/027/028/030/031/032.** Every one of those open issues is a potential ECO. Per our operating principle, no ECO gets approved without a written cert-impact answer. If any of those issues resolves with a component swap, a firmware security patch, or a mechanical dimensional change, it can re-trigger PCI PTS, FCC, or safety listing. I need a cert-impact screen run on all nine issues **before DVT build, not after**.

**Numbers:**
- PCI PTS pre-assessment: 07/06 (25 days post-DVT build) — lab queue risk if sample isn't clean
- FCC TCB queue: ~6–8 weeks from submission → submission must be no later than early July to clear before beta Sept
- Safety NRTL: typically 8–12 weeks; must be in parallel, not sequential
- Contract RF consultant: ~$15–25K, available in 1–2 weeks
- Cert-dedicated DVT unit (separate from functional test pool): ~$5–10K incremental build cost, eliminates rework-on-cert-sample risk

**Recommendation:** Freeze cert sample hardware NOW (pre-rework closure), run a written cert-impact screen on all nine open issues before 06/22, and fund a contract RF consultant immediately to eliminate the single-point-of-failure on FCC path — these three actions protect the only hard stop-ship gate in the program.

**Brain references:** laws.md (FCC 47 CFR Part 15; UL/IEC 62368-1 NRTL; PCI PTS implied by payment-capable device per products.md AMG-100 feature set); products.md (AMG-100 DVT status, payment/RF content); state.md (growth stage — a cert slip at launch is a revenue event, not just a schedule event)

#### [[bom-eco-plm]]

**BOM/ECO take:** AMG-100 is 11 days from DVT build with no confirmed revision baseline locked. The antenna rework (ISS-014) is the live landmine — parts ETA 06/16 gives 3 days to receive, inspect, update the BOM, issue a formal ECO, and get factory acknowledgment before 06/22. That is not enough buffer if customs or incoming inspection slips even one day.

**Numbers:** eMMC dual-source ECO is still "in flight" — until a second AVL entry is approved and effectivity set, we're one supplier disruption from a build stop. AMG-100 DVT BOM must reflect the antenna change at a locked revision before the build starts, or we're building to an ambiguous spec. Contingency is $111.6k — one rework loop on wrong-rev units burns that fast.

**Flags:**
1. Antenna ECO must have explicit effectivity (serial number cut-in) and cert-impact box completed before 06/22 — no exceptions
2. eMMC alternate-source AVL approval needs a hard closure date, not "in flight"
3. DVT BOM freeze date should be 06/18 at the latest — two days before build to allow factory acknowledgment

**Recommendation:** Lock DVT BOM revision by 06/18, close antenna ECO with cert sign-off by 06/17, or push DVT rather than build to an uncontrolled revision.

**Brain references:** products.md — AMG-100 status: DVT; margin 42% leaves room to absorb expedite costs to protect revision integrity.

#### [[launch-readiness]]

**Readiness take:** CONDITIONAL NO-GO for DVT build confidence. Launch chain has structural gaps that will surface at first shipment if not closed now.

**Three flags:**

1. **Ramp criteria aren't locked.** 88% DVT yield target exists but I need written agreement on escape thresholds, capacity gates, and who signs the DVT exit — verbal alignment doesn't count (products.md: AMG100 DVT status).

2. **Service side is launch scope, not post-launch.** Beta trial starts September. Depot readiness, RMA lane, and spare parts stocking need owners and dates *now* — not after DVT exit. TS-90R pool (products.md) shows we know how to run RMA; replicate that infrastructure for AMG-100 before beta ships.

3. **Packaging/label/cert chain has zero slack after 08/18.** FCC Part 15 + UL/IEC 62368-1 + PCI/EMV all required (laws). One slip cascades directly into ship date. Need cert evidence on file, not "in progress."

**Numbers:** 9 open issues, 111.6k contingency, beta September.

**Recommendation:** Spend contingency to accelerate depot setup and cert pre-work; freeze ramp criteria this week.

#### [[sourcing-buyer]]

**Sourcing take:** eMMC dual-source qualification is in-flight but unconfirmed — this is the single highest-risk material exposure for DVT and ramp. If second source isn't PO-ready before Tet pre-build, we're effectively single-sourced into a 95% MP yield ramp. RF module is similarly exposed given the single-engineer bus factor (R-09); if that engineer is unavailable, alternate sourcing decisions stall.

**Numbers:** 872k spent / 2.0M budget; 111.6k contingency remaining. Tet pre-build timing means any eMMC shortage surfacing post-holidays hits with zero recovery runway. Broker risk is real if we scramble — authenticity controls mandatory, cost premium likely 15-25%.

**Recommendation:** Expedite eMMC second-source qualification POs now (cost delta acceptable), lock Tet pre-build quantities against confirmed dual sources only, and document a written exit plan for RF module single-source before DVT builds start 06/22.

**Brain references:** products.md (AMG100, DVT status), budget.md (2.0M material budget, 111.6k contingency)

#### [[odm-program-mgmt]]

**Factory take:** DVT build on 06/22 is 11 days out and I don't have written factory commits confirmed against the antenna rework parts (ISS-014, ETA 06/16 — 3-day buffer only). If that shipment slips 72 hours for any reason — customs hold, courier miss, inspection fail — DVT moves. That's not acceptable with zero cert slack after 08/18.

**Numbers:**
- ISS-014 antenna parts: 06/16 ETA, 3-day buffer to 06/22 build start. Need written factory receiving confirm by EOD 06/17.
- BrightPath single-site (strategy.md: site concentration risk) — no fallback qualified for AMG-100 tooling. DVT → PVT transition is the last low-cost window to run an overlap build at a second site.
- Contingency: $111.6K remaining. Expedite freight + buffer stock on antenna rework parts is spend I'd authorize today.

**Recommendation:** Get written factory commit on antenna parts receipt by 06/17 or escalate to air-freight expedite immediately — DVT date is not movable given cert critical path.

**Brain references:** products.md (AMG100, DVT status), strategy.md (site risk, uptime target)

### Department synthesis

# NPI & Program Management — Round 1 Position
## AMG-100 Program Review | 06/11/2026

---

**Program position:** AMG-100 is 11 days from DVT build in a fragile but recoverable state. The program has a hard certification stop-ship boundary at 08/18 with zero slack, a 3-day material buffer on the antenna rework parts that is the single most acute near-term risk, and a reliability trajectory that is not yet consistent with the 99.5% fleet uptime target in strategy.md. Spending to protect quality gates is authorized; compressing gate criteria is not.

---

**Team signals — what each team raised and where they agree or disagree:**

Every team converged on three points independently, which gives me high confidence in them:
1. **ISS-014 antenna parts (ETA 06/16, 3-day buffer) is the single highest-urgency item.** Hardware PM, BOM/ECO, ODM, and Sourcing all flagged it. If that shipment slips one day for customs, courier miss, or incoming inspection failure, DVT moves — and DVT moving collapses the cert critical path.
2. **The R-09 single RF engineer bus factor is a real program risk, not an HR footnote.** Certification and Hardware PM both named it. FCC Part 15 authorization for a Wi-Fi/BT device cannot advance without RF expertise, and TCB labs are running 6–8 week queues right now.
3. **eMMC dual-source is unconfirmed and is the highest-risk material exposure for ramp.** Sourcing and BOM/ECO both flagged it; if second-source AVL isn't approved with a PO-ready date before Tet pre-build, we are effectively single-sourced into a 95% MP yield ramp.

One productive tension: BOM/ECO says DVT BOM freeze must be 06/18 — two days before build — to allow factory acknowledgment. ODM says they need written factory receiving confirmation on antenna parts by EOD 06/17. These are compatible, but the sequencing is tight: parts land 06/16, inspection clears 06/17 (confirmed in writing), ECO closes with cert-impact sign-off 06/17, BOM freezes 06/18. That chain has no slack. I am not averaging this — I am stating it as a hard sequence that requires daily owner accountability starting today.

---

**Critical path — the binding constraint:**

**PCI PTS pre-assessment on 07/06** is the certification throat. It sits 25 days after DVT build and has zero schedule slack after 08/18 (per Certification and Hardware PM, independently). The lab needs a frozen, rework-free hardware sample. The antenna rework on ISS-014 — if not fully closed before 06/22 build — risks being quietly carried into the cert sample as a retrofit, which is exactly the kind of thing that fails a pre-assessment and burns 3–4 weeks of recovery time we do not have. Per Certification: build a dedicated cert unit with the rework already incorporated, not retrofitted. That is the right call and I am adopting it.

The binding date sequence is:
- **06/16** — ISS-014 parts land
- **06/17** — Incoming inspection complete; factory receiving confirmation in writing; antenna ECO signed with cert-impact box completed
- **06/18** — DVT BOM frozen at locked revision
- **06/22** — DVT build starts against clean, frozen BOM
- **07/06** — PCI PTS pre-assessment with rework-free cert sample
- **08/18** — Last date with any schedule slack on cert path

Miss 06/17 and 06/22 is at risk. Miss 06/22 and 07/06 is at risk. Miss 07/06 clean and 08/18 becomes a stop-ship exposure.

---

**Reliability flag (separate from cert):**

MTBF at 62k hours is below the trajectory needed for 2.0% AFR. Alpha uptime is 99.1% vs. 99.5% target (strategy.md). Battery 8D is at D6 — root cause not closed. Per Hardware PM: DVT reliability test coverage must be defined and locked *before* build starts, not after. A build without pass criteria is not a gate — it is a party. This is non-negotiable per our principles.

---

**Budget position:**

$872k spent of $2.0M; $111.6k contingency remaining (budget.md). Contingency is thin relative to the open risks. Specific spend I would authorize today:

- Contract RF/EMC consultant: ~$15–25k (per Certification) — buys parallelism on FCC path and eliminates the R-09 single-point-of-failure
- Dedicated cert DVT unit: ~$5–10k incremental build cost — eliminates rework-on-cert-sample risk
- Antenna parts air-freight expedite buffer: authorize now (per ODM) — cost is likely $5–15k and it buys the 06/17 confirmation deadline
- eMMC second-source qualification POs: cost delta acceptable per Sourcing — lock this before Tet pre-build

Total incremental spend to de-risk the critical path: roughly $25–50k against $111.6k contingency. That is justified. Spending it protects a 42% margin product (products.md, AMG-100) with a September beta trial and a stop-ship cert gate. Not spending it risks a multi-week slip that costs far more in revenue and customer credibility.

---

**Nine open issues (ISS-019/021/023/025/027/028/030/031/032):**

Per Certification: none of these have documented cert-impact verdicts. Every one is a potential ECO. If any resolves with a component swap, a firmware security patch, or a mechanical dimensional change, it can re-trigger PCI PTS, FCC, or safety listing. A cert-impact screen must be run on all nine **before DVT build on 06/22**, not after. This is not optional — it is the discipline that prevents a post-DVT ECO from blowing up the 07/06 pre-assessment. Owner: BOM/ECO with Certification sign-off. Deadline: 06/19 (three days before build, one day after BOM freeze, to allow any last sequencing).

---

**Recommendation:**

Five actions, sequenced by urgency:

1. **Today (06/11):** Assign a named daily owner to ISS-014 parts tracking. Confirm air-freight expedite authorization for antenna parts if 06/16 ETA is at any risk. Authorize contract RF/EMC consultant engagement immediately (~$15–25k). *(Owners: ODM for factory commit, Sourcing for parts tracking, Certification for consultant scope)*

2. **By 06/17:** ISS-014 antenna parts received and inspected; ECO closed with cert-impact box signed off; factory receiving confirmation in writing. No exceptions — if this date slips, we formally assess DVT date move rather than carry the risk silently. *(Owners: BOM/ECO, ODM, Certification)*

3. **By 06/18:** DVT BOM frozen at locked revision. Written DVT gate pass criteria finalized — yield (88%), reliability test coverage, battery 8D closure plan. *(Owners: BOM/ECO, Hardware PM, Quality — gate criteria sign-off per our workflow)*

4. **By 06/19:** Written cert-impact screen completed on all nine open issues (ISS-019 through ISS-032). Dedicated cert DVT unit designated in the build plan (~$5–10k). *(Owners: BOM/ECO + Certification)*

5. **Before 06/22 build start:** eMMC second-source AVL approval with hard closure date and PO-ready status confirmed. BrightPath second-site overlap build scoped for DVT→PVT window (this is the last low-cost opportunity per ODM). *(Owners: Sourcing, ODM)*

**No action in this plan weakens a quality gate.** Gate criteria are not negotiated — spend is. The $25–50k incremental authorization I am recommending buys the conditions under which the gates can actually be passed, not waived.

**Brain references:** products.md (AMG-100, DVT status, 42% margin); strategy.md (99.5% fleet uptime target, growth state); budget.md (2.0M material budget, 111.6k contingency); laws.md (FCC 47 CFR Part 15; UL/IEC 62368-1 NRTL; PCI PTS payment device obligation)

## [[01-Departments/03-quality-reliability/index|03-quality-reliability]]

### Team inputs

#### [[qa-system]]

**QA System take:** DVT build in 11 days with 9 open issues, 78% EVT yield, and a cert critical path with zero slack post-08/18 — the QMS is being stress-tested simultaneously on incoming quality, process capability, and certification evidence integrity.

**Numbers:**
- 3 items demand immediate system-level response: EVT yield 78% vs DVT gate 88% (10-point gap, no procedure yet written for what happens if DVT misses), battery 8D stuck at D6 (CAPA is open but closure evidence undefined), and zero-slack cert path means any stale/missing document post-08/18 = ship delay
- 9 open issues entering DVT with no stated closure criteria in the record is an audit finding waiting to happen

**Recommendation:** Before 06/22, document explicit pass/fail criteria for each open issue and the DVT yield gate — controlled, owned, dated — so closure is evidence-based, not declared.

**Brain references:** laws.md — UL/IEC 62368-1 NRTL listing and FCC 47 CFR Part 15 both require traceable test records; a zero-slack cert path means document control failures become certification failures.

#### [[qc-inspection]]

**Inspection take:** DVT build lands in 11 days with no incoming inspection criteria locked for AMG-100 components. Zero prior lot history on AMG-100 parts — we're flying blind on Day 1 yield. eMMC single-source (dual-source "in flight") means no switching-rule baseline exists yet. EVT yield was 78% — dock escapes likely contributed; we don't know because EVT inspection records aren't cited.

**Numbers:**
- DVT build 06/22 — need AQL criteria, visual workmanship photos, and dimensional limits finalized by **06/18** (4 days before build)
- Antenna rework parts ETA 06/16: 3-day buffer requires immediate incoming inspection plan — no criteria = no inspection = blind build
- eMMC: tightened sampling (AQL 0.65 critical / 1.0 major) until second source qualifies and we have 3+ accepted lots
- Battery 8D at D6: no battery lot ships to DVT without passed dimensional + capacity incoming check

**Recommendation:** Spend $8–12K now on expedited criteria documentation and pilot-lot inspection fixtures — an escape into DVT costs 10× more than catching it at the dock.

**Brain references:** products.md — AMG-100 DVT status; 78% EVT yield signals upstream process not yet capable, skip-lot is years away.

#### [[validation-reliability]]

**Validation take:** DVT gate is 11 days out with three reliability red flags that cannot be papered over: MTBF at 62k hrs doesn't close the 2.0% AFR target mathematically, alpha uptime 99.1% is 40 basis points short of the 99.5% fleet goal (strategy.vision), and battery 8D is still at D6 — root cause not closed before we build DVT units we'll need for life testing.

**Numbers:**
- MTBF 62k h → AFR ≈ 1.59% best case; need ~43.8k h for 2.0% — we're actually *above* target on MTBF but alpha uptime gap signals a systematic field-mode failure not captured in bench prediction
- EVT yield 78% → DVT target 88%: 10-point jump requires identified yield loss mechanisms, not hope
- Contingency: $111.6k remaining of $2.0M — thin

**Recommendation:** Before DVT build approval, require written root-cause closure on battery 8D and alpha uptime gap; treat them as gate criteria, not post-DVT action items.

**Brain references:** products.md — AMG100 status: DVT; strategy — >99.5% fleet uptime

#### [[firmware-qa]]

**FW QA take:** HOLD — three blocking issues before DVT build starts.

**Must-flag:**

1. **Update path coverage is undefined for TS-90 fleet (products.md — TS-90 MP, TS-90R Active).** AMG-100 will eventually coexist in mixed fleets. If OTA infrastructure is shared, regression must cover rollback from every TS-90 firmware version currently fielded. No evidence this is scoped. Battery 8D at D6 means power-loss-mid-update scenarios on degraded cells are untested — that's the highest-risk OTA failure mode in a 24/7 casual-dining duty cycle.

2. **Single RF engineer (R-09) owns antenna validation firmware + radio stack.** If that person is blocked, OTA and radio regression cannot complete before the cert critical path freezes 08/18. Zero slack means one person's absence kills the release.

3. **EVT yield 78% → DVT target 88% is a 10-point jump with no confirmed root-cause closure on the yield drivers.** Shipping firmware on hardware that isn't stable is gating on hope.

**Numbers:** 0 OTA regression runs confirmed, R-09 single point, 08/18 zero-slack gate.

**Recommendation:** Do not enter DVT firmware integration until OTA update-path test plan is signed and R-09 bus-factor is mitigated with a second-qualified reviewer.

**Brain references:** products.md (TS-90 MP, TS-90R Active); state: growth (>99.5% fleet uptime target non-negotiable).

#### [[field-quality-rma-fa]]

**Field Quality take:**

Three signals demand immediate attention before DVT builds start.

**1. Battery 8D stuck at D6 — this is the highest risk.**
An unresolved battery failure mechanism entering DVT means we're building potentially flawed units into the beta population. D6 (implement corrective action) must reach D7 (validated) before beta trial units ship in September. With alpha uptime at 99.1% vs. 99.5% target, battery is likely a contributor. I need bench findings from Repair to confirm mechanism, not just symptom.

**2. EVT yield 78% → DVT target 88%.**
We don't know which failure modes drove the 22% EVT fallout. Without a Pareto by mode and cohort, we're flying blind into DVT. If connector, display, or RF assembly are top causes, those become field reliability predictors — and with TS-90 in the installed base for rate benchmarking, we have a comparison floor.

**3. 99.5% fleet uptime is the strategic target (Brain: strategy.vision).**
MTBF 62k hours sounds good in isolation, but AFR math needs to be validated against actual field cohort data from TS-90 returns — not just prediction models.

**Recommendation:** No DVT build until battery 8D reaches D7 and EVT yield Pareto is published with owners on top-3 modes.

### Department synthesis

# Quality & Reliability — Round 1 Position
## AMG-100 DVT Readiness | 06/11/2026

---

**Quality position:** No clean bill of health for 06/22 DVT build as the program currently stands. Four conditions must be met before build-start authorization; none require stopping the clock — they require front-loading work in the next 11 days. No product is on ship-hold today, but DVT entry is conditionally gated.

---

**Team signals — what each team raised, and where they agree or diverge:**

All five teams converged on three issues independently, which tells me these are real, not noise:

1. **Battery 8D stuck at D6** — every team flagged this. No team accepted "corrective action in progress" as sufficient to build DVT units. Per Field Quality/RMA-FA: D6 must reach D7 (validated closure) before beta units ship in September. I agree, and I'm pulling the gate earlier: D7 evidence required *before* DVT build-start, not after.

2. **EVT yield 78% with no published Pareto** — QC Inspection, Validation, and Field Quality all flagged that the 10-point gap to the 88% DVT gate has no identified root causes attached to it. We are not jumping 10 points on hope. Per QC Inspection: without knowing whether that 22% fallout came from connectors, RF assembly, display, or dock, our incoming inspection criteria are targeting the wrong things.

3. **Zero-slack cert path after 08/18** — QA System and Firmware QA both flagged this from different angles. QA System: stale or missing documents after 08/18 become certification failures under UL/IEC 62368-1 and FCC 47 CFR Part 15 (laws.md). Firmware QA: R-09 is a single point of failure for the radio stack and antenna validation firmware — one absence and the cert path breaks.

**One internal disagreement to name honestly:** Firmware QA called a full HOLD on DVT firmware integration; Validation and QC Inspection stopped short of a full hold and focused on specific gate criteria instead. My position: Firmware QA's HOLD is correct on OTA regression coverage and the R-09 bus-factor, but it doesn't require delaying the *hardware* DVT build — it means firmware integration cannot be called complete until those two conditions are met. I will not let schedule pressure collapse that distinction in the wrong direction.

---

**Risk — what escapes if we proceed as asked:**

- **Battery failure mode unresolved → beta units in the field September with a known-open 8D.** In a 24/7 casual-dining duty cycle with power-loss-mid-OTA as the highest-risk update scenario (per Firmware QA), this is a safety-adjacent field escape, not a yield stat.
- **No incoming inspection criteria for AMG-100 parts by 06/22 → dock escapes compound the EVT yield problem into DVT.** Per QC Inspection: $8–12K now versus 10× that cost when escapes surface mid-build.
- **R-09 single point on cert critical path → one personnel event after 08/18 causes a ship delay.** Fleet uptime target of >99.5% (strategy.md) is unreachable if we ship late into a market that's already comparing us to TS-90 benchmarks.
- **9 open issues entering DVT without documented pass/fail closure criteria → audit finding, and potential evidence gap for NRTL listing.** Per QA System: this is traceable-record risk, not a paperwork preference.

---

**Recommendation (containment + CAPA + verification):**

Four actions before 06/22; owners handed off where appropriate:

1. **Battery 8D to D7 by 06/18** — no DVT build-start without validated corrective action evidence. Owner: Field Quality/RMA-FA leads the 8D; design-cause elements hand off to HW Engineering. Dimensional + capacity incoming check on every battery lot entering DVT (per QC Inspection).

2. **EVT yield Pareto published by 06/15, top-3 failure modes with owners** — this feeds incoming inspection criteria (due 06/18 per QC Inspection), DVT process controls, and Validation's life-test configuration decisions. Owner: QC Inspection + Field Quality/RMA-FA jointly; manufacturing process causes hand off to MSQ Manager.

3. **All 9 open issues assigned explicit pass/fail closure criteria in the controlled document system by 06/15** — date-stamped, owner-named, evidence-defined. "Closed" without before/after data will reopen. Owner: QA System.

4. **R-09 bus-factor mitigated by 06/18** — second-qualified engineer designated and read into radio stack and antenna validation firmware. OTA regression test plan covering TS-90 fleet rollback scenarios signed off before firmware integration is called complete. Owner: Firmware QA escalates to NPI PM Manager for resource action; I will co-sign the escalation.

Spending $8–12K on expedited inspection criteria and fixtures (per QC Inspection's estimate) is approved in principle — that is well within contingency ($111.6K remaining, budget-tracker) and is the highest-ROI spend on the table right now.

---

**Brain references:** products.md — AMG-100 DVT status, TS-90 MP/TS-90R Active (mixed-fleet OTA risk); laws.md — UL/IEC 62368-1 NRTL listing, FCC 47 CFR Part 15 (traceable cert records); strategy.md — >99.5% fleet uptime (the number every reliability gap is measured against).

## [[01-Departments/04-mfg-supplier-quality/index|04-mfg-supplier-quality]]

### Team inputs

#### [[odm-quality]]

**ODM Quality take:** DVT build is 11 days out with antenna rework parts arriving 06/16 — that's a 3-day buffer to verify rework quality, update golden samples, and confirm OQC criteria before build kick-off. That is not enough time if the rework introduces any dimensional or RF impedance variation. EVT yield at 78% must be decomposed by failure mode *at the line*, not from slide summaries — I need OQC station data and FPY by station before DVT starts.

**Numbers:** EVT 78% yield → DVT target 88% = 10-point gain required. MTBF 62k hrs vs. target implied by 2.0% AFR (~50k hrs is fine, but alpha uptime 99.1% vs. 99.5% target suggests field escapes from process variation, not just design). Contingency 111.6k remaining.

**Flags:**
1. Antenna rework = unauthorized-change risk — golden sample comparison and material cert required before 06/22 build release
2. 78% EVT yield root cause must be closed *before* DVT build, not during
3. BrightPath single-site: OQC correlation audit needed now

**Recommendation:** Gate DVT build release on signed-off rework golden sample and station-level EVT Pareto — no build until both confirmed.

**Brain references:** products.md — AMG100 (DVT status)

#### [[supplier-quality]]

**Supplier Quality take:** AVL is the weak point entering DVT. eMMC dual-source qualification is "in flight" — meaning we're 11 days from a build with a single qualified source on a critical storage component. That's a hard qualification gap, not a schedule note.

**Numbers:**
- eMMC: 1 of 2 required sources qualified — dual-source rule violated until closed
- EVT yield 78% — component-level escapes likely contributed; need lot-level rejection data before DVT kits ship
- BrightPath single-site: no approved alternate = supply continuity risk on the AVL
- Broker/Tet pre-build parts: must run full authenticity protocol before any lot enters the build — non-negotiable

**Three flags:**
1. Do NOT pull eMMC alternate parts into the 06/22 DVT build unqualified — run FAI on qualified source only, parallel-track second source audit now
2. Tet pre-build inventory needs authenticity screening logged before kit release
3. 78% EVT yield needs component-level Pareto before DVT kits are committed

**Recommendation:** Fund accelerated eMMC second-source audit immediately (~$15–25K travel/lab); DVT builds only on qualified lots.

**Brain references:** products.md — AMG-100 DVT status; decisions-log — no recorded risk acceptance on single-source eMMC

#### [[manufacturing-engineering]]

**Mfg engineering take:** DVT build in 11 days is the real test. EVT yield of 78% tells me at least one process step is broken — not just a design problem. I need to know which station is the yield killer before we repeat the same process at DVT and buy the same defects at higher volume.

**Numbers I'm watching:**
- 78% EVT → 88% DVT target = 10-point lift required in one build cycle. That's achievable only if we already know the root cause and have a process fix verified, not just a theory.
- Antenna rework parts landing 06/16 gives 3 working days to update fixtures/work instructions before 06/22. That is not enough if any mechanical fit changed.
- Battery 8D at D6 means chemistry or formation parameters are still open — formation is a line-time gate we can't shortcut.

**Recommendation:** Force a pre-DVT process FMEA walk on the top 3 yield loss modes from EVT before parts arrive; no build until station capability is confirmed on the antenna rework geometry.

**Brain references:** products.md — AMG100 (DVT status)

#### [[factory-test-yield]]

**Test/Yield Take:**

EVT FPY at 78% is the anchor problem for the whole program. Three flags:

1. **78% → 88% DVT path is unproven.** We don't have a clean fallout Pareto from EVT — we need to know what fraction is genuine HW defects (fixable by DVT design changes), what's fixture/station artifact, and what's retest-to-pass hiding real escapes. If retest rate at EVT was >5%, the 78% headline is lying in both directions.

2. **Antenna rework (ISS-014) will stress ICT/FCT RF coverage.** New antenna geometry arriving 06/16 means our test limits and golden units need requalification before 06/22 build. Three days is not enough to recorrelate RF test stations — this is an escape vector.

3. **Station correlation between Tet pre-build and full MP line is unestablished.** Single-site BrightPath risk means we may ship with one station dataset. Two uncorrelated stations = two products.

**Numbers:** EVT FPY 78%, DVT target 88% (10pt gap, root cause not closed), retest rate unknown.

**Recommendation:** Mandate EVT fallout Pareto with retest discipline audit before 06/22 — no DVT build until station correlation plan is signed off.

**Brain references:** products.md — AMG100 DVT status; state: growth (quality gates inviolable per brief).

### Department synthesis

**MSQ Position:** DVT build in 11 days is not ready. Four independent teams have landed on the same conclusion through different lenses — this is not pessimism, it's signal. The factory-quality state for AMG-100 entering DVT is: yield root cause open, rework qualification incomplete, eMMC single-sourced, and test station correlation unestablished. Any one of those is a gate hold. All four together means we'd be purchasing defects at higher volume with no ability to separate process noise from design progress.

---

**Team Signals:**

All four teams are aligned on the core problem — EVT 78% FPY is unresolved — but each adds a distinct dimension:

- **ODM Quality** flags the antenna rework (ISS-014) as an unauthorized-change risk: 3 days is insufficient to verify dimensional conformance, update golden samples, and requalify OQC criteria. Hard agree.
- **Supplier Quality** flags the eMMC dual-source gap as a hard AVL violation, not a schedule note. Also flags that Tet pre-build inventory needs documented authenticity screening before any kit is released. Hard agree on both — per decisions-log, there is no recorded risk acceptance on single-source eMMC entering DVT.
- **Manufacturing Engineering** flags that 78% → 88% in one build cycle is only achievable if root cause is already closed and a verified process fix is in place. Running DVT on a broken process buys the same defects at higher volume.
- **Factory Test/Yield** adds the sharpest concern: we don't have a clean EVT fallout Pareto. If EVT retest rate exceeded 5%, the 78% headline is distorted in both directions — it may hide real escapes *and* inflate apparent defects. RF test station requalification after the antenna rework also cannot be done in 3 days.

No material disagreements between teams. Manufacturing Engineering and Factory Test are the most emphatic about the "fix before build" principle; Supplier Quality is most emphatic about the eMMC gate. ODM Quality is most emphatic about the rework golden sample requirement. All four are correct.

---

**Numbers** (per EVT data and Brain/products.md — AMG-100 DVT status):

| Metric | Current | Target | Gap |
|---|---|---|---|
| EVT FPY | 78% | 88% (DVT) | 10 pts — root cause not closed |
| MTBF | 62,000 hrs | ~50,000 hrs (2.0% AFR) | Passes, but alpha uptime 99.1% vs. 99.5% suggests field escapes from process variation |
| eMMC sources qualified | 1 of 2 | 2 (dual-source rule) | Hard gap |
| EVT retest rate | Unknown | <5% | Cannot validate 78% headline |
| Contingency remaining | $111,600 | — | Limited; targeted spend justified |

---

**Recommendation:**

**Gate DVT build release. Do not build on 06/22 until the following are confirmed — each has an owner:**

1. **EVT fallout Pareto with retest discipline audit** — Factory Test/Yield owns; ODM Quality co-signs station data. Required before any DVT kit commitment. Without this, we cannot know if 78% is a design problem, a fixture problem, or a test artifact. *Deadline: 06/16.*

2. **Antenna rework (ISS-014) golden sample sign-off** — ODM Quality owns; Manufacturing Engineering validates fixture/work-instruction changes for new geometry. Golden sample comparison + material cert required before build release, not concurrently. *Deadline: 06/18 at latest, to allow 4 days before build.*

3. **RF test station requalification after rework geometry change** — Factory Test/Yield owns with Manufacturing Engineering. Three days (06/16–06/19) is the window; if requalification cannot be completed by 06/19, the build date moves. *Deadline: 06/19.*

4. **eMMC qualified-source-only DVT kits; accelerated second-source audit funded now** — Supplier Quality owns. Recommend spending $15–25K (travel + lab) immediately to accelerate second-source audit. This is the single highest-value spend of remaining contingency. DVT builds only on qualified lots — no exceptions. *Audit initiated: 06/12; build kits from qualified source only.*

5. **Tet pre-build authenticity screening documented** — Supplier Quality owns. Lot-level authentication log required before kit release. Non-negotiable. *Deadline: before kit release.*

6. **Pre-DVT process FMEA on top 3 EVT yield loss modes** — Manufacturing Engineering owns. Walk the line on the specific failure modes from the Pareto (item 1 above). No build until station capability is confirmed on the rework geometry. *Deadline: 06/19.*

**Handoffs:**
- Schedule impact of a build slip → [[npi-pm-manager]]: if 06/22 build moves to 06/25–06/26, what is the downstream effect on PCI PTS pre-assessment 07/06 and the cert critical path with zero slack after 08/18?
- Alpha uptime 99.1% vs. 99.5% target and battery 8D still at D6 → [[quality-manager]]: field escape correlation needed to separate design causes from process variation before DVT build scope is finalized.
- Antenna dimensional changes from rework → [[hw-engineering-manager]]: confirm no impedance or fit change from ISS-014 rework parts before golden sample sign-off.

**Bottom line:** A 3–5 day slip to DVT build, used to close these five items properly, costs less than a repeat DVT cycle caused by process noise drowning out design-change signal. The contingency ($111.6K) should fund the eMMC second-source audit first — that is the highest-leverage spend available right now.

**Brain references:** products.md — AMG-100 (DVT status); decisions-log — no recorded risk acceptance on single-source eMMC; state: growth (quality gates confirmed inviolable).

## [[01-Departments/05-service-operations/index|05-service-operations]]

### Team inputs

#### [[repair]]

**Repair take:** DVT build 11 days out — repair bench needs to be in the loop now, not at beta.

**Three flags:**

1. **EVT yield 78% means ~22% of DVT units will likely return to bench.** At 88% DVT target, we're chasing 10 points of yield improvement with zero repair runbook yet written. If fault codes aren't standardized before 06/22, NFF units pile up undiagnosed. NFF is a trash bin here until proven otherwise.

2. **TS-90R refurb margin is 22% — depot economics are tight.** AMG-100 repair cost ceiling needs to be set *before* beta (Sept), not after. Battery 8D at D6 is a red flag: if cell swaps become a depot repair action, that needs a test spec and a parts kanban before ramp.

3. **Single RF engineer (R-09) is a bench dependency too** — antenna rework diagnostic criteria come from that person. If ISS-014 parts slip past 06/16, we need written rework instructions in hand, not tribal knowledge.

**Recommendation:** Issue repair intake criteria, fault code taxonomy, and repair cost ceiling for AMG-100 before DVT build starts — bench readiness is on the critical path.

**Brain references:** products.md (TS-90R, AMG-100); state.md (growth stage, >99.5% uptime target)

#### [[fulfillment]]

**Fulfillment take:** DVT is 11 days out and I cannot commit a single ship date against AMG-100 until three things are confirmed: eMMC dual-source qualification (single-source = allocation risk at ramp), factory yield reaching 88% DVT target (78% EVT means ~22% of units can't be kitted and shipped as configured), and firmware/config baseline locked before bench verification protocols are written.

**Numbers:**
- EVT yield 78% → if that holds into DVT, ~1 in 5 units fails kitting verification — unacceptable mis-ship risk
- eMMC single-source (products.md, supply chain) — no approved alternate means I cannot substitute without violating anti-pattern #1
- Beta trial September: depot and serialization infrastructure must be ready 4–6 weeks prior

**Flags:**
1. No approved eMMC alternate = I cannot promise allocation to beta sites
2. 78% yield = kitting throughput is severely degraded
3. Depot readiness for beta needs a confirmed date now

**Recommendation:** Lock eMMC dual-source qualification and DVT yield target as hard gates before any beta ship date is committed.

**Brain references:** products.md (AMG100, DVT status); state.md (growth stage, fleet uptime vision)

#### [[inventory]]

**Inventory take:** DVT is 11 days out and I don't have confirmed spares pool sizing for the beta trial (Sept) or depot readiness — that's the gap I'm flagging now, not after beta starts.

**Three flags:**

1. **TS-90R pool cannibalization risk.** Beta trial will pull refurb AMG-100 units before we have failure-rate data. If we size the pool wrong, we raid TS-90R stock (products.md: TS90R, $145, 22% margin) and distort RMA fill rates for existing MP customers.

2. **eMMC single-source = E&O cliff.** If dual-source qualifies late and we overbuy primary-source eMMC, we're holding aging components with no exit — carrying cost hits the $6.8M budget with zero revenue offset.

3. **No depot parts kanban yet.** Without DVT yield data (currently 78%, target 88%), I can't set repair-parts reorder points. Waiting until beta to learn failure modes is too late.

**Numbers:** Yield gap = 10 pts; alpha uptime 99.1% vs 99.5% target — both drive spares pool up.

**Recommendation:** Fund a small DVT-yield-informed spares pre-build now; don't wait for beta failure data.

**Brain references:** products.md (TS90R, AMG100), budget.md (total $6.8M)

#### [[deployment-support]]

**Deployment take:** Beta trial (Sept) and ramp gates are at risk — depot isn't ready to support a fleet that hasn't hit 99.5% uptime yet, and we have no confirmed spares buffer staged for the beta wave.

**Three flags:**

1. **Alpha uptime 99.1% vs. 99.5% target** — if this doesn't close before beta, we'll be swapping units live in customer venues with no depot stock confirmed. That's a cannibalization scenario waiting to happen.

2. **Depot readiness undefined** — no acceptance criteria, no trained techs, no spares policy locked before a Sept beta with real restaurant sites. "Installed" without sign-off is an open order; beta sites need the same rigor.

3. **Battery 8D at D6** — field swap policy for battery failures isn't set. If units start degrading mid-beta, we need a clear swap-vs-return decision tree before wave 1.

**Recommendation:** Gate beta entry on depot readiness sign-off and staged spares — not just device DVT pass.

**Brain references:** strategy.md (>99.5% fleet uptime, harsh 24/7 environment), state.md (growth stage, AMG-100 DVT)

#### [[logistics]]

**Logistics take:** Three issues demand immediate flag: (1) **ISS-014 antenna rework parts ETA 06/16** — 3-day buffer to 06/22 DVT build is unacceptable. Any customs hold, courier exception, or DG paperwork gap on lithium-containing assemblies kills the build date. (2) **BrightPath single-site risk** — one factory failure or export disruption collapses the entire ramp lane with no qualified alternate routing. (3) **Tet pre-build** — we need inventory positioned before February; ocean lead times from China/Vietnam mean PO cutoff is ~October, and that window is already tight given current DVT/MP schedule.

**Numbers:** Antenna parts on air freight — estimate $8–15K expedite premium vs. ocean; worth every dollar. BrightPath dual-site qualification adds ~$40–60K logistics setup (separate HTS validation, new origin docs) but eliminates a single point of failure on a $329 product with 42% margin.

**Recommendation:** Confirm antenna parts cleared customs today; escalate to air courier with dedicated DG handling — do not accept broker assurance without proof of entry.

**Brain references:** laws.md (19 U.S.C. HTS; 49 CFR/IATA DG lithium battery transport); products.md (AMG100, AMG-D10 battery content); budget.md (2.0M program budget, 111.6K contingency)

### Department synthesis

# Service Operations — Round 1 Position: AMG-100 Program Review

---

**Service ops position:** We are 11 days from DVT build and service operations is not ready to support a September beta trial. Every one of my five teams raised a version of the same warning: the product is moving toward the field faster than the depot infrastructure, spares pool, and repair bench can catch up. That gap is the risk I'm owning in this review.

---

**Team signals:**

**Repair** flagged that no fault-code taxonomy, no repair runbook, and no repair cost ceiling exist for AMG-100 yet. At EVT yield of 78%, roughly 1-in-5 units is already returning to bench — and without standardized diagnostics, those become NFF (No Fault Found) dispositions, which is data destruction, not triage. The battery 8D at D6 is especially concerning: if cell swaps become a depot repair action, we need a test spec and a parts kanban *before* beta, not after a field failure teaches us the hard way.

**Fulfillment** cannot commit a beta ship date. Single-source eMMC means I cannot substitute without violating a quality gate, and 78% yield means roughly 1-in-5 units fails kitting verification. Those two facts together mean fulfillment throughput is severely degraded before we've even kitted a single beta box.

**Inventory** flagged the TS-90R cannibalization risk: if we size the AMG-100 beta spares pool wrong, we raid the refurb pool supporting *existing* paying MP customers (strategy.md: >99.5% fleet uptime is the value prop). That's a customer-facing SLA risk, not just an inventory inconvenience. The eMMC single-source also creates an E&O cliff — overbuy now and we're holding aging components against a $6.8M total budget with zero revenue offset yet.

**Deployment Support** named the hardest constraint plainly: alpha uptime is 99.1% against a 99.5% target (strategy.md). We cannot launch a beta into restaurant venues — harsh environment, 24/7 duty cycle — without closing that 40-basis-point gap and without staged spares confirmed. "Installed" without depot sign-off is an open work order, not a deployment.

**Logistics** raised the most time-sensitive single issue: ISS-014 antenna rework parts are ETA 06/16 with a 3-day buffer to the 06/22 build. Any customs hold or DG paperwork exception on lithium-containing assemblies (49 CFR / IATA DG) kills the build date. Per Logistics, we need customs clearance confirmation *today*, not broker assurance.

**Disagreement to name:** Repair and Inventory differ slightly on timing — Repair wants runbook and cost ceiling before DVT build starts; Inventory wants a small spares pre-build funded now off DVT yield data. Both are right; they're solving different weeks. I'm sequencing Repair's ask first (runbook is a prerequisite to knowing what spare parts to stock).

---

**Numbers:**
- EVT yield: 78% (target 88% DVT, 95% MP) — 10-point gap unresolved
- Alpha uptime: 99.1% vs. 99.5% target — 40 bps short
- TS-90R refurb margin: 22% (products.md) — thin enough that pool cannibalization materially hurts contribution
- Antenna parts buffer: 3 days — not a buffer, it's a single point of failure
- Total budget: $6.8M; program budget $2.0M; $872K spent, $111.6K contingency remaining

---

**Recommendation:**

Three actions before DVT build on 06/22:

1. **Confirm ISS-014 antenna parts customs clearance today** (Logistics owns, escalate to air courier with dedicated DG handling — per Logistics, $8–15K expedite is justified against a $329/42% margin product on a hard build date).

2. **Issue AMG-100 repair intake criteria and fault-code taxonomy before 06/22** (Repair owns; NPI-PM gates this; without it, every DVT return is undiagnosable noise, not yield data).

3. **Set beta entry gate: depot readiness sign-off required, not just DVT pass** (Deployment Support owns criteria; Inventory sizes spares pre-build off DVT yield data immediately after build). Beta does not ship until uptime gap closes to ≥99.5% and staged spares are confirmed — per strategy.md, that uptime number is the core customer promise.

No action here compromises a quality gate. The antenna expedite protects the build schedule so DVT testing can happen on time. The repair taxonomy *enables* yield data quality. The depot gate *adds* rigor, it doesn't remove it.

**Brain references:** products.md (AMG100 DVT, TS90R active), strategy.md (>99.5% fleet uptime, harsh environment ICP), budget.md ($6.8M total, $2.0M program), laws.md (49 CFR / IATA DG lithium battery transport, 19 U.S.C. customs)