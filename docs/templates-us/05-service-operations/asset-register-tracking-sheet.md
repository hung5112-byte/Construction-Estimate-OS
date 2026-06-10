### PROMPT 03: Asset Register / Tracking Sheet

#### Description
An asset-register template — managing all company assets: from desks and computers to vehicles and machinery. Tracks location, user, condition, and depreciation.

#### Information to collect (ask the user before generating)
1. How many main asset categories? (IT, furniture, vehicles, machinery...)
2. Asset-numbering convention? (e.g. IT-NB-001 = IT-Notebook-001)
3. Depreciation method? (straight-line for books; MACRS for federal tax)
4. Physical-count frequency? (6 months / 1 year)
5. Managed in software or Excel?

> US note on capitalization & depreciation: for federal tax, assets are typically depreciated under MACRS (IRC §168; IRS Pub. 946). Many small businesses expense lower-cost items under the de minimis safe harbor — up to $2,500 per item, or $5,000 with an applicable financial statement (Treas. Reg. §1.263(a)-1(f)) [verify current threshold]. Section 179 expensing (IRC §179) and bonus depreciation may also apply [verify with CPA]. Book depreciation follows US GAAP and may differ from tax.

#### Suggested template
Structure:
- **Asset Register**: Asset ID | Name | Category | Purchase date | Cost | Accumulated depreciation | Net book value | Location | User | Status (In use/Repair/Disposed/Lost)
- **Categories**: IT | Furniture | Vehicles | Machinery | Other
- **Transfer**: Asset ID | From | To | Date | Signature
- **Disposal**: Asset ID | Reason | Remaining value | Method | Approval
- **Physical count**: Asset ID | Book | Actual | Variance | Notes

Confirm the structure before generating.

#### File-generation prompt
```
Create an Asset Register.

CONTEXT:
- Company: [Name] — # categories: [number] — Est. total assets: [number]
- Numbering: [convention]
- Depreciation: [straight-line book / MACRS tax]
- Physical count: [6 months / 1 year]
- Tool: [software / Excel]

FORMAT:
- Master register: 15+ columns, full info per asset (USD)
- Naming convention: table Category | Prefix | Example
- Depreciation reference: Asset type | Useful life (years) | Method (book straight-line; tax MACRS per IRS Pub. 946) [verify]
- Transfer form: half a page, two-party signature
- Physical-count template: book vs. actual reconciliation
- Summary dashboard: Total assets | Value | In use | To dispose | Variance

TONE: Management, accurate, easy to update.
LENGTH: 4-6 pages.

NOTE: Capitalization/depreciation thresholds are tax matters — confirm with a CPA.
```

---
✍️ Author: Brian H. Doan
