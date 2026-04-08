# version: 1.0
"""Compatibility helpers for legacy path references.

This module exposes the same helpers as :mod:`core.settings_manager`
while additionally monitoring accesses to the historical backup
directory (``C:\\wm\\data\\backup``).  Once a legacy path is detected we
emit a stack trace to ease migration.
"""

from __future__ import annotations

import os
import traceback

from core.settings_manager import Settings

_cfg = Settings(path="config.json", project_root=__file__)

ROOT_DIR = _cfg.path_root()
DATA_DIR = _cfg.path_data()
ASSETS_DIR = _cfg.path_assets()
BACKUP_DIR = _cfg.path_backup()


# --- 1️⃣ HOOK legacy ścieżki -----------------------------------------------
LEGACY_BACKUP = r"C:\\wm\\data\\backup"
_warned = False


def _legacy_trace(msg: str) -> None:
    tb = "".join(traceback.format_stack(limit=8))
    print(f"[LEGACY-PATH] {msg}\n{tb}\n{'-' * 70}")


def _check_legacy(path: str) -> None:
    global _warned
    if not _warned and path.lower().startswith(LEGACY_BACKUP.lower()):
        _warned = True
        _legacy_trace(f"ODWOŁANIE DO LEGACY BACKUP: {path}")


# --- 2️⃣ Funkcje zgodne wstecz ---------------------------------------------
def path_root(*parts: str) -> str:
    """Return the project root path."""

    return _cfg.path_root(*parts)


def path_data(*parts: str) -> str:
    """Return the data directory path."""

    return _cfg.path_data(*parts)


def path_assets(*parts: str) -> str:
    """Return the assets directory path."""

    return _cfg.path_assets(*parts)


def path_backup(*parts: str) -> str:
    """Return the backup directory and warn on legacy references."""

    base = _cfg.path_backup()
    if parts:
        joined = os.path.join(base, *parts)
        _check_legacy(joined)
        return joined
    _check_legacy(base)
    return base


# --- 3️⃣ Stałe (dla kompatybilności) ---------------------------------------
# jeśli ktoś ma w kodzie "from core.paths_compat import BACKUP_DIR" itd.
_check_legacy(BACKUP_DIR)
