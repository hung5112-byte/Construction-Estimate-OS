---
type: clarification
answered: true
---

# 🤖 Questions from the system (Brain-first)

> Tick `[x]` for the Department Head's choice, or fill in free text. Save the file.

## Q1 [CRITICAL]
_Cite: 00-Brain/products.json_

Which product(s) in the Cyber family need the 1-day compression? Your brief says 'CY-80 family,' but our records show only CY-80L (with 4G LTE), CY-80R (refurbished), and CYS-10 (charging cradle). There is no base 'CY-80' model.

- [x] CY-80L (4G LTE) only
- [ ] CY-80R (refurbished) only
- [ ] All three: CY-80L, CY-80R, and CYS-10
- [ ] CY-80L and CYS-10 only

## Q2 [CRITICAL]
_Cite: 00-Brain/budget.json_

What is the maximum additional cost you're willing to absorb for this 1-day compression? Our budget shows $6.8M total annual allocation with no department-level breakdowns or unit economics, so I cannot estimate overtime, expedited freight, or line charges without a per-unit or per-run cost target.

- [ ] No hard cap — tell me what it costs and I'll decide
- [x] Up to $50K in additional cost is acceptable
- [ ] Up to $150K in additional cost is acceptable
- [ ] Up to $300K in additional cost is acceptable

## Q3 [CRITICAL]
_Cite: 00-Brain/headcount.json_

Which department or role owns the production schedule for this run? We have six active departments (hardware-eng, NPI program-mgmt, quality-reliability, mfg-supplier-quality, service-ops, finance) but no named owners for the CY-80 line. I need a clear decision-maker for shift changes, QA signoff delegation, and logistics.

- [ ] NPI Program Management owns the schedule
- [x] Manufacturing & Supplier Quality owns the schedule
- [ ] Hardware Engineering owns the schedule
- [ ] free_text

## Q4 [WARN]
_Cite: 00-Brain/products.json_

Does the compression need to work within existing contract manufacturer lead times and supply agreements, or are you authorizing renegotiation or premium expediting outside normal channels? All products are in Mass Production, so steady-state constraints apply.

- [x] Stay within existing agreements — no renegotiation
- [ ] Premium expediting and renegotiation are authorized
- [ ] I don't know — tell me the difference in cost and risk between both options
