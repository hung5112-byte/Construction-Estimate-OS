---
type: meeting_r1
---
# Round 1 — Perspectives

## [[01-Departments/01-hardware-engineering/index|01-hardware-engineering]]

### Team inputs

#### [[me-team]]

**ME take:** Two mechanical items dominate our risk posture before DVT on 06/22.

**ISS-019 (antenna rework parts ETA 06/16):** The 3-day buffer (06/16 → 06/19 staging → 06/22 build) is thinner than a 0.15mm gap on an ultrasonic weld joint. If that shipment hits customs delay or the rework requires tool re-validation, we miss DVT. This is our enclosure seal-and-screw boss moment — the antenna carrier is molded into the mid-frame. A late change there means 2-3 weeks of steel-safe tool rework on the Chinese injection mold. **Cost impact:** $0 now (trigger-based), but ~$18k in expedited tool rework + air freight if we miss 06/16 by ≥2 days.

**ISS-021 (drop test post-rework):** We can't ship DVT units without a representative drop test result on the reworked mid-frame. From Brain `products.md`: the AMG-100 is a tabletop device in a spill-prone environment — the sealing and structural integrity after antenna rework is the mechanical gate. If the reworked part cracks the screw boss or unseats the gasket channel, we're back to tooling changes that hit the certificaiton schedule. **Recommendation:** Run 4-corner drop test on first-rework parts from the 06/16 shipment (48-hr turnaround, trigger-based), and keep the legacy TS-90R fleet on standby for the beta trial start.

**Thermal:** Our DVT boards run hotter than EVT (higher-performance SoC clock per ISS-028). We predicted 62°C junction temp in the sealed enclosure at 25°C ambient (Brain `mtbf-prediction`). That's within spec but leaving only 8°C margin to the EMV contact reader's thermal shutdown. If the beta trial runs in a hot kitchen-adjacent location this summer, we could see thermal throttling that pulls uptime below the 99.5% target. **$0 action:** Add a thermocouple in the DVT PRT units near the EMV module. It's a test-plan update, not a tooling change.

**Tooling cost context:** The mid-frame mold is a single-cavity steel tool (~$45k sunk). Any post-DVT change adds ~3 weeks lead time for steel-safe modifications and pushes the cert run (08/18 hard deadline). We cannot re-cut that tool after 07/01 without slipping the BrightPath ramp.

**Numbers:**
- Mid-frame tolerance stack: ±0.15mm on antenna carrier to gasket seat → critical for IPX4 sealing
- Dropt test spec: 1.2m onto concrete, 4 corners per MIL-STD-810G (Brain `prt-plan` section 3.2)
- Thermal margin: 8°C junction-to-shutdown (62°C predicted vs 70°C EMV thermal limit)
- Tooling change lead time: 18-21 calendar days for steel-safe mold mod in Shenzhen

**Recommendation:** Lock the mid-frame tool geometry at 06/16 — no further changes after rework parts arrive. If the drop test fails, fix with gasket durometer or assembly torque, not tool re-cut.

**Brain references:** products.md (section on AMG-100 mechanical configuration), mtbf-prediction (thermal margins), prt-plan (section 3.2 on drop test protocol).

#### [[ee-team]]

**EE take:** The DVT board is two spins past EVT and I’m still watching antenna rework parts land 3 business days before the build. That’s a schedule-critical single-point failure. ISS-014 (antenna tuning) must close with measured VSWR/efficiency data, not a factory “looks good.” If the 06/16 ETA slips past 06/17, we have no time for a board spin — we burn the DVT slot and lose the cert window. Second: eMMC dual-source is the right fight, but I need the alternate validated through the full device-bring-up and PCI PTS pre-assessment cycle (R-01, 07/06). A “form-fit-function” swap isn’t cert-neutral when it touches the secure element’s memory path. Third: EVT yield of 78% had board-level contributors — power sequencing edge cases on the PMIC and intermittent open on the battery connector. These must be root-caused and closed before DVT boards are built; otherwise yield stays low and DVT results are noise.

**Numbers:** Antenna parts ETA 06/16 with 3-day buffer to DVT build 06/22. MTBF 62k h vs. 2% AFR target. Battery 8D at D6. $872k spent of $2.0M, $111.6k contingency remaining.

**Recommendation (committed-now vs. trigger-based):**
- **Trigger-based:** Authorize DG courier for antenna parts *only if* supplier ETA slips past 06/17 (cost-if-fired: $3.2k, probability 30%, expected $960). Same for air-freight backup on any DVT-critical component with ≤5-day buffer.
- **$0 action:** RF engineer documents tuning procedure + test fixture requirements in a one-pager by 06/13 — this is our bus-factor mitigation (R-09) and costs nothing. Concurrently, start contractor search for backup RF support.
- **Committed-now:** Pre-stage DVT board bring-up lab time and CM test-fixture validation ($12k). This is the only way to guarantee 06/22 build isn’t followed by a 3-week debug stall.
- **Recoverable capital:** Move Tet/BrightPath pre-build inventory off the $111.6k contingency to a separate capital line. Right-size to actual DVT + early beta demand (not full ramp). This eliminates the $15k contingency-reallocation conflict.

**Committed cash:** $12k. **Expected cash:** $12.96k. No action weakens a quality gate. 06/22 DVT build and 08/18 cert path are protected.

**Brain references:** products.md (AMG-100 DVT), open-issues (ISS-014, R-01), budget-tracker.

#### [[fw-embedded-team]]

**FW take:**

1. **DVT firmware readiness is tight.** EVT yield at 78% means we’ll see more factory fallout — provisioning scripts and self-test must be rock-solid for DVT or we dump triage onto the CM. ISS-028 (battery gauge drift) is a firmware-calibration patch candidate; closure by DVT is optimistic without EE correlation data. ISS-032 (touchscreen false wakes in high-humidity) needs sensor-threshold tuning — firmware-only mitigation possible but must be validated at PRT.

2. **OTA path isn’t DVT-gating, but field beta is June-adjacent.** If we’re shipping DVT units to beta sites in September, the secure-update pipeline (signed images, rollback partition, canary-wave logic) must be tested end-to-end *before* beta ship. Right now that’s not on the PRT plan. We’ll need a firmware-QA gate added.

3. **Diagnostics completeness.** RMA cannot distinguish battery from PMIC from SW hang without structured fault codes in the watchdog dump. ISS-025 (random reboots) stays open until we log root-cause breadcrumbs. I’ll write the fault-code spec for FA handoff — $0 action, high leverage.

**Numbers:** EVT 78% → DVT target 88%; field uptime 99.1% vs 99.5% target; zero OTA test cycles logged.

**Recommendation:** Add firmware health-dump diag to DVT build, define OTA smoke-test gate before beta, and resolve ISS-025/028 with structured fault coding before ramp — all $0, all de-risk schedule.

**Cost re-tag (per new directive):** All three actions above are **$0 committed-now** — no trigger needed. The CM standby hold for provisioning debug support can shift to **trigger-based** (trigger: EVT-level yield pattern repeats in DVT first 24h; cost-if-fired $4.2k). No quality gate weakened. 06/22 and 08/18 unaffected.

**Brain references:** products.md (AMG100, AMGD10 status), state.md (growth stage).

#### [[system-architecture]]

## System Architecture take

**The decision at stake:** The AMG-100 platform architecture is locked — this DVT isn't about architecture exploration, it's about execution integrity. The real architectural question is whether we're inadvertently baking in a single-source dependency that will haunt AMGD10 dock and any Gen 4 follow-on.

**My team flags 3 items:**

1. **BrightPath single-site risk (R-09) is architectural, not just supply chain.** If we don't qualify a second MCU/PMIC fab site now, it becomes a platform constraint for AMGD10 and the next tablet. DVT is when we lock the BOM for cert — after 08/18, changing silicon means re-cert. **Recommendation:** Authorize second-source qualification now ($12k committed, 4-week lead). Cite: Products.md AMGD10 shares AMG-100 compute architecture.

2. **eMMC dual-source is on-track but incomplete.** The FW abstraction layer was scoped for one NAND geometry. If the second source uses different page/block sizing, we're introducing a latent field-failure mode (ISS-019). **$0 action:** Require FW team to document NAND abstraction spec before DVT build — no hardware cost, pure risk reduction. Cite: Brain state=growth, this becomes a platform asset.

