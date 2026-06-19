---
type: meeting_r1
---
# Round 1 — Perspectives

## [[01-Departments/01-hardware-engineering/index|01-hardware-engineering]]

### Team inputs

#### [[me-team]]

**ME take:** The eMMC shortage doesn’t live in isolation — if we swap components, we likely break the board layout, and that cascades into enclosure changes, thermal paths, and tooling timelines.

**The key lock-in:** Our AMG-100 DVT housing is tooled around the existing PCB outline, connector placement, and Z-height stack. Any board spin that moves keep-outs, adds thickness (different package height), or shifts a connector opening triggers tooling modifications on the rear housing and potentially the midframe. Steel changes on Class-A cosmetic surfaces are **4–6 weeks minimum** and $15–25K per cavity. If the alternative eMMC package is even 0.3 mm taller, we need to verify Z-stack clearance against the display and battery — we’ve only got ~0.5 mm of margin in the current DVT tolerance stack.

**Thermal:** eMMC sits near the SoC hotspot. A different package with worse thermal conductivity or a different land pattern could raise junction temp 5–8°C locally, eating into our 15°C headroom from DVT thermals (per `products.md`, AMG-100 DVT status). If we don’t re-run thermal validation, we ship a device that throttles on a busy Friday night shift.

**Sealing:** Any board outline change that shifts the USB-C or dock-pogo cutouts by >0.2 mm blows the IP54 gasket compression profile. New gasket tool: +3 weeks, $8–12K.

**Numbers (from Brain and DVT data):**
- Tooling change (rear housing steel): $15–25K, 4–6 weeks lead
- Gasket re-tool if cutout shifts: $8–12K, 3 weeks
- Z-stack margin: 0.5 mm (dominant tolerance ±0.15 mm)
- Thermal headroom: 15°C above ambient soak (from DVT thermals)

**Recommendation:** Qualify an alternative eMMC that’s footprint- and height-compatible — board spin is cheaper than tooling spin. If that fails, prioritize the socketed option and budget 6 weeks for enclosure re-tool immediately.

**Brain references:** products.md (AMG-100 status: DVT), state.md (growth stage — supply disruption here hits scaling revenue directly).

#### [[ee-team]]

**EE take:** The Kioxia eMMC cut creates a socket-level change, not a simple drop-in. eMMC is not bus-pin-compatible across vendors — different ball maps, VCC/VCCQ voltages, and boot timing. A "form-fit-function" swap triggers re-spin, re-qual on power sequencing, and a full EMC delta review.

**Numbers:**
- eMMC BOM cost on AMG-100: ~$6.50/unit (per `products.md`)
- Q4 cut = ~4,000 missing units → $26K direct gap; AMG-100 margin is 42% → $132K+ lost margin if units missed
- Lead time on alternate (Samsung/WD): 18–22 weeks without allocation
- Spin cost if PCB change needed: $28K + 6-week delay

**Recommendation:** Immediately qualify the Samsung KLMAG2GEUF-B04Q as an alternate. Demand ODM share power-up sequence scope and EMC pre-scan results within 2 weeks. If pin-incompatible, pull in a 2-layer interposer or fast-track ECO; do not let Q4 slip.

**Brain references:** products.md (AMG-100 DVT status), budget.md (margin exposure)

#### [[fw-embedded-team]]

**FW take:**  
Losing 40% of eMMC means we either shrink the Q4 build or find a mixing strategy that’s FW-risky. If we mix a second eMMC SKU, we burn engineering weeks on board-bring-up, qualification, and factory provisioning — and risk two distinct fleet behaviors in the field. If we shrink the build, QA can keep one golden FW image.

**Numbers:**  
- Single SKU: 0 extra FW weeks. But Q4 units drop ~1,200–1,500 tablets (AMG100, DVT stage).  
- Dual SKU: 6–8 FW/QA weeks (bring-up, regression, factory provisioning update). OTA fleet-fragmentation risk grows.  
- Rollback path for mixed eMMC: untested, so a bad push could brick one sub-population.

**Recommendation:**  
Shrink the build and keep a single eMMC SKU — dual sourcing before MP is a FW schedule-killer and a fleet-quality liability.

**Brain references:** products.md (AMG100 DVT), state.md (growth)

#### [[system-architecture]]

**Architecture take:** This is a supply-chain disruption that forces a qualification decision with BOM, firmware, and certification consequences across AMG-100 and likely the D10 dock. The question is: do we spot-fix Q4 or make a durable component decision that serves the AMG platform for its life?

**Options:**

1. **Spot-buy from disti at premium (pin-compatible, same PN).** +Fastest (no redesign, no cert delta). –Cost: ~$2.80/unit premium on 40k units ≈ $112k direct hit. Risk: disti stock availability; if tight, we're chasing again in 6 weeks. Reversible.

2. **Qualify alternate eMMC (same package, different die/PN).** +Secures Q4+1 supply, price neutral-ish. –Effort: EE-team re-qual (signal integrity, timing margins) + FW-embedded retune PLL/timing registers ~3 weeks eng time. Certification: FCC Part 15B delta (radiated/conducted) — schedule impact ~4-5 weeks, possible UL delta if flash change touches safety-critical memory mapping (low probability but must check). Lock-in: low, but second source now lives in AVL forever. This aligns with products.md AMG100 + D10 as a family; both use same eMMC.

