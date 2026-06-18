---
type: project-doc
project: Cyber
section: cert
tags: [demo, synthetic, certification]
last_updated: 06/17/2026
---
# CY-80 — Certification Matrix (maintained)

> ⚠️ SYNTHETIC DEMO DATA · Hub: [[Project-Cyber-Hub]] · Owner: Certification team / Rachel Adeyemi · Dept: [[01-Departments/02-npi-program-management/index|NPI & PM]]
> General regulatory information only — submissions/renewals to be confirmed with the relevant accredited labs and a licensed attorney where contracts are involved.

## Granted & maintained
| Cert                              | Market           | Granted | Expiry / renewal      | Status                 |
| --------------------------------- | ---------------- | ------- | --------------------- | ---------------------- |
| FCC Part 15 B/C                   | US               | 01/2025 | per-device, stable    | 🟢                     |
| ISED RSS                          | Canada           | 01/2025 | stable                | 🟢                     |
| CE (RED, EMC, LVD)                | EU               | 02/2025 | self-decl maintained  | 🟢                     |
| UKCA                              | UK               | 02/2025 | maintained            | 🟢                     |
| UL/cUL 62368-1                    | US/CA safety     | 12/2024 | factory follow-up     | 🟢                     |
| EMV L1/L2 (contact + contactless) | global payment   | 12/2024 | kernel version-locked | 🟢                     |
| **PCI PTS POI v6.2**              | payment security | 01/2025 | **renewal due 2027**  | 🟡 file Q1 2027 (R-08) |
| RoHS / REACH / WEEE               | EU enviro        | 02/2025 | maintained            | 🟢                     |

## In progress
| Cert | Market | Why | Status |
|---|---|---|---|
| RCM | Australia / NZ | ANZ chain rollout (roadmap) | 🟡 Lab booked Q3 2026 → [[schedule-milestones]] |

## Change-control rules (the cert tripwires)
1. **PCI PTS v6.2 + EMV** — any change inside the payment secure boundary (SP-25 module, tamper mesh, its rails, secure FW) forces re-cert. ECO-CY-048/051/052 are all routed clear of it → [[schematic-pcb-status]].
2. **FCC/CE RF** — scan-engine 2nd source (Aurora AX-20) and any antenna/Wi-Fi change need RF delta review; Aurora is non-radiating (imager) so low risk, but confirm in qual.
3. **Renewal discipline** — PCI PTS expiry 2027 is on the lifecycle roadmap; filing must precede expiry or payment SKUs cannot ship (R-08).

## Risk
- 🟡 R-08 PCI PTS renewal — owner Rachel; filing Q1 2027; freeze on payment-boundary hardware until renewed.
