---
type: meeting_r1
---
# Round 1 — Perspectives

## [[01-Departments/01-hardware-engineering/index|01-hardware-engineering]]
**Engineering position:**
The hardware engineering department supports qualifying SanDisk iNAND as a production‑ready second source *now* — by the DVT‑2 build window — rather than paying a premium after allocation cuts. We can meet DVT/ PVT gate timing, and this path preserves both the BOM target and PVT’s “two qualified sources” requirement.

**Team signals:**

- **EE team (electrical):** The PCB Rev B already has SanDisk strapping resistors stuffed (EDVT‑approved). Lab bring‑up shows no signal‑integrity issues on the eMMC bus; re‑qualification is a firmware‑qualification exercise, not a board spin.
- **System‑architecture team:** Confirms the SanDisk iNAND (industrial‑temp grade) matches the Kioxia power‑up sequence and JEDEC command set; no risk to boot ROM.
- **FW/embedded team:** Needs one‑week soak (48‑hr burn‑in, complete boot‑count validation, provisioning path regression). They call out that the SanDisk‑specific flash‑wear‑leveling profile hasn’t been qualified end‑to‑end yet — this is the sole blocking activity.
- **ME team:** No impact — package outline is JEDEC 153‑ball NAND, same thermal profile; drop‑test data already collected with SanDisk‑stuffed boards during EDVT (no failures).

**Risks (ranked):**
1. **FW qualification completeness (R‑04) — embedded team.** Full‑scale wear‑leveling and retention test requires 10‑12 calendar days from DVT‑2 samples. Risk: slipping PVT exit if SanDisk is primary in the second PVT lot. Mitigation: begin accelerated endurance cycling on engineering samples week of June 30.
2. **Kioxia broker‑buy reliability — quality team.** Broker parts carry no chain‑of‑custody guarantee; counterfeits or humidity‑damaged reels would fail PVT burn‑in (ISS‑030). Engineering recommends against the $30k spend.
3. **Single‑source ramp exposure — supply‑chain.** Even after SanDisk qualification, Kioxia remains A‑risk until two qualified batches are built. The second PVT lot (week of Sept 8) must run SanDisk‑only boards to clear the gate for ramp month 3.

**Recommendation:**
- **Accelerate SanDisk qualification** (Option 1), no slip to ramp month 2, no broker buy.
- Hold the $30k premium spend in reserve only if PVT SanDisk yield falls below 98%.
- **Decision‑gate:** FW wear‑leveling sign‑off by July 14; if not met, escalate to ramp slip conversation *at that point* — not today.

**Brain references:** products.md (AMG‑100 DVT status), budget.md (NRE headroom sufficient for FW endurance testing), state.md (growth stage — ramp commitments must be protected).

## [[01-Departments/02-npi-program-management/index|02-npi-program-management]]
**Program position:** Allocate the $30k premium cap now for broker Kioxia parts covering ramp months 2–3, and simultaneously accelerate SanDisk iNAND qualification to meet PVT gate criteria (two qualified sources on the eMMC A-risk part). This is a buy-time, don’t-slip-the-ramp decision.

**Team signals:**
- **[[sourcing-buyer]]** flags that broker buy is executable within the $30k premium cap (~$2.10/unit adder) and can secure volume through ramp month 3 (per ISS-030). They need a PO released this week.
- **[[hardware-pm]]** confirms SanDisk qual straps are already in PCB rev B and the DVT build (06/22) will produce units for qualification. Full qual data by late September — tight but feasible for PVT gate (requires two qualified sources on A-risk parts per the gate checklist). PVT line trial currently targeted mid-October.
- **[[certification]]** has no new certification dependency from an eMMC source swap (same interface, same controller); no schedule impact.
- **[[bom-eco-plm]]** confirms the cost walk has ~$3.00 headroom vs. the $142.00 MP BOM target. The $2.10 premium fits, provided we have a path back to standard pricing when SanDisk qualifies.
- **[[launch-readiness]]** is firm on wave-1 deployment commitments (Jan 2027) and Tet pre-build. Slipping ramp month 2 volumes erodes buffer stock ahead of Tet and risks missing customer pilot go-live dates.

