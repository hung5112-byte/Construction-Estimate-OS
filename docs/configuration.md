# Configuration — Hardware Division OS

The main config files + how to tune them.

---

## Config files

| File | Location | Purpose | Committed? |
|---|---|---|---|
| `.vncoderc` | `<vault>/.vncoderc` or `~/.vncoderc` | Settings (vault path, packs, meeting, translator) | **NO** (gitignored) |
| `.env` | `<vault>/.env` | API keys (TAVILY, ANTHROPIC, ...) | **NO** (gitignored) |
| `claude_desktop_config.json` | OS-specific (see below) | MCP server registration | NO (Claude config) |

### Path to `claude_desktop_config.json`

| OS | Path |
|---|---|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

---

## `.vncoderc` — full reference

```yaml
# Vault path (auto-set by vn_onboard)
vault_path: F:/work/division-vault

# Installed packs (auto-set by vn_onboard; none ship by default)
packs: []

version: "0.1.0"

# Translator scope — RULE 4 Department-Head-friendly language
# off              → do NOT simplify
# final_only       → only the final decision report (default)
# all_intermediate → every output: perspectives, debate, final
translator_mode: final_only

# Meeting config — default LITE to avoid MCP timeout (v0.1.0+)
meeting:
  max_perspective_rounds: 0      # Round 3 perspective debate (default 0 = skip)
  max_debate_rounds: 1           # # of Pro/Con rounds (default 1, raise to 2-3 for strategic)
  max_perspective_debate_rounds: 1
  total_max: 3                   # Hard limit on total LLM calls / meeting
  use_checkpointer: false        # opt-in crash recovery (LangGraph SqliteSaver)
  # V2 intra-department round: every team agent gives a ≤150-word take, then the
  # department manager synthesizes them into the department perspective.
  # Cost: ~1 extra LLM call per team per participating department
  # (a 5-department meeting ≈ 29 round-1 calls instead of 5; budget 10-20 min
  # via MCP sampling). Set false for quick operational meetings.
  intra_department_round: true

# LLM config (only used if NOT going through MCP sampling)
llm:
  primary: claude-sonnet-4-6
  secondary: gemini-2-5-pro
  max_retries: 3
  max_tokens_per_task: 100000
  max_cost_usd_per_task: 2.0
```

### When to edit?

- **Never** edit `vault_path`, `packs`, `version` — auto-set by vn_onboard
- Commonly edited:
  - `meeting.intra_department_round: false` for quick/cheap meetings (managers speak without the team round — ~5× fewer round-1 calls)
  - `translator_mode: all_intermediate` if you want every intermediate output simplified
  - `meeting.max_debate_rounds: 2-3` for strategic decisions (trade-off: +50% cost, +1-2 min latency, MCP-timeout risk)
  - `meeting.max_perspective_rounds: 1` to enable the Round 3 perspective debate
  - `meeting.use_checkpointer: true` if you need crash recovery (advanced)

> **Recommendation:** keep the lite defaults (`0/1/3`) for operational tasks. Bump rounds only when
> running a big strategic decision, and raise the MCP client timeout at the same time
> (see [troubleshooting.md](troubleshooting.md#vn_run--vn_meeting-timeout)).

---

## `.env` — API keys

```bash
# Search law/competitors/web (free 1000 req/month at tavily.com)
TAVILY_API_KEY=tvly-xxx

# NOT needed when using MCP sampling via Claude Desktop
ANTHROPIC_API_KEY=

# Optional fallbacks
GOOGLE_API_KEY=
OPENAI_API_KEY=
BRAVE_API_KEY=
```

### After adding/changing a key — REQUIRED

```powershell
vn-os install-mcp --vault "F:\work\xyz-vault"
# Restart Claude Desktop
```

→ Injects the new env into the MCP server. The plugin reads `<vault>/.env` on every request, but the MCP server process is launched by Claude Desktop with the startup env → a re-install is required.

---

## Packs

No packs ship by default — the 5 division departments are the core. The pack
mechanism remains available for overlays you build yourself.

### Create a new pack
See [how-to-create-pack.md](how-to-create-pack.md). In short:
1. Create `docs/packs/<your-pack>/pack.yaml`
2. Add new departments under `docs/packs/<your-pack>/departments/`
3. (Optional) `brain-template/` to override the default Brain

### Install your pack
Edit `.vncoderc`, add `- <your-pack>` under `packs:`, then call `vn_upgrade` —
or pass `packs=["<your-pack>"]` to `vn_onboard` for a new vault.

---

## BYOT — Bring Your Own Templates

If the business has its own contract/form templates → import them into `<vault>/00-Templates-Custom/`.

### Method 1: at onboard time
```
Set up the vault. Import templates from the folder F:\old-templates.
```

The plugin auto-classifies files by keyword:
- `schematic-*`, `design-*`, `firmware-*` → `01-hardware-engineering/`
- `bom-*`, `eco-*`, `certification-*`, `po-*`, `sourcing-*` → `02-npi-program-management/`
- `quality-*`, `inspection-*`, `dvt-*`, `8d-*`, `qms-*` → `03-quality-reliability/`
- `supplier-*`, `scar-*`, `vendor-*`, `yield-*` → `04-mfg-supplier-quality/`
- `rma-*`, `repair-*`, `sop-*`, `inventory-*`, `shipping-*`, `freight-*`, `report-*` → `05-service-operations/`
- Other → `_unsorted/` (sort manually later)

### Method 2: after onboarding
Copy the file into `<vault>/00-Templates-Custom/<dept-code>/<file-name>.docx`.

### How the plugin picks a template (RULE 6)
When `vn_execute` needs to render the `rma-process-sop` template:
1. **Division custom**: `<vault>/00-Templates-Custom/05-service-operations/rma-process-sop.docx` ← wins
2. **Pack refs**: `<vault>/01-Departments/05-service-operations/refs/rma-process-sop.docx`
3. **Default**: `docs/templates-us/05-service-operations/rma-process-sop.md`

---

## Multi-company setup (consultant pattern)

One consultant serving multiple companies → one vault per company:

```
F:/clients/
├── abc-coffee/         # Company 1 vault
│   ├── .env            # ABC's TAVILY_API_KEY
│   ├── .vncoderc
│   ├── 00-Brain/
│   ├── 01-Departments/
│   └── ...
├── xyz-tech/           # Company 2 vault
└── def-retail/         # Company 3 vault
```

Re-install the MCP for whichever vault you're working in (Claude Desktop reads only one env at a time):
```powershell
vn-os install-mcp --vault "F:\clients\abc-coffee"
# Work with ABC...
vn-os install-mcp --vault "F:\clients\xyz-tech"
# Work with XYZ...
```

The tool cache is per-vault (P2.3) — no cross-poisoning.

---

## Advanced — Custom MCP server

If you need to wrap the MCP with a specific env (e.g. staging vs. prod):

Edit `claude_desktop_config.json` manually:
```json
{
  "mcpServers": {
    "vn-business-os-prod": {
      "command": "vn-os-mcp",
      "env": {
        "TAVILY_API_KEY": "tvly-prod",
        "VN_OS_VAULT": "F:/clients/abc-coffee"
      }
    },
    "vn-business-os-staging": {
      "command": "vn-os-mcp",
      "env": {
        "TAVILY_API_KEY": "tvly-staging"
      }
    }
  }
}
```

Restart Claude Desktop → both MCP servers are available in chat.
