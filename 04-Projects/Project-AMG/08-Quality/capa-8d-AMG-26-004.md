---
type: project-doc
project: AMG
section: quality
tags: [demo, synthetic, quality, 8d, capa]
last_updated: 06/10/2026
---
# 8D Report — CAPA-26-004: Battery Cell Swelling, Veltron Lot VE2605A

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Champion: James Park (SQE) · Issue: ISS-021 · Status: **D6 — permanent fix verification**

## D1 — Team
James Park (SQE, lead) · Dr. Henry Wu (reliability) · Veltron QE (Ms. Chen, line 3) · Kevin Tran (ODM PM) · Rachel Adeyemi (quality approval)

## D2 — Problem Description
During EVT PRT battery cycle-life test (T12, 45 °C leg), **3 of 280 cells from Veltron lot VE2605A exhibited swelling 1.8 mm** (limit: no visible swell, now quantified ≤ 0.5 mm) at ~200 cycles. Lot ships in 1S2P packs for AMG-100. Zero swelling in lots VE2602B, VE2603A (560 cells cumulative).

## D3 — Containment (done 04/19–04/24)
- Lot VE2605A quarantined at BrightPath + Veltron: 1,200 cells blocked, scrapped under deviation — $18.4k contingency draw → [[budget-tracker]]
- 100% X-ray screening at BrightPath incoming for ALL Veltron lots until PVT (jellyroll alignment check)
- EVT field/alpha units audited: 24 alpha units = lots 02B/03A only ✅ no exposure
- DVT build material: lot VE2606A pre-screened, X-ray clean ✅

## D4 — Root Cause
**Electrolyte contamination at Veltron line 3** — moisture excursion during a 6-hour dry-room dehumidifier fault (03/12, logged in Veltron MES but not flagged to customers). Moisture → HF generation → gas → swelling under elevated temp cycling. Verified by: teardown GC-MS of 3 swollen cells (electrolyte water 38 ppm vs spec ≤ 20), correlation with MES dry-room logs, reproduction on retained lot samples (2/40 swell at accelerated 60 °C cycling).
Escape point: Veltron lot-release test = capacity + IR only; no moisture/“cycle-to-stress” sampling.

## D5 — Permanent Corrective Actions (chosen)
| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Veltron line 3: dehumidifier interlock — auto line-stop + customer notification on dry-room excursion | Veltron | 06/15 ✅ done |
| 2 | Lot release adds: electrolyte moisture sample (n=5) + 50-cycle 45 °C stress sample (n=20) per lot | Veltron QE | 06/20 |
| 3 | **Dual-source mandate: DynaCell qualified by PVT** (no MP gate single-sourced) — VP decision 04/24 → [[../../00-Brain/decisions-log\|log]] | James Park | 09/15 |
| 4 | AMG ORT: swell limit quantified ≤ 0.5 mm, monthly battery leg → [[prt-plan]] | Dr. Wu | live ✅ |
| 5 | Fleet telemetry: pack thickness proxy via gauge impedance trend alert | Anna Volkov | FW 1.0.0 |

## D6 — Verification (in progress)
- Veltron audit of actions 1–2: **on-site 06/26** (James + Kevin) ⏳
- VE2606A (post-fix lot): 40-cell stress sample at 45 °C — 0 swell @ 150 cycles to date, completes 07/08 ⏳
- DynaCell qual lot ships 06/30 → T12 dual-source leg in DVT PRT

## D7 — Prevent Recurrence
- Supplier requirement spec updated: dry-room excursion = mandatory 24 h customer notification, all cell suppliers (added to DynaCell contract from day 1)
- SQE audit checklist: dry-room interlock verification added for any Li-ion supplier → [[../../01-Departments/04-mfg-supplier-quality/index|MSQ]] supplier-quality playbook

## D8 — Closure
Target close: 07/15/2026 after D6 evidence. Recognition: Veltron transparency post-escalation noted; commercial recovery = scrap cost credit on next PO (negotiated by Linda Gomez).
