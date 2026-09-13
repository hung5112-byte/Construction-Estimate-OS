# How to Create a New Agent

## Format

Each agent is one `.md` file with YAML frontmatter + a system-prompt body.

## Path

- Core dept: `docs/departments/<dept-code>/agents/<agent-id>.md`
- Pack dept: `docs/packs/<pack>/departments/<dept-code>/agents/<agent-id>.md`

## Frontmatter fields

| Field | Required | Type | Description |
|---|---|---|---|
| id | Y | str | Unique agent slug (kebab-case) |
| name_local | Y | str | Display name |
| department | Y | str | Dept code (e.g. 05-service-operations) |
| seniority | N | str | junior/mid/senior |
| emoji | N | str | Optional |
| expertise | N | list | Skills/domains |
| required_refs | N | list | Templates that must be read |
| required_tools | N | list | Tools the agent uses |
| deliverables | N | list | Output expected |
| temperature | N | float | LLM temp (0.0-1.0) |
| model_override | N | str | Override the default model |

> Note: `name_local` is a schema key kept for backward compatibility; its value is now the English display name.

## Body

The system prompt, in English — defines the role, the way of working, and the principles.

## Example

`docs/departments/05-service-operations/agents/spares-planner.md`:
```markdown
---
id: spares-planner
name_local: "Spares Planner"
department: 05-service-operations
seniority: mid
expertise:
  - "Spares pool sizing"
  - "Service-level modeling"
  - "Repair-loop planning with RMA"
required_tools:
  - industry_benchmark
deliverables:
  - "Spares plan per deployment"
  - "Spares stock policy"
temperature: 0.4
---

# Spares Planner

## Role
You are a spares planner with 5+ years supporting fielded electronic-device fleets. You size spares pools against failure rates and repair turnaround.

## How you work
1. Read the brief + Brain (fleet size, return rate, deployment commitments)
2. Model spares need: failure rate × turnaround time × service level
3. Cite hardware benchmarks (industry_benchmark) for failure-rate ranges
4. Hand the stock policy to the inventory controller

## Principles
- ALWAYS check the fleet and return-rate figures in the Brain
- State the service-level trade-off explicitly (cost vs. downtime)
- Plain English, define terms (spares pool, advance replacement)
- Do NOT promise coverage the repair loop can't sustain
```

## Routing rule

In `department.yaml`, add a routing rule to auto-select this agent:

```yaml
routing_rules:
  - keywords: ["spares", "spare parts", "service level"]
    agent: spares-planner
```

## Test

```python
from core.agents.registry import Registry
reg = Registry(Path("departments"))
dept = reg.get("05-service-operations")
agent = dept.select_agent_for_brief("Size the spares pool for the pilot")
assert agent.id == "spares-planner"
```
