---
type: project-doc
project: AMG
section: production
tags: [demo, synthetic, production, test]
last_updated: 06/10/2026
---
# AMG-100 — Factory Test Station Plan

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Omar Haddad + factory-test-yield team · Line 2 (NPI) / Line 5 (MP), BrightPath

## Station Flow (MP layout, 12 stations)

| # | Station | Time (MP target) | Coverage | Fixture status |
|---|---|---|---|---|
| 1 | SPI + AOI (SMT inline) | inline | Paste, placement, polarity | ✅ line-standard |
| 2 | ICT bed-of-nails | 45 s | Opens/shorts/passives, 42 test points | ✅ EVT-proven, rev B adapter 06/15 |
| 3 | FW download + eFuse provisioning | 90 s (parallel ×4) | Golden image, SN, keys; UART eFuse at MP only | ✅ scripts dry-run |
| 4 | Boot + functional self-test | 60 s | Boot, memory, sensors, RTC | ✅ |
| 5 | **Touch calibration (post-aging)** | 75 s | Cal AFTER 24 h panel relax — EVT pareto fix #1 | 🟡 new buffer rack 06/14 |
| 6 | **RF cal + test (golden-unit method)** | 110 s (parallel ×2) | Wi-Fi TX/RX per chain, BT, NFC field — EVT pareto fix #2 | 🟡 fixture #1 ready; #2 for MP 08/15 ($12k) |
| 7 | Display/camera (auto vision) | 50 s | Pixels, luminance, color, QR decode | ✅ |
| 8 | Audio (anechoic box) | 40 s | SPL, THD, buzz signature 800 Hz watch (ISS-027) | ✅ + buzz FFT added |
| 9 | Payment module pair + transaction sim | 55 s | SP-30 handshake, NFC/EMV/MSR loopback card set | ✅ — timeout counter logs ISS-028 rate per unit |
| 10 | Burn-in / soak | 4 h rack (12 min effective takt) | Thermal + duty script; infant mortality screen | ✅ racks for 5k/mo; expansion quote for 8k |
| 11 | FATP final functional + cosmetic OQC | 90 s + visual | Full I/O, buttons, dock mate, grade-A cosmetic at PVT+ | ✅ |
| 12 | Pack-out + weight check + SN scan | 35 s | Genealogy close, box contents check | ✅ → [[packaging-spec]] |

**Total effective test time: MP target 8.4 min/unit** (EVT actual 14.2) — soak cut 30→12 min effective via parallel racks + data-justified reduction at PVT (needs DVT soak-fail data = 0 to approve) → cost input [[cost-walk]]

## Data & SPC
- All stations log to BrightPath MES → nightly extract to our quality data lake; dashboards: FPY by station, top-10 fail codes, drift charts (RF power, touch linearity, audio THD)
- SPC rules: Western Electric on RF TX power + touch cal offsets; OOC = auto station hold + SMS to MfgE
- Weekly yield review (Thu): Omar + James + Rachel + Kevin → feeds [[weekly-dashboard-2026-W23|weekly dashboard]]

## OQC / AQL (with [[../../01-Departments/03-quality-reliability/index|Q&R]] qc-inspection team)
- OQC sampling: ANSI/ASQ Z1.4, GB level II — AQL 0.65 major / 1.5 minor (cosmetic per grade-A spec at PVT+)
- IQC: displays (lot sample luminance), batteries (100% X-ray until PVT per [[capa-8d-AMG-26-004]]), SP-30 (cert seal check 100%)
- Customer-sim audit: monthly 20-unit out-of-box audit at Fort Worth DC by Service Ops → [[rma-process-dashboard]]
