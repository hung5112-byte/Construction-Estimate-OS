### PROMPT 04: Warehouse / Inventory Management SOP

#### Description
The warehouse-management process — receiving, issuing, physical count, min/max inventory management, FIFO, and handling damaged/expired goods. Applies to both finished-goods and supplies warehouses.

#### Information to collect (ask the user before generating)
1. Warehouse type? (goods / raw materials / finished goods / mixed)
2. Inventory-management software? (integrated accounting / a dedicated WMS / Excel)
3. Inventory costing method? (FIFO / weighted average / specific identification)
4. Number of SKUs? Any items with expiration dates?
5. Count frequency? (monthly / quarterly / annual)
6. Multiple warehouses / branches?

> US note: under US GAAP and IRS rules, FIFO, weighted-average, and specific-identification are permitted. LIFO is allowed for US tax (IRC §472) but requires book/tax conformity and an election [verify with CPA].

#### Suggested template
Structure:
- **Receiving**: inspect → match PO → receive → enter in software → put away
- **Issuing**: issue request → approve → pick (FIFO) → deliver → update
- **Physical count**: count schedule → count → reconcile → resolve variance → report
- **Inventory management**: min/max level, reorder point, safety stock
- **Damaged/expired goods**: detect → isolate → handle → report
- **Warehouse safety**: fire safety, arrangement, entry/exit rules

Confirm the structure before generating.

#### File-generation prompt
```
Create a Warehouse Management SOP.

CONTEXT:
- Company: [Name] — Warehouse type: [goods / raw materials / finished goods]
- Software: [name / Excel]
- Costing: [FIFO / weighted average / specific identification]
- SKUs: [number] — Expiration: [Yes/No]
- Count: [frequency]
- Multi-warehouse: [Yes/No] — # warehouses: [number]

FORMAT:
- Receiving flowchart: Mermaid — 6 steps + controls
- Issuing flowchart: Mermaid — 5 steps + FIFO highlight
- Count checklist: table SKU | Book | Counted | Variance | Cause
- Min/Max template: SKU | Min | Max | Reorder Point | Lead Time | Current Stock | Status
- Damaged-goods handling: decision tree — Expired → Damaged → Vendor defect → Action
- Receiving/issuing slip templates: 2 standard forms

TONE: Standard SOP, logistics-focused.
LENGTH: 6-8 pages.
```

---
✍️ Author: Brian H. Doan
