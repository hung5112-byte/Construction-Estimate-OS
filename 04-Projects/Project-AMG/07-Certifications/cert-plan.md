---
type: project-doc
project: AMG
section: certs
tags: [demo, synthetic, certification]
last_updated: 06/10/2026
---
# AMG-100 — Certification & Compliance Plan

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Rachel Adeyemi · Dept: [[../../01-Departments/02-npi-program-management/index|NPI & PM]] (certification team) + [[../../01-Departments/03-quality-reliability/index|Q&R]]
> Labs (fictional): Pinnacle Compliance (Plano, TX) — FCC/ISED/UL · Atlas Security Labs — PCI/EMV

## Certification Matrix

| # | Cert / Mark | Standard | Lab | Samples | Submit | Grant (plan) | Cost | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | FCC Part 15B (unintentional) | ANSI C63.4 | Pinnacle | 3 DVT | 08/18 | 10/02 | $14k | 🟡 Pre-scan #1 failed 5.8 GHz harmonic +1.2 dB (ISS-025); fix in rev B, **pre-scan #2 07/14** |
| 2 | FCC Part 15C/15E (Wi-Fi/BT intentional) | KDB 558074 etc. | Pinnacle | 3 DVT | 08/18 | 10/09 | $28k | 🟡 Depends on antenna fix ISS-014 — OTA re-verify in DVT |
| 3 | ISED Canada (RSS-247/Gen) | — | Pinnacle (co-test) | shared | 08/18 | 10/09 | $9k | 🟢 rides FCC test data |
| 4 | UL/cUL 62368-1 (safety) | UL 62368-1 3rd ed | Pinnacle (UL CB) | 4 DVT + parts | 08/11 | 10/16 | $32k | 🟢 Pre-review done 05/14; battery pack UL 2054 cert from cell vendors on file — **DynaCell cert doc due 06/30** (R-03) |
| 5 | **EMV L1 contact + contactless** | EMVCo | via NovaPay module | module-level | — | inherited | in module $ | ✅ SP-30 carries L1; **integration-level field test** at Atlas 07/06 wk |
| 6 | **EMV L2 kernel** | EMVCo | Atlas | 2 DVT | 08/25 | 10/30 | $38k | 🟡 Kernel config on FW 0.9.x; freeze at 1.0.0-RC |
| 7 | **PCI PTS POI v6.2** | PCI SSC | Atlas | 4 DVT + docs | 09/01 | 11/20* | $52k | 🔴 **Top program risk R-01** — pre-assessment 07/06–07/10; *grant lands after MP gate → ship-hold on payment activation until grant (fleet activates via OTA) — accepted by VP 03/2026 |
| 8 | Wi-Fi Alliance (Wi-Fi 6) | WFA | module cert + derivative | 2 PVT | 09/28 | 10/30 | $11k | 🟢 derivative of MT7921 module cert |
| 9 | Bluetooth SIG QDID | BT 5.2 | derivative listing | docs | 09/28 | 10/16 | $5k | 🟢 |
| 10 | CA Prop 65 / RoHS / REACH | — | supplier decs + XRF audit | docs | 08/01 | 09/15 | $6k | 🟢 87% supplier decs collected |
| 11 | DOE Level VI (adapter) | — | adapter vendor cert | docs | — | on file | $0 | ✅ |
| 12 | HTS/origin ruling (Vietnam) | CBP | customs counsel | docs | 07/15 | 09/01 | $8k | 🟢 substantial-transformation memo drafted → [[logistics-plan]] |

**Cert budget: $195k · committed $124k · spent $61k** → [[budget-tracker]]

## Critical Path & Logic
1. **ISS-025 EMC fix must pass pre-scan #2 on 07/14** — formal FCC submit 08/18 has zero slack to PVT-exit cert-grant need (10/23)
2. **PCI PTS pre-assessment 07/06**: any finding touching the secure boundary → hardware change → PVT slip 4–6 wks (R-01). Design choice that protects us: PCI scope confined to NovaPay SP-30 module; our main board stays outside the tamper boundary
3. PTS final grant 11/20 lands **after** MP 11/09 → mitigation: units ship with payment disabled, OTA-activate on grant (precedent: TS-90 launch 2023)
4. Any PCB change after 08/18 = FCC retest $14–28k + 6 wks → **rev C must be cosmetic/DFM only**

## Label & Documentation
- E-label (FCC ID, IC) in Android settings + physical UL mark on rear housing; artwork rev 3 in PLM under ECO-0151
- Cert binder: declarations, test reports, cell certs, adapter certs — maintained by certification team; audit-ready for customer security reviews
