---
description: "Same-day ROM with the trade agents: deterministic playbook ROM first, then one ROM trade estimator per activated trade reads the notes/photos and corrects quantities, then re-price, review and report. Usage: /rom --type restaurant-ti --name 'Pho 88' --sf 3200 --city Plano [--field hood_lf=14] [--exclude fire-sprinkler] [--notes '...'] [--package <dir with notes/photos>]"
---

Run a **ROM estimate** for the intake the user describes. Load the `drawing-reading` skill first (the provenance rules apply to notes and photos too).

## Steps

1. **Deterministic ROM.** From the repo root:
   ```bash
   .venv/bin/ce-os estimate rom --type <type> --name "<name>" --sf <gross_sf> --city <city> [--field k=v ...] [--exclude trade ...] [--allowance name=amount ...] [--notes "..."] --vault .
   ```
   Note the folder it prints (`02-Estimates/<slug>`). If the user supplied notes or photos, copy them into `<folder>/package/` (create it) so the trade agents can read them.

2. **Trade agents (the Workflow).** Call the `Workflow` tool with the script in `.claude/workflows/rom-trades.js` and `args: {folder: "<folder>"}`. It reads `00-playbook.json` for the activated trades and runs one `ce-rom-trade-estimator` per trade in parallel; each writes `readers/rom-<trade>.json`. Then merge each file:
   ```bash
   .venv/bin/ce-os estimate takeoff <folder> --merge <folder>/readers/rom-<trade>.json
   ```

3. **Re-price, review, report.**
   ```bash
   .venv/bin/ce-os estimate price <folder> --vault . && .venv/bin/ce-os estimate review <folder> && .venv/bin/ce-os estimate report <folder>
   ```

4. **Present.** Show the user the low / target / high, the class and band, the verdict, the open CRITICAL questions (from `05-questions.json`) and where the proposal draft is (`09-proposal-draft.md`). A ROM with open CRITICAL questions is a draft, not a price.

Never state a dollar figure that is not in `06-estimate.json`.
