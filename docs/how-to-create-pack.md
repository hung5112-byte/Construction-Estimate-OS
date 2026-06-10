# How to Create a Pack

Create an overlay pack that adds departments to the 5 division departments
(e.g. a product-line pack, a regulatory pack, or a customer-program pack).
No packs ship by default.

## 1. Folder structure

```
packs/<pack-code>/
├── pack.yaml            # metadata
├── README.md
├── departments/
│   └── XX-new-dept/
│       ├── department.yaml
│       └── agents/
│           └── <agent-id>.md
└── brain-template/      # optional
    └── strategy.md      # override default
```

## 2. pack.yaml schema

```yaml
name: "Pack Name"
code: pack-code
version: 0.1.0
description: "Pack description — which industry, when to use it"
target_industries: ["industry1", "industry2"]
adds_departments:
  - 06-new-dept-1
  - 07-new-dept-2
brain_template: brain-template/    # optional
compliance_refs:
  - "Law ABC YYYY"
```

> Note: an `extends_departments` key is parsed by `PackLoader` for forward
> compatibility but is **not applied** by onboarding — packs add whole
> departments via `adds_departments`; they do not inject agents into core ones.

## 3. Department definition

`packs/<pack>/departments/06-XX/department.yaml`:
```yaml
code: "06-XX"
name_vn: "Department name"
tier: 3                    # 1-5, lower = higher priority
agents:
  - agent-id-1
default_speaker: agent-id-1
refs_folder: refs/
depends_on: ["05-service-operations"]
debate_role:
  default: pro              # or con
```

> Note: `name_vn` is a schema key kept for backward compatibility; its value is the English display name.

## 4. Agent definition

`packs/<pack>/departments/06-XX/agents/agent-id.md`:
```markdown
---
id: agent-id
name_vn: "Agent Name"
department: 06-XX
seniority: senior
expertise: ["skill1", "skill2"]
required_tools: [us_law_search]
deliverables: ["Output 1", "Output 2"]
temperature: 0.5
---

# Agent Name

## Role
You are a [agent role] with [years] years of experience at a US company.

## How you work
1. Read the brief + Brain
2. Speak from your role's perspective
3. Make proposals with data
4. Cite the Brain for each claim

## Principles
- ALWAYS plain English
- Define terms
- Cite the Brain
```

## 5. Test the pack

```python
from core.agents.pack_loader import PackLoader
loader = PackLoader(Path("packs"))
pack = loader.load("your-pack-code")
print(pack.adds_departments)
```

## 6. Submit a PR

Include:
- pack.yaml
- All dept folders + agents
- README.md
- Sample brain-template (if overriding)
- A test verifying the pack loads
