---
type: project-doc
project: AMG
section: production
tags: [demo, synthetic, production]
last_updated: 06/10/2026
---
# AMG-100 — NPI Build Plan (EVT → DVT → PVT → MP)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Kevin Tran (ODM PM) + Omar Haddad (MfgE) · Site: BrightPath Electronics, Bac Ninh, Vietnam — Line 2 (NPI) → Line 5 (MP)

## Build Summary

| Build | Dates | Qty | Line | Config | Status |
|---|---|---|---|---|---|
| P0 bring-up | 02/02–02/04 | 12 boards | bench | rev P0 boards only | ✅ done |
| EVT | 03/23–03/27 | 50 | Line 2 (NPI) | rev A, T0 housings, grade-B cosmetics | ✅ done — FPY 78% → [[factory-yield-evt]] |
| **DVT** | **06/22–07/01** | **200** | Line 2 | rev B, T1 housings (incl. ISS-023 mod), FW 0.9.0 | 🟡 BRR 06/12; material 94% on-dock, antenna kits ETA 06/16 ⚠️ |
| PVT | 09/28–10/09 | 500 | **Line 5 (MP line)** | rev C, T2 textured, MP fixtures, MP operators | planned |
| MP ramp M1 | 11/09– | 2,000 | Line 5 | MP | planned |
| MP M2 / M3 | Dec / Jan | 3,000 / 5,000 | Line 5 (+wkd shifts) | MP | planned |

## DVT Build Readiness (BRR 06/12) — gate checklist
| Item | Owner | Status |
|---|---|---|
| Material on-dock (188/200 sets; shortage: antenna kits, foam gaskets) | Kevin | 🟡 94% — kits ETA 06/16, gaskets 06/14 |
| Rev B PCBA from SMT (fab arrives 06/13 → SMT 06/17–18) | Omar | 🟡 tight, line slot held |
| FW 0.9.0 freeze + golden image to factory | Anna | 🟢 freeze 06/18 |
| Test stations updated (touch cal post-aging, golden-unit RF) | Omar | 🟢 scripts in dry-run → [[test-stations]] |
| Line-side antenna rework station + QC gate (first 40 units fallback) | Kevin | 🟢 SOP drafted |
| FAI plan (first 5 units full dimensional + functional) | Rachel | 🟢 checklist agreed |
| Deviation log open, waiver process confirmed | Rachel | 🟢 |

## Allocation (DVT 200) — repeated from [[schedule-milestones]]
60 PRT · 40 cert formal · 40 FW/QA · 40 field trial (12 DFW sites, Sept) · 20 line/spares

## MP Line 5 readiness (PVT entry criteria)
- 12 stations, takt 52 s, capacity 5.5k/month single shift + Saturdays → 8k/month with 2nd shift (trigger: sustained demand, see [[tooling-tracker]] 2nd tool set)
- Fixtures: 14 of 18 MP fixtures ordered (committed $96k → [[budget-tracker]] ws7); RF cal fixture #2 arrives 08/15
- Operator certification: 24 operators trained on NPI line by PVT; payment-module handling = PCI-controlled area, badge access, dual-person key ceremony room built 05/30 ✅
- ORT room: chambers booked from PVT (40-unit rotation) → [[prt-plan]]

## Traceability
Unit SN → PCBA SN → cell lot + date codes (battery), display lot, SP-30 module SN — full genealogy in BrightPath MES, queryable by our quality team via portal; required for any battery containment (proven in ISS-021 audit, 24 alpha units traced in < 2 h) → [[capa-8d-AMG-26-004]]
