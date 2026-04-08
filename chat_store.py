# Lokalny magazyn wiadomości (Messenger MVP)
# Format: JSONL (1 linia = 1 wiadomość)

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

CHAT_FILE = Path("data/chat_messages.jsonl")
CHAT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Dodatkowy log "produkcyjny" (nie dotykamy narzędzi / zleceń)
PROD_LOG_FILE = Path("data/logi/chat_prod_history.jsonl")
PROD_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def append_message(sender: str, text: str, role: str | None = None) -> None:
    msg = {
        "ts": _now(),
        "from": sender,
        "role": (role or "").strip(),
        "text": text,
        "read_by": [],
    }
    with CHAT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(msg, ensure_ascii=False) + "\n")

    # Log produkcyjny (JSONL) – oddzielny plik, bez zmian w danych domenowych
    try:
        rec = {
            "ts": msg["ts"],
            "type": "chat",
            "from": msg["from"],
            "role": msg.get("role", ""),
            "text": msg["text"],
        }
        with PROD_LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def read_messages(limit: int = 200) -> List[Dict]:
    if not CHAT_FILE.exists():
        return []

    lines = CHAT_FILE.read_text(encoding="utf-8").splitlines()
    msgs = []
    for line in lines[-limit:]:
        try:
            msgs.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return msgs


def get_unread_count(user: str) -> int:
    if not CHAT_FILE.exists():
        return 0

    count = 0
    for m in read_messages():
        if user not in m.get("read_by", []):
            count += 1
    return count


def mark_read(user: str) -> None:
    if not CHAT_FILE.exists():
        return

    msgs = read_messages(limit=10_000)
    changed = False

    for m in msgs:
        rb = m.setdefault("read_by", [])
        if user not in rb:
            rb.append(user)
            changed = True

    if not changed:
        return

    with CHAT_FILE.open("w", encoding="utf-8") as f:
        for m in msgs:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
