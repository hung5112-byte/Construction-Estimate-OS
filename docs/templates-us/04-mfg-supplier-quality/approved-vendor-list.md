### PROMPT 08: Approved Vendor List (AVL)

#### Description
A consolidated registry of all vendors that have passed evaluation and been approved. You may only order from vendors on this list (except special cases approved by the owner).

#### Information to collect (ask the user before generating)
1. How many vendors do you currently work with?
2. How do you group vendors? (category / service / region)
3. What info to store per vendor? (Tax ID/EIN, contact, master agreement, score...)
4. Who can add/remove vendors from the list?
5. Review frequency? (6 months / 1 year)
6. Any vendors currently suspended or blacklisted?

#### Suggested template
Structure:
- **Master Registry**: a consolidated table — ID, name, Tax ID/EIN, category, contact, agreement, score, status
- **Grouping**: by category/service — top vendors per group
- **Status tracking**: Active 🟢 | Under Review 🟡 | Suspended 🟠 | Blacklisted 🔴
- **Quick lookup**: category → top 3 recommended vendors (by score)
- **Add/remove process**: a simple flowchart — propose → evaluate → approve → update AVL
- **Update log**: Date | Change | Reason | Updated by

Confirm the structure before generating.

#### File-generation prompt
```
Create an Approved Vendor List (AVL).

CONTEXT:
- Company: [Name] — # vendors: [number]
- Grouping: [category / service / region]
- Approver: [title]
- Review cycle: [6 months / 1 year]

FORMAT:
- Registry: # | Vendor | Tax ID/EIN | Category | Contact | Phone | Email | Master agreement # | Expiry | Score | Status
- Grouping: by category/service
- Status: Active 🟢 | Under Review 🟡 | Suspended 🟠 | Blacklisted 🔴
- Quick lookup: category → top 3 recommended vendors
- Update process: flowchart to add/remove a vendor
- Update log: Date | Change | Updated by

TONE: Registry, reference material, easy to look up.
LENGTH: 2-4 pages.

CROSS-REFERENCE: Links to the Vendor Scorecard (P-OPS-07) for evaluation scores.
```

---
✍️ Author: Brian H. Doan
