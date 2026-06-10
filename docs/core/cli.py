"""CLI entry: vn-os <command>."""
from __future__ import annotations
import sys

import click
from rich.console import Console

# Windows consoles often default to cp1252 — degrade glyphs to '?' instead of
# crashing on UnicodeEncodeError (e.g. '✓'/'→' when output is piped/captured).
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(errors="replace")

console = Console()


@click.group()
@click.version_option("0.2.0")
def main():
    """VN Business OS — AI agent OS for a US hardware engineering & supply chain division."""


@main.command()
@click.option("--vault", type=click.Path(), default=".", help="Path to vault")
def status(vault):
    """Print the current vault status."""
    from pathlib import Path
    from core.brain.reader import BrainReader

    try:
        ctx = BrainReader(Path(vault)).load()
        console.print("[green]✓[/] Brain loaded")
        console.print(f"  ICP: {ctx.strategy.icp[:60]}")
        console.print(f"  Products: {len(ctx.products)}")
        console.print(f"  Active depts: {len(ctx.headcount.active_departments)}")
    except FileNotFoundError as e:
        console.print(f"[red]✗[/] {e}")


@main.command()
@click.argument("brief_arg", required=False, default=None)
@click.option("--brief", "brief_opt", default=None, help="Task brief (alternative to positional argument)")
@click.option("--vault", type=click.Path(), default=".", help="Vault path (default: current directory)")
def run(brief_arg, brief_opt, vault):
    """Run a task through the orchestrator (Stage 1: brief → clarification).

    Usage (short syntax — recommended):
      vn-os run "Draft an RMA intake SOP, 10-business-day turnaround"

    Or the long syntax (backward compat):
      vn-os run --vault . --brief "Draft an RMA intake SOP..."
    """
    from pathlib import Path
    from core.orchestrator.flow_controller import FlowController, FlowStage
    from core.llm.providers import get_default_provider

    # Resolve brief: positional arg takes priority, fallback to --brief option
    brief = brief_arg or brief_opt
    if not brief:
        console.print("[red]✗ Missing brief. Use:[/]")
        console.print('  [cyan]vn-os run "Your brief text"[/]')
        console.print("Or:")
        console.print('  [cyan]vn-os run --brief "Your brief text"[/]')
        return

    from core.utils.config import apply_vault_env_to_os
    vault_path = Path(vault)
    apply_vault_env_to_os(vault_path)
    fc = FlowController(vault_root=vault_path, llm=get_default_provider())
    result = fc.run(brief)

    if result.stage == FlowStage.PAUSE_CLARIFICATION:
        console.print("[yellow]⏸  Paused for clarification[/]")
        console.print(f"   Folder: {result.task_folder}")
        console.print(f"   {result.message}")
        console.print(f"\n[bold]Next:[/] open {result.task_folder}/03-clarification.md, "
                      f"tick your answers, save the file. Then run:")
        console.print(f"  [cyan]vn-os resume {result.task_folder}[/]")
    elif result.stage == FlowStage.ERROR:
        console.print(f"[red]✗ {result.error}[/]")
    else:
        console.print(f"[green]→ {result.stage.value}[/]: {result.message}")


@main.command()
@click.argument("task_folder", type=click.Path(exists=True))
def resume(task_folder):
    """Resume the flow after the CEO answers clarification."""
    from pathlib import Path
    from core.orchestrator.flow_controller import FlowController, FlowStage
    from core.llm.providers import get_default_provider

    from core.utils.config import apply_vault_env_to_os
    folder = Path(task_folder)
    vault_root = folder.parent.parent   # task_folder = vault/02-Tasks/<id>
    apply_vault_env_to_os(vault_root)

    fc = FlowController(vault_root=vault_root, llm=get_default_provider())
    result = fc.resume_after_clarification(folder)
    if result.stage == FlowStage.ERROR:
        console.print(f"[red]✗ {result.error}[/]")
    else:
        console.print(f"[cyan]Stage:[/] {result.stage.value}")
        console.print(f"   {result.message}")


@main.command()
@click.argument("task_folder", type=click.Path(exists=True))
def meeting(task_folder):
    """After the CEO answers clarification → run the meeting (Stop 1)."""
    from pathlib import Path
    import re
    from core.orchestrator.flow_controller import FlowController
    from core.llm.providers import get_default_provider

    from core.utils.config import apply_vault_env_to_os
    folder = Path(task_folder)
    apply_vault_env_to_os(folder.parent.parent)
    fc = FlowController(vault_root=folder.parent.parent, llm=get_default_provider())

    routing_md = (folder / "01-routing.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Departments:\*\* (.+)", routing_md)
    if not m:
        console.print("[red]✗ Cannot find Departments line in 01-routing.md[/]")
        return
    depts = [d.strip() for d in m.group(1).split(",")]

    result = fc.run_meeting(folder, departments=depts)
    console.print(f"[green]→ {result.stage.value}[/]: {result.message}")


