---
type: meeting_r1
---
# Round 1 — Perspectives

## [[01-Departments/01-hardware-engineering/index|01-hardware-engineering]]
**Engineering position:** We recommend accelerating SanDisk iNAND second-source qualification (option 1) with a fallback of limited broker buys (option 2, pre‑approved $30k cap) to protect month‑2 volumes. Slip is not acceptable — the PVT gate requires two qualified sources on A‑risk parts, and ramp slip cascades into Tet pre‑build and customer wave‑1 Jan 2027 deployment.

**Team signals:**
- **EE team:** Per the EE team, the SanDisk qual straps are already in PCB rev B (the DVT build 2025‑06‑22 boards). Firmware driver qualification can start on bench samples now. They flag the Kioxia allocation cut as a single‑source supply risk (ISS‑030) that triggers R‑04 in the risk register.
- **FW/embedded team:** Firmware re‑qualification for SanDisk iNAND requires a 3‑week wear‑levelling stress cycle (must start by mid‑July to complete before PVT). No architectural concerns.
- **System architecture:** SanDisk iNAND was the planned second source; no SoC or board‑support‑package changes required. They strongly recommend against relying on a single source through ramp — a second allocation cut would halt production.
- **ME team:** No mechanical impact — the SanDisk package fits the existing B‑side keep‑out zone.

**Risks (ranked):**
1. **Single‑source halt (R‑04, owner: EE team, severity: critical).** If Kioxia reduces allocation further, production stops. Mitigation: accelerate SanDisk qual.
2. **SanDisk qual delay (owner: FW/embedded team, severity: high).** If the 3‑week firmware stress cycle finds late issues, PVT gate slips. Mitigation: start bench qual immediately, broker buy as bridge.
3. **Cost creep on broker parts (owner: Hardware Eng Mgr, severity: medium).** Premium buys at +$2.10/unit erode margin, but the BOM target of $142 ± $3 has ~$1.80 headroom from the latest cost walk. A $30k cap covers ~14k units — sufficient for month‑2 gap if SanDisk qual stays on track.

**Recommendation:**
1. **Option 1 first:** Kick off SanDisk iNAND qualification now. EE orders 50 bench‑samples today; FW starts stress cycle no later than 2025‑07‑14.
2. **Option 2 as bridge:** Authorize a limited broker buy of Kioxia parts (cap $30k, ~14k units at +$2.10/unit) only for month‑2 volume — enough to cover SanDisk qual buffer.
3. **No slip (option 3 rejected):** Slip costs ramp momentum, violates PVT gate (two qualified sources required), and risks wave‑1 customer commitments.
4. **Verification handoff to [[validation‑reliability]]:** SanDisk iNAND must pass the full PVT qualification suite (electrical stress, temp cycling, read‑disturb) per the PVT test plan.
5. **ECO handoff to [[bom‑eco‑plm]]:** On successful qual, cut an ECO to release SanDisk as an approved alternate source on the MP BOM.

**Brain references:** products.md (AMG‑100 DVT status), budget.md (total year $6.8M — the $30k broker cap is within NRE contingency), state.md (growth — we must support ramp).

## [[01-Departments/02-npi-program-management/index|02-npi-program-management]]
# NPI & Program Management — Round 1 Position

## Program Position
AMG-100 ramp is threatened on the critical path by single-source eMMC supply. Not a schedule debate — a gate-criteria and coverage debate. The program **cannot** launch with one qualified source on an A-risk part, and right now we have **zero qualified sources if Kioxia doesn't deliver**.

## What We Care About
1. **PVT gate criteria**: Per the PVT checklist, A-risk parts require two qualified, volume-capable sources. Today we have one (Kioxia) — and they just cut us.
2. **Ramp coverage**: ISS-030 confirms PO coverage only extends through Month 2. Month 3 volumes (5k units) have zero material committed.
3. **Tet pre-build**: Ramp plan assumes 4-6 week material lead for January 2027 deployments. If parts arrive late November, we miss Tet factory shutdown and wave-1 commitments.
4. **Cost walk integrity**: MP BOM target $142.00 ± $3.00. Premium buys eat headroom; design changes risk re-qual. Both hit margin if not managed.

## Team Signals
- **Sourcing-Buyer**: Kioxia allocation cut confirmed. Broker premium at ~$2.10/unit, caps at $30k. That buys ~14k units — covers ramp Month 3 shortfall but not long-term.
- **Hardware-PM**: DVT build 06/22 already includes SanDisk iNAND straps on PCB rev B. Qualification not starting from zero.
- **Certification**: No new FCC/UL required for same-footprint flash swap, but PCI PTS re-validation likely if BOM changes post-PVT. Pre-PVT is cleanest.
- **ODM Program Mgmt**: Factory needs line-side stock by 10/15 for ramp Month 1. Broker parts must clear IQC — timeline tight.
- **Launch Readiness**: Wave-1 deployments Jan 2027 — slip = customer penalties, RMA pool miss, TS-90R fleet can't backfill game revenue units.

