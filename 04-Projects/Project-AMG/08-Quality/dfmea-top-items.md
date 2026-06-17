---
type: project-doc
project: AMG
section: quality
tags: [demo, synthetic, quality, dfmea]
last_updated: 06/10/2026
---
# AMG-100 — DFMEA Top Items (RPN ≥ 100)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Rachel Adeyemi · Full DFMEA (214 lines) lives in PLM; this is the working top-10 · S/O/D scale 1–10, RPN = S×O×D

| #   | Item / Failure mode                              | Effect                                          | S   | O   | D   | RPN                             | Action                                                                          | Status                                        | Verify               |
| --- | ------------------------------------------------ | ----------------------------------------------- | --- | --- | --- | ------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------- | -------------------- |
| 1   | Battery cell swelling in field (heat + cycles)   | Housing bulge, thermal event risk, brand damage | 9   | 3   | 5   | **135**                         | Dual source, 100% X-ray incoming, 0.5 mm ORT swell limit, longevity charge FW   | 🟡 Actions in flight → [[capa-8d-AMG-26-004]] | PVT T12              |
| 2   | Payment data path compromise (tamper)            | PCI breach — catastrophic                       | 10  | 2   | 6   | **120**                         | Buy pre-certified SP-30; tamper domain isolated from main SoC; Atlas pre-review | 🟢 design-protected                           | PTS pre-assess 07/06 |
| 3   | Liquid ingress past front gasket (spill)         | Dead unit, RMA                                  | 7   | 4   | 4   | **112**                         | IP54 gasket, drain channel, spill PRT T8 each phase                             | 🟢 EVT pass                                   | DVT T8               |
| 4   | USB-C boss crack on drop                         | Crack propagates → board damage                 | 7   | 4   | 4   | **112**                         | Rib + radius T1 mod (ISS-023)                                                   | 🟡 fix cut in                                 | DVT T4               |
| 5   | eMMC wear-out before 3-yr life (logging duty)    | Boot fail year 2–3                              | 8   | 3   | 4   | 96→**actioned anyway**          | Log-rotation FW cap, wear telemetry in fleet OTA, 64 GB headroom                | 🟢                                            | HTOL T2 + fleet data |
| 6   | Antenna detune by metal trim (assembly variance) | Wi-Fi degraded fleet-wide                       | 6   | 5   | 3   | 90→**108 after EVT** (O raised) | Re-match + standoff (ISS-014); OTA TIS/TRP sample audit per lot                 | 🟡                                            | DVT RF audit         |
| 7   | Dock pogo wear → charge fail                     | Table down nightly                              | 6   | 4   | 4   | 96→**watch**                    | Pin hardness upgrade (ISS-031), sacrificial dock-side design                    | 🟡                                            | Dock DVT T10         |
| 8   | Thermal runaway of charge at hot ambient         | Skin temp, battery stress                       | 8   | 2   | 6   | 96→**watch**                    | FW governor (verified EVT), charge-derate telemetry                             | 🟢                                            | DVT T2/T15           |
| 9   | Sanitizer embrittlement of housing (years)       | Cracks at screw bosses yr 2+                    | 6   | 3   | 6   | 108                             | Resin grade FR + additive verified T9 10k wipes; ORT chemical leg monthly       | 🟡 long-term                                  | ORT trend            |
| 10  | Touch ghosting at high ambient + payment heat    | False orders, guest frustration                 | 5   | 4   | 5   | 100                             | Shield flex grounding + palm-reject v2 (ISS-019)                                | 🟡                                            | DVT T2 leg           |

## Process notes
- DFMEA reviewed at each gate; O/D re-scored from phase test data (item 6 O was raised 3→5 after EVT OTA results — honest scoring, no grade inflation)
- Top-10 RPN items get named owners + verification hooks in [[prt-plan]] — traceability: DFMEA ↔ ISS ↔ PRT test ↔ gate
- PFMEA (process side) owned by BrightPath + [[01-Departments/04-mfg-supplier-quality/index|MSQ]], reviewed at line audit 03/10; next audit pre-PVT 09/15