3. **Antenna rework (ISS-014) — 3 days buffer is tight but acceptable.** The architectural bet we made on trace antenna vs. chip antenna was correct for cost, but the tuning window is narrow. **Recommendation:** Keep the courier expedite as trigger-based (fire if ETA slips past 06/17). No committed spend needed — 06/16 ETA has been holding.

**Explicit confirmation:** None of these actions weaken PRT coverage, dual-source rule, PCI/EMV cert rigor, or battery 8D closure. Quality gates remain intact.

---

**Re-cost per Department Head directive (06/15):**

| Action | Type | Committed $ | Expected $ |
|--------|------|-------------|------------|
| BrightPath 2nd source qual | Committed-now | $12,000 | $12,000 |
| FW NAND abstraction spec | $0 (free) | $0 | $0 |
| RF engineer documentation + contractor search | $0 (free) | $0 | $0 |
| Antenna courier expedite | Trigger-based (ETA slips past 06/17) | $0 | $4,500 (est. 30% probability = $1,350 expected) |
| Tet pre-build inventory | → Move to capital line, not contingency | $0 | $0 |
| CM build standby hold | Trigger-based (parts missing at 06/20) | $0 | $8,000 (est. 20% probability = $1,600 expected) |

**Totals:** Committed cash = $12,000. Expected cash = $14,950.  
**Savings vs. prior plan:** ~$18,000 removed or converted to trigger-based.

**06/22 and 08/18 cert path confirm:** Unaffected. BrightPath qual runs parallel, not on critical path.

**Quality gate confirm:** Second-source qual *strengthens* dual-source rule; FW spec closes ISS-019 properly; no gate weakened.

### Department synthesis

## Engineering position

The AMG-100 DVT build on 06/22 is achievable but fragile — three business days of buffer on the antenna rework parts (ISS-014) is our single-point schedule risk. The mechanical, electrical, and system architecture teams agree: if that 06/16 shipment slips, we burn the cert window. My department’s stance is **protect the 06/22 DVT slot and 08/18 cert deadline above all else, using the minimum committed cash to do it.** We have alignment across teams on the risk ranking, but meaningful disagreement on where to spend.

**Team signals:**

- **ME team** raised the loudest flag — the mid-frame antenna rework is mechanically irreversible after 06/16. Tool rework lead time is 18–21 days in Shenzhen. If we fail drop test post-rework, they recommend fixing via gasket durometer or assembly torque, not tool re-cut. I endorse this constraint. Thermal margin (8°C to EMV shutdown) is real but manageable with a thermocouple in DVT PRT units — $0 action, per ME team.

- **EE team** insists ISS-014 closure requires measured VSWR/efficiency data, not a factory sign-off. They also want $12k committed now for CM test-fixture validation and board bring-up lab pre-stage. Per EE team, this is the only way to prevent a 3-week debug stall after 06/22. I agree: this is base-workstream readiness, not a discretionary expedite. **Disagreement:** System architecture recommends the $12k go to BrightPath second-source qualification instead. My call — both are necessary, but the bring-up pre-stage protects 06/22 directly. BrightPath second-source qual can run parallel without threatening the critical path. Per system architecture’s own confirmation, it’s not on the critical path.

- **FW team** raised three $0 actions that materially de-risk DVT and beta: firmware health-dump diagnostics in the DVT build, structured fault codes for ISS-025/028, and an OTA smoke-test gate before beta ship. Per FW team, these cost nothing and prevent triage chaos at the CM. I fully support adding these to the plan.

- **System architecture** correctly flags the eMMC NAND abstraction gap (ISS-019) and the single-RF-engineer bus factor (R-09). The FW NAND abstraction spec is a $0 action and must close before DVT build. The RF documentation one-pager + contractor search is also $0 and addresses R-09 without committed spend.

## Risks (ranked, with owners)

1. **ISS-014 antenna parts ETA slip past 06/17** — blocks DVT build, delays cert. Owner: EE team (tuning) + ME team (mechanical integration). Mitigation: trigger-based DG courier if ETA moves.
2. **ISS-021 drop test failure on reworked mid-frame** — could force tool re-cut, missing cert. Owner: ME team. Mitigation: 48-hr drop test on first rework parts; fix with gasket/torque, not tool steel.
3. **ISS-028 battery gauge drift + ISS-025 random reboots** — field uptime below 99.5% target if unresolved. Owner: FW team (fault coding) + EE team (correlation data).
4. **R-09 single RF engineer bus factor** — no backup if engineer is unavailable during tuning. Owner: System architecture (contractor search). Mitigation: $0 documentation + contractor pipeline.
5. **eMMC dual-source NAND geometry mismatch (ISS-019)** — latent field failure if abstraction layer isn’t validated. Owner: FW team (NAND abstraction spec) + EE team (validation).

## Recommendation

| Action | Type | Committed $ | Expected $ | Owner |
|--------|------|-------------|------------|-------|
| CM test-fixture validation + bring-up pre-stage | Committed-now | $12,000 | $12,000 | EE team |
| Antenna DG courier expedite | Trigger-based (ETA slips past 06/17) | $0 | $960 (30% × $3,200) | EE team |
| CM build standby hold | Trigger-based (EVT yield pattern repeats in DVT first 24h) | $0 | $840 (20% × $4,200) | FW team |
| RF documentation + contractor search (R-09) | $0 (free) | $0 | $0 | System architecture |
| FW NAND abstraction spec (ISS-019) | $0 (free) | $0 | $0 | FW team |
| FW health-dump diag + fault codes (ISS-025/028) | $0 (free) | $0 | $0 | FW team |
| Thermocouple in DVT PRT near EMV | $0 (free) | $0 | $0 | ME team |
| BrightPath second-source qual | Committed-now (parallel, non-critical-path) | $12,000 | $12,000 | System architecture |
| Drop test on first rework parts (48-hr turnaround) | Committed-now | $0 (in plan) | $0 | ME team |
| Tet/BrightPath pre-build inventory | → Move to capital line, not contingency | $0 | $0 | NPI PM |

**Totals:** Committed cash = $24,000. Expected cash = $25,800.

**Confirmations:**
- 06/22 DVT build protected: bring-up pre-stage and trigger-based courier cover the antenna buffer.
- 08/18 cert path unaffected: no action alters certification sequencing.
- No quality gate weakened: second-source qualification strengthens dual-source rule; FW diag adds PRT coverage; drop test and thermocouple add mechanical validation.
- Savings vs. prior plan: ~$18,000 removed or converted to trigger-based (per Department Head directive).
- Per ME team recommendation: lock mid-frame tool geometry at 06/16 — no further tool re-cuts. Fix any drop test issues with non-tooling adjustments.

**Brain references:** products.md (AMG-100 DVT status, AMGD10 dock architecture), budget-tracker ($872k spent of $2.0M, $111.6k contingency), open-issues (ISS-014, ISS-019, ISS-021, ISS-025, ISS-028), prt-plan (section 3.2 drop test), mtbf-prediction (thermal margins, 62k h MTBF), risk-register (R-01, R-09).

## [[01-Departments/02-npi-program-management/index|02-npi-program-management]]

### Team inputs

#### [[hardware-pm]]

From: Hardware PM
To: NPI PM Manager
Subject: AMG-100 DVT Readiness & Cost-Optimized Recovery Plan

**Program Take:** DVT is 11 days out, and we have a 3-day buffer on a critical path part (antenna, ETA 06/16 per `04-Projects/Project-AMG/risk-register`). This is a real schedule risk with zero slack. EVT yield was 78% and we're targeting 88% for DVT, but open issues like the battery 8D (ISS-030) still at D6 and single-source RF risk (R-09) aren't closed. The 08/18 cert gate is hard and drives everything.

**My Team's Top 3 Flags:**

1.  **Schedule risk on antenna (ISS-014):** The 3-day buffer before the 06/22 build is unacceptable. We can't commit the full DG courier cost now. We make it **trigger-based**: authorize only if the supplier misses the 06/16 ETA. This is the single best point to protect 06/22 without burning cash.
2.  **Risk R-09 (Single RF Engineer):** This is a bus-factor of one. The **$0 action** here is to immediately task the engineer with creating a "hit-by-a-bus" documentation file this week. We pair this with a contractor search, but the immediate documentation is a no-cost schedule protector.
3.  **Tet Pre-build Capital (budget):** Reclassifying the Tet pre-build inventory as recoverable working capital per the directive immediately frees up $15k in the contingency line, resolving that reallocation problem and clarifying our true risk posture.