@main.command()
@click.argument("task_folder", type=click.Path(exists=True))
def approve(task_folder):
    """CEO approves the decision report → generate the execution plan."""
    from pathlib import Path
    from core.orchestrator.flow_controller import FlowController
    from core.llm.providers import get_default_provider

    from core.utils.config import apply_vault_env_to_os
    folder = Path(task_folder)
    apply_vault_env_to_os(folder.parent.parent)
    fc = FlowController(vault_root=folder.parent.parent, llm=get_default_provider())
    result = fc.approve_decision(folder)
    console.print(f"[green]{result.message}[/]")


@main.command(name="execute")
@click.argument("task_folder", type=click.Path(exists=True))
def execute_cmd(task_folder):
    """CEO approves execute → generate .docx/.xlsx into 03-Outputs/."""
    from pathlib import Path
    from core.orchestrator.flow_controller import FlowController
    from core.llm.providers import get_default_provider

    from core.utils.config import apply_vault_env_to_os
    folder = Path(task_folder)
    apply_vault_env_to_os(folder.parent.parent)
    fc = FlowController(vault_root=folder.parent.parent, llm=get_default_provider())
    result = fc.execute(folder)
    console.print(f"[green]→ DONE[/] {result.message}")


@main.command()
@click.option("--vault", type=click.Path(), required=True)
def onboard(vault):
    """Wizard to create a new vault for a company."""
    import subprocess
    import sys
    from pathlib import Path
    repo = Path(__file__).parent.parent
    subprocess.run(
        [sys.executable, str(repo / "scripts" / "onboard.py"), "--vault", vault]
    )


@main.command(name="install-mcp")
@click.option(
    "--vault",
    type=click.Path(exists=True, file_okay=False),
    help="Vault path to load .env (TAVILY_API_KEY, ...) and inject into the MCP env",
)
@click.option(
    "--target",
    type=click.Choice(["desktop", "claude-code", "both"], case_sensitive=False),
    default="both",
    show_default=True,
    help="Host to register the MCP server with",
)
def install_mcp_cmd(vault, target):
    """Install vn-business-os as MCP server (Claude Desktop + Claude Code).

    Registers with both by default. Use --target to choose one.
    After installing, restart Claude Desktop / Claude Code to load the server.
    """
    from core.install_mcp import install_for_target
    from pathlib import Path

    results = install_for_target(
        target=target,
        vault_path=Path(vault) if vault else None,
    )

    for host, result in results.items():
        label = "Claude Desktop" if host == "desktop" else "Claude Code"
        if not result["ok"]:
            console.print(f"[red]✗ {label}: {result.get('error', 'install failed')}[/]")
            continue
        console.print(f"[green]✓ {label}:[/] {result['config_path']}")
        if result.get("backup"):
            console.print(f"   Backup: {result['backup']}")
        if result.get("env_keys_injected"):
            console.print(f"   Env injected: {', '.join(result['env_keys_injected'])}")

    targets_installed = [k for k, v in results.items() if v.get("ok")]
    if targets_installed:
        parts = []
        if "desktop" in targets_installed:
            parts.append("Claude Desktop")
        if "claude-code" in targets_installed:
            parts.append("Claude Code")
        console.print(f"\n[bold]Next:[/] Restart {' + '.join(parts)} to load the MCP server.")


@main.command(name="uninstall-mcp")
@click.option(
    "--target",
    type=click.Choice(["desktop", "claude-code", "both"], case_sensitive=False),
    default="both",
    show_default=True,
    help="Host to remove the MCP server from",
)
def uninstall_mcp_cmd(target):
    """Remove vn-business-os MCP server entry from config(s)."""
    from core.install_mcp import uninstall, get_config_path, get_claude_code_config_path

    targets = []
    if target in ("desktop", "both"):
        targets.append(("desktop", get_config_path()))
    if target in ("claude-code", "both"):
        targets.append(("claude-code", get_claude_code_config_path()))

    for host, cfg_path in targets:
        label = "Claude Desktop" if host == "desktop" else "Claude Code"
        result = uninstall(config_path=cfg_path)
        if result.get("removed"):
            console.print(f"[green]✓ {label}:[/] removed from {result['config_path']}")
        else:
            console.print(f"[yellow]→ {label}:[/] nothing to remove ({result.get('reason', 'unknown')})")


if __name__ == "__main__":
    main()