## Critical Path
**SanDisk iNAND qualification completion date** vs. **Month 3 volume cutoff**. If SanDisk qual finishes before PVT gate (target 08/15/2026 per ramp-plan), we meet the two-source requirement and avoid premium buys for production. If it slips past PVT, we gate-fail — regardless of calendar.

## Recommendation
**Do both Option 1 and Option 2, sequenced:**
- **Accelerate SanDisk qual now** (Option 1): DVT straps exist. Run qualification in parallel with remaining DVT builds. Target qual report by 07/30. This is the strategic fix — it satisfies PVT gate criteria and gives ODM a qualified second source.
- **Broker-buy bridge volume only** (Option 2): Purchase ~10k units via broker at premium ($21k) to cover Month 3–4 until SanDisk production volumes flow. Cap exposure at $25k, not $30k. This buys schedule without buying a permanent premium BOM.
- **Reject Option 3 (slip ramp)**: Wave-1 commitments are contractual. Tet pre-build is non-negotiable for on-time deployment. A slip cascades into customer penalties, budget miss (product revenue line), and TS-90R pool strain.

## Brain References
- `products.md`: AMG-100 DVT status, $329 ASP with 42% margin — cost walk headroom exists but is thin at $142 ± $3
- `strategy.md`: "predictable supply" and PCI security are ICP pain points — single-source flash violates both
- `budget.md`: $6.8M annual budget; $25k bridge buy is 0.37% — within program contingency envelope
- Open issues: ISS-030 (PO coverage gap), risk register R-04 (single-source flash), bom-evt (SanDisk straps present), cost-walk (impact of $2.10 premium on BOM variance)

## Next Handoff
- Qualification acceleration plan → **Hardware Engineering Manager** (test plan, SI validation)
- Broker purchase order → **Sourcing-Buyer** (negotiate, PO, IQC coordination)
- PVT gate criteria update → **Quality Manager** (confirm two-source requirement with timing)

## [[01-Departments/03-quality-reliability/index|03-quality-reliability]]
## Quality & Reliability Perspective — Round 1

**Cares About:** I care whether an unqualified memory supplier weakens our production gate criteria and whether a capacity scramble creates a quality escape in the field. My team holds the PVT gate that demands two qualified sources on A‑risk parts, and we will not waive it under schedule pressure.

### Current Signals from My Teams

- **Validation‑Reliability** — SanDisk iNAND qual is *in progress*, not complete. We have engineering‑sample hours in‑house (~200 h on bench), but our DVT protocol for eMMC demands 1,000 power‑cycle transitions, 500 h of write‑aging, and 3‑full‑profile temperature corners (−20 °C, +25 °C, +70 °C). We are 40 % through. The PCB‑B strap is populated, which helps, but a “strap” does not equal a qualified second source.
- **Firmware QA** — Three firmware commits pending for SanDisk block‑management quirks. Regression depth is thin (2 of 4 planned test‑sweeps done). A fully qualified second source requires FW sign‑off, not just hardware presence.
- **Field‑Quality / RMA** — TS‑90 fleet return data shows that rushed memory quals (there was a Toshiba‑to‑Kioxia bridge in 2022) contributed 15 of 220 early‑life failures. I will not repeat that.
- **QC‑Inspection** — Broker‑buy parts lose traceability and counterfeit‑chain integrity. My IQC protocol cannot accept spot‑market eMMC without documented provenance; we risk a material‑trace hold at IQC that shelves the line.
- **QA‑System** — PVT gate requires two qualified sources on A‑risk parts (Risk Register R‑04). Kioxia is qualified; SanDisk is not. Option 2 (broker) does **not** create a second *qualified* source — it creates an uncontrolled inventory stream.

### Risk Statement
If we proceed with Option 1 (accelerate) or Option 2 (broker) without completing the qual, two escapes are possible:
1. A latent early‑life failure signature in a volume we cannot contain (2,000 units in ramp‑month 2 alone).
2. A traceability audit failure at IQC that triggers a material hold, blocking the line entirely — worse than a slip.

Option 3 (slip month‑2 volumes) is the only path that does **not** compromise gate integrity.

### Recommendation
1. **Containment:** Slip ramp month 2 volumes to the minimum needed for PVT gate completion (per `ramp-plan` in Project‑AMG).
2. **Verification:** Validation‑Reliability and Firmware QA complete the SanDisk qual on an accelerated but uncompromised schedule — dual‑shift bench capacity, no skipped cycles.
3. **System Fix:** Update ISS‑030 and Risk Register R‑04 to reflect that the second‑source qual is the pacing item. Handshake with MSQ Manager to lock SanDisk supply once qualified.
4. **Hold Position:** I will exercise hold authority on the PVT gate if SanDisk qual data is incomplete at gate review. Two‑source requirement stands.

Per Validation‑Reliability and Firmware QA teams — the data isn’t there yet. We close the qual, then we ship. Not before.

**Brain References:** products.md (AMG‑100 status DVT), state.md (growth stage, ramp schedule), decisions‑log (Toshiba‑Kioxia 2022 field‑return precedent), 04‑Projects/Project‑AMG (open‑issues ISS‑030, risk‑register R‑04, ramp‑plan).

