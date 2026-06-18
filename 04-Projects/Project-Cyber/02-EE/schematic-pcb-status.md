---
type: project-doc
project: Cyber
section: ee
tags: [demo, synthetic, pcb, eco]
last_updated: 06/17/2026
---
# CY-80 — PCB Revision & ECO History

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Priya Nair · Dept: [[01-Departments/01-hardware-engineering/index|Hardware Eng]]

## Main PCBA revision history
| Rev | Released | In production | Change summary |
|---|---|---|---|
| A | EVT 08/2024 | — | First proto |
| B | DVT 10/2024 | — | EMC shield can, touch ground, scan-engine connector |
| C | PVT 12/2024 → SOP | 02/2025–09/2025 | MP release; **ECO-CY-031** USB-C bracket + pad-stack cut mid-rev (09/2025) |
| **D** | 04/2026 | **current** | **ECO-CY-044** battery contact (spring/Au); minor cost-down passives |

## ECO log (production)
| ECO | Title | Driver | Type | Cut-in | Status |
|---|---|---|---|---|---|
| ECO-CY-031 | USB-C reinforcement bracket + pad-stack | ISS-CY-018 drop fatigue | HW | 09/2025 | ✅ Closed — returns −62% |
| ECO-CY-039 | Scan-window oleophobic coating | ISS-CY-024 / CAPA-007 | ME/optics | 02/2026 | ✅ Closed → [[capa-8d-CY-26-007]] |
| ECO-CY-040 | MSR head spring + guide rib | ISS-CY-047 read rate | ME | 03/2026 | ✅ Closed |
| ECO-CY-044 | Battery contact spring +18%, Au plate | ISS-CY-029 | HW/ME | 04/2026 | ✅ Closed (rev D) |
| ECO-CY-048 | Display 2nd source (Crystalview) qual straps | cost-down | EE | — | 🟡 Qual (cut Q3) → [[cost-walk]] |
| ECO-CY-051 | Graphite thermal pad over S1 | ISS-CY-064 LTE throttle | ME | — | 🟡 Eval (FW-first) |
| ECO-CY-052 | Scan-engine 2nd source (Aurora AX-20) footprint enable | R-02 single-source | EE | — | 🟡 ORT — pin/protocol drop-in |

## Design freeze constraints
- **Payment boundary frozen** — any change to SP-25 region, tamper mesh, or its rails triggers PCI PTS re-cert (R-08). ECO-CY-048/051/052 are all routed clear of the secure boundary.
- Cut-in discipline: every ECO carries a line-break SN range + reverse-traceability in PLM (genealogy → [[factory-yield-mp]]).

## Open EE actions
1. Aurora AX-20 (ECO-CY-052) — confirm aim/decode parity in ORT, then release rev E *footprint-compatible* (no spin) — owner Priya, ORT data 07/2026
2. Crystalview display gamma/optical match sign-off (ECO-CY-048) — owner Priya, Q3
