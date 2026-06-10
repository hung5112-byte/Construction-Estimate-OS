# Document Storage Rules

> **Mandatory principle:** Every document created by the system MUST follow the naming convention and be saved into the correct folder. After creating a document, you MUST update the "Folder Usage Guide" if the structure changes.

---

## 1. FILE NAMING RULES

### Standard format
```
[Time] [Type] - [Document name] - [Dept/Version]
```

### Time codes

| Symbol | Meaning | Example |
|----------|---------|-------|
| `[STANDARD]` | Permanent document, no expiry | SOP, work instruction, policies |
| `[2026]` | Annual document | Annual plan, budget, cert renewal calendar |
| `[2026-Q1]` | Quarterly document | Quarterly report, supplier scorecard |
| `[2026-04]` | Monthly document | Monthly report, RMA dashboard, meeting minutes |

### Document-type codes

| Code | Type | Code | Type |
|----|------|-----|------|
| **SOP** | Process/Procedure | **WI** | Work instruction |
| **POL** | Policy/Standard | **RPT** | Report |
| **PLAN** | Plan | **FORM** | Form/Template (ECO, SCAR, RMA) |
| **MIN** | Minutes | **DOC** | Document/Reference |

### Document classification

| Type | Characteristic | Time code |
|------|----------|-------------|
| **Permanent** | Rarely changes, updated only on process/spec change | `[STANDARD]` |
| **Annual** | Updated periodically by year or quarter | `[2026]`, `[2026-Q1]` |
| **Ongoing** | Updated frequently (weekly/monthly) | `[2026-04]` |

### Standard naming examples
- `[STANDARD] SOP - RMA process - SvcOps v2.0`
- `[STANDARD] FORM - Engineering change order - NPI v1.0`
- `[2026-Q1] RPT - Supplier quality scorecard - MSQ`
- `[STANDARD] SOP - Receiving & inspection - SvcOps v1.0`
- `[2026] PLAN - Certification renewal calendar - NPI`

---

## 2. STANDARD FOLDER STRUCTURE (mirrors the 5 departments)

| Code | Folder | Access |
|----|---------|-----------|
| 00 | VP Office (division-wide) | VP |
| 01 | Hardware Engineering | HW Eng + VP |
| 02 | NPI & Program Management | NPI/PM + VP |
| 03 | Quality & Reliability | Quality + all (view: released SOPs/criteria) |
| 04 | Manufacturing & Supplier Quality | MSQ + VP |
| 05 | Service Operations | Service Ops + VP |
| 09 | Consolidated Reporting | VP + leadership |
| _ARCHIVE | Old documents | All (read-only) |

---

## 3. MAPPING: TEMPLATE → FOLDER

### 01 — Hardware Engineering

| Document | Folder | Suggested file name |
|-----------|--------|----------------|
| Improvement proposal | 01 | `[STANDARD] FORM - Improvement proposal - HWEng v1.0` |
| Design review records | 01 | `[2026] DOC - Design review <product> - HWEng` |

### 02 — NPI & Program Management

| Document | Folder | Suggested file name |
|-----------|--------|----------------|
| Bill of materials | 02 | `[STANDARD] DOC - BOM <product> rev <X> - NPI` |
| Engineering change order | 02 | `[STANDARD] FORM - ECO-<number> - NPI v1.0` |
| NPI / product development SOP | 02 | `[STANDARD] SOP - NPI process - NPI v1.0` |
| Product brief / roadmap / catalog | 02 | `[2026] PLAN - Product roadmap - NPI` |
| Certification tracker | 02 | `[2026] DOC - Certification tracker - NPI` |
| Purchase-order SOP / shortage plan | 02 | `[STANDARD] SOP - Purchase orders - NPI v1.0` |
| ODM management SOP | 02 | `[STANDARD] SOP - ODM management - NPI v1.0` |
| Asset procurement SOP | 02 | `[STANDARD] SOP - Asset procurement - NPI v1.0` |

### 03 — Quality & Reliability

| Document | Folder | Suggested file name |
|-----------|--------|----------------|
| Quality policy / QMS docs | 03 | `[STANDARD] POL - Quality policy - Quality v1.0` |
| Standard SOP template / SOP review process | 03 | `[STANDARD] DOC - Standard SOP template - Quality v1.0` |
| Incoming inspection plan | 03 | `[STANDARD] SOP - IQC plan - Quality v1.0` |
| Quality-control SOP | 03 | `[STANDARD] SOP - Quality control - Quality v1.0` |
| DVT test plan & report | 03 | `[2026] RPT - DVT report <product> - Quality` |
| 8D failure analysis | 03 | `[2026] RPT - 8D <failure mode> - Quality` |
| Complaint SOP / log | 03 | `[STANDARD] SOP - Complaint management - Quality v1.0` |

### 04 — Manufacturing & Supplier Quality

| Document | Folder | Suggested file name |
|-----------|--------|----------------|
| SCAR | 04 | `[STANDARD] FORM - SCAR-<number> - MSQ v1.0` |
| Vendor evaluation / scorecard / AVL | 04 | `[2026-QX] RPT - Vendor scorecard - MSQ` |
| Core process SOPs / kaizen board | 04 | `[STANDARD] SOP - Core processes - MSQ v1.0` |

### 05 — Service Operations

| Document | Folder | Suggested file name |
|-----------|--------|----------------|
| RMA process SOP / refurb standard | 05 | `[STANDARD] SOP - RMA process - SvcOps v1.0` |
| Warranty policy / after-sales SOP | 05 | `[STANDARD] POL - Warranty policy - SvcOps v1.0` |
| Receiving & inspection SOP | 05 | `[STANDARD] SOP - Receiving & inspection - SvcOps v1.0` |
| Inventory / cycle count | 05 | `[STANDARD] SOP - Cycle count program - SvcOps v1.0` |
| Field deployment checklist | 05 | `[STANDARD] FORM - Deployment checklist - SvcOps v1.0` |
| Landed cost model | 05 | `[2026] DOC - Landed cost model - SvcOps` |
| Incident SOP / ops manual / safety | 05 | `[STANDARD] SOP - Incident management - SvcOps v1.0` |
| Weekly/monthly ops reports | 09 | `[2026-MM] RPT - Weekly operations report - SvcOps` |

### Generic / shared (from `templates-us/_shared/`)

| Document | Folder | Suggested file name |
|-----------|--------|----------------|
| Meeting minutes | 00 | `[2026-MM] MIN - <meeting> - <dept>` |
| Monthly management report | 09 | `[2026-MM] RPT - Monthly division report - VP` |
| Budget | 00 | `[2026] PLAN - Division budget - VP` |
| Any HR/finance/marketing doc you pull from `_shared/` | 00 | per Section 1 convention |

---

## 4. PROCESS AFTER CREATING A DOCUMENT

1. **Name the file** per the standard format in Section 1
2. **Identify the target folder** per the mapping in Section 3
3. **Check for duplicates** — if a similar file exists, bump the version (v1.0 → v1.1)
4. **Upload/save** the file into the correct subfolder
5. **Update the Folder Usage Guide** if you created a new subfolder or changed the structure

## 5. IMPORTANT NOTES

- Controlled QMS documents (SOPs, criteria, standards) follow the document-control rules in the quality manual — version bumps require Quality's sign-off
- Do not delete old files — rename with `_old` or move to `_ARCHIVE`
- Ongoing documents: create a new file each cycle, don't overwrite the old one
- Replace `[YYYY]` with the actual year, `[MM]` with the month, `[QX]` with the quarter

---
✍️ Author: Brian H. Doan
