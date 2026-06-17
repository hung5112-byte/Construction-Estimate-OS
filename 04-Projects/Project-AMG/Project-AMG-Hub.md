---
type: project-hub
project: AMG
aliases: ["Project AMG", "AMG", "AMG-100 Program"]
tags: [demo, synthetic, hub]
last_updated: 06/10/2026
---
# 🚀 Project AMG — Program Hub

> ⚠️ **SYNTHETIC DEMO DATA** — Lone Star Interactive Systems (LSI) is a fictional company. All names, suppliers, costs, and data on these pages are invented for demonstration. No real company information.

**AMG-100** — 13.3" restaurant tabletop tablet (order/play/pay) + AMG-D10 dock.
Concept → EVT → **DVT (current)** → PVT → MP · Budget **$2.0M** · MP gate **11/09/2026** · Sponsor: Brian H. Doan (VP) · PM: Sarah Whitfield

## 📊 Status at a glance (06/10/2026)
|          |                                                                |
| -------- | -------------------------------------------------------------- |
| Phase    | ✅ EVT exited 05/08 (2 waivers) → **DVT build 06/22** (12 days) |
| Budget   | $872k / $2,000k spent (43.6%) — 🟢 forecast $1,978k            |
| Issues   | 10 open: 0 Sev-1 · 5 Sev-2 · 5 Sev-3                           |
| Top risk | PCI PTS pre-assessment 07/06 (R-01)                            |
| BOM      | EVT $186.40 → MP forecast $142.70 (target $142 ± 3) 🟢         |
| Field    | Alpha trial live: 24 units, 3 sites, uptime 99.1%              |

## 🗂️ Program documents

### 01 — Program Management ([[01-Departments/02-npi-program-management/index|NPI & PM]])
[[charter|Program charter]] · [[schedule-milestones|Schedule & gates]] · [[budget-tracker|Budget tracker ($2M)]] · [[04-Projects/Project-AMG/01-PM/risk-register|Risk register]] · [[open-issues|Issue tracker]] · [[team-roster|Team roster]] · [[meeting-minutes-2026-06-05|Latest minutes 06/05]]

### 02 — Electrical Engineering ([[01-Departments/01-hardware-engineering/index|Hardware Eng]])
[[electrical-architecture|Architecture & block diagram]] · [[power-budget|Power budget & battery life]] · [[schematic-pcb-status|Schematic/PCB status]] · [[evt-ee-test-report|EVT EE test report]]

### 03 — Mechanical Engineering
[[mechanical-design|ID & mechanical design (FRUs)]] · [[tooling-tracker|Tooling tracker ($420k)]] · [[evt-me-test-results|EVT drop/thermal/environmental]]

### 04 — Firmware
[[firmware-plan|FW plan, release train, OTA]]

### 05 — BOM & Cost
[[bom-evt|BOM (EVT→DVT→MP)]] · [[cost-walk|Cost walk $186 → $142]]

### 06 — Reliability / PRT ([[01-Departments/03-quality-reliability/index|Quality & Reliability]])
[[prt-plan|PRT plan (the dinner-rush simulator)]] · [[prt-results-evt|EVT PRT results]] · [[mtbf-prediction|MTBF 62k h & AFR model]]

### 07 — Certifications
[[cert-plan|Cert matrix: FCC · UL · EMV · PCI PTS · trade]]

### 08 — Quality ([[01-Departments/03-quality-reliability/index|Q&R]] + [[01-Departments/04-mfg-supplier-quality/index|MSQ]])
[[dfmea-top-items|DFMEA top-10]] · [[capa-8d-AMG-26-004|8D: battery swelling (Veltron)]] · [[factory-yield-evt|EVT yield 78% & pareto]]

### 09 — Production ([[01-Departments/04-mfg-supplier-quality/index|MSQ]])
[[build-plan|NPI build plan EVT→MP]] · [[test-stations|Factory test stations]] · [[ramp-plan|MP ramp 2k→5k/mo]]

### 10 — RMA & Field ([[01-Departments/05-service-operations/index|Service Ops]])
[[rma-process-dashboard|RMA & depot readiness + TS-90 dashboard]] · [[field-trial-report|Field trials: alpha live, beta plan]]

### 11 — Fulfillment
[[logistics-plan|Logistics, customs, freight]] · [[packaging-spec|Packaging spec]]

### 12 — Data
[[weekly-dashboard-2026-W23|Weekly dashboard W23]]

## 🧠 Brain links
[[00-Brain/strategy|Strategy]] · [[00-Brain/products|Products]] · [[00-Brain/budget|Division budget]] · [[00-Brain/state|Current state]] · [[00-Brain/decisions-log|Decisions log]] · [[00-Brain/headcount|Headcount]]

## 🔁 The story in one paragraph (for demos)
Gen-2 (TS-90) taught us where tabletop tablets die: connectors, displays, batteries, and soda. AMG-100 answers each with design (pogo dock, FRU serviceability, dual-source cells, IP54 + drain channel), discipline (gates, PRT, DFMEA↔issue↔test traceability), and data (alpha trial telemetry already catching Wi-Fi roam and payment-module bugs before DVT freeze). The $2M program is 44% spent, on schedule, with one genuinely scary risk — the PCI pre-assessment on 07/06 — and a paper trail showing exactly what we'll do if it bites.