## [[01-Departments/04-mfg-supplier-quality/index|04-mfg-supplier-quality]]
**MSQ position:** The immediate risk is not supply continuity — it’s qualification readiness for a second source on a single‑screened, A‑risk part. Our five sites can’t flip eMMC brands on the fly without validated test coverage and process capability data.

**Team signals:**
- **Supplier Quality** raised R‑04 three weeks ago: Kioxia backlog visibility was already soft, and the AVL still shows SanDisk status as *Qual‑in‑progress* (not conditionally approved). Their SCAR‑aging report flagged that any emergency qualification now would skip the full 3‑lot PVT verification window.
- **Factory Test & Yield** warn that the current test station cover‑age for eMMC initialisation and wear‑levelling corner cases was characterised only on Kioxia silicon. The PCB rev‑B strap exists, but the test limit file hasn’t been correlated for SanDisk — we’d be flying blind on FPY for at least the first 500 units.
- **Manufacturing Engineering** confirm the fixture and process are brand‑agnostic; the risk is parametric, not mechanical.
- **ODM Quality** note that the PVT gate criteria (two qualified sources on A‑risk parts) is the one hard blocker we cannot waive without a formal risk acceptance.

**Numbers:**
- Current Kioxia allocation covers ramp month 1 + ~60% of month 2 → ~2,000‑unit shortfall at month‑2 rate of 3k.
- Broker premium: ≤$30k cap, ~$2.10/unit — stays inside cost walk headroom if volume ≤14.3k units (BOM target $142 ±$3).
- iNAND qualification lead time, realistic fast‑track: 6‑8 weeks to PVT gate data (3‑lot build + 500‑hr stress), puts approval mid‑September — *after* DVT build but ahead of PVT start.
- Risk if we broker only and skip qualification: single‑source violation at PVT gate → ramp slip anyway, plus field recall exposure (eMMC is A‑risk per DFMEA).

**Recommendation:**
1. **Accelerate SanDisk qualification immediately** — Owner: Supplier Quality + Factory Test. Target conditional approval on 2‑lot data by 09/15, full 3‑lot by PVT gate. This pulls the safety net forward.
2. **Broker‑buy Kioxia parts** up to the $30k cap to cover the month‑2 gap — Owner: Sourcing‑Buyer. This is tactical bridging, not a fix.
3. **Do not slip ramp** unless qualification data forces it; a slip here cascades into Tet pre‑build and wave‑1 deployment penalties that far exceed the broker premium.

Containment: any brokered lots get 100% incoming eMMC validation on the correlated test station before line release — per Factory Test. If SanDisk qual fails a gate, we escalate the slip decision with data, not conjecture.

**Brain references:** `products.md` (AMG‑100 DVT status), budget context (quality cost of rework/scrap if bypassing qualification), `decisions‑log.md` (R‑04 risk register), PVT gate criteria (two qualified sources on A‑risk parts).

## [[01-Departments/05-service-operations/index|05-service-operations]]
**Service ops position:** The Kioxia cut creates a real ship-stop risk for the wave‑1 deployments we’ve committed to in Jan 2027, and my teams cannot absorb a last‑minute schedule slip without breaking fulfillment SLAs.

**Team signals:**
- **Fulfillment:** Ramp month‑2 (2 k→3 k units) already has customer site‑install windows locked. Slipping volume ≥30 days will force rescheduling 50+ deployments with labor idle penalties.
- **Inventory:** We have zero buffer stock of finished AMG‑100s (DVT‑only) and no alternate eMMC banked. We are exposed.
- **Repair:** Not directly impacted today, but early field failures on a single‑source part create long‑term RMA turnaround risk if that part becomes hard to procure later.

**Numbers:**
- Ramp plan (products.md): 2 k / 3 k / 5 k units per month starting Nov 2026.
- Wave‑1 customer deployment commitment: Jan 2027 (strategy.md). A slip in Dec output puts ≈3 k units at risk.
- Broker‑buy cap: $30 k, ~+$2.10/unit (brief). Covers ≈14 k units before the budget is exhausted — enough to bridge ramp month‑2, but not free.
- Tet (Chinese New Year) pre‑build: typically requires 4‑6 weeks of safety stock; any slip now tightens that window in Dec/Jan.

**Recommendation:**
1. **Authorize broker buy** immediately for the gap volume at ramp month‑2 only (≤$30 k). This is a one‑time insurance payment, not a structural fix. Inventory will hold the premium parts in a separate bin; cost accounting tagged for this quarter.
2. **Parallel‑path SanDisk qualification** now — the PCB already has the straps (PCB rev B), so acceleration is feasible. Target PVT gate with two sources per R‑04.
3. **Do not slip ramp month‑2 volumes.** The downstream deployment cost and customer trust damage exceed the $30 k premium.

**Brain references:**
- products.md: AMG-100 ramp volume commitments.
- strategy.md: Jan 2027 wave‑1 deployments; fleet uptime SLA expectations.
- budget.md: total‑year $6.8 M — $30 k represents <0.5% of annual ops budget; manageable.