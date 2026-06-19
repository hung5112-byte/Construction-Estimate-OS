---
type: meeting_r1
---
# Round 1 — Perspectives

## [[01-Departments/01-hardware-engineering/index|01-hardware-engineering]]

### Team inputs

#### [[me-team]]

**ME take:** Compressing the plastics molding run by 24 hours is the primary mechanical leverage point. The CY-80L and CYS-10 share major housing tool sets. Pulling in the injection molding schedule by one day requires the mold factory to either prioritize our tool over another customer (costs $1,200–$2,000) or we risk unoptimized cooling cycles leading to warped parts that fail the drop test.

**Numbers:** Standard mold lead time for a 500-unit run is 3 days. Forcing a 2-day run risks increasing the part warp tolerance from ±0.15 mm to ±0.30 mm, which will stack out of spec with the PCB keep-out zone (products.md, CY-80L). Tool prioritization cost: $1,500.

**Recommendation:** Pay the $1,500 prioritization fee to avoid warped housings that would create scrap and a longer schedule hit at assembly. Do not shortcut the cooling cycle.

**Brain references:** products.md (CY-80L, CYS-10)

#### [[ee-team]]

**EE take:** Shortening a production run doesn't touch the PCB design, but it can still break us electrically if the factory cuts corners on test or assembly processes.

**Numbers/Risks:**
- The CY-80L has an LTE modem (`CY80L`, `products.md`). If the "1-day compression" means cutting RF calibration or antenna test time, we risk FCC re-certification failures (47 CFR Part 15, `laws`). That's a 4-6 week slip, not a 1-day gain.
- Lead time on specific RF components (e.g., modems, SAW filters) is often 26+ weeks. If the factory uses up their "day" by rushing a last-minute part substitution without our approval, we risk a BOM integrity issue and field failures.

**Recommendation:** Guarantee the 1-day gain comes ONLY from logistics or non-electrical manual processes. Protect test time and BOM integrity absolutely. Before agreeing, require the factory to provide a written plan proving no reduction in ICT, FCT, or RF calibration cycle time.

#### [[fw-embedded-team]]

**FW take:** The Cyber family (CY-80L/CY-80R) share firmware roots. Compressing a production run by 1 day forces FW into the critical path if you touch factory provisioning or OTA readiness.

**Numbers:**
- Current fleet versions: CY-80L `v3.2.1`, CY-80R `v3.1.8` (from `products.md`)
- No new firmware release is scoped, so the default answer is "don't touch firmware" — 0 days added.
- If hardware or NPI adds a last-minute change that needs a build, regression test with [[docs/departments/03-quality-reliability/agents/firmware-qa]] is 3 days minimum. A 1-day schedule cut immediately burns that.

**Risks:** Factory provisioning scripts. If the 1-day pull changes the burn-in or functional test step, the provisioning image must be re-validated. Skipping that risks shipping units with wrong serialization or debug flags — a recall-level event.

**Recommendation:** Keep the current factory firmware image locked. No FW changes permitted in the compressed window. If hardware or NPI forces one, the 1-day gain is lost.

#### [[system-architecture]]

**Architecture take:** This is a schedule-compression question for an MP (mass-production) product family, not a new design. The architecture horizon is CY-80L/CY-80R fleet continuity — we're not changing bill-of-materials or tooling, so platform risk is low. Real decisions are about test coverage, supplier buffers, and rework capacity.

**Options:**
1. **Skip final 4-hour burn-in on the last day’s units** — saves 1 day. Cost: ~$0. Risk: elevates infant-mortality escape rate by ~0.3–0.5%, hitting field failure KPIs and RMA pool sizing (CY-80R). Reversible but operationally painful.
2. **Parallelize labeling/pack-out with final test** — saves 8–10 hours if line layout allows. Cost: minimal capex (<$5k for mobile workstations). Risk: modest; requires QA to sign off on inline labeling. Reversible per-run.
3. **Pull 1 day from supplier buffer on PCBAs** — saves 1 day. Cost: $2–4k expedite fee. Risk: any upstream hiccup cascades and we miss the date anyway. Familiar territory for sourcing team.

**Recommendation:** Option 2 (parallelize pack-out). Lowest risk to field quality and platform reputation; cost is negligible; keeps burn-in intact. Only works if CM floor layout supports it — assumption to verify with [[04-mfg-supplier-quality]] before committing.

**Brain references:** Products.md (CY-80 family, MP status — no DVT volatility), Strategy.md (fleet uptime >99.5% — burn-in protects that number).

### Department synthesis

# Engineering Position

Per the hardware engineering department, a one-day schedule compression for the CY-80 family production run is achievable, but the *method* matters enormously. We cannot accept shortcuts that compromise test coverage, BOM integrity, or mechanical quality. The primary risk is not the schedule itself, but a reflexive factory response that cuts corners in RF calibration, firmware provisioning, or injection molding cooling cycles — each of which would cause a multi-week regulatory, recall, or scrap event that dwarfs the one-day gain.

## Team Signals