**One-Line Recommendation:** Protect the 06/22 build with trigger-based expedite options and $0 documentation actions, and reclassify pre-build inventory to remove pressure from the program contingency without touching a single quality gate.

#### [[certification]]

## Cert Take

**Matrix State:**
- **AMG-100**: No current certifications. FCC, UL, PCI PTS, EMVCo Level 1/2 all required before MP. FCC lab selected, PCI PTS pre-assessment scheduled 07/06. No certified product exists yet — we're building from zero.
- **TS-90**: All certs active, no expirations threatening AMG program.
- **Gap**: The 08/18 cert critical path has **zero slack** and sits entirely post-DVT. Any DVT slip directly consumes cert margin.

**Schedule Risk from Cert Perspective:**
The PCI PTS pre-assessment on 07/06 runs 14 days after DVT build. If DVT units aren't identical to what the lab sees, we invalidate pre-assessment findings and restart. The antenna rework (ISS-014, parts ETA 06/16) is a cert-triggering change — any RF path alteration requires FCC retest and potentially impacts EMVCo contactless performance.

**Budget Re-cost Specifics:**
1. **ISS-014 antenna rework**: Must be committed-now for DVT. The $3k DG courier on antenna samples IS a cert-protection expense — three days buffer lets us verify RF performance before locking DVT config. **Committed-now, $3k.**

2. **Pre-stage labor for DVT build**: Can be **trigger-based**. Pre-stage only if antenna parts miss 06/16. Probability ~20%. Expected cost: $5k × 0.2 = $1k. Committed cash: $0.

3. **BrightPath/Tet pre-build inventory**: Agree — this is recoverable working capital, not NRE burn. Move the $15k off contingency to a capital line. No cert impact.

**Numbers:**
- FCC lab queue: 8 weeks typical, we've reserved 6 weeks starting 08/18
- PCI PTS full evaluation: 12-16 weeks after pre-assessment
- EMVCo Level 1: 8 weeks (contactless testing)
- **Total cert spend to date**: $0 of $300k cert budget allocated (labs not yet committed)

**Critical Dependencies:**
- R-01 (PCI PTS pre-assessment date 07/06) drives entire payment cert chain
- R-09 (single RF engineer) is a $0 fix waiting to happen — documentation and captured knowledge prevent cert stalls if they leave
- BOM changes from ISS-019, ISS-025, ISS-031 must each get a cert-impact verdict BEFORE ECO approval

**Recommendation:** Protect the 07/06 PCI pre-assessment date by freezing the DVT RF and payment subsystem config after 06/22 build — any subsequent antenna or NFC matching network change is a cert reset event. The $3k expedite on antenna samples is the cheapest insurance against slipping the entire cert critical path.

**Brain references:** laws.md (FCC, UL, PCI PTS, EMVCo entry), products.md (AMG-100 RF/payment content requiring certs), strategy.md (US casual dining = PCI mandatory for payment devices).

#### [[bom-eco-plm]]

**BOM/ECO take:** Pipeline is stable for TS-90 MP but fragile for AMG-100 DVT. The ISS-014 antenna rework parts are the critical path — 3-day buffer before DVT build. If those parts miss 06/16, we face a revision-control nightmare: factories may build with unapproved pre-rework units to hold the line, creating an undispositioned stock problem we’ll spend weeks untangling.

**Numbers:**
- ISS-014 rework parts: committed-now courier from DG ($2,800 committed, not trigger-based — 3 days is no slack)
- Tet pre-build inventory: $15k recoverable working capital, not contingency burn (Brain: ramp-plan section); move to separate capital line
- EVT yield 78% → DVT 88% path: $0 action — tighten CM first-pass yield gates now, no new tooling

**Risk alert:** Single RF engineer (R-09) is a PLM bus-factor. If they’re out during ECO processing, antenna rework dispositions stall. $0 fix: mandate documentation file by 06/16, start contractor search now.

**Recommendation:** Commit only the DG courier now; shift Tet pre-build to capital line; protect DVT cut-in with explicit serial-number effectivity for rework parts to avoid undispositioned builds.

**Brain references:** products.md (AMG100 status), budget.md (contingency 111.6k), state.md (DVT stage).

#### [[launch-readiness]]

## Launch Readiness — AMG-100 Readiness Snapshot

**Readiness take:** Conditional go for DVT, not yet ready for production ramp. Three items need immediate attention: RMA/depot process undefined (no owner), beta trial success criteria not locked, and packaging/label cert artwork not released.

**Numbers:**
- DVT build: 06/22 (11 days). Buffer on antenna rework parts: 3 days (tight but workable).
- Cert critical path: zero slack after 08/18. FCC/UL/PCI PTS pre-assessment on 07/06 must hold.
- Depot readiness: no confirmed spares allocation, RMA lane not open, deployment docs absent from ramp plan.
- Budget: $872k spent of $2.0M. Launch readiness line items (spares, labels, RMA setup) not yet committed.

**What we must flag:**

1. **Spares and RMA lane have no owner or trigger date.** The factory ramp plan references Tet pre-build and BrightPath inventory, but nobody has sized the initial depot spares pool or confirmed RMA processes will be live before first customer ship. This is a gate violation waiting to happen. Owner: needs assignment from Service Ops. Cost: minimal to define now, cost of no-action is field failure response collapse.

2. **Beta trial success criteria for 99.5% uptime.** The alpha trial at 99.1% missed target. The beta trial (Sept) must have written, signed-off pass/fail criteria tied to uptime, MTBF, and RMA turnaround — not just "we'll review the data." Without this, the ramp gate is unenforceable. Zero cost to lock criteria now.

3. **Packaging and label art not released.** Cert team confirms FCC/UL marks are approved, but the physical label artwork and carton markings (lithium battery transport, HTS codes, serialization barcode spec) are not signed off. Discovery at first shipment = customs hold or rejection. This is a committed-now action ($0, just approval cycle time).

**Recommendation:** Open the RMA lane and lock beta criteria within 7 days — these are free actions that prevent field launch failures; no budget commitment required, just assignment and sign-off.

**Brain references:** `products.md` (AMG-100 — status DVT, no service artifacts referenced); `state.md` (growth phase — service infrastructure must scale before launch, not after).

#### [[sourcing-buyer]]

## Sourcing take

We’re 11 days from DVT and supply is the tightest link I see. Two BOM items are red: the antenna-flex rework parts (ISS-014, ETA 06/16 leaving 3-day buffer) and the eMMC dual-source — still “in flight,” not qualified, not on a PO. A 3-day gap on the flex means any hiccup on 06/16 pushes the build to 06/23 or worse. Single-site BrightPath and single RF engineer (bus-factor 1, not a sourcing issue but correlates to supply risk) need documenting. Tet pre-build inventory is sitting — that’s capital, not contingency, and should be right-sized (budget.md, contingency $111.6k).

### Numbers
- **Antenna flex ETA risk:** 3 days buffer; expedite via DG courier adds $2.3k committed, drops transit to 1 day.
- **eMMC dual-source:** qualification still open. Worst case — broker buy for 500 pcs at $9.80/ea vs. contracted $6.40, adds ~$1,700 + $1.5k authenticity testing (X-ray, decap) → ~$3.2k exposure.
- **Tet pre-build:** $15k capital, not contingency; move to separate capex line frees budget.md contingency from false pressure.

### Recommendation
Commit DG courier on antenna flex now to lock 06/22 — cheapest insurance on the board (products.md, AMG-100 DVT). Move eMMC qualification to trigger-based (broker + test only if supplier fails 06/18 delivery confirmation). Reclassify Tet pre-build as recoverable capital, not program contingency — no cut, just correct accounting.

**Brain references:** products.md (AMG-100 BOM), budget.md ($111.6k contingency, $1,978k base), schedule risk (ISS-014).

**Tagging actions:**
- **Committed-now:** DG courier on flex rework parts — $2.3k.
- **Trigger-based (trigger + cost-if-fired):** eMMC broker buy + authenticity test — trigger: supplier ETA misses 06/18; cost if fired: $3.2k.
- **$0 action:** RF engineer documents dual-source qualification workflow, contractor search initiated — removes bus-factor risk at no cost, no gate weakened.

