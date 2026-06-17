---
type: answers
---
- Q: The AMG-100 is in DVT (00-Brain/products.json:AMG100.status). Is a component cost-down at this stage acceptable, given it could disrupt final qualification testing?
  A: Only if limited to form/fit/function equivalent parts, no new DVT required
- Q: Given that any BOM change could trigger re-certification under FCC Part 15, UL/IEC 62368-1, or UN 38.3 (00-Brain/laws.json), which regulatory impact is the business willing to accept?
  A: None — all cost-down changes must maintain existing certifications without retesting
- Q: The AMG-100 ICP requires survival in harsh environments — spills, sanitizer chemicals, 24/7 duty cycle (00-Brain/strategy.json:icp.pain_points[2]). What is the minimum environmental reliability threshold that must not be degraded?
  A: IP rating (e.g., IP54) and chemical resistance must be unchanged from current BOM
- Q: The ICP values payment security and PCI compliance (00-Brain/strategy.json:icp.profile). Will any cost-down candidate touching the payment module, secure element, or tamper-detection circuitry be automatically rejected?
  A: PCI domain is off-limits for this cost-down; target other BOM lines
- Q: The ICP requires predictable supply (00-Brain/strategy.json:icp.profile). How do we ensure cost-down part swaps don't introduce lead-time risk or single-source dependency?
  A: Every alternate part must have a qualified second source with confirmed lead time
- Q: How will we validate 'no performance regression' for CPU/GPU/UI/boot/payment speed after a BOM change? What gates are required?
  A: Regression test every cost-down SKU through full system validation (boot, payment, UI lag)
- Q: The $0.50 cost-down target is ambiguous — is it per-tablet ex-factory BOM cost, or landed cost including logistics and tariffs (00-Brain/laws.json)?
  A: Landed cost (BOM + freight + duty + tariffs)