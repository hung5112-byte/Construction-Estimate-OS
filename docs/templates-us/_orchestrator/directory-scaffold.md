# PROMPT 03: Directory Scaffold

#### Description
An SOP for creating a complete directory tree for the business — including a naming convention, numbering system, and a README template for each folder. Ensures 200+ files are organized logically, easy to find, and easy to maintain.

#### Information to collect (ask the user before generating)
1. Where will the company store these? (Google Drive / SharePoint / Notion / local folder / Git repo)
2. A specific naming convention? (e.g. [Dept]-[Type]-[Name]-v[Version])
3. File-name language: English, or codes?
4. Need version control? (v1, v2... or date-based?)
5. Need folder-level access permissions?

#### Suggested template
Structure:
- **Naming Convention** — naming rules: `[##]-[Category]-[Type]-[Name].[ext]`
- **Numbering System** — 00-12 for skills, 00.1-00.x for sub-groups
- **Folder Structure** — a full 5-tier tree view
- **README Template** — each folder has a README describing its contents
- **File Types** — POL/MAN/SOP/FRM/RPT + extension mapping
- **Auto-generation Script** — pseudocode/script to create the whole tree

Confirm the structure before generating.

#### File-generation prompt
```
Create a "Directory Scaffold" SOP — a guide to building the standard directory tree for the Business Packaging set.

CONTEXT:
- A system of 13 skills (00-12), each with sub-groups, each sub-group with 3-8 files
- Total: 200+ files to organize logically
- Storage: [Google Drive / SharePoint / Notion / Local / Git]
- Naming: [specific convention or use the standard]
- Language: [English / Code]

FORMAT:
- Full tree view as ASCII art — to level 3 (Skill → Sub-group → File)
- Mapping table: Folder → Description → Owner → Access Level
- Naming-convention reference card (1 page, printable for the wall)
- Folder-creation script (bash/python) if using local/Git
- README.md template for each folder

TONE: Technical, precise, easy to follow.
LENGTH: 4-6 pages + appendix (full tree view).
```

---
✍️ Author: Brian H. Doan