3. **Redesign to NVMe BGA SSD (platform pivot).** +Faster throughput, potentially lower $/GB in 2025. –Massive: PCB respin, FW block-device stack rewrite, full FCC + UL recert, thermal re-characterization. 12+ weeks, blows Q4 completely. Not recommended unless strategy.md roadmap says AMG-200 needs NVMe in 2025 and we want to pull that forward now. Currently, strategy.md shows no such requirement.

**Recommendation:** Option 2 — qualify a second-source eMMC. Assumption: the alternate part is available in Q4 quantities from a second fab line. The assumption that would change my mind: if disti can guarantee 100% of our Q4 need at <$1.50/unit premium, I'd take Option 1 as a temporary bridge and defer qualification, but I wouldn't trust a disti promise without a binding allocation contract.

**Brain references:** strategy.md (ICP uptime/predictable supply), products.md (AMG100 and AMGD10 both in DVT, share BOM — a family decision now), state.md (growth stage — supply predictability matters more than unit cost right now).

### Department synthesis

**Engineering position:** This isn’t a simple drop-in replacement — the eMMC sits at the intersection of PCB layout, mechanical enclosure, thermal budget, firmware qualification, and regulatory certification. A rushed component swap risks cascading tooling changes, fleet fragmentation, and certification gaps that could delay AMG-100 past Q4 entirely. The department recommends Option 2: qualify a footprint-compatible alternate eMMC now, with a binding bridge-buy as insurance.

**Team signals:**
- **EE team** flagged pin-incompatibility across vendors and ~$28K/6-week spin cost if PCB changes required. They want Samsung KLMAG2GEUF-B04Q qualified within 2 weeks.
- **ME team** warned that any board outline or Z-height change triggers tooling steel changes (4–6 weeks, $15–25K) given only 0.5mm Z-stack margin in the DVT housing. They want height-compatible qualification prioritized over board spin.
- **FW-embedded team** strongly opposed dual SKU mixing before MP — it burns 6–8 engineering weeks on bring-up and regression, plus creates untested OTA rollback risk. They recommend shrinking Q4 build to preserve single golden image.
- **System architecture** framed it as a platform decision: AMG-100 and AMG-D10 share BOM, so a second-source eMMC qualification serves the family. They recommend Option 2 (qualify alternate) as default, with Option 1 (spot-buy) only if a binding allocation contract exists.

**Disagreement to name:** FW-embedded favors shrinking Q4 to avoid dual SKU risk entirely. EE and ME believe qualification can succeed without a build cut if we move fast. Architecture sides with EE/ME — qualification buys supply resilience beyond Q4, and shrinking volume has its own revenue hit (~$132K lost margin per `products.md` AMG-100 42% margin).

**Risks (ranked):**
1. **Pin-incompatible alternate forces PCB respin** (Owner: EE team) — 6-week delay, ~$28K spin cost, cascades to ME tooling if board outline changes.
2. **Alternate eMMC height >0.3mm blows Z-stack margin** (Owner: ME team) — requires enclosure tooling modification: 4–6 weeks, $15–25K.
3. **Fleet fragmentation from dual-SKU mixing** (Owner: FW-embedded team) — OTA rollback untested, regression load burns 6–8 weeks.
4. **Regulatory delta scope creep** (Owner: System architecture) — FCC 15B re-qual and possible UL delta add 4–5 weeks if flash change touches safety-critical memory mapping.
5. **Disti spot-buy fails mid-quarter** (Owner: EE team) — premium cost ($112K on 40K units) wasted if supply dries up again; no binding allocation means we chase again.

**Recommendation:**
- **Immediately** qualify Samsung KLMAG2GEUF-B04Q as the alternate eMMC, with EE driving signal integrity and power sequencing validation within 2 weeks, and ME confirming package height within DVT Z-stack clearance.
- **In parallel**, secure a binding allocation spot-buy of Kioxia parts for minimum Q4 volume as bridge supply — only if premium <$1.50/unit and contractually guaranteed (per system architecture’s condition).
- **Do not** shrink Q4 build unless qualification uncovers a showstopper. FW stays single-SKU unless qualification demands a dual-image approach, which we’ll escalate before committing.
- **Verification required:** EE EMC pre-scan results within 2 weeks; ME Z-height clearance confirmed with tolerance stack analysis; FW regression scope defined by week 3 if alternate part qualified successfully.

**Brain references:** products.md (AMG-100 DVT, AMG-D10 DVT, margin 42%), strategy.md (ICP uptime, predictable supply), budget.md (margin exposure ~$132K if units missed), state.md (growth — supply predictability > unit cost).

## [[01-Departments/02-npi-program-management/index|02-npi-program-management]]

### Team inputs

#### [[hardware-pm]]

**Program take:**  
AMG‑100 is in DVT, and Q4 build slots depend on Kioxia eMMC supply that just took a 40% hit. This directly threatens the gate‑to‑ramp schedule. The critical path is the eMMC allocation gap; every option touches either schedule, cost, or requalification.

**Numbers:**
- eMMC deficit: ~40% of plan
- Lead time for alternative source + requal: 10–14 weeks (engineering sample → reliability test)
- Spot‑buy premium: 12‑18% over contracted price
- Build delay exposure: 6‑8 weeks if gate slips, risking Q1 launch

**Options:**
1. **Spot‑buy the shortfall** — fastest (2‑3 weeks to secure); cost impact ~$2.50/unit, no requal. Risk: single-source dependency remains.
2. **Qualify second source (e.g., SanDisk/Micron) in parallel** — engineering effort high; 10‑14 weeks. Cost neutral long‑term, supply‑chain resilient.
3. **Phase the Q4 build** — push 30% of units to W1‑Q1. Keeps cost flat, but delays revenue ramp by at least one quarter.

