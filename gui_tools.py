# version: 1.0
"""Helpery I/O dla modułu narzędzi (NN/SN)."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Any, Iterable

from config_manager import get_root, resolve_rel
from utils_json import ensure_json

logger = logging.getLogger(__name__)
try:
    from tkinter import messagebox
except ImportError:  # pragma: no cover - środowiska bez GUI
    messagebox = None


def _load_allowed_from_file(base: str, filename: str, key: str | None = None) -> list[str]:
    path = os.path.join(base, filename)
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except Exception:
        return []
    values: Iterable[str] = []
    if isinstance(payload, dict):
        if key and isinstance(payload.get(key), (list, tuple)):
            values = payload.get(key, [])  # type: ignore[assignment]
        elif not key:
            values = []
    if not values and isinstance(payload, dict):
        # typy_narzedzi.json używa klucza "types"
        if isinstance(payload.get("types"), (list, tuple)):
            values = payload.get("types", [])  # type: ignore[assignment]
        else:
            values = [
                item
                for value in payload.values()
                if isinstance(value, (list, tuple))
                for item in value
            ]
    if not values and isinstance(payload, list):
        values = payload
    return [str(item).strip() for item in values if str(item).strip()]


def _validate_tool_payload(
    data: dict, base_dir: str, nr: int, *, previous_status: str | None = None
) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "Brak danych narzędzia (oczekiwano słownika)."

    identifier = str(
        data.get("id") or data.get("nr") or data.get("numer") or f"{nr:03d}"
    ).strip()
    if not identifier:
        return False, "Pole ID/nr narzędzia jest wymagane."

    name = str(data.get("nazwa") or data.get("name") or "").strip()
    if not name:
        return False, "Pole nazwa jest wymagane."

    tool_type = str(data.get("typ") or data.get("type") or "").strip()
    allowed_types = _load_allowed_from_file(base_dir, "typy_narzedzi.json", key="types")
    if not tool_type:
        return False, "Pole typ jest wymagane."
    if allowed_types and tool_type not in allowed_types:
        return False, "Nieznany typ narzędzia."

    status = data.get("status")
    if status is not None:
        status_text = str(status).strip()
        if not status_text:
            return False, "Pole status nie może być puste."
        allowed_statuses = _load_allowed_from_file(base_dir, "statusy_narzedzi.json")
        if allowed_statuses and status_text not in allowed_statuses:
            return False, "Status spoza listy dozwolonych."
        if previous_status and previous_status in allowed_statuses:
            idx = allowed_statuses.index(previous_status)
            allowed_targets = {allowed_statuses[idx]}
            if idx > 0:
                allowed_targets.add(allowed_statuses[idx - 1])
            if idx < len(allowed_statuses) - 1:
                allowed_targets.add(allowed_statuses[idx + 1])
            if status_text not in allowed_targets:
                return False, "Nieprawidłowa zmiana statusu (tylko kroki sąsiednie)."
    else:
        status_text = None

    for key, value in data.items():
        if any(marker in key.lower() for marker in ("date", "data", "ts")):
            if isinstance(value, datetime):
                return False, f"Pole {key} powinno być tekstem daty, nie datetime."
            if value not in (None, "") and not isinstance(value, str):
                return False, f"Pole {key} powinno być zapisane jako tekst."

    data.setdefault("id", identifier)
    if status_text is not None:
        data["status"] = status_text

    return True, ""


def _load_cfg(cfg_manager: Any) -> dict:
    """Bezpiecznie wczytaj konfigurację z ``cfg_manager``."""

    cfg: dict[str, Any] | None = None
    if cfg_manager is None:
        return {}
    try:
        if hasattr(cfg_manager, "load") and callable(getattr(cfg_manager, "load")):
            cfg = cfg_manager.load()
        elif hasattr(cfg_manager, "merged"):
            cfg = getattr(cfg_manager, "merged", None)
    except Exception:
        cfg = None
    return cfg if isinstance(cfg, dict) else {}


def _tools_dir_abs(cfg: dict) -> str:
    """Zwraca absolutną ścieżkę do katalogu ``<root>/narzedzia``."""

    abs_dir = resolve_rel(cfg, "tools.dir")
    if not abs_dir:
        abs_dir = os.path.join(get_root(cfg) or "", "narzedzia")
    os.makedirs(abs_dir, exist_ok=True)
    return abs_dir


def save_tool_entry(cfg_manager: Any, nr: int, data: dict) -> bool:
    """Zapisz definicję narzędzia ``nr`` pod ``<root>/narzedzia``."""

    cfg = _load_cfg(cfg_manager)
    base = _tools_dir_abs(cfg)
    path = os.path.join(base, f"{nr:03d}.json")
    previous_status = None
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                existing = json.load(handle)
            prev = str(existing.get("status", "")).strip()
            previous_status = prev or None
        except Exception:  # pragma: no cover - walidacja ignoruje błędy odczytu
            previous_status = None

    is_valid, reason = _validate_tool_payload(
        data, base, nr, previous_status=previous_status
    )
    if not is_valid:
        logger.error(
            "[WM-ERR][narzedzia] walidacja zapisu narzędzia nieudana: %s", reason
        )
        if messagebox is not None:
            messagebox.showerror(
                "Błąd danych narzędzia",
                "Błąd danych narzędzia – sprawdź wymagane pola (ID, nazwa, typ, status).",
            )
        return False
    ensure_json(path, default=data if data else {})
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
        logger.info("[TOOLS] Zapisano %s", path)
        return True
    except Exception as exc:  # pragma: no cover - log + False
        logger.exception("[TOOLS] Błąd zapisu %s: %s", path, exc)
        return False


__all__ = ["save_tool_entry"]
