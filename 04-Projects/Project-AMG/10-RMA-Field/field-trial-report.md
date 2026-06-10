---
type: project-doc
project: AMG
section: rma
tags: [demo, synthetic, field-trial]
last_updated: 06/09/2026
---
# AMG-100 — Field Trials: Alpha (running) + Beta Plan

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Sarah Whitfield + Anna Volkov (data) · Sites are fictional DFW restaurants

## Alpha Trial — LIVE (started 05/26/2026)
- **24 EVT units, 3 sites** (2 casual-dining, 1 fast-casual; staff-guided guest use)
- Purpose: early reliability/UX signal before DVT freeze — R-10 mitigation
- FW: 0.8.5 + telemetry package (uptime, crashes, thermals, battery, Wi-Fi events, transaction sim — **no real payment data, payment module in demo mode until PCI grant**)

### Week 1–2 Results (05/26–06/08)
| Metric | Value | Target (PVT) | Notes |
|---|---|---|---|
| Uptime | 99.1% | ≥ 99.5% | Driver: SP-30 handshake timeouts (ISS-028) |
| Crashes / 24 h / unit | 0.21 | < 0.1 | Same driver — NovaPay v2.1.4 expected 06/20 |
| Wi-Fi roam drops | 2 events (site 2) | 0 | AP handoff aggressiveness → ISS-032, FW 0.9.0 param |
| Thermal events (governor trips) | 3 (all at window-adjacent tables, afternoon sun) | informational | Governor worked as designed → [[power-budget]] |
| Battery: avg drop during 90-min un-docked service window | 22% | ≤ 30% | 🟢 healthy margin |
| Physical: drops/spills observed | 2 spills (soda), 1 knock-over | survive | ✅ both spills survived, drain channel praised by ops staff |
| Staff qualitative | "wipe-down feels safe", "want brighter at window tables" | — | Window-table brightness request logged for product (450-nit panel = cost +$2.60, **declined** — placement guidance instead) |
| Sanitizer wear (visual, 2 wks) | none visible | — | W-02 monitoring continues |

## Beta Trial — PLANNED (09/08/2026, 4 weeks)
- **40 DVT units, 12 DFW sites** (allocation in [[build-plan]]), unguided guest use, full menu/game app stack from Software BU
- Entry: FW 0.9.5, ISS-028 verified closed, sites surveyed for AP layout (ISS-032 learning)
- Exit criteria → feeds PVT exit gate:
  1. Uptime ≥ 99.5% across sites
  2. Zero Sev-1 field issues; DOA = 0 on install
  3. NTF-style false claims ≤ 1 (validates on-device diag codes)
  4. Guest transaction sim completion ≥ 99.8% (demo mode)
  5. Ops staff CSAT ≥ 4.2/5 (survey, n ≥ 36 staff)
- Data: daily telemetry rollup to quality data lake; weekly readout in core team → [[weekly-dashboard-2026-W23|dashboard format]]

## Trial logistics
Install/training by Service Ops (Carlos) — dry-run of real deployment playbook; site swap kits (2 spare units/site) pre-staged at Fort Worth DC → [[logistics-plan]]