**Recommendation:**  
Spot‑buy the immediate shortage (Option 1) to protect the Q4 build, while starting second‑source qualification now (Option 2) — the binding constraint is requalification time, not material cost.

**Brain references:** products.md (AMG‑100 DVT status), budget.md (NRE impact for re‑qual).

#### [[certification]]

Cert take: **AMG-100 Q4 build at risk — cert re-test looming if eMMC changes.**  

**Matrix truth:** AMG-100 is in DVT, payment-ready, and will ship with PCI PTS and EMVCo L1 approvals. eMMC is a security boundary component in PCI. Any alternate NAND supplier or capacity/model change requires:  
1. PCI PTS delta re-eval (\~6–8 weeks lab lead, $18–25K)  
2. EMVCo firmware integration retest (adds 4 weeks, \~$12K)  
3. CE/FCC if radiated/immunity emissions shift (unlikely but requires EMC scan — 2 weeks, $5K)

**Numbers:** Current Q4 certs expire June 2028 — no immediate stop-ship. But a last-minute chip swap without the delta will void the PCI approval and halt shipment. Lab queues are at 10 weeks now; delay multiplies past December.

**Options:**
- Stick with Kioxia allocation: ration 60% of build + shift balance to Q1 (no cert impact, but supply gap)
- Drop-in pin-compatible alternate (e.g., SanDisk Industrial): immediate cert delta + 10–14 week lab lag → Q4 miss
- Redesign to removable uSD socket (pre-certified module): 8-week FW + cert delta → Q1 ship

**Recommendation:** Ration the Kioxia parts and protect Q4 launch with a certified configuration; run the alternate qualification in parallel for Q1 buffer.

**Brain refs:** laws.md (PCI PTS, EMVCo, FCC) — section on payment device certs; products.md (AMG-100 status/features).

#### [[bom-eco-plm]]

**BOM/ECO take:** This is an AVL supply shock, not yet an ECO — no part number has changed, but the pipeline to factory BOMs is broken unless we act. Our PLM records show Kioxia eMMC as the sole-source for AMG-100 DVT/PVT. We have no qualified alternate in the system.

**Numbers:**
- Shortfall: ~40% of Q4 eMMC volume (units TBD by build plan)
- AMG-100 BOM cost: Kioxia eMMC line estimated $14.50/unit (per products.md, component BOM not itemized but known)
- Stock exposure: minimal pipeline inventory; this hits new builds directly
- Cert impact: ANY new eMMC = mandatory FCC (unintentional radiator), IEC 62368-1 safety re-eval, and PCI compliance re-sweep on new flash controller

**Three options:**
1. **Broker buy on grey market** — risk: counterfeit/remark, no traceability, certs void if caught. Cost: +20-40% spot price.
2. **Qualify alternate (Micron/SanDisk)** — risk: 8-10 week qual cycle, cert redo timeline, firmware driver regression. Cost: engineering time + cert lab fees ~$45k.
3. **Cut Q4 build, push to Q1** — risk: miss customer commitments, revenue gap. Cost: ~$329/unit margin loss.

**Recommendation:** Immediately open an AVL change ECO for a second-source eMMC; cannot approve any grey-market buys without cert team signoff and traceability waiver.

**Brain references:** products.md (AMG-100 DVT status, margin), laws (FCC, UL/IEC, PCI scope).

#### [[launch-readiness]]

**Launch Readiness perspective — 🚩 RED condition on critical path**

AMG-100 is still in DVT (per `products.md`), so the eMMC allocation cut hits before first PVT — but Q4 *is* the planned launch window for the Gen 3 tablet. A 40% eMMC shortfall means one of three things happens:

**1. Q4 build plan shrinks.** You protect launch quality but ship fewer units. Risk: launch customers get partial allocation, service spares pool starts underfilled. Cost is commercial (deferred revenue), not engineering.

**2. Alternate source qualification compresses DVT → PVT.** You dual-source the eMMC now. Cost: requal cycle pulls reliability testing tight, and certs (FCC Part 15, UL 62368-1) may need re-eval if the new part changes emissions or power profile. Owner: HW eng + cert team.

**3. Delay launch to Q1.** All AMG-100 dependencies (packaging, serialization, spares planning, RMA lane setup) slip. Cost: TS-90 legacy pool burns hotter while customers wait.

**Numbers:** 0 of 6 launch checklist gates can close without a firm PVT allocation. Ramp criteria (yield, escapes, capacity) not yet agreed — and now they'll shift with the eMMC answer.

**Our flag for the manager:** Pick the alternate source path and run it *now* — but don't let the ops/support side get surprised. If build volume changes, spares mix, RMA pool size, and deployment sequencing all need re-plan before first ship.

**Recommendation:** Go/no-go isn't today's call — but freeze the answer inside 48 hours or AMG-100 launch slips to Q1.

#### [[sourcing-buyer]]

**Sourcing take:** AMG-100 Q4 eMMC coverage just dropped from 100% to 60%. We have a confirmed 40% gap on a single-sourced BOM line item (Kioxia THGAMSG9T24BAIL, per `products.md`). This part is DVT-locked, no qualified alternate exists, and AMG-100 is targeting volume ramp this quarter.

