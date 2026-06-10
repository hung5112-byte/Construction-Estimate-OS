### PROMPT 02: Asset Procurement SOP

#### Description
The process to purchase assets/equipment — from a need arising, through a proposal, approval, comparative quotes, ordering, and acceptance, to handover and entry into asset management.

#### Information to collect (ask the user before generating)
1. Procurement approval tiers? (< $5,000: Manager | < $20,000: Owner | > $20,000: Board?)
2. How many comparative quotes? (2 / 3 / 5?)
3. Payment process: advance or pay-after-delivery?
4. A procurement committee?
5. Fixed-asset capitalization threshold? (e.g. the IRS de minimis safe harbor — $2,500/item, or $5,000 with an applicable financial statement, Treas. Reg. §1.263(a)-1(f)) [verify]

#### Suggested template
Structure:
- **Step 1** — Procurement proposal: proposal form + justification
- **Step 2** — Approval: by tier + budget check
- **Step 3** — Get quotes: number of quotes, comparison table
- **Step 4** — Select vendor & order: selection criteria, PO
- **Step 5** — Receive & inspect: check, acceptance record
- **Step 6** — Payment: documents, process
- **Step 7** — Handover & manage: tag, register, hand to user

Confirm the structure before generating.

#### File-generation prompt
```
Create an Asset Procurement SOP.

CONTEXT:
- Company: [Name] — Tiers: < $[X] (Manager) | < $[Y] (Owner) | > $[Y] (Board)
- # quotes: [2/3/5]
- Payment: [advance / pay-after-delivery]
- Capitalization threshold: [$2,500 / $5,000 / custom] [verify with CPA]
- Procurement committee: [Yes/No]

FORMAT:
- 7-step flowchart: Mermaid — highlight approval gates
- Proposal form template: Requester | Description | Justification | Quantity | Budget line | Est. cost (USD)
- Quote-comparison table: Vendor | Price | Delivery time | Warranty | Payment | Score
- Acceptance record template: Goods received | Quantity | Quality | Variance | Signature
- Decision matrix: value < X → fast track | > X → full process
- Timeline: proposal → receipt target [days]

TONE: Standard SOP, cost-controlled.
LENGTH: 5-7 pages.

NOTE: The capitalization threshold is a tax matter — confirm with a CPA.
```

---
✍️ Author: Brian H. Doan
