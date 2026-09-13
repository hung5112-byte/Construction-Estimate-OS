---
type: brain
section: markup-policy
aliases: ["Markup Policy", "Markups", "Bid Authority Matrix", "Contingency Policy"]
last_updated: 09/12/2026
label: internal
trust_tier: brain
---
# Markup, contingency and bid-authority policy

> ⚠️ **SYNTHETIC DEMO DATA** — fictional policy of Blackland Commercial Builders (BCB). Every rate below is a planning default; the cost engine cites this file when it applies one, and the report says "[POLICY DEFAULT]" until a bid-specific rate replaces it.

## Contingency by estimate class (AACE 56R-08)
| Class | Definition | Default contingency | Expected accuracy |
|---|---|---|---|
| 5 | order of magnitude, $/SF | 15% | −30% / +50% |
| 4 | schematic, assemblies | 10% | −20% / +30% |
| 3 | design development | 7% | −15% / +20% |
| 2 | bid / construction documents | 3% (5% renovation or incomplete MEP) | −10% / +15% |
| 1 | check / pre-bid | 2% | −5% / +10% |

## Markup stack (applied in this order)
1. Direct cost (labor + material + equipment + subcontracts, with waste factors)
2. General conditions (duration-driven staff + temporary facilities) — sanity band 8–15% of direct
3. Contingency (class table above, reconciled to the risk register EMV)
4. Escalation to the bid mid-point using the Turner Building Cost Index (state the index value and date)
5. Builder's risk and general liability insurance: 1.2% of items 1–4 [POLICY DEFAULT — verify with broker]
6. Performance & payment bond: 0.9% of items 1–5 [POLICY DEFAULT — verify with surety; public work per Tex. Gov't Code ch. 2253]
7. Texas sales tax on materials: per contract type (lump-sum: tax in material cost; separated: collected from owner) — Comptroller Pub. 94-116
8. Overhead and profit (fee): 4% industrial · 5% office · 6% retail/medical · 8% TI · 4% public K-12 [POLICY DEFAULT]

## Bid-authority matrix
| Bid value | Fee decision | Contingency below class default | Sign-off |
|---|---|---|---|
| < $5M | Chief Estimator | Chief Estimator | Chief Estimator |
| $5M–$20M | Chief Estimator + President | President | both |
| > $20M or new building type | Executive committee | Executive committee | committee |

## Standing exclusions and qualifications (customize per bid)
- Permit and impact fees by owner unless the bid form says otherwise
- Hazardous materials abatement, unforeseen subsurface conditions, rock excavation (unit price)
- Owner-furnished equipment, FF&E, low-voltage cabling beyond raceway unless in Division 27
- Utility company fees and primary service extensions
- Winter conditions beyond the stated schedule; escalation beyond the stated bid validity (30 days)
