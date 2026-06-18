---
type: project-doc
project: Cyber
section: pm
tags: [demo, synthetic, risk]
last_updated: 06/17/2026
---
# Project Cyber — Risk Register (sustaining)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Score = Probability (1-5) × Impact (1-5)

| ID | Risk | P | I | Score | Owner | Mitigation | Status |
|---|---|---|---|---|---|---|---|
| R-01 | DynaCell battery lot recurrence (swell) escapes to field → safety/recall exposure | 2 | 5 | 🔴 10 | Grace Lim | 100% incoming X-ray on DC26xx lots; [[capa-8d-CY-26-007\|8D]] containment model; Quanex 2nd source active | Open — monitoring |
| R-02 | **Scan engine single source** (Helios N4200) — allocation, price hike, or quality stop halts line | 3 | 4 | 🔴 12 | Grace Lim | Aurora AX-20 2nd-source EE-qual in ORT; 8-wk safety stock held; LTB clause in Helios contract | Open — qual Q4 2026 |
| R-03 | Field AFR stalls above 3.5% → warranty/advance-exchange cost overrun | 3 | 3 | 🟡 9 | Sofia Ramirez | ECO retrofit-on-RMA for pre-039 fleet; drop-rate education kit for top-3 chains; glidepath review monthly | Open → [[field-reliability-report]] |
| R-04 | Kioxia UFS allocation gap Q1 2027 + QCM6125 SoC EOL window | 3 | 4 | 🔴 12 | Daniel Reyes | SanDisk UFS dual-qual; LTB decision Q4 2026; SoC roadmap aligned to Gen-1.5 study | Open |
| R-05 | Cost-down $148 target missed (display dual-source slips / commodity prices) | 2 | 3 | 🟢 6 | Priya Nair | Crystalview display qual ahead of need; quarterly should-cost re-quote; SoC price erosion banked | Open |
| R-06 | Refurb (CY-80R) pool depletion if AFR spikes during Q4 retail peak | 2 | 4 | 🟡 8 | Carlos Mendez | Pre-stage +400 refurb units before Oct; advance-exchange pool sized to 2% of fleet | Mitigating |
| R-07 | Tariff / logistics shift on Malaysia origin raises landed cost | 2 | 3 | 🟢 6 | Daniel Reyes | Origin documentation current; freight contract locked FY26; China surge line dormant-qualified | Watch |
| R-08 | PCI PTS v6.2 lapses before renewal filed → cannot ship payment SKUs | 1 | 5 | 🟡 5 | Rachel Adeyemi | Renewal filing Q1 2027; no payment-boundary hardware change permitted without re-cert | Open |
| R-09 | CYS-10 cradle pogo wear (ISS-CY-068) becomes a fleet-wide accessory RMA driver | 2 | 2 | 🟢 4 | Tom Becker | Hardness-upgraded pins in production from May; field-swap kit at depot | Mitigating |
| R-10 | Anchor-customer rollout demand spike (+15% Q4) exceeds Meridian capacity | 2 | 3 | 🟢 6 | Wei Lim | Capacity reservation signed; 3rd assembly line on standby; build-ahead buffer | Planned |

## Retired risks
| ID | Risk | Outcome |
|---|---|---|
| R-00a | USB-C port drop fatigue field returns climbing | Closed 10/2025 — ECO-CY-031 bracket; return rate −62% on post-cut units |
| R-00b | Scan window haze in QSR grease environments | Closed 02/2026 — ECO-CY-039 oleophobic coating + [[capa-8d-CY-26-007\|CAPA-007]]; recurrence < 0.3% |
| R-00c | PVT→MP yield stuck at 89% | Closed 06/2025 — touch-cal + scan-aim station rework, FPY 94.5% → [[factory-yield-mp]] |
