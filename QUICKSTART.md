# Quick start

The full guide is in [README.md](README.md). This page is the short version.

```bash
python3.12 -m venv .venv && .venv/bin/pip install -e ".[dev]"      # macOS system python3 is 3.9; name the interpreter
.venv/bin/python -m pytest docs/tests -q                             # sanity check, no LLM
```

**Unattended run on the sample package** (no LLM, about 20 s):

```bash
.venv/bin/ce-os estimate run docs/tests/fixtures/sample-set-prairie-creek --name "Prairie Creek Bldg 2" --type office-warehouse --city Plano --vault .
```

**A real package, stage by stage:**

```bash
F=$(.venv/bin/ce-os estimate intake ./my-bid-package --name "Cedar Springs MOB" --type "medical office" --city Dallas --class 2 --render --vault . | grep -o '02-Estimates/[^ ]*')
.venv/bin/ce-os estimate takeoff $F           # seed ledger from schedules + vector geometry
.venv/bin/ce-os estimate read $F --vault .    # headless vision readers (needs a logged-in `claude` CLI, see README)
.venv/bin/ce-os estimate rfi $F               # ⏸ answer 05-clarification.md
.venv/bin/ce-os estimate resume $F
.venv/bin/ce-os estimate price $F --vault .   # 03-Cost-Library/*.csv first, seed library second (marked)
.venv/bin/ce-os estimate review $F            # gates G1–G13
.venv/bin/ce-os estimate report $F            # ⏹ 08-estimate-report.md
.venv/bin/ce-os estimate approve $F --vault . # 03-Outputs/<slug>/estimate-workbook.xlsx + basis-of-estimate.docx + proposal-draft.docx
```

**Headless readers** need `claude auth login --claudeai` once and, per shell:

```bash
export BD_OS_LLM_PROVIDER=claude-cli BD_OS_CLAUDE_BIN="$(command -v claude)" BD_OS_LLM_TIMEOUT_SECONDS=420
```

**Inside Claude Code:** `/estimate ./my-bid-package --name "..." --type office-warehouse --city Plano` or `/rom --type restaurant-ti --name "Pho 88" --sf 3200 --city Plano`.

**Same-day ROM without drawings:**

```bash
.venv/bin/ce-os estimate rom --type restaurant-ti --name "Pho 88" --sf 3200 --city Plano --field hood_lf=14 --exclude fire-sprinkler --allowance signage=8000 --vault .
```

**Service and MCP:** `ce-os estimate serve --port 8801 --vault .` and `ce-os install-mcp`.

**Your cost data:** CSVs in `03-Cost-Library/` with `item_code, description, unit, labor, material, equipment, sub, source, quote_date, valid_until, location, notes` (optional `unit_low`, `unit_high`, `pricing_basis`).
