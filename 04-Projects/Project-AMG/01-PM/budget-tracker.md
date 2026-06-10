---
type: project-doc
project: AMG
section: pm
tags: [demo, synthetic, budget]
last_updated: 06/10/2026
---
# Project AMG — Budget Tracker ($2.0M NRE)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Brain: [[../../00-Brain/budget|division budget]]

## Summary (as of 06/10/2026)
- **Budget: $2,000.0k · Committed: $1,247.3k · Spent: $872.4k (43.6%) · Remaining: $1,127.6k**
- Burn rate: ~$145k/month, peaks at DVT (June–July) and PVT (Sept–Oct) builds
- Contingency: $130.0k budget, $18.4k drawn (battery lot scrap, CAPA-26-004) → $111.6k left

## Breakdown by Workstream

| # | Workstream | Budget | Spent | Committed | ETC* | Variance | Notes |
|---|---|---|---|---|---|---|---|
| 1 | EE NRE & PCB respins | $230.0k | $148.2k | $176.0k | $228.5k | +$1.5k 🟢 | 2 respins done; DVT respin in committed |
| 2 | ME design + tooling | $545.0k | $301.5k | $425.0k | $552.0k | −$7.0k 🟡 | T1 mod for ISS-023 rib added $7k |
| 3 | FW / SW NRE | $180.0k | $86.0k | $118.0k | $178.0k | +$2.0k 🟢 | NovaPay integration heavier than planned |
| 4 | Prototype builds (EVT/DVT/PVT) | $385.0k | $128.7k | $262.0k | $381.0k | +$4.0k 🟢 | DVT 200 units PO issued $118k |
| 5 | Certifications | $195.0k | $61.0k | $124.0k | $193.0k | +$2.0k 🟢 | → [[cert-plan]] |
| 6 | Reliability & test lab | $110.0k | $54.3k | $71.0k | $108.0k | +$2.0k 🟢 | EVT PRT done; DVT PRT booked |
| 7 | Factory NRE, fixtures, stencils | $145.0k | $48.9k | $96.0k | $147.0k | −$2.0k 🟡 | +1 RF cal fixture for ISS-014 |
| 8 | Field trial + logistics | $80.0k | $25.4k | $38.0k | $79.0k | +$1.0k 🟢 | 12-site DFW trial starts Sept |
| 9 | Contingency | $130.0k | $18.4k | $18.4k | — | $111.6k left | Battery lot scrap draw 04/24 |
| | **Total** | **$2,000.0k** | **$872.4k** | **$1,328.4k** | **$1,866.5k + cont.** | 🟢 | Forecast at complete: $1,978k |

*ETC = estimate at complete, excl. contingency

## Tooling Detail (inside workstream 2) → [[tooling-tracker]]
| Tool | Vendor | Cost | Status |
|---|---|---|---|
| Housing front (2-cavity) | BrightPath toolroom | $96k | T1 shot 05/20, mod for ISS-023 |
| Housing rear + battery door | BrightPath toolroom | $88k | T1 ok |
| Display bezel + trim | VinaMold (Hanoi) | $64k | T1 ok — metal trim antenna issue ISS-014 |
| Dock AMG-D10 (4 tools) | VinaMold | $112k | T0 06/30 |
| Stamping/diecast brackets | BrightPath | $60k | Done |

## Spend by Month (actuals)
| Month | Spend | Cum. | Event |
|---|---|---|---|
| Nov–Dec 2025 | $74k | $74k | Concept, architecture |
| Jan 2026 | $92k | $166k | C1 gate, ODM kickoff |
| Feb | $118k | $284k | EE NRE peak, tooling kickoff $ |
| Mar | $186k | $470k | EVT build 50 units + tooling milestones |
| Apr | $159k | $629k | EVT test, PRT, battery scrap $18.4k |
| May | $147k | $776k | EVT exit, T1 shots, DVT prep |
| Jun (MTD) | $96k | $872k | DVT material, antenna rework parts |

## Decisions affecting budget
- 02/06 buy-not-build payment module: −$220k NRE avoided, +$11.80/unit BOM → [[../../00-Brain/decisions-log|log]]
- 04/24 battery dual-source: +$28k qual cost (workstream 6/7), contingency-neutral
