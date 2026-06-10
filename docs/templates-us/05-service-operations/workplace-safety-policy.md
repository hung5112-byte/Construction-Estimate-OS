### PROMPT 14: Workplace Safety Policy (Occupational Safety)

#### Description
A workplace health & safety policy — safety rules, personal protective equipment (PPE), first aid, fire safety, and drills. Aligned with **OSHA** (the federal Occupational Safety and Health Act). General information only — not legal/safety-compliance advice; confirm requirements with a qualified safety professional. (Note: Texas has no state OSHA plan for private employers — federal OSHA applies.)

#### Information to collect (ask the user before generating)
1. Type: office / manufacturing / warehouse / construction?
2. Any employees in a hazardous environment?
3. PPE needed? (hard hat, safety shoes, glasses, gloves, masks...)
4. A dedicated safety function?
5. Fire-drill frequency?
6. Any prior workplace accidents?

#### Suggested template
Structure:
- **Leadership commitment**: a safety statement from the Department Head
- **General safety rules**: 10-15 key rules — poster format
- **PPE matrix**: position/task × required PPE × recommended PPE
- **First aid**: kit locations, trained personnel, process
- **Fire safety / emergency**: extinguisher locations, exit routes, drill schedule (OSHA emergency action plan, 29 CFR 1910.38; local fire code/NFPA)
- **Accident reporting**: form template + reporting process (OSHA recordkeeping, 29 CFR 1904; report severe injuries/fatalities to OSHA within the required window [verify: generally 8 hours for a fatality, 24 hours for hospitalization/amputation])
- **Safety training**: annual schedule + mandatory content
- **Violations**: severity → consequence

Confirm the structure before generating.

#### File-generation prompt
```
Create a Workplace Safety Policy (OSHA-aligned).

CONTEXT:
- Company: [Name] — Type: [office / manufacturing / warehouse / construction]
- Hazards: [Yes/No] — Type: [describe]
- PPE: [list]
- Safety function: [Yes/No]
- Fire drills: [frequency]
- Authority: OSH Act (29 U.S.C. §651); OSHA general industry standards (29 CFR 1910); OSHA recordkeeping (29 CFR 1904); emergency action plan (29 CFR 1910.38). Texas: federal OSHA applies (no state plan).

FORMAT:
- Leadership commitment: one paragraph from the Department Head
- Safety rules: 10-15 key rules + poster-friendly
- PPE matrix: Position/Task | Required PPE | Recommended PPE
- First aid: kit location, trained person, process
- Fire/emergency: extinguisher locations, exits, drill schedule
- Accident reporting: form template + OSHA reporting timeline
- Training: annual safety-training schedule

TONE: Safety — serious, clear, adequately cautionary.
LENGTH: 6-10 pages.

NOTE: General information, not safety-compliance advice. Confirm OSHA obligations with a qualified safety professional.
```

---
✍️ Author: Brian H. Doan
