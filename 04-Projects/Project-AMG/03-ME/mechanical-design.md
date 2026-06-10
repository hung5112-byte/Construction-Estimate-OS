---
type: project-doc
project: AMG
section: me
tags: [demo, synthetic, me]
last_updated: 06/10/2026
---
# AMG-100 — Mechanical Design & ID

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Miguel Torres (ME lead) · Dept: [[../../01-Departments/01-hardware-engineering/index|Hardware Engineering]]

## Industrial Design Intent
Restaurant tabletop: wedge stand profile (28° screen angle), grab-handle top edge, payment module front-right at natural card reach. Survives nightly sanitizer wipe-downs and the occasional soda bath.

## Envelope & Mass
| Parameter | Spec | EVT actual |
|---|---|---|
| Dimensions (W×H×D) | 322 × 218 × 64 mm (with stand) | 322.4 × 218.1 × 63.8 |
| Mass | ≤ 1,450 g | 1,418 g |
| Screen angle | 28° fixed | 28° |
| Tip-over (15° table tilt + 25 N top push) | no tip | ✅ pass |

## Stack-up (front to back)
1. Cover glass 1.1 mm AG-etched, ion-exchange strengthened, 2.5D edge
2. GFF touch sensor, direct-bond (OCA) to glass
3. 13.3" IPS panel (BOE) in aluminum trim frame ← **trim caused antenna detune ISS-014; DVT adds 0.5 mm dielectric standoff**
4. Mid-frame: Mg-Al die-cast — display + PCBA mounting, thermal spreader path
5. Main PCBA + shield cans, battery 1S2P in steel cage
6. Rear housing PC+ABS (Sabic FR grade + antimicrobial additive), brass inserts ×8
7. Stand: ZDC2 zinc die-cast core, TPE foot pads, cable channel

## Materials & Finishes
| Part | Material | Finish | Why |
|---|---|---|---|
| Front housing | PC+ABS FR | MT-11002 matte texture | Camera flare fix (ISS-011); hides wipe scratches |
| Rear housing | PC+ABS FR + antimicrobial | Same matte | Sanitizer resistance — W-02 waiver: ΔGloss spec relaxed 5→8 → [[prt-results-evt]] |
| Mid-frame | AZ91D Mg or ADC12 Al | — | Cost trade open: Mg −38 g / Al −$1.85 — decide at DVT exit |
| Gaskets | Si foam, IP54 front face | — | Spill protection (60 ml pour test) |

## Serviceability (FRU design) — with [[../../01-Departments/05-service-operations/index|Service Ops]]
| FRU | Fasteners | Target time | EVT teardown |
|---|---|---|---|
| Display module (glass+touch+panel) | 6× T6 + 2 clips | < 4 min | 3:40 ✅ |
| Battery pack | 2× T6, blind-mate conn | < 2 min | 1:55 ✅ |
| Main PCBA | 8× T6 | < 5 min | 5:30 🟡 cable dressing fix in DVT |
| Payment module SP-30 | 2× T6 + tamper label | < 3 min | 2:50 ✅ (PCI re-key procedure applies) |
| USB-C sub-board | 2× T6 | < 2 min | 1:40 ✅ |

## Thermal Design
- Passive only (no fan — grease + mid-frame spreading, rear vent slots top edge)
- Worst case 40 °C ambient: SoC 88 °C (limit 95), skin 45.8 °C at kitchen-window placement → FW governor caps charge (see [[power-budget]])

## Open ME items
- ISS-023 USB-C boss crack: rib + radius T1 mod verified 10-shot — confirm at DVT drop → [[open-issues]]
- ISS-027 speaker buzz: foam gasket + box rib in DVT BOM
- ISS-031 dock pogo wear: pin hardness upgrade w/ vendor
- Mg vs Al mid-frame cost/mass decision — input to [[cost-walk]] at DVT exit
