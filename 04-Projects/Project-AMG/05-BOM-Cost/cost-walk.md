---
type: project-doc
project: AMG
section: bom
tags: [demo, synthetic, cost]
last_updated: 06/10/2026
---
# AMG-100 — Cost Walk: EVT $186.40 → MP $142.00

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Linda Gomez · Target: MP unit cost $142.00 ± $3.00 @ 25k/yr

## Walk (unit cost, USD)

| Step | Δ | Cumulative | Mechanism | Status |
|---|---|---|---|---|
| **EVT actual** | — | **186.40** | 50-unit proto rates | ✅ baseline |
| Volume pricing EVT→DVT (silicon, display, memory) | −9.10 | 177.30 | 200-unit + LOI quantities quoted | ✅ contracted |
| Bridge IC deletion (native DSI panel, rev B) | −3.20 | 174.10 | EE redesign | ✅ in rev B |
| Mechanical amortization T0→T1 + cavity yield | −5.70 | 168.40 | Tooling matured | ✅ |
| Proto→pilot conversion cost (SMT/FATP rates) | −3.10 | 165.30 | DVT line rates | ✅ quoted |
| Shield can + foam gasket + standoff (issue fixes) | +0.43 | 165.73 | ISS-025/027/014 adders | ✅ accepted |
| Misc consolidation (labels, packaging litho) | −1.53 | **164.20** | **= DVT estimate** | ✅ |
| MP volume tier (SoC, display, memory @ 25k/yr) | −12.10 | 152.10 | Annual contracts, Q3 negotiation | 🟡 quotes in hand, unsigned |
| MP conversion rate (line speed 38 s, FPY 95%, test time cut 22%) | −4.30 | 147.80 | [[test-stations]] optimization + yield | 🟡 depends on FPY ≥ 95% |
| Display panel B second source leverage | −1.40 | 146.40 | Dual-source negotiation | 🟡 qual at PVT |
| Mechanical MP (2-cavity full rate + resin contract) | −2.90 | 143.50 | BrightPath annual resin buy | 🟡 |
| Packaging optimization (4-pack master, litho→flexo) | −0.80 | 142.70 | → [[packaging-spec]] | 🟡 |
| Mg→Al mid-frame (OPTION) | −1.85 | 140.85 | +38 g mass; decision DVT exit | ⬜ option |
| **MP forecast** | | **142.70** (140.85 w/ option) | vs target 142.00 ± 3.00 | 🟢 inside tolerance |

## Threats to the walk
| Threat | Exposure | Trigger | Mitigation |
|---|---|---|---|
| eMMC broker buy (ISS-030) | +$2.10 | Kioxia allocation cut Q4 | SanDisk qual by PVT; pre-approved broker cap $30k total |
| FPY < 95% at ramp | +$1.20/pt below target | DVT/PVT yield data | EVT pareto fixes → [[factory-yield-evt]] |
| Resin price index (PC+ABS) | +$0.40 | quarterly index > +8% | Annual buy locks 70% |
| Air freight during ramp months 1–2 | +$3.80/unit landed (not BOM) | Ocean lead vs deploy schedule | Planned & budgeted in [[logistics-plan]] — first 2 months only |

## Landed cost view (MP, Vietnam origin)
| Element | $ |
|---|---|
| Unit cost EXW | 142.00 |
| Ocean freight + insurance (FCL, amortized) | 2.10 |
| Duty (HTS 8471.30 — ADP machines, 0%) + MPF/HMF | 0.55 |
| 3PL inbound + DC handling | 1.85 |
| **Landed Fort Worth** | **146.50** | 
Target landed ≤ $158 → 🟢 $11.50 headroom (absorbs air-freight ramp months)
