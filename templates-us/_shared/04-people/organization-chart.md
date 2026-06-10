# P-PPL-01: Organization Chart

#### Description
The official org chart — showing the department structure, reporting lines, and span of control. The "map of authority" that helps everyone understand who reports to whom and who's responsible for what.

#### Information to collect (ask the user before generating)
1. How many departments/units in the current structure?
2. Current total headcount? Distribution by department?
3. Structure: functional / divisional (by product/geography) / matrix?
4. Any vacant positions to fill?
5. Plans to change the structure in the next 6-12 months?
6. Special relationships: dotted-line, dual-hat, outsourced?

#### Suggested template
Structure:
- **Overview**: structure type, # management levels, total headcount
- **Org Chart**: a Mermaid diagram — from Owner/Board down to departments
- **Detail table**: Department | Head | Headcount | Main function | Reports to
- **Span of Control**: analysis — how many people each manager leads
- **Vacant Positions**: open roles + hiring timeline
- **Planned Changes**: expected changes + timeline

Confirm the structure before generating.

#### File-generation prompt
```
Create an Organization Chart.

CONTEXT:
- Company: [Name] — Size: [headcount] — Structure: [Functional / Divisional / Matrix]
- Departments: [list]
- Headcount per dept: [detail]
- Vacant positions: [list]
- Planned changes: [describe]

FORMAT:
- Mermaid org chart: Owner/Board → CEO → leads → department heads → teams
- Detail table: Dept | Head | HC | Function | Reports to | Dotted line
- Span of control: Manager | Direct reports | Ratio → highlight if >7
- Color coding: Filled 🟢 | Vacant 🔴 | Planned 🟡
- Metrics: Total HC | Mgr:Staff ratio | Avg span of control | Layers

TONE: Formal, visual, clear.
LENGTH: 3-5 pages.
```

---
✍️ Author: Brian H. Doan
