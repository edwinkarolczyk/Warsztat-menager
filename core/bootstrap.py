# version: 1.0
# WM-VERSION: 0.1
"""Helper utilities for preparing configuration paths without UI prompts."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Set

from config.paths import get_app_root, get_backup_dir, get_data_root, get_logs_dir
from core.path_utils import resolve_root_path


def _safe_get(cfg: Dict[str, Any], dotted_key: str, default: Any | None = None) -> Any:
    """Return value for ``dotted_key`` accepting flat and nested config forms."""

    if dotted_key in cfg:
        return cfg.get(dotted_key, default)

    parts = dotted_key.split(".")
    node: Any = cfg
    for part in parts:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return default
    return node


def _set_if_missing(cfg: Dict[str, Any], dotted_key: str, value: Any) -> None:
    """Populate ``dotted_key`` only when absent in both flat and nested forms."""

    if dotted_key in cfg:
        return

    parts = dotted_key.split(".")
    node = cfg
    for part in parts[:-1]:
        node = node.setdefault(part, {})  # type: ignore[assignment]
    node.setdefault(parts[-1], value)


def _ensure_or_default(
    cfg: Dict[str, Any],
    key: str,
    default_path: str,
    suppress_prompts: bool,
) -> None:
    """Ensure ``key`` points to an existing path or fallback to ``default_path``."""

    current = _safe_get(cfg, key, "")
    if current and Path(str(current)).exists():
        return

    if suppress_prompts:
        _set_if_missing(cfg, key, default_path)
        return

    # Legacy behaviour kept intentionally when prompts are allowed.


def _collect_directories(
    cfg: Dict[str, Any], candidates: Iterable[str], base_root: Path
) -> Set[Path]:
    """Return a normalized set of directories that should exist on disk."""

    directories: Set[Path] = set()
    for key in candidates:
        value = _safe_get(cfg, key)
        if not value:
            continue
        resolved = resolve_root_path(base_root, str(value))
        directories.add(Path(resolved).expanduser())
    return directories


def bootstrap_paths(
    cfg: Dict[str, Any], *, create_dirs: bool = True
) -> Dict[str, Any]:
    """Inject deterministic file paths when prompt suppression is enabled.

    When ``create_dirs`` is set to ``True`` (default) all directories derived
    from the configuration are created if they do not already exist. Passing
    ``create_dirs=False`` can be used by dry-run tooling to inspect the
    resulting paths without touching the filesystem.
    """

    suppress = bool(_safe_get(cfg, "system.suppress_json_prompts", False))

    project_root = Path(__file__).resolve().parents[1]
    anchor_raw = _safe_get(cfg, "paths.anchor_root")
    if anchor_raw:
        anchor_dir = Path(resolve_root_path(project_root, str(anchor_raw)))
    else:
        anchor_dir = project_root
    anchor_dir = anchor_dir.expanduser()

    data_root_raw = (
        _safe_get(cfg, "system.data_root") or _safe_get(cfg, "paths.data_root")
    )
    if data_root_raw:
        data_root_path = Path(resolve_root_path(anchor_dir, str(data_root_raw)))
    else:
        data_root_path = anchor_dir / "data"
    data_root_path = data_root_path.expanduser()
    _ensure_or_default(
        cfg,
        "hall.machines_file",
        str(data_root_path / "layout" / "maszyny.json"),
        suppress,
    )
    _ensure_or_default(
        cfg,
        "tools.types_file",
        str(data_root_path / "narzedzia" / "typy_narzedzi.json"),
        suppress,
    )
    _ensure_or_default(
        cfg,
        "tools.statuses_file",
        str(data_root_path / "narzedzia" / "statusy_narzedzi.json"),
        suppress,
    )
    _ensure_or_default(
        cfg,
        "tools.task_templates_file",
        str(data_root_path / "narzedzia" / "szablony_zadan.json"),
        suppress,
    )
    _ensure_or_default(
        cfg,
        "bom.file",
        str(data_root_path / "produkty" / "bom.json"),
        suppress,
    )
    _ensure_or_default(
        cfg,
        "warehouse.stock_source",
        str(data_root_path / "magazyn" / "magazyn.json"),
        suppress,
    )
    _ensure_or_default(
        cfg,
        "warehouse.reservations_file",
        str(data_root_path / "magazyn" / "rezerwacje.json"),
        suppress,
    )

    for dotted_key, relative in (
        ("paths.layout_dir", "layout"),
        ("paths.tools_dir", "narzedzia"),
        ("paths.products_dir", "produkty"),
        ("paths.warehouse_dir", "magazyn"),
        ("paths.orders_dir", "zlecenia"),
    ):
        target_dir = (data_root_path / relative).expanduser()
        _set_if_missing(cfg, dotted_key, str(target_dir))

    _set_if_missing(cfg, "paths.logs_dir", str((anchor_dir / "logs").expanduser()))
    _set_if_missing(cfg, "paths.backup_dir", str((anchor_dir / "backup").expanduser()))
    _set_if_missing(cfg, "sciezka_danych", str(data_root_path))

    directories = _collect_directories(
        cfg,
        (
            "paths.data_root",
            "paths.layout_dir",
            "paths.tools_dir",
            "paths.products_dir",
            "paths.warehouse_dir",
            "paths.orders_dir",
            "paths.logs_dir",
            "paths.backup_dir",
        ),
        anchor_dir,
    )
    directories.add(data_root_path)

    if create_dirs:
        for directory in sorted(directories):
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except OSError:
                # Directory creation failures are non-fatal – callers may not
                # have permissions or run in read-only environments.
                continue

    return cfg


def _load_config(path: Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


_DRIVE_PATTERN = re.compile(r"[\\/][A-Za-z]:[\\/]")


def check_paths_sanity(
    cfg: Dict[str, Any] | None = None,
    *,
    config_path: Path | None = None,
) -> int:
    """Wypisuje podstawowe ścieżki i ostrzega, gdy wyglądają podejrzanie."""

    suspicious = False

    app_root = get_app_root()
    if config_path is None:
        env_cfg = os.environ.get("WM_CONFIG_FILE")
        if env_cfg:
            config_path = Path(env_cfg).expanduser()
        else:
            config_path = app_root / "config.json"

    config_path = config_path.expanduser()
    if cfg is None:
        cfg = _load_config(config_path)

    data_root = Path(get_data_root(cfg)).expanduser()
    logs_dir = Path(get_logs_dir(cfg)).expanduser()
    backup_dir = Path(get_backup_dir(cfg)).expanduser()
    jarvis_path = (data_root / "jarvis" / "jarvis_notifications.json").expanduser()

    entries = (
        ("config", config_path),
        ("data", data_root),
        ("backup", backup_dir),
        ("logs", logs_dir),
        ("jarvis", jarvis_path),
    )

    for label, path_value in entries:
        as_text = str(path_value)
        normalized = as_text.replace("/", "\\")
        is_bad = "<root>" in as_text or bool(_DRIVE_PATTERN.search(normalized))
        status = "OK" if not is_bad else "WARN"
        print(f"[PATH-CHECK] {label:<6}: {as_text}  {status}")
        if is_bad:
            suspicious = True
            print(f"[PATH-CHECK][WARN] Podejrzana ścieżka: {as_text}")

    return 1 if suspicious else 0


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrapuj ścieżki danych WM.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.defaults.json"),
        help="Ścieżka do pliku konfiguracyjnego użytego do wyliczenia ścieżek.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Twórz katalogi na dysku (domyślnie tylko podgląd).",
    )
    parser.add_argument(
        "--check-paths",
        action="store_true",
        help="Wypisz sanity-check kluczowych ścieżek konfiguracji.",
    )
    args = parser.parse_args(argv)

    cfg = _load_config(args.config)
    cfg = bootstrap_paths(cfg, create_dirs=args.apply)

    project_root = Path(__file__).resolve().parents[1]
    anchor_raw = _safe_get(cfg, "paths.anchor_root")
    if anchor_raw:
        base_root = Path(resolve_root_path(project_root, str(anchor_raw))).expanduser()
    else:
        base_root = project_root.expanduser()

    directories = _collect_directories(
        cfg,
        (
            "paths.data_root",
            "paths.layout_dir",
            "paths.tools_dir",
            "paths.products_dir",
            "paths.warehouse_dir",
            "paths.orders_dir",
            "paths.logs_dir",
            "paths.backup_dir",
        ),
        base_root,
    )
    fallback_root = (
        _safe_get(cfg, "paths.data_root")
        or _safe_get(cfg, "system.data_root")
        or "data"
    )
    resolved_fallback = resolve_root_path(base_root, str(fallback_root))
    directories.add(Path(resolved_fallback).expanduser())

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] Sprawdzane katalogi ({len(directories)}):")
    for directory in sorted(directories):
        print(f" - {directory}")

    exit_code = 0
    if args.check_paths:
        exit_code = max(exit_code, check_paths_sanity(cfg, config_path=args.config))

    return exit_code


def main() -> None:
    sys.exit(_cli())


__all__ = [
    "bootstrap_paths",
    "check_paths_sanity",
    "main",
]


if __name__ == "__main__":
    main()

