"""Signals daemon entry: python -m core.signals.daemon [--vault .] [--dry-run].

Single pass by default (cron/launchd-friendly); --interval N loops forever.
Recommended first week: run with --dry-run and tune 00-Brain/signal-rules.yaml
against the notes written to 01-Inbox/Events/ before arming real triggers.
"""
from __future__ import annotations

import time
from pathlib import Path

import click
from rich.console import Console

console = Console()


@click.command()
@click.option("--vault", type=click.Path(exists=True), default=".",
              help="Vault path (default: current directory)")
@click.option("--dry-run", is_flag=True,
              help="Triage + log only — never start a meeting")
@click.option("--interval", type=int, default=0,
              help="Loop every N seconds (0 = single pass, for cron/launchd)")
@click.option("--limit", type=int, default=25, help="Max messages per poll")
def main(vault: str, dry_run: bool, interval: int, limit: int) -> None:
    """Poll watchers and run each new event through the signals pipeline."""
    vault_root = Path(vault)
    while True:
        _poll_once(vault_root, dry_run=dry_run, limit=limit)
        if interval <= 0:
            break
        time.sleep(interval)


def _poll_once(vault_root: Path, dry_run: bool, limit: int) -> None:
    from core.llm.providers import get_default_provider
    from core.signals.pipeline import process_event
    from core.signals.watchers.email_imap import fetch_events

    try:
        events = fetch_events(limit=limit)
    except EnvironmentError as exc:
        console.print(f"[red]✗ {exc}[/]")
        raise SystemExit(1)

    if not events:
        console.print("[dim]No new messages.[/]")
        return

    try:
        llm = get_default_provider()
    except Exception:  # noqa: BLE001 — pipeline degrades to keyword fallback
        llm = None
        console.print("[yellow]⚠ No LLM provider — deterministic fallback triage[/]")

    for event in events:
        outcome = process_event(event, vault_root, llm=llm, dry_run=dry_run)
        color = {"trigger-meeting": "red", "log-only": "yellow",
                 "dropped": "dim"}.get(outcome["outcome"], "white")
        console.print(f"[{color}]{outcome['outcome']:16}[/] {event.subject[:60]} "
                      f"— {outcome['reason']}")
        if outcome.get("needs_human"):
            console.print(f"  [bold]→ Department Head action needed:[/] "
                          f"{outcome['task_folder']}")


if __name__ == "__main__":
    main()
