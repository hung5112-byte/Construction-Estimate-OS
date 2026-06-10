### PROMPT 06: Tech Stack Map

#### Description
A document consolidating all the technology, software, platforms, and IT infrastructure the company uses. Categorized by function, recording license, cost, owner, and status. The "map" for the CTO/IT to manage and plan technology investment.

#### Information to collect (ask the user before generating)
1. List all software/tools in use? (SaaS, on-premise, custom-built)
2. Hosting/Infrastructure? (AWS / GCP / Azure / On-premise / VPS / shared hosting)
3. Accounting, CRM, ERP, HR software in use?
4. Communication tools? (Slack, Teams, Email)
5. Total IT cost/month? License costs?
6. Any tech debt / legacy systems to replace?

#### Suggested template
Structure:
- **Part 1** — Architecture Overview: an overall system diagram
- **Part 2** — Stack by category: Frontend, Backend, Database, Infrastructure, DevOps, SaaS tools
- **Part 3** — Tool Inventory: a detailed table per tool — name, category, license, cost, users, owner, status
- **Part 4** — Integration Map: Tool A ↔ Tool B — API / Zapier / manual
- **Part 5** — Cost Summary: total IT cost, cost per employee
- **Part 6** — Tech Debt & Modernization Plan: Legacy → Target, timeline
- **Part 7** — Review Cadence: stack-review frequency, renewal calendar
- **Appendix**: tool-evaluation criteria, vendor-comparison template

Confirm the structure before generating.

#### File-generation prompt
```
Create a Tech Stack Map.

CONTEXT:
- Company: [Name] — IT scale: [# users]
- Hosting: [AWS / GCP / Azure / On-prem / VPS]
- Main tools: [top 10]
- IT cost: [total/month]
- Tech debt: [describe]

FORMAT:
- Architecture diagram: Mermaid — layer-based (Frontend → API → Backend → DB → Infra)
- Tool inventory: 10+ column table — Tool | Category | Type (SaaS/On-prem/Custom) | License | Cost/month | Users | Owner | Contract end | Status | Notes (USD)
- Integration map: Mermaid flowchart — tool connections
- Cost dashboard: Category | Monthly | Annual | % Total IT | Cost/User
- Renewal calendar: Tool | Contract end | Auto-renew? | Action needed | Owner
- Tech debt register: System | Issue | Impact | Replacement | Timeline | Cost
- Evaluation scorecard: Criteria | Weight | Tool A | Tool B → Score

TONE: Technical, inventory-style, easy to look up and update.
LENGTH: 5-8 pages.
```

---
✍️ Author: Brian H. Doan
