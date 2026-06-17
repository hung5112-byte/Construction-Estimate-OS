---
type: meeting_r1
---
# Round 1 — Perspectives

## [[01-Departments/01-hardware-engineering/index|01-hardware-engineering]]

### Team inputs

#### [[me-team]]

**ME take:**  
The enclosure and structural mechanics are the wrong place to chase $0.50 — tooling changes erase any BOM savings. But we can commit to two zero-tooling, no-regression moves.

**Numbers:**  
- Wall thickness reduction: requires steel-safe tool mod → $8k–15k and 4–6 weeks lead per mold; kills any $0.50/unit payback inside 50k units.  
- Adhesive change (PSA to snap-fit on battery cover): eliminates 2 adhesive strips/unit → $0.18 saving; no tool change, drop/IP test required.  
- Screw count reduction (4→2 on main PCB bracket): saves $0.22 in fasteners + assembly time; requires boss rib reinforcement (tool-safe, $0 extra) and vibration test.  
- Cosmetic finish downgrade (soft-touch to texture-in-mold): saves $0.35/unit, zero tool cost — but factory must validate mold texture consistency across 4-cavity tool.

**Recommendation:**  
Target adhesive + screw reductions first ($0.40 combined). Avoid any tooling geometry change — schedule risk outweighs $0.50. No performance impact; purely mechanical assembly optimization.

**Brain references:** products.md (AMG100 — DVT status, enclosure defined; AMG-D10 dock interface unchanged)

#### [[ee-team]]

**EE take:** Three sensible pockets exist, but each has an electrical hook:

1. **Battery pack wiring gauge (AMG100 → AMGD10 charging path):** The dock charge harness is over-specified at 22 AWG. Dropping to 24 AWG saves ~$0.22 at the assembly level while staying within the 2.4A max charge current thermal envelope (16.5°C rise vs 12.3°C — still well under the 30°C UL limit). Must verify ripple on the tablet PMIC input stays <50mV at peak load.

2. **MLCC consolidation on the mainboard:** Two 10µF/25V X7R decoupling caps near the PMIC can merge into a single 22µF/25V with no PDN impact. Saves $0.18, frees 12mm² of placement area. Requires transient load-step test to confirm Vdroop <3%.

3. **WiFi/BT antenna matching network:** Remove one redundant shunt element (3.3pF) from the diversity path. Saves $0.09. Return loss delta <0.4dB at 2.4/5GHz — pre-scan to confirm no EMC margin erosion.

**Numbers:** Total savings $0.49. All parts are multi-sourced, in-stock at DigiKey/Mouser. No single-source risk.

**Recommendation:** Bundle all three; validation gate = 24-hour burn-in + EMC pre-scan + load-step transient on 5 DVT units.

**Brain references:** products.md (AMG100 DVT status, AMGD10 dock dependency), budget.md ($329 ASP, 42% margin target).

#### [[fw-embedded-team]]

**FW take:** This cost-down mandate will likely touch components that firmware depends on — memory, PMIC, sensors, or radios. Any substitution risks subtle timing/performance regressions if not validated properly. We need 3 things:

1. **BOM change impact assessment on firmware** — If a component swap affects bootloader init, power sequencing, I2C/SPI timing, or driver compatibility, firmware rework is required. This isn't just a hardware change.

2. **No regression means identical firmware benchmarks** — Must define and freeze current AMG-100 performance baselines (boot time, GPU frame rates for games/UI transitions, NFC payment processing latency from tap-to-auth). Without these, "no regression" is meaningless.

3. **Fleet compatibility** — If any component change forces a firmware fork (AMG-100 v1 vs v2), we now maintain two images forever — provisioning, OTA, and RMA complexity spike.

**Numbers:** Even a "simple" component swap can mean 4-6 weeks firmware integration + test. If we touch boot-critical components, add 2 weeks for factory provisioning re-validation with ODM team. Risk: high if rushed.

**Recommendation:** Freeze firmware performance baselines FIRST, then evaluate every proposed BOM change against firmware impact before approving — not after.

#### [[system-architecture]]

**Architecture take:** The $0.50 BOM reduction is a tactical single-product ask, but will cascade into the AMG family and dock ecosystem if not scoped. The real architectural question: which components can change without triggering re-certification or dock interoperability faults?

**Options:**
1. **Memory downgrade (DRAM/NAND bin)** — save $0.30–0.60 by moving to slower speed-grade LPDDR4 or eMMC. *Trade-off:* must prove no UI jank or boot time regression under worst-case thermal. Risk: borderline on AMG-100's heavy game/upsell workload.
2. **Passive consolidation** — replace 2–3 discrete passives (decoupling/filtering) with single integrated packages or thinner-tolerance MLCCs. *Trade-off:* ~$0.20–0.40 savings; low risk but requires full SI/PI re-validation. No cert impact.
3. **Connector/mechanical cost-out** — swap pogo-pin block or flex assembly on dock interface. *Trade-off:* must ensure AMG-D10 dock mate/demate cycles hold. Schedule risk: tooling lead time.

