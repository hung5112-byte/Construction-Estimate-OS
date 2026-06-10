# PROMPT 03: Licenses & Permits Registry

#### Description
A consolidated registry of all licenses, professional certifications, and permits the company needs beyond its entity registration. Tracks status, expiration, and issuing agency. US licensing is industry- and locality-specific — check federal, Texas, and local requirements for each activity. General information only — not legal advice.

#### Information to collect (ask the user before generating)
1. Primary & secondary lines of business? (each may need different permits)
2. Any activity that requires a federal/state/local license? (e.g. food service, alcohol/TABC, professional services)
3. Import/export? Anything involving fire, food safety, or environmental permits?
4. Operating locations? (each city/county may have its own requirements)

#### Suggested template
Structure:
- **Registry table**: # | Permit/License name | Issuing agency | Number | Issue date | Expiration | Status (Active/Expiring/Expired) | Owner | Notes
- **Grouping**: by area (fire, health/food, environmental, labor, industry-specific...)
- **Alert calendar**: renewal alerts 90/60/30 days ahead
- **Renewal process**: a summary of required documents & processing time per type

Confirm the structure before generating.

#### File-generation prompt
```
Create a Licenses & Permits Registry.

CONTEXT:
- Company: [Name] — Industry: [primary + secondary]
- Licensed activity: [Yes/No] — Detail: [list, e.g. food service, alcohol/TABC]
- Import/export: [Yes/No] — Fire: [Yes/No] — Food/health: [Yes/No] — Environmental: [Yes/No]
- Locations: [city/county, TX]

FORMAT:
- Registry table: # | Permit | Agency | Number | Issue date | Expiration | Status (🟢🟡🔴) | Owner | Notes
- Alert section: expiring within 90 days → highlight red
- Group by area
- Renewal-process summary: type | documents | time | cost | where to file
- Leave blank for the company to fill in real data

TONE: Administrative, standard.
LENGTH: 3-5 pages.

NOTE: General information, not legal advice. Confirm licensing with the relevant agency/attorney.
```

---
✍️ Author: Brian H. Doan
