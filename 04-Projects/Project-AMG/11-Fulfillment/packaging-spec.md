---
type: project-doc
project: AMG
section: fulfillment
tags: [demo, synthetic, packaging]
last_updated: 06/10/2026
---
# AMG-100 — Packaging Specification

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-AMG-Hub]] · Owner: Dana Schultz + Janet Liu (structural) · Verified: ASTM D4169 truck profile, EVT first-article → [[prt-results-evt]] T6

## Unit Box
| Parameter | Spec |
|---|---|
| Contents | Tablet, quick-start guide, cleaning guidance card (sanitizer do/don't) |
| NOT included | Charger/dock (B2B — docks ship separately per site config; cuts box volume 40%) |
| Box | B-flute kraft, 350 × 250 × 95 mm, flexo 1-color (litho deleted at MP, −$0.30 → [[cost-walk]]) |
| Cushion | Molded pulp end caps (no EPS — waste-stream preference of chain customers) |
| Unit gross weight | 1.95 kg |
| Drop spec (packaged) | 76 cm, 10-drop, ISTA-style — ✅ EVT pass |

## Master Carton & Pallet
| Level | Config |
|---|---|
| Master carton | 4 units, 520 × 370 × 210 mm, 8.4 kg |
| Pallet (48×40 GMA) | 20 cartons (4 layers × 5) = **80 units/pallet**, 1.12 m height, stretch + corner boards |
| 40'HC container | 20 pallets = **1,600 units** → [[logistics-plan]] |
| Dock AMG-D10 | Own box, 2/master; site-kit shrink-wrapped pallet mix allowed for deployment staging |

## Labeling
- Unit box: SN + MAC barcodes (Code-128) + QR (links to install app), no consumer branding (B2B plain)
- Carton: SSCC-18 license plate, contents SN range list; pallet: SSCC + ASN via EDI 856
- Compliance marks on unit rear label, not box (e-label strategy → [[cert-plan]])
- Country of origin "Made in Vietnam" — box + unit label (customs requirement)

## Site-kit (deployment unit, staged at DC)
1 kit = 45 tablets (typical site) + 12 docks + mounting hardware box + site manifest. Kit BOM controlled in ERP; pick-accuracy target 99.95% (3PL SLA).

## Sustainability notes
Pulp + kraft = curbside recyclable; box-less bulk option (reusable totes) under study with anchor customer ops teams for 2027 waves — potential −$1.10/unit, parked until after ramp.
