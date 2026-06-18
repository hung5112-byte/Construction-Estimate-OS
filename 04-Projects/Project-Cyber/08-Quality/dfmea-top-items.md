---
type: project-doc
project: Cyber
section: quality
tags: [demo, synthetic, dfmea]
last_updated: 06/17/2026
---
# CY-80 — DFMEA Top Items (field-updated)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Rachel Adeyemi · Dept: [[01-Departments/03-quality-reliability/index|Quality & Reliability]]
> RPN = Severity × Occurrence × Detection (1–10 each). **O** updated from field returns, not just design estimate.

| # | Item / function | Failure mode | S | O | D | RPN | Controls / status |
|---|---|---|---|---|---|---|---|
| 1 | Display assembly | Crack on 1.2 m drop | 7 | 6 | 2 | 84 | Bumper energy mgmt, bond line, ORT drop; **field #1 (27%)** — drop-education |
| 2 | Battery pack | Cell swell / thermal | 9 | 3 | 3 | 81 | 100% X-ray on flagged lots, fuel-gauge limits, dual source (ISS-CY-070) |
| 3 | Scan engine window | Haze / no-read (grease) | 6 | 4 | 3 | 72 | ECO-CY-039 oleophobic; recurrence < 0.3% (CAPA-007 closed) |
| 4 | USB-C / charge port | Solder fatigue on drop | 6 | 4 | 3 | 72 | ECO-CY-031 bracket; returns −62% |
| 5 | Payment module | Tamper false-trip / EMV wear | 8 | 2 | 3 | 48 | PCI boundary, EMV endurance ORT, depot FRU |
| 6 | Touch controller | Ghosting near NFC | 4 | 4 | 4 | 64 | FW 1.8 reject v2 (ISS-CY-066, OTA) |
| 7 | CY-80L thermal | Throttle > 40 °C | 5 | 4 | 3 | 60 | FW governor + graphite pad eval (ISS-CY-064) |
| 8 | Cradle pogo | Contact wear | 4 | 5 | 3 | 60 | Au upgrade + spring (ISS-CY-068) |
| 9 | Seal / ingress | Liquid past IP54 | 7 | 3 | 4 | 84 | Gasket spec, ORT spill panel; spill-education |
| 10 | MSR head | Read-rate fade on worn cards | 4 | 4 | 3 | 48 | ECO-CY-040 spring/guide; depot FRU |

## How field data changed the DFMEA
- **Display & ingress RPN rose** post-launch — drops/spills occur more than design Occurrence assumed; both now top-RPN and drive the drop/spill-education program with anchor chains.
- **Scan, USB-C RPN fell** after ECOs closed the mechanisms — verified by return-rate, not just lab.
- DFMEA is reviewed each quarter against the [[field-reliability-report]] pareto so Occurrence reflects reality, not the original estimate.
