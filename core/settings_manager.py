# version: 1.0
from __future__ import annotations

"""Settings management utilities."""

import json
import os
import threading
import time
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from core.path_utils import resolve_root_path


def _to_bool(value: Any, default: bool = False) -> bool:
    """Convert value to bool with fallback."""
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    string_value = str(value).strip().lower()
    if string_value in ("1", "true", "yes", "y", "on"):
        return True
    if string_value in ("0", "false", "no", "n", "off"):
        return False
    return default


def _to_int(value: Any, default: int = 0) -> int:
    """Convert value to int with fallback."""
    try:
        return int(value)
    except Exception:
        return default


def _to_str(value: Any, default: str = "") -> str:
    """Convert value to str with fallback."""
    return default if value is None else str(value)


@dataclass
class KeySpec:
    """Description of a single configuration key."""

    path: str
    typ: Callable[[Any], Any]
    default: Any
    description: str = ""
    choices: Optional[List[Any]] = None
    deprecated_aliases: List[str] = field(default_factory=list)


@dataclass
class SectionSpec:
    """Description of a configuration section."""

    name: str
    keys: List[KeySpec]
    group: str
    order: int = 100


GROUP_GUI = "GUI"
GROUP_PATHS = "Ścieżki"
GROUP_MAG = "Magazyn"
GROUP_MASZ = "Maszyny"
GROUP_SYS = "System"

SCHEMA: List[SectionSpec] = [
    SectionSpec(
        "gui",
        group=GROUP_GUI,
        order=10,
        keys=[
            KeySpec(
                "gui.theme",
                _to_str,
                "dark",
                "Motyw",
                ["dark", "light"],
                ["ustawienia.theme"],
            ),
            KeySpec(
                "gui.language",
                _to_str,
                "pl",
                "Język",
                ["pl", "en"],
                ["ustawienia.jezyk"],
            ),
            KeySpec(
                "gui.wrap_windows",
                _to_bool,
                True,
                "Zawijanie dużych okien",
            ),
            KeySpec(
                "gui.main.remember_geometry",
                _to_bool,
                True,
                "Zapamiętuj geometrię okna",
            ),
            KeySpec(
                "gui.main.geometry",
                _to_str,
                "",
                "Ostatnia geometria okna (WxH+X+Y)",
            ),
            KeySpec(
                "gui.main.maximized",
                _to_bool,
                False,
                "Czy okno było zmaksymalizowane",
            ),
            KeySpec(
                "gui.main.active_tab",
                _to_str,
                "Maszyny",
                "Ostatnio aktywna karta",
            ),
            KeySpec(
                "gui.maszyny.show_grid",
                _to_bool,
                True,
                "Siatka (ON/OFF)",
            ),
            KeySpec(
                "gui.maszyny.scale_mode",
                _to_str,
                "fit",
                "Skala: fit|100",
                ["fit", "100"],
            ),
        ],
    ),
    SectionSpec(
        "paths",
        group=GROUP_PATHS,
        order=20,
        keys=[
            KeySpec(
                "paths.data_dir",
                _to_str,
                "data",
                "Katalog danych",
                None,
                ["paths.datadir", "dane.sciezka"],
            ),
            KeySpec(
                "paths.backup_dir",
                _to_str,
                "backup",
                "Katalog kopii",
            ),
            KeySpec(
                "paths.assets_dir",
                _to_str,
                "assets",
                "Katalog zasobów",
            ),
        ],
    ),
    SectionSpec(
        "maszyny",
        group=GROUP_MASZ,
        order=30,
        keys=[
            KeySpec("maszyny.canvas.min_x", _to_int, 0, "Min X"),
            KeySpec("maszyny.canvas.min_y", _to_int, 0, "Min Y"),
            KeySpec("maszyny.icons.cache", _to_bool, True, "Cache ikon"),
        ],
    ),
    SectionSpec(
        "system",
        group=GROUP_SYS,
        order=5,
        keys=[
            KeySpec(
                "system.require_reauth",
                _to_bool,
                True,
                "Wymagaj ponownego logowania",
            ),
            KeySpec(
                "system.logs_dir",
                _to_str,
                "logs",
                "Katalog logów",
                None,
                ["logi.sciezka"],
            ),
        ],
    ),
]

GLOBAL_ALIASES = {
    "theme": "gui.theme",
    "language": "gui.language",
    "data_dir": "paths.data_dir",
    "backup_dir": "paths.backup_dir",
}