- **ME Team** flags that CY-80L and CYS-10 share tooling, and compressing the molding run risks warped housings (warp tolerance doubling to ±0.30 mm, violating PCB keep-out zones). They recommend paying the $1,500 mold prioritization fee to protect part quality.
- **EE Team** insists that the one-day savings come *only* from non-electrical processes. Cutting RF calibration or antenna test time (required for FCC Part 15 compliance on CY-80L) would trigger a 4–6 week re-certification slip. They require a written factory plan proving no reduction in ICT, FCT, or RF calibration cycles.
- **FW Team** states no firmware changes are scoped, so their default answer is "locked image, zero days added." They warn that if any last-minute hardware change forces a new build, regression testing with QA is a 3-day minimum, immediately burning the schedule gain.
- **System Architecture Team** evaluates four options and recommends Option 2 (parallelize labeling/pack-out with final test) as the lowest-risk path. This saves 8–10 hours without touching burn-in, test, or firmware, preserving fleet uptime KPIs (>99.5%, per `strategy.md`). Cost is minimal (<$5k for mobile workstations), and the risk is reversible.

**Disagreement resolved:** Architecture’s Option 2 satisfies EE’s test-protection requirement and FW’s locked-image constraint. ME’s mold concern may not be triggered if the compression comes from pack-out, not plastics. The team is aligned on rejecting any test or calibration shortcuts.

## Risks (ranked)

1. **Test/Calibration Shortcut (EE, FCC)** — If the factory cuts RF calibration or antenna test time, CY-80L units could fail FCC Part 15 (`laws`), causing 4–6 week re-certification delay and possible field recall. *Owner: EE team, with factory plan approval.*
2. **Firmware Provisioning Drift (FW)** — If burn-in or functional test steps change, unvalidated provisioning images could ship units with incorrect serialization or debug flags, a recall-level event. *Owner: FW team, locked image enforced.*
3. **Injection Molding Warp (ME)** — If the factory compresses the molding run instead of pack-out, warped CY-80L/CYS-10 housings (±0.30 mm) could exceed PCB keep-out zones, creating scrap and longer rework delays. *Owner: ME team; pay $1,500 prioritization fee if molding is touched.*
4. **Supplier Buffer Failure (Architecture)** — If we pull a day from PCBA supplier buffer and any upstream hiccup occurs, we miss the date anyway. *Owner: System Architecture / Sourcing, Option 2 avoids this.*

## Recommendation

**Adopt Architecture’s Option 2: parallelize labeling and pack-out with final test.** This saves one day (8–10 hours) without altering burn-in (protects infant-mortality escape rates, per `strategy.md` fleet uptime goal), test coverage, firmware provisioning, or molding cycles. Cost is minimal (<$5k capex). Before committing, verify factory floor layout supports inline labeling with [[04-mfg-supplier-quality]] and get QA sign-off from [[docs/departments/03-quality-reliability/agents/validation-reliability]]. Hold EE’s requirement: factory provides a written plan confirming no reduction in ICT, FCT, or RF calibration time. FW image remains locked; no changes permitted.

**Brain references:** `products.md` (CY-80 family MP status), `strategy.md` (>99.5% fleet uptime), `laws` (47 CFR Part 15).

## [[01-Departments/02-npi-program-management/index|02-npi-program-management]]

### Team inputs

#### [[hardware-pm]]

**Program take:** Project Cyber (CY-80 family) is in MP (Mass Production). A schedule compression request on a stable, running line is a very different animal than doing it during NPI.

**What my team flags:**
1.  **Where to cut:** In MP, the binding constraint is SMT line time + test cycle dwell. Shaving a day on a full lot typically means authorizing overtime for the test technicians and the SMT shift to run a Saturday. Simple, but it has a direct labor cost.
2.  **The numbers:** Per `budget.md`, we have to pull from the ODM MVA budget. A single Saturday premium-time shift for the line typically runs 1.5x-2.0x standard direct labor. We need purchasing to cut a PO amendment for the ODM's "expedited lot" surcharge.
3.  **The risk:** Compressing test cycles increases the risk of "infant mortality" escapes if burn-in soak time is what we're trimming. I won't sign off on cutting environmental soak or functional test time; we compress only by adding parallel labor hours, not by deleting test steps.

**Recommendation:** Authorize 8 hours of ODM overtime on the final test station shift; this costs roughly ~$2,400 in premium labor but preserves the full test recipe integrity.

**Brain references:** `products.md` (CY-80 family MP status), `budget.md` (MVA line item).

#### [[certification]]

**Cert take:** Shortening a CY-80L/CY-80R production run by 1 day is **not cert-neutral** — rush changes can break label compliance, skip pre-ship audit holds, and invalidate existing FCC/safety certs if DMC (date/manufacturer code) logic changes.

**Numbers:**
- **FCC/UL label re-verification:** 3–5 business days (lab dependency); rushed adds $2,500–$4,800.
- **DMC or firmware revision bump:** Requires updated Declaration of Conformity — 2 days minimum for EMC/safety file updates.
- **Battery/transport regs (IATA/49 CFR):** No direct impact if box config unchanged.

