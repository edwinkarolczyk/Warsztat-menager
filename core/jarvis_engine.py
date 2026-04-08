# version: 1.0
"""Silnik integrujący Jarvisa z główną aplikacją Warsztat Menager."""

from __future__ import annotations

import json
import os
import re
import threading
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from wm_log import err as wm_err
from wm_log import info as wm_info

# >>> PATCH START: Jarvis – GUI notifications
from core.path_utils import resolve_root_path
# <<< PATCH END: Jarvis – GUI notifications

try:
    from core.jarvis_prompt_engine import DEFAULT_MODEL, summarize_wm_data
except Exception as exc:  # pragma: no cover - zależne od środowiska
    summarize_wm_data = None  # type: ignore[assignment]
    DEFAULT_MODEL = "gpt-3.5-turbo"
    _PROMPT_ENGINE_IMPORT_ERROR = exc
else:
    _PROMPT_ENGINE_IMPORT_ERROR = None

try:
    from config_manager import ConfigManager
except Exception as exc:  # pragma: no cover - defensywna degradacja
    ConfigManager = None  # type: ignore[assignment]
    _CONFIG_MANAGER_IMPORT_ERROR = exc
else:
    _CONFIG_MANAGER_IMPORT_ERROR = None


def _data_root(cfg) -> Path:
    if cfg is not None:
        try:
            candidate = cfg.path_data()
        except Exception:
            candidate = None
        else:
            if candidate:
                return Path(candidate)

    env = os.environ.get("WM_DATA_ROOT", "").strip()
    if env:
        resolved = resolve_root_path("<root>", env)
        return Path(resolved)

    fallback = resolve_root_path("<root>", "data")
    return Path(fallback)


_JARVIS_TIMER: threading.Timer | None = None
_JARVIS_TIMER_LOCK = threading.Lock()
_LOGGED_ALERTS: set[str] = set()
_LAST_INFO: dict[str, bool] = {
    "disabled": False,
    "missing_engine": False,
    "missing_config": False,
    "ai_disabled": False,
}
_notifications: list[dict[str, Any]] = []
_NOTIFICATIONS_FILE: Path | None = None
_NOTIFICATIONS_LOCK = threading.Lock()
_NOTIFICATIONS_MTIME: float | None = None

_STATUS_FILE: Path | None = None
_STATUS_LOCK = threading.Lock()
_STATUS_CACHE: dict[str, Any] = {}
_STATUS_MTIME: float | None = None


_LEVEL_NAMES = {
    0: "info",
    1: "info",
    2: "info",
    3: "warning",
    4: "error",
    5: "error",
}


# >>> PATCH START: Jarvis – GUI notifications
def _jarvis_storage_dir(cfg: ConfigManager | None = None) -> Path:
    """Return the directory where Jarvis stores its runtime data."""

    if cfg is None:
        cfg_factory = globals().get("_config_manager")
        if callable(cfg_factory):
            try:
                cfg = cfg_factory()
            except Exception:
                cfg = None
    data_root = _data_root(cfg)
    return data_root / "jarvis"


def _emit_gui_notification(category: str, message: str, level: int) -> bool:
    """Emit Jarvis notification to GUI toasts if possible."""

    title = (category or "jarvis").strip().upper() or "JARVIS"
    text = message.strip()
    payload = text or title
    level_name = _LEVEL_NAMES.get(int(level), "info")

    toast_ok = False
    try:
        from jarvis_dispatch import dispatch as _jarvis_dispatch
    except Exception as dispatch_exc:
        print(f"[JARVIS][DISPATCH][WARN] {dispatch_exc}")
    else:
        try:
            toast_ok = bool(
                _jarvis_dispatch(
                    f"{title}: {payload}",
                    level=level_name,
                    origin="Jarvis",
                )
            )
        except Exception as dispatch_exc:
            print(f"[JARVIS][DISPATCH][ERR] {dispatch_exc}")

    if not toast_ok:
        try:
            from gui_notifications import show_notification as _show_notification
        except Exception:
            pass
        else:
            try:
                toast_ok = bool(_show_notification(f"[{title}] {payload}", level=level_name))
            except Exception:
                toast_ok = False

    if toast_ok:
        try:
            wm_info(
                "core.jarvis_engine",
                "Jarvis → Toast OK",
                category=title,
                level=level_name,
            )
        except Exception:
            pass
        print("Jarvis → Toast OK")

    return toast_ok


def _update_status_flag(*, offline: bool, reason: str | None, source: str) -> None:
    """Update status cache without emitting duplicate GUI notifications."""

    normalized_reason = None
    if reason is not None:
        normalized_reason = reason.strip() or None

    timestamp = datetime.now().isoformat(timespec="seconds")
    level = 4 if offline else 1
    event = {
        "timestamp": timestamp,
        "category": "fallback" if offline else "status",
        "message": normalized_reason
        or ("Jarvis działa w trybie offline." if offline else "Jarvis działa poprawnie."),
        "level": level,
        "level_name": _LEVEL_NAMES.get(level, "info"),
        "source": source,
    }

    with _STATUS_LOCK:
        _refresh_status_cache_locked()
        current_offline = bool(_STATUS_CACHE.get("offline"))
        current_reason = str(_STATUS_CACHE.get("offline_reason") or "").strip()
        if (
            current_offline == offline
            and (current_reason or None) == (normalized_reason or None)
        ):
            _STATUS_CACHE["updated_at"] = timestamp
            _persist_status_locked()
            return

        history = _STATUS_CACHE.get("history")
        if not isinstance(history, list):
            history = []
        history.append(deepcopy(event))
        _STATUS_CACHE["history"] = history[-50:]
        _STATUS_CACHE["last_event"] = deepcopy(event)
        _STATUS_CACHE["offline"] = offline
        if normalized_reason:
            _STATUS_CACHE["offline_reason"] = normalized_reason
        else:
            _STATUS_CACHE.pop("offline_reason", None)
        _STATUS_CACHE["updated_at"] = timestamp
        _persist_status_locked()


# <<< PATCH END: Jarvis – GUI notifications


