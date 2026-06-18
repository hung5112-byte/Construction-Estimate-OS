---
type: project-hub
project: Cyber
aliases: ["Project Cyber", "Cyber", "CY-80 Program"]
tags: [demo, synthetic, hub]
last_updated: 06/17/2026
---
# 🛰️ Project Cyber — Program Hub

> ⚠️ **SYNTHETIC DEMO DATA** — Lone Star Interactive Systems (LSI) is a fictional company. All names, suppliers, costs, RMA numbers, and field data on these pages are invented for demonstration. No real company information.

**CY-80** — 8.0" rugged handheld retail/QSR point-of-sale tablet (scan · order · pay) + CYS-10 5-bay cradle + CY-80L LTE variant.
Concept → EVT → DVT → PVT → **MASS PRODUCTION (Year 2)** · SOP 02/2025 · Run rate **100k/yr** · Sponsor: Brian H. Doan (VP) · PM: Daniel Reyes

## 📊 Status at a glance (06/17/2026 — Year-2, month 5)
|          |                                                                       |
| -------- | --------------------------------------------------------------------- |
| Phase    | ✅ In mass production 16 months · ~134k shipped / ~128k active in field |
| Volume   | Y1 actual 92.4k · Y2 plan 100k (run rate ~8.3k/mo) 🟢                  |
| Field    | **AFR 3.9%** (launch 6.8%) → target ≤ 3.5% by Y2-Q4 🟡                 |
| RMA      | ~530 receipts/mo · depot TAT 2.4 d · FTF 93% · NTF 9% 🟡              |
| Quality  | FPY 94.5% (target 95%) · 7 open sustaining issues (0 Sev-1, 3 Sev-2)  |
| BOM      | Launch $168.90 → **$151.20 now** (cost-down target $148) 🟢           |
| Top risk | Single-source scan engine (Helios N4200) — 2nd-source qual in flight  |

## 🗂️ Program documents

### 01 — Program Management ([[01-Departments/02-npi-program-management/index|NPI & PM]])
[[charter|Program charter]] · [[schedule-milestones|History + sustaining roadmap]] · [[risk-register|Risk register]] · [[open-issues|Sustaining issue tracker]] · [[team-roster|Team roster]] · [[meeting-minutes-2026-06-04|Latest MP review 06/04]]

### 02 — Electrical Engineering ([[01-Departments/01-hardware-engineering/index|Hardware Eng]])
[[electrical-architecture|Architecture & block diagram]] · [[power-budget|Power budget & battery life]] · [[schematic-pcb-status|PCB rev / ECO history]]

### 03 — Mechanical Engineering
[[mechanical-design|ID, ruggedization & FRUs]] · [[tooling-tracker|Tooling tracker (amortized)]]

### 04 — Firmware
[[firmware-plan|FW release train & OTA fleet status]]

### 05 — BOM & Cost
[[bom-mp|MP BOM (current rev)]] · [[cost-walk|Cost walk $168.90 → $151.20]]

### 06 — Reliability / ORT ([[01-Departments/03-quality-reliability/index|Quality & Reliability]])
[[ort-plan|Ongoing Reliability Test (in-production)]] · [[mtbf-afr-model|MTBF / AFR model vs field actuals]]

### 07 — Certifications
[[cert-plan|Cert matrix: FCC · ISED · CE/UKCA · UL · EMV · PCI PTS · renewals]]

### 08 — Quality ([[01-Departments/03-quality-reliability/index|Q&R]] + [[01-Departments/04-mfg-supplier-quality/index|MSQ]])
[[dfmea-top-items|DFMEA top-10 (field-updated)]] · [[capa-8d-CY-26-007|8D: scan-engine window haze (Helios)]] · [[factory-yield-mp|MP yield trend 88% → 94.5%]]

### 09 — Production ([[01-Departments/04-mfg-supplier-quality/index|MSQ]])
[[production-plan|Production plan & capacity (100k/yr)]] · [[test-stations|Factory test stations]]

### 10 — RMA & Field ([[01-Departments/05-service-operations/index|Service Ops]])
[[rma-dashboard|RMA & depot dashboard (live field data)]] · [[field-reliability-report|Field reliability report & pareto]]

### 11 — Fulfillment
[[logistics-plan|Logistics, customs, freight]] · [[packaging-spec|Packaging spec]]

### 12 — Data
[[monthly-dashboard-2026-05|Monthly program dashboard — May 2026]]

## 🧠 Brain links
[[00-Brain/strategy|Strategy]] · [[00-Brain/products|Products]] · [[00-Brain/budget|Division budget]] · [[00-Brain/state|Current state]] · [[00-Brain/decisions-log|Decisions log]] · [[00-Brain/headcount|Headcount]]

## 🔁 The story in one paragraph (for demos)
CY-80 is what AMG looks like two years later: a product that survived its own launch. It shipped in Feb 2025 into the harshest tablet environment there is — a retail floor and a QSR line, where handhelds get dropped onto concrete, soaked in grease, and battery-swapped mid-shift. Year 1 hurt: a 6.8% AFR driven by drop-cracked displays, a USB-C port that fatigued, and a barcode scan window that hazed over after nine months of fryer steam. The program answered with the boring machinery of sustaining engineering — five ECOs cut into the line, three field CAPAs (one still open), a depot in Fort Worth turning RMAs in 2.4 days, and a cost-down that walked BOM from $168.90 to $151.20 without touching reliability. AFR is now 3.9% and still falling. The interesting question for the demo isn't "will it launch" — it's "where does the money leak in year 2, and which of the seven open issues is the one that actually matters."