**Totals:** committed cash = $2.3k; expected cash = $2.3k + ($3.2k × 0.30 probability) = ~$3.26k. DVT 06/22 and 08/18 cert path unaffected. No quality gate weakened — PRT coverage, dual-source rule, PCI rigor intact.

#### [[odm-program-mgmt]]

## ODM Program Management — Program Review with Re-Cost (06/15/2026)

**Factory take:** DVT build on 06/22 is tight — only 3-day buffer on antenna rework parts (ETA 06/16). BrightPath is committed to the slot but has flagged that any material miss past 06/19 will push us into their next available line window (07/02). Single-site risk is real — BrightPath is our only DVT/PVT capable line for AMG-100.

**Numbers:**
- DVT slot: 06/22–06/28, 150 units committed, factory ready
- Antenna part ETA: 06/16 (ISS-014) — 3 business-day buffer
- EVT yield: 78% → DVT target 88% (gap: soldering consistency on Type-C connector — ISS-027)
- Tet pre-build: $15k in contingency today — this should be recoverable working capital, not NRE burn
- BrightPath single-site exposure: no backup line qualified for AMG-100 until PVT

**Recommendations (re-costed per 06/15 directive):**

1. **Antenna parts — trigger-based air freight ($1.2k committed-if-fired).** Trigger: supplier ETA slips past 06/17. Not committed now. Expected cash: $0.3k (25% probability). Protects 06/22 without upfront spend.

2. **CM build-team standby hold ($4.5k) — remove.** BrightPath confirms the 06/22 slot is held without payment. Free action: send written slot confirmation with escalation path if material is late. Saves $4.5k committed.

3. **Tet pre-build inventory ($15k) — move to capital line.** This is recoverable working capital tied to ramp demand, not program contingency. Removing it from the $111.6k contingency frees that margin for true risk items. Confirmed per Department Head directive.

4. **RF engineer bus-factor (R-09) — $0 action first.** Document RF matching procedures and tuning parameters in a controlled file this week. Parallel: post contractor req to RF engineering firms. No paid retainer needed yet. Removes the $8k expedite retainer from plan.

5. **Type-C connector yield (ISS-027) — committed-now $3.2k.** BrightPath rework station setup and operator training must happen before DVT. This is base workstream, not a de-risk add. Keeps DVT 88% yield target on path.

6. **eMMC dual-source qual — no cost change.** Already in base plan. Samples due 06/20. Confirm BrightPath has alternate BOM loaded for DVT units if second source clears in time.

**Committed-cash total (new de-risk items):** $3.2k  
**Expected-cash total (incl. trigger-based):** $3.5k  
**06/22 and 08/18 cert path:** Unaffected  
**Quality gates:** All intact — no PRT coverage reductions, no source waivers, no cert shortcuts

**Brain references:** products.md (AMG100 DVT status), strategy.md (volume outlook requiring dual-source and multi-site readiness), budget.md ($2.0M program budget, $111.6k contingency)

### Department synthesis

**Program position:** AMG-100 stands 11 days from DVT build (06/22) with a 3-day buffer on antenna rework parts (ISS-014) and a hard certification gate at 08/18 with zero slack. The program office position is clear: we hold 06/22 and 08/18 without weakening any quality gate, while reducing committed cash per the Department Head's 06/15 directive.

**Team signals:**
- **Hardware PM** flags antenna schedule risk (ISS-014) as trigger-based expedite, wants $0 RF documentation, and reclassification of Tet pre-build
- **Certification** says antenna rework is a cert-triggering change — $3k DG courier IS cert protection, not a discretionary expedite. PCI PTS pre-assessment 07/06 sits 14 days post-DVT; any DVT config change after 06/22 is a cert reset event
- **BOM/ECO** warns of undispositioned factory builds if ISS-014 parts miss — revision-control nightmare requiring serial-number effectivity lock
- **Launch Readiness** signals three $0 gaps: no RMA/depot owner, untethered beta success criteria, unreleased label/packaging artwork
- **Sourcing** prices DG courier at $2.3k committed, eMMC broker exposure at $3.2k (30% probability), confirms Tet reclassification
- **ODM Program Mgmt** confirms BrightPath single-site exposure — next available slot 07/02 if 06/19 material miss — and prices Type-C rework station at $3.2k committed

**Disagreements resolved:**
- Certification vs. Hardware PM on antenna expedite: Certification is right. The $2.8-3k DG courier on ISS-014 parts is a cert-protection expense, not a schedule luxury. If those parts miss and DVT config shifts, we invalidate the 07/06 PCI pre-assessment and restart — a 12-16 week hit on a path with zero slack. **Committed-now.** Per Certification and BOM/ECO.
- ODM vs. Sourcing on Type-C yield: Both agree the $3.2k rework station is base workstream, not de-risk. **Committed-now.**

**Critical path:** Antenna rework parts (ISS-014) → DVT build 06/22 → PCI PTS pre-assessment 07/06 → cert complete 08/18. The binding constraint is the antenna parts ETA 06/16 with only 3 business-day buffer. No slack after 08/18 (per `products.md` AMG-100 status).

**Recommendation (re-costed per 06/15 directive):**

| Action | Type | Cost | Owner |
|--------|------|------|-------|
| DG courier on ISS-014 antenna parts | Committed-now | $2.8k | Sourcing |
| Type-C rework station + operator training | Committed-now | $3.2k | ODM PM |
| eMMC broker buy + authenticity test | Trigger-based (trigger: supplier misses 06/18; 30% probability) | Expected $960 | Sourcing |
| RF engineer documentation file + contractor search | $0 action | $0 | Hardware PM |
| Tet pre-build reclassification to capital line | $0 action (removes $15k from contingency) | $0 | BOM/ECO |
| RMA/depot owner assignment + beta criteria lock | $0 action (due within 7 days) | $0 | Launch Readiness → Service Ops |
| Packaging/label artwork release | $0 action (approval cycle only) | $0 | Launch Readiness + Certification |
| CM build-team standby hold | Removed from plan per ODM confirmation slot held without payment | $0 savings | ODM PM |

**Committed cash:** $6.0k  
**Expected cash:** $6.96k  
**Contingency freed:** $15k (Tet reclassification)  
**06/22 and 08/18 cert path:** Unaffected  
**Quality gates:** All intact — no PRT coverage reduction, no single-source waiver, no cert shortcut, serial-number effectivity locked for ISS-014 cut-in per BOM/ECO

**Brain references:** `products.md` (AMG-100 DVT status, cert requirements), `budget.md` ($111.6k contingency, $1,978k base), `strategy.md` (PCI mandatory for payment devices, 99.5% uptime target), `state.md` (growth phase — service infrastructure must scale before launch).

## [[01-Departments/03-quality-reliability/index|03-quality-reliability]]

### Team inputs

#### [[qa-system]]

## QA System take:

The spend-to-protect-speed plan has a document-control problem that will bite us later. The QMS doesn't yet reflect the 06/22 DVT build — no controlled build procedure, inspection criteria, or acceptance thresholds for the antenna rework parts arriving 06/16. If we build on 06/22 without those, we're producing evidence we can't defend in certification. The audit trail starts cold.

PCI PTS pre-assessment 07/06 has zero slack — any evidence that isn't ready means a finding that cascades into the 08/18 cert path. I see no evidence-retention plan tied to ISS-014 (antenna rework disposition) or ISS-019 (yield investigation). Those records are cert-audit gold — if they're not controlled now, they're fiction later.

**Numbers:** 
- EVT yield 78% → DVT 88% target: 10-point gap without a controlled corrective-action trail linking ISS-019/021/025 to process changes. Repeat findings cost 3x more to close than first-instance.
- Battery 8D at D6: not yet a repeat, but if closure evidence isn't retained, expect recurrence in alpha.
- PRT plan exists but I can't see version control or review dates — checked this morning.

**Recommendation:** Before 06/22, lock the DVT build procedure, antenna-rework disposition, and yield-corrective-action evidence package under document control. Free action. No cost. Protects cert audit trail. 🛡️ Brain: laws.md (PCI/EMV cert rigor), state.md (DVT stage).

#### [[qc-inspection]]

**Inspection take:** EVT yield benchmark is set. DVT is unproven — we have no in-control data yet, and the build is in 11 days. Supply chain risk is real — our eMMC dual-source is still open, BrightPath is single-site. My tolerance for escapes into the factory is nil.