**Numbers:**
- Gap: 4,800 units of 12,000-unit Q4 plan
- Expedite with Kioxia: +22% unit cost, delivery scattered across 8 weeks, still leaves 15% uncovered
- Broker buy (spot market): +85% markup, 6-week lead, authenticity controls (X-ray, decapsulation) add $4.50/unit and 5 days — counterfeit risk is real on this density
- ECO to alternate (Micron MTFC32GAZAQHD): $18k engineering cost, 10-week requal, pushes 4,800 units into Q1
- Partial build (7,200 now, 4,800 later): $67k line-down risk if Kioxia recovery slips, but preserves margin

**Recommendation:** Partial build with expedited Kioxia push to close gap; start Micron alternate qualification in parallel to break single-source dependency long-term.

**Brain references:** products.md (AMG-100 BOM), budget.md (total year $6.8M, material budget exposure)

#### [[odm-program-mgmt]]

**Factory take:** AMG-100 eMMC supply is now the binding constraint on Q4 builds. Current commitment vs. demand gap: ~40% of Q4 PO quantity at risk.

**Numbers:**
- AMG-100 eMMC (Kioxia): 40% allocation cut, ~6,000 units impacted at the Shenzhen ODM
- Alternative eMMC (Samsung/SanDisk): 14-week lead time, $4.20/unit adder, requires re-qualification (DVT impact)
- Dual-sourcing qualification timeline: 8 weeks minimum (golden samples + FAI)
- Current WIP already has material for ~2 weeks of line rate

**Options assessed:**
1. **Accept Kioxia partial shipment, re-phase builds** → shifts ~2,400 units into Q1, minimal cost but delays revenue
2. **Spot-buy through ODM broker network** → available in 3 weeks, $12-18/unit premium, authenticity risk
3. **Fast-track alternate eMMC qualification** → protects full Q4 volume but consumes scarce engineering bandwidth during DVT

**Recommendation:** Execute options 1 and 2 in parallel — re-phase 50% of at-risk units to Q1 while spot-buying to cover the other 50%, and launch alternate qualification for Q1 protection.

**Brain references:** products.md (AMG100 — DVT status, volume-critical), strategy.md (fleet uptime dependency on uninterrupted supply).

### Department synthesis

**Program position:** AMG‑100 Q4 build at risk — 40% eMMC gap must close inside 48 hours or DVT→PVT gate slips to Q1.

**Team signals:**
- **Hardware PM** flagged eMMC as critical path — 6–8 week delay exposure if unresolved.
- **Certification** warns any alternate eMMC triggers PCI/EMVCo re‑eval (8–12 weeks, ~$30–37K) — lab queues stretch past December.
- **BOM/ECO/PLM** confirms no qualified alternate exists; grey‑market buys risk cert voiding and traceability failure.
- **Launch Readiness** shows red condition — 0 of 6 launch checklist gates close without a firm PVT allocation; ops/support replanning required.
- **Sourcing Buyer** recommends partial build + expedited Kioxia push to close gap, plus second‑source qualification in parallel.
- **ODM Program Mgmt** recommends re‑phasing 50% of at‑risk units to Q1, spot‑buying the other 50% via broker network, and dual‑sourcing for Q1.

**Disagreements:** Sourcing and ODM both propose spot‑buy/broker paths, but BOM/ECO and Certification will not sign off on grey‑market material without traceability waiver and cert re‑check. Hardware PM and Launch Readiness push for speed — Certification and BOM/ECO hold the compliance line.

**Critical path:** eMMC supply → DVT exit → PVT start → Q4 launch. The binding constraint is certification lead time for any new part; the binding schedule date is the factory line‑down risk in ~2 weeks when current WIP exhausts.

**Recommendation:**
1. **Immediate:** Partial build with expedited Kioxia allocation (protects 60% of Q4 units with zero cert impact). No broker/grey‑market buys unless Certification and BOM/ECO jointly approve traceability controls — per their explicit flags.
2. **Inside 48 hours:** Open ECO to qualify second‑source eMMC (Micron/SanDisk); HW Eng and Cert teams start requal in parallel — 10–14 week cycle means material lands Q1, not Q4.
3. **Q1 buffer:** Re‑phase the 40% shortfall to Q1 using the qualified second source; launch readiness replans spares, RMA pool, and deployment sequencing accordingly.

**Brain references:** products.md (AMG‑100 DVT status, $329 ASP, $14.50 eMMC cost), budget.md ($6.8M annual, NRE impact for requal), laws (FCC, UL/IEC 62368‑1, PCI PTS/EMVCo).

Per Certification: Q4 ships only on Kioxia — no last‑minute chip swap without the lab delta, or we ship nothing.

## [[01-Departments/04-mfg-supplier-quality/index|04-mfg-supplier-quality]]

### Team inputs

#### [[odm-quality]]

**ODM quality take: Factory at risk of unauthorized BOM drift under allocation pressure.**

**Numbers:**
- Q4 AMG-100 build plan depends on ~40% more eMMC than Kioxia will supply
- At Shenzhen site, two prior shortages in the last 12 months triggered three unauthorized material substitutions (2 caught at OQC, 1 shipped and later recalled)
- Current OQC first-pass yield for AMG-100 DVT lots: 94.2% — below the 97% target, with root cause still open on power-cycling failures (tied to flash timing)

**Top finding:** If the program pushes the factory to source on the spot market without a qualification window and locked golden-sample comparison, the risk of a repeat unauthorized substitution is near-certain. Factory will prioritize schedule over spec if left unchecked.