class Settings:
    """Settings container with schema-driven defaults and migrations."""

    def __init__(self, path: str = "config.json", project_root: Optional[str] = None):
        self._file_path = os.path.abspath(path)
        self.path_config = self._file_path
        self._config_dir = os.path.dirname(self._file_path)
        self._explicit_project_root = (
            self._normalize_root_path(project_root)
            if project_root is not None
            else None
        )
        self.project_root = self._explicit_project_root or self._config_dir
        self._data: Dict[str, Any] = {}
        self._defaults = self._build_defaults()
        self._observers: List[Callable[[], None]] = []
        self._save_lock = threading.Lock()
        self._last_save = 0.0
        self._save_delay = 3.0
        self.reload()

    def get(self, key: str, default: Any = None) -> Any:
        """Return value by key path."""
        return self._get_by_path(self._data, key.split("."), default)

    def set(self, key: str, value: Any) -> None:
        """Set value by key path."""
        self._set_by_path(self._data, key.split("."), value)

    def save(self) -> bool:
        """Persist current settings to disk using atomic replace."""
        target_path = Path(self.path_config)
        tmp_path = target_path.with_suffix(target_path.suffix + ".tmp")
        backup_path = target_path.with_suffix(target_path.suffix + ".bak")
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            text = json.dumps(self._data, ensure_ascii=False, indent=2)
            with tmp_path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
                handle.flush()
                try:
                    os.fsync(handle.fileno())
                except OSError:
                    pass
            if target_path.exists():
                try:
                    backup_path.write_text(
                        target_path.read_text(encoding="utf-8"), encoding="utf-8"
                    )
                except Exception:
                    pass
            tmp_path.replace(target_path)
        except Exception as error:  # pragma: no cover - logging only
            print("[Settings] Save error:", error)
            try:
                if tmp_path.exists():
                    tmp_path.unlink()
            except Exception:
                pass
            return False
        self.notify_observers()
        return True

    def save_throttled(self) -> bool:
        """Persist settings if sufficient time elapsed since last save."""
        self._update_save_delay()
        now = time.time()
        with self._save_lock:
            if (now - self._last_save) < self._save_delay:
                return False
            self._last_save = now
        return self.save()

    def add_observer(self, callback: Callable[[], None]) -> None:
        """Register a callback invoked after a successful save."""
        if callback and callback not in self._observers:
            self._observers.append(callback)

    def remove_observer(self, callback: Callable[[], None]) -> None:
        """Unregister a previously registered callback."""
        try:
            self._observers.remove(callback)
        except ValueError:
            pass

    def notify_observers(self) -> None:
        """Notify registered observers about a save event."""
        errors: List[Exception] = []
        for observer in list(self._observers):
            try:
                observer()
            except Exception as exc:  # pragma: no cover - diagnostics only
                errors.append(exc)
        if errors:
            print("[WM][SETTINGS] observer errors:", errors)

    def reload(self) -> None:
        """Reload settings from disk and apply schema transformations."""
        loaded: Dict[str, Any] = {}
        if os.path.exists(self.path_config):
            try:
                with open(self.path_config, "r", encoding="utf-8") as file:
                    loaded = json.load(file)
            except Exception:
                loaded = {}
        self._data = self._merge(self._defaults, loaded or {})
        self._migrate_aliases_inplace(self._data)
        self._coerce_types_inplace(self._data)
        if not isinstance(self._data.get("paths"), dict):
            self._data["paths"] = {}
        self._update_project_root()
        self._update_save_delay()

    def load_defaults(self, defaults_path: Optional[str] = None) -> Dict[str, Any]:
        """Load defaults from disk or fall back to schema defaults."""
        if defaults_path is None:
            defaults_path = os.path.join(self.project_root, "config.defaults.json")
        path = Path(defaults_path)
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return deepcopy(self._defaults)

    def reset_to_defaults(self, defaults_path: Optional[str] = None) -> None:
        """Replace current configuration with defaults and persist."""
        defaults = self.load_defaults(defaults_path)
        if isinstance(defaults, dict):
            merged = self._merge(deepcopy(self._defaults), defaults)
        else:
            merged = deepcopy(self._defaults)
        self._data = merged
        self._update_save_delay()
        self.save()

    # UI helpers
    def ui_groups(self) -> List[Tuple[str, List[KeySpec]]]:
        """Return grouped key specifications for building UI."""
        groups: Dict[str, List[KeySpec]] = {}
        for section in sorted(SCHEMA, key=lambda spec: spec.order):
            groups.setdefault(section.group, []).extend(section.keys)
        return list(groups.items())

    # Path helpers
    def path_data(self, *parts: str) -> str:
        """Return path inside project data directory."""
        base_dir = self._resolve_under_root(self.get("paths.data_dir", "data"))
        return os.path.join(base_dir, *parts) if parts else base_dir

    def path_backup(self, *parts: str) -> str:
        """Return backup path resolved against repository root."""
        configured = self.get("paths.backup_dir")
        if not configured:
            configured = "backup"
        base_dir = self._resolve_under_root(configured)
        return os.path.join(base_dir, *parts) if parts else base_dir

    def path_assets(self, *parts: str) -> str:
        """Return assets path resolved against repository root."""
        assets_dir = self.get("paths.assets_dir", "assets")
        base_dir = self._resolve_under_root(assets_dir)
        return os.path.join(base_dir, *parts) if parts else base_dir

    def print_root_info(self) -> None:
        """Print diagnostics related to the resolved project root."""
        print("[WM ROOT DIAGNOSTICS]")
        print(f"  project_root : {self.project_root}")
        print(f"  path_config  : {self.path_config}")
        print(f"  path_data()  : {self.path_data()}")
        print(f"  path_backup(): {self.path_backup()}")
        print(f"  path_assets(): {self.path_assets()}")

    # Internals
    def _build_defaults(self) -> Dict[str, Any]:
        defaults: Dict[str, Any] = {}
        for section in SCHEMA:
            for key_spec in section.keys:
                self._set_by_path(defaults, key_spec.path.split("."), key_spec.default)
        return defaults

    def _merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key in set(base) | set(override):
            base_value = base.get(key)
            override_value = override.get(key)
            if isinstance(base_value, dict) and isinstance(override_value, dict):
                result[key] = self._merge(base_value, override_value)
            elif key in override:
                result[key] = override_value
            else:
                result[key] = base_value
        return result

    def _migrate_aliases_inplace(self, data: Dict[str, Any]) -> None:
        for alias, target in GLOBAL_ALIASES.items():
            self._migrate_one(data, alias, target)
        lookup = {key_spec.path: key_spec for section in SCHEMA for key_spec in section.keys}
        for spec in lookup.values():
            for alias in spec.deprecated_aliases:
                self._migrate_one(data, alias, spec.path)

    def _migrate_one(self, data: Dict[str, Any], alias: str, target: str) -> None:
        value, parent = self._get_with_parent(data, alias.split("."))
        if parent is None:
            return
        current = self.get(target, None)
        default = self._get_by_path(self._defaults, target.split("."))
        if value is not None and (current is None or current == default):
            self.set(target, value)
        self._delete_by_path(data, alias.split("."))

    def _coerce_types_inplace(self, data: Dict[str, Any]) -> None:
        spec_lookup = {key_spec.path: key_spec for section in SCHEMA for key_spec in section.keys}

        def walk(base: str, node: Any) -> None:
            if isinstance(node, dict):
                for key, value in list(node.items()):
                    walk(f"{base}.{key}" if base else key, value)
            else:
                key_spec = spec_lookup.get(base)
                if key_spec:
                    self.set(base, key_spec.typ(node))

        walk("", data)

    def _update_project_root(self) -> None:
        root_from_config = None
        paths_section = self._data.get("paths", {})
        if isinstance(paths_section, dict):
            for key in ("root", "anchor_root"):
                candidate = paths_section.get(key)
                if isinstance(candidate, str) and candidate.strip():
                    root_from_config = candidate.strip()
                    break
            if root_from_config is None:
                data_candidate = paths_section.get("data_dir") or paths_section.get(
                    "data_root"
                )
                if isinstance(data_candidate, str) and data_candidate.strip():
                    candidate = data_candidate.strip()
                    for placeholder in ("<root>", "<ROOT>"):
                        if placeholder in candidate:
                            candidate = candidate.replace(placeholder, self.project_root)
                    candidate_path = self._normalize_root_path(candidate)
                    if os.path.basename(candidate_path).lower() == "data":
                        candidate_path = os.path.dirname(candidate_path)
                    root_from_config = candidate_path
        if self._explicit_project_root is not None:
            self.project_root = self._explicit_project_root
        elif root_from_config:
            self.project_root = self._normalize_root_path(root_from_config)
        else:
            self.project_root = self._config_dir

    def _resolve_under_root(self, relative_path: str) -> str:
        """Resolve ``relative_path`` against the configured project root.

        The configuration historically stores placeholder literals such as
        ``"<root>\\backup"`` (Windows style) that are expected to be
        replaced with the actual project root at runtime.  The original
        implementation simply joined the value with ``project_root`` which
        resulted in paths like ``"/repo/<root>\\backup"``.  Aside from being
        incorrect, such paths also break when passed to filesystem APIs on
        Windows due to the invalid ``<`` character.  We normalise the path by
        expanding placeholders and handling user/UNC prefixes before falling
        back to a standard ``os.path.join``.
        """

        if not relative_path:
            return os.path.normpath(self.project_root)

        return resolve_root_path(self.project_root, relative_path)

    @staticmethod
    def _normalize_root_path(candidate: str) -> str:
        abs_candidate = os.path.abspath(candidate)
        if os.path.isfile(abs_candidate):
            return os.path.dirname(abs_candidate)
        return abs_candidate

    def _update_save_delay(self) -> None:
        try:
            delay = float(self.get("ui.autosave_delay_sec", self._save_delay))
        except (TypeError, ValueError):
            delay = 3.0
        if delay <= 0:
            delay = 0.0
        self._save_delay = delay

    @staticmethod
    def _get_by_path(root: Dict[str, Any], parts: List[str], default: Any = None) -> Any:
        current: Any = root
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]
        return current

    @staticmethod
    def _set_by_path(root: Dict[str, Any], parts: List[str], value: Any) -> None:
        current = root
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    @staticmethod
    def _delete_by_path(root: Dict[str, Any], parts: List[str]) -> None:
        current = root
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                return
            current = current[part]
        current.pop(parts[-1], None)

    @staticmethod
    def _get_with_parent(
        root: Dict[str, Any], parts: List[str]
    ) -> Tuple[Any, Optional[Dict[str, Any]]]:
        current = root
        for part in parts[:-1]:
            if not isinstance(current, dict) or part not in current:
                return None, None
            current = current[part]
        if not isinstance(current, dict):
            return None, None
        return current.get(parts[-1], None), current