**Numbers:**
- **EVT yield:** 78% — reflects immature process. DVT acceptance plan is tightened: **Normal-to-Tightened switching** will trigger if the first DVT lot falls below 95% first-pass yield.
- **Line-reject limit (AQL):** Critical defects (safety, PCI, antenna) — we sample at c=0. Non-critical cosmetic/haptics — we can negotiate AQL 0.65 if yields support it.
- **TS-90 DPPM (for context):** Incoming dock rate is 1200 DPPM (cosmetic dominant).

**Recommendation:** Do not relax a single inspection criterion to save pre-build time. The 3-day buffer for antenna rework is a trap — if parts land late, the build *must* push, not the inspection gate. We inspect to the DVT checklist or we ship risk. I'll brief the [[01-Departments/03-quality-reliability/agents/qa-system|QA System lead]] on the DVT checklist finalization today — photo-anchored criteria, no "looks bad."

**Brain references:** `products.md` (DVT readiness AMG-100), `state.md` (growth — MP process not yet validated).

#### [[validation-reliability]]

**Validation take:** DVT readiness with <3-day buffer on antenna rework parts (ISS-014) is a red condition — we cannot validate antenna-to-PCI coexistence with a hard 07/06 PTS pre-assessment (R-01) if parts slip. ISS-019/021/023/025/027/028/030/031/032 closure plans lack DVT test coverage mapping — 4 of 8 issues affect touch/power paths that EVT at 78% yield didn't fully stress. PRT plan covers 12 of 14 failure modes; the two gaps (dock pogo-cycle fatigue, battery swell at 45°C edge) need HALT inserts before DVT exit.

**Numbers:** MTBF 62k h vs. 2.0% AFR target = 53k h required — passes on point estimate, but the 90% lower confidence bound at current sample (n=18 EVT units × 1,200 h) is 28k h. Alpha uptime 99.1% vs. 99.5% target; the 0.4% gap traces to 3 Wi-Fi roam-drop events — not a tablet defect but a system-reliability KPI we own. Battery 8D at D6 — D5 root cause confirmed (charge taper at high SOC), but D7 validation plan only samples 20 cells, which won't resolve a 1% infant-mortality rate.

**Recommendation:** Hold DVT entry gate until antenna rework parts are in-hand AND the two HALT inserts are scoped — commit the $6k HALT cost now, move antenna expedite to trigger-based (authorize courier only if tracking shows ETA slip past 06/17).

**Committed-now:** HALT inserts ($6k). **Trigger-based:** DG courier ($4.2k, trigger = parts not shipped by 06/17 5pm SGT); CM standby hold ($12k, trigger = antenna fit-check fails at IQC 06/16). **Expected cash:** $6k + (0.3 × $4.2k) + (0.15 × $12k) = $9.1k committed, $6k committed-now. Tet/BrightPath pre-build moves to capital line — removes $15k from contingency. 06/22 and 08/18 cert path held. No quality gate weakened.

**Brain references:** products.md (AMG-100 DVT status), state.md (growth phase, field return context)

#### [[firmware-qa]]

# FW QA Perspective

## What We Must Flag

**1. Alpha trial uptime gap (99.1% vs 99.5% target) is the field-incident-in-waiting.**
We didn't hit the number in controlled alpha with hand-held units. Beta at scale in September — without root cause closed — means we ship the gap to 300+ locations. Battery 8D at D6 means we're still in containment, not permanent fix. If this is a firmware corner case (brownout recovery, dock/undock state machine, OTA resume-after-power-loss), it's on us to find it before DVT.

**2. No mention of update-path testing from TS-90 fleet versions.**
If AMG-100 shares any OTA infrastructure, bootloader, or comms stack with the Gen 2 TS-90 install base (per products.md — TS-90 in MP, TS-90R in RMA pool), we need an explicit regression gate. Field escapes happen when QA tests only the new device's clean path.

**3. DVT build at 78% yield entering test tells us we're gating firmware on marginal hardware.**
We'll burn test cycles chasing hardware ghosts instead of finding firmware defects. PRT coverage must account for this noise.

## Recommendation
Close alpha uptime root cause to code commit before DVT build freeze. Begin update-path regression matrix now — not during DVT.

#### [[field-quality-rma-fa]]

We’ve triangulated the brief with product and state data from the Brain. Here’s our field-quality take, focused on risks that can break the 99.5% uptime target and what to do about it now — before DVT bakes in field defects.

**Field quality take:** Battery lifecycle failure is the #1 field-risk for AMG-100. The 8D at D6 means root cause unconfirmed — DVT units will ship without validated corrective action. Second, single-supplier eMMC (ISS-019) is a ticking field-population problem; dual-source must be locked before DVT. Third, EVT yield at 78% with target 88% for DVT signals process immaturity that will drive early-life returns.

**Numbers:**
- MTBF 62k h vs 2.0% AFR target — this is already borderline given harsh-use environment; any slip on battery fix pushes it over.
- Alpha uptime 99.1% vs 99.5% target — gap = ~35 hrs/unit/year excess downtime; battery-related resets are the leading cause per field-trial-report.
- TS-90 fleet return rate (Gen 2) sits at 3.2% AFR; assuming AMG-100 similar, 50,000-unit install base means 1,600 RMAs/year at $145/unit refurb cost = $232k burden — battery alone could drive half.

**Recommendation:**
1. **Battery 8D fast-track to D8 (verify fix) before DVT build** — freeze DVT battery firmware/config only after bench validation passes ([[repair]] to run accelerated cycle test on 20 units; [[validation-reliability]] to confirm mechanism).
2. **eMMC dual-source qualification** — second source must ship in DVT units, not MP; single-source is a fleet-level recall risk ([[supplier-quality]] to drive SCAR for any qualification gap).
3. **Containment on process yield** — mandate 100% functional test at DVT with burn-in on first 200 units; capture early-life failures before they hit beta sites ([[msq-manager]] to own).

**Brain references:** products.md (TS-90 fleet size for rate context), state.md (99.5% uptime goal vs 99.1% current). No action weakens a quality gate — battery validation accelerates within existing PRT coverage, eMMC dual-source strengthens the qualified-sources rule. Cost: trigger-based only — authorize accelerated battery test only if D6 milestone slips past 06/14; otherwise use existing PRT resources.

### Department synthesis

## Quality & Reliability Department Position

**Quality position:** AMG-100 DVT build 06/22 carries unacceptable quality risk in current state. Three inviolable gates are soft — battery validation, antenna coexistence, and document control for cert audit trail. I am not issuing a hold yet, but I am one trigger away.

Per Field Quality RMA/FA, battery 8D at D6 means root cause unconfirmed — DVT units will ship without validated corrective action. Per Validation, antenna rework parts ETA 06/16 leaves 3 days buffer for coexistence validation before 07/06 PCI pre-assessment. Per QA System, DVT build procedure isn’t under document control — zero audit trail for certification evidence.

**Team signals (disagreements named):**
- **QC Inspection** flags eMMC single-source as fleet-level recall risk; FW QA adds that we’re burning test cycles on marginal hardware (78% EVT yield entering DVT)
- **Validation** wants HALT inserts committed now ($6k) — I agree: those two failure modes (dock pogo-cycle fatigue, battery swell at 45°C) aren’t covered by PRT and EVT stress didn’t touch them
- **QA System** and **QC Inspection** both flag document control — free action, no cost, protects cert path. No disagreement here
- **Field Quality** wants battery 8D fast-tracked to D8 before DVT; **Validation** notes D7 plan only samples 20 cells — insufficient for 1% infant-mortality. I side with Field Quality: accelerate within existing PRT resources, don’t weaken the gate

**Risk:** Proceeding to 06/22 DVT build without these closures means:
1. Battery field-return rate could match TS-90’s 3.2% AFR — at 50k units, that’s $232k/year in RMA burden, half from battery alone
2. Antenna coexistence failure discovered after 06/22 cascades into 07/06 PCI pre-assessment — one finding delays 08/18 cert, no slack
3. Uncontrolled DVT evidence means PCI cert auditor rejects the build record — repeat audit costs 3x more to close

**Recommendation (re-costed per Department Head directive):**

**Committed-now ($6k total):**
- **HALT inserts** for dock pogo-cycle fatigue and battery swell at 45°C — $6k, Validation owns, complete before DVT exit. This closes two PRT gaps. **(Committed-now)**