**Recommendation:** Freeze AMG-100 eMMC BOM to qualified alternates only — no spot buys without 72-hr qualification run, golden-sample audit, and OQC hold.

**Brain references:** products.md (AMG-100 DVT), state.md (growth stage, Q4 build exposure)

#### [[supplier-quality]]

**Supplier quality take:** Kioxia eMMC — constrained; part is sole-sourced, qualification-critical, field-escape risk surfaces.

**Numbers:**
- Current Kioxia DPPM: 12 (trailing 12 months, all commodities).
- Kioxia lot rejections: zero past 4 quarters.
- Open Kioxia SCARs: 0.
- **Risk spike:** No alternate eMMC is qualified for AMG-100. Any broker-sourced lot will trigger full incoming screen (per authenticity protocol); expect 6–8 week qualification cycle for an alternate source if forced.

**Recommendation:** Do not chase the broker market — accelerate qualification of a second source parallel to eating the allocation cut on Kioxia’s committed volume, and tighten incoming inspection on every lot from the cut point until supply stabilizes.

**Brain references:**
- products.md (AMG-100, eMMC criticality)
- decisions-log.md (no prior supplier risk acceptances on this commodity)

#### [[manufacturing-engineering]]

**Mfg engineering take:** Kioxia's 40% allocation cut is a line-stopping event for AMG-100. The eMMC is likely a single-source BOM item soldered on the SMT line — it gates the entire process. If we don’t have it locked before line set-up, we’ll idle the line and still burn fixed costs (overhead, trained operators, fixture amortization).  

**Numbers:** Estimated SMT takt for AMG-100 mainboard is ~45 sec; a missing component stops the line entirely. Changeover to an alternate eMMC (if footprint/pinout differ) likely requires new stencil, SPI program, reflow profile, and requal — 4–6 weeks minimum, plus Cpk re-baseline on placement and solder joint inline X-ray (Cpk target >1.33).  

**Recommendation:** Buy available Kioxia allocation now; in parallel, rapidly qualify the closest pin-compatible drop-in from Samsung or WD — rework SMT program and run a limited pre-PVT build to prove capability.  

**Brain references:** products.md (AMG100 DVT status); unbuildable risk escalates to ME/EE team for BOM change control.

#### [[factory-test-yield]]

**Test/yield take:** If we react by relaxing test guardbands or skipping DPPM gates to hit volume, we ship AMG‑100 with blind spots we won’t see until RMA returns spike. Our ICT and FCT stations already show 2.3% fallout on eMMC flash — mostly weak sectors and slow write-verify on marginal lots. Cutting allocation means we’ll burn through prime silicon first, then pull from secondary bins that fail correlation more often.

**Numbers:**  
- AMG‑100 FPY: 91.4% (ICT 97.2%, FCT 94.1%)  
- eMMC-driven fallout: 2.3% of total FCT failures, DPPM escapes on flash in DVT stub runs ~1,200  
- Retest rate: 4.7%, with eMMC miscorrelations driving 0.9% of those retests — fixture‑wear suspect

**Risk:** If we switch eMMC source or bin tier without re‑correlating the test stations, station agreement (ICT‑vs‑FCT‑vs‑OQC) will degrade 400–800 DPPM. These are latent field failures under sanitizer/thermal cycling — hardest to catch.

**Recommendation:** Lock the flash test limits; don’t widen. Prioritize the allocation on the top two yield‑forgiving bins. Run a 200‑unit correlation study before accepting any substitute NAND. **Brain references:** products.md (AMG‑100 DVT), state.md (growth phase).

### Department synthesis

**MSQ position:**
We have a single-sourced eMMC line-down situation with a 40% volume gap in Q4. Allocation collapse doesn’t just gate volume — it triggers a chain of quality escapes if we handle it wrong. Historical pattern: the Shenzhen factory, under pressure, substitutes without qualification, and we get field recalls. We cannot repeat that. Containment starts by locking the BOM now, not after the first spot buy.

**Team signals (with differences surfaced):**
- **Supplier-quality** and **ODM-quality** are aligned on the top risk: unauthorized broker sourcing causing a field escape. Both want a frozen BOM, golden-sample gate, and no unqualified buys. Supplier-quality adds the practical timeline — any alternate eMMC qualification is 6–8 weeks, so we can’t wait for the shortage to bite before starting.
- **Manufacturing engineering** flags the line-stopping reality: missing eMMC on the SMT line burns fixed cost with zero output. Their estimate of 4–6 weeks for stencil/reflow requal on a non-drop-in alternate underscores the schedule window we’re already in. Disagreement with supplier-quality is minor: ME would push harder for immediate second-source qualification even if Kioxia’s committed volume could be stretched, because they see the tactical risk of a single missed lot.
- **Factory test** is the outlier warning: even if we get die, bin-tier switching without re-correlation will silently increase DPPM escapes (400–800 DPPM estimated) that field will feel later. They want to lock test limits now and run a 200-unit correlation study on any substitute. That adds 1–2 weeks to any alternate cut-in but prevents a latent field-reliability spike.

My call: factory test’s warning is underappreciated in a schedule-driven conversation but historically validated in our RMA data from the TS-90 recall. I weight it heavily.

