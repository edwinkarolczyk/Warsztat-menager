# version: 1.0
"""Warstwa pośrednia dla narzędzi w stabilnej gałęzi WM.

Moduł zapewnia niezależny od GUI punkt dostępu do ``ToolDataBridge``.
Implementacja bazuje na logice z panelu narzędzi V2, ale nie wymaga
ładowania modułu beta GUI.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

try:  # pragma: no cover - moduł może nie być dostępny w środowisku testowym
    from config_manager import ConfigManager, resolve_rel as cfg_resolve_rel
except ImportError as exc:  # pragma: no cover - fallback, gdy ConfigManager niedostępny
    logging.getLogger(__name__).debug(
        "[WM-DBG][narzedzia] pomijam opcjonalny moduł config_manager (ImportError: %s)",
        exc,
    )
    ConfigManager = None  # type: ignore

    def cfg_resolve_rel(_cfg: dict, _what: str, *extra: str):  # type: ignore
        return ""

from tools_config_loader import get_status_names_for_type, get_types, load_config
from utils_json import safe_read_json
from utils_paths import tools_dir
from utils_tools import ensure_tools_sample_if_empty, load_tools_rows_with_fallback

LOGGER = logging.getLogger(__name__)


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "tak"}
    return bool(value)


class ToolDataBridge:
    """Warstwa pośrednia pomiędzy logiką WM a danymi narzędzi."""

    def __init__(self, cfg_manager: Optional[ConfigManager] = None):  # type: ignore[assignment]
        self._cfg_manager = cfg_manager or self._try_init_cfg_manager()
        self._cfg = self._load_cfg()
        self._index_rows: Optional[List[Dict[str, Any]]] = None
        self._index_path: Optional[str] = None
        self._definitions: Optional[Dict[str, Any]] = None
        self._detail_catalog: Optional[set[str]] = None
        self._detail_catalog_path_override: Optional[str] = None

    # --- konfiguracja i indeks ---
    def _try_init_cfg_manager(self) -> Optional[ConfigManager]:  # type: ignore[return-value]
        if ConfigManager is None:  # type: ignore[comparison-overlap]
            return None
        try:
            return ConfigManager()
        except Exception:  # pragma: no cover - środowiska testowe
            LOGGER.debug("[ToolDataBridge] Brak ConfigManager – fallback", exc_info=True)
            return None

    def _load_cfg(self) -> Dict[str, Any]:
        if self._cfg_manager is None:
            return {}
        try:
            return self._cfg_manager.load()
        except Exception:  # pragma: no cover - konfiguracja opcjonalna
            LOGGER.warning("[ToolDataBridge] Nie udało się wczytać konfiguracji WM", exc_info=True)
            return {}

    def _ensure_index_cache(self) -> None:
        if self._index_rows is not None:
            return
        rows, primary = load_tools_rows_with_fallback(self._cfg, cfg_resolve_rel)
        rows = ensure_tools_sample_if_empty(rows, primary)
        self._index_rows = [dict(row) for row in rows if isinstance(row, dict)]
        self._index_path = primary

    def reload_index(self) -> None:
        """Reload tool index from JSON files."""
        self._index_rows = None
        self._ensure_index_cache()

    def normalize_nr(self, value: Any) -> str:
        nr = str(value or "").strip()
        if nr.isdigit() and len(nr) <= 3:
            return nr.zfill(3)
        return nr

    # --- źródła danych ---
    def available_tools(self, *, exclude: Optional[str] = None) -> List[Dict[str, Any]]:
        self._ensure_index_cache()
        items: List[Dict[str, Any]] = []
        excluded = self.normalize_nr(exclude) if exclude else ""
        for row in self._index_rows or []:
            nr = self.normalize_nr(row.get("nr") or row.get("numer") or row.get("id"))
            if not nr or (excluded and nr == excluded):
                continue
            items.append(
                {
                    "nr": nr,
                    "nazwa": str(row.get("nazwa", "")),
                    "narzedzie_etapowe": _coerce_bool(row.get("narzedzie_etapowe") or row.get("is_stage_tool")),
                }
            )
        items.sort(key=lambda item: item["nr"])
        return items

    def list_index_rows(self) -> List[Dict[str, Any]]:
        self._ensure_index_cache()
        return list(self._index_rows or [])

    def _load_definitions(self) -> Dict[str, Any]:
        if self._definitions is not None:
            return self._definitions
        path = None
        if self._cfg_manager is not None:
            try:
                path = str(self._cfg_manager.path_data("zadania_narzedzia.json"))
            except Exception:
                path = None
        try:
            self._definitions = load_config(path)
        except Exception:  # pragma: no cover - fallback
            LOGGER.warning("[ToolDataBridge] Nie udało się wczytać definicji narzędzi", exc_info=True)
            self._definitions = {}
        return self._definitions or {}

    def _detail_catalog_path(self) -> Optional[str]:
        if self._detail_catalog_path_override:
            return self._detail_catalog_path_override
        if self._cfg_manager is None:
            return None
        try:
            return str(self._cfg_manager.path_data("katalog_detal.json"))
        except Exception:
            return None

    def _load_detail_catalog(self) -> set[str]:
        if self._detail_catalog is not None:
            return self._detail_catalog
        path = self._detail_catalog_path()
        if not path or not os.path.exists(path):
            self._detail_catalog = set()
            return self._detail_catalog
        try:
            data = safe_read_json(path, default=[], ensure=False)
        except Exception:
            data = []
        ids: set[str] = set()
        if isinstance(data, list):
            for entry in data:
                if isinstance(entry, dict):
                    identifier = str(
                        entry.get("id") or entry.get("nr") or entry.get("numer") or ""
                    ).strip()
                    if identifier:
                        ids.add(identifier)
                elif isinstance(entry, str):
                    cleaned = entry.strip()
                    if cleaned:
                        ids.add(cleaned)
        elif isinstance(data, dict):
            for key in ("items", "detale", "details"):
                items = data.get(key)
                if isinstance(items, list):
                    for entry in items:
                        if isinstance(entry, dict):
                            identifier = str(
                                entry.get("id")
                                or entry.get("nr")
                                or entry.get("numer")
                                or ""
                            ).strip()
                            if identifier:
                                ids.add(identifier)
                        elif isinstance(entry, str):
                            cleaned = entry.strip()
                            if cleaned:
                                ids.add(cleaned)
        self._detail_catalog = ids
        return self._detail_catalog

    def _status_sequence(self, tool_type: Optional[str]) -> List[str]:
        definitions = self._load_definitions()
        ordered: List[str] = []
        if tool_type:
            for collection in ("NN", "SN"):
                sequence = get_status_names_for_type(definitions, collection, tool_type)
                if sequence:
                    ordered = [str(item).strip() for item in sequence if str(item).strip()]
                    break
        if not ordered:
            ordered = ["projekt", "przyjęte", "testy", "aktywny", "wycofany"]
        return ordered

    def terminal_statuses(self, tool_type: Optional[str] = None) -> set[str]:
        ordered = self._status_sequence(tool_type)
        if not ordered:
            return set()
        return {ordered[-1]}

    def _transition_map(self, tool_type: Optional[str]) -> Dict[str, set[str]]:
        definitions = self._load_definitions()
        custom = definitions.get("transitions") if isinstance(definitions, dict) else None
        mapping: Dict[str, set[str]] = {}
        if isinstance(custom, dict):
            for src, targets in custom.items():
                if not isinstance(targets, (list, tuple)):
                    continue
                src_clean = str(src).strip()
                if not src_clean:
                    continue
                mapping[src_clean] = {str(t).strip() for t in targets if str(t).strip()}
        if mapping:
            return mapping

        # FIX(STATUS): brak własnej mapy przejść nie może wymuszać sekwencji 1->2->3.
        # Użytkownik ma móc przejść z dowolnego statusu do dowolnego innego statusu
        # zdefiniowanego dla danego typu narzędzia.
        ordered = self._status_sequence(tool_type)
        allowed_all = {str(status).strip() for status in ordered if str(status).strip()}
        for status in ordered:
            current = str(status).strip()
            if not current:
                continue
            mapping[current] = set(allowed_all)
        return mapping

    def is_transition_allowed(self, current: str, target: str, tool_type: Optional[str]) -> bool:
        src = (current or "").strip()
        dst = (target or "").strip()
        if not src or not dst:
            return True
        mapping = self._transition_map(tool_type)
        if src not in mapping:
            return True
        return dst in mapping.get(src, {dst})

    def validate_detail_binding(self, detail_id: str) -> None:
        detail = (detail_id or "").strip()
        if not detail:
            return
        catalog = self._load_detail_catalog()
        if catalog and detail not in catalog:
            raise ValueError("Powiązany detal nie istnieje w katalogu detali.")

    # --- ścieżki ---
    def tools_dir(self) -> str:
        base = tools_dir(self._cfg)
        os.makedirs(base, exist_ok=True)
        return base

    # --- dostępne typy/statusy ---
    def available_types(self) -> List[str]:
        self._ensure_index_cache()
        names = {str(row.get("typ", "")).strip() for row in self._index_rows or [] if row.get("typ")}
        definitions = self._load_definitions()
        for collection in ("NN", "SN"):
            for tool_type in get_types(definitions, collection):
                name = str(tool_type.get("name", "")).strip()
                if name:
                    names.add(name)
        cleaned = [name for name in sorted(names) if name]
        if not cleaned:
            cleaned = ["Tłoczące", "Obróbcze", "Pomocnicze"]
        return cleaned

    def available_statuses(self, tool_type: Optional[str] = None) -> List[str]:
        self._ensure_index_cache()
        statuses: set[str] = set()
        definitions = self._load_definitions()
        if tool_type:
            for collection in ("NN", "SN"):
                for name in get_status_names_for_type(definitions, collection, tool_type):
                    if name:
                        statuses.add(str(name))
        if not statuses:
            for row in self._index_rows or []:
                value = str(row.get("status", "")).strip()
                if value:
                    statuses.add(value)
        if not statuses:
            statuses.update({"projekt", "przyjęte", "testy", "aktywny", "wycofany"})
        return sorted(statuses)


__all__ = ["ToolDataBridge"]
