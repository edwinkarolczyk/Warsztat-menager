# version: 1.0
"""Prosta warstwa logiki dla operacji na maszynach.
Czyta dane z pliku JSON i pozwala wyciągnąć kolejne zadania."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from config_manager import get_machines_path
from io_utils import read_json, write_json
from logger import log_akcja
from utils_paths import resolve_rel as resolve_root_path


def _resolve_data_file() -> Path:
    """Locate the canonical machines JSON file with graceful fallbacks."""

    logger = logging.getLogger(__name__)
    try:
        candidate = Path(get_machines_path())
        if candidate.exists():
            logger.debug("[WM-DBG][MASZYNY] SoT=%s", candidate.as_posix())
            return candidate
    except Exception as exc:  # pragma: no cover - diagnostics only
        logger.debug("[WM-DBG][MASZYNY] get_machines_path error: %r", exc)

    fallback = Path(
        resolve_root_path("<root>", "data", "maszyny", "maszyny.json")
    )
    logger.debug(
        "[WM-DBG][MASZYNY] fallback SoT=%s (repo default)", fallback.as_posix()
    )
    return fallback


DATA_FILE: Path = _resolve_data_file()


def load_machines() -> List[Dict[str, Any]]:
    """Wczytuje listę maszyn z pliku JSON z walidacją kluczy."""
    data = read_json(str(DATA_FILE)) or []
    if not isinstance(data, list):
        log_akcja("[MASZYNY] Nieprawidłowy format danych maszyn")
        return []

    valid: List[Dict[str, Any]] = []
    for m in data:
        if not isinstance(m, dict):
            log_akcja("[MASZYNY] Pominięto rekord – nie jest dict")
            continue
        missing = [k for k in ("hala", "x", "y", "status") if k not in m]
        if missing:
            log_akcja(
                f"[MASZYNY] Maszyna {m.get('nr_ewid')} brak pól {missing}"
            )
            continue
        if not isinstance(m["x"], (int, float)) or not isinstance(
            m["y"], (int, float)
        ):
            log_akcja(
                f"[MASZYNY] Maszyna {m.get('nr_ewid')} ma nieprawidłowe współrzędne"
            )
            continue
        valid.append(m)
    return valid


def _save_machines(data: List[Dict[str, Any]]) -> bool:
    """Zapisuje listę maszyn do pliku JSON."""
    valid: List[Dict[str, Any]] = []
    for m in data:
        if not isinstance(m, dict):
            log_akcja("[MASZYNY] Nieprawidłowy rekord przy zapisie")
            continue
        missing = [k for k in ("hala", "x", "y", "status") if k not in m]
        if missing:
            log_akcja(
                f"[MASZYNY] Maszyna {m.get('nr_ewid')} brak pól {missing}"
            )
            continue
        valid.append(m)
    return write_json(str(DATA_FILE), valid)


def next_task(machine: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Zwraca najbliższe zadanie dla maszyny (najwcześniejsza data).
    Jeżeli brak zadań, zwraca None.
    """
    tasks = machine.get("zadania") or []
    if not tasks:
        return None
    return sorted(tasks, key=lambda z: z.get("data"))[0]


def machines_with_next_task() -> List[Dict[str, Any]]:
    """Zwraca listę maszyn z informacją o najbliższym zadaniu."""
    machines = load_machines()
    wynik = []
    for m in machines:
        m2 = dict(m)
        m2["next_task"] = next_task(m)
        wynik.append(m2)
    return wynik
