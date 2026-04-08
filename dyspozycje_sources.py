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
    try:
        from start import CONFIG_MANAGER  # type: ignore

        if CONFIG_MANAGER is not None and hasattr(CONFIG_MANAGER, "load"):
            cfg = CONFIG_MANAGER.load() or {}
            if isinstance(cfg, dict):
                return cfg
    except Exception:
        pass
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


def _root_path(*parts: str) -> str:
    try:
        from start import CONFIG_MANAGER  # type: ignore

        if CONFIG_MANAGER is not None:
            path_root = getattr(CONFIG_MANAGER, "path_root", None)
            if callable(path_root):
                return path_root(*parts)
    except Exception:
        pass
    if ConfigManager is not None:
        try:
            return ConfigManager().path_root(*parts)
        except Exception:
            pass
    return os.path.join(os.getcwd(), *parts)


def _data_path(*parts: str) -> str:
    try:
        from start import CONFIG_MANAGER  # type: ignore

        if CONFIG_MANAGER is not None:
            path_data = getattr(CONFIG_MANAGER, "path_data", None)
            if callable(path_data):
                return path_data(*parts)
    except Exception:
        pass
    if ConfigManager is not None:
        try:
            return ConfigManager().path_data(*parts)
        except Exception:
            pass
    return os.path.join("data", *parts)


def _first_existing_path(*candidates: str | None) -> str | None:
    for candidate in candidates:
        if not candidate:
            continue
        try:
            if os.path.exists(candidate):
                return candidate
        except Exception:
            continue
    return None


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
        return _root_path("narzedzia", *extra)
    if key in {"warehouse", "warehouse_stock"}:
        return _root_path("magazyn", "magazyn.json")
    if key in {"orders", "orders_dir"}:
        return _root_path("zlecenia", *extra)
    return None


# =========================================================
# NARZĘDZIA
# =========================================================
def load_tool_choices() -> List[Tuple[str, str]]:
    tools_dir = _first_existing_path(
        _root_path("narzedzia"),
        _resolve_rel_path("tools.dir"),
        _resolve_rel_path("tools_item_dir"),
        _resolve_rel_path("tools_dir"),
        _data_path("narzedzia"),
    ) or _root_path("narzedzia")
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
    cfg = _cfg()
    machine_path = None

    if callable(get_machines_path):
        try:
            machine_path = get_machines_path(cfg)
        except Exception:
            machine_path = None

    path = _first_existing_path(
        _root_path("maszyny", "maszyny.json"),
        machine_path,
        _resolve_rel_path("machines"),
        _data_path("maszyny", "maszyny.json"),
    )
    if not path:
        return []

    try:
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
    out: List[Tuple[str, str]] = []
    seen: set[str] = set()

    candidates = [
        _resolve_rel_path("warehouse_stock"),
        _resolve_rel_path("warehouse"),
        _root_path("magazyn", "magazyn.json"),
        _root_path("magazyn", "katalog.json"),
        _data_path("magazyn", "katalog.json"),
    ]

    for path in [p for p in candidates if p]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        rows = []
        if isinstance(data, dict):
            if isinstance(data.get("items"), list):
                rows = data.get("items") or []
            elif isinstance(data.get("pozycje"), list):
                rows = data.get("pozycje") or []
            elif isinstance(data.get("magazyn"), list):
                rows = data.get("magazyn") or []
            else:
                for key, row in data.items():
                    if isinstance(row, dict):
                        code = str(
                            row.get("id")
                            or row.get("kod")
                            or row.get("nr")
                            or key
                        ).strip()
                        if not code or code.lower() in seen:
                            continue
                        seen.add(code.lower())
                        name = str(row.get("nazwa") or row.get("name") or "").strip()
                        label = f"{code} - {name}" if name else code
                        out.append((code, label))
                if out:
                    return out
                continue
        elif isinstance(data, list):
            rows = data

        for row in rows:
            if not isinstance(row, dict):
                continue
            code = str(
                row.get("id")
                or row.get("kod")
                or row.get("nr")
                or row.get("symbol")
                or ""
            ).strip()
            if not code or code.lower() in seen:
                continue
            seen.add(code.lower())
            name = str(
                row.get("nazwa")
                or row.get("name")
                or row.get("opis")
                or ""
            ).strip()
            label = f"{code} - {name}" if name else code
            out.append((code, label))

        if out:
            return out

    return out


# =========================================================
# ZLECENIE WYKONANIA
# =========================================================
def load_zlecenie_wykonania_choices() -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    seen: set[str] = set()

    candidates = [
        ("produkt", _root_path("produkty")),
        ("polprodukt", _root_path("polprodukty")),
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
    katalog_candidates = [
        _root_path("magazyn", "katalog.json"),
        _data_path("magazyn", "katalog.json"),
    ]
    katalog = {}
    try:
        for katalog_path in katalog_candidates:
            try:
                with open(katalog_path, "r", encoding="utf-8") as f:
                    katalog = json.load(f)
                if katalog:
                    break
            except Exception:
                continue
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
