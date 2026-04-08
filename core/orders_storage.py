# version: 1.0
"""Utilities for loading and saving orders list."""

from __future__ import annotations

import json
import os
import pathlib
import tempfile
import time
from typing import Any, Dict, List

from utils_paths import resolve_rel


def _project_root() -> pathlib.Path:
    """Return repository root (two levels above this file)."""

    return pathlib.Path(__file__).resolve().parent.parent


def orders_file_path(cfg: Any | None = None) -> pathlib.Path:
    """Return path to the orders JSON file.

    Priority order:
    1. ``config['orders.file']`` (absolute or relative to repo root)
    2. ``<root>/data/zlecenia/zlecenia.json``
    """

    root = _project_root()
    try:
        if cfg:
            raw_path = (cfg.get("orders.file") or "").strip()
            if raw_path:
                path = pathlib.Path(raw_path)
                if not path.is_absolute():
                    path = root / path
                return path
    except Exception:
        pass
    return pathlib.Path(
        resolve_rel("<root>", "data", "zlecenia", "zlecenia.json")
    )


def _ensure_parent(path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_orders(path: pathlib.Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            return []
        data = json.loads(text)
        return data if isinstance(data, list) else []
    except Exception:
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_name = f"zlecenia_corrupt_{timestamp}.json"
            path.rename(path.with_name(backup_name))
        except Exception:
            pass
        return []


def _atomic_write(path: pathlib.Path, data: Any) -> None:
    _ensure_parent(path)
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        prefix="zlecenia_", suffix=".json", dir=str(path.parent)
    )
    os.close(tmp_fd)
    tmp_path = pathlib.Path(tmp_path_str)
    try:
        tmp_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        os.replace(str(tmp_path), str(path))
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass


def save_orders(path: pathlib.Path, items: List[Dict[str, Any]]) -> None:
    _atomic_write(path, items)
