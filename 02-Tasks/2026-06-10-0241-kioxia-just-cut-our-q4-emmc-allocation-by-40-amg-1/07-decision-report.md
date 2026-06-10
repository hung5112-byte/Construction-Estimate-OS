---
type: decision_report
stop: 1
---
## 📌 Bottom line (30-second read)
- Our memory chip supplier cut Q4 shipments by 40%, creating a 1,200-chip shortage that threatens January customer deliveries.
- We recommend buying just those 1,200 chips now on the open market (~$2,520 extra) as a bridge while qualifying a backup supplier on the normal schedule.
- No production delay today—but we'll set a hard checkpoint in 4–6 weeks to decide if backup testing results force a delay later.
- Customer communication must be drafted now as insurance in case the checkpoint forces us to change course.

---

# Decision Report: AMG-100 Memory Chip Supply Shortage — How We Fix It

## 📌 Bottom Line (30-Second Read)
Our memory chip supplier cut our Q4 shipment by 40%. We're short about 1,200 chips for our December production run. This puts our January 2027 customer deliveries at risk.

We have three options:
1. **Qualify a backup supplier** (SanDisk) as fast as possible
2. **Buy the missing chips on the open market** at about $2.10 extra per chip (we've already approved up to $30,000 for this)
3. **Delay production by 4–6 weeks**

**Our recommendation: Do both #1 and #2, but with strict limits.** Buy only the 1,200 chips we absolutely need now (~$2,520 total extra cost). Run the full backup supplier testing on our normal schedule — no shortcuts. Set a checkpoint meeting to decide whether to keep going or change course.

**Why this matters:** Our quality standards require two approved suppliers for the **boot memory chip** (the single chip that starts up the tablet — without it, the device is dead). This rule cannot be changed or waived.

The open-market purchase is a temporary bridge. The backup supplier is the permanent solution. We must prepare customer communication now, just in case testing results force a delay later.

## Our Recommendation
**Move forward with limits** — Do both #1 and #2 at the same time, with the tight controls described in the Balanced approach below. Do not approve unlimited open-market buying. Do not delay production today.

## What Changed From the Original Plan
| Item | Original Plan | Our Recommendation | Why |
|------|----------------|----------------|--------|
| Scope of open-market buying | Buy for months 2–3 of production (up to $30k limit) | Buy for month 2 only (1,200 chips, ~$2,520 extra) | Limits financial risk while protecting January 2027 commitments; month 3 decision will be made at the checkpoint review |
| Backup supplier testing timeline | Rush it to meet quality gate on a compressed schedule | Run full standard testing on normal schedule — no shortcuts, no skipped tests | Quality gate rules are absolute; rushing testing risks incomplete data and unreliable products in the field |
| Production delay decision | Decide now whether to delay or not | No delay today; checkpoint review triggers delay only if backup supplier testing shows critical failure | Protects customer commitments while keeping a clean exit path if test data is bad |

## Detailed Analysis

### What Each Department Said

**Hardware Engineering:** Go with Option 1 — fast-track the backup supplier now. Our circuit board already has the connections needed for the SanDisk chip (approved in earlier testing). Lab testing shows no signal problems. The only blocking task is **firmware wear-leveling testing** (testing how the software manages the chip's lifespan — this keeps the chip working evenly so no single part wears out too fast), which needs 10–12 days from when we get test samples. We oppose open-market buying because of the risk of counterfeit or mishandled parts from unknown sources.

**Product Launch Program Management:** Do both — buy on the open market for months 2–3 AND fast-track the backup supplier. Open-market buying works within the $30,000 limit and secures chips through month 3. The circuit board already supports SanDisk connections. Our quality gate requires two approved suppliers for critical parts like this memory chip — no exceptions. We must protect January 2027 customer commitments and pre-holiday production.

**Quality & Reliability:** Option 3 with safety measures — delay month 2 production by 4 weeks. Full backup supplier qualification is not just paperwork. It requires:
- **JEDEC endurance cycling** (industry-standard testing that repeatedly writes and erases data to simulate years of use — takes at least 3 weeks)
- **Power-fail robustness testing** (testing what happens if power cuts out during writing)
- **Firmware compatibility testing** (ensuring the software works correctly with the new chip)

We reference a previous product where a "qualified alternative" memory chip caused 3 months of silent data corruption because it handled background cleanup differently. Open-market chips carry traceability risk: mixed manufacturing dates, counterfeit relabeling, improper moisture protection during storage. We recommend 100% incoming inspection if open-market parts are used.

**Manufacturing & Supplier Quality:** Go with Option 1 — fast-track backup supplier with a controlled, traceable bridge supply, NOT open-market buying. One quality complaint from a questionable-market chip erases the cost savings ten times over. SanDisk must be added to the **ODM approved vendor list** (the list of suppliers our manufacturing partner is allowed to buy from) before production test build. The quality gate requires two approved sources — the question is timing, not whether. We recommend negotiating with our current supplier for an official, traceable bridge supply with written rights to return defective parts, rather than buying on the open market.

**Service Operations:** Execute open-market buying (Option 2) to cover month 2 volumes, while simultaneously fast-tracking the backup supplier. A production delay cascades into missed site installation windows — restaurant chains book installations months in advance with tight blackout periods. The $30,000 extra cost is 0.44% of our $6.8M annual operations budget — we can absorb it. But caveat: if open-market parts can't be traced or certified compliant (especially for lithium battery shipping regulations), escalate immediately.

### The Debate

**Argument FOR doing both immediately (Bridge and Qualify):**
The extra cost (~$2.10 per chip on 8,000 chips for months 2–3 = ~$16,800) is a contained expense to protect our product launch. Each tablet sells for $329 at 42% profit margin. Missing a single restaurant chain deployment of 2,000 tablets across 50 locations is roughly $658,000 in lost revenue — far larger than the extra chip cost. The circuit board already supports SanDisk, so we're not starting from zero. Production testing phase 2 is the right window to complete qualification.

**Argument FOR delaying production (Option 3):**
The $30,000 spending cap is wishful thinking — if backup supplier testing hits delays (likely, based on history), extra costs will extend beyond the cap. Qualification is not just about physical compatibility — it requires environmental stress testing, supplier factory audit, and predicting how the part will perform in the field. Our previous product history proves "qualified alternative" memory chips can cause silent failures in the field. Our **ideal customer** (the VP of Operations at a 500-location chain) cares more about uptime than a 30-day delay. "We either ship right, or we don't. There's no 'kinda right' on a critical component."

### Three Strategic Perspectives

**AGGRESSIVE GROWTH: Full "Bridge and Qualify" — No Hesitation.**
Execute open-market buying immediately for months 2–3 ($16,800, well under the $30k cap). Fast-track backup supplier testing. The $2.10 per chip extra is temporary — it disappears when SanDisk becomes a second approved source. Option 3 (delay) is a strategy killer: it misses pre-holiday production, breaks January 2027 commitments, and signals market weakness. "You don't get to #1 by delaying launches. You get there by working through supply constraints."

**CAUTIOUS: Option 3 — Delay Month 2 by 4–6 Weeks.**
The quality gate criteria are absolute: two approved sources for critical parts. SanDisk is not approved today, and having connection points on a circuit board is not the same as proven validation. If we attempt parallel work and SanDisk hits a delay, we face an impossible choice at the quality gate: ship unqualified, or delay anyway — after burning through the $30k and exhausting the team. Revenue protection requires delivery of *working* products, not just delivery. The customer's main concern is "device downtime kills revenue at the checkout" — a 3% field failure rate erases any goodwill from on-time delivery. Sets specific stop/kill conditions: SanDisk must show successful boot and full test pass at production testing midpoint; open-market spending capped at $25k (not $30k); quality gate criteria are absolute.

**BALANCED: Staggered execution with hard checkpoints.**
Authorize open-market buying **only for the month 2 gap** (1,200 chips × $2.10 = **$2,520 total**). Run backup supplier testing on the full standard schedule — no compression. Set a hard decision checkpoint at production testing midpoint (4–6 weeks in): if SanDisk is on track, continue transition to backup supplier; if critical failure, pivot immediately to Option 3 for month 3 and beyond. Prepare customer communication now as insurance. This spends $2,520 to buy a 30-day window on protecting January deployments — a reasonable bet that limits financial risk while preserving both reliability standards and market momentum.

## What Must Happen Before Launch (Blocking Tasks)
- [ ] **Release purchase order for open-market chips for month 2 only** — 1,200 chips, ~$2,520 extra cost. Owner: sourcing-buyer. Deadline: this week.
- [ ] **Complete SanDisk supplier factory audit and add to manufacturing partner's approved vendor list** before production test build (June 22). Owner: Supplier Quality.
- [ ] **Run SanDisk soldering profile verification on production-representative test board** during test build. Owner: Manufacturing Engineering.
- [ ] **Complete firmware wear-leveling qualification** — begin accelerated endurance testing on engineering samples week of June 30. Target approval: July 14. Owner: Firmware team.
- [ ] **Run full endurance testing, power-fail robustness, and 500-hour accelerated life testing** on SanDisk-equipped test units. Owner: Validation/Reliability.
- [ ] **Update incoming inspection procedures** for SanDisk (supplier-specific visual and electrical criteria). Owner: Quality Inspection.
- [ ] **Draft customer communication** for "Schedule Adjustment Due to Quality Assurance" — approve now, deploy within 48 hours if production testing checkpoint triggers Option 3. Owner: launch-readiness.
- [ ] **Negotiate with current supplier for official allocation bridge** with written return/defect analysis rights as preferred alternative to open-market channel. Owner: sourcing-buyer with Supplier Quality.

## Quality Checkpoint Gates
| Checkpoint | Timing | Condition | Action if NOT met |
|------|--------|-----------|-------------------|
| **Firmware wear-leveling approval** | July 14, 2026 | SanDisk-specific flash-wear-leveling profile tested end-to-end | Escalate to executive team; evaluate production delay at that point — not today |
| **Production testing midpoint data review** | ~4–6 weeks into testing window | SanDisk demonstrates successful boot, full test suite pass, no timing problems at temperature extremes, preliminary quality ≥98% on minimum 100-unit sample | Stop ALL open-market procurement beyond month 2; pivot to Option 3 (delay month 3+); deploy customer communication within 48 hours |
| **SanDisk qualification report complete** | September 30, 2026 | Full qualification data package signed off by hardware program manager and certification | Quality gate cannot close with one approved source on critical part; month 3+ in jeopardy — escalate |
| **Open-market spending hard cap** | Ongoing | Total extra cost ≤ $25,000 (not $30,000 — preserve $5k buffer) | Escalate to executive team before any additional purchase order |
| **Per-chip extra cost** | Ongoing | ≤ $3.00 per chip (vs. current ~$2.10) | Escalate to executive team — price increase is leading indicator of sustained scarcity |
| **Final quality gate sign-off** | Final gate review (~mid-October 2026) | Two fully qualified memory chip sources on critical parts; no waivers, no conditional approval | Product does not ship. Gate documented and communicated to board/investment committee — cannot be overridden by program team under schedule pressure |
| **SanDisk standard-cost reversion** | After month 3 of production | SanDisk pricing ≤$0.80–$1.20 per chip vs. current supplier baseline | **BOM cost register** (list of all component costs that make up the product) updated; extra open-market cost retired |

## Decisions You Must Make
**A) Approve the Balanced Staggered Execution plan:**
- Open-market buying for month 2 ONLY (1,200 chips, ~$2,520 extra)
- Full backup supplier testing on standard schedule (no compression)
- Production testing midpoint checkpoint triggers go/no-go decision before month 3 open-market exposure
- Customer communication prepared now as insurance

**B) Approve the Growth "Full Bridge and Qualify" plan:**
- Open-market buying for months 2–3 (up to $30k cap)
- Accelerated backup supplier testing on compressed timeline
- Higher financial risk, higher January 2027 certainty