**Numbers (per Brain & team data):**
- AMG-100 FPY: 91.4% (below 97% target); eMMC flash fallout 2.3% of FCT failures
- Current DPPM escapes on flash (DVT stubs): ~1,200
- Station agreement degradation risk on bin/source switch: 400–800 DPPM
- Alternate qual cycle: 6–8 weeks (supplier-quality); SMT requal: 4–6 weeks (ME); correlation add: 1–2 weeks (test)
- Kioxia trailing DPPM: 12; zero lot rejections; zero open SCARs — it’s a clean, known source, which makes substitution risk higher by comparison

**Recommendation:**
1. **Buy all Kioxia allocation immediately** and lock committed volume against the build schedule — no spot market tail-chasing (per supplier-quality, ODM-quality).
2. **Parallel-qualify the closest pin-compatible drop-in** (Samsung or WD eMMC) starting this week — treat the qualification as a 6–8 week project with golden-sample audit, OQC hold, and SMT requal (per ME, ODM-quality).
3. **Protect test integrity:** freezel flash test limits, map acceptable Kioxia bins to the top two yield-forgiving tiers, and run a 200-unit correlation study before accepting any alternate die into production (per factory test). That correlation window must be built into the schedule now, not retrofitted.
4. **Escalate to design engineering** ([[01-Departments/01-hardware-engineering/agents/hw-engineering-manager]]) if the alternate eMMC requires any footprint or pinout deviation — BOM change control is their gate, not ours. And flag to [[docs/departments/02-npi-program-management/agents/npi-pm-manager]] that Q4 build plan needs a phased ramp, not a burst, to absorb the qualification timeline.

**Brain references:** products.md (AMG-100 DVT, eMMC criticality), state.md (growth phase, Q4 exposure), decisions-log.md (no prior risk acceptances on this commodity).

## [[01-Departments/05-service-operations/index|05-service-operations]]

### Team inputs

#### [[repair]]

**Repair take:** Bench queue 38% over SLA — RMA volume steady at TS-90/CY-80L legacy fleet (avg 72 units/week), but we’re seeing early AMG-100 field returns from DVT beta sites. Backlog aging is 9 days against a 5-day SLA. Yield on TS-90R holding at 87%; CY-80R at 83%. Parts blockers: TS-90 batteries (3-week lead) and AMG-100 eMMC modules — already flagged as single-source risk.

**Numbers:** Turnaround 8.2 days avg (vs. 5-day SLA), repair cost $38/unit, TS-90R yield 87%, CY-80R yield 83%. AMG-100 returns are <5 units so far — all eMMC-related boot failures.

**Recommendation:** The 40% eMMC cut will crater our AMG-100 repair pool before Q4 even starts. We can’t refurb what we can’t reflash. Push for dual sourcing now, and prioritize the AMG-100 spares allocation against the build plan — repair pool gets zero otherwise, and every field return becomes a dead unit eating SLA.

**Brain references:** products.md (AMG-100 section — DVT stage means no refurb pipeline yet; TS-90R/CY-80R pools are live).

#### [[fulfillment]]

**Fulfillment take:** Q4 AMG-100 shipments are at immediate risk — every late or incomplete order hits our >98% OTS commitment and triggers customer penalties.

**Risk:** 40% eMMC cut means we can only ship ~60% of committed Q4 volumes on time. No alternative eMMC source is qualified. Substituting unqualified flash risks configuration drift, field failures, and traceability breaks — violations of our "verify at kitting" principle.

**Numbers:** Q4 committed orders against current allocation show a shortfall of roughly 40% of AMG-100 units. Every late shipment erodes OTS and creates exception counts we can't absorb without process breaks. Serial tracking requires matched components — swapping eMMC without re-qualifying breaks the manifest chain.

**Recommendation:** Cut Q4 AMG-100 commitments now to match known supply, prioritize existing TS-90/CY-80R fulfillment where possible, and flag allocation gaps to Inventory for re-balancing. No unqualified substitutions.

**Brain references:** products.md (AMG100 configuration, packaging requirements); state.md (growth stage with volume expectations)

#### [[inventory]]

**eMMC allocation cut — inventory perspective**

**Risk 1 — Unbalanced stock building.** If we pull forward other BOM parts to "stay ready," we'll inflate WIP inventory with no assembly to consume it. That drives raw-material dollars up and hides reallocation pain. *Brain ref: budget.md total_year_usd $6.8M; products.md AMG-100 DVT status means we're pre-revenue — no demand to burn through over-bought silicon.*

**Risk 2 — Fragmented lot control.** If the 40% reallocated volume lands in salvage-market channels (spot buys), traceability snaps. Later, if Kioxia firmware or NAND revision matters, RMA root-cause gets messy — think field failures tracked to a mystery lot. *Brain ref: state.md says growth — early field quality impression sticks.*

**Dependency — No spares pool yet.** AMG-100 doesn't have an active installed base, so we can't borrow from spares (unlike TS-90/CY-80). Safety stock is simply purchase coverage.

**Numbers:** No current AMG-100 inventory (DVT). Exposure is not holding cost — it's the **missed Q4 fulfillment commitment cost**.

**Recommendation:** Lock the unaffected 60% immediately into firm POs by date-code; do NOT pre-buy dependent BOM parts until build certainty clears. Flag partial-build E&O risk to BOM team.

#### [[deployment-support]]

**Deployment take:** Pilot-ready sites (currently 3 of 12 committed for Q4) must be prioritized for the reduced eMMC supply. If we can't ship full kits, wave-1 installs stall, delaying acceptance and revenue recognition.

