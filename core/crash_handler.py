# version: 1.0
"""Global crash handler and helpers for WM."""

from __future__ import annotations

import datetime as _dt
import json
import os
import platform
import sys
import traceback
from pathlib import Path
from typing import Tuple

from core.path_utils import get_app_root, resolve_root_path

_CRASH_LOG_NAME = "wm_crash.log"
_CRASH_STATE_NAME = "wm_crash_state.json"
_PREVIOUS_HOOK = None
_HANDLER_INSTALLED = False


def _load_config_manager():
    try:
        from config_manager import ConfigManager  # type: ignore

        return ConfigManager()
    except Exception:
        return None


def _get_crash_log_dir() -> Path:
    manager = _load_config_manager()
    if manager is not None:
        try:
            logs_dir = manager.path_logs()
            if logs_dir:
                return Path(logs_dir)
        except Exception:
            pass
        try:
            data_root = manager.path_data()
            if data_root:
                resolved = resolve_root_path(data_root, "logs")
                if resolved:
                    return Path(resolved)
        except Exception:
            pass
    app_root = get_app_root()
    return app_root / "logs"


def _get_crash_log_path() -> Path:
    return _get_crash_log_dir() / _CRASH_LOG_NAME


def _get_state_path() -> Path:
    return _get_crash_log_dir() / _CRASH_STATE_NAME


def get_crash_log_path() -> Path:
    """Public helper returning the crash log path."""

    return _get_crash_log_path()


def _get_wm_version() -> str:
    try:
        from __version__ import get_version  # type: ignore

        return get_version()
    except Exception:
        return "unknown"


def _count_log_entries(log_path: Path) -> int:
    try:
        if not log_path.exists():
            return 0
        count = 0
        with log_path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if line.startswith("["):
                    count += 1
        return count
    except Exception:
        return 0


def _read_state_count() -> int:
    path = _get_state_path()
    try:
        if not path.exists():
            return 0
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return int(data.get("last_read_count", 0))
    except Exception:
        return 0


def _write_state_count(count: int) -> None:
    path = _get_state_path()
    payload = {
        "last_read_count": max(int(count), 0),
        "updated_at": _dt.datetime.utcnow().isoformat(timespec="seconds"),
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get_crash_log_stats() -> Tuple[int, int]:
    """Return (total_entries, unread_entries)."""

    log_path = _get_crash_log_path()
    total = _count_log_entries(log_path)
    read_count = _read_state_count()
    unread = max(total - read_count, 0)
    return total, unread


def mark_crash_log_read(total_count: int | None = None) -> None:
    """Mark crash log entries as read."""

    if total_count is None:
        log_path = _get_crash_log_path()
        total_count = _count_log_entries(log_path)
    try:
        _write_state_count(total_count or 0)
    except Exception:
        pass


def clear_crash_log() -> None:
    """Remove crash log file and reset the read counter."""

    log_path = _get_crash_log_path()
    try:
        if log_path.exists():
            log_path.unlink()
    except Exception:
        pass
    try:
        _write_state_count(0)
    except Exception:
        pass


def _write_crash(exc_type, exc_value, exc_traceback) -> Path:
    log_path = _get_crash_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    ts = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    wm_version = _get_wm_version()
    frozen_mode = bool(getattr(sys, "frozen", False))
    info_lines = [
        f"WM version: {wm_version}",
        f"Python: {platform.python_version()} ({sys.executable})",
        f"Platform: {platform.platform()}",
        f"Frozen: {frozen_mode}",
        f"Working dir: {os.getcwd()}",
    ]

    try:
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"[{ts}] {exc_type.__name__}: {exc_value}\n")
            for line in info_lines:
                handle.write(line + "\n")
            handle.write(tb_text)
            handle.write("\n" + "-" * 80 + "\n")
    except Exception:
        pass

    return log_path


def _show_crash_dialog(log_path: Path) -> None:
    try:
        import tkinter as tk
        from tkinter import messagebox
    except Exception:
        return

    try:
        root = getattr(tk, "_default_root", None)
        owns_root = False
        if root is None:
            root = tk.Tk()
            root.withdraw()
            owns_root = True
        messagebox.showerror(
            "Warsztat-Menager – błąd krytyczny",
            (
                "Wystąpił nieoczekiwany błąd.\n\n"
                f"Szczegóły zapisano w pliku:\n{log_path}\n\n"
                "Zgłoś ten raport osobie odpowiedzialnej za WM."
            ),
        )
        if owns_root:
            root.destroy()
    except Exception:
        pass


def _global_excepthook(exc_type, exc_value, exc_traceback):
    if exc_type is KeyboardInterrupt:
        previous = _PREVIOUS_HOOK or sys.__excepthook__
        try:
            previous(exc_type, exc_value, exc_traceback)
        except Exception:
            pass
        return

    try:
        log_path = _write_crash(exc_type, exc_value, exc_traceback)
        _show_crash_dialog(log_path)
    except Exception:
        pass
    finally:
        previous = _PREVIOUS_HOOK or sys.__excepthook__
        try:
            previous(exc_type, exc_value, exc_traceback)
        except Exception:
            pass


def init_crash_handler() -> None:
    """Install the global crash handler if not already active."""

    global _PREVIOUS_HOOK, _HANDLER_INSTALLED
    if _HANDLER_INSTALLED:
        return
    _PREVIOUS_HOOK = getattr(sys, "excepthook", sys.__excepthook__)
    sys.excepthook = _global_excepthook
    _HANDLER_INSTALLED = True