**Critical path:** eMMC supply for ramp months 2–3 (Kioxia PO coverage exhausted after month 1). Broker buy resolves this through month 3. The secondary bind is SanDisk qualification completion vs. PVT gate — if qualification data isn’t complete, PVT gate cannot close with only one qualified source on an A-risk part. Recovery: qualify SanDisk on DVT units, close qual by PVT gate, and cut over to standard-cost SanDisk parts for volume production post-ramp month 3.

**Recommendation:**
1. **Approve broker buy** — Release PO for Kioxia premium parts covering months 2–3, within the $30k pre-approved cap. Owner: [[sourcing-buyer]].
2. **Accelerate SanDisk qualification** — Dedicate DVT units to eMMC qualification; target qualification report complete by 09/30. Owner: [[hardware-pm]] with [[certification]] sign-off.
3. **Gate condition** — PVT gate closes only with two qualified eMMC sources. No waiver. Owner: [[odm-program-mgmt]] and [[quality-manager]].
4. **Cost walk tracking** — Load the premium adder into the cost walk and flag the SanDisk standard-cost reversion trigger. Owner: [[bom-eco-plm]].

**Brain references:** products.md (AMG100 DVT status), budget.md (NRE/tooling headroom for the $30k premium), strategy.md (wave-1 commitments Jan 2027, Tet pre-build).

## [[01-Departments/03-quality-reliability/index|03-quality-reliability]]
# Quality & Reliability Perspective — Round 1

## What We Care About

Our primary obligation is ensuring the AMG-100 meets PVT gate criteria and doesn't ship devices that will spike the field return rate. The gate specifically requires **two qualified sources on A-risk parts** — eMMC is an A-risk component (single-threaded boot path, no failover). If we ship with only one qualified source, we're accepting a single point of failure that our own process explicitly prohibits.

The Kioxia cut isn't just a supply problem — it's a **qualification problem with a clock**. Per `state.md`, we're in growth phase, and our ICP's pain point #2 is "device downtime kills revenue." We cannot afford a class-wide eMMC reliability escape.

## Team Signals

**Validation/Reliability** flags: SanDisk iNAND qualification is not a paper exercise. The straps are in PCB rev B, but we need:
- Full JEDEC endurance cycling (minimum 3 weeks accelerated)
- Power-fail robustness across temperature corners
- 500-hour HTOL on the SanDisk-populated units
- Firmware compatibility regression (wear leveling, bad block management differ by vendor)

**Firmware QA** flags: Different eMMC vendors implement different command queue depths and trim behavior. We've been burned before — Gen 2 (TS-90) had a 3-month field issue where a "qualified alternative" eMMC caused silent data corruption under high write load because the eMMC's internal garbage collection timing differed. Per that 8D, our firmware eMMC driver abstraction needs explicit validation per vendor, not just "pin-compatible."

**Field Quality/RMA** flags: Our TS-90 fleet is running 2.8% annual return rate, with eMMC-related failures at 0.3% of that. Any degradation here eats our margin via RMA pool growth (`TS-90R` refurb costs). We cannot inherit a new eMMC risk into the AMG-100 launch.

**QC Inspection** notes: PVT gate inspection criteria for incoming eMMC require lot traceability and two-source AQL sampling. We're not ready to receive SanDisk lots yet — IQC procedures need updating with vendor-specific visual/electrical criteria.

## Risk Assessment

**If we rush SanDisk qualification (Option 1):**
- Qualification won't complete before PVT unless we cut corners
- Cutting corners on A-risk part qualification contradicts our CAPA history (ref: TS-90 eMMC 8D closed Q3 2025)
- DVT units with SanDisk are helpful but not sufficient — we need PVT-representative builds with process-capable assembly

**If we broker-buy Kioxia (Option 2):**
- Premium cost is one issue, but our quality concern is **traceability risk** from grey market parts. Brokered eMMC lots may be date-code mixed, re-marked, or improperly stored (MSL/humidity exposure). We'd need 100% incoming inspection with extended electrical test, which we don't have staffed.
- $2.10/unit premium doesn't include the quality cost of potential escapes

**If we slip ramp (Option 3):**
- Delay hurts customer commitments, but a field quality escape hurts them more

## Recommendation

