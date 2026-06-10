---
type: project-doc
project: AMG
section: pm
tags: [demo, synthetic, issues]
last_updated: 06/10/2026
---
# Project AMG — Issue Tracker

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Sev-1 = stop-ship/gate-blocker, Sev-2 = must fix before next gate, Sev-3 = fix when able

## Open Issues

| ID | Sev | Title | Found | Owner | Dept | Fix / Plan | Verify at | Status |
|---|---|---|---|---|---|---|---|---|
| ISS-014 | 2 | Wi-Fi 5 GHz throughput −18%: metal display trim detunes main antenna | EVT RF test 04/02 | Elena Rodriguez | [[01-Departments/01-hardware-engineering/index\|HW Eng]] | Re-matched feed + 0.5 mm trim standoff; rework parts ETA 06/16 | DVT build | 🟡 Parts in transit |
| ISS-019 | 3 | Touch ghosting at >45 °C ambient near payment module | EVT thermal 04/11 | David Chen | HW Eng | FW palm-reject tuning v2 + grounded shield flex | DVT PRT | 🟡 FW fix in test |
| ISS-021 | 2 | Battery swelling, Veltron lot VE2605A (3 of 280 cells, 1.8 mm bulge @ 200 cycles) | EVT cycle life 04/18 | James Park | [[01-Departments/04-mfg-supplier-quality/index\|MSQ]] | 8D → [[capa-8d-AMG-26-004]]; lot quarantined; 100% incoming X-ray; DynaCell 2nd source | PVT | 🟡 Contained (D5) |
| ISS-023 | 2 | 1.0 m corner drop: crack at USB-C boss, front housing (3/8 units) | EVT PRT 04/22 | Miguel Torres | HW Eng | Rib + radius added, T1 tool mod done 05/20 ($7k) | DVT PRT drop | 🟡 Fix cut in |
| ISS-025 | 2 | EMC radiated emissions: 5.8 GHz harmonic 1.2 dB OVER limit (pre-scan) | Cert pre-scan 04/29 | David Chen | HW Eng | Shield can over PMIC + ferrite on display flex; DVT PCB rev B | Pre-scan #2 07/14 | 🟡 In DVT rev |
| ISS-027 | 3 | Speaker buzz at max volume, 800 Hz enclosure resonance | EVT audio 04/08 | Miguel Torres | HW Eng | Foam gasket + speaker box rib; EQ notch in FW interim | DVT audio | 🟡 Fix cut in |
| ISS-028 | 3 | Payment module handshake timeout 0.3% of transactions (SP-30 FW) | Alpha trial 05/30 | Anna Volkov | HW Eng | NovaPay FW v2.1.4 fix promised 06/20; retry logic added our side | DVT FW QA | 🟡 Vendor fix pending |
| ISS-030 | 2 | eMMC (Kioxia 64 GB) allocation risk Q4 — coverage thru ramp month 2 only | Sourcing review 05/27 | Linda Gomez | [[01-Departments/02-npi-program-management/index\|NPI & PM]] | SanDisk iNAND qual in DVT; broker buy pre-approved ≤$30k premium | PVT sourcing review | 🟡 Open |
| ISS-031 | 3 | Dock pogo pin wear marks at 5k insertions (spec 30k) | Dock DVT prep 06/03 | Janet Liu | HW Eng | Pin vendor hardness upgrade (Au 0.76 µm); re-test | Dock DVT | 🟡 Open |
| ISS-032 | 3 | Alpha trial: 2 units logged Wi-Fi roam drops between APs during peak hours | Alpha trial 06/05 | Anna Volkov | HW Eng | Roaming aggressiveness FW param; site survey at trial site #2 | DVT field FW | 🆕 New |

## Closed Issues (selection)

| ID | Sev | Title | Resolution | Closed |
|---|---|---|---|---|
| ISS-007 | 2 | Boot loop on 5 EVT units — eMMC timing margin | eMMC driver strength tune, FW 0.8.2 | 04/15 |
| ISS-011 | 3 | Camera flare from bezel gloss | Matte bezel texture (MT-11002) at T1 | 05/20 |
| ISS-016 | 2 | USB-C PD negotiation fail with 3rd-party 65 W chargers | PD stack update + cap change | 05/02 |
| ISS-018 | 3 | MSR read rate 94% (spec ≥98%) on worn cards | Head spring force +15%, guide rib | 05/12 |

## Issue stats for weekly dashboard → [[weekly-dashboard-2026-W23]]
- Open: 10 (Sev-1: 0 · Sev-2: 5 · Sev-3: 5) · Closed to date: 22 · Avg days-to-close: 16
- Gate rule: **DVT exit requires zero open Sev-1/Sev-2 without approved waiver**
