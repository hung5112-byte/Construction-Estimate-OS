"""IMAP watcher — polls an inbox (Gmail-compatible) for UNSEEN mail.

Stdlib only (imaplib + email). Credentials come from env vars — never
hardcoded. For Gmail: enable 2FA, create an App Password, set:

  BD_SIGNALS_IMAP_HOST=imap.gmail.com   (default)
  BD_SIGNALS_IMAP_USER=you@example.com
  BD_SIGNALS_IMAP_PASSWORD=<app password>
  BD_SIGNALS_IMAP_FOLDER=INBOX          (default)

Fetching a message marks it \\Seen, so the same mail is not reprocessed
on the next poll.
"""
from __future__ import annotations

import email
import email.policy
import imaplib
import os
from datetime import datetime
from email.message import EmailMessage

from core.signals.schema import Event


class ImapConfig:
    def __init__(self) -> None:
        self.host = os.environ.get("BD_SIGNALS_IMAP_HOST", "imap.gmail.com")
        self.user = os.environ.get("BD_SIGNALS_IMAP_USER", "")
        self.password = os.environ.get("BD_SIGNALS_IMAP_PASSWORD", "")
        self.folder = os.environ.get("BD_SIGNALS_IMAP_FOLDER", "INBOX")

    def validate(self) -> None:
        missing = [n for n, v in (("BD_SIGNALS_IMAP_USER", self.user),
                                  ("BD_SIGNALS_IMAP_PASSWORD", self.password)) if not v]
        if missing:
            raise EnvironmentError(f"Missing env vars: {', '.join(missing)}")


def _body_text(msg: EmailMessage) -> str:
    part = msg.get_body(preferencelist=("plain", "html"))
    if part is None:
        return ""
    text = part.get_content()
    return text if isinstance(text, str) else ""


def _to_event(uid: str, raw: bytes) -> Event:
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    received = msg.get("Date")
    try:
        received_at = email.utils.parsedate_to_datetime(received) if received else datetime.now()
    except (TypeError, ValueError):
        received_at = datetime.now()
    return Event(
        source="email",
        external_id=uid,
        sender=str(msg.get("From", "unknown")),
        subject=str(msg.get("Subject", "")),
        body=_body_text(msg),
        received_at=received_at.replace(tzinfo=None),
    )


def fetch_events(config: ImapConfig | None = None, limit: int = 25) -> list[Event]:
    """Fetch up to `limit` UNSEEN messages as Events (oldest first)."""
    config = config or ImapConfig()
    config.validate()

    events: list[Event] = []
    conn = imaplib.IMAP4_SSL(config.host)
    try:
        conn.login(config.user, config.password)
        conn.select(config.folder)
        status, data = conn.uid("SEARCH", None, "UNSEEN")
        if status != "OK":
            return events
        uids = data[0].split()[:limit]
        for uid in uids:
            status, msg_data = conn.uid("FETCH", uid, "(RFC822)")
            if status == "OK" and msg_data and msg_data[0]:
                events.append(_to_event(uid.decode(), msg_data[0][1]))
    finally:
        try:
            conn.logout()
        except Exception:  # noqa: BLE001 — logout failure must not mask fetched mail
            pass
    return events