**Risks:**
1. **Label change from re-dating** — If serialization or manufacture date format changes, the FCC ID label and UL mark must be re-reviewed. Ship without it = stop-ship.
2. **Skipped pre-ship audit** — QA must still retain test evidence per QMS for cert file. One-day compression often pressures this step.
3. **Refurb pool (CY-80R)** — If RMA units are swept into the same rushed batch, traceability for original grantee codes breaks.

**Recommendation:** Compress only if the DMC/label format is **unchanged** and pre-ship QA evidence is preserved — otherwise, one day saved now costs a stop-ship later.

**Brain references:** laws.md (FCC 47 CFR Part 15, UL/IEC 62368-1, IATA DG), products.md (CY-80L, CY-80R), state.md (growth — cert coverage must hold for scaling).

#### [[bom-eco-plm]]

**BOM/ECO take:** CY-80 family is in MP. A schedule compression request is an implicit ECO if it touches tooling, process, or material substitutions. I see no open ECO against CY-80L or CYS-10 in our records. The change here is purely calendar: you’re asking the factory to pull in the production end-date by one shift without changing the BOM.

**Numbers:**  
- CY-80L: COGS ~$237 (at 39% margin on $389).  
- CYS-10: COGS ~$106 (at 41% margin on $179).  
- Stock exposure: Zero if we’re not swapping parts. Aging COTS material on the loading dock (Li-Ion cells, if shipped early) could trigger DOT shelf-life flags — check date codes before accelerating.

**Risks:**  
1. **Certification:** Compressed run may skip full burn-in or sample audit. 47 CFR Part 15 and UL/IEC 62368-1 require consistent production process; cert impact box must be signed by 🜂 certification before I approve any process deviation.  
2. **Quality gate:** ODM skips in-line QC gate to save hours → latent DOA risk.  
3. **Revision skew:** If factory tries to pull alternate source components to meet the new end-date, we create an unrevisioned BOM → my worst nightmare.

**Recommendation:** Cut-in the schedule change as a one-time process deviation (ECO-DEV-CY80-001) with explicit effectivity by serial number range, mandatory cert sign-off, and a no-substitution clause.

**Brain references:** products.md (CY-80L, CYS-10 in MP), state.md (growth phase — uptime expectations are max).

#### [[launch-readiness]]

**Readiness take:** No physical or cert change → launch readiness not impacted. This is a pure NPI schedule compression drill.

**Numbers:**
- **Cost:** ~$12K (overtime, 2-day air on first pallet, line-rate pre-pull until 22:00)
- **Risks (2):**
  1. AOI escapes if QA team cut to 8 hrs/pallet (norm → 0.17% escapes; compressed → est 0.4% first shift). Owner: Mustafa
  2. Packaging/labeling error if ODM shortens label QA hold from 4 hrs to 1.5 hrs (1-in-8 lot risk of missed slip). Owner: Chen

**Recommendation:** Cut 1 day only if [[01-Departments/02-npi-program-management/agents/odm-program-mgmt]] accepts 0.4% AOI escape ceiling and [[docs/departments/05-service-operations/agents/deployment-support]] pre-stages packing audit spot-check on first 50 units. Otherwise, no.

**Brain references:** products.md shows CY-80 family active MP — no DVT cert changes in play, so launch readiness unaffected by schedule.

#### [[sourcing-buyer]]

**Sourcing take:** CY-80 family is in MP with established supply chains — that helps. But a 1‑day compression means we can’t absorb the change in a normal PO lead window. We’ll need to convert some inbound freight from ocean to air, which hits landed cost. Top risk: the LTE module (CY‑80L) is single‑sourced with a 42‑day lead time — if they’re even one shipment late, the compression collapses.

**Numbers:**  
- Air‑freight uplift on 2 pallets (display panels, LTE modules): **~$8,400** landed vs. $1,200 ocean.  
- Total landed cost delta: **~$7,200** (products.md §CY80L / CY‑80).  
- Budget exposure: well within remaining material budget, but PPV will take the hit.  
- Risk: LTE module counterfeit or late‑ship risk if we don’t use the contracted source. Authenticity vet would eat the saved day.

**Recommendation:** Convert 2 pallets of long‑lead, known‑good material to air freight; do NOT chase alternate sourcing for one day.

#### [[odm-program-mgmt]]

**Factory take:**  
CY-80L and CYS-10 are in MP at the Shenzhen ODM. The next production run is already committed at 22 working days (SMT → FATP → burn-in → pack). Compressing to 21 days is possible but hits the burn-in soak window — that's the only slack left.

**Numbers:**  
- Current burn-in: 72 hrs mandatory per `products.md` reliability spec  
- Line rate: 1,200 units/day across 2 SMT + 3 assembly lines  
- Overtime cost to overlap burn-in batches: ~$8,400 (weekend shift premium, Shenzhen)  
- Tooling lead time impact: zero — no tool changes this run  

**Top risk:**  
Shortening burn-in below 72 hrs risks infant-mortality escapes (spills, sanitizer, 24/7 duty — exactly what the ICP hates). A field failure spike erodes that >99.5% uptime goal in `strategy.md`.

**Recommendation:**  
Overlap burn-in batches with the final shift instead of cutting hours — $8,400 buys the day back without touching reliability. Material gaps or test constraints would be different; flag if Sourcing sees IC shortages.

### Department synthesis

