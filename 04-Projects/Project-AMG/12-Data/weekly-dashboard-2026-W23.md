---
type: project-doc
project: AMG
section: data
tags: [demo, synthetic, dashboard]
last_updated: 06/08/2026
---
# AMG Program Dashboard — Week 23 (06/01–06/07/2026)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Auto-compiled from MES/PLM/telemetry extracts + workstream inputs · Owner: Sarah Whitfield

## Program Health: 🟢 GREEN · 12 days to DVT build

| Dimension | Status | Driver |
|---|---|---|
| Schedule | 🟢 | DVT 06/22 holds; antenna kits = only watch item (ETA 06/16, buffer 3 days) |
| Budget | 🟢 | $872.4k / $2,000k (43.6%); forecast-at-complete $1,978k → [[budget-tracker]] |
| Quality / issues | 🟡 | 10 open (0 Sev-1, 5 Sev-2) — all Sev-2 have DVT closure paths → [[open-issues]] |
| Risk | 🟡 | R-01 PCI pre-assessment 07/06 = biggest single exposure → [[risk-register]] |
| Supply | 🟡 | eMMC Q4 coverage gap (ISS-030); battery 8D at D6 → [[capa-8d-AMG-26-004]] |

## KPI Snapshot

| KPI | This week | Last week | Target | Trend |
|---|---|---|---|---|
| Open issues (Sev-2) | 5 | 6 | 0 by DVT exit | ↓ 🟢 |
| Avg issue age (days) | 23 | 26 | < 30 | ↓ 🟢 |
| DVT material on-dock | 94% | 87% | 100% by 06/18 | ↑ 🟢 |
| Alpha trial uptime | 99.1% | 98.9% | ≥ 99.5% (PVT) | ↑ 🟡 |
| Alpha crashes /24 h/unit | 0.21 | 0.24 | < 0.1 | ↓ 🟡 (ISS-028 fix 06/20) |
| Budget burn vs plan | 100.4% | 99.8% | ≤ 105% | 🟢 |
| Cert pre-scan readiness (ISS-025 fix) | rev B released | — | pre-scan #2 07/14 | 🟢 |
| Tooling: tools at T1+ | 11/12 | 11/12 | dock T0 06/30 | 🟢 |

## This week's highlights
1. Rev B PCB released to fab 06/02 — shield can (ISS-025) + antenna re-match (ISS-014) + SanDisk straps (ISS-030) all in
2. Veltron permanent fix #1 (dehumidifier interlock) confirmed done; audit 06/26
3. Alpha trial: 2 soda spills survived in the wild — drain channel validated by reality 🥤
4. Issue ISS-032 opened (Wi-Fi roam at site 2) — param fix already in FW 0.9.0 scope

## Next week (W24) must-do
- 06/12: DVT Build Readiness Review (extended core team) → [[meeting-minutes-2026-06-05|last minutes]]
- 06/12: antenna kit AWB confirmation deadline (A-118, Elena)
- 06/13: rev B fab on-dock BrightPath · 06/16: antenna kits on-dock · 06/18: FW 0.9.0 freeze
- 06/20: NovaPay v2.1.4 delivery (ISS-028) — escalation letter ready if missed

## Data sources
BrightPath MES (yield/genealogy) · PLM (BOM/ECO: rev 2.1, 14 ECOs) · fleet telemetry (24 alpha units) · workstream trackers in this folder → [[Project-AMG-Hub]]
