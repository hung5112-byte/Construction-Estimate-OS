# Getting Started — Hardware Division OS

A guide from zero to your first task. About **15-20 minutes** if you already have Claude Desktop + Python 3.11+.

---

## Requirements

| | |
|---|---|
| **Python** | 3.11+ |
| **Claude Desktop** | Latest version ([download](https://claude.ai/download)) — with a Pro/Team subscription |
| **Obsidian** | (recommended) — to view the vault visually |
| **Git** | Any version |
| **TAVILY_API_KEY** | (optional) — enables law/competitor search. Free tier 1000 req/month at [tavily.com](https://tavily.com) |
| **Anthropic API key** | **NOT needed** — the plugin uses MCP sampling via the Claude Desktop subscription |

---

## Step 1 — Install the plugin

```powershell
git clone https://github.com/<owner>/<repo>.git vn-business-os
cd vn-business-os

python -m venv .venv
.venv\Scripts\activate                      # Windows
# source .venv/bin/activate                 # macOS/Linux

pip install -e .
```

Verify:
```powershell
vn-os --help
# Shows: onboard, install-mcp, uninstall-mcp, ...
```

---

## Step 2 — Install the MCP server into Claude Desktop

```powershell
vn-os install-mcp
```

Output:
```
✓ Installed MCP server 'vn-business-os'
   Config: C:\Users\<you>\AppData\Roaming\Claude\claude_desktop_config.json
   Backup: ...claude_desktop_config.json.bak

Next: Restart Claude Desktop to load the MCP server.
```

**→ Fully quit Claude Desktop, reopen it.**

Verify in a Claude Desktop chat:
```
List the available MCP tools.
```

You should see 9 tools: `vn_run`, `vn_resume`, `vn_meeting`, `vn_approve`, `vn_execute`, `vn_draft`, `vn_status`, `vn_onboard`, `vn_upgrade`.

---

## Step 3 — Create a vault for your division

In a Claude Desktop chat:

```
Set up a vault for my hardware division at the path:
F:\work\division-vault

My TAVILY_API_KEY: tvly-xxx
```

Claude automatically calls `vn_onboard(vault=..., tavily_api_key="tvly-xxx")`.

The plugin will:
1. Copy the vault scaffold (8 Brain files + 5 departments + division templates)
2. Generate wikilinks for the Obsidian graph view
3. Save the key to `<vault>/.env` (auto-added to `.gitignore`)
4. Init a private Git repo

Sample output:
```yaml
ok: true
vault: F:\work\division-vault
steps:
  - Copied scaffold to F:\work\division-vault
  - Installed core departments
  - Saved 1 API key(s) → .env (TAVILY_API_KEY)
  - Wikilinks: brain_hub=True, dept_hubs=5, agents_linked=29
  - Git initialized
packs: []
next_steps:
  - Open <vault>/00-Brain/ and fill strategy.md, products.md, ...
```

---

## Step 4 — Inject the API key into the MCP server

**Required when you onboarded with a TAVILY_API_KEY** — so Claude Desktop launches the MCP with the env.

```powershell
vn-os install-mcp --vault "F:\work\xyz-vault"
```

The output adds:
```
   Env injected: TAVILY_API_KEY
```

**→ Restart Claude Desktop again.**

Verify in a chat:
```
vn_status vault F:\work\xyz-vault
```

You should see:
```yaml
tools_live:
  - web_search
  - us_law_search
  - us_local_regulation
  - competitor_research
  - industry_benchmark
  - tax_calculator
tools_skipped: []
```

If `tools_skipped` still lists search tools → the key wasn't injected. Re-run install-mcp.

---

## Step 5 — Fill in the Brain (one time)

Open `<vault>/` in Obsidian. Open `00-Brain/`:

| File | What to fill in |
|---|---|
| `strategy.md` | 3-5 year vision, mission, ICP (3 traits), yearly goals |
| `products.md` | Product/service table: \| code \| name \| price \| margin \| status \| |
| `budget.md` | Total yearly budget, allocation by department |
| `headcount.md` | Which departments are active (`- 01-hardware-engineering`, `- 02-npi-program-management`, ...), expertise gaps |
| `state.md` | Stage (seed/growth/mature/pivot), fleet size, quarterly KPIs |
| `laws.md` | Applicable law & certifications — pre-filled with TBOC, FLSA, FCC Part 15, UL, PCI PTS/EMVCo, customs/HTS notes. Add product specifics |

Ask Claude for help:
```
Read the current Brain of the vault at F:\work\division-vault. Suggest how I should
fill in the strategy for an electronic-device division.
```

---

## Step 6 — Run your first task

```
We need to pilot 500 units of the new terminal with our top customer by 06/30.
Budget about $20,000.
```

The plugin runs the 5 stages automatically:

### Stage 1: `vn_run` (router + clarification)
- Classifies COMPLEX (3-5 departments debate)
- Departments: `01-hardware-engineering`, `02-npi-program-management`, `03-quality-reliability`, `05-service-operations`
- Creates `03-clarification.md` with 4 questions
- → Open the file, answer the checkboxes

### Stage 2: `vn_resume`
- Reads the answers → continue

### Stage 3: `vn_meeting`
- Live research: certification rules + hardware benchmarks
- Intra-department round: each team gives its manager a short take, the manager synthesizes
- 5 managers debate × Pro + Con + 3 perspectives (Growth/Cautious/Balanced)
- Synthesizer + Translator + Citation validator → `07-decision-report.md`

### Stage 4: `vn_approve`
- Generates `08-execution-plan.md` with:
  - A tasks table (owner, deadline, deliverable)
  - A table of templates to render
  - Risks + mitigation + KPIs

### Stage 5: `vn_execute`
- Renders `.docx/.xlsx` from templates → `<vault>/03-Outputs/<task>/`
- You open the folder, send it to the team

---

## Next

- [User Guide](user-guide.md) — each stage in detail + other task examples
- [Configuration](configuration.md) — `.vncoderc`, packs, BYOT
- [Troubleshooting](troubleshooting.md) — common errors
- [Architecture](architecture.md) — architecture + 6 RULES