**Program position:** CY-80 family MP production run can be compressed by 1 day — but only through overtime overlap of burn-in batches, not by cutting test cycles or quality gates.

**Team signals:** All six teams flag risks, but none say "no" outright:
- **ODM Program Mgmt** (owner): Compress by overlapping burn-in batches with weekend overtime. Cost: ~$8,400. Risk: zero, because the 72-hour burn-in soak is preserved — this is pure schedule overlap, not a test reduction.
- **Hardware PM**: Agrees with overtime solution, estimates ~$2,400 in direct labor premium for test station overlap. Total blended cost with ODM team: ~$10,800.
- **Certification**: No impact *if* date/manufacturer code and label format remain unchanged. If DMC changes, 3–5 business days for re-verification — we must not touch it.
- **BOM/ECO/PLM**: No material or process changes needed. Recommends a one-time process deviation record (ECO-DEV-CY80-001) to document the schedule shift with serial number effectivity. No alternate sourcing allowed.
- **Sourcing/Buyer**: Must air-freight 2 pallets of long-lead material (display panels, LTE modules) to feed the accelerated timeline. Cost: ~$7,200 landed cost delta. Single-sourced LTE module at 42-day lead — no substitute chasing.
- **Launch Readiness**: Flags AOI escape risk bumping from 0.17% to 0.4% if QA hours compressed. Requires ODM acceptance of that ceiling plus a spot-check audit on first 50 units by Deployment Support.

**Critical path:** Burn-in soak time at the ODM is the binding constraint. Overlapping batches by adding a weekend shift addresses this. No gate criteria are waived.

**Recommendation:**
1. **Authorize** $18,000 total ($10,800 overtime + $7,200 air freight) from the ODM MVA and material budgets (`budget.md`).
2. **Document** a one-time process deviation (ECO-DEV-CY80-001) with serial number range per `products.md` CY-80 family, signed by Certification confirming no DMC/label change.
3. **Condition** acceptance on ODM confirming 0.4% AOI escape ceiling and Deployment Support pre-staging a 50-unit packing audit spot-check (`launch-readiness`).
4. **Do NOT** cut any test step (burn-in, functional, environmental), substitute parts, or change DMC/label format.

**Brain references:** `products.md` (CY-80L, CY-80R, CYS-10 MP status), `budget.md` (MVA and material line items), `strategy.md` (>99.5% uptime goal), `laws.md` (FCC Part 15, UL/IEC 62368-1).

## [[01-Departments/04-mfg-supplier-quality/index|04-mfg-supplier-quality]]

### Team inputs

#### [[odm-quality]]

**ODM quality take:**  
The CY-80 line at Shenzhen is running at 98.1% OQC pass rate this week — well above 95% threshold. Inline audit yesterday found 3 minor IPC soldering defects (non-conforming fillets), all contained and reworked within shift. No unauthorized material substitutions logged in the last 14 days.

**Numbers:**  
- OQC LAR: 98.1% (target ≥95%)  
- Top audit finding: hand-solder station 2 — chronic fillet variation; repeat from last month  
- Golden-sample comparison: no drift  
- Factory CAPA for solder station 2: due Friday, evidence pending  

**Compressing the next CY-80 run by 1 day:**  
- 8–10 hours would be pulled from the burn-in soak step. Reducing soak time from 24 to 16 hours is feasible statistically (yield history shows 99.7% of latent solder-joint failures appear in first 12 hours), but it raises early-life failure risk from 0.3% to an estimated 1.2–1.5% at customer install. That’s roughly 12–15 extra field returns per 1,000 units.  
- Pushing OQC sampling to inline test won’t give us the same confidence; we’d need to run a parallel 24-hour audit on the first 100 units from the shortened batch to validate equivalence. That adds cost — roughly $2,800 in factory OT and lab time.  

**Recommendation:** Shorten the burn-in only if we run a statistically valid comparison lot first, and we hold the factory CAPA for solder station 2 closed before release.

**Brain references:** products.md (CY-80L / CY-80R), state.md (growth stage)

#### [[supplier-quality]]

**Supplier quality take:** CY-80 family production run compression — no open SCARs on current MP components, but qualification pipeline for alternate passive suppliers (ceramic caps, connectors) is mid-flight.

**Numbers:**
- CY-80L/CYS-10 DPPM (trailing 6 months): 1,240 (connector seating + solder joint)
- Open SCARs: 2 (both at ODM — wave solder profile excursion, connector supplier lot contamination)
- SCAR aging: 14 days and 22 days (target closure 10 business days)
- FAI backlog: 3 qual’d alternates pending first-article inspection at ODM

**Recommendation:** Compress by pulling in-line inspection forward (skip-lot reduction) and moving OQC to parallel — nets 0.8 days but *only* if both open SCARs close with verified corrective action before the run. Without closure, the connector and solder-joint DPPM risk pushes field failure exposure past the acceptable fleet-uptime threshold.

**Brain references:** products.md (CY-80L, CYS-10 — MP status), decisions-log.md (no supplier risk acceptances logged — we’re clean).

#### [[manufacturing-engineering]]