1. **Option 3 with containment**: Slip ramp month 2 volumes by 4 weeks. This buys qualification time.
2. **Accelerate SanDisk qual properly**: Validation/Reliability runs the full JEDEC plan on engineering builds now. Firmware QA starts compatibility regression immediately. Do not abbreviate.
3. **Option 2 as bridge only**: Use brokered Kioxia for PVT builds and early ramp month 1, with mandatory 100% incoming test (extended power-fail cycling on sample basis per lot). This stays within the $30k cap if limited to ~2k units.
4. **No single-source waiver**: Do not ship month 2 volumes without two qualified sources. Per CAPA-2025-014 (TS-90 eMMC), I will hold shipment if this condition isn't met.

## Brain References
- `products.md`: AMG-100 status is DVT — we're not yet at PVT gate
- `laws.md`: Product safety listing (UL/IEC 62368-1) — eMMC reliability affects safety-critical functions (thermal shutdown, PMIC communication)
- State context: Growth phase, fleet uptime requirement >99.5% — eMMC is in that critical path

## [[01-Departments/04-mfg-supplier-quality/index|04-mfg-supplier-quality]]
**MSQ position:** Factory-side qualification and supply continuity for AMG-100 eMMC flash.

**What we care about**
We can’t ship tablets without eMMC, and we can’t qualify a second source after PVT because that resets the test coverage picture and supplier audit cycle. The 40% cut hits exactly when yield is lowest — the first mass-production months — so wafer excursions, test escapes, and factory DPPM are all elevated risk right at ramp. Our job is to make sure the eMMC that runs on the ODM SMT line is qualified, traceable, and covered by a supplier that passes a clean QSA before we run PVT.

**Team signals**

- **Supplier Quality** (owner of SCARs and AVL health): Kioxia’s allocation cut is a supply risk, not yet a quality risk — but a premium broker buy blows up traceability. Gray-market eMMC means no authorized returns, no FA support on infant mortality, and a nightmare field RMA story. Strong vote against option (2) unless we get written safety guarantees we’ve never seen in broker channels.

- **Factory Test Yield** (owner of FPY and test coverage): The SanDisk qual straps are already in PCB rev B per the brief, which is the heavy lift. But PVT gate criteria require two qualified sources on A-risk parts — and eMMC is definitely A-risk (single-component hard-down on boot). If we don’t finish SanDisk qual before PVT, we fail gate exit. That gates ramp. Per our test team, a new eMMC needs full DPPM characterization across at least three process corners before we trust FPY numbers.

- **ODM Quality** (owner of site audits and process sign-off): We still need to audit SanDisk’s assembly/test subcon or get their latest QBR scorecard. Without that, we’re qualifying a part number, not a supplier system. Kioxia’s audit is current (last cycle 2024 Q4); SanDisk is not yet on the ODM’s approved vendor list for this commodity code.

- **Manufacturing Engineering** (owner of DFM, SMT profiles): Pin-compatible is not drop-in from a process standpoint. Reflow profile verification for SanDisk — with the real PCB panel — is a DVT build activity. We need at least one pre-PVT engineering run with SanDisk soldered down, not just strained into test sockets.

**Numbers**

- **Allocation gap:** 40% of Q4 eMMC volume missing; ramp month 2 (Dec 2026) uncovered with current PO coverage.
- **Cost walk headroom:** SanDisk iNAND pricing usually comes within $0.80–$1.20/unit of Kioxia. The broker premium (+$2.10/unit) burns most of the $3.00 BOM tolerance on a single part, leaving zero room for other overruns during ramp (per `cost-walk` — we should verify current MP BOM line 6.7 cost).
- **PVT gate:** Two qualified sources on A-risk parts is mandatory (per `PVT gate criteria` cited in brief). SanDisk must be qualified — question is timing, not whether.

**Recommendation**
**Go with option (1) — accelerate SanDisk second-source qualification — and supplement with a controlled, documented allocation bridge, not a broker buy.**

