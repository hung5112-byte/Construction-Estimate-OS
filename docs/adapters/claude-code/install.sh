#!/usr/bin/env bash
# Install Claude Code skill + register MCP server in Claude Code global config.
set -euo pipefail

CLAUDE_SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$CLAUDE_SKILLS_DIR/bd-business-os"

cp "$(dirname "$0")/skill.md" "$CLAUDE_SKILLS_DIR/bd-business-os/SKILL.md"
echo "✓ Skill installed to $CLAUDE_SKILLS_DIR/bd-business-os/"

# Register MCP server in Claude Code global config (~/.claude.json)
if command -v bd-os &>/dev/null; then
    bd-os install-mcp --target claude-code
    echo "✓ MCP server registered in ~/.claude.json"
else
    echo "⚠ bd-os not found. Run after installing package:"
    echo "    pip install -e ."
    echo "    bd-os install-mcp --target claude-code"
fi

echo ""
echo "Then type a brief in Claude Code — the skill activates automatically."
