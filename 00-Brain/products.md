---
type: brain
section: products
aliases: ["Products", "Services", "Products & Services"]
last_updated: 06/10/2026
---
# Products / Services

> ⚠️ **SYNTHETIC DEMO DATA** — fictional products of Lone Star Interactive Systems (LSI).

## Product List

| Code | Name | Price (B2B, USD) | Margin % | Status |
|---|---|---|---|---|
| AMG100 | AMG-100 — 13.3" tabletop guest tablet (Gen 3) | $329 | 42 | DVT |
| AMGD10 | AMG-D10 — charging/printer dock | $89 | 38 | DVT |
| TS90 | TS-90 — 11.6" tabletop tablet (Gen 2, legacy) | $289 | 35 | MP |
| TS90R | TS-90R — refurbished TS-90 (RMA pool) | $145 | 22 | Active |
| CY80 | CY-80 — 8.0" rugged handheld retail/QSR POS tablet | $349 | 40 | MP (Year 2) |
| CY80L | CY-80L — CY-80 with 4G LTE | $389 | 39 | MP |
| CYS10 | CYS-10 — 5-bay charging/sync cradle | $179 | 41 | MP |
| CY80R | CY-80R — refurbished CY-80 (RMA pool) | $169 | 24 | Active |

> AMG-100 + AMG-D10: MP gate 11/09/2026, program details → [[Project-AMG-Hub]]. AMG-100 sells with a per-device SaaS subscription (Software BU). TS-90 EOL Q2 2027.
> CY-80 family: in mass production since 02/2025 (Year 2), ~100k/yr, program details → [[Project-Cyber-Hub]]. Field AFR 3.9% → target 3.5%.

## Key Features by Product

### AMG-100 (Project AMG) — flagship
- 13.3" FHD 1920×1080 IPS, 400 nits, anti-glare, 10-pt GFF touch (glove/wet-finger tuned)
- MediaTek Genio 700 (MT8390), 4 GB LPDDR4X, 64 GB eMMC 5.1, Android 14 (AOSP, locked launcher)
- Integrated payment: EMV chip + NFC contactless + MSR — PCI PTS POI v6.2 target
- 8 MP front camera (QR / loyalty), 2× 2 W speakers, Wi-Fi 6 + BT 5.2, Ethernet via dock
- 5,000 mAh hot-warm-swap battery, USB-C PD 27 W + dock pogo charging
- Restaurant-grade: IP54 front face, sanitizer-resistant PC+ABS housing, 1.0 m drop, 0–40 °C
- Serviceability: top-5 FRUs (display, battery, main PCBA, payment module, USB-C board) < 12 min swap

### AMG-D10 dock
- Pogo-pin charging, 58 mm thermal receipt printer, RJ45 Ethernet pass-through

### TS-90 (legacy baseline)
- 11.6" HD, MT8168, Android 11, EMV+NFC, AFR 3.1% — field data feeds AMG-100 reliability targets

### CY-80 (Project Cyber) — volume handheld, in mass production
- 8.0" WUXGA 1920×1200 IPS, 450 nits, Gorilla Glass 5, 10-pt bonded touch
- Qualcomm QCM6125, 4 GB LPDDR4X, 64 GB UFS 2.2, Android 13 (AOSP, locked launcher)
- Integrated payment: EMV chip + NFC contactless + MSR — PCI PTS POI v6.2 (granted)
- 2D barcode imager (Helios N4200) — line-bust scan/checkout; 13 MP rear + 5 MP front camera
- 5,000 mAh hot-swap removable battery (dual-source), USB-C PD 18 W + CYS-10 cradle pogo
- Rugged handheld: IP54, 1.2 m drop, MIL-STD-810H, 0–50 °C; 382 g
- CY-80L variant adds 4G LTE Cat-4 + eSIM; serviceability top-5 FRUs < 14 min swap
- Status: MP Year 2, ~134k shipped, field AFR 3.9%, 5 ECOs cut, 3 CAPAs (1 open) → [[Project-Cyber-Hub]]

## Roadmap
- This quarter (Q2 FY26): AMG-100 DVT build (6/22), close ISS-014 antenna + ISS-023 drop fix, PCI PTS lab pre-assessment
- Next quarter (Q3): DVT exit 8/14 → PVT 9/28; cert submissions (FCC/UL/EMV L2); field trial 12 DFW sites
- Q4: PVT exit 10/23 → MP ramp 11/09 (2k/3k/5k per month); first fleet deployment Jan 2027