**Recommendation:** Option 2 (passive consolidation) as primary path — no speed regression surface, zero certification re-spin, fastest to validation gate. Layer in Option 1 only if BOM analysis shows enough margin at the memory speed bin (I need the EE team's SI margin report before committing). The assumption: the passive changes don't uncover a PDN resonance that forces a layout tweak.

**Brain references:** products.md (AMG100 + AMGD10 dock dependency), strategy.md (uptime and harsh-environment durability still gate any connector change).

### Department synthesis

## Engineering Position

We can meet the $0.50 cost-down target without performance regression, but we must sequence the work carefully and avoid any changes that require tooling or firmware forks. Our position: pursue passive changes that are electrically equivalent and mechanically zero-tooling first. Defer memory speed-bin downgrades until we have margin data in hand. No commitment on schedule until validation gates are defined — the electrical burn-in and EMC pre-scan define the critical path.

## Team Signals

**ME Team** raised a hard constraint: no tooling geometry changes — the payback math fails inside 50k units due to mold modification cost and lead time. They identified two zero-tooling moves (adhesive elimination, screw count reduction) totaling $0.40. I credit this as the safest mechanical baseline.

**EE Team** identified three electrical pockets totaling $0.49 — wire gauge drop, MLCC consolidation, antenna shunt removal. All are multi-sourced, in-stock parts with clear validation criteria. This is our primary path to the $0.50 target.

**FW Embedded Team** flagged a critical process gap: any component change that touches boot-critical hardware, PMIC sequencing, or radio interface timing can force a firmware rewrites and potentially a fork. They demand frozen performance baselines before we approve any BOM change — I endorse this fully. Without baselines, "no regression" is a hand-wave.

**System Architecture** correctly scoped the ecosystem risk: AMG-D10 dock interoperability and certification exposure are the hidden tripwires. They recommend passive consolidation as the primary path, with memory downgrade only if SI margin supports it. I agree.

**Key disagreement:** ME wants to go first (adhesive/screws). EE wants to go first (electrical changes). Architecture wants passives first. Resolution: we bundle the EE passive changes with the ME assembly optimizations into a single validation lot — they are independent changes, no interaction risk, and together they hit the target.

## Risks (ranked by severity)

1. **Validation cycle time compression (Owner: Hardware Engineering, all teams)** — bundling changes into one DVT lot means we test five things at once. A single failure stalls the entire plan. Mitigation: pre-test each change in isolation on earlier rev boards where possible.

2. **PDN resonance uncovered by MLCC consolidation (Owner: EE Team)** — replacing two 10µF caps with one 22µF changes the decoupling network impedance profile. A resonance at the wrong frequency could cause PMIC instability. Mitigation: load-step transient test and impedance sweep on DVT units; if failing, we fall back to original BOM and eat the $0.18 gap.

3. **Firmware baseline drift (Owner: FW Embedded Team)** — if we don't lock baseline performance metrics before testing new hardware, we cannot prove no regression. Mitigation: freeze baselines Week 1 of cost-down sprint.

4. **Antenna matching margin erosion (Owner: EE Team)** — removing a shunt element is low-risk on paper, but EMC pre-scan is non-negotiable. If return loss margin degrades, we revert — cost impact $0.09.

5. **Mold texture consistency (Owner: ME Team)** — texture-in-mold saves $0.35 but requires factory validation across 4-cavity tool. Risk: aesthetic variation at scale. Mitigation: golden-samples from all cavities during trial run.

## Recommendation

**Adopt the following cost-down plan:**

| Change | Owner | Savings |
|--------|-------|---------|
| Adhesive elimination (PSA→snap-fit) | ME | $0.18 |
| Screw count reduction (4→2) | ME | $0.22 |
| Wire gauge drop (22→24 AWG) | EE | $0.22 |
| MLCC consolidation (2×10µF→1×22µF) | EE | $0.18 |
| Antenna shunt removal | EE | $0.09 |
| **Total** | | **$0.89** |

We over-target intentionally — select the safest $0.50+ from this menu based on validation results. Cosmetic finish change ($0.35) held in reserve if any EE change fails validation.

**Validation gate:** 24-hour burn-in + EMC pre-scan + load-step transient + vibration test on 10 DVT units with frozen firmware baseline. FW team signs off on performance benchmarks before ECO approval.

**Critical path:** EMC pre-scan scheduling (1-2 week lead time at test lab). We cannot commit a gate-pass date until the lab slot is booked.

**Brain references:** products.md (AMG100 DVT status, AMG-D10 dock dependency; both products in DVT phase), budget.md ($329 ASP, 42% margin target — $0.50 reduction is 0.15% of ASP, achievable without structural risk).

## [[01-Departments/02-npi-program-management/index|02-npi-program-management]]

### Team inputs

#### [[hardware-pm]]

**Program take:** AMG-100 is in DVT. This is the wrong phase to go fishing for $0.50 on a 329-dollar device. Every BOM change here requires re-validation of the build you're about to freeze. Top risk: a late-cycle ECO trades $0.50 for a schedule slip that delays DVT exit or forces a partial re-do.

**Numbers:** DVT units are likely building now or soon (products.md). BOM cost-down at this stage costs 3–5x more in engineering re-spin than one deferred to a post-launch PCR. We have no visibility into budget.md NRE headroom for this side-quest.

**Recommendation:** Table the cost-down until after DVT gate. If forced: replace the single highest-dollar discrete (likely PMIC or DRAM) with a pin-compatible lower-cost variant, validated through a focused reliability bench. Let sourcing buyer [[01-Departments/02-npi-program-management/agents/sourcing-buyer]] quote the top 3 BOM line items for reference, and let quality manager [[docs/departments/03-quality-reliability/agents/quality-manager]] define the regression test suite before any change is cut in. **Binding constraint:** DVT phase integrity. No ECO without a dated build slot and predefined pass/fail criteria.

**Brain references:** products.md (AMG-100 DVT phase), budget.md (NRE undefined)

#### [[certification]]

Cert take: This cost-down BOM change on an **in-DVT payment device** is a high-watch item. AMG-100 is a PCI PTS and EMVCo Level 1/2 candidate — any component swap in the secure boundary, power supply, or RF chain can re-trigger testing and add 8–14 weeks to the critical path.

Numbers:
- PCI PTS PoC: Lab queue 6–8 weeks + sample build 2 weeks = 10-week risk if touch secure boundary.
- FCC 47 CFR Part 15: Antenna matching, shielding changes → Class B re-test, 3–4 weeks.
- UL/IEC 62368-1 safety: Only if power path or battery charger changes.
- ECO cost: Lab fees start at $12K (EMVCo) + $8K (FCC) if retest required.

Recommendation: Before ECO approval, lock the BOM line items targeted and get a written “no cert impact” from the lab or we risk a st-op-ship on the Gen 3 launch.

Brain references: laws.md (PCI PTS, FCC, UL sections), products.md (AMG-100 DVT status).

#### [[bom-eco-plm]]

**BOM/ECO take:** AMG-100 is DVT stage. No open ECOs on the current rev. Any cost-down now is a DVT-phase change that must go through formal ECO — no skipping paperwork because "it's only 50 cents."

**Numbers:**
- $0.50 reduction on $329 ASP, 42% margin — margin impact negligible, but across 50k+ units/year, that's $25k+ annual savings
- Cost-down vectors ranked: (1) alternate DRAM/flash vendor — $0.30–$0.50, but must validate timing/latency parity; (2) PCB layer count reduction or impedance tolerance relaxation — $0.20–$0.40, risk to signal integrity; (3) passive component substitution (capacitors, resistors) — $0.05–$0.15, low risk
- Stock exposure: DVT builds are small, so scrap/rework cost is low — change now before PVT lock-in

**Risk:** Any memory or storage change triggers mandatory cert re-qual ([[01-Departments/02-npi-program-management/agents/certification]] — FCC, UL). EE team must provide timing margin analysis proving no throughput regression ([[docs/departments/01-hardware-engineering/agents/ee-team]]). Supplier qualification on alternate parts goes through [[docs/departments/04-mfg-supplier-quality/agents/supplier-quality]].

**Recommendation:** Target DRAM alternate as primary cost-down path, gate on full performance characterization + cert pre-scan before ECO approval — no cert verdict, no factory cut-in.

#### [[launch-readiness]]

## Launch Readiness Perspective

**Top flags:**

1. **BOM change = cert refresh risk.** Any component substitution (even passives) can invalidate FCC Part 15 and UL/IEC 62368-1 listings. If the $0.50 comes from a radio, power, or display component, recertification lead time must be in the schedule, not an afterthought.

2. **Packaging/labeling trigger.** A component change that touches the bill of materials may require updated labeling (regulatory marks, RoHS, country of origin). This hits serialization and box art — verify before first shipment.

3. **Ramp criteria gap.** We have no agreed performance regression criteria for the AMG-100 in `products.md`. Boot time, payment latency, and UI jank metrics must be quantified and signed off *before* validation, not debated during PVT.

**Numbers:** AMG-100 is in DVT, price $329 at 42% margin (`products.md`). $0.50 savings is ~0.15% of unit cost — make sure the cert/validation overhead doesn’t eat the margin.

**Recommendation:** Don’t approve cost-down without a cert impact assessment and a quantified performance regression gate signed by Engineering and Quality before the first PVT build.

#### [[sourcing-buyer]]

**Sourcing take:** I’m the last function to get the cost-down target — this likely hits procurement levers, not silicon or active components if speed is locked. Top candidates: passive discretes (resistors, capacitors), connectors, packaging, or logistics consolidation. No coverage risk yet for AMG-100 DVT BOM — build plan is confirmed against prototype volumes only (products.md, AMG100 status: DVT). At-risk parts: anything we re-source without a second source qualified, delaying DVT exit.

**Numbers:** $0.50/unit x 6,000 initial build = $3,000 target savings. Real savings path: consolidated ocean freight (saves ~$0.18/unit landed), alternate MLCC supplier (saves ~$0.22/unit, no performance impact), packaging slim-down (saves ~$0.10/unit). Total landed cost delta: –$0.50/unit, zero regression risk. Budget impact: negligible against $6.8M year; hits material budget line in budget.md.

**Recommendation:** Execute the MLCC alternate + packaging + freight bundle — zero silicon changes, no speed regression, fully validatable through standard DVT gates.

**Brain references:** products.md (AMG-100 DVT status, cost target not yet locked), budget.md (material budget line open, no spend to date).

#### [[odm-program-mgmt]]

**Factory take:** No AMG-100 build commits yet — still in DVT, no capacity locked. If cost-down requires a new component (e.g., alternate RAM, PMIC, PCB), tooling lead time could shift NPI build slots 4–6 weeks. That’s the real constraint, not the $0.50.

**Numbers:**
- AMG-100: DVT phase per `products.md` — pre-PVT, no SMT fixture freeze yet
- New component qualification: 3–4 weeks for samples, another 2 for first-article inspection at the ODM
- Any PCB respin adds 3–4 weeks to PVT entry unless we dual-source the old BOM in parallel

**Recommendation:** Lock the cost-down candidate list with engineering first. If it touches the PCB or a single-sourced active component, we protect NPI slots by running the baseline BOM build in parallel while the new rev qualifies — ODM won’t wait otherwise.

### Department synthesis

**Program position:** AMG-100 is in DVT. A $0.50 cost-down at this phase is a schedule risk, not a savings win. The critical path is DVT exit → PVT entry, not margin optimization on a $329 device at 42% margin. However, if forced to execute, the only zero-regression paths are non-silicon, non-PCB levers — and they must clear cert, quality, and factory gates before ECO approval.

**Team signals:**
- **Hardware PM:** Wrong phase for cost-down. DVT re-validation cost exceeds savings. Only pin-compatible alternatives acceptable.
- **Certification:** Any component swap in secure boundary, power path, or RF chain risks 8–14 weeks of re-cert (PCI, FCC, UL). Lab fees start at $20K combined.
- **BOM/ECO:** DRAM alternate is the fastest path to $0.50, but requires full timing margin analysis and cert pre-scan. Stock exposure is low now — change before PVT lock-in.
- **Launch readiness:** BOM change may invalidate regulatory marks and packaging. No performance regression criteria defined in `products.md` — gate must be set before PVT.
- **Sourcing buyer:** Zero-regression bundle achievable: MLCC alternate supplier (–$0.22), ocean freight consolidation (–$0.18), packaging slim-down (–$0.10) = –$0.50 total. No silicon touched.
- **ODM program management:** If cost-down touches PCB or active components, PVT entry slips 4–6 weeks. Baseline BOM build must run in parallel.

*Disagreement:* BOM/ECO wants DRAM alternate for speed to target; Sourcing says passive + logistics bundle avoids all risk. Certification will veto any active-component swap without pre-scan.

**Critical path:** Certification lead time if active components change (8–14 weeks to lab queue + retest) OR ODM requalification if new component requires tooling/fixture changes (4–6 weeks). The binding constraint is **DVT schedule integrity** per `products.md` (AMG-100 DVT status): no ECO that delays PVT entry.

**Recommendation:**
1. **Execute Sourcing’s bundle immediately:** MLCC alternate supplier, freight consolidation, packaging trim. All three are zero-regression, no-silicon changes validatable through standard DVT gates. ECO process applies per BOM/ECO team — no exceptions.
2. **Defer active-component cost-down to post-launch PCR.** DRAM/flash alternates will be re-evaluated after PVT, with full cert pre-scans and lab scheduling built into the program plan.
3. **Set performance regression gates now.** Launch readiness’s flag is correct: boot time, payment latency, UI responsiveness metrics must be defined, signed by Engineering and Quality, and tested in PVT before any cost-down that touches silicon.
4. **Owners:** Sourcing buyer executes bundle quote and supplier qualification (with Supplier Quality). Certification confirms no FCC/UL/PCI impact from passive + logistics changes. Hardware PM protects DVT schedule — no ECO without dated build slot.

**Brain references:** products.md (AMG-100 DVT phase — schedule integrity is the primary constraint), budget.md (material budget line open, $0.50/unit savings negligible against $6.8M annual budget).

## [[01-Departments/03-quality-reliability/index|03-quality-reliability]]

### Team inputs

#### [[qa-system]]

**QA System take:** Cost-down changes hit controlled documents — BOMs, inspection criteria, supplier qualification records. If we swap a component to save $0.50, the system must reflect the new part number, the new supplier (if any), updated incoming inspection checks, and traceability to the ECO that authorized the change. Miss that, and we fail a traceability audit or ship mixed-revision devices.

**Numbers:** Currently zero open audit findings, zero overdue CAPAs. That’s clean air we don’t want to foul. A component change without a controlled document path creates an instant finding — every certification audit checks BOM-to-build alignment.

**Recommendation:** Lock the ECO → BOM update → inspection criteria update → supplier qualification update chain before approving any component swap. No shortcut.

**Brain references:** laws.md (FCC 47 CFR Part 15 — any RF-adjacent component change may retrigger; UL/IEC 62368-1 — safety-critical part substitution requires NRTL review); state.md (DVT stage — changes now are cheaper than post-launch, but still require control).

#### [[qc-inspection]]

**Inspection take:**  
No AMG-100 in MP yet (DVT stage per products.md), so we have no dock data on this SKU. The $0.50 cost-down pushes toward second-source passives, lower-spec mechanicals, or PCB consolidation — all of which historically degrade cosmetic/functional DPPM if not bounded by tight incoming criteria. Our TS-90 MP baseline: passive component escapes at 1,200 DPPM from commodity suppliers; mechanical (connector/plastic) at 850 DPPM. These are the categories where cost-down usually hits.

**Numbers:**  
No AMG-100 lot-acceptance rates exist. TS-90 AQL for critical passives: 0.65%; minor mechanicals: 1.5%. For AMG-100 DVT pilot lots, we'll recommend AQL 0.40% critical / 1.0% minor until 3 lots clear, then consider skip-lot for capable suppliers.

**Recommendation:**  
Require first-article inspection with photo-anchored criteria for any cost-reduced BOM line. No supplier substitution without IQC re-qualification. Speed regression gates are the engineering team's problem — ours is catching cheap caps that short under thermal cycling.

**Brain references:** products.md (AMG-100 status: DVT; TS-90 MP baseline DPPM).

#### [[validation-reliability]]

**Validation take:** Cost-down without regression is a reliability gating exercise — every target component’s second-source or substitute must clear environmental stress and life-cycle testing at fleet-representative sample sizes. AMG-100 is DVT per `products.md`; we cannot swap in an unqualified part and wave it through. Marginals in thermal cycling or vibration would be a hard FAIL.

**Numbers:**  
- `products.md` / status: **DVT** → any BOM change requires a DVT-2 delta qualification, not later  
- Fleet uptime target: **>99.5%** (from strategy). Life test must show no impact to this.  
- Sample size: I need **n=30** per change (minimum for 95% confidence on 1% failure rate).  
- Test limits: Boot time < 2.0 s (ref: AMG-100 spec), payment latency < 150 ms, UI frame drop rate < 0.1%.

**Recommendation:** Gate all cost-down candidates with a dedicated reliability delta-qual (environmental + performance) before any PO cut. Zero tolerance for marginal results.

**Brain references:** products.md (status), strategy (uptime target)

#### [[firmware-qa]]

**FW QA take:** Blocked by incomplete update-path testing plan. The cost-down touches components that could subtly change timing behavior (power sequencing, flash timing, bootloader interaction) — that’s regression territory we gate on.

**What my team flags:**

1. **OTA update path regression risk.** Changing passives or substituting flash/NAND could alter boot timing or power rails enough to brick devices on update. We need update-from-all-fleet-versions campaigns (Gen2 TS-90, current AMG-100 early builds) plus power-loss mid-update tests — per products.md, fleet runs Gen2 and Gen3 concurrently.

2. **Boot time measurement baseline gap.** The brief says “no speed regression” but we don’t have formal boot-time or payment-transaction-latency regression suites agreed with [[firmware-embedded-team]]. Cost-down validation gates are undefined until we lock that.

3. **Field escape loop.** If this ships and 0.5% of units show delayed boot in harsh environments (sanitizer chemicals, thermal cycling per products.md), Field Quality/RMA will own $329 × fleet scale incidents. Every such escape becomes permanent regression.

**Numbers:** 0 test cases defined for update paths; 0 regression suites for boot/transaction timing; dependency on 3 firmware baselines (Gen2 legacy, Gen3 early units, Gen3-DVT).

**Recommendation:** Freeze the cost-down BOM change until [[docs/departments/01-hardware-engineering/agents/fw-embedded-team]] defines and runs the update-path + timing regression suite, and [[01-Departments/03-quality-reliability/agents/validation-reliability]] signs off on power-loss OTA. Then I gate.

**Brain references:** products.md (AMG-100, TS-90/TS-90R fleet versions), state.md (growth stage — field population matters).

#### [[field-quality-rma-fa]]

**Field quality take:** Cost-down on AMG-100 during DVT is premature — we have zero field failure data on this design. My concern isn’t the $0.50; it’s that component swaps (memory, PMIC, passives) done without fleet history will create failure modes we can’t predict from bench testing alone. We’ve seen this on TS-90: a “minor” capacitor cost-down in year 2 took 6 months to show as intermittent dock failures, affecting 3% of the fleet before we caught it.

**Numbers:** TS-90 fleet: ~18,000 units deployed; that capacitor issue at 3% rate = 540 returns before containment. We cannot afford a repeat on AMG-100 when it hits volume.

**Recommendation:** Any BOM change — especially memory timing or power rail components — must run through [[validation-reliability]] for accelerated life testing that includes speed/perf regression gates. Flag the affected part numbers with [[supplier-quality]] for PCN monitoring. If the cost-down touches anything on the USB or charging path, I want dock-interop regression testing included — that’s where our latent failures cluster.

**Brain references:** products.md (AMG-100 DVT, no fleet data); state.md (zero field returns on AMG-100, no failure baseline to judge “no regression”)

### Department synthesis

**Quality position:** AMG-100 is in DVT — zero field failure history, zero fleet data. The $0.50 BOM cost reduction is premature and carries unacceptable risk without a structured qualification gate. Currently, the QMS is clean (zero audit findings, zero overdue CAPAs), and I intend to keep it that way. Any component substitution that proceeds without a locked ECO → BOM → inspection criteria → supplier qualification chain will create an instant traceability finding. I am not placing this device on hold yet, but I will if the cost-down BOM change clears without the delta-qualification package my teams are demanding.

**Team signals:**
- **QA System** flags audit risk: any undocumented component swap breaks BOM-to-build traceability and may re-trigger FCC/UL compliance review.
- **QC Inspection** warns that cost-down hits passive and mechanical categories where TS-90 MP baseline escapes are 1,200 and 850 DPPM respectively — and we have zero incoming-inspection baseline for AMG-100.
- **Validation & Reliability** requires n=30 delta-qual per changed part, covering environmental stress and life-cycle testing, with zero tolerance for marginal results. This hasn't happened.
- **Firmware QA** is blocked outright: zero test cases defined for OTA update regression, zero boot-time/transaction-latency regression suites, and three firmware baselines in play across the fleet. A timing-sensitive component swap without this suite risks bricking devices.
- **Field Quality / RMA** cites TS-90 precedent: a "minor" capacitor cost-down caused 3% fleet failure (540 returns) that took 6 months to surface. No AMG-100 fleet data means no ability to detect latent failure modes before volume.

There is no disagreement among my teams — all five are aligned that this BOM change is not ready to proceed.

**Risk:** If we approve a component swap now, without delta-qualification and without firmware regression suites, we ship a risk of intermittent failures (thermal cycling, dock interoperability, OTA bricking) that will surface at fleet scale — $329 per unit × thousands of deployed devices — with escalating RMA costs and damage to the >99.5% uptime commitment. The cost-down savings will be erased by a single field escape.

**Recommendation:** Containment — freeze the cost-down BOM change. Before any PO cut: (1) lock the ECO → document update chain per QA System, (2) complete n=30 delta-qualification per Validation & Reliability including OTA power-loss and dock-interop testing, (3) [[docs/departments/01-hardware-engineering/agents/fw-embedded-team]] must define and execute the firmware regression suite Firmware QA requires, and (4) any changed part number goes through IQC re-qualification with photo-anchored first-article inspection per QC Inspection. I expect a CAPA plan with before/after data before I lift this gate.

**Brain references:** products.md (AMG-100: DVT, no fleet data; TS-90: MP baseline DPPM), strategy (>99.5% uptime target), laws.md (47 CFR Part 15, UL/IEC 62368-1 — component substitution may re-trigger compliance).

## [[01-Departments/04-mfg-supplier-quality/index|04-mfg-supplier-quality]]

### Team inputs

#### [[odm-quality]]

**ODM quality take:**  
AMG‑100 is pre‑MP in DVT — we have no locked factory process. On our last site audit we saw only three uncalibrated torque drivers on the test line. That is exactly the kind of slippage that turns a “safe” cost‑down (e.g. memory or PMIC change) into a field‑failure risk when the factory isn’t building to the golden sample.

**Numbers:**  
- Audit: 3 open findings from last SZ visit (torque tool cal, ESD mat grounding, OQC sampling plan missing for functional test)  
- OQC pass rate on current AMG‑100 DVT builds: 94.2% — already below the 97% gate for pilot  

**Recommendation:**  
Any BOM change must come with a control‑plan addendum and a pre‑qualification OQC audit against the golden sample — we verify the factory can build it before we ship it.

**Brain references:** products.md (AMG‑100 — DVT); state.md (growth)

#### [[supplier-quality]]

**Supplier quality take:** Cost-down shifts risk unless supplier part history supports it.

**Numbers:**
- AMG-100 is DVT — no MP field-history yet, so DPPM data on alternate components is absent.
- Any BOM substitution reopens supplier qualification, FAI, and DPPM monitoring from zero.
- Unqualified supplier slipped into AVL = SCAR risk before first MP lot.

**What we must flag:**
1. If the $0.50 comes from a lower-grade passive, connector, or PCB finish, we need the supplier’s DPPM history on that exact commodity — not generic capability claims.
2. Alternate source for same spec? Requires full qualification audit + FAI. Schedule pressure is the enemy here — skip it and field returns spike.
3. Root cause of any future escape must trace back to supplier process change, not just “operator error.” SCAR closure requires lot-acceptance data proving containment held.

**Recommendation:** Lock qualification gates before PO: audit, FAI, and 3-lot DPPM trend — no exceptions, even for a $0.50 move.

**Brain references:** products.md (AMG-100, DVT status), decisions-log.md (no supplier risk acceptances logged yet).

#### [[manufacturing-engineering]]

**Mfg engineering take:** $0.50 is thin — you’re not touching silicon or major PCB layout at that level. Realistic levers are things we can change without retooling a production line: adhesives, fasteners, labels, packaging simplification, or a second-source connector/cable that’s drop-in qualified. Any BOM change that forces a fixture change will eat more than the saving in NRE.

**Numbers:**
- Current AMG-100 DVT line takt: ~90s (products.md, AMG100 status DVT)
- A single-station fixture changeover costs $1,800–3,500; process requal adds 2–3 weeks.
- Yield-critical stations (display bonding, pogo-pin test) have Cpk ≥1.33 at DVT — any material change here risks that.

**What I’d flag now:**
1. **Second-source the internal flex cable or SMA connector** — ~$0.30–0.40 savings, drop-in if pinout/form identical; must pass our insertion/withdrawal cycle test at the same rate.
2. **Consolidate screws from 3 types to 2 across the assembly** — saves ~$0.10 in part cost and ~4 seconds assembly time (operator load reduction).
3. **Remove a redundant label or switch to in-mold marking on the rear housing** — avoids a manual placement station.

**Recommendation:** Run the flex cable second-source qualification first — highest savings with lowest line impact; validate at DVT2 before we lock the PVT process.

**Brain references:** products.md (AMG100, AMGD10 status/DVT)

#### [[factory-test-yield]]

**Test/yield take:** Cost-down that touches anything seen by production test is a yield excursion waiting to happen. First pass yield (FPY) on AMG-100 DVT is still stabilizing — we’re at ~91.3% aggregate, with top fallout from touch controller calibration drift (1.8% DPPM) and PMIC rail sequencing (0.9%). Our station correlation between FCT1 and FCT2 is shaky at 0.87 — we’re still chasing fixture-to-fixture variance on the new Gen 3 board. A BOM change, even passive alternates, risks sending that backwards.

**Numbers:** FPY 91.3%, DPPM escapes (known) ~2,100, retest rate 6.7%, FCT1↔FCT2 correlation r=0.87.

**What I need to see in any cost-down BOM swap:**
- Golden unit re-correlation across ALL FCT stations with the new part before first article ships — I will not sign off a deviation that dilutes test discrimination.
- Limit-file review: a cheaper PMIC or timing component can shift a rail by 20mV and trigger false fails. If EE changes a decoupling cap, I want 100-unit correlation run against the baseline.
- If the $0.50 comes from an antenna or RF path, expect shielding/gasket tolerance fallout — our near-field fixture sees that before OTA.

**Recommendation:** No BOM change ships without a station re-correlation protocol and a 200-unit yield bridge run — $0.50 is not worth losing test integrity.

### Department synthesis

**MSQ position:** We can save $0.40–0.50 with near-zero quality risk by second-sourcing a drop-in flex cable — that’s the only realistic path that meets the constraint (“no performance/throughput regression”) while protecting factory yield and supplier integrity. The other levers (fastener consolidation, label elimination) add small savings but must not distract from the main qualification. The bigger quality risk is that someone tries to touch silicon, power, or RF passives for $0.50, which is where test instability, supplier escapes, and field regressions live. On AMG‑100 at DVT, our baseline is shaky — we fix the process *before* we change the BOM.

**Team signals:**
- **Supplier quality** (per input) warns: alternate-source qualification requires audit + FAI + 3‑lot DPPM trend. No shortcuts.
- **ODM quality** (per input) flags the site isn’t process‑locked: 3 open audit findings, OQC pass rate already below gate (94.2% vs. 97% target). Any BOM change without a control‑plan addendum is premature.
- **Manufacturing engineering** (per input) identifies the flex cable or SMA connector second-source as the highest‑savings, lowest‑line‑impact move. Consolidating screws and labels can follow — but neither saves enough alone.
- **Factory test yield** (per input) insists: any BOM swap seen by FCT must go through golden‑unit re‑correlation and a 200‑unit yield bridge. We will not ship through shaky test (FPY 91.3%, FCT1↔FCT2 r=0.87) with an unvalidated part.

**Numbers** (from the Brain + teams):
- AMG‑100 status: DVT (products.md)
- ODM OQC pass rate: 94.2% (gate 97%) — ODM quality
- FPY: 91.3%; retest rate 6.7%; escapes ~2,100 DPPM — factory test yield
- Takt: ~90s — mfg engineering
- Supplier qualification DPPM baseline: none exists for AMG‑100 alternate components yet — supplier quality

**Recommendation:**
1. **Immediate path (owner: Manufacturing Engineering + Supplier Quality):** Qualify a drop‑in second‑source for the internal flex cable. Savings est. $0.30–0.40. Gate: audit + FAI + 3‑lot DPPM trend; insertion/withdrawal cycle validation to existing spec. No performance regression — pure interconnect, zero effect on CPU/GPU/UI.
2. **Supplementary path (owner: Manufacturing Engineering):** Consolidate screws (3 types → 2) and remove one redundant label. Savings est. $0.10‑0.15. Gate: process proof on PVT line; no fixture change. Combined, these two actions hit the $0.50 target without touching electronics.
3. **Quality hold line (owner: ODM Quality + Factory Test Yield):** Every BOM change subjected to these slides under a control‑plan addendum and station re‑correlation protocol *before* first article ships. No deviation from the 200‑unit yield bridge requirement for anything on the FCT path.
4. **What we block:** Any PMIC, decoupling cap, memory, or RF‑path change for $0.50 — the test‑stability and field‑regression risk is out of proportion to the saving, and the performance constraint makes it unsupportable at DVT maturity.

**Brain references:** products.md (AMG‑100 DVT), state.md (growth)

## [[01-Departments/06-finance/index|06-finance]]

### Team inputs

#### [[controller]]

## Controller take

Cost-down proposals are engineering hypothesis until they are committed on the ledger. Right now, Brain budget has $0 committed for BOM cost-reduction engineering effort — that work has to land against someone’s budget line before it is real.

## Numbers

- FY24 total engineering budget: $6.8M (all departments). Zero dollars currently coded to a BOM cost-down sprint for AMG-100 (Brain `budget.md`).
- AMG-100 unit material cost is not in budget.md; margin target is 42% at MSRP $329. A $0.50 BOM reduction would add ≈15 bp to gross margin — material to the P&L only at scale.

## Classification

- Any NRE spent to find the $0.50 is R&D expense — sunk once incurred.
- If a component change requires new tooling/fixtures, those become committed POs; classify as capital (recoverable over volume) or expense (consumed).
- Inventory already on hand at old BOM revision — already spent, cannot be re-costed retroactively.

## Recommendation

Before engineering starts the sprint, get a $25k–$50k PO on the ledger for the validation effort (benchmark testing, supplier samples). If not yet approved, flag it as an unfunded request.

**Brain references:** budget.md (current-year spend, no cost-down line) · products.md (AMG-100 margin target)

#### [[financial-analyst]]

**Analyst take:** This is a cost-reduction exercise — small unit impact but scales with volume. The $0.50/unit matters only if we ship meaningful quantities of AMG-100, so the model needs a volume assumption and a clear distinction between committed NRE (the engineering work to validate) vs. expected value (the savings if it works).

**Numbers:**
- **Per-unit savings:** $0.50 on a $329 ASP, 42% margin device — adds ~15 bps to margin once in production.
- **Breakeven volume:** If validation NRE runs ~$25K (engineering time + test builds + supplier samples), we need to ship 50,000 units to cover the investment. Below that, this is a negative-ROI project.
- **Committed cash:** Engineering and qualification NRE (likely $15K–$30K, sourced from the $6.8M annual budget). No committed inventory impact unless a new BOM line item requires a last-time-buy or MOQ.
- **Expected cash:** $0.50 × projected AMG-100 volume over the product’s remaining life (need Strategy’s volume forecast to pin this).

**Scenarios:**
- *Base:* 100K units shipped → $50K gross savings, ~$25K NRE → ~$25K net positive. Payback at 50K units.
- *Risk-fires:* If a substituted component fails qualification (yield hit, reliability flag) and triggers a re-spin, NRE could double to $50K–$75K, pushing breakeven to 100K–150K units. The “no performance regression” constraint amplifies this risk — any validation slip is expensive.
- *Upside:* If the cost-down applies across multiple SKUs sharing the same component, savings multiply without additional NRE.

**Key sensitivity:** Volume assumption. At <50K units lifetime, the project destroys value. Need the NPI or Strategy volume forecast to confirm.

**Recommendation:** Fund the engineering analysis (committed ~$10K–$15K to identify/scope the component swap), but make full validation NRE trigger-based — only commit once the component passes initial bench testing and we confirm AMG-100 volume exceeds 60K units. Reject if volume forecast is soft.

**Brain references:**
- `budget.md` — Engineering NRE fits within the $6.8M annual budget, but no specific line item for cost-down; needs allocation.
- `products.md` — AMG-100 at $329 ASP / 42% margin; the $0.50 is marginal to the unit economics, so this only matters at scale.
- `strategy.md` — ICP volumes (50–1,200-location chains, 20–60 devices/site) suggest ramp is real, but need the NPI forecast to lock the assumption.

### Department synthesis

**Finance position:** Conditional fund — proceed with scoping phase only; full validation NRE requires volume and bench-test triggers before commitment.

**Team signals:**
- *Controller* flags that zero dollars are currently on the ledger for BOM cost-down; any work is unfunded until a PO hits the books. This is the hard reality — engineering intent without a budget line is just a wish.
- *Analyst* makes the ROI case: $0.50/unit is noise unless we ship 50K+ units. At <50K, this destroys value. The “no performance regression” constraint compounds the risk — a failed qualification re-spin doubles NRE and pushes breakeven to 100K+ units. Both agree that committed cash (what we actually wire) must be separated from expected cash (future savings * probability).
- No disagreement between my teams, but we both need a volume number from NPI/Strategy before this moves beyond scoping.

**Numbers:**
- **Committed cash today:** $0. No work authorized, no POs issued.
- **Recommended next commitment:** $10K–$15K for scoping phase (component identification, supplier samples, bench testing plan) — drawn from the $6.8M annual engineering budget (needs reallocation per Controller).
- **Expected cash (if successful):** $0.50 × volume × probability. At 100K units and 80% confidence, that’s $40K expected value — net ~$15K positive after $25K NRE. At 40K units, it’s negative.
- **Recoverable capital:** None — all NRE is R&D expense, sunk once spent. If a tooling change emerges, that would be capital, but that’s not on the table yet.

**Guardrail:** No single PO over $50K without VP sign-off. Any full-validation NRE commit (tooling, qualification builds) >$25K triggers CCB and decisions-log entry. I’ll hold that line.

**Recommendation:**
1. **Fund now:** $10K–$15K scoping phase. HW engineering identifies candidate components, runs bench benchmarks (CPU/GPU/payment speed), orders supplier samples. Controller cuts a PO against reallocated engineering budget. Owner: HW Eng; deadline: 2 weeks.
2. **Gate before full validation:** Before committing the remaining NRE (qualification test builds, reliability runs, ~$10K–$15K additional), confirm:
   - Bench tests show zero performance regression (Quality signs off).
   - NPI confirms AMG-100 lifetime volume forecast >60K units (Analyst’s threshold with margin for re-spin risk).
3. **Reject if:** Volume forecast is soft (<50K), or initial bench tests show slowdown — kill it there.

**Brain references:** budget.md (spend allocation required, no cost-down line item) · products.md (AMG-100 margin target, ASP, unit economics) · strategy.md (ICP volume — ramp looks plausible but needs NPI’s committed forecast).