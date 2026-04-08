# version: 1.0
"""Utilities for tool history tracking."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

ALLOWED_ACTIONS = {
    "CREATE",
    "EDIT",
    "STATUS_CHANGE",
    "STATUS_CHANGED",
    "TASK_AUTOCHECK",
    "TASK_ADDED",
    "TASK_DONE",
    "ASSIGN",
    "QR_ISSUE",
    "QR_RETURN",
    "QR_FAULT",
}

TOOL_HISTORY_DIR = Path("data") / "narzedzia_historia"
LOGGER = logging.getLogger(__name__)


try:
    import fcntl

    def _lock_file(handle):
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)

    def _unlock_file(handle):
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

except ImportError:  # pragma: no cover - Windows fallback
    try:
        import msvcrt

        def _lock_file(handle):
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)

        def _unlock_file(handle):
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                pass

    except ImportError:  # pragma: no cover - brak blokady
        def _lock_file(_handle):
            return None

        def _unlock_file(_handle):
            return None


def _is_serializable(value: Any) -> bool:
    try:
        json.dumps(value)
        return True
    except (TypeError, ValueError):
        return False


def _prepare_event(tool_id: str, user: str, action: str, **kwargs: Any) -> Dict[str, Any]:
    tool_identifier = str(tool_id or "").strip()
    action_normalized = str(action or "").strip().upper()
    if not tool_identifier or action_normalized not in ALLOWED_ACTIONS:
        LOGGER.error(
            "[WM-ERR][narzedzia_history] odrzucono event historii (niepoprawne dane): %s",
            {"tool_id": tool_id, "action": action},
        )
        return {}

    timestamp = kwargs.pop("timestamp", None)
    if isinstance(timestamp, datetime):
        timestamp_text = timestamp.isoformat()
    elif isinstance(timestamp, str) and timestamp.strip():
        timestamp_text = timestamp.strip()
    else:
        timestamp_text = datetime.now(timezone.utc).isoformat()

    raw_details: Dict[str, Any] = {}
    for key, value in kwargs.items():
        if key == "details" and isinstance(value, dict):
            raw_details.update(value)
            continue
        if isinstance(key, str):
            raw_details[key] = value

    raw_details.setdefault("user", user)
    details: Dict[str, Any] = {}
    for key, value in raw_details.items():
        if not isinstance(key, str):
            continue
        if _is_serializable(value):
            details[key] = value
        else:
            details[key] = repr(value)

    return {
        "timestamp": timestamp_text,
        "tool_id": tool_identifier,
        "action": action_normalized,
        "details": details,
    }


def append_tool_history(tool_id: str, user: str, action: str, **kwargs: Any) -> None:
    """Append an entry to the tool history log.

    Parameters:
        tool_id: Identifier of the tool.
        user: User performing the action.
        action: Allowed action type.
        **kwargs: Additional data stored in the entry.

    The entry is appended as a JSON line with a UTC timestamp.
    """
    event = _prepare_event(tool_id, user, action, **kwargs)
    if not event:
        return

    dest_dir = TOOL_HISTORY_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"{event['tool_id']}.jsonl"

    def _last_event(file_path: Path) -> Optional[Dict[str, Any]]:
        if not file_path.exists():
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                for line in reversed(handle.readlines()):
                    cleaned = line.strip()
                    if not cleaned:
                        continue
                    return json.loads(cleaned)
        except Exception:
            LOGGER.debug("[TOOLS-HIST] Nie udało się odczytać ostatniego wpisu", exc_info=True)
        return None

    last_event = _last_event(path)
    if last_event:
        try:
            if (
                last_event.get("action") == event.get("action")
                and last_event.get("details") == event.get("details")
            ):
                LOGGER.debug(
                    "[TOOLS-HIST] Pominięto duplikat wpisu (%s) dla narzędzia %s",
                    event.get("action"),
                    event.get("tool_id"),
                )
                return
        except Exception:
            LOGGER.debug("[TOOLS-HIST] Nie udało się porównać wpisów historii", exc_info=True)

    line = json.dumps(event, ensure_ascii=False)
    fd = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY)
    with os.fdopen(fd, "a", encoding="utf-8") as f:
        _lock_file(f)
        try:
            f.write(line + "\n")
        finally:
            _unlock_file(f)
