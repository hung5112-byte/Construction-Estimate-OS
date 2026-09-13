---
description: "Run the estimating pipeline on a bid package with the agent readers: intake → discipline readers in parallel → RFI gate → price → review → report. Usage: /estimate <package-dir> --name '...' --type office-warehouse --city Plano"
---

Run the **Construction-Estimate-OS pipeline** on the bid package the user names. Load the `drawing-reading` skill first.

## Steps

1. **Intake (deterministic).** From the repo root:
   ```bash
   .venv/bin/ce-os estimate intake <package-dir> --name "<name>" --type <building-type> --city <city> --class 2 --render --vault .
   ```
   Note the folder it prints (`02-Estimates/<slug>`). Then `.venv/bin/ce-os estimate takeoff <folder>` for the seed ledger.

2. **Readers (the Workflow).** Call the `Workflow` tool with the script in `.claude/workflows/estimate-takeoff.js` and `args: {folder: "<folder>"}`. It runs one reader agent per discipline group in parallel (civil/structural, architectural, MEP), then the spec analyst and the RFI coordinator, and writes `readers/*.json`. When it returns, merge each reader file:
   ```bash
   .venv/bin/ce-os estimate takeoff <folder> --merge <folder>/readers/<id>.json
   ```

3. **RFI gate (human).** `.venv/bin/ce-os estimate rfi <folder>` writes `05-clarification.md`. Show the CRITICAL questions to the user and stop. When they have answered in the file: `.venv/bin/ce-os estimate resume <folder>`.

4. **Price + review + report (deterministic, then agents).** `price`, then `review`, then spawn the `ce-chief-estimator` agent with the folder path: it reads `07-review-scorecard.md`, `06-estimate.md`, `04-takeoff-ledger.md`, `05-questions.json` and writes `07-judged-review.json` (`[{reviewer, rubric, score, issues[]}]`). Re-run `review`, then `report`. Spawn `ce-proposal-writer` to write `08-narrative.json` (`{tldr, verdict, measured_vs_assumed, assumptions[], narrative}`) and re-run `report`.

5. **Stop 1.** Present `08-estimate-report.md` to the user. On approval: `.venv/bin/ce-os estimate approve <folder> --vault .`

Never invent a quantity or a price in chat; everything comes from the folder files.
