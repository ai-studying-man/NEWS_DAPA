from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(frozen=True, slots=True)
class TelegramSendError(RuntimeError):
    """Telegram sendMessage failure."""

    status_code: int
    body: str

    def __str__(self) -> str:
        return f"Telegram send failed: HTTP {self.status_code} {self.body}"


def send_telegram_message(*, token: str, chat_id: str, text: str) -> None:
    """Send a plain text message through Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    }
    timeout = httpx.Timeout(connect=5.0, read=20.0, write=5.0, pool=5.0)
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.post(url, json=payload)
    if response.status_code >= 400:
        raise TelegramSendError(status_code=response.status_code, body=response.text)


def parse_chat_ids(raw_chat_ids: str) -> tuple[str, ...]:
    """Parse comma-separated Telegram chat IDs."""
    return tuple(
        chat_id
        for chat_id in (part.strip() for part in raw_chat_ids.split(","))
        if chat_id
    )


def send_telegram_messages(
    *,
    token: str,
    chat_ids: tuple[str, ...],
    text: str,
) -> None:
    """Send the same message to one or more Telegram chats."""
    for chat_id in chat_ids:
        send_telegram_message(token=token, chat_id=chat_id, text=text)
