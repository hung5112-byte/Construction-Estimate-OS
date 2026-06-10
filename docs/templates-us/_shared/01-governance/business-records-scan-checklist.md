# PROMPT 02: Business Records Scan Checklist (Entity-registration document checklist)

#### Description
A checklist to review, scan, and digitize all original legal documents. Ensures nothing is missing and every scan has complete metadata.

#### Information to collect (ask the user before generating)
1. Entity type? (affects the list of required documents)
2. How long has the company operated? (older companies have more amendments)
3. Any branches / additional locations / DBAs?
4. Where is it stored digitally? (Google Drive / NAS / SharePoint)
5. File naming convention? (e.g. Formation_2024_v1.pdf)

#### Suggested template
Structure:
- **Main checklist table**: # | Document name | Required? | Original on hand? | Scanned? | File path | Scan date | Notes
- **Categories**: (A) Formation documents, (B) Entity changes (SOS filings), (C) Licenses/permits, (D) Tax (EIN, returns), (E) Other
- **Scan guidance**: resolution, format (PDF), naming, folder structure
- **Metadata checklist**: each scan needs: issue date, issuing agency, number, expiration

Confirm the structure before generating.

#### File-generation prompt
```
Create a Business Records Scan Checklist — review & digitize legal documents.

CONTEXT:
- Entity type: [type]
- Year formed: [year] — Number of SOS amendments: [number]
- Branches/locations: [yes/no] — Count: [number]
- Storage: [Google Drive / NAS / SharePoint]
- Naming: [convention]

FORMAT:
- Checklist table: a ☐ checkbox for each item
- 5 groups: (A) Formation, (B) Entity changes, (C) Licenses/permits, (D) Tax, (E) Other
- Each item: Name | Number | Issue date | Agency | Expiration | Original ☐ | Scan ☐ | Link
- Scan guidance: 300dpi, PDF/A, naming = [Type]_[Number]_[Date].pdf
- Summary: __/__ documents complete, __/__ scanned

TONE: Administrative, clear, form-style.
LENGTH: 3-5 pages.
```

---
✍️ Author: Brian H. Doan
