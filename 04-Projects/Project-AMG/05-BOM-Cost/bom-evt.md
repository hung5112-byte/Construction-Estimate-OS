---
type: project-doc
project: AMG
section: bom
tags: [demo, synthetic, bom, cost]
last_updated: 06/10/2026
---
# AMG-100 — BOM (EVT actuals → DVT estimate)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Linda Gomez (sourcing) + David Chen (EE) · BOM rev: 2.1 (DVT) · Currency: USD, EXW BrightPath

## Cost Summary
| Phase | Material | Conversion (SMT+FATP+test) | Total unit cost | Volume basis |
|---|---|---|---|---|
| EVT actual | $171.20 | $15.20 (proto rates) | **$186.40** | 50 units |
| DVT estimate | $152.10 | $12.10 | **$164.20** | 200 units |
| **MP target** | **$131.20** | **$10.80** | **$142.00** | 25k/yr |

## Top-Level BOM (major lines, DVT rev 2.1)

| Level | Item | Supplier (fictional where partner) | Qty | EVT $ | DVT $ | MP target $ | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Display 13.3" FHD IPS (NV133FHM) | BOE | 1 | 38.50 | 34.20 | 29.80 | 2nd source: panel B qual at PVT |
| 1 | Touch sensor GFF + lamination | ClearTouch (Suzhou) | 1 | 12.40 | 11.10 | 9.60 | Lamination yield 96.5% |
| 1 | Cover glass AG, ion-exchanged | — | 1 | 6.80 | 6.10 | 5.40 | |
| 1 | Main PCBA (assembled) | BrightPath SMT | 1 | 58.10 | 51.30 | 43.10 | breakdown below |
| 2 | — SoC Genio 700 (MT8390) | MediaTek | 1 | 23.40 | 21.10 | 17.80 | 25k/yr pricing tier |
| 2 | — LPDDR4X 4 GB | Micron | 1 | 7.10 | 6.40 | 5.30 | |
| 2 | — eMMC 64 GB | Kioxia / SanDisk (qual) | 1 | 5.20 | 4.90 | 4.20 | ISS-030 dual source; broker risk +2.10 |
| 2 | — Wi-Fi/BT module MT7921 | — | 1 | 4.60 | 4.20 | 3.60 | |
| 2 | — PMIC + power tree | MediaTek/TI | set | 5.90 | 5.30 | 4.50 | |
| 2 | — 8L HDI bare board | — | 1 | 4.80 | 4.10 | 3.30 | 2-up panel at MP |
| 2 | — Passives/connectors/shields | various | set | 7.10 | 5.30 | 4.40 | shield can added (ISS-025) +0.35 |
| 1 | Payment module SP-30 | NovaPay | 1 | 12.60 | 11.80 | 11.80 | Contract-fixed; carries EMV/PCI certs |
| 1 | Battery pack 5,000 mAh 1S2P | Veltron / DynaCell | 1 | 9.40 | 8.60 | 7.40 | dual source by PVT (R-03) |
| 1 | Camera module 8 MP FF | — | 1 | 3.80 | 3.40 | 2.90 | |
| 1 | Speakers 2×2 W + box | AAC | 2 | 2.60 | 2.40 | 2.10 | + foam gasket (ISS-027) +0.08 |
| 1 | Mechanicals (housings, mid-frame, stand) | BrightPath/VinaMold | set | 16.90 | 11.20 | 9.10 | T1→MP amortization; Mg vs Al pending |
| 1 | USB-C sub-board + cables/flex | — | set | 4.10 | 3.60 | 3.00 | FRU |
| 1 | Misc (gaskets, labels, screws, thermal) | various | set | 3.20 | 2.80 | 2.30 | label change post-85/85 |
| 1 | Packaging (unit box, foam, QSG) | — | set | 2.20 | 1.90 | 1.70 | → [[packaging-spec]] |
| | **Material total** | | | **171.20** | **152.10** | **131.20** | |

## Cost risks & opportunities → details in [[cost-walk]]
- 🔴 eMMC broker scenario +$2.10 (ISS-030) — would eat 70% of the $3 MP tolerance
- 🟡 Mg→Al mid-frame: −$1.85 opportunity, +38 g mass — decision at DVT exit
- 🟢 Display: panel B (2nd source) quote $1.40 under BOE at MP volumes — qual at PVT
- 🟢 Bridge IC deletion already banked in rev B (−$3.20, in DVT estimate)

## BOM data hygiene (PLM)
- BOM rev 2.1 in PLM, ECO-controlled; ECOs to date: 14 (EVT→DVT cut-in list under ECO-0142) — owner [[../../01-Departments/02-npi-program-management/index|NPI & PM]] (bom-eco-plm)
- AVL: 2 sources minimum on A-risk lines (battery, eMMC, display) per 04/24 decision → [[../../00-Brain/decisions-log|log]]
