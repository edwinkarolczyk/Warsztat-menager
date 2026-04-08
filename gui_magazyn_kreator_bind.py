# version: 1.0
from __future__ import annotations

from typing import Optional, Dict, Any, Callable
import tkinter as tk
from tkinter import ttk

try:
    from core.settings_manager import Settings as _Settings
except Exception:  # pragma: no cover - fallback dla środowisk testowych
    _Settings = None

from core.zlecenia_loader import (
    try_load_direct_creator,
    load_creator_from_settings,
    safe_open_creator,
    resolve_master,
)


def _find_treeview(container: tk.Misc) -> Optional[ttk.Treeview]:
    if not container or not container.winfo_exists():
        return None

    stack = [container]
    while stack:
        widget = stack.pop()
        if isinstance(widget, ttk.Treeview) and widget.winfo_exists():
            return widget
        try:
            stack.extend(list(widget.winfo_children()))
        except Exception:
            pass
    return None


def _prefill_from_selection(tree: Optional[ttk.Treeview]) -> Dict[str, Any]:
    if not tree:
        return {"item_id": "", "name": "", "qty": 1, "unit": "", "location": ""}

    selection = tree.selection()
    if not selection:
        return {"item_id": "", "name": "", "qty": 1, "unit": "", "location": ""}

    iid = selection[0]
    values = tree.item(iid, "values") or []
    return {
        "item_id": values[0] if len(values) > 0 else "",
        "name": values[1] if len(values) > 1 else "",
        "qty": values[2] if len(values) > 2 else 1,
        "unit": values[3] if len(values) > 3 else "",
        "location": values[4] if len(values) > 4 else "",
    }


def invoke_creator_from_magazyn(
    container: tk.Misc,
    *,
    get_user_role: Optional[Callable[[], str]] = None,
):
    """
    RĘCZNE, jednoznaczne wywołanie kreatora:
      1) Priorytet: DIRECT (gui_zlecenia_creator.open_order_creator(master, autor))
      2) Fallback: loader (obsługa order_type/prefill/user_role/**kwargs)
    """

    role = "brygadzista"
    try:
        if callable(get_user_role):
            role = get_user_role() or role
    except Exception:
        pass

    master = resolve_master(container)
    tree = _find_treeview(container)
    prefill: Dict[str, Any] = {"source": "magazyn"}
    try:
        prefill.update(_prefill_from_selection(tree))
    except Exception:
        pass

    direct = try_load_direct_creator()
    if callable(direct):
        try:
            return direct(master, autor=role or "brygadzista")
        except Exception as exc:
            print(f"[Mag→Kreator][DIRECT] Błąd: {exc}")

    cfg = None
    try:
        if _Settings:
            cfg = _Settings(path="config.json", project_root=__file__)
    except Exception:
        cfg = None

    opener = load_creator_from_settings(cfg) if cfg else None
    if callable(opener):
        return safe_open_creator(
            opener,
            master=master,
            order_type=None,
            prefill=prefill,
            user_role=role,
        )

    print(
        "[Mag→Kreator] NIE ZNALEZIONO kreatora (ani DIRECT, ani via settings). Sprawdź moduł/funkcję."
    )


def bind_kreator_button(
    btn: tk.Misc,
    tree: Optional[ttk.Treeview],
    *,
    get_user_role: Optional[Callable[[], str]] = None,
    get_cfg: Optional[Callable[[], Any]] = None,
):
    """Zachowaj zgodność wsteczną dla mechanizmu autobind."""

    if not btn or not btn.winfo_exists():
        return

    def _resolve_role() -> str:
        role = "brygadzista"
        if callable(get_user_role):
            try:
                role = get_user_role() or role
            except Exception:
                pass
        return role

    def _resolve_cfg():
        if callable(get_cfg):
            try:
                return get_cfg()
            except Exception:
                return None
        if _Settings:
            try:
                return _Settings(path="config.json", project_root=__file__)
            except Exception:
                return None
        return None

    def _handler(_evt=None):
        role = _resolve_role()
        master = resolve_master(btn)
        prefill: Dict[str, Any] = {"source": "magazyn"}
        try:
            prefill.update(_prefill_from_selection(tree))
        except Exception:
            pass

        direct = try_load_direct_creator()
        if callable(direct):
            try:
                return direct(master, autor=role or "brygadzista")
            except Exception as exc:
                print(f"[Mag→Kreator][DIRECT] Błąd: {exc}")

        cfg = _resolve_cfg()
        opener = load_creator_from_settings(cfg) if cfg else None
        if callable(opener):
            return safe_open_creator(
                opener,
                master=master,
                order_type=None,
                prefill=prefill,
                user_role=role,
            )

        print(
            "[Mag→Kreator] NIE ZNALEZIONO kreatora (ani DIRECT, ani via settings). Sprawdź moduł/funkcję."
        )

    try:
        btn.configure(command=_handler)
    except Exception:
        try:
            btn.bind("<Button-1>", _handler, add="+")
        except Exception:
            pass

