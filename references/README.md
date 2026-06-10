# References

> Source material to vendor / reference when re-coding or comparing patterns.

---

## 📦 Files available

### `business-builder.plugin` (~370 KB, zip archive)
- A Claude plugin — 13 skills, 191 standard business documents (originally authored in Vietnamese, now localized to US English)
- Follows ISO 9001:2015, EOS/Traction, E-Myth, McKinsey 7S, SYSTEMology
- The legal/financial content has been re-mapped from Vietnamese law to US federal + Texas law (US GAAP, TBOC, FLSA, IRS)
- **Purpose:** vendor the 191 templates from the plugin's `references/` skill folders into `templates-us/`
- **Vendor script:** `scripts/dev/vendor-bb-plugin.sh` (created in Phase 1, Task 3)
- **How to extract:**
  ```bash
  unzip references/business-builder.plugin -d /tmp/bb-plugin
  # /tmp/bb-plugin/skills/bb-*/references/ contains 191 .md templates
  ```

---

## 🌐 GitHub repos (clone as needed)

### 1. TradingAgents (TauricResearch/TradingAgents)
- URL: https://github.com/TauricResearch/TradingAgents
- **Purpose:** reference debate engine (LangGraph + Bull/Bear + 3-tier risk)
- **Patterns to take:** `tradingagents/graph/trading_graph.py` + `conditional_logic.py` + `checkpointer.py` + `agent_states.py`
- **How to use:** clone into `references/tradingagents/` (remember to add `references/` to `.gitignore`)

```bash
git clone --depth 1 https://github.com/TauricResearch/TradingAgents references/tradingagents
echo "references/tradingagents/" >> .gitignore
```

⚠️ **RULE 2 (Domain-neutral):** code copied from here MUST rename all Bull/Bear/trade/finance/ticker — don't let it leak into core/.

### 2. agency-agents (msitarzewski/agency-agents)
- URL: https://github.com/msitarzewski/agency-agents
- **Purpose:** reference 144+ role definitions (markdown). Inspiration for the Tech-SaaS agents pack (engineering, design, product...).
- **How to use:** clone for reference, do NOT vendor into the repo (only adapt + localize as needed).

```bash
git clone --depth 1 https://github.com/msitarzewski/agency-agents.git references/agency-agents
echo "references/agency-agents/" >> .gitignore
```

---

## 🔒 Important notes

- This `references/` folder only holds local files or reference clones — **do NOT vendor into the distributed package**
- When the repo is public, add `references/` to `.gitignore` so third-party forks aren't uploaded
- All credits / licenses for source material are noted in the main repo's `LICENSE` / `NOTICE`

---

## 🛠️ When to use this folder?

| Situation | Action |
|---|---|
| Phase 1 Task 3: vendor 191 templates | Run `bash scripts/dev/vendor-bb-plugin.sh references/business-builder.plugin` |
| Phase 2: lift the debate engine | `git clone TradingAgents` → read graph/* → adapt |
| Phase 5: need more role inspiration | `git clone agency-agents` → adapt each agent |
| A new bb-plugin version is available | Copy the new file over `references/business-builder.plugin`, then re-run the vendor script |