def _notifications_path() -> Path:
    """Return the path to the persistent notifications JSON file."""

    global _NOTIFICATIONS_FILE
    if _NOTIFICATIONS_FILE is not None:
        return _NOTIFICATIONS_FILE

    env_override = os.environ.get("WM_JARVIS_NOTIFICATIONS", "").strip()
    if env_override:
        candidate = Path(resolve_root_path("<root>", env_override))
    else:
        candidate = _jarvis_storage_dir() / "jarvis_notifications.json"

    _NOTIFICATIONS_FILE = candidate
    return candidate


def _status_path() -> Path:
    """Return the path to the persistent status JSON file."""

    global _STATUS_FILE
    if _STATUS_FILE is not None:
        return _STATUS_FILE

    notifications_dir = _notifications_path().parent
    candidate = notifications_dir / "jarvis_status.json"
    _STATUS_FILE = candidate
    return candidate


def _refresh_notifications_cache_locked() -> None:
    """Synchronise in-memory notifications with the on-disk cache."""

    global _NOTIFICATIONS_MTIME
    path = _notifications_path()
    try:
        stat = path.stat()
    except FileNotFoundError:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as handle:
                json.dump([], handle, ensure_ascii=False, indent=2)
        except Exception:
            pass
        _notifications.clear()
        _NOTIFICATIONS_MTIME = None
        return

    mtime = stat.st_mtime
    if _NOTIFICATIONS_MTIME is not None and mtime <= _NOTIFICATIONS_MTIME:
        return

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        data = []

    if not isinstance(data, list):
        data = []

    _notifications.clear()
    _notifications.extend(
        [entry for entry in data if isinstance(entry, dict)][-100:]
    )
    _NOTIFICATIONS_MTIME = mtime


def _persist_notifications_locked() -> None:
    """Write notifications cache to disk, ignoring IO errors."""

    global _NOTIFICATIONS_MTIME
    path = _notifications_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(_notifications[-100:], handle, ensure_ascii=False, indent=2)
        _NOTIFICATIONS_MTIME = path.stat().st_mtime
    except Exception:
        pass


with _NOTIFICATIONS_LOCK:
    _refresh_notifications_cache_locked()


def _refresh_status_cache_locked() -> None:
    """Synchronise in-memory status information with the on-disk cache."""

    global _STATUS_MTIME
    path = _status_path()
    try:
        stat = path.stat()
    except FileNotFoundError:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as handle:
                json.dump({}, handle, ensure_ascii=False, indent=2)
        except Exception:
            pass
        _STATUS_CACHE.clear()
        _STATUS_MTIME = None
        return

    mtime = stat.st_mtime
    if _STATUS_MTIME is not None and mtime <= _STATUS_MTIME:
        return

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        data = {}

    if not isinstance(data, dict):
        data = {}

    _STATUS_CACHE.clear()
    _STATUS_CACHE.update(data)
    _STATUS_MTIME = mtime


def _persist_status_locked() -> None:
    """Write status cache to disk, ignoring IO errors."""

    global _STATUS_MTIME
    path = _status_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(_STATUS_CACHE, handle, ensure_ascii=False, indent=2)
        _STATUS_MTIME = path.stat().st_mtime
    except Exception:
        pass


with _STATUS_LOCK:
    _refresh_status_cache_locked()


def _record_status_event(category: str, message: str, level: int) -> None:
    """Update persistent status cache with the latest notification."""

    timestamp = datetime.now().isoformat(timespec="seconds")
    event = {
        "time": timestamp,
        "category": category,
        "message": message,
        "level": int(level),
        "level_name": _LEVEL_NAMES.get(int(level), "info"),
    }

    with _STATUS_LOCK:
        _refresh_status_cache_locked()
        history = _STATUS_CACHE.get("history")
        if not isinstance(history, list):
            history = []
        history.append(deepcopy(event))
        _STATUS_CACHE["history"] = history[-50:]
        _STATUS_CACHE["last_event"] = deepcopy(event)

        offline_flag = bool(_STATUS_CACHE.get("offline"))
        offline_reason = _STATUS_CACHE.get("offline_reason")

        if category == "fallback" and level >= 3:
            offline_flag = True
            offline_reason = message
        elif category == "status" and level <= 2:
            offline_flag = False
            offline_reason = None

        _STATUS_CACHE["offline"] = offline_flag
        if offline_reason:
            _STATUS_CACHE["offline_reason"] = str(offline_reason)
        else:
            _STATUS_CACHE.pop("offline_reason", None)

        _STATUS_CACHE["updated_at"] = timestamp
        _persist_status_locked()


def notify(category: str, message: str, level: int = 2) -> None:
    """Dodaje komunikat do bufora powiadomień Jarvisa."""

    from datetime import datetime as _dt

    entry = {
        "time": _dt.now().strftime("%H:%M:%S"),
        "category": category,
        "message": message,
        "level": level,
    }
    with _NOTIFICATIONS_LOCK:
        _refresh_notifications_cache_locked()
        _notifications.append(entry)
        if len(_notifications) > 100:
            del _notifications[:-100]
        _persist_notifications_locked()
    _record_status_event(category, message, level)
    print(f"[JARVIS][NOTIFY][{category.upper()}] {message}")

    # >>> PATCH START: Jarvis – GUI notifications
    _emit_gui_notification(category, message, level)
    # <<< PATCH END: Jarvis – GUI notifications

    try:  # pragma: no cover - zależne od środowiska
        from plyer import notification as _plyer_notification

        if level >= 4:
            _plyer_notification.notify(
                title="Jarvis – Warsztat Menager",
                message=message,
                app_name="Warsztat Menager",
                timeout=5,
            )
    except Exception as exc:  # pragma: no cover - zależne od środowiska
        print("[JARVIS][NOTIFY][SYS] Błąd systemowego powiadomienia:", exc)


def get_notifications() -> list[dict[str, Any]]:
    with _NOTIFICATIONS_LOCK:
        _refresh_notifications_cache_locked()
        return list(_notifications)


def get_status() -> dict[str, Any]:
    with _STATUS_LOCK:
        _refresh_status_cache_locked()
        return deepcopy(_STATUS_CACHE)


@dataclass
class JarvisAlert:
    level: str
    message: str
    detail: str | None = None