Specific actions:
1. **Supplier Quality** completes SanDisk QSA and adds to ODM AVL before DVT build (06/22), using the already-strapped PCB rev B for engineering samples.
2. **Factory Test Yield** runs a designed DPPM characterization on SanDisk across three process corners during DVT, with results feeding the PVT gate package.
3. **Manufacturing Engineering** verifies the reflow profile with SanDisk on a production-representative panel during DVT, not after.
4. **Containment on the gap:** Instead of broker parts (option 2), we negotiate with Kioxia sales leadership — through our sourcing buyer — for an official, traceable allocation bridge for ramp months 2–3 with written FA and return rights. Even at a premium, that’s safer than gray-market. If Kioxia refuses, we pull in SanDisk qualification with enough lead time that PVT can run dual-source, and we slip only the Dec volume that depends on broker parts — not the entire ramp month 2.
5. **No slip of overall ramp** (option 3 avoided) — but we accept a managed volume reduction in Dec if the only alternative is untraceable parts. Customer wave-1 commitments (Jan 2027) are still covered if we pre-build Tet inventory using qualified dual-source supply.

Per Supplier Quality: one SCAR from a gray-market eMMC erases any premium savings ten times over. Let’s qualify the second source, run the PVT gate clean, and keep the supply chain traceable.

**Brain references:** products.md (AMG-100, AMG-D10 status DVT), open-issues ISS-030, risk-register R-04, ramp-plan (Q4 allocation cut, monthly volumes), bom-evt (eMMC line item and cost walk).

## [[01-Departments/05-service-operations/index|05-service-operations]]
**Service ops position:** Option 2 (broker buy) is the least-bad answer for service operations, but it’s a tactical bridge — not a strategy. The real risk isn’t the $2.10/unit premium; it’s breaking the deployment commitments we’ve already made to wave-1 customers with January 2027 go-live dates.

**Team signals:**
- **Fulfillment** and **Deployment-Support** flag that a ramp slip (Option 3) will cascade into missed site-install windows — restaurant chains book these months in advance and have tight blackout periods around holidays. A volume shortfall in ramp month 2 means either short-shipping sites (which destroys trust) or pushing deployments into February, breaking wave-1 commitments.
- **Inventory** points out that TS-90/TS-90R spares pools are stable today, but any AMG-100 deployment delay means the existing fleet runs longer, aging the TS-90R refurb pool faster. Not critical yet, but a data point.
- **Logistics** notes broker buys often come from non-authorized channels — traceability and customs paperwork can get messy. Lithium battery shipping compliance (per 49 CFR / IATA DG) requires documented chain of custody. We can manage it, but it’s overhead.
- **Repair** is neutral — we won’t see AMG-100 RMAs until mid-2027 at the earliest, so bench capacity isn’t the constraint here.

**Numbers:**
- Broker premium: ~$2.10/unit against MP BOM target of $142.00 (within the ±$3.00 tolerance, barely). Total cost exposure: ~$30k ceiling (per budget, this is small relative to the $6.8M annual ops budget — we’re talking 0.44%).
- Ramp volumes at risk without broker buy: ramp month 2 = 3,000 units. That’s ~60–150 restaurant sites that don’t get their devices on time, per `04-Projects/Project-AMG/ramp-plan`.
- PVT gate criteria (per Project-AMG risk-register R-04) require two qualified sources on A-risk parts — SanDisk qualification is already on the DVT PCB rev B, but accelerating that qualification into production-readiness is an engineering and quality timeline, not an ops one.

**Recommendation:**
1. **Execute the broker buy (Option 2)** to cover ramp month 2 volumes — authorized by the $30k cap. This preserves deployment commitments and avoids site-level chaos. Per Fulfillment, we need purchase orders cut within 5 business days to secure allocation.
2. **Simultaneously push SanDisk second-source qualification** (Option 1) with a hard target for PVT gate sign-off — not as an emergency, but as the structural fix. Until that’s done, we’re one allocation cut away from this same fire next quarter.
3. **No slip on ramp (Option 3 rejected)** — the customer impact isn’t worth the ~$6,300 premium at risk (3,000 units × $2.10).

**Caveat:** If the broker source can’t provide traceable, compliant parts (per Logistics), we escalate immediately to the exec team — no part is worth a customs hold or a lithium shipping violation.

**Brain references:** `budget.md` (annual ops budget $6.8M — $30k is absorbable), `strategy.md` (“>99.5% fleet uptime” and deployment commitments drive this decision), `products.md` (AMG-100 status DVT, ramp plan referenced from Project-AMG).