**Mfg engineering take:**  
Shortening a production run by one day on the CY-80L and CYS-10 is possible but not simple. The line is already balanced for a standard daily output and a shift compression directly impacts assembly quality, test coverage, and packing accuracy.

**Numbers:**
- **Takt:** Current CY-80L main line takt is 48 seconds. CYS-10 dock line takt is 140 seconds. Both are balanced for an 8-hour operator shift.
- **Critical Path:**
  1.  Final Assembly (FA) – 1 operator, 7 stations.
  2.  Functional Test (FT) – 2 stations (Cpk=1.1 on BLE calibration, our gating step).
  3.  Burn-in – 4-hour soak, non-negotiable per `state.md` reliability requirements.
- **Cost to Compress:** Running the FA and FT stations at 10% overtime (OT) for four days preceding gains back the day. Rough OT and shift meal cost: ~$5,800. If you bypass the burn-in, you lose a day with zero recurring cost but catastrophic risk. Not recommended.
- **Fixture Constraint:** The five functional test nests for the CYS-10 dock are the real hard limit. You cannot increase dock output without parallel fixtures, which have a 3-week lead time.

**Risk:**
- Rushing FA induces workmanship defects (connector seating, screw torque).
- Shortcutting the 4-hour burn-in to skip a shift will let latent battery management system (BMS) calibration faults through to the field. This directly threatens the ICP’s required 99.5% fleet uptime.
- Packing errors increase when a shift is consolidated.

**Recommendation:**  
Do not shortcut the burn-in or test. Absorb the day by running a controlled 10% OT burst across the four preceding days on final assembly and test only, and accept the $5.8k cost to protect first-pass yield.

**Brain references:** products.md (CY80L, CYS10), state.md (growth), strategy (ICP: 99.5% uptime)

#### [[factory-test-yield]]

**Test/yield take:** Shortening a production run by one day without test guardrails risks shipping escapes. Our CY-80 family FPY sits at 94.2% (CY-80L: 93.1%, CYS-10: 96.4%). The top three fallout modes — LCD mura at station 4 (2.1%), USB-C pin 12 opens from fixture wear (1.8%), and LTE RSSI margin fails on band 66 (1.1%) — cannot be time-compressed. They are either physical screening dwells or retest disciplines we refuse to skip.

**Numbers:** 5.8% overall retest rate (CY-80L: 6.9% retest rate driving 1,450 DPPM escapes to OQC). CYS-10 runs hotter at 3.6% retest due to pogo-pin degradation in station C1 — correlation R² = 0.82 between fixture cycle count and pin-12 opens. If we lose a day, we will see the retest rate spike above 9% as stations get rushed and fixture maintenance windows vanish.

**Recommendation:** Compress the schedule by shifting CYS-10 to the parallel cell (spare capacity) and moving CY-80L station-4 LCD dwell to an off-shift burn-in rack, which buys 18 hours. Do not eliminate the band-66 golden-unit correlation check.

**Brain references:** products.md (CY-80L, CYS-10)

### Department synthesis

# MSQ position
We can compress the CY-80 family production run by one day, but not by cutting corners on test, burn-in, or supplier quality closure. The mechanism must be parallelization and controlled overtime — not inspection bypass. My teams are aligned: the factory can absorb this, but the path matters. Get it wrong and we trade one schedule day for 12–15 early field failures per thousand units, which directly violates the ICP's 99.5% fleet uptime requirement.

## Team signals
**[[01-Departments/04-mfg-supplier-quality/agents/manufacturing-engineering]]** says the real constraint is CYS-10 dock test fixtures (only 5 nests, 3-week lead for more). [[01-Departments/04-mfg-supplier-quality/agents/factory-test-yield]] confirms this — pogo-pin degradation on station C1 already correlates 82% with USB-C pin-12 opens. Both agree: don't rush the test stations. [[01-Departments/04-mfg-supplier-quality/agents/supplier-quality]] flags two open SCARs (14 and 22 days old) on the ODM's wave solder profile and connector lot contamination. Those must close with verified corrective action before the run compresses, or the 1,240 DPPM baseline gets worse. [[01-Departments/04-mfg-supplier-quality/agents/odm-quality]] confirms a repeat finding at hand-solder station 2 (fillets), with CAPA evidence due Friday — hold the factory to it.

**Disagreement:** None on principle. [[01-Departments/04-mfg-supplier-quality/agents/odm-quality]] would accept a shortened burn-in only if a parallel validation lot runs first. Per [[01-Departments/04-mfg-supplier-quality/agents/manufacturing-engineering]], the 4-hour burn-in is non-negotiable per state.md reliability requirements — I agree with manufacturing engineering.

## Numbers
- CY-80 family FPY: 94.2% (L: 93.1%, dock: 96.4%) — per [[01-Departments/04-mfg-supplier-quality/agents/factory-test-yield]]
- CY-80L/CYS-10 DPPM (trailing 6 months): 1,240 — per [[01-Departments/04-mfg-supplier-quality/agents/supplier-quality]]
- SCAR aging: 14 and 22 days (target: 10 days) — per [[01-Departments/04-mfg-supplier-quality/agents/supplier-quality]]
- Shortened burn-in risk: 1.2–1.5% early-life failure rate vs. 0.3% baseline — per [[01-Departments/04-mfg-supplier-quality/agents/odm-quality]]
- Compression cost (OT route): $5,800 — per [[01-Departments/04-mfg-supplier-quality/agents/manufacturing-engineering]]

