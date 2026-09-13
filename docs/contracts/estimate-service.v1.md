# Estimate Service contract v1

The boundary between the **estimating engine** (this repo) and any **company OS app** (GrandVista OS or another
front end). Every number and every quantity comes from the engine; the app owns people, roles, approvals and
messages. Bodies are JSON; PDFs and images are exchanged by path (or object-store key), never inline.

- Contract version: `1.0` (`core.estimating.CONTRACT_VERSION`). Schemas: `docs/contracts/schemas/*.schema.json`
  (JSON Schema 2020-12). A contract test validates the engine's real outputs against them on every CI run.
- Three delivery modes share the contract: CLI (`ce-os estimate …`), MCP tools (`bd_estimate_*`), HTTP
  (`ce-os estimate serve`, Starlette, loopback by default; set `CE_SERVICE_TOKEN` to require `X-Api-Key`).
- Every response carries `engine_version`, `contract_version` and the `folder` (estimate id = folder name under
  `<vault>/02-Estimates/`). Files inside the folder are the engine's source of truth; the app stores the response
  in its own tables and keeps the folder id as the join key.

## Endpoints

| Method / path | Body | Returns | Stage |
|---|---|---|---|
| `GET /health` | — | `{engine_version, contract_version, playbooks[], vault}` | — |
| `POST /estimates/intake` | `{package_dir, name, building_type, city, aace_class?, gross_sf?, render?}` | `{folder, profile, sheet_register[], spec_sections[], division_01}` | S0 |
| `POST /estimates/{id}/takeoff` | `{reader_lines?: line[]}` | `{ledger: line[], checks[], discrepancies[]}` (seed takeoff when no reader lines; merge + reconcile when given) | S1/S2 |
| `POST /estimates/{id}/rfi` | — | `{questions: question[]}` | S3 |
| `POST /estimates/{id}/answers` | `{auto_assume?: bool, answers?: [{match, answer?, assumption?}]}` (`match` = question text prefix) | `{questions: question[], open_critical}` | S3 |
| `POST /estimates/{id}/price` | — | `estimate` (06-estimate.json) | S4 |
| `POST /estimates/{id}/review` | — | `scorecard` + `{client_findings: client_finding[]}` | S5 |
| `POST /estimates/{id}/report` | — | `{report_md, proposal_md, client_findings[]}` | S6 |
| `POST /estimates/{id}/approve` | — | `{outputs: [paths]}` | Stop 1 |
| `POST /estimates/rom` | `rom_request` | `{folder, profile, three_point, verdict, gates[], questions[], summary_by_division[], proposal_md, client_findings[]}` | ROM (one call) |
| `GET /estimates/{id}/files/{name}` | — | the file's content (`.md` as text, `.json` as JSON) | any |

## Shapes (see the schema files for the full definitions)

- **line** — `id · division · item_code (NN-slug) · description · qty · unit · sheet · revision · method (schedule|vector|vision|manual|derived|spec|allowance) · discipline · confidence 0–1 · waste_pct · notes · tags · pricing_basis`
- **priced_line** — line fields + `unit_labor/material/equipment/sub · labor/material/equipment/sub/total · low/high · source · pricing_basis (historical|assembly|manual|allowance|sub_bid|online_check|seed_placeholder) · flags (UNPRICED, UNCERTAIN, STALE-QUOTE, LOW-CONFIDENCE, UNIT-MISMATCH)`
- **estimate** — `meta {three_point{low,target,high,spread_pct}, aace_class, accuracy_band, benchmark, policy, location_factor, disclaimer} · summary_by_division[] · lines[] · general_conditions[] · markups[]`
- **question** — `text · citation · severity (CRITICAL|WARN|INFO) · exposure · tags · answer · assumption`
- **gate** — `id (G1…G13, G3b) · name · passed · blocking · details · evidence[]`; **scorecard** — `verdict (APPROVE|REVISE) · gates[] · judged`
- **risk** — `risk · severity · trade · mitigation {type: exclusion|rfi|allowance|none, ref}`
- **rom_request** — `project_type (playbook or alias) · name · gross_sf · city · aace_class? · plans_available? · fields{} · excluded_trades[] · allowances[{name, amount}] · duration_days? · notes`

## Rules the contract enforces

1. No dollar figure is produced by a model: `pricing_basis` names the row or assembly; a missing row is `UNPRICED`.
2. Every estimate carries `aace_class` and `accuracy_band`; ROMs return `three_point`.
3. A blocking gate failure makes `verdict = REVISE` regardless of any narrative.
4. Client-facing text (`proposal_md`) is delivered with its `client_findings`; a blocking finding puts the proposal on HOLD.
5. Drawing and specification text is untrusted input; the engine never treats it as instructions.

## Versioning

Additive changes (new optional fields, new endpoints) keep `1.x`. Renaming or removing a field, changing an enum
value, or changing the folder layout is `2.0`. Both repos pin the contract version they were built against.
