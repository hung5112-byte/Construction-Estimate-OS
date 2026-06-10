---
type: project-doc
project: AMG
section: pm
tags: [demo, synthetic, charter]
last_updated: 06/10/2026
---
# Project AMG — Program Charter

> ⚠️ SYNTHETIC DEMO DATA — fictional program of Lone Star Interactive Systems (LSI).
> Hub: [[Project-AMG-Hub]] · Owner: Sarah Whitfield (PM) · Sponsor: Brian H. Doan (VP)

## Objective
Develop and ramp the **AMG-100** 13.3" restaurant tabletop tablet (+ AMG-D10 dock) from concept to mass production: **MP gate 11/09/2026**, ≤ **$2.0M** program NRE, MP BOM ≤ **$142.00**, year-1 AFR ≤ **2.0%**.

## Business Case
- Replace aging TS-90 (Gen 2, EOL Q2 2027, AFR 3.1%) before fleet refresh cycles begin
- 25,000 units year 1 committed across 3 anchor chain customers (fictional)
- Payment certification (PCI PTS v6.2 + EMV) is the competitive moat — consumer tablets can't follow

## Scope
| In scope | Out of scope |
|---|---|
| AMG-100 tablet (EE/ME/FW/cert/reliability) | Cloud/menu software (Software BU) |
| AMG-D10 charging/printer dock | Kitchen display systems |
| Factory test development at BrightPath | TS-90 sustaining (separate budget) |
| Depot repair readiness + FRU strategy | International SKUs (2027, phase 2) |

## Key Stakeholders
| Role | Who | Department |
|---|---|---|
| Sponsor / gate chair | Brian H. Doan (VP) | Division |
| Program manager | Sarah Whitfield | [[01-Departments/02-npi-program-management/index\|NPI & PM]] |
| EE lead | David Chen | [[01-Departments/01-hardware-engineering/index\|Hardware Eng]] |
| ME lead | Miguel Torres | [[01-Departments/01-hardware-engineering/index\|Hardware Eng]] |
| FW lead | Anna Volkov | [[01-Departments/01-hardware-engineering/index\|Hardware Eng]] |
| Quality lead | Rachel Adeyemi | [[01-Departments/03-quality-reliability/index\|Quality & Reliability]] |
| SQE | James Park | [[01-Departments/04-mfg-supplier-quality/index\|Mfg & Supplier Quality]] |
| ODM PM (resident) | Kevin Tran | BrightPath Bac Ninh |
| Service readiness | Carlos Mendez | [[01-Departments/05-service-operations/index\|Service Operations]] |

## Success Criteria (MP gate)
1. PVT FPY ≥ 92%, MP target 95% by ramp month 3
2. All certs granted or scheduled with zero hardware-change risk: FCC, ISED, UL/cUL 62368-1, EMV L1/L2, PCI PTS v6.2 → [[cert-plan]]
3. BOM at $142.00 ± $3 @ 25k/yr → [[cost-walk]]
4. PRT complete, zero open Sev-1 reliability issues → [[prt-plan]]
5. Two qualified sources for battery, eMMC, display → [[00-Brain/decisions-log|decisions log]]
6. Depot FRU stock + repair SOPs live at Fort Worth → [[rma-process-dashboard]]

## Constraints & Assumptions
- BrightPath DVT line slot fixed at 06/22/2026 — missing it costs +5 weeks
- Payment module is buy-not-build (NovaPay SP-30) per 02/06/2026 decision
- Vietnam origin maintained for tariff position; China line for surge only
- Program contingency $130k; draws > $25k need CCB approval
