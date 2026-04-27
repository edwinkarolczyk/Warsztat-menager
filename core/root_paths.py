# version: 1.0
"""Centralny resolver ROOT dla Warsztat Menager.

APP_ROOT = folder programu / repozytorium / Git
WM_ROOT  = folder danych wybrany przez użytkownika
DATA_ROOT = WM_ROOT / "data"

Ten moduł nie dotyka mechanizmu aktualizacji Git.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT_FILE_NAME = "wm_root.json"
DEFAULT_ROOT_NAME = "wm"


def _norm(path: Path | str) -> Path:
    p = path if isinstance(path, Path) else Path(str(path))
    try:
        return p.expanduser().resolve()
    except Exception:
        return p.expanduser()


def get_app_root() -> Path:
    """Zwraca folder programu/repozytorium, a nie folder danych."""

    if getattr(sys, "frozen", False):
        return _norm(Path(sys.executable).parent)
    return _norm(Path(__file__).resolve().parents[1])


def root_file_path(app_root: Path | None = None) -> Path:
    return _norm((app_root or get_app_root()) / ROOT_FILE_NAME)


def _read_root_file(path: Path) -> Path | None:
    try:
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict):
            raw = str(payload.get("root") or "").strip()
        else:
            raw = ""
        if not raw:
            return None
        return _norm(Path(raw))
    except Exception as exc:
        print(f"[WM-ROOT][WARN] Nie można odczytać {path}: {exc}")
        return None


def _write_root_file(path: Path, wm_root: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump({"root": str(wm_root)}, handle, ensure_ascii=False, indent=2)


def _default_wm_root() -> Path:
    drive = Path.cwd().anchor or "C:\\"
    try:
        return _norm(Path(drive) / DEFAULT_ROOT_NAME)
    except Exception:
        return _norm(get_app_root() / DEFAULT_ROOT_NAME)


def _ask_root_folder(initial: Path) -> Path | None:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except Exception:
        return None

    try:
        root = tk.Tk()
        root.withdraw()
        try:
            messagebox.showinfo(
                "Folder danych WM",
                "Wskaż jeden główny folder danych Warsztat Menager.\n\n"
                "Przykład:\n"
                "C:\\wm\n\n"
                "Nie wybieraj folderu programu ani samego folderu data.",
                parent=root,
            )
        except Exception:
            pass
        selected = filedialog.askdirectory(
            parent=root,
            initialdir=str(initial),
            title="Wskaż główny folder danych WM",
        )
        root.destroy()
    except Exception as exc:
        print(f"[WM-ROOT][WARN] Nie udało się pokazać wyboru ROOT: {exc}")
        return None

    if not selected:
        return None
    return _norm(Path(selected))


def resolve_wm_root(*, prompt: bool = False) -> Path:
    """Ustal WM_ROOT z ENV, wm_root.json albo wyboru użytkownika."""

    app_root = get_app_root()

    env_root = os.environ.get("WM_ROOT") or os.environ.get("WM_APP_ROOT")
    if env_root:
        wm_root = _norm(Path(env_root))
        return wm_root

    pointer = root_file_path(app_root)
    from_file = _read_root_file(pointer)
    if from_file is not None:
        return from_file

    initial = _default_wm_root()
    selected = _ask_root_folder(initial) if prompt else None
    wm_root = selected or initial
    try:
        _write_root_file(pointer, wm_root)
        print(f"[WM-ROOT][BOOT] Zapisano ROOT_FILE: {pointer}")
    except Exception as exc:
        print(f"[WM-ROOT][WARN] Nie można zapisać ROOT_FILE {pointer}: {exc}")
    return wm_root


def get_root_anchor() -> Path:
    return resolve_wm_root(prompt=False)


def get_data_root() -> Path:
    return get_root_anchor() / "data"


def path_config() -> Path:
    return get_root_anchor() / "config.json"


def path_logs() -> Path:
    return get_root_anchor() / "logs"


def path_backup() -> Path:
    return get_root_anchor() / "backup"


def path_assets() -> Path:
    return get_root_anchor() / "assets"


def path_profiles() -> Path:
    return get_data_root() / "profiles.json"


def path_tools_dir() -> Path:
    return get_data_root() / "narzedzia"


def path_machines() -> Path:
    return get_data_root() / "maszyny" / "maszyny.json"


def path_warehouse() -> Path:
    return get_data_root() / "magazyn" / "magazyn.json"


def path_bom() -> Path:
    return get_data_root() / "produkty" / "bom.json"


def path_orders_dir() -> Path:
    return get_data_root() / "zlecenia"


def path_dyspozycje() -> Path:
    return get_data_root() / "dyspozycje" / "dyspozycje.json"


def ensure_root_tree() -> None:
    """Tworzy strukturę katalogów wyłącznie pod WM_ROOT."""

    dirs = [
        get_root_anchor(),
        get_data_root(),
        path_logs(),
        path_backup(),
        path_assets(),
        get_data_root() / "user",
        path_tools_dir(),
        get_data_root() / "maszyny",
        get_data_root() / "magazyn",
        get_data_root() / "produkty",
        get_data_root() / "polprodukty",
        path_orders_dir(),
        get_data_root() / "dyspozycje",
        get_data_root() / "layout",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def install_environment(*, prompt: bool = False) -> dict[str, str]:
    """Ustawia ENV dla reszty aplikacji i zwraca snapshot ścieżek."""

    wm_root = resolve_wm_root(prompt=prompt)
    data_root = wm_root / "data"

    os.environ["WM_ROOT"] = str(wm_root)
    os.environ["WM_APP_ROOT"] = str(wm_root)
    os.environ["WM_DATA_ROOT"] = str(data_root)
    os.environ["WM_CONFIG_FILE"] = str(wm_root / "config.json")

    ensure_root_tree()

    return {
        "app_root": str(get_app_root()),
        "root_file": str(root_file_path()),
        "wm_root": str(wm_root),
        "config": str(path_config()),
        "data_root": str(data_root),
        "profiles": str(path_profiles()),
        "tools_dir": str(path_tools_dir()),
        "machines": str(path_machines()),
        "warehouse": str(path_warehouse()),
        "bom": str(path_bom()),
        "orders_dir": str(path_orders_dir()),
        "dyspozycje": str(path_dyspozycje()),
        "logs_dir": str(path_logs()),
        "backup_dir": str(path_backup()),
    }


def print_root_diagnostics(snapshot: dict[str, Any] | None = None) -> None:
    snap = snapshot or install_environment(prompt=False)
    print("[WM-ROOT][BOOT] =====================================")
    print(f"[WM-ROOT][BOOT] APP_ROOT    = {snap.get('app_root')}")
    print(f"[WM-ROOT][BOOT] ROOT_FILE   = {snap.get('root_file')}")
    print(f"[WM-ROOT][BOOT] WM_ROOT     = {snap.get('wm_root')}")
    print(f"[WM-ROOT][BOOT] CONFIG      = {snap.get('config')}")
    print(f"[WM-ROOT][BOOT] DATA_ROOT   = {snap.get('data_root')}")
    print(f"[WM-ROOT][BOOT] PROFILES    = {snap.get('profiles')}")
    print(f"[WM-ROOT][BOOT] TOOLS_DIR   = {snap.get('tools_dir')}")
    print(f"[WM-ROOT][BOOT] MACHINES    = {snap.get('machines')}")
    print(f"[WM-ROOT][BOOT] WAREHOUSE   = {snap.get('warehouse')}")
    print(f"[WM-ROOT][BOOT] BOM         = {snap.get('bom')}")
    print(f"[WM-ROOT][BOOT] ORDERS_DIR  = {snap.get('orders_dir')}")
    print(f"[WM-ROOT][BOOT] DYSP_FILE   = {snap.get('dyspozycje')}")
    print(f"[WM-ROOT][BOOT] LOGS_DIR    = {snap.get('logs_dir')}")
    print(f"[WM-ROOT][BOOT] BACKUP_DIR  = {snap.get('backup_dir')}")
    print("[WM-ROOT][BOOT] =====================================")

    app_data = get_app_root() / "data"
    try:
        if app_data.exists() and _norm(app_data) != _norm(get_data_root()):
            print(f"[WM-ROOT][WARN] Wykryto lokalny folder data przy programie: {app_data}")
            print(f"[WM-ROOT][WARN] Aktywny DATA_ROOT: {get_data_root()}")
            print("[WM-ROOT][WARN] Lokalny folder data nie powinien być używany.")
    except Exception:
        pass
