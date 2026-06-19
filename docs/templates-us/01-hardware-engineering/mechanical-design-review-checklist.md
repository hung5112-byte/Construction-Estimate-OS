# P-HWE-17: Mechanical Design Review Checklist (ME)

#### Description
A mechanical gate for the enclosure and internals — fit, draft, wall thickness, fastening, serviceability, and tooling readiness — before cutting steel.

#### Information to collect (ask the user before generating)
1. Product, housing material, and process (injection mold, sheet metal)?
2. Key mechanical requirements (IP rating, drop, operating temp)?
3. Serviceability targets (FRU access, screw count)?
4. Tooling stage (proto, soft tool, hard tool)?
5. Assembly/CM constraints?

#### Suggested template
Structure:
- Requirements recap (environmental, structural, serviceability)
- Moldability: wall thickness, draft, ribs, boss/snap design
- Fit + tolerance interactions (link to tolerance stack)
- Fastening + assembly sequence; FRU access
- Tooling readiness + DFM flags; findings/go-no-go

Confirm the structure before generating.

#### File-generation prompt
```
Create a Mechanical Design Review Checklist (ME).

CONTEXT:
- Product: [model] — Material/process: [...] — Tooling: [proto/soft/hard]
- Requirements: [IP/drop/temp/serviceability]

FORMAT:
- Checklist by area with pass/fail + note
- Findings table (item, severity, owner)
- Sign-off + go/no-go to tooling

RULES: wall-thickness and draft callouts must be present for molded parts; any BLOCK item blocks tooling release.
```

---
✍️ Author: Brian H. Doan
