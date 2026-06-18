---
type: project-doc
project: Cyber
section: pm
tags: [demo, synthetic, charter]
last_updated: 06/17/2026
---
# Project Cyber — Program Charter (sustaining phase)

> ⚠️ SYNTHETIC DEMO DATA — fictional program of Lone Star Interactive Systems (LSI).
> Hub: [[Project-Cyber-Hub]] · Owner: Daniel Reyes (PM) · Sponsor: Brian H. Doan (VP)

## Objective
Sustain and optimize the **CY-80** 8.0" rugged handheld POS tablet (+ CYS-10 cradle, CY-80L LTE variant) through its mass-production lifecycle: hold **100,000 units/yr**, drive field **AFR ≤ 3.5%**, walk BOM to **≤ $148.00**, and keep all certifications and second sources current through planned EOL (2028).

> The original NPI program (concept → MP, $2.4M) closed **03/2025** at $2.32M. This charter governs the **sustaining/lifecycle phase**.

## Business Case
- CY-80 is LSI's volume handheld: 92.4k shipped Year 1, 100k committed Year 2 across 6 retail/QSR chain customers (fictional)
- Margin protection: every $1 of BOM cost-down at 100k/yr = **$100k/yr** to the division; every 0.5% of AFR avoided ≈ **$215k/yr** in warranty + advance-exchange cost
- Payment certification (PCI PTS v6.2 + EMV L1/L2) + 2D scan engine is the moat vs. consumer tablets and phone-based mPOS

## Scope
| In scope | Out of scope |
|---|---|
| CY-80 sustaining (EE/ME/FW/cert/reliability) | Cloud/POS software (Software BU) |
| CY-80L LTE variant + CYS-10 cradle | Kitchen display & receipt printers (3rd-party) |
| ECO / CAPA / cost-down execution | New-platform Gen-2 NPI (separate charter, study only) |
| Field RMA, depot, refurb (CY-80R) | International SKUs beyond EU/ANZ (phase 3) |
| Component EOL & second-source management | — |

## Key Stakeholders
| Role | Who | Department |
|---|---|---|
| Sponsor / review chair | Brian H. Doan (VP) | Division |
| Program manager (sustaining) | Daniel Reyes | [[01-Departments/02-npi-program-management/index\|NPI & PM]] |
| EE sustaining lead | Priya Nair | [[01-Departments/01-hardware-engineering/index\|Hardware Eng]] |
| ME sustaining lead | Tom Becker | [[01-Departments/01-hardware-engineering/index\|Hardware Eng]] |
| FW lead | Raj Mehta | [[01-Departments/01-hardware-engineering/index\|Hardware Eng]] |
| Quality / reliability lead | Rachel Adeyemi | [[01-Departments/03-quality-reliability/index\|Quality & Reliability]] |
| Supplier quality (resident) | Grace Lim | [[01-Departments/04-mfg-supplier-quality/index\|Mfg & Supplier Quality]] |
| ODM PM (resident) | Wei Lim | Meridian EMS, Penang |
| Service / depot owner | Carlos Mendez | [[01-Departments/05-service-operations/index\|Service Operations]] |
| RMA / field-quality analyst | Sofia Ramirez | [[01-Departments/05-service-operations/index\|Service Operations]] |

## Success Criteria (FY26 sustaining)
1. Field AFR ≤ 3.5% by Y2-Q4 (rolling 3-mo annualized) → [[field-reliability-report]]
2. FPY ≥ 95% sustained at Meridian → [[factory-yield-mp]]
3. BOM ≤ $148.00 at 100k/yr without reliability regression → [[cost-walk]]
4. All certs maintained; ANZ (RCM) added Q3; PCI PTS renewal on file before expiry → [[cert-plan]]
5. Two qualified sources for battery cell, UFS, **and scan engine** (the open gap) → [[00-Brain/decisions-log\|decisions log]]
6. Depot TAT ≤ 3 days, NTF ≤ 8%, refurb pool ≥ advance-exchange demand → [[rma-dashboard]]

## Constraints & Assumptions
- Malaysia (Meridian Penang) origin maintained for tariff position; no second factory funded in FY26
- Scan engine (Helios N4200) is single-source — qualifying Aurora AX-20 as 2nd source is the top sustaining risk (R-02)
- QCM6125 SoC and Kioxia UFS both face EOL/allocation windows in 2027 — last-time-buy planning required
- Cost-down draws on tooling/contingency > $25k need CCB approval
- Warranty terms: 2-yr standard, advance-exchange next-business-day SLA*

*General information only — warranty/SLA and any customer-contract language to be confirmed with a licensed Texas attorney.