**Trigger-based ($0 committed, $6.3k expected):**
- **DG courier expedite** for antenna rework parts — $4.2k, authorize only if supplier tracking shows ETA slip past 06/17 5pm SGT. Probability ~30% = $1.3k expected. **(Trigger-based)**
- **CM standby hold** — $12k, authorize only if antenna fit-check fails at IQC 06/16. Probability ~15% = $1.8k expected. **(Trigger-based)**

**$0 actions (remove all paid equivalents):**
- **Document control lock** — QA System owns, complete by 06/16. DVT build procedure, antenna rework disposition, yield corrective-action evidence package under version control. Free. Protects 07/06 PCI pre-assessment and 08/18 cert audit trail
- **RF engineer documentation file** — per the single RF engineer bus-factor (R-09), require a documented design rationale and test plan before DVT build. Free. Removes the paid contractor-search item
- **eMMC dual-source qualification** — QC Inspection and Field Quality jointly own; second source must ship in DVT units, not MP. Free action to enforce existing two-qualified-sources rule. Does not require new spend — it’s a sourcing decision
- **Update-path regression matrix** — FW QA owns; test AMG-100 OTA path from TS-90 fleet versions. Free action, prevents field escapes from shared comms stack

**Capital reclassification:**
- **Tet/BrightPath pre-build inventory** — move $15k from program contingency to capital line. This is recoverable working capital, not NRE burn. Removes the contingency-reallocation problem. Confirmed.

**Verification plan:**
- Battery 8D: Field Quality and Validation jointly verify D8 closure with accelerated cycle test using existing PRT resources (no new spend) — must complete before DVT battery firmware/config freeze
- Antenna coexistence: Validation signs off R-01 (PCI PTS pre-assessment readiness) only after parts in-hand and fit-check passed at IQC
- DVT yield: QC Inspection enforces Normal-to-Tightened switching if first DVT lot falls below 95% first-pass yield per tightened acceptance plan

**Committed cash:** $6k. **Expected cash:** $6k + (0.3 × $4.2k) + (0.15 × $12k) = $9.1k.

**Gate confirmation:** No action weakens a quality gate. Battery validation accelerates within existing PRT — no coverage removed. Two-qualified-sources rule enforced — strengthened, not weakened. PCI/EMV cert rigor protected — document control free action hardens the audit trail. 06/22 DVT build and 08/18 cert path unaffected.

**Brain references:** products.md (AMG-100 DVT status, TS-90 fleet for field-rate context); laws.md (PCI/EMV cert rigor per cert-plan); state.md (growth phase, 99.5% uptime goal vs. 99.1% current).

## [[01-Departments/04-mfg-supplier-quality/index|04-mfg-supplier-quality]]

### Team inputs

#### [[odm-quality]]

**ODM quality take:** JDM factory is tracking for DVT but running at the edge — EVT OQC yield was only 78% (touchscreen haze 8%, battery connector seating 5%, dock alignment 3%) and we still have three open 8Ds that haven't reached D5 at the line. ISS-027 (touchscreen cosmetic spec) hasn't been gage R&R'd with the new golden sample, and ISS-028 (OQC sampling plan) shows the factory still pulling from pallet #1 of 5. I won't sign DVT build-readiness until those two are closed with floor evidence.

**Numbers:**
- EVT OQC pass rate: 78% (target 88% DVT, 95% MP)
- Audit findings open: 5 major, 2 minor — oldest 45 days
- ISS-027: golden-sample alignment overdue since 06/01
- ISS-028: OQC sampling bias found 06/08, factory CAPA not submitted
- ISS-025 (battery connector): 8D at D4, rework parts ETA 06/16 — **only 3 days buffer** before DVT start
- ISS-019 (eMMC purge): second-source qualification plan approved but no line-trial date

**Risk flagged:** The antenna rework (ISS-014, parts ETA 06/16) and battery connector rework (ISS-025) converge on the same three days before build. Rework operators are the same crew. If either part arrives late or rework takes longer, DVT slips. Also, Tet pre-build inventory is sitting at $42k — that's capital, not contingency, and should move off your $111.6k as your budget note says.

**Cost view for Department Head's reframe:**
- Factory standby hold for rework crew ($18k): **trigger-based** — authorize only if ETA confirmation on 06/14 shows slip past 06/17. Committed now: $0. Expected: $18k × 30% probability = $5.4k.
- Air-freight backup for connector parts ($8k): **trigger-based** — fire if supplier ETA slips or tracking shows Shanghai departure after 06/16 10:00 CST. Committed now: $0.
- Pre-stage labor expedite ($12k): **trigger-based** — only if rework completion passes 06/19 18:00. Don't commit now.
- OQC sampling plan fix (ISS-028): **$0 action** — floor instruction change and re-training this week. Already in progress.
- Golden-sample alignment (ISS-027): **$0 action** — joint gage R&R with NPI Quality, scheduled 06/13.
- Tet pre-build capital reclass: remove $15k from contingency, no new committed cash.

**Committed-cash total:** $0 new committed (all de-risk items moved to trigger-based).  
**Expected-cash total:** ~$5.4k (only the most probable trigger).  
**06/22 & 08/18 cert path:** Unaffected. Quality gates: strengthened — closing ISS-027/028 before DVT is more rigorous, not less. PRT coverage, dual-source rule, PCI PTS pre-assessment 07/06 all unchanged.

**Recommendation:** Close ISS-027 and ISS-028 with floor evidence by 06/16, move all expedites to trigger-based, and shift Tet pre-build to capital — protects schedule, reduces committed spend to near zero, hardens quality gates.

**Brain references:** products.md (AMG100 status: DVT), factory-yield-evt, open-issues ISS-027/028/025/014.

#### [[supplier-quality]]

**Supplier quality take:** AMG-100 DVT readiness — critical supplier risks at BrightPath (single-site, single RF engineer) and eMMC dual-source qualification not complete.

**Numbers:**
- eMMC dual-source: qualification incomplete; if 2nd source fails FAI, sole-source risk materializes
- BrightPath: single RF engineer (bus-factor R-09), single site
- EVT yield 78% — supplier-related defects must be isolated from assembly issues
- SCAR aging: battery 8D at D6 — closure evidence due before DVT build

**What we must flag:**
1. eMMC 2nd source FAI must pass before DVT — if not, we're on single-source with no documented risk acceptance (violates two-qualified-sources rule). **$0 action:** expedite FAI scheduling now.
2. BrightPath RF engineer single point — any absence during DVT debug or cert testing stops progress. **$0 action:** mandate documentation file + contractor search this week.
3. Battery 8D must reach D8 (verified CAPA, lot-acceptance data) before DVT units ship. SCAR closure on "operator retrained" is unacceptable.

**Recommendation:** Prioritize eMMC FAI completion and RF engineer documentation before any paid expedites; commit no cash until those $0 actions are done. No quality gate weakened.

**Brain references:** products.md (AMG100 DVT status), decisions-log.md (no risk acceptances logged for sole-source).

#### [[manufacturing-engineering]]

**Mfg engineering take:**

*Process readiness for DVT build (06/22) is at medium risk.* We've walked the AMG100/AMGD10 assembly sequence end-to-end. Takt time targeting 12.5 min per unit (30 units/hr line rate) is achievable only if ISS-021 (antenna rework) parts arrive by 06/16 with zero defect on the contact-side — we need 3 days for inline process validation before build start. Any slip at the antenna station cascades to full DVT line stoppage.

**Numbers:**
- **Takt:** 12.5 min/unit (30 uph) — validated on EVT line, no change proposed
- **Capability risk:** ISS-027 (battery connector press-fit) showed Cpk 0.82 at EVT — unacceptable. We need Cpk ≥1.33 before DVT; fixture modification and operator training must verify by 06/19. Without it, yield stays below 80.
- **Changeover cost:** Dock-to-tablet line changeover currently 47 min — acceptable for DVT, but must be under 30 min for MP. Not a gate issue now.

**Buildability flags:**
1. **ISS-021 (antenna rework):** 3-day buffer is tight. We *must* trigger air-freight if ETA slips past 06/17. Design needs DFM confirmation that contact pad geometry doesn't create a tombstone risk at reflow — flag to ME team now.
2. **ISS-027 (press-fit yield):** Fixture revision required. This is a gate — no workaround. Authorize fixture mod today.
3. **ISS-025 (dock alignment):** EVT showed 4% misalignment on pogo-pin contact. Process fix: alignment jig, not design change. We'll validate at line setup 06/20. No cost increase.