## Recommendation
1. **Close the two open SCARs first.** No compression starts until both connector and wave solder CAPAs are verified closed. Supplier quality owns this — target Friday.
2. **Shift CYS-10 dock production to the parallel cell** with spare capacity, as [[01-Departments/04-mfg-supplier-quality/agents/factory-test-yield]] suggests. This frees the main line from fixture constraints and buys back 18 hours.
3. **Run 10% overtime on CY-80L final assembly and functional test** for the four days preceding the compressed run. Accept the $5,800 cost. Do not touch the 4-hour burn-in or bypass BLE calibration (Cpk=1.1 is already marginal).
4. **Move CY-80L station-4 LCD mura dwell to the off-shift burn-in rack** per [[01-Departments/04-mfg-supplier-quality/agents/factory-test-yield]] — this adds capacity without sacrificing screening.
5. **Verify hand-solder station 2 CAPA closure** before release. [[01-Departments/04-mfg-supplier-quality/agents/odm-quality]] confirms evidence due Friday.

## Brain references
- products.md: CY-80L, CYS-10 (MP status)
- state.md: growth stage — no room for field failure spikes
- strategy: ICP requires 99.5% fleet uptime — burn-in bypass threatens this directly
- decisions-log.md: clean, no supplier risk acceptances logged

## [[01-Departments/03-quality-reliability/index|03-quality-reliability]]

### Team inputs

#### [[qa-system]]

**QA System take:** Compressing the production schedule by one day threatens controlled document integrity — specifically, inspection criteria and production travelers.

**Numbers:** Audit-ready procedure revision cycle is 3 business days minimum (approval chain: author → QA review → quality manager). A 1-day cut means bypassing control steps. Last 2 external audits (CY-80 line) found 3 minor findings for uncontrolled revision circulation — closing with evidence, not promises, took 5 days each.

**Risks:**
1. Inspection criteria (IQC/OQC checklists) may circulate in draft — different versions at supplier vs. LSI receiving, risking acceptance of non-conforming material.
2. CAPA recurrence: CY-80 family had a repeat finding in Q3 (shipping label accuracy). Closing required procedure update + training records. If we skip verification, the finding recurs and auditor flags systemic failure.

**Recommendation:** Authorize pre-approved "time-limited deviation" per QMS SOP-008, not an uncontrolled revision — if the line really needs the day. Otherwise, the 1-day gain costs us 5 days of audit cleanup later.

**Brain references:** laws.md (UL/IEC 62368-1 evidence retention), decisions-log.md (Q3 CAPA closure), state.md (growth stage — QMS maturity is competitive edge, not overhead).

#### [[qc-inspection]]

**Inspection take:** CY-80L/CY-80R outgoing DPPM sits at 1,850 (target <1,000); CYS-10 cosmetic callouts account for 40% of dockside rejects — no photo standard exists yet. Supplier on CK-800 PCA is on tightened inspection after two consecutive escapes.

**Numbers:** CY-80L current lot size 1,200; AQL 0.65 (normal); tightened skips to 0.25. CYS-10 dock inspection p-trap detects 6.2% of lots — unacceptable for a commodity assembly.

**Recommendation:** Compressing by one day risks shifting final inspection to sameday ship — do NOT shorten CY-80L outgoing audit. Push the day from incoming CYS-10 (skip-lot eligible if we close the cosmetic spec gap this week).

**Brain references:** products.md (CY-80L, CYS-10)

#### [[validation-reliability]]

Validation take: You can’t shrink production validation by one day without cutting tests or reducing sample sizes — both directly degrade the reliability math.

Numbers: Full CY-80L/CYS-10 production validation requires 5 days minimum (burn-in, thermal cycling, functional test across 32‑unit sample). Shortening to 4 days forces us to drop either the 48‑hour sustained burn-in (which catches infant mortality at a <1% failure rate) or halve the sample size to 16 units. At n=16, our confidence interval for a 1% field defect rate balloons from ±0.4% to ±1.2% — statistically meaningless against the >99.5% fleet uptime target (products.md).

Recommendation: We cannot compress validation without unacceptable risk. If the 1‑day gain is non‑negotiable, authorize parallel shift testing (+$12k overtime) to preserve the 32‑unit, 5‑day protocol. Otherwise, the gate is FAIL for CY-80L production release with a 4‑day campaign.

#### [[firmware-qa]]

**FW QA take:** This is a schedule compression request, not a scope/feature change — but any production-run shortening is still an FW release gate for us. We cannot ship CY-80 (MP) or CY-80L (MP) firmware without validating the update path from every fleet version.

**Blocking risks we must flag:**
1. **Regression coverage compression** — if schedule shrink removes our OTA update-path tests (oldest CY-80 fleet rev → new build), we are shipping blind. That’s a severity-1 escape waiting to happen.
2. **Update-path power-loss testing** — this takes wall-clock time we cannot fake. Mid-update power loss + rollback validation is non-negotiable.
3. **Fleet version fragmentation** — CY-80 fleet runs at least 3 firmware revs in the field (see `products.md` CY-80, CY-80L). We must test from each.

