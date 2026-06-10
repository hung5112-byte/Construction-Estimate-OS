### PROMPT 12: Core Process SOPs (1-2-3)

#### Description
Three core SOPs that directly create value for the customer — depending on the company's industry. These are the "core processes" in EOS: the processes that, done right, make the company succeed; done wrong, make it fail.

#### Information to collect (ask the user before generating)
1. What are the company's 3 most core processes? (e.g. Sell → Deliver → Post-sale support)
2. How many steps does each currently have?
3. Where are the bottlenecks / frequent errors?
4. Who owns each process?
5. The KPI that measures each process?

#### Suggested template
Structure — each SOP follows the Standard SOP Template (P-OPS-11):
- **Process map**: end-to-end flowchart, 5-10 main steps
- **Swimlane diagram**: role × step — who does what at each step
- **Step detail**: Input | Action | Output | Tool | Time | Quality check
- **Exception handling**: 3-5 abnormal situations + how to handle
- **KPI per process**: 3-5 metrics + target + how measured
- **Handover points**: handoffs between functions — clear input/output
- EOS style: "Documented, Simplified, Followed By All"

Confirm the structure before generating.

#### File-generation prompt
```
Create 3 Core Process SOPs (EOS Core Process).

CONTEXT:
- Company: [Name] — Industry: [industry]
- 3 Core Processes: [Name 1] | [Name 2] | [Name 3]
- Bottlenecks: [describe]
- KPIs: [per process]

FORMAT — each SOP follows the Standard SOP Template:
- Process map: Mermaid end-to-end — 5-10 main steps
- Swimlane: role × step — who does what
- Step detail: Input | Action | Output | Tool | Time | Quality check
- Exception handling: 3-5 abnormal situations + handling
- KPI per process: 3-5 metrics + target + measurement method
- EOS style: "Documented, Simplified, Followed By All"

TONE: Operational, specific, actionable.
LENGTH: 4-6 pages per SOP (12-18 pages total).

CROSS-REFERENCE: Use the Standard SOP Template (P-OPS-11) as the format.
```

---
✍️ Author: Brian H. Doan
