---
type: project-doc
project: AMG
section: pm
tags: [demo, synthetic, schedule]
last_updated: 06/10/2026
---
# Project AMG — Schedule & Phase Gates

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · 📅 Today: 06/10/2026

## Master Gate Schedule

| Gate | Phase | Plan | Actual / Forecast | Status | Exit criteria highlights |
|---|---|---|---|---|---|
| C0 | Concept approval | 11/14/2025 | 11/14/2025 | ✅ Done | Business case, $2.0M budget approved |
| C1 | Architecture / planning | 01/16/2026 | 01/16/2026 | ✅ Done | EE/ME architecture locked, ODM signed, BOM v0.5 |
| **EVT build** | Engineering validation | 03/23/2026 | 03/23/2026 (50 units) | ✅ Done | Proto verification, [[evt-ee-test-report\|EE report]] |
| **EVT exit** | | 05/01/2026 | 05/08/2026 (+1 wk) | ✅ w/ 2 waivers | W-01 drop crack, W-02 sanitizer gloss → [[00-Brain/decisions-log\|log]] |
| **DVT build** | Design validation | 06/22/2026 | 06/22/2026 (200 units) | 🟢 On track | All EVT fixes cut in: ISS-014/023/025 |
| **DVT exit** | | 08/14/2026 | 08/14/2026 | 🟢 | Full PRT pass, cert samples shipped |
| **PVT build** | Production validation | 09/28/2026 | 09/28/2026 (500 units) | 🟢 | MP tooling, MP fixtures, FPY ≥ 92% |
| **PVT exit** | | 10/23/2026 | 10/23/2026 | 🟢 | Certs granted, ramp readiness review |
| **MP** | Mass production | 11/09/2026 | 11/09/2026 | 🟢 | Ramp 2k → 3k → 5k /month |
| Launch | First fleet deployment | 01/12/2027 | 01/12/2027 | 🟢 | 3 anchor chains, 38 sites wave 1 |

## Critical Path (today → MP)
1. **DVT build 06/22** ← ISS-014 antenna rework parts arrive 06/16 (3-day buffer) ⚠️
2. PCI PTS pre-assessment @ Atlas Security Labs 07/06–07/10 — hardware change here = 4–6 wk slip (top program risk, R-01)
3. DVT PRT complete 08/07 → DVT exit 08/14
4. Cert formal submissions 08/18 (FCC/ISED/UL/EMV L2) — 8–10 wk grant cycles land just before PVT exit
5. MP tooling release 08/21 (T2 mods from DVT learnings) → [[tooling-tracker]]

## Build Quantities & Purpose
| Build | Qty | Allocation |
|---|---|---|
| EVT (done) | 50 | 20 EE bench, 12 PRT, 8 FW, 5 cert pre-scan, 5 mgmt demo |
| DVT | 200 | 60 PRT, 40 cert formal, 40 FW/QA, 40 field trial (12 DFW sites), 20 spares |
| PVT | 500 | 100 PRT/ORT, 60 depot training + FRU seeding, 300 wave-1 staging, 40 ongoing reliability |
| MP ramp | 2,000/mo → 5,000/mo | Revenue units |

## Schedule Risks
- 🔴 R-01 PCI PTS pre-assessment finding → see [[04-Projects/Project-AMG/01-PM/risk-register]]
- 🟡 R-04 eMMC allocation Q4 (ISS-030) — PO coverage through ramp month 2 only
- 🟡 Tet holiday (02/2027) — BrightPath shutdown 2 wks, pre-build buffer planned in ramp month 3