**C) Approve the Cautious "Option 3 — Delay Production" plan:**
- No open-market buying
- Delay month 2 volumes by 4–6 weeks
- Proactive customer communication now
- Protect cost targets, protect quality gate integrity

**D) Request additional information or analysis before deciding.**

## ✅ CEO DECISION (06/10/2026)
**Option A approved — Balanced Staggered Execution plan**, by Brian H. Doan (VP):
- Open-market buy for month 2 ONLY (1,200 chips, ~$2,520 premium); prefer the negotiated Kioxia bridge allocation if secured first
- Full SanDisk qualification on the standard schedule — no compression, no skipped tests
- Hard go/no-go checkpoint at PVT midpoint before any month-3 open-market exposure; spend cap tightened to $25k
- Customer communication drafted now as insurance
The execution plan must implement Option A only.

---

*Report based on input from Hardware Engineering, Program Management, Quality & Reliability, Manufacturing & Supplier Quality, and Service Operations teams. Market research confirms our current supplier's 2026 memory chip production is fully sold out, with supply-demand imbalance persisting until at least 2027.*

---

## ⚠️ Warning: claims missing a source

The following sentences contain figures or legal references but no clear citation was found. The CEO should verify them before proceeding:

- **[Line 6] Figure:** - Our memory chip supplier cut Q4 shipments by 40%, creating a 1,200-chip shortage that threatens January customer deliveries.
- **[Line 7] Figure:** - We recommend buying just those 1,200 chips now on the open market (~$2,520 extra) as a bridge while qualifying a backup supplier on the normal schedule.
- **[Line 8] Figure:** - No production delay today—but we'll set a hard checkpoint in 4–6 weeks to decide if backup testing results force a delay later.
- **[Line 16] Figure:** Our memory chip supplier cut our Q4 shipment by 40%.
- **[Line 16] Figure:** We're short about 1,200 chips for our December production run.
- **[Line 20] Figure:** **Buy the missing chips on the open market** at about $2.10 extra per chip (we've already approved up to $30,000 for this)
- **[Line 21] Figure:** **Delay production by 4–6 weeks**
- **[Line 23] Figure:** **Our recommendation: Do both #1 and #2, but with strict limits.** Buy only the 1,200 chips we absolutely need now (~$2,520 total extra cost).
- **[Line 43] Figure:** The only blocking task is **firmware wear-leveling testing** (testing how the software manages the chip's lifespan — this keeps the chip working evenly so no single part wears out too fast), which nee
- **[Line 45] Figure:** Open-market buying works within the $30,000 limit and secures chips through month 3.
- **[Line 47] Figure:** **Quality & Reliability:** Option 3 with safety measures — delay month 2 production by 4 weeks.
- **[Line 48] Figure:** - **JEDEC endurance cycling** (industry-standard testing that repeatedly writes and erases data to simulate years of use — takes at least 3 weeks)
- **[Line 52] Figure:** We reference a previous product where a "qualified alternative" memory chip caused 3 months of silent data corruption because it handled background cleanup differently.
- **[Line 52] Figure:** We recommend 100% incoming inspection if open-market parts are used.
- **[Line 56] Figure:** The $30,000 extra cost is 0.44% of our $6.8M annual operations budget — we can absorb it.
- **[Line 61] Figure:** The extra cost (~$2.10 per chip on 8,000 chips for months 2–3 = ~$16,800) is a contained expense to protect our product launch.
- **[Line 61] Figure:** Each tablet sells for $329 at 42% profit margin.
- **[Line 61] Figure:** Missing a single restaurant chain deployment of 2,000 tablets across 50 locations is roughly $658,000 in lost revenue — far larger than the extra chip cost.
- **[Line 64] Figure:** The $30,000 spending cap is wishful thinking — if backup supplier testing hits delays (likely, based on history), extra costs will extend beyond the cap.
- **[Line 69] Figure:** Execute open-market buying immediately for months 2–3 ($16,800, well under the $30k cap).
- **[Line 69] Figure:** The $2.10 per chip extra is temporary — it disappears when SanDisk becomes a second approved source.
- **[Line 69] Figure:** "You don't get to #1 by delaying launches.
- **[Line 71] Figure:** **CAUTIOUS: Option 3 — Delay Month 2 by 4–6 Weeks.**
- **[Line 72] Figure:** If we attempt parallel work and SanDisk hits a delay, we face an impossible choice at the quality gate: ship unqualified, or delay anyway — after burning through the $30k and exhausting the team.
- **[Line 72] Figure:** The customer's main concern is "device downtime kills revenue at the checkout" — a 3% field failure rate erases any goodwill from on-time delivery.
- **[Line 72] Figure:** Sets specific stop/kill conditions: SanDisk must show successful boot and full test pass at production testing midpoint; open-market spending capped at $25k (not $30k); quality gate criteria are absol
- **[Line 75] Figure:** Authorize open-market buying **only for the month 2 gap** (1,200 chips × $2.10 = **$2,520 total**).
- **[Line 75] Figure:** Set a hard decision checkpoint at production testing midpoint (4–6 weeks in): if SanDisk is on track, continue transition to backup supplier; if critical failure, pivot immediately to Option 3 for mon
- **[Line 75] Figure:** This spends $2,520 to buy a 30-day window on protecting January deployments — a reasonable bet that limits financial risk while preserving both reliability standards and market momentum.
- **[Line 78] Figure:** - [ ] **Release purchase order for open-market chips for month 2 only** — 1,200 chips, ~$2,520 extra cost.
- **[Line 84] Figure:** - [ ] **Draft customer communication** for "Schedule Adjustment Due to Quality Assurance" — approve now, deploy within 48 hours if production testing checkpoint triggers Option 3.
- **[Line 100] Figure:** - Open-market buying for month 2 ONLY (1,200 chips, ~$2,520 extra)
- **[Line 106] Figure:** - Open-market buying for months 2–3 (up to $30k cap)
- **[Line 112] Figure:** - Delay month 2 volumes by 4–6 weeks
- **[Line 120] Figure:** Market research confirms our current supplier's 2026 memory chip production is fully sold out, with supply-demand imbalance persisting until at least 2027.*