@dataclass
class JarvisReport:
    summary: str
    stats: Dict[str, Any]
    alerts: list[JarvisAlert] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    offline: bool = False


_WM_LOG_PATH = Path("wm.log")


def _log_alert_once(message: str) -> None:
    normalized = message.strip()
    if not normalized:
        return
    if normalized in _LOGGED_ALERTS:
        return
    _LOGGED_ALERTS.add(normalized)
    try:
        with _WM_LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(f"[JARVIS][ALERT] {normalized}\n")
    except Exception:
        pass


def _add_alert(alerts: list[JarvisAlert], level: str, message: str, detail: str | None = None) -> None:
    alerts.append(JarvisAlert(level=level, message=message, detail=detail))
    log_message = message if not detail else f"{message} ({detail})"
    _log_alert_once(log_message)


_PERSON_KEYS = {
    "login",
    "owner",
    "assigned_to",
    "uzytkownik",
    "user",
    "username",
    "operator",
    "pracownik",
    "osoba",
    "nazwisko",
    "imie",
    "fullname",
    "reported_by",
}

_PERSON_CONTAINER_KEYS = {
    "aktywni",
    "obciazenie",
    "per_operator",
    "per_osoba",
    "users",
    "uzytkownicy",
    "operatorzy",
}

_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\\\[^\s]+|/(?:[^\s]+))")
_IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_NAME_PATTERN = re.compile(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{2,}\s+[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{2,}")


def _config_manager() -> ConfigManager | None:
    if ConfigManager is None:
        return None
    try:
        return ConfigManager()
    except Exception:
        return None


def _load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return None



def anonymize_for_ai(data: Mapping[str, Any]) -> dict[str, Any]:
    """Usuń dane wrażliwe zanim zostaną przekazane do silnika AI."""

    user_map: dict[str, str] = {}
    path_map: dict[str, str] = {}
    ip_map: dict[str, str] = {}

    def _mask_user(value: str) -> str:
        key = value.strip().lower()
        if not key:
            return ""
        alias = user_map.get(key)
        if alias is None:
            alias = f"user_{len(user_map) + 1}"
            user_map[key] = alias
        return alias

    def _mask_path(value: str) -> str:
        key = value.strip()
        alias = path_map.get(key)
        if alias is None:
            alias = f"path_{len(path_map) + 1}"
            path_map[key] = alias
        return alias

    def _mask_ip(value: str) -> str:
        key = value.strip()
        alias = ip_map.get(key)
        if alias is None:
            alias = f"ip_{len(ip_map) + 1}"
            ip_map[key] = alias
        return alias

    def _should_mask_key(key: str, parent: Optional[str]) -> bool:
        lowered = key.lower()
        if lowered in _PERSON_KEYS:
            return True
        if parent and parent.lower() in _PERSON_CONTAINER_KEYS:
            return True
        return False

    def _should_mask_value(parent: Optional[str], grand: Optional[str]) -> bool:
        if parent and parent.lower() in _PERSON_KEYS:
            return True
        if parent and parent.lower() in _PERSON_CONTAINER_KEYS:
            return True
        if grand and grand.lower() in _PERSON_CONTAINER_KEYS:
            return True
        return False

    def _looks_like_name(value: str) -> bool:
        return bool(_NAME_PATTERN.search(value))

    def _sanitize(value: Any, path_keys: tuple[str, ...]) -> Any:
        parent = path_keys[-1] if path_keys else None
        grand = path_keys[-2] if len(path_keys) > 1 else None

        if isinstance(value, Mapping):
            sanitized: dict[Any, Any] = {}
            for raw_key, raw_val in value.items():
                if isinstance(raw_key, str):
                    key_parent = path_keys[-1] if path_keys else None
                    masked_key = raw_key
                    if _should_mask_key(raw_key, key_parent):
                        masked_key = _mask_user(raw_key)
                    elif _IP_PATTERN.search(raw_key):
                        masked_key = _mask_ip(raw_key)
                    elif _PATH_PATTERN.search(raw_key):
                        masked_key = _mask_path(raw_key)
                    next_path = path_keys + (raw_key,)
                else:
                    masked_key = raw_key
                    next_path = path_keys
                sanitized[masked_key] = _sanitize(raw_val, next_path)
            return sanitized

        if isinstance(value, list):
            return [_sanitize(item, path_keys) for item in value]

        if isinstance(value, str):
            sanitized = value
            stripped = sanitized.strip()

            if stripped and _IP_PATTERN.search(sanitized):
                for match in set(_IP_PATTERN.findall(sanitized)):
                    sanitized = sanitized.replace(match, _mask_ip(match))

            if _PATH_PATTERN.search(sanitized):
                sanitized = _PATH_PATTERN.sub(lambda m: _mask_path(m.group(0)), sanitized)

            stripped = sanitized.strip()

            if stripped and (_looks_like_name(stripped) or _should_mask_value(parent, grand)):
                return _mask_user(stripped)

            return sanitized if sanitized else stripped

        return value

    if not isinstance(data, Mapping):
        return {}

    return _sanitize(data, tuple())
_TOOL_INDEX_FILES = {
    "statusy_narzedzi.json",
    "typy_narzedzi.json",
    "szablony_zadan.json",
}

_TOOL_IDLE_STATUSES = {
    "ok",
    "idle",
    "sprawne",
    "wolne",
    "dostępne",
    "dostepne",
    "available",
}

_TASK_DONE_STATUSES = {
    "done",
    "zakończone",
    "zakonczone",
    "zamknięte",
    "zamkniete",
    "wykonane",
    "completed",
}

_MACHINE_ALERT_STATUSES = {
    "awaria",
    "serwis",
    "uszkodzone",
    "stop",
}


def _config_as_dict(cfg: ConfigManager | None) -> dict:
    if cfg is None:
        return {}
    try:
        data = getattr(cfg, "global_cfg", None)
        if isinstance(data, dict):
            return data
    except Exception:
        return {}
    return {}


def _normalize_status(value: object, default: str = "nieznany") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text.lower() if text else default


def _parse_datetime(value: object) -> Optional[datetime]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if "T" not in text and " " in text:
        text = text.replace(" ", "T", 1)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except Exception:
        return None


def _tool_identifier(data: Mapping[str, Any]) -> str:
    for key in ("id", "numer", "nr", "kod"):
        value = data.get(key)
        if value:
            text = str(value).strip()
            if text:
                return text
    return ""


def _count_open_tool_tasks(tasks: Any) -> int:
    if not isinstance(tasks, list):
        return 0
    total = 0
    for task in tasks:
        if not isinstance(task, dict):
            continue
        status = _normalize_status(task.get("status"))
        if status in _TASK_DONE_STATUSES:
            continue
        if task.get("done"):
            continue
        total += 1
    return total


def _tools_summary(cfg: ConfigManager | None, root: Path) -> dict[str, Any]:
    try:
        from utils_tools import load_tools_rows_with_fallback
        from config_manager import resolve_rel
    except Exception:
        load_tools_rows_with_fallback = None  # type: ignore[assignment]
        resolve_rel = None  # type: ignore[assignment]

    rows: List[dict[str, Any]] = []
    if load_tools_rows_with_fallback and resolve_rel:
        try:
            cfg_dict = _config_as_dict(cfg)
            rows, _ = load_tools_rows_with_fallback(cfg_dict, resolve_rel)
        except Exception:
            rows = []

    tools_dir = root / "narzedzia"
    seen_status: dict[str, str] = {}
    status_counter: Counter[str] = Counter()
    open_tasks = 0

    def _register(tool_id: str, status: str, payload: Mapping[str, Any] | None) -> None:
        nonlocal open_tasks
        previous = seen_status.get(tool_id)
        if previous:
            if previous == status:
                open_tasks += _count_open_tool_tasks(payload.get("zadania") if payload else None)
                return
            status_counter[previous] -= 1
        seen_status[tool_id] = status
        status_counter[status] += 1
        open_tasks += _count_open_tool_tasks(payload.get("zadania") if payload else None)

    for row in rows or []:
        if not isinstance(row, dict):
            continue
        tool_id = _tool_identifier(row)
        if not tool_id:
            continue
        file_path = tools_dir / f"{tool_id}.json"
        if file_path.is_file():
            continue
        status = _normalize_status(row.get("status") or row.get("stan"))
        _register(tool_id, status, row)

    if tools_dir.is_dir():
        for item in tools_dir.glob("*.json"):
            if item.name in _TOOL_INDEX_FILES:
                continue
            payload = _load_json(item)
            if not isinstance(payload, dict):
                continue
            tool_id = _tool_identifier(payload) or item.stem
            status = _normalize_status(payload.get("status") or payload.get("stan"))
            _register(tool_id, status, payload)

    idle_tools = [
        tool_id
        for tool_id, status in seen_status.items()
        if status in _TOOL_IDLE_STATUSES
    ]

    return {
        "count": len(seen_status),
        "per_status": {key: value for key, value in status_counter.items() if value > 0},
        "open_tasks": open_tasks,
        "idle": sorted(idle_tools),
    }


def _machines_summary(cfg: ConfigManager | None, root: Path) -> dict[str, Any]:
    try:
        from utils_maszyny import load_machines_rows_with_fallback
        from config_manager import resolve_rel
    except Exception:
        load_machines_rows_with_fallback = None  # type: ignore[assignment]
        resolve_rel = None  # type: ignore[assignment]

    rows: List[dict[str, Any]] = []
    if load_machines_rows_with_fallback and resolve_rel:
        try:
            cfg_dict = _config_as_dict(cfg)
            rows, _ = load_machines_rows_with_fallback(cfg_dict, resolve_rel)
        except Exception:
            rows = []

    if not rows:
        payload = _load_json(root / "maszyny" / "maszyny.json")
        if isinstance(payload, dict):
            rows = [row for row in payload.get("maszyny", []) if isinstance(row, dict)]
        elif isinstance(payload, list):
            rows = [row for row in payload if isinstance(row, dict)]

    status_counter: Counter[str] = Counter()
    service_due_ids: List[str] = []
    service_overdue_ids: List[str] = []
    alert_ids: List[str] = []
    seen_ids: set[str] = set()

    today = datetime.now().date()
    soon_threshold = today + timedelta(days=30)

    for row in rows or []:
        if not isinstance(row, dict):
            continue
        machine_id = str(row.get("id") or row.get("nr_ewid") or "").strip()
        if not machine_id:
            continue
        status = _normalize_status(row.get("status"))
        status_counter[status] += 1
        if status in _MACHINE_ALERT_STATUSES:
            alert_ids.append(machine_id)
        seen_ids.add(machine_id)

        tasks = row.get("zadania")
        if not isinstance(tasks, list):
            continue
        for task in tasks:
            if not isinstance(task, dict):
                continue
            date_str = str(task.get("data") or task.get("termin") or "").strip()
            if not date_str:
                continue
            try:
                deadline = datetime.fromisoformat(date_str)
            except Exception:
                continue
            deadline_date = deadline.date()
            if deadline_date < today:
                service_overdue_ids.append(machine_id)
            elif deadline_date <= soon_threshold:
                service_due_ids.append(machine_id)

    due_set = {mid for mid in service_due_ids if mid}
    overdue_set = {mid for mid in service_overdue_ids if mid}
    alert_set = {mid for mid in alert_ids if mid}

    return {
        "count": len({mid for mid in seen_ids if mid}),
        "per_status": dict(status_counter),
        "service_due_30d": len(due_set),
        "service_overdue": len(overdue_set),
        "service_due_ids": sorted(due_set),
        "service_overdue_ids": sorted(overdue_set),
        "alert_ids": sorted(alert_set),
    }


def _load_tasks_data(root: Path) -> List[dict[str, Any]]:
    candidates = [
        root / "zadania_zlecenia.json",
        root / "zadania_przypisania.json",
        root / "zadania.json",
    ]

    items: List[dict[str, Any]] = []
    seen: set[str] = set()

    for path in candidates:
        if not path.exists():
            continue
        payload = _load_json(path)
        if isinstance(payload, dict):
            records: Iterable[Any] = payload.values()
        elif isinstance(payload, list):
            records = payload
        else:
            continue

        for idx, record in enumerate(records):
            if not isinstance(record, dict):
                continue
            identifier = str(
                record.get("id")
                or record.get("nr")
                or record.get("zlecenie")
                or f"{path.name}:{idx}"
            ).strip()
            if not identifier:
                identifier = f"{path.name}:{idx}"
            if identifier in seen:
                continue
            seen.add(identifier)
            copy = dict(record)
            copy.setdefault("_source", path.name)
            items.append(copy)

    return items


def _load_orders_data(root: Path) -> List[dict[str, Any]]:
    orders_dir = root / "zlecenia"
    items: List[dict[str, Any]] = []

    if orders_dir.is_dir():
        for path in orders_dir.glob("*.json"):
            if path.name.startswith("_"):
                continue
            payload = _load_json(path)
            if isinstance(payload, dict):
                data = dict(payload)
                data.setdefault("_source", path.name)
                items.append(data)
    else:
        payload = _load_json(root / "zlecenia.json")
        if isinstance(payload, list):
            for entry in payload:
                if isinstance(entry, dict):
                    items.append(dict(entry))

    return items


def _tasks_metrics(tasks: List[dict[str, Any]]) -> dict[str, Any]:
    status_counter: Counter[str] = Counter()
    owner_active: Counter[str] = Counter()
    overdue_ids: set[str] = set()
    due_soon_ids: set[str] = set()
    unassigned = 0

    today = datetime.now().date()
    soon_threshold = today + timedelta(days=3)

    for task in tasks:
        if not isinstance(task, dict):
            continue
        status = _normalize_status(task.get("status"))
        status_counter[status] += 1

        login = str(
            task.get("login")
            or task.get("owner")
            or task.get("assigned_to")
            or ""
        ).strip()

        if status not in _TASK_DONE_STATUSES:
            if login:
                owner_active[login] += 1
            else:
                unassigned += 1

        deadline_raw = task.get("termin") or task.get("deadline")
        if deadline_raw:
            try:
                text = str(deadline_raw)
                if text.endswith("Z"):
                    text = text[:-1] + "+00:00"
                deadline = datetime.fromisoformat(text)
                deadline_date = deadline.date()
            except Exception:
                deadline_date = None
            if deadline_date:
                if status not in _TASK_DONE_STATUSES:
                    identifier = str(task.get("id") or task.get("zlecenie") or "").strip()
                    if deadline_date < today:
                        if identifier:
                            overdue_ids.add(identifier)
                    elif deadline_date <= soon_threshold:
                        if identifier:
                            due_soon_ids.add(identifier)

    return {
        "count": len(tasks),
        "per_status": dict(status_counter),
        "per_operator": dict(owner_active),
        "overdue": len(overdue_ids),
        "due_soon": len(due_soon_ids),
        "overdue_ids": sorted(overdue_ids),
        "due_soon_ids": sorted(due_soon_ids),
        "unassigned": unassigned,
    }


def _order_lead_time(order: Mapping[str, Any]) -> Optional[float]:
    history = order.get("historia")
    start = _parse_datetime(order.get("utworzono"))
    finish: Optional[datetime] = None

    if isinstance(history, list):
        for event in history:
            if not isinstance(event, Mapping):
                continue
            when = _parse_datetime(event.get("kiedy"))
            if when is None:
                continue
            description = str(event.get("co") or "").lower()
            if start is None and "utworzenie" in description:
                start = when
            if any(keyword in description for keyword in ("zako", "archiw", "zamk")):
                finish = when

    if finish is None and order.get("status"):
        status = _normalize_status(order.get("status"))
        if status in _TASK_DONE_STATUSES:
            finish = _parse_datetime(order.get("zrealizowano"))

    if start and finish and finish >= start:
        return (finish - start).total_seconds() / 86400.0
    return None


def _orders_summary(
    orders: List[dict[str, Any]],
    tasks_metrics: dict[str, Any],
) -> dict[str, Any]:
    status_counter: Counter[str] = Counter()
    lead_times: List[float] = []

    for order in orders:
        if not isinstance(order, dict):
            continue
        status = _normalize_status(order.get("status"))
        status_counter[status] += 1
        lead = _order_lead_time(order)
        if lead is not None:
            lead_times.append(lead)

    if not status_counter and isinstance(tasks_metrics.get("per_status"), dict):
        status_counter.update(tasks_metrics["per_status"])

    avg_lead = None
    if lead_times:
        avg_lead = sum(lead_times) / len(lead_times)

    return {
        "count": len(orders),
        "per_status": dict(status_counter),
        "lead_time_days_avg": round(avg_lead, 2) if avg_lead is not None else None,
        "lead_time_samples": len(lead_times),
        "tasks_count": tasks_metrics.get("count", 0),
        "overdue": tasks_metrics.get("overdue", 0),
        "due_soon": tasks_metrics.get("due_soon", 0),
        "per_operator": tasks_metrics.get("per_operator", {}),
        "unassigned": tasks_metrics.get("unassigned", 0),
        "tasks_overdue_ids": tasks_metrics.get("overdue_ids", []),
        "tasks_due_soon_ids": tasks_metrics.get("due_soon_ids", []),
    }


def _profiles_summary(
    cfg: ConfigManager | None,
    root: Path,
    tasks: List[dict[str, Any]],
) -> dict[str, Any]:
    try:
        from profile_utils import load_profiles
    except Exception:
        load_profiles = None  # type: ignore[assignment]

    users: List[dict[str, Any]] = []
    if load_profiles and cfg is not None:
        try:
            payload = load_profiles(cfg)
            if isinstance(payload, dict):
                raw_users = payload.get("users") or payload.get("profiles") or []
                if isinstance(raw_users, list):
                    users = [entry for entry in raw_users if isinstance(entry, dict)]
        except Exception:
            users = []

    if not users:
        payload = _load_json(root / "profiles.json")
        if isinstance(payload, dict):
            raw_users = payload.get("users") or payload.get("profiles") or []
            if isinstance(raw_users, list):
                users = [entry for entry in raw_users if isinstance(entry, dict)]

    role_counter: Counter[str] = Counter()
    active_users = 0
    logins: List[str] = []

    for entry in users:
        login = str(entry.get("login") or entry.get("user") or "").strip()
        if not login:
            continue
        logins.append(login)
        role = _normalize_status(entry.get("rola") or entry.get("role"), "")
        if role:
            role_counter[role] += 1
        is_active = entry.get("active")
        if is_active in (None, "", True, 1, "1"):
            active_users += 1

    workload = Counter[str]()
    unassigned = 0
    for task in tasks:
        if not isinstance(task, dict):
            continue
        status = _normalize_status(task.get("status"))
        if status in _TASK_DONE_STATUSES:
            continue
        login = str(
            task.get("login")
            or task.get("owner")
            or task.get("assigned_to")
            or ""
        ).strip()
        if login:
            workload[login] += 1
        else:
            unassigned += 1

    return {
        "count": len(logins),
        "aktywni": active_users,
        "per_rola": dict(role_counter),
        "obciazenie": dict(workload),
        "zadania_bez_przypisania": unassigned,
    }


def _resolve_definitions_path_for_diag(
    cfg: ConfigManager | None,
    root: Path,
) -> Path | None:
    candidates: list[Path] = []

    candidate_raw: str | None = None
    if cfg is not None:
        try:
            value = cfg.get("tools.definitions_path", None)
        except Exception:
            value = None
        if isinstance(value, str) and value.strip():
            candidate_raw = value.strip()

    if candidate_raw:
        candidate_path = Path(candidate_raw)
        if not candidate_path.is_absolute():
            try:
                from config_manager import resolve_rel
            except Exception:
                resolve_rel = None  # type: ignore[assignment]
            if resolve_rel:
                try:
                    resolved = resolve_rel(cfg, candidate_raw)
                except Exception:
                    resolved = None
                if resolved:
                    candidate_path = Path(resolved)
                else:
                    candidate_path = (root / candidate_raw).resolve()
            else:
                candidate_path = (root / candidate_raw).resolve()
        candidates.append(candidate_path)

    candidates.extend(
        [
            root / "zadania_narzedzia.json",
            root / "narzedzia" / "szablony_zadan.json",
        ]
    )

    seen: set[Path] = set()
    ordered: list[Path] = []
    for candidate in candidates:
        if not isinstance(candidate, Path):
            continue
        try:
            resolved = candidate.resolve()
        except Exception:
            resolved = candidate
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(resolved)

    for candidate in ordered:
        if candidate.exists():
            return candidate
    return ordered[0] if ordered else None


def _definitions_counts(path: Path | None) -> tuple[int, int]:
    if path is None or not path.exists():
        return 0, 0
    data = _load_json(path)
    if not isinstance(data, Mapping):
        return 0, 0
    collections = data.get("collections")
    types_total = 0
    statuses_total = 0
    if isinstance(collections, Mapping):
        for entry in collections.values():
            if not isinstance(entry, Mapping):
                continue
            types = entry.get("types")
            if isinstance(types, list):
                for tool_type in types:
                    if not isinstance(tool_type, Mapping):
                        continue
                    types_total += 1
                    statuses = tool_type.get("statuses")
                    if isinstance(statuses, list):
                        statuses_total += sum(1 for status in statuses if isinstance(status, Mapping))
    if types_total == 0 and statuses_total == 0:
        if isinstance(data.get("types"), list):
            types_total = len(data["types"])
        if isinstance(data.get("statuses"), list):
            statuses_total = len(data["statuses"])
    return types_total, statuses_total


def _normalize_module_name(name: str) -> str:
    cleaned = name.strip()
    if "(" in cleaned:
        cleaned = cleaned.split("(", 1)[0].strip()
    return cleaned


def _iter_gui_log_candidates(root: Path) -> Iterable[Path]:
    seen: set[Path] = set()
    for candidate in (root / "logi_gui.txt", Path.cwd() / "logi_gui.txt"):
        try:
            resolved = candidate.resolve()
        except Exception:
            resolved = candidate
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            yield resolved


def _detect_slow_module_loads(root: Path) -> list[tuple[str, float]]:
    pending: dict[str, datetime] = {}
    slowest: dict[str, float] = {}

    for log_path in _iter_gui_log_candidates(root):
        try:
            with log_path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line or not line.startswith("["):
                        continue
                    try:
                        ts_str, payload = line.split("]", 1)
                        timestamp = datetime.fromisoformat(ts_str[1:])
                    except Exception:
                        continue
                    payload = payload.strip()
                    if payload.lower().startswith("kliknięto:") or payload.lower().startswith("kliknieto:"):
                        module = _normalize_module_name(payload.split(":", 1)[1])
                        pending[module] = timestamp
                    elif payload.lower().startswith("otworzono:"):
                        module = _normalize_module_name(payload.split(":", 1)[1])
                        start = pending.pop(module, None)
                        if start is None:
                            continue
                        delta = (timestamp - start).total_seconds()
                        if delta > 2.5:
                            previous = slowest.get(module, 0.0)
                            slowest[module] = max(previous, delta)
        except Exception:
            continue

    return sorted(slowest.items(), key=lambda item: item[1], reverse=True)


def _sanity_checks(stats: Mapping[str, Any], root: Path, alerts: list[JarvisAlert]) -> None:
    narzedzia = stats.get("narzedzia")
    if isinstance(narzedzia, Mapping):
        if int(narzedzia.get("count") or 0) == 0:
            tools_dir = root / "narzedzia"
            has_files = False
            if tools_dir.is_dir():
                for file in tools_dir.glob("*.json"):
                    if file.name in _TOOL_INDEX_FILES:
                        continue
                    has_files = True
                    break
            if not has_files:
                detail = str(tools_dir)
                _add_alert(alerts, "warning", "Brak plików narzędzi w katalogu danych.", detail)

    maszyny = stats.get("maszyny")
    if isinstance(maszyny, Mapping) and int(maszyny.get("count") or 0) == 0:
        machines_file = root / "maszyny" / "maszyny.json"
        if not machines_file.exists():
            _add_alert(alerts, "warning", "Brak pliku z definicją maszyn.", str(machines_file))

    zlecenia = stats.get("zlecenia")
    if isinstance(zlecenia, Mapping) and int(zlecenia.get("count") or 0) == 0:
        orders_dir = root / "zlecenia"
        orders_file = root / "zlecenia.json"
        if not orders_dir.is_dir() and not orders_file.exists():
            _add_alert(alerts, "warning", "Brak danych zleceń (nie znaleziono plików).", str(orders_dir))

    operatorzy = stats.get("operatorzy")
    if isinstance(operatorzy, Mapping) and int(operatorzy.get("count") or 0) == 0:
        profiles_file = root / "profiles.json"
        if not profiles_file.exists():
            _add_alert(alerts, "warning", "Brak pliku profiles.json z operatorami.", str(profiles_file))


def local_diagnostics(
    stats: Mapping[str, Any],
    cfg: ConfigManager | None,
    root: Path | None = None,
) -> list[JarvisAlert]:
    data_root = root or _data_root(cfg)
    alerts: list[JarvisAlert] = []

    if not data_root.exists():
        _add_alert(alerts, "alert", "Katalog danych warsztatu nie istnieje.", str(data_root))
        return alerts

    definitions_path = _resolve_definitions_path_for_diag(cfg, data_root)
    type_count, status_count = _definitions_counts(definitions_path)
    if definitions_path is None or not definitions_path.exists():
        detail = str(definitions_path) if definitions_path else "(brak ścieżki)"
        _add_alert(alerts, "alert", "Nie znaleziono pliku tools.definitions_path.", detail)
        notify(
            "alert",
            "Brak pliku definicji narzędzi (tools.definitions_path)",
            level=5,
        )
    elif type_count == 0 or status_count == 0:
        detail = f"{definitions_path} (typy={type_count}, statusy={status_count})"
        _add_alert(alerts, "alert", "Plik tools.definitions_path nie zawiera typów/statusów.", detail)

    for module, delay in _detect_slow_module_loads(data_root):
        message = f"Moduł \"{module}\" ładował się {delay * 1000:.1f} ms."
        _add_alert(alerts, "warning", message)

    _sanity_checks(stats, data_root, alerts)

    if alerts:
        for alert in alerts:
            notify("diagnostyka", alert.message, level=4)

    return alerts


def _autosave_report(root: Path, summary: str) -> Path | None:
    text = summary.strip()
    if not text:
        return None
    timestamp = datetime.now()
    report_dir = root / "reports" / "auto"
    try:
        report_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        return None
    filename = f"jarvis_{timestamp:%Y%m%d_%H%M%S}.txt"
    target = report_dir / filename
    try:
        content = f"[{timestamp:%Y-%m-%d %H:%M:%S}]\n{text}\n"
        target.write_text(content, encoding="utf-8")
    except Exception:
        return None
    return target


def collect_wm_stats() -> Dict[str, Any]:
    """Zbierz podstawowe statystyki wykorzystywane w promptach Jarvisa."""

    cfg = _config_manager()
    root = _data_root(cfg)

    tasks_data = _load_tasks_data(root)
    orders_data = _load_orders_data(root)
    task_metrics = _tasks_metrics(tasks_data)

    stats: Dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "narzedzia": _tools_summary(cfg, root),
        "maszyny": _machines_summary(cfg, root),
        "zlecenia": _orders_summary(orders_data, task_metrics),
        "operatorzy": _profiles_summary(cfg, root, tasks_data),
    }

    # Alias for older integrations still expecting the ``zadania`` key
    stats.setdefault("zadania", task_metrics)

    try:
        from services.profile_service import ProfileService

        active_user = ProfileService.ensure_active_user_or_none()
        if active_user:
            stats["uzytkownik"] = {"login": active_user}
    except Exception:
        pass

    return stats


def run_analysis_report(
    model: str | None = None,
    allow_ai: bool | None = None,
    question: str | None = None,
) -> JarvisReport:
    if summarize_wm_data is None:
        raise RuntimeError("Brak silnika promptów Jarvisa") from _PROMPT_ENGINE_IMPORT_ERROR

    cfg = _config_manager()
    stats = collect_wm_stats()
    data_root = _data_root(cfg)
    diagnostics = local_diagnostics(stats, cfg, data_root)

    target_model = model or _read_model(cfg)
    if allow_ai is None:
        allow_flag = _read_bool(cfg, "jarvis.allow_ai", True)
    else:
        allow_flag = bool(allow_ai)

    safe_stats = anonymize_for_ai(stats)
    metadata_raw = summarize_wm_data(
        safe_stats,
        model=target_model,
        allow_ai=allow_flag,
        question=question,
        return_metadata=True,
    )

    if isinstance(metadata_raw, Mapping):
        metadata: dict[str, Any] = dict(metadata_raw)
        summary_text = str(metadata.get("text") or "")
    else:
        summary_text = str(metadata_raw or "")
        metadata = {"text": summary_text, "model": target_model, "used_ai": False}

    metadata.setdefault("allow_ai", allow_flag)

    autosave_path = _autosave_report(data_root, summary_text)
    if autosave_path is not None:
        metadata["report_path"] = str(autosave_path)

    fallback_model = metadata.get("fallback_model") if metadata.get("used_ai") else None
    if fallback_model:
        fallback_reason = metadata.get("fallback_reason")
        detail = str(fallback_reason) if fallback_reason else None
        _add_alert(diagnostics, "info", f"Użyto modelu zapasowego: {fallback_model}", detail)

    offline_reason = metadata.get("offline_reason") or None
    offline = bool(offline_reason)

    return JarvisReport(
        summary=summary_text.strip(),
        stats=stats,
        alerts=diagnostics,
        metadata=metadata,
        offline=offline,
    )


def run_analysis_now(
    model: str | None = None,
    allow_ai: bool | None = None,
    question: str | None = None,
) -> str:
    """Uruchom analizę Jarvisa korzystając z bieżących danych warsztatu."""

    report = run_analysis_report(model=model, allow_ai=allow_ai, question=question)

    if report.alerts:
        for alert in report.alerts:
            notify("alert", alert.message, level=4)
    else:
        notify("status", "Analiza zakończona pomyślnie – brak problemów", level=1)

    metadata = report.metadata or {}
    allow_flag = bool(metadata.get("allow_ai", True))
    offline_reason = str(metadata.get("offline_reason") or "").strip()
    if report.offline or offline_reason or not allow_flag:
        notify("fallback", "Przełączono na tryb offline (brak dostępu do OpenAI)", level=3)

    return report.summary


def _read_interval(cfg: ConfigManager | None) -> int:
    if cfg is None:
        return 0
    try:
        value = cfg.get("jarvis.auto_interval_sec", 0)
    except Exception:
        return 0
    if isinstance(value, (int, float)):
        return max(0, int(value))
    try:
        parsed = int(str(value).strip())
    except Exception:
        return 0
    return max(0, parsed)


def _read_bool(cfg: ConfigManager | None, key: str, default: bool) -> bool:
    if cfg is None:
        return default
    try:
        value = cfg.get(key, default)
    except Exception:
        return default
    if isinstance(value, str):
        value = value.strip().lower()
        if value in {"1", "true", "yes", "tak"}:
            return True
        if value in {"0", "false", "no", "nie"}:
            return False
    return bool(value)


def _read_model(cfg: ConfigManager | None) -> str:
    model = DEFAULT_MODEL
    if cfg is None:
        return model
    try:
        candidate = cfg.get("jarvis.model", DEFAULT_MODEL)
    except Exception:
        return model
    if isinstance(candidate, str) and candidate.strip():
        return candidate
    return model


def _schedule_next(sec: int) -> None:
    if sec <= 0:
        return
    timer = threading.Timer(sec, _tick)
    timer.daemon = True
    with _JARVIS_TIMER_LOCK:
        global _JARVIS_TIMER
        _JARVIS_TIMER = timer
    timer.start()


def _tick() -> None:
    cfg = _config_manager()
    interval = _read_interval(cfg)

    if ConfigManager is None:
        if not _LAST_INFO["missing_config"]:
            wm_err(
                "core.jarvis_engine",
                "ConfigManager niedostępny – automatyczna analiza wyłączona.",
                exc=_CONFIG_MANAGER_IMPORT_ERROR,
            )
            _LAST_INFO["missing_config"] = True
        # >>> PATCH START: Jarvis – GUI notifications
        _update_status_flag(
            offline=True,
            reason="ConfigManager niedostępny – automatyczna analiza wyłączona.",
            source="tick",
        )
        # <<< PATCH END: Jarvis – GUI notifications
        return

    if summarize_wm_data is None:
        if not _LAST_INFO["missing_engine"]:
            wm_err(
                "core.jarvis_engine",
                "Brak silnika promptów Jarvisa – pomijam analizę.",
                exc=_PROMPT_ENGINE_IMPORT_ERROR,
            )
            _LAST_INFO["missing_engine"] = True
        if interval > 0:
            _schedule_next(interval)
        # >>> PATCH START: Jarvis – GUI notifications
        _update_status_flag(
            offline=True,
            reason="Brak silnika promptów Jarvisa – pomijam analizę.",
            source="tick",
        )
        # <<< PATCH END: Jarvis – GUI notifications
        return

    enabled = _read_bool(cfg, "jarvis.enabled", True)
    if not enabled:
        if not _LAST_INFO["disabled"]:
            wm_info("core.jarvis_engine", "Automatyczna analiza Jarvisa wyłączona w konfiguracji.")
            _LAST_INFO["disabled"] = True
        if interval > 0:
            _schedule_next(interval)
        # >>> PATCH START: Jarvis – GUI notifications
        _update_status_flag(
            offline=True,
            reason="Jarvis wyłączony w ustawieniach.",
            source="tick",
        )
        # <<< PATCH END: Jarvis – GUI notifications
        return

    _LAST_INFO["disabled"] = False
    _LAST_INFO["missing_engine"] = False
    _LAST_INFO["missing_config"] = False

    allow_ai = _read_bool(cfg, "jarvis.allow_ai", True)
    if not allow_ai:
        if not _LAST_INFO["ai_disabled"]:
            wm_info(
                "core.jarvis_engine",
                "Analiza Jarvisa w trybie offline – AI wyłączone w konfiguracji.",
            )
            _LAST_INFO["ai_disabled"] = True
    else:
        _LAST_INFO["ai_disabled"] = False

    try:
        report = run_analysis_report(model=_read_model(cfg), allow_ai=allow_ai)
        wm_info(
            "core.jarvis_engine",
            "Automatyczna analiza Jarvisa",
            summary=report.summary,
            model=report.metadata.get("model"),
            offline=report.offline,
        )
        # >>> PATCH START: Jarvis – GUI notifications
        offline_reason = str(report.metadata.get("offline_reason") or "").strip()
        _update_status_flag(
            offline=bool(report.offline or offline_reason),
            reason=offline_reason or None,
            source="tick",
        )
        # <<< PATCH END: Jarvis – GUI notifications
    except Exception as exc:  # pragma: no cover - zależne od API
        wm_err("core.jarvis_engine", "Błąd podczas automatycznej analizy Jarvisa.", exc=exc)
        # >>> PATCH START: Jarvis – GUI notifications
        _update_status_flag(
            offline=True,
            reason="Błąd podczas automatycznej analizy Jarvisa.",
            source="tick",
        )
        # <<< PATCH END: Jarvis – GUI notifications

    if interval > 0:
        _schedule_next(interval)


def run_jarvis_background() -> None:
    interval = _read_interval(_config_manager())

    if interval <= 0:
        return

    with _JARVIS_TIMER_LOCK:
        global _JARVIS_TIMER
        if _JARVIS_TIMER and _JARVIS_TIMER.is_alive():
            return

    _schedule_next(interval)


def stop_jarvis() -> None:
    with _JARVIS_TIMER_LOCK:
        global _JARVIS_TIMER
        if _JARVIS_TIMER is not None:
            try:
                _JARVIS_TIMER.cancel()
            except Exception:
                pass
            _JARVIS_TIMER = None


__all__ = [
    "JarvisAlert",
    "JarvisReport",
    "collect_wm_stats",
    "local_diagnostics",
    "run_analysis_report",
    "run_analysis_now",
    "run_jarvis_background",
    "stop_jarvis",
]

