---
type: project-doc
project: Cyber
section: pm
tags: [demo, synthetic, schedule]
last_updated: 06/17/2026
---
# Project Cyber — History & Sustaining Roadmap

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · 📅 Today: 06/17/2026

## Original NPI Gate History (closed program)

| Gate | Phase | Plan | Actual | Result |
|---|---|---|---|---|
| C0 | Concept approval | 03/2024 | 03/11/2024 | ✅ Business case + $2.4M approved |
| C1 | Architecture / planning | 05/2024 | 05/20/2024 | ✅ EE/ME locked, Meridian signed |
| EVT | Engineering validation | 08/2024 | 08/19/2024 (60 units) | ✅ w/ 3 waivers |
| DVT | Design validation | 10/2024 | 10/28/2024 (220 units) | ✅ Full PRT pass |
| PVT | Production validation | 12/2024 | 12/16/2024 (600 units) | ✅ FPY 89% at exit |
| **SOP / MP** | Start of production | 02/2025 | 02/10/2025 | ✅ Ramp 4k→6k→8k/mo |
| Launch | First chain rollouts | 03/2025 | 03/17/2025 | ✅ 4 anchor chains |
| — | Program financial close | 03/2025 | 03/31/2025 | ✅ $2.32M / $2.4M (3.3% under) |

> Program retrospective lessons (drop, scan window, USB-C) fed directly into the FY26 ECO list below → [[00-Brain/decisions-log\|decisions log]].

## Production Milestones (actual)
| Milestone | Date | Note |
|---|---|---|
| 50k cumulative shipped | 09/2025 | First reliability re-baseline (AFR 5.1%) |
| ECO-CY-031 USB-C bracket cut-in | 09/2025 | Drop-fatigue fix, line break SN ≥ CY5A-2xxxx |
| 100k cumulative shipped | 02/2026 | End of Year 1 (92.4k Y1 net of cradle/accessory) |
| ECO-CY-039 scan-window coating | 02/2026 | CAPA-007 permanent fix |
| ECO-CY-044 battery contact spring | 04/2026 | Intermittent-charge fix |
| **Today — 134k shipped** | 06/2026 | Y2 month 5, AFR 3.9% |

## Sustaining / Lifecycle Roadmap (FY26 → EOL)

| Item | Owner | Target | Status |
|---|---|---|---|
| Cost-down Phase 2 → BOM $148 (display dual-source, SoC erosion, mech re-source) | Priya Nair | Q3 2026 | 🟢 On plan ($151.20 today) → [[cost-walk]] |
| **Scan engine 2nd source** (Aurora AX-20 qual) — close single-source risk | Grace Lim | Q4 2026 EE-qual, MP Q1 2027 | 🟡 Qual lot in ORT → [[risk-register]] |
| ANZ market add (RCM cert) for AU/NZ rollout | Certification team | Q3 2026 | 🟢 Lab booked → [[cert-plan]] |
| PCI PTS v6.2 renewal filing (expiry 2027) | Rachel Adeyemi | File by Q1 2027 | 🟢 Tracking |
| UFS / SoC EOL & last-time-buy plan (Kioxia, QCM6125) | Daniel Reyes | LTB decision Q4 2026 | 🟡 Watch → R-04 |
| CY-80 **Gen-1.5 refresh study** (550-nit display, GG6, scan engine swap) | Brian H. Doan | Concept gate Q4 2026 | 🟢 Study only |
| EOL plan: production through 2028, customer last-time-buy notice | Daniel Reyes | Draft Q2 2027 | ⚪ Not started |

## Critical Path (sustaining watch items)
1. **Scan engine 2nd source** — single Helios source is the one supply risk that can stop the line (R-02); Aurora AX-20 EE-qual must clear ORT by Q4 2026
2. **UFS allocation** — Kioxia coverage firm only through Q1 2027; SanDisk qual + LTB decision needed (R-04)
3. **AFR glidepath** — must reach 3.5% by Y2-Q4 to hit warranty-cost plan; gated on pre-ECO-039 fleet aging out via RMA retrofit
4. Cost-down $148 gate — display dual-source (Crystalview) qual completion Q3

## Holiday / capacity notes
- 🟡 Meridian Penang: Hari Raya shutdown (1 wk, ~04/2027) — pre-build buffer planned
- 🟡 Q4 retail peak (Oct–Dec): anchor-customer store rollouts push demand +15% — capacity reservation confirmed with Meridian