**Numbers:**
- Q4 sites ready for install: 3/12 confirmed (`products.md` shows AMG100 = DVT, so pilot only)
- eMMC cut: 40% reduction = ~60% of planned units available
- Install backlog risk: if allocation <60 units, we can't cover all 3 ready sites (20 devices/site minimum per `strategy.md` ICP)

**Recommendation:** Stage spares *before* wave-1 installs, not after. Cut the eMMC allocation to cover only confirmed-ready sites, and freeze unconfirmed sites until supply stabilizes. Field swaps from incomplete installs break two sites — don't let it happen.

**Brain references:** products.md (AMG100 DVT status), strategy.md (20-60 devices/site ICP)

#### [[logistics]]

**Logistics take:** If we shift sourcing to protect Q4 volume, the lane and customs exposure changes immediately. Two paths need logistics vetting: Mexico‑build (reducing inbound transit but changing duty treatment under USMCA) and Vietnam‑build transfer from ODMs already running AMG‑100 qualifications. Air freight will be the fallback if any option stalls — and air eats the freight budget.

**Numbers:**
- **Option A – Current China lane, constrained allocation:** 40% shortfall on eMMC so ~12k units at risk; no change to landed cost (~$21.50/unit DDP, 28‑day ocean). But the 12k gap either dies or flies.
- **Option B – Mexico ODM push:** Landed cost drops ~$3.80/unit (USMCA, no Section 301, 4‑day truck). Risk: USMCA qualification doc not yet ready — filing wrong kills the saving and invites audit.
- **Option C – Vietnam ODM backup:** Landed cost roughly +$4.20/unit vs China (no FTA, 34‑day ocean). If eMMC is urgently air‑freighted from Shenzhen to Vietnam to keep line running, add ~$11.20/unit in air freight — total crossing $36/unit landed, 2× budget model.
- Duty exposure: Mexico lane wrong HTS or origin cert = penalties up to 2× duty owed. Vietnam lane no GSP, so full MFN rate.

**Brain references:** products.md (AMG100 values, origins), budget.md (freight model ~$18‑22/unit DDP, $6.8M total year).

**Recommendation:** Lock Mexico lane only if USMCA paperwork is filed this week; otherwise run the China shortfall via Vietnam surface — no air freight unless the CFO signs off the budget overrun.

### Department synthesis

# Service ops position

The Kioxia allocation cut is not a supply-chain abstraction — it’s an imminent SLA, fulfillment, and field-readiness event. We cannot absorb a 40% part shortfall through ops heroics. My teams are already running hot on legacy fleets; the AMG‑100 hasn’t even built its safety net yet.

## Team signals

**Repair** flagged the most binding constraint first: we currently have *zero* AMG‑100 spares. Every field return with this eMMC failure signature will become a dead unit — no refurb pipeline (per `products.md`, AMG‑100 is DVT, so no refurb pool exists). That puts the repair bench at immediate SLA risk once pilot installs go live.

**Fulfillment** confirmed ~60% of Q4 volumes can ship if we lock the remaining allocation. They are dead right: no unqualified substitutions — serial traceability and configuration control are non‑negotiable. Per Fulfillment, even one unqualified flash lot would break the kitting‑manifest chain and create traceability gaps that Quality will flag later.

**Inventory** warned against the classic panic move — pre‑buying dependent BOM parts. That inflates WIP with no assembly to consume it, masking the real problem in raw‑material dollars (budget.md shows we’re at $6.8M total, pre‑revenue; `state.md` says growth — there’s no demand burn‑off for idle silicon).

**Deployment** tied the math to real sites: 3 of 12 Q4 pilot sites confirmed ready, each needing ≥20 devices (`strategy.md` ICP). They recommend staging spares *before* wave‑1 installs — I support this completely. Field swaps that poach units from an incomplete site break two installs, not one.

**Logistics** gave us three lanes, and the cost spread matters. Mexico (Option B) is the best long‑term bet if USMCA paperwork is filed this week — $3.80/unit savings vs China. But if that paperwork isn’t ready, the Vietnam backup (Option C) hits ~$36/unit landed with emergency airfreight, double the budget model (`budget.md` freight ~$18‑22/unit DDP). Air freight from any lane requires CFO sign‑off — I will not absorb that in ops without budget amendment.

## Numbers

| Metric | Value |
|--------|-------|
| Q4 AMG‑100 units at risk | ~40% of build plan |
| Legacy fleet turnaround | 8.2 days (vs 5‑day SLA) |
| AMG‑100 spares pool | Zero — DVT stage |
| Mexico landed cost delta | –$3.80/unit (if USMCA filed) |
| Vietnam air‑fallback landed cost | ~$36/unit (2× budget) |

## Recommendation

1. **Lock the 60% immediately** into firm POS — per Inventory.
2. **Allocate that 60% to the 3 confirmed‑ready pilot sites** — per Deployment.
3. **Stage spares component kits (eMMC modules) for Repair now** — even 10–15 units — so the first field returns aren't dead ends.
4. **Green‑light Mexico lane only if Logistics confirms USMCA filing this week** — otherwise run China shortfall via Vietnam surface; no air freight without CFO approval.
5. **Cut Q4 commitments to match supply** — per Fulfillment — before customer penalties stack on top of SLAs we already can’t hold.

**Brain references:** `products.md` AMG‑100 DVT status and spares absence; `strategy.md` ICP (20–60 devices/site); `budget.md` total year $6.8M and freight model $18‑22/unit; `state.md` growth stage.

## [[01-Departments/06-finance/index|06-finance]]

### Team inputs

#### [[controller]]

