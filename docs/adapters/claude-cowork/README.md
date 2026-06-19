# Claude Cowork Plugin Adapter

Plugin for Claude Cowork. Bundles the `bd-business-os` skill into a `.plugin` package you can install into a Cowork workspace.

## Prerequisites

```bash
pip install bd-business-os
bd-os install-mcp        # auto-edit Claude config (Desktop / Code)
# Restart Claude
```

## Build plugin

```bash
bash adapters/claude-cowork/build-plugin.sh
```

Output: `bd-business-os.plugin`, ready to install into a Cowork workspace.

## Verify

After installing the plugin into Cowork, type naturally about a business task:
> Create an ad campaign targeting high-income individuals

Cowork will activate the `bd-business-os` skill and call the 9 MCP tools (`bd_status`, `bd_run`, `bd_resume`, `bd_meeting`, `bd_approve`, `bd_execute`, `bd_draft`, `bd_onboard`, `bd_upgrade`).

## Notes

- Requires a Claude Pro or Max subscription (the Free tier rate limit is too low)
- 1 COMPLEX task ≈ 30-40 sampling calls
- No ANTHROPIC_API_KEY needed (LLM thinking runs through the subscription)
