### PROMPT 08: Quotation Process SOP

#### Description
A standardized process from receiving a quote request to sending the quote, following up, and closing. Ensures quotes are accurate, timely, properly authorized, and status-tracked.

#### Information to collect (ask the user before generating)
1. Who receives quote requests? (Sales rep / Admin / Website form)
2. Committed response time? (e.g. 24h / 48h / 72h)
3. Who prices it? Who approves? Multiple approval levels?
4. How is the quote sent? (PDF / Email / system / print)
5. Quote validity? (7 days / 15 days / 30 days)
6. Follow-up process: how many times? How far apart?
7. Special quotes (preferential, large project) — separate process?

#### Suggested template
Structure:
- **Purpose & scope**
- **Overall process**: an 8-step flowchart — Receive → Gather requirements → Price → Approve → Create quote → Send → Follow up → Close/Cancel
- **Step detail**: action, owner, timeline, output
- **Pricing approval tiers**: standard price (auto) / discounted (Sales Manager) / special (Director)
- **Quote SLA**: committed response time
- **Follow-up protocol**: follow-up schedule + sample script
- **Tracking**: a quote-status tracking template
- **Appendix**: quotation request form, price calculation sheet

Confirm the structure before generating.

#### File-generation prompt
```
Create a Quotation Process SOP.

CONTEXT:
- Company: [Name] — Products/services: [# types]
- Receiver: [Sales rep / Admin / Website form]
- Response SLA: [24h / 48h / 72h]
- Pricing approval: [Sales rep / Manager / Director — by level]
- Format: [PDF / Email / system]
- Validity: [7 / 15 / 30 days]
- Follow up: [# times] — Interval: [days]

FORMAT:
- Flowchart: Mermaid — 8 steps + decision points (standard vs. special price)
- Per-step: table Step | Action | Owner | Timeline | Output | Control
- Approval matrix: table Price level | Sales Rep | Sales Manager | Director | Owner
- SLA dashboard: RFQ type | SLA | Actual avg | Status (met/not)
- Follow-up schedule: Day 1 | Day 3 | Day 7 | Day 14 — Action + short script
- Tracking template: RFQ # | Customer | Product | Value | Sent date | Status | Next action | Owner
- Error handling: wrong price / expired / no response → resolution

TONE: Standard SOP — clear, step-by-step.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
