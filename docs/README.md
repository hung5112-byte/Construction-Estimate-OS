# Construction-Estimate-OS — engine docs

The engine in `docs/core/` is the fleet engine (see `CLAUDE.md` and `architecture.md`) plus `docs/core/estimating/`, the deterministic estimating pipeline described in the repository `README.md` and `QUICKSTART.md`.

- `docs/core/estimating/` — pdfio · sheet_register · sheet_text · sheet_tables · sheet_geometry · sheet_render · spec_index · takeoff_ledger · cost_engine · rfi · review_gates · workbook · report · pipeline
- `docs/core/tools/estimating_tools.py` — the eight `BaseTool` wrappers the tool router can call
- `docs/core/tools/data/estimating/` — seed unit costs (placeholders, `[UNCERTAIN]`), waste factors, DFW benchmarks, location factors
- `docs/departments/` — pack copies of the six estimating departments (the vault copies in `01-Departments/` are the source of truth)
- `docs/templates-us/` — 16 estimating templates + the generic library
- `docs/tests/fixtures/sample-set-prairie-creek/` — the synthetic bid package and its ground truth; regenerate with `scripts/make_sample_set.py`
