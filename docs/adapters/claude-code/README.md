# Claude Code / Desktop Skill Adapter

Skill for Claude Code (CLI / desktop). After installing, the Department Head types naturally about a business task and the skill activates and calls the MCP tools.

## Prerequisites

```bash
pip install bd-business-os
bd-os install-mcp        # auto-edit claude_desktop_config.json
# Restart Claude Desktop
```

## Install skill

```bash
bash adapters/claude-code/install.sh
```

## Verify

In a Claude Desktop / Code session, type:
> Create an ad campaign targeting high-income individuals

Claude will:
1. Detect the `bd-business-os` skill is active
2. Call `bd_status(vault)` to verify the Brain
3. Call `bd_run(brief, vault)` → PAUSE for clarification
4. Read `03-clarification.md`, ask the Department Head to answer
5. Continue through the stages

## Notes

- Requires a Claude Pro or Max subscription (the Free tier rate limit is too low)
- 1 COMPLEX task ≈ 30-40 sampling calls
- No ANTHROPIC_API_KEY needed (LLM thinking runs through the subscription)
