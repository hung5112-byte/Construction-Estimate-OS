# P-SCM-03: Landed Cost Model

#### Description
A per-product landed-cost workbook — unit cost + freight + duty/tariff + fees + inventory-in-transit cost — so sourcing and site decisions compare total cost, not unit price. Built with the logistics coordinator's current rates.

#### Information to collect (ask the user before generating)
1. Products and origins to model? (e.g. device A from China vs. Mexico)
2. Current HTS classification and duty/tariff rates? [verify with the customs
   broker — Section 301 and similar tariffs change]
3. Freight modes/lanes used (ocean/air) with current rates?
4. Incoterms with each supplier?
5. Volume assumptions (units per shipment/container)?

#### Suggested template
Structure (per product × origin scenario):
- **Inputs**: ex-works unit cost, units/carton, cartons/pallet, container fill
- **Freight**: ocean and air rates per lane, consolidation assumptions,
  cost-per-unit at given fill
- **Duty & tariffs**: HTS code, base duty %, additional tariffs (e.g. §301)
  [UNCERTAIN — verify current rates], MPF/HMF fees
- **Other**: broker fees, insurance, drayage, inventory carrying cost in transit
  (transit days × cost of capital)
- **Output**: landed cost per unit per scenario, side-by-side comparison,
  break-even volume between scenarios
- **Sensitivity**: tariff ±X%, freight ±Y% — which decision flips

Confirm the structure before generating.

#### File-generation prompt
```
Create a Landed Cost Model workbook (.xlsx).

CONTEXT:
- Scenarios: [product × origin list] — Incoterms: [terms]
- HTS/duty: [codes + rates, flag unverified] — Freight rates: [current]

FORMAT (.xlsx):
- Sheet "Inputs": all rates and assumptions, dated, with source notes
- Sheet per scenario: cost build-up from ex-works to landed unit cost
- Sheet "Comparison": scenarios side by side + break-even volumes
- Sheet "Sensitivity": tariff/freight swing table

RULES: every duty/tariff cell carries a verify-with-broker note and an
as-of date; no rate without a source.
```

---
✍️ Author: Brian H. Doan
