"""Channel watchers — each yields normalized core.signals.schema.Event objects.

email_imap ships first; a chat watcher (Slack/Telegram) plugs in by
implementing the same fetch_events() -> list[Event] shape.
"""