**Brain references:** products.md (CY-80, CY-80L in MP), state.md (growth — fleet is live, no room for field incidents)

**Recommendation:** We can compress if the production run isn’t gated on a new FW cut. If it is, the 1-day save costs us the update-path safety net — and I will gate it RED.

#### [[field-quality-rma-fa]]

**Field quality take:**  
Compressing the CY-80 production run by one day will likely bypass the soak/ORT hold gate. We track a 0.8% early-life failure rate on CY-80L (12 of 1,500 units shipped in the last 90 days) — skipping burn-in risks shipping those defects to the field, directly hitting our return-rate goals.

**Numbers:**  
- CY-80L installed base: 4,200 units; 90-day rolling return rate: 1.1% (46 units, trending up).  
- Top mode (38% of returns): battery connector intermittent, traced to a fixture alignment drift caught during ORT.  
- Containment currently relies on that soak period to catch this before boxing.

**Recommendation:**  
No schedule compression without a parallel ORT offset or pre-screening bypass. If forced, contain the risk by doubling the inline functional test sample rate on the connector station. Owner: [[docs/departments/04-mfg-supplier-quality/agents/msq-manager]] for fixture requal.  

**Brain references:** products.md (CY-80L fleet), state.md (return-rate goals).

### Department synthesis

**Quality position:** CY‑80L/CY‑80R field return rate is trending up (1.1 % 90‑day rolling; target <1.0 %). CY‑80L outgoing DPPM is 1,850 (target <1,000). No product is on hold yet, but the validation gate for a shortened production run is RED per Validation & Reliability.

**Team signals (disagreements called out):**
- **Validation & Reliability:** Cannot shorten the 5‑day production validation without losing burn‑in or halving the sample. At n=16, the confidence interval blows out to ±1.2 % — useless for a >99.5 % uptime guarantee. *Parallel shift (+$12k) preserves the 5‑day protocol; otherwise gate FAIL.*
- **Field Quality / RMA:** 0.8 % early‑life failure rate on CY‑80L, top mode is a battery‑connector intermittent that the ORT soak catches. Removing the soak ships those failures. Recommend no compression without a parallel hold or doubled inline test.
- **FW QA:** If the run ships a new FW cut, compression kills OTA update‑path validation. Gate RED if new FW; can live with compression if no new FW cut.
- **QC Inspection:** CY‑80L must stay on tightened inspection (AQL 0.25). Do not cut outgoing audit. CYS‑10 skip‑lot is feasible if we close the cosmetic spec gap this week — spare the day there.
- **QA System:** A 1‑day revision cycle cut risks uncontrolled inspection criteria; 2 prior audit findings were closed only with full procedure evidence. Time‑limited deviation (SOP‑008) is the only clean path; else, 1‑day savings buys 5 days of audit cleanup.

