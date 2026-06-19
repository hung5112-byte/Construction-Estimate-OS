# Design: Claude Code MCP Support

**Date:** 2026-05-08  
**Status:** Approved

## Problem

`bd-os install-mcp` only writes to the Claude Desktop config (`claude_desktop_config.json`). Claude Code uses a separate config (`~/.claude.json`). The Department Head wants to type a brief in the Claude Code terminal — the `bd_run`, `bd_meeting`... tools must be available via MCP.

## Solution

Extend `install_mcp.py` + `cli.py` to support the Claude Code global MCP config. The MCP server itself doesn't change — it runs the same on both hosts.

## Architecture

Only 2 files change:

| File | Change |
|------|----------|
| `core/install_mcp.py` | Add `get_claude_code_config_path()` + `write_claude_code_config()` + rename `install_mcp()` → `write_desktop_config()` |
| `core/cli.py` | Add `--target [desktop\|claude-code\|both]` to the `install-mcp` command (default: `both`) |
| `adapters/claude-code/install.sh` | Update to call `bd-os install-mcp --target claude-code` |

## Config Paths

| Host | Config file |
|------|------------|
| Claude Desktop | `%APPDATA%/Claude/claude_desktop_config.json` (Windows) |
| Claude Code | `~/.claude.json` (cross-platform) |

Both use the same `mcpServers` key and the same JSON format — the code reuses `get_server_command()`.

## `install_mcp.py` Changes

```python
def get_claude_code_config_path() -> Path:
    return Path.home() / ".claude.json"

def write_claude_code_config(vault_root: Path | None = None) -> Path:
    config_path = get_claude_code_config_path()
    config = json.loads(config_path.read_text()) if config_path.exists() else {}
    config.setdefault("mcpServers", {})
    command, args = get_server_command()
    entry = {"command": command, "args": args}
    if vault_root:
        entry["env"] = {"VN_OS_VAULT": str(vault_root)}
    config["mcpServers"]["bd-business-os"] = entry
    config_path.write_text(json.dumps(config, indent=2))
    return config_path

def write_desktop_config(vault_root: Path | None = None) -> Path:
    # rename of the old install_mcp() — logic unchanged
    ...

def install_mcp(target: str = "both", vault_root: Path | None = None) -> None:
    if target in ("desktop", "both"):
        path = write_desktop_config(vault_root)
        print(f"✓ Claude Desktop: {path}")
    if target in ("claude-code", "both"):
        path = write_claude_code_config(vault_root)
        print(f"✓ Claude Code:    {path}")
    print("→ Restart Claude Desktop + Claude Code to apply.")
```

## CLI Usage

```bash
bd-os install-mcp                                       # default: both
bd-os install-mcp --target claude-code
bd-os install-mcp --target desktop
bd-os install-mcp --target both --vault F:/work/xyz-vault
```

## Error Handling

- Config file doesn't exist → create a new one with `{}`
- `mcpServers` key missing → `setdefault`
- `bd-os-mcp` not on PATH → fallback `python -m core.mcp_server` (current logic)

## Testing

- Unit test `write_claude_code_config()`: mock `Path.home()`, assert the JSON output is correct
- Unit test merge: an existing config with other `mcpServers` → don't overwrite the other entry
- Unit test `--target` flag: assert the right function is called

## Out of Scope

- The MCP sampling provider doesn't change
- The `adapters/claude-code/skill.md` skill is already correct, no content change needed
- Claude Code per-project `.mcp.json` (the global one is enough)