**Controller take:** Kioxia’s 40% eMMC cut for AMG-100 hits Q4 build plan directly. We haven’t PO’d the full Q4 eMMC volume yet, but we *have* POs for other AMG-100 BOM items already placed. Those are committed, not reallocable.

**Numbers:**
- AMG-100 unit cost (BOM): **$190.82** (from products.md — $329 price, 42% margin → COGS $190.82). eMMC is ~$12–18/unit based on market; 40% cut on a 10k-unit Q4 plan = **$48k–72k gap** if we spot-buy.
- FY budget: **$6.8M total** (budget.md). Q4 allocation TBD, but contingency sits at 5% standard (~$340k). This qualifies as a contingency draw request.
- No over-threshold PO (>$50k) triggered yet, but a spot-buy above that will need CFO sign-off.

**Classification:**
- Already-placed AMG-100 POs (displays, touch panels, enclosures): **sunk/committed** — can’t claw back without penalties.
- eMMC allocation loss: **not yet spent** — we have options.
- Any expedited spot-buy premium: **expensed** cost of goods, not capital.

**Recommendation:** Broker buy or alternate sourcing for the shortfall now — before spot market spikes. Open a $75k contingency draw for Q4 eMMC bridge, with buyer approval logged before PO. If we wait, the premium eats Q4 margin.

**Brain references:** budget.md (contingency guardrail), products.md (AMG-100 COGS).

#### [[financial-analyst]]

### Analyst take
Kioxia’s 40% cut to our AMG-100 eMMC allocation creates a hard Q4 supply gap. The AMG-100 is our highest-margin product (42% at $329 ASP). Failure to meet the build plan directly erodes revenue from our core ICP—casual-dining chains deploying 20–60 units per site, where downtime kills their labor and upsell model.

### Numbers
**Base (no action):** 40% shortfall = ~1,200 units lost (based on planned build). Revenue at risk: ~$395K; margin lost: ~$166K.  
**Committed cash:** None yet; this is a trigger-based exposure.  
**Expected cost:** 70% probability this cut holds × $166K margin loss = ~$116K expected value.

### Scenarios
- **Upside:** Kioxia partially restores allocation in 30 days (20% probability) — cut reduces to 20%, saving ~$83K margin.
- **Risk-fires:** Spot market buy at 2.5x standard cost erodes unit margin to ~28%, costing ~$55K additional for the same 1,200 units.
- **Trigger sensitivity:** Time-to-broker. Every week delayed increases spot premium by ~5%.

### Recommendation
Trigger immediate spot-market sourcing for 500 units to bridge output while negotiating partial restoration. Do NOT commit full gap yet.  
**Brain references:** `products.md` (AMG-100 margin), `budget.md` (no Q4 contingency allocated for eMMC spot buys).

### Department synthesis

**Finance position:** Fund-with-conditions — authorize a $75k contingency draw for immediate bridge sourcing, but only on the condition that NPI PM confirms the first 500-bridge build plan and Engineering validates the alternate component in 10 days. This is a schedule-preservation spend with a clear ROI.

---

**Team signals:**

- **Controller:** We have *not* committed POs for this Q4 eMMC volume yet. Already-placed BOM POs (displays, touch panels) are sunk — can’t reallocate. She recommends broker or alternate sourcing now, before spot pricing spikes, and logs this as a $75k contingency draw.
- **Financial Analyst:** Revenue at risk is $395k if we do nothing (margin loss ~$166k). Expected value of that loss = ~$116k (70% probability × $166k). Recommends *partial* sourcing for 500 units, not the full gap, while negotiating with Kioxia.
- Disagreement: Controller wants full bridge; Analyst wants staged. I agree with the staged approach — we buy time without blowing the full reserve in one bet.

---

**Numbers:**

- **Committed cash:** $0 for eMMC. Other AMG-100 POs (displays, enclosures) are committed and unrecoverable.
- **Expected cash:** $48k–72k gap at standard cost if we have to spot-buy full Q4 volume. Analyst’s recommended 500-unit bridge: ~$20k at standard cost, up to $40k at 2x spot.
- **Recoverable capital:** Not applicable — spot purchases are expensed COGS, not inventory pre-sold.
- **Margin impact:** 500-unit run at 42% margin (~$69k margin generated) offsets the bridge cost. Even at 2x spot premium, net margin contribution remains positive.
- **ROI:** If the Kioxia cut holds at 40%, $20k–40k spend protects $166k in Q4 contribution margin — 4x–8x return.

---

**Guardrail:** Any PO > $50k needs my sign-off (per budget.md). The contingency draw of $75k also requires entry into the decisions log and CCB notification. I’m capping initial authorization at $45k for the first 1,000 units sourced — keeps us under threshold while we validate.

---

**Recommendation:**
1. **NPI PM Manager** — Confirm the first 500-unit bridge build plan within 3 days, with updated Q4 ship dates.
2. **Engineering** — Validate an alternate eMMC SKU (from broker) in 10 days. No full gap commitment until validated.
3. **Controller** — Open $45k contingency authority now; escalate if spot-market quotes exceed 2x standard cost.
4. **Analyst** — Track Kioxia allocation signals weekly. If partial restoration by week 4, we may cancel unspent authority.
5. **Quality (MSQ)** — Vet any broker-sourced lot for authenticity before acceptance.

**Brain references:** `budget.md` (contingency draw guardrail, $340k reserve), `products.md` (AMG-100 margin — 42% at $329 ASP, BOM cost basis).