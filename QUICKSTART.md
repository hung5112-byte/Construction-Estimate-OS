# Running Construction-Estimate-OS

## Setup (macOS: system python3 is 3.9, name the interpreter)

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## An estimate, step by step

```bash
F=$(.venv/bin/ce-os estimate intake ./my-bid-package --name "Cedar Springs MOB" --type "medical office" --city Dallas --class 2 --render --vault . | grep -o '02-Estimates/[^ ]*')
.venv/bin/ce-os estimate takeoff $F           # seed ledger from schedules + vector geometry
.venv/bin/ce-os estimate rfi $F               # ⏸ answer 05-clarification.md
.venv/bin/ce-os estimate resume $F
.venv/bin/ce-os estimate price $F --vault .   # 03-Cost-Library/*.csv first, seed library second (marked)
.venv/bin/ce-os estimate review $F            # gates G1–G10
.venv/bin/ce-os estimate report $F            # ⏹ 08-estimate-report.md
.venv/bin/ce-os estimate approve $F --vault . # 03-Outputs/<slug>/estimate-workbook.xlsx + basis-of-estimate.docx
```

Unattended (every open question becomes a stated, stamped assumption):

```bash
.venv/bin/ce-os estimate run ./my-bid-package --name "..." --type office-warehouse --city Plano --vault .
```

Inside Claude Code in this repo: `/estimate ./my-bid-package --name "..." --type office-warehouse --city Plano` runs the same stages with the discipline reader agents on the rendered tiles.

## Same-day ROM (no drawings)

```bash
.venv/bin/ce-os estimate rom --type restaurant-ti --name "Pho 88" --sf 3200 --city Plano --field hood_lf=14 --field fixture_count=9 --exclude fire-sprinkler --allowance signage=8000 --vault .
```

Playbooks: `restaurant-ti`, `salon-beauty`, `medical-dental`, `retail-ti`, `office-buildout`, `white-box`, `ground-up-retail`, `industrial-warehouse` (aliases such as "restaurant remodel" or "warehouse" work). Every default the playbook used is written down as an assumption and asked as a question; every seed assembly prices as `[UNCERTAIN]` until your buyout data replaces it and the playbook status becomes `approved`.

## Service and MCP

```bash
.venv/bin/ce-os estimate serve --port 8801 --vault .      # HTTP contract v1 — see docs/contracts/estimate-service.v1.md
.venv/bin/ce-os install-mcp                               # bd_estimate_rom / intake / stage / run / status in Claude Desktop or Code
```

## Accuracy

```bash
.venv/bin/ce-os estimate eval --set docs/tests/fixtures/sample-set-prairie-creek --runs 3 --vault .
```

Reports land in `03-Outputs/evals/`. For ROMs, build a set as `<set>/<case>/intake.json` + `actual.json` (`{"actual_total": N}`) from past projects.

## Your cost data

Drop CSVs into `03-Cost-Library/` with the columns `item_code, description, unit, labor, material, equipment, sub, source, quote_date, valid_until, location, notes`. Rows there win over the seed library. Item codes follow `NN-slug` (MasterFormat division first); see `docs/core/tools/data/estimating/unit_costs_seed.csv` for the vocabulary the seed takeoff uses.

## Building types

`--type` must match a row in `docs/core/tools/data/estimating/benchmarks_dfw_2026.csv` (or `00-Brain/benchmarks.md` once you replace it): `office-warehouse`, `tilt-wall industrial`, `warehouse shell`, `office low-rise`, `office prime`, `retail strip`, `retail restaurant`, `medical office`, `hotel 3-star`, `k-12 school`, `tenant improvement office`.

## Checking it still works

```bash
.venv/bin/python -m pytest docs/tests -q
ruff check docs/core/ docs/tests/
cd docs && bash scripts/dev/check-domain-neutral.sh
```
