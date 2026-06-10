# Troubleshooting — US One Person Company

Common errors + how to fix them.

---

## Installation

### `vn-os: command not found`
- Forgot to activate the venv: `.venv\Scripts\activate` (Win) or `source .venv/bin/activate`
- Forgot `pip install -e .` (note the trailing `.`)
- Verify: `which vn-os` (Linux/Mac) / `where vn-os` (Win)

### `pip install -e .` fails with "Microsoft Visual C++ 14.0 required"
- You need Build Tools for Windows: [vs_buildtools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Or: use pre-built wheels: `pip install -e . --only-binary :all:`

### Python version
```powershell
python --version
# If < 3.11: install Python 3.11+ from python.org
```

---

## MCP Server

### Claude Desktop doesn't see `vn_run`/`vn_meeting`/...
1. Verify config:
   ```powershell
   # Windows
   type "$env:APPDATA\Claude\claude_desktop_config.json"
   ```
2. There must be a `"vn-business-os": {"command": "vn-os-mcp"}` entry
3. Restart Claude Desktop **COMPLETELY** (quit from the system tray, not just close the window)
4. Check Claude Desktop logs:
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`
   - macOS: `~/Library/Logs/Claude/mcp*.log`

### MCP server crashes on startup
The logs show a Python error → usually a missing dep:
```powershell
# Re-install
pip install -e .
# Test directly
vn-os-mcp
# Should hang quietly (waiting for MCP messages). Ctrl+C to exit.
```

### `'dict' object has no attribute 'content_as_list'`
Fixed in commit `d4c9a33`. Update the repo:
```powershell
git pull
pip install -e .
# Restart Claude Desktop
```

### `vn_run: 'NoneType' object has no attribute 'session'`
The MCP context wasn't injected. The tools are running outside an MCP session (e.g. via the CLI `vn-os run`, which doesn't support MCP sampling). Use the MCP tool in Claude Desktop chat.

---

## Vault setup

### `vn_onboard` timeout (~4 min)
Fixed by removing the subprocess (commit `ad21206`). Update the repo + restart Claude Desktop.

### `vn_run` / `vn_meeting` timeout

**Symptom:** the tool reports a timeout after ~60s, even though the work isn't done.

**Cause:** each step of `vn_run` (router → gap → clarify) and `vn_meeting`
(research + perspectives × N depts + Pro/Con × M rounds + synthesizer) is one LLM
call via MCP sampling. The total round-trip through Claude Desktop easily exceeds the
default client timeout (~60s) when configured with many rounds.

**How to fix (in priority order):**

#### 1. Use `vn_draft` for doc boilerplate
Employment agreement, JD, work rules, receipt, simple SOP → no debate engine needed.
Just one LLM call, ~10-30s, never times out.

```
Draft an employment offer for an accounting assistant at cafe ABC, $45k/year, 2-month introductory period,
must know QuickBooks and US GAAP. Vault: F:\work\xyz-vault.
```

(Claude Desktop will pick `vn_draft` instead of `vn_run` if the prompt is clearly about drafting a
specific document. Otherwise call it explicitly: "Use vn_draft to draft ...")

#### 2. Reduce rounds in `.vncoderc`
The new default (v0.1.0+) is already lite — `0/1/3`. If still slow, reduce further:
```yaml
meeting:
  max_perspective_rounds: 0      # Skip the Round 3 perspective debate
  max_debate_rounds: 1           # 1 round of Pro/Con (not 2)
  total_max: 2                   # Hard cap
```
→ Total ~2-3 LLM calls/meeting instead of 5-10.

#### 3. Increase the MCP client timeout (Claude Desktop)
Edit `claude_desktop_config.json`:
```json
"vn-business-os": {
  "command": "vn-os-mcp",
  "env": {"TAVILY_API_KEY": "..."},
  "timeout": 300000
}
```
Restart Claude Desktop. Raise the timeout to 5 minutes for a heavy meeting.

#### 4. When `vn_run`/`vn_meeting` is worth it
- Strategic decisions: opening a location, changing prices, hiring senior, M&A
- Significant legal/financial risk
- Need multi-perspective review + citation validation

Boilerplate doc → always `vn_draft`.

### Vault path with spaces / Unicode
The plugin supports it but you should avoid it. Recommended:
- ✓ `F:/work/xyz-vault`
- ✓ `C:/Users/admin/vaults/abc`
- ✗ `F:/My Files/vault` (possible Git/PowerShell edge case)
- ✗ `C:/My Documents/vault` (has a space)

### `Vault not found`
- Check the path actually exists: `Test-Path "F:\work\xyz-vault"`
- The plugin expands `~` (home dir) but does NOT expand env vars like `%USERPROFILE%`

---

## Search/Research

### `tools_skipped: [web_search, us_law_search, ...]`
Missing `TAVILY_API_KEY`. Fix:
```powershell
# Chat: enter the key via vn_onboard
# OR edit the file manually:
echo "TAVILY_API_KEY=tvly-xxx" >> "F:/work/xyz-vault/.env"

# Re-install MCP to inject the env
vn-os install-mcp --vault "F:/work/xyz-vault"
# Restart Claude Desktop
```

### `Tavily 401 Unauthorized`
The key is invalid or expired. Create a new key at [tavily.com](https://tavily.com/dashboard).

### `Tavily 429 Too Many Requests`
Free tier exhausted (1000 req/month). Options:
- Wait until next month
- Upgrade the Tavily plan
- Temporarily enable `meeting.use_checkpointer: true` to avoid re-researching after a crash

### Search returns wrong/stale results
The tool cache `<vault>/.cache/tool_cache.db` is kept 24h. Force refresh:
```powershell
Remove-Item "F:/work/xyz-vault/.cache/tool_cache.db"
```

---

## Meeting / Debate

### Meeting hangs forever
- Check `tools_skipped` in `vn_status` — if all 4 Tavily tools are skipped + the brief needs a lot of research → the LLM may loop. Enable at least one tool.
- LLM rate limit → there's a retry in P1.3. If it still hangs → restart Claude Desktop.

### Decision report too short / generic
- Empty Brain / placeholder text → the meeting has no real data to debate
- Fix: fill in `00-Brain/strategy.md`, `products.md`, `state.md` completely

### Decision report has a "claims missing a source" warning
This is a **feature** (P1.8), not a bug. The CEO reviews those claims:
- If the claim is correct → add a citation manually to the report
- If the claim is uncertain → the CEO doesn't approve, re-run the task with more clarification

### `07-decision-report.md` saved but the `.docx` isn't rendered
- Check `08-execution-plan.md` has a `## Templates to create` table
- If not → the execution plan is incomplete, the plugin LLM falls back to extracting template names
- Verify the TemplateResolver finds the template: the name in the table must match `docs/templates-us/<dept>/<name>.docx` or `<vault>/00-Templates-Custom/<dept>/<name>.docx`

### Research tools always return "skipped" despite a key
- Verify the env injection:
  ```powershell
  type "$env:APPDATA\Claude\claude_desktop_config.json" | Select-String "TAVILY"
  ```
- You should see `"TAVILY_API_KEY": "tvly-..."` in the `env:` section of vn-business-os
- If not → re-run `vn-os install-mcp --vault <path>`

---

## Git / Vault sync

### `Git commit failed (Stop 1): ...`
Check `<vault>/.vn-business-os.log`:
```powershell
Get-Content "F:/work/xyz-vault/.vn-business-os.log" -Tail 20
```

Common causes:
- Git not initialized: `cd <vault>; git init`
- Merge conflict from CEO edit + plugin edit on the same file → resolve manually
- Permission denied: vault folder is read-only → fix permissions

### `<vault>/.env` got committed to git
**SERIOUS.** Fix immediately:
```powershell
cd <vault>
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "fix: gitignore .env"
# Rotate keys immediately (Tavily, Anthropic, ...) since they were exposed
```

### Push to GitHub fails (CEO's private repo)
The plugin only commits locally. The CEO does the push:
```powershell
cd <vault>
git remote add origin <your-private-repo-url>
git push -u origin main
```

---

## Performance / Cost

### High LLM cost (>$2/task)
- Reduce `meeting.max_debate_rounds: 1`
- Reduce `meeting.max_perspective_rounds: 0` (skip the perspective phase)
- `translator_mode: off` instead of `final_only` (skip the translator LLM call)

### Meeting runs slowly (>15 min)
- Brain too large → P2.7 already filters per agent, but if the Brain is >20K chars → consider splitting the file (`strategy-1.md`, `strategy-2.md`)
- Research tool slow → reduce queries in the ToolRouter

---

## Plugin upgrade

### A new plugin version is out
```powershell
cd <plugin-dir>
git pull
pip install -e .

# Refresh the existing vault with new prompts
# In Claude chat:
# "Upgrade vault F:/work/xyz-vault"
```

`vn_upgrade` only touches:
- Agent .md (refresh prompts)
- Department.yaml (new aliases)
- Brain frontmatter (inject aliases)

Does NOT touch:
- Brain content (CEO data)
- Tasks/Outputs

### After upgrade, re-test
```powershell
python -m pytest docs/tests/ -q
# Should pass 261+
```

---

## Reporting a bug

If your error isn't here, open a [GitHub issue](https://github.com/<owner>/<repo>/issues) with:
- The full error message (redact API keys if any)
- `vn_status` output
- Plugin version (`git rev-parse HEAD`)
- Python version + OS
- Steps to reproduce
