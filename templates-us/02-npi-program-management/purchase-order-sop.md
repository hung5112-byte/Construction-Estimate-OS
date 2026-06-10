### PROMPT 09: Purchase Order SOP

#### Description
The purchase-order (PO) process — from when a need arises to receiving goods and paying. Links to the Asset Procurement SOP (for large assets) and the Warehouse Management SOP (receiving).

#### Information to collect (ask the user before generating)
1. PO approval tiers by value? (e.g. < $5,000 Manager, < $20,000 Owner, > $20,000 Board)
2. PO management software? (ERP / accounting software / Excel / email)
3. Order only from AVL vendors, or allow exceptions?
4. How many comparative quotes before ordering? (1/2/3)
5. Current 3-way matching process? (PO vs. receiving vs. invoice)
6. Current average PO processing time?
7. Emergency POs? What's the process?

#### Suggested template
Structure:
- **Step 1** — Need arises: who requests, request form
- **Step 2** — Check AVL: is the vendor on the approved list?
- **Step 3** — Get quotes: compare 2-3 vendors
- **Step 4** — Approve PO: by tier limit
- **Step 5** — Send PO to vendor: confirm the order
- **Step 6** — Receive & inspect: check quantity, quality
- **Step 7** — 3-way matching: PO vs. receiving vs. invoice
- **Step 8** — Payment: hand off to accounting
- **Exceptions**: emergency PO, over-limit PO, off-AVL PO

Confirm the structure before generating.

#### File-generation prompt
```
Create a Purchase Order SOP.

CONTEXT:
- Company: [Name] — PO approval tiers: [detail in USD]
- Software: [ERP / Excel / email]
- Vendors: AVL only / exceptions with a process
- Quotes needed: [1/2/3]

FORMAT:
- Flowchart: Mermaid — Request → Check AVL → Quotes → Compare → Approve PO → Send vendor → Receive → Inspect → Pay
- PO template: PO # | Date | Vendor | Items | Qty | Unit price | Total | Delivery | Terms | Approved by (USD)
- 3-way matching: PO vs. receiving report vs. invoice → approve payment
- Exception handling: emergency PO, over-limit PO, off-AVL PO
- Approval matrix: PO value → approval level
- Lead-time tracking: from request → receipt = target [days]

TONE: Standard SOP, procurement.
LENGTH: 4-6 pages.

CROSS-REFERENCE: Links to the AVL (P-OPS-08) and the Warehouse Management SOP (P-OPS-04).
```

---
✍️ Author: Brian H. Doan
