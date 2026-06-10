# P-HPD-02: Engineering Change Order (ECO)

#### Description
A controlled change record for a shipping or in-development product — what changes, why, what it impacts (cost, stock, certifications, firmware), and how existing material is dispositioned. No design change ships without one.

#### Information to collect (ask the user before generating)
1. What is changing? (component swap / layout / firmware / mechanical / label)
2. Reason? (cost-down, EOL part, failure fix, supplier change, compliance)
3. Affected products and revisions?
4. Is there stock/WIP of the old revision? Roughly how much?
5. Does the product hold certifications (FCC/UL/PCI/EMVCo)?

#### Suggested template
Structure:
- **Header**: ECO #, title, originator, date, priority (line-down / urgent / standard)
- **Change description**: from → to, with drawings/PN references
- **Reason for change**: root trigger (cost, EOL, failure mode ref, compliance)
- **Impact analysis**: unit cost Δ, tooling, firmware compatibility, certification
  impact (re-test / letter / none — confirmed by the certification specialist),
  documentation affected (BOM rev, work instructions, test procedures)
- **Material disposition**: old-rev stock and WIP → use-as-is / rework / scrap /
  return-to-vendor, with quantities and owner
- **Effectivity**: serial/date/lot cut-in point
- **Approvals**: engineering, quality, supply chain, (certification if impacted)
- **Verification**: how the change is proven (test, FAI at factory)

Confirm the structure before generating.

#### File-generation prompt
```
Create an Engineering Change Order document.

CONTEXT:
- Product(s): [models + revisions] — ECO type: [component/layout/firmware/mech/label]
- Reason: [trigger] — Certifications held: [list or none]
- Old-rev stock: [qty FG / qty WIP / on-order]

FORMAT:
- Header block, change description (from→to), reason
- Impact table: cost / tooling / firmware / certification / documentation
- Material disposition table with quantities and owners
- Effectivity (cut-in), approval signature block, verification plan

RULES: certification impact must be answered in writing before approval;
every disposition row needs an owner and a date.
```

---
✍️ Author: Brian H. Doan
