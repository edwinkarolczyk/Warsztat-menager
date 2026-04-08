# version: 1.0
from __future__ import annotations

import glob
import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List

from config.paths import p_tools_defs


DEFAULT_CONFIG: Dict[str, Any] = {
    "collections": {"NN": {"types": []}, "SN": {"types": []}}
}


def _candidate_paths(definitions_path: str | None = None) -> List[str]:
    """Return ordered list of candidate paths for the tools definitions file."""

    candidates: List[str] = []

    def _add(path: str | None) -> None:
        if not path:
            return
        norm = os.path.normpath(path)
        if norm not in candidates:
            candidates.append(norm)

    _add(definitions_path)

    cfg_mgr = None
    try:
        from config_manager import ConfigManager

        cfg_mgr = ConfigManager()
    except Exception:
        cfg_mgr = None

    if cfg_mgr is not None:
        try:
            _add(str(p_tools_defs(cfg_mgr)))
        except Exception:
            pass

    if not candidates:
        _add(str(Path("zadania_narzedzia.json").resolve()))
    return candidates


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _write_atomic(path: str, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f"{target.name}.tmp_{int(time.time() * 1000)}")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    os.replace(tmp, target)


def _sanitize_json(text: str) -> str:
    text = text.lstrip("\ufeff")
    text = re.sub(r"//[^\n\r]*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    text = re.sub(r"([\[{]\s*),", r"\1", text)
    return text


def _try_load(text: str) -> Dict[str, Any]:
    return json.loads(text) if text.strip() else {}


def _normalize_payload(data: Any) -> Dict[str, Any] | None:
    if isinstance(data, dict):
        return data
    print(
        "[WARNING] Nieprawidłowy format definicji zadań narzędzi "
        f"(oczekiwano obiektu, otrzymano {type(data).__name__})."
    )
    return None


def _restore_latest_backup(path: str) -> Dict[str, Any] | None:
    pattern = f"{path}.bak.*.json"
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    for candidate in files:
        try:
            data = _try_load(_read_text(candidate))
            candidate_name = os.path.basename(candidate)
            print(
                "[WARNING] Przywrócono definicje z backupu: "
                f"{candidate_name}"
            )
            _write_atomic(path, json.dumps(data, ensure_ascii=False, indent=2))
            return data
        except Exception:
            continue
    return None


def load_config(definitions_path: str | None = None) -> Dict[str, Any]:
    candidates = _candidate_paths(definitions_path)
    if not candidates and definitions_path:
        candidates.append(definitions_path)
    path = candidates[0] if candidates else ""
    for candidate in candidates:
        if os.path.exists(candidate):
            path = candidate
            break
    resolved = os.path.abspath(path) if path else path
    print(f"[WM-DBG][TOOLS] definicje z pliku: {resolved}")
    if not path or not os.path.exists(path):
        print(f"[WARNING] Brak pliku definicji – ścieżka: {resolved}")
        return DEFAULT_CONFIG
    try:
        payload = _normalize_payload(_try_load(_read_text(path)))
        return payload if payload is not None else DEFAULT_CONFIG
    except Exception:
        try:
            raw = _read_text(path)
            fixed = _sanitize_json(raw)
            data = _normalize_payload(_try_load(fixed))
            path_name = os.path.basename(path)
            if data is None:
                return DEFAULT_CONFIG
            print(
                "[WARNING] Auto-heal definicji: "
                f"{path_name} (naprawiono format JSON)."
            )
            corrupt = f"{path}.corrupt.{int(time.time())}.json"
            try:
                shutil.copy2(path, corrupt)
            except Exception:
                pass
            _write_atomic(path, json.dumps(data, ensure_ascii=False, indent=2))
            return data
        except Exception as exc:
            print("[ERROR] Nie można wczytać definicji (strict ani sanitize):", exc)
            backup = _restore_latest_backup(path)
            if isinstance(backup, dict):
                return backup
            return DEFAULT_CONFIG


def _normalize_type_key(value: str) -> str:
    """Return normalized key for comparing tool type identifiers."""

    return re.sub(r"[^a-z0-9]", "", str(value or "").strip().lower())


def get_types(cfg: Dict[str, Any], collection: str) -> List[Dict[str, Any]]:
    try:
        types = cfg["collections"][collection]["types"]
    except (KeyError, TypeError):
        return []
    return list(types or [])


def find_type(cfg: Dict[str, Any], collection: str, type_name: str) -> Dict[str, Any] | None:
    target = _normalize_type_key(type_name)
    for tool_type in get_types(cfg, collection):
        name_norm = _normalize_type_key(tool_type.get("name") or "")
        id_norm = _normalize_type_key(tool_type.get("id") or "")
        id_base_norm = _normalize_type_key(str(tool_type.get("id") or "").rstrip("0123456789"))
        aliases = tool_type.get("aliases") or []
        alias_norm = {_normalize_type_key(alias) for alias in aliases if isinstance(alias, str)}

        if target in {name_norm, id_norm, id_base_norm} | alias_norm:
            return tool_type
    return None


def get_status_names_for_type(cfg: Dict[str, Any], collection: str, type_name: str) -> List[str]:
    tool_type = find_type(cfg, collection, type_name)
    if not tool_type:
        return []
    statuses = tool_type.get("statuses") or []
    result = []
    for status in statuses:
        if isinstance(status, dict):
            value = status.get("name") or status.get("id") or str(status)
        else:
            value = str(status)
        value = value.strip()
        if value:
            result.append(value)
    return result


def get_tasks_for_status(
    cfg: Dict[str, Any],
    collection: str,
    type_name: str,
    status_name: str,
) -> List[str]:
    tool_type = find_type(cfg, collection, type_name)
    if not tool_type:
        return []
    target = (status_name or "").strip().lower()
    for status in tool_type.get("statuses") or []:
        if (status.get("name") or "").strip().lower() == target:
            return [str(task) for task in (status.get("tasks") or [])]
    return []