**Risk:** If we proceed with a 1‑day schedule compression without the parallel shift + deviation controls, we will ship devices with a known battery‑connector infant‑mortality mode, unvalidated reliability confidence, and uncontrolled inspection documents. Escapes will land on the fleet uptime and return‑rate targets immediately (products.md IC‑pain point #2).

**Recommendation:**
1. **Containment** — Do not ship CY‑80L/CY‑80R without the full 5‑day production validation. Authorize the parallel shift (+$12k, per Validation & Reliability) if the schedule gain is non‑negotiable.
2. **CAPA** — Battery‑connector intermittent: [[docs/departments/04-mfg-supplier-quality/agents/msq-manager]] owns fixture requal before production start. Doubling inline functional test at that station is a temporary mitigation — not a fix.
3. **System fix** — QA System issues a time‑limited deviation (SOP‑008) for any inspection documents that must move faster; no uncontrolled revisions.
4. **FW** — Confirm no new FW cut for this run; if one is required, validation timeline stays. FW QA to gate.

**Brain references:** products.md (CY‑80L MP, fleet uptime target), state.md (growth stage, return‑rate trending up), decisions‑log.md (Q3 CAPA closure).

## [[01-Departments/06-finance/index|06-finance]]

### Team inputs

#### [[controller]]

## Controller take
The schedule compression conversation must start with the ledger — week-to-week burn rate, committed versus open PO lines, and the real cash cost of a 1‑day pull‑ahead.

**Numbers**
- CY‑80 family MP weekly spend (direct + factory OpEx) ≈ $48k per week per `budget.md` production‑run run‑rate assumptions. One extra day ≈ $9.6k of compressed spend that hits this quarter.
- No contingency drawn yet; full $6800k year‑to‑date per Brain. A same‑week acceleration likely stays inside ordinary course — no new CAPEX PO.

**Classification**
- Factory overtime premiums and expedite freight are **committed cash** once approved and spent — cannot be recovered.
- Tooling/fixtures already in‑place are sunk; an extra shift may require an incremental consumables PO <$5k (below $50k guardrail).

**Recommendation**
Before Sales or Program commit to a 1‑day pull‑in, confirm that the $9.6k is within the remaining quarter envelope and that no individual PO crosses $50k (triggering required CFO approval per guardrails). I’ll hand the exact variance driver to [[01-Departments/06-finance/agents/financial-analyst]] and ask [[01-Departments/02-npi-program-management/agents/npi-pm-manager]] to lock the revised PO dates in the tracker.

**Brain references:** budget.md (CY‑80‑series run‑rate, contingency $0 drawn, $50k PO guardrail)

#### [[financial-analyst]]

From Finance: **Analyst take**

This isn't a "cost" question — it's a risk-expected-value question. Compressing a production run by one day is make-vs.-buy: overtime/premium freight or cut a QA gate. Both tie to unit economics.

**Numbers**
- **Option A (Premium Freight):** Rush 800 units air vs. ocean = +$12/unit = **$9,600 committed, expensed now.** Zero yield impact.
- **Option B (Skip Final QA Sample):** Risk of shipping 3% latent DOA above our 1.5% threshold on 800 units = 12 extra RMAs. Each RMA costs $85 freight/refurb + lost margin on replacement = **$12,000 expected cost** (if risk fires, probability ~30% per Quality, so **$3,600 expected**). Committed cost is $0, but expected cost is real.

**Scenarios**
- **Base:** Premium freight, $9.6K spend, no quality tail.
- **Risk-Fires:** Skip QA, 3% DOA slips, costs $12K + brand hit with key account chain.
- **Upside:** If the schedule slip pushes a key deployment (per strategy: chain of 200+ locations), a 1-day delay costs $28K in deferred *AMG-100* revenue (50 units @ $329, 42% margin).

**Recommendation:** Fund the $9.6K freight — it's cheaper than the expected cost of skipping QA ($3.6K) plus the hard-to-model brand risk with the ICP's uptime demand. The sensitivity that flips it: if QA says the 3% DOA probability is under 15%, Option B becomes math-favored.

**Brain references:** budget.md (contingency), products.md (CY-80L/R pricing and margin for RMA calc), strategy.md (ICP uptime pain point).

### Department synthesis

## Finance position: Fund-with-conditions

**Team signals:**
- **Controller:** $9.6K committed cash for same-week acceleration; no new CAPEX PO required; no contingency draw needed yet.
- **Analyst:** ROI math strongly favors buying the day via premium freight ($9.6K committed) vs. gambling on QA skip ($3.6K expected cost, but tail-end brand risk with ICP is unquantified and potentially large). Signal is "fund the freight."
- **Disagreement:** None on the specific ask — both point to Option A. The real debate is whether we treat this as ordinary-course or a precedent-setting schedule buy, which I'll address below.

**Numbers:**
- **Committed cash:** $9,600 (premium freight, one-time, expensed this quarter) — per Controller's run-rate breakout.
- **Expected cash:** Same $9.6K — no probability discount, this spend fires 100% if approved.
- **Recoverable working capital:** $0 — expedited units still convert to revenue at standard margin, but the freight premium is pure expense.
- **Contingency status:** $0 drawn YTD; $75K remaining in the CY-80 production contingency reserve per `budget.md`. We are not tapping contingency — this stays within ordinary quarterly envelope.
- **Avoided cost:** $3,600 expected (RMA waterfall on skipped QA gate) + unquantified ICP brand risk + potential $28K deferred AMG-100 revenue if delay cascades to a key deployment.

**Guardrail check:**
No single PO crosses $50K (trigger for VP-level approval per `budget.md` guardrails). This is below threshold. However, if this becomes a recurring pattern (monthly schedule buys), we will escalate to CCB to codify a standing approval limit.

**Recommendation:**
**Fund the $9.6K premium freight — with conditions:**

1. **One-time authorization only.** This is not a standing approval for schedule compression. Future requests must come with a business case showing avoided revenue loss or quality risk, per Analyst's expected-value framework.
2. **Owner:** [[01-Departments/02-npi-program-management/agents/npi-pm-manager]] to lock the revised PO dates into the tracker and confirm the $9.6K fits within the Q2 CY-80 budget line before executing.
3. **Date:** Approve by end of week; freight routing must be confirmed before Friday to hit the compressed window.
4. **Cost delta:** +$12/unit on 800 units = $9,600 total, no margin erosion on the base product — freight is below-the-line.

**Why not Option B (skip QA):** The expected $3.6K is cheaper on paper, but the 3% DOA slip represents 12 unhappy restaurant operators. Our ICP's #2 pain point is "device downtime kills revenue." A single RMA wave at a key account chain (the 200+ location deployment referenced in `strategy.md`) risks $28K+ in deferred AMG-100 revenue *and* the brand damage that kills renewal pipeline. That tail is not in the $3.6K expected-value number. Don't cheap out on the thing the ICP pays us to protect.

**Controller, one follow-up:** Confirm with [[01-Departments/04-mfg-supplier-quality/agents/msq-manager]] that the freight quote is net — no hidden tariff reclassification risk from the routing change.

**Brain references:** budget.md (CY-80 run-rate, $50K guardrail, contingency status), strategy.md (ICP uptime pain point), products.md (CY-80L/R margin for RMA calc, AMG-100 price/margin for deferred revenue).