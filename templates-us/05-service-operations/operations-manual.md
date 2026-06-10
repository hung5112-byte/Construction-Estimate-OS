### PROMPT 10: Operations Manual

#### Description
An overview document describing the company's entire operating system — principles, process structure, operational KPIs, escalation. The "bible" so anyone joining understands how the company runs. Per the E-Myth philosophy: "Document everything so anyone can run it."

#### Information to collect (ask the user before generating)
1. What field does the company operate in? (manufacturing / services / trading / SaaS)
2. How many core processes create value for the customer? (EOS: usually 3-7)
3. Main operational KPIs? (on-time delivery, quality rate, utilization...)
4. Any shifts? Multiple sites/branches?
5. Biggest operational pain point right now?

#### Suggested template
Structure:
- **Chapter 1** — Overview: operating mission, principles, key team
- **Chapter 2** — Value chain: value-chain diagram, core-process map
- **Chapter 3** — Process catalog: SOP registry — name, ID, version, owner
- **Chapter 4** — Operational KPIs: dashboard metrics, targets, measurement
- **Chapter 5** — Escalation: escalation matrix by incident severity
- **Chapter 6** — Continuous improvement: PDCA cycle, suggestion box, Kaizen events
- **Chapter 7** — Tools & systems: software, equipment, infrastructure
- **Appendix**: master process map, SOP index, contact directory

Confirm the structure before generating.

#### File-generation prompt
```
Create an Operations Manual.

CONTEXT:
- Company: [Name] — Field: [Manufacturing / Services / Trading / SaaS]
- Core processes: [number] — Names: [list]
- Main KPIs: [list]
- Shifts: [Yes/No] — Multi-site: [Yes/No]
- Pain points: [list]

FORMAT:
- Value-chain diagram: Mermaid — input → core processes → output → customer
- SOP registry: table SOP ID | Name | Department | Owner | Version | Last updated | Status
- KPI dashboard: table KPI | Target | Actual | Status 🟢🟡🔴 | Trend
- Escalation matrix: Severity (1-4) | Description | Response time | Handler | Notify
- PDCA template: Plan-Do-Check-Act for improvement
- Ops organization: a mini org chart for the operations team

TONE: E-Myth style — systematized, anyone can follow it.
LENGTH: 10-15 pages.
```

---
✍️ Author: Brian H. Doan
