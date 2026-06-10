---
type: project-doc
project: AMG
section: fulfillment
tags: [demo, synthetic, logistics]
last_updated: 06/10/2026
---
# AMG-100 — Logistics & Fulfillment Plan

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Dana Schultz · Dept: [[01-Departments/05-service-operations/index|Service Operations]] · 3PL: Alliance Fulfillment Partners, Fort Worth DC
> General information only — customs/trade items to be confirmed with a licensed customs broker/attorney.

## Trade & Customs
| Item | Plan |
|---|---|
| HTS classification | 8471.30 (portable ADP machine) — **0% duty**; binding-ruling request drafted, files 07/15 → [[cert-plan]] #12 |
| Country of origin | **Vietnam** (substantial transformation at BrightPath Bac Ninh) — keeps §301 China tariff exposure at zero; origin memo + BOM-by-origin analysis with customs counsel |
| Dock AMG-D10 | 8504/8443 split analysis in work (printer in dock complicates) — worst case 2.6% duty on dock only |
| Importer of record | LSI (us); customs broker: (fictional) Lone Star Trade Services |
| Incoterms | FOB Haiphong (we own ocean + insurance — control + landed-cost visibility) |

## Freight Plan
| Phase | Mode | Route | Transit | Cost/unit |
|---|---|---|---|---|
| DVT/PVT samples + cert units | Air | SGN/HAN → DFW | 4–6 days | $11.80 |
| **MP M1–M2 (ramp)** | **Air (budgeted)** | HAN → DFW | 5 days | **$3.80 amortized** (mix air/ocean) — covers deploy schedule while ocean pipeline fills → [[cost-walk]] threat table |
| MP steady state | Ocean FCL 40'HC | Haiphong → LA/LB → rail → Fort Worth | 28–32 days | $2.10 |
| Tet buffer (R-07) | Ocean, pre-built +6k units | ship by 01/15/2027 | — | — |

40'HC capacity: 80 units/pallet × 20 pallets = **1,600 units/container** → steady state ~3 containers/month.

## Fort Worth DC Operations
| Function | Plan |
|---|---|
| Inbound | 3 containers/mo steady; receiving QC = customer-sim out-of-box audit 20 units/mo (with [[test-stations]] OQC loop) |
| Inventory policy | 4 weeks forward cover finished goods; ABC: tablets A (cycle count weekly), docks B, FRU kits A (depot-critical) |
| Deployment staging | Site kitting: N tablets + docks + mounting + quick-start; site manifest from ops portal; wave-1 = 38 sites × ~45 units staged across Dec–Jan |
| Advance-exchange pool | 375 units by ramp M3 (1.5% fleet) — co-located with depot → [[rma-process-dashboard]] |
| Systems | 3PL WMS ↔ our ERP via EDI 940/945; SN-level genealogy maintained from factory MES through to site install record |
| Staffing | +2 temps M1–M3; +1 perm from M4 if velocity holds |

## Risks
- Port congestion (LA/LB peak season Oct–Dec) overlaps ramp → mitigation: air-mix budget + 2-week safety stock
- Single 3PL site: fire/weather DR plan = BrightPath holds 1-week FG buffer + direct-ship lane quoted (air) as backup
- eMMC broker buy (ISS-030) would arrive via air to BrightPath — customs pre-cleared component lane exists
