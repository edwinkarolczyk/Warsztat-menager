# version: 1.0
"""Źródła danych dla Dyspozycji (bez GUI)."""

from __future__ import annotations

import json
import os
from typing import List, Tuple

try:
    from config_manager import ConfigManager, get_config, get_machines_path, resolve_rel
except Exception:  # pragma: no cover
    ConfigManager = None  # type: ignore
    get_config = None  # type: ignore
    get_machines_path = None  # type: ignore
    resolve_rel = None  # type: ignore


def _cfg() -> dict:
    if callable(get_config):
        try:
            cfg = get_config() or {}
            if isinstance(cfg, dict):
                return cfg
        except Exception:
            pass
    if ConfigManager is not None:
        try:
            cfg = ConfigManager().load() or {}
            if isinstance(cfg, dict):
                return cfg
        except Exception:
            pass
    return {}


def _data_path(*parts: str) -> str:
    if ConfigManager is not None:
        try:
            return ConfigManager().path_data(*parts)
        except Exception:
            pass
    return os.path.join("data", *parts)


def _resolve_rel_path(key: str, *extra: str) -> str | None:
    cfg = _cfg()
    if callable(resolve_rel):
        try:
            path = resolve_rel(cfg, key, *extra)
            if path:
                return path
        except Exception:
            pass
    if key in {"tools", "tools.dir", "tools_dir"}:
        return _data_path("narzedzia", *extra)
    if key in {"warehouse", "warehouse_stock"}:
        return _data_path("magazyn", "magazyn.json")
    return None


# =========================================================
# NARZĘDZIA
# =========================================================
def load_tool_choices() -> List[Tuple[str, str]]:
    tools_dir = (
        _resolve_rel_path("tools.dir")
        or _resolve_rel_path("tools_dir")
        or _data_path("narzedzia")
    )
    out = []

    try:
        for filename in sorted(os.listdir(tools_dir)):
            if not filename.endswith(".json"):
                continue

            path = os.path.join(tools_dir, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = json.load(f)
            except Exception:
                continue

            file_stem = os.path.splitext(filename)[0].strip()
            tool_id = str(doc.get("id") or file_stem).strip()
            name = str(doc.get("nazwa") or "").strip()

            if not tool_id:
                continue

            label = f"{tool_id} - {name}" if name else tool_id
            out.append((tool_id, label))

    except Exception:
        return []

    return out


# =========================================================
# MASZYNY
# =========================================================
def load_machine_choices() -> List[Tuple[str, str]]:
    if not callable(get_machines_path):
        return []

    try:
        cfg = _cfg()
        path = get_machines_path(cfg)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []

    rows = data.get("maszyny", []) if isinstance(data, dict) else data

    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue

        mid = str(row.get("id") or row.get("nr_ewid") or "").strip()
        name = str(row.get("nazwa") or "").strip()

        if not mid:
            continue

        label = f"{mid} - {name}" if name else mid
        out.append((mid, label))

    return out


# =========================================================
# MAGAZYN
# =========================================================
def load_magazyn_choices() -> List[Tuple[str, str]]:
    path = _data_path("magazyn", "katalog.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []

    out = []

    if isinstance(data, dict):
        for key, row in data.items():
            code = str(key).strip()
            name = ""
            if isinstance(row, dict):
                name = str(row.get("nazwa") or "").strip()

            label = f"{code} - {name}" if name else code
            out.append((code, label))

    return out


# =========================================================
# ZLECENIE WYKONANIA
# =========================================================
def load_zlecenie_wykonania_choices() -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    seen: set[str] = set()

    candidates = [
        ("produkt", _data_path("produkty")),
        ("polprodukt", _data_path("polprodukty")),
    ]

    for prefix, folder in candidates:
        try:
            names = sorted(os.listdir(folder))
        except Exception:
            names = []
        for filename in names:
            if not filename.endswith(".json"):
                continue
            code = os.path.splitext(filename)[0].strip()
            if not code:
                continue
            key = f"{prefix}:{code}".lower()
            if key in seen:
                continue
            seen.add(key)
            label = f"{prefix.upper()} - {code}"
            out.append((f"{prefix}:{code}", label))

    # katalog magazynowy jako "elementy / pozycje magazynowe"
    try:
        with open(_data_path("magazyn", "katalog.json"), "r", encoding="utf-8") as f:
            katalog = json.load(f)
    except Exception:
        katalog = {}

    if isinstance(katalog, dict):
        for key, row in katalog.items():
            code = str(key or "").strip()
            if not code:
                continue
            uniq = f"element:{code}".lower()
            if uniq in seen:
                continue
            seen.add(uniq)
            name = ""
            if isinstance(row, dict):
                name = str(row.get("nazwa") or "").strip()
            label = f"ELEMENT - {code}" + (f" - {name}" if name else "")
            out.append((f"element:{code}", label))

    return out
