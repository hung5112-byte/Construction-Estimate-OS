---
type: project-doc
project: AMG
section: ee
tags: [demo, synthetic, ee, power]
last_updated: 06/10/2026
---
# AMG-100 — Power Budget (EVT measured, rev A)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Marcus Lee · Measured on 8 EVT units, 25 °C, FW 0.8.5

## Use-Case Power (system, at battery)

| Mode | Spec | Measured (avg) | Margin | Notes |
|---|---|---|---|---|
| Off (ship mode) | ≤ 80 µW | 62 µW | 🟢 | Gauge in shutdown |
| Idle, display off, Wi-Fi assoc | ≤ 0.9 W | 0.81 W | 🟢 | Wake on dock/touch |
| Menu browsing (display 300 nits) | ≤ 5.2 W | 4.86 W | 🟢 | Dominant use case, 70% duty |
| Game (GPU mid) + audio | ≤ 7.5 W | 7.92 W | 🔴 −0.42 W | GPU governor tune in FW 0.9 — tracking |
| Payment transaction (NFC field on) | ≤ 6.0 W | 5.41 W | 🟢 | 8 s transaction window |
| Charging (dock, display on) | ≤ 27 W in | 24.3 W | 🟢 | Thermal-limited to 21 W > 38 °C skin |

## Battery Life Model (5,000 mAh ≈ 19.2 Wh, 1S2P)
- Restaurant duty cycle (14 h service day): 70% browse / 20% idle / 8% game / 2% payment → **avg 4.42 W → 4.3 h off-dock**
- Requirement: ≥ 4.0 h off-dock (tables un-docked during service reconfig) → 🟢 pass with 7.5% margin
- End-of-life (80% capacity, 500 cycles): 3.5 h → still > 3.0 h EOL requirement
- Cycle plan: dock-charge to 80% during overnight (battery longevity mode, FW-controlled)

## Rail Budget (key rails, rev A measured at typ load)

| Rail | Source | Volts | Budget | Measured | Margin |
|---|---|---|---|---|---|
| VSYS | BQ25713 | 3.5–4.4 V | 8.5 A pk | 7.1 A pk | 🟢 |
| VCORE (SoC big) | MT6365 BUCK1 | 0.55–1.0 V | 4.0 A | 3.2 A | 🟢 |
| VGPU | MT6365 BUCK2 | 0.55–0.9 V | 3.0 A | 2.9 A | 🟡 game mode, see above |
| VDD_LPDDR | BUCK5 | 1.1 V | 1.2 A | 0.8 A | 🟢 |
| V_PAYMENT (SP-30) | LDO + load switch | 5.0 V | 1.0 A | 0.62 A pk (NFC tx) | 🟢 isolated, brown-out monitored |
| V_DISPLAY | Boost | 5.8 V | 1.4 A | 1.1 A @ 400 nits | 🟢 |

## Thermal tie-in
- Skin temp limit 43 °C (UL + comfort): worst case measured 41.2 °C at game+charge, 25 °C ambient → 🟢 but **fails at 40 °C ambient kitchen-window placement (45.8 °C)** → FW thermal governor caps charge to 15 W above 38 °C skin — verified
- ISS-019 (touch ghosting > 45 °C) is adjacent to payment module heat — shield flex grounding in DVT → [[open-issues]]

## DVT actions
1. GPU governor tune to recover 0.42 W game-mode overage (FW 0.9.0) — re-measure on 10 rev-B units
2. Re-baseline all rails on rev B (shield can may shift PMIC thermals slightly)
3. Validate DynaCell pack impedance vs Veltron (R-03) — gauge profile per source