**Recommendation:** Commit fixture mod spend for ISS-027 now ($0 NRE — it's a CM tooling mod, $2.5k expedite to tool shop). Make antenna air-freight trigger-based (trigger: ETA past 06/17, cost $3.2k if fired). This protects 06/22 without weakening any quality gate, and keeps $3.2k as expected cost vs committed.

**Brain references:** products.md (AMG100, AMGD10 assemblies), state.md (DVT phase)

#### [[factory-test-yield]]

For MSQ leadership, here's the factory test/yield perspective.

---

**Test/yield take:** EVT 78% FPY is not a production test problem — it’s an EVT coverage gap problem being measured by production test. The yield number is honest; the risk is that DVT adds complexity faster than the test stations can discriminate real failures from fixture artifacts. If DVT FPY comes in below 75% without clear Pareto, DVT build schedule stalls on triage.

**Numbers:** EVT FPY 78% (top fallout: wireless calibration 8%, display uniformity 5%, dock-charging handshake 4%). Retest rate 14% — half of those pass on first retry, indicating station repeatability, not product. No DPPM escapes yet (small population). 88% DVT target is achievable only if calibration limits aren't widened and fixture wear isn't confused with fallout.

**Coverage risk:** DVT test plan adds PCI PTS pre-assessment (R-01) but doesn't yet include dock-charging loop under real cable-impedance conditions — that's where EVT saw the 4% handshake loss. If the dock test at the CM doesn't simulate field cables, we'll build DVT units that pass factory and fail beta.

**Recommendation:** Before DVT build, correlate EVT retest-pass units (pairs) against golden units across stations — if correlation is below 0.92, delay DVT build by 48 hours to re-baseline stations. Cost: two tech days (~$3k). This is trigger-based: fire only if station correlation audit on 06/19 fails threshold. Committed now: zero. Expected cash: $3k × 30% probability = $0.9k. No quality gate weakened.

**Brain references:** `products.md` — AMG-100 DVT status; `state.md` — growth stage, DVT build target 06/22.

### Department synthesis

**MSQ position:** DVT build-readiness is achievable for 06/22, but it’s not secure yet — we have three days of buffer, two open quality gates (ISS-027/028), and supplier risk concentration that can’t be bought down with cash. Committed spend can be driven to near zero while maintaining the schedule, but only if we close the free actions this week and move all expedites to trigger-based authorization. Quality gates remain inviolable.

**Team signals:**
- **ODM Quality** flags ISS-027 (golden-sample alignment) and ISS-028 (OQC sampling bias) as gating for DVT build-readiness. EVT OQC 78% won’t improve without these closed. I agree — floor evidence by 06/16, not a promise.
- **Supplier Quality** raises the BrightPath single-RF-engineer bus factor (R-09) and eMMC dual-source qualification as sole-source risks. Both are $0 actions this week; neither should wait for a paid expedite.
- **Manufacturing Engineering** confirms 12.5-min takt is viable only if ISS-021 (antenna) parts arrive 06/16 and ISS-027 (press-fit) fixture Cpk improves from 0.82 to ≥1.33 before build. Fixture mod is the only committed spend I support ($2.5k tool shop expedite, NRE).
- **Factory Test** wants a station correlation audit before DVT — trigger-based, cost $3k if fired. The risk (fixture artifacts disguised as fallout) is real; 14% retest rate with 50% first-retry pass supports this.

**Numbers:**
- DPPM escapes: zero from EVT (small population), but process capability isn’t proven yet
- EVT FPY: 78% (top fallout: wireless cal 8%, display 5%, dock handshake 4%)
- SCAR aging: battery 8D at D6, closure evidence due before DVT; antenna 8D at D4 with parts ETA 06/16
- Open audit findings: 5 major, 2 minor — oldest 45 days
- Tet pre-build inventory: $42k (working capital, not contingency)

**Recommendation:**
1. **$0 actions this week (before any cash is committed):**
   - Close ISS-027 (golden-sample gage R&R) and ISS-028 (OQC sampling plan fix) with floor evidence — per ODM Quality, due 06/16.
   - Expedite eMMC second-source FAI scheduling; mandate BrightPath RF-engineer documentation file + contractor search — per Supplier Quality.
   - Move Tet/BrightPath pre-build inventory ($15k) off program contingency to a capital line — per budget recost rules.

2. **Committed-now spend (only where $0 action won’t hold 06/22):**
   - ISS-027 press-fit fixture modification: $2.5k tool shop expedite — committed now, per Manufacturing Engineering. Cpk must verify ≥1.33 by 06/19.

3. **Trigger-based items (authorize only if trigger fires):**
   - Air-freight backup for antenna/connector parts: trigger = supplier ETA past 06/17; cost $8k if fired.
   - Factory standby hold for rework crew: trigger = rework completion past 06/19 18:00; cost $18k if fired.
   - Pre-stage labor expedite: trigger = rework past 06/19 18:00; cost $12k if fired.
   - Station correlation audit (Factory Test): trigger = correlation below 0.92 on 06/19 audit; cost $3k if fired.

**Committed-cash total:** $2.5k.  
**Expected-cash total:** ~$9.8k ($2.5k + $5.4k rework standby probability + $0.9k audit probability + $0.8k air-freight probability).  
**06/22 & 08/18 cert path:** Unaffected — all triggers protect schedule without weakening gates.  
**Quality gates:** Strengthened — ISS-027/028 closure before DVT is more rigorous, not less. PRT coverage, dual-source rule, PCI PTS pre-assessment 07/06 all unchanged.

**Brain references:** products.md (AMG100 DVT status), state.md (growth stage, DVT 06/22), decisions-log.md (no risk acceptances logged), budget.md (contingency $111.6k).

## [[01-Departments/05-service-operations/index|05-service-operations]]

### Team inputs

#### [[repair]]

**Repair take:** Current bench — TS-90 fleet RMA volume running 14 units/week, 4.3-day turnaround against 5-day SLA. Yield tracking 82% (just above EVT-level performance). One parts blocker: TS-90 battery kits ETA 06/18 — 22 units in queue will age past SLA if that slips. No AMG-100 units in repair flow yet (pre-DVT), but depot readiness is open.

**Numbers:** Turnaround 4.3 days; yield 82%; cost-per-repair $47.18 (parts + labor avg). Backlog 22 units awaiting battery kits.

**Recommendation:** The AMG-100 DVT build doesn't hit my bench for months — my flag is **depot readiness for beta trial (Sept)**. I need the AMG-100 service manual, spares BOM, and diagnostic flash image by 08/01 to train techs and stock the kanban. Without that, Sept beta RMAs become dead units in a bin, not data points. I'll also flag: if TS-90 battery ETA slips past 06/20, I need authorization to pull from refurb stock to clear the queue and protect fleet uptime SLA. Zero AMG-100 budget impact now — all free actions (manual review, kanban design) in this window.

**Brain references:** products.md (TS-90R refurb pool, AMG-100 DVT status); state.md (growth phase, no AMG RMA volume yet).

#### [[fulfillment]]

**Fulfillment take:** DVT build readiness on 06/22 is tight — antenna rework parts ETA 06/16 leaves only 3 business days buffer. If that slips even 2 days, kitting for 150 DVT units breaks. Currently, no AMG-100 packaging spec or serialization manifest exists in products.md — that’s a risk manifesting at build, not later.

**Numbers:**
- EVT yield: 78% → DVT target 88%; bad units at kitting kill ship accuracy
- Budget: $872k spent of $2.0M; contingency $111.6k remaining
- Alpha uptime: 99.1% vs. 99.5% target — reliability gap directly impacts RMA volume forecasting

**Flagged risks:**
1. **Kitting readiness gap** — No packing spec, no serial-tracking procedure for AMG-100. I cannot commit on-time ship without these locked.
2. **Antenna parts buffer** — ISS-014 (3-day buffer). Recommend trigger-based air freight authorization if supplier ETA slips past 06/17 ($2.8k committed if fired, 30% probability → $840 expected).
3. **CM build-team standby** — Should be trigger-based, not committed now ($0 committed, $4k if fired).

**Recommendation:** Lock AMG-100 packing spec and serialization manifest this week (free action); move CM standby to trigger-based; keep air-freight trigger at 06/17 threshold.

**Brain references:** products.md (no AMG-100 packaging defined), state.md (growth, DVT phase).

#### [[inventory]]

**Inventory take:**
The current state file shows no active inventory tracking for TS-90 (MP) or AMG-100/D10 (DVT). We have no stock records, no spares pools sized, and no warehouse/depot readiness baseline. This is a red flag — we're 11 days from DVT build and have no visibility into parts availability or RMA pool readiness for the alpha trial fleet.

**Numbers:** Accuracy unknown (no records), turns N/A, E&O $ unknown. We can't confirm the $872k spent includes any inventory build for DVT parts or alpha trial spares.

**Recommendation:** Immediately establish inventory records for (1) DVT build parts — all BOM items on-site or in-transit with ETA, (2) alpha trial spares pool sized using MTBF 62k h × 2.0% AFR target × 99.1% current uptime gap, and (3) depot RMA kanban for TS-90R refurbished units serving as bridge stock until AMG-100 ramps.

**Brain references:** products.md — TS-90R is active RMA pool product, no AMG-100 spares structure defined; state.md — "growth" stage with alpha trial deployed, no fleet size specified for spares math.

#### [[deployment-support]]

**Deployment take:** Three sites at risk unless we clear DVT build readiness now.

**Flags for the manager:**

1. **ISS-014 (antenna rework parts ETA 06/16)** gives us only 3 working days before the 06/22 DVT build. If that slips even one day, we blow the build slot. Deployment can’t prep sites without DVT units for beta installs in September — this is a committed-now risk, not trigger-based.

2. **Alpha trial uptime 99.1% vs. 99.5% target** (field-trial-report). That 0.4-point gap on a 62k-h MTBF device means beta sites will see 2–3 extra outages per month per location. We’ll be swapping units in the field before we’ve even finished prepping spares. Depot readiness and ramp gates (ramp-plan) need that gap closed or the beta trial burns the spares pool before MP.

3. **Tet / BrightPath pre-build.** Strategy committed “spares staged before wave 1.” If DVT slips, the pre-build inventory sits as working capital tied up in units we can’t deploy. Right-size it against actual beta demand, move it off contingency, and confirm depot staging dates. (state.md — fleet and current programs.)

**Recommendation:** Lock 06/16 antenna parts ETA with a committed-now expedite; any slip past 06/17 triggers air freight. Confirm beta spares quantities against 99.1% uptime reality — don’t pre-build to fantasy numbers.

**Brain references:** strategy.md (fleet uptime commitments), state.md (fleet/programs), products.md (AMG100 DVT status), ramp-plan (beta Sept gates), field-trial-report (alpha uptime).

#### [[logistics]]

**Logistics take:** DVT schedule has a single-point-of-failure customs entry — AMG-100 contains lithium batteries (UN3480, Class 9 DG). Antenna rework parts arriving 06/16 with just 3 days buffer is a hard logistics risk. If that shipment hits customs hold for DG paperwork deficiency, DVT build start moves right.

**Numbers:**
- Antenna parts inbound: likely air courier ex-Vietnam or ex-China. DG-certified courier (FedEx/IATA Section II) adds ~$1.2k vs. standard air. Transit 48-72h door-to-door. If customs flags UN38.3 test summary missing, add 2-5 days.
- Tet/BrightPath pre-build: treat as recoverable working capital per directive. 500-unit pre-build at $105/unit landed = $52.5k. This is ramp inventory, not contingency. Remove from $111.6k program contingency → separate capital line.
- DVT unit shipments to US test sites: same DG rules apply. Budget $3-5k for compliant outbound, not $1.5k cheapest forwarder.

**Recommendation:** Authorize DG-compliant courier now for antenna parts (committed-now, $1.2k). Shift Tet pre-build to capital line (frees $15k contingency). No air-freight backup needed — conditional trigger "only if tracking shows customs hold by 06/18" saves committed cash.

**Brain references:** products.md (AMG100 battery content), budget.md (contingency $111.6k), laws.md (49 CFR/IATA DG, 19 U.S.C. customs).

### Department synthesis

**Service ops position:** DVT build readiness depends on clearing the antenna parts bottleneck with zero slip — but we can hold 06/22 without committing unnecessary cash. Alpha trial uptime gap (99.1% vs. 99.5%) means beta deployment burns spares faster than planned. Depot readiness for AMG-100 is unfunded preparation work that must start now ($0 actions), or September beta RMAs become dead units.

**Team signals:**
- **Fulfillment** and **Deployment Support** both flag ISS-014 antenna parts ETA 06/16 with only 3 days buffer as the highest DVT schedule risk. Deployment Support calls it "committed-now"; Logistics and I disagree — a trigger-based approach works.
- **Inventory** surfaces a foundational gap: no active stock records for DVT parts or alpha spares. That’s a $0 fix that eliminates guesswork at build kitting.
- **Logistics** correctly identifies the DG lithium battery compliance risk on inbound parts and outbound DVT units. Per Logistics: treat Tet pre-build as recoverable capital, not contingency spend.
- **Repair** flags depot readiness for beta trial (September): without AMG-100 service manual, spares BOM, and diagnostic image by 08/01, we can’t train techs or stock the kanban. All $0 actions in this window.

**Numbers:**
- ISS-014 buffer: 3 business days (06/16 → 06/22)
- RMA turnaround: 4.3 days against 5-day SLA (TS-90 fleet)
- Alpha uptime delta: 0.4 points below target → 2–3 extra field swaps/month/site at beta
- Tet pre-build: $52.5k (500 units × $105 landed) — reclassify as capital, not contingency
- Logistics DG courier: $1.2k committed-now vs. standard air

**Recommendation (cost-optimized, speed-maintained):**

1. **ISS-014 antenna parts: trigger-based air freight** (per Logistics)
   - **Trigger:** DG-compliant courier authorized *now* ($1.2k committed, per Logistics)
   - **Conditional trigger:** Authorize air-freight backup *only if* supplier ETA slips past 06/17 OR customs hold confirmed by 06/18 ($2.8k if fired, 30% probability = $840 expected)
   - **Owner:** Fulfillment + Logistics
   - **Cost delta:** $1,200 committed, $840 expected

2. **CM build-team standby: convert to trigger-based** (per Fulfillment)
   - **Trigger:** Activate only if DVT build start confirmed by 06/20 ($4k if fired, 30% probability = $1,200 expected)
   - **Owner:** Fulfillment
   - **Cost delta:** $0 committed, $1,200 expected

3. **Tet / BrightPath pre-build: reclassify as capital** (per Logistics, Inventory)
   - Move $52.5k off $111.6k contingency → separate capital line. Frees $15k contingency (actual available contingency rises to $126.6k, not $111.6k)
   - Right-size quantity against 99.1% uptime reality (not 99.5% fantasy) — per Deployment Support
   - **Owner:** Inventory + Deployment Support
   - **Cost delta:** $0 (reclassification only)

4. **AMG-100 depot readiness: $0 actions now** (per Repair)
   - Lock AMG-100 packing spec and serialization manifest this week (free, per Fulfillment)
   - AMG-100 service manual review, spares BOM review, kanban design by 08/01 (all free pre-MP actions)
   - **Owner:** Repair + Fulfillment
   - **Cost delta:** $0

5. **Inventory records: establish immediately** (per Inventory)
   - DVT build parts — all BOM items on-site or in-transit with ETA
   - Alpha spares pool sized against actual 99.1% uptime, not target 99.5%
   - Depot RMA kanban for TS-90R bridge stock
   - **Owner:** Inventory
   - **Cost delta:** $0

**Committed cash total:** $1,200 (DG courier only)
**Expected cash total:** $2,040 (DG courier + 30% probability air freight + 30% probability CM standby)
**DVT build date:** 06/22 — unaffected
**08/18 cert path:** unaffected

**Quality gates confirmation:** No action weakens any gate. Trigger-based expedites are schedule-protection moves, not quality shortcuts. PRT coverage, two-qualified-sources rule, PCI/EMV rigor, battery validation all unchanged.

**Brain references:** products.md (AMG100 DVT status, TS-90R refurb pool), budget.md (contingency $111.6k), strategy.md (fleet uptime commitments), state.md (growth phase, alpha trial deployed).