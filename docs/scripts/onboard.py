"""Onboarding wizard CLI — wraps core.onboard library.

Pure Python lib lives in core/onboard.py — this is just a CLI front-end
for interactive wizard / non-interactive mode.
"""
from __future__ import annotations
import sys
from pathlib import Path

import click
from rich.console import Console

# Allow running this script directly: ensure repo root on sys.path so `core` imports.
_REPO_ROOT = Path(__file__).parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.onboard import onboard_vault  # noqa: E402

# Windows consoles often default to cp1252 — degrade glyphs to '?' instead of
# crashing on UnicodeEncodeError (e.g. '✓' when output is piped/captured).
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(errors="replace")

console = Console()


@click.command()
@click.option("--vault", type=click.Path(), required=True, help="Vault destination")
@click.option("--non-interactive", is_flag=True, help="Skip prompts (for CI/MCP)")
@click.option("--pack", multiple=True, help="Pack code(s) to install")
def main(vault, non_interactive, pack):
    """Onboard wizard: create a vault + choose packs + import company templates."""
    vault_path = Path(vault).expanduser().resolve()
    selected_packs = list(pack)
    byot_src = None

    if vault_path.exists() and any(vault_path.iterdir()):
        if not non_interactive:
            from rich.prompt import Confirm
            if not Confirm.ask(
                f"⚠️  {vault_path} already has data. Continue? (will overwrite)"
            ):
                console.print("[red]Cancelled.[/]")
                return

    # Interactive pack selection
    api_keys: dict[str, str] = {}
    if not non_interactive and not selected_packs:
        from rich.prompt import Confirm, Prompt

        for code, name in [
            ("fnb", "F&B (restaurant/cafe/bar)"),
            ("retail", "Retail (shop/e-commerce/D2C)"),
            ("tech-saas", "Tech/SaaS (software startup)"),
        ]:
            if Confirm.ask(f"  Install the {name} pack?", default=False):
                selected_packs.append(code)

        if Confirm.ask(
            "  Do you have your own contract/form templates?", default=False
        ):
            byot_src = Prompt.ask(
                "  Template folder path (will copy into 00-Templates-Custom/)"
            )

    # Interactive API key prompts
    if not non_interactive:
        from rich.prompt import Confirm, Prompt
        console.print(
            "\n[bold]API Keys[/] — Search/research tools need TAVILY_API_KEY "
            "(law, competitors, web). Skip → tools skip but the flow still runs."
        )
        if Confirm.ask("  Enter TAVILY_API_KEY now?", default=False):
            console.print(
                "    [dim]Free tier 1000 req/month at https://tavily.com[/]"
            )
            tavily = Prompt.ask("    TAVILY_API_KEY", default="", password=True)
            if tavily:
                api_keys["TAVILY_API_KEY"] = tavily
        if Confirm.ask("  Enter ANTHROPIC_API_KEY (fallback outside MCP)?", default=False):
            anth = Prompt.ask("    ANTHROPIC_API_KEY", default="", password=True)
            if anth:
                api_keys["ANTHROPIC_API_KEY"] = anth

    # Run onboard via lib
    console.print("[bold]Creating vault...[/]")
    result = onboard_vault(
        vault_path=vault_path,
        packs=selected_packs,
        byot_src=byot_src,
        init_git=True,
        api_keys=api_keys if api_keys else None,
    )

    if not result.get("ok"):
        console.print(f"[red]✗ {result.get('error', 'unknown error')}[/]")
        sys.exit(1)

    for step in result.get("steps", []):
        console.print(f"  ✓ {step}")
    for w in result.get("warnings", []):
        console.print(f"  [yellow]⚠ {w}[/]")

    console.print(f"\n[green]✅ Vault ready at {result['vault']}[/]")
    console.print("[bold]Next:[/]")
    for s in result.get("next_steps", []):
        console.print(f"  - {s}")


# Backwards-compat shims: existing test imports `_install_pack` from this module.
from core.onboard import (  # noqa: E402, F401
    _install_departments,
    _install_pack,
    _import_byot,
)


if __name__ == "__main__":
    main()
