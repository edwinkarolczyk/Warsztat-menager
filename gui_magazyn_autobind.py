# version: 1.0
from __future__ import annotations

from typing import Any, Callable, Dict, Optional
import weakref

import tkinter as tk
from tkinter import ttk

from gui_magazyn_kreator_bind import bind_kreator_button

# --- REJESTR SŁABYCH REFERENCJI (panel → {tree, btn}) ---
_MAG_REGISTRY: Dict[int, Dict[str, weakref.ReferenceType]] = {}


def register_magazyn_widgets(
    panel_root: tk.Misc,
    tree_widget: Optional[ttk.Treeview] = None,
    btn_kreator: Optional[tk.Misc] = None,
):
    """Zarejestruj kontrolki Magazynu w rejestrze słabych referencji."""

    if not panel_root or not panel_root.winfo_exists():
        return

    pid = int(panel_root.winfo_id())
    entry = _MAG_REGISTRY.get(pid, {})

    if tree_widget and tree_widget.winfo_exists():
        entry["tree"] = weakref.ref(tree_widget)

    if btn_kreator and btn_kreator.winfo_exists():
        entry["btn"] = weakref.ref(btn_kreator)

    _MAG_REGISTRY[pid] = entry


def _get_registered(panel_root: tk.Misc):
    try:
        entry = _MAG_REGISTRY.get(int(panel_root.winfo_id()))
        if not entry:
            return None, None

        tree_ref = entry.get("tree")
        btn_ref = entry.get("btn")

        tree = tree_ref() if tree_ref else None
        btn = btn_ref() if btn_ref else None

        if tree and not tree.winfo_exists():
            tree = None
        if btn and not btn.winfo_exists():
            btn = None

        return tree, btn
    except Exception:
        return None, None


_RETRY_DELAY_MS = 150
_MAX_RETRIES = 20


def _find_treeview(parent: tk.Misc) -> Optional[ttk.Treeview]:
    if parent is None:
        return None
    tv = getattr(parent, "_mag_tree_ref", None)
    if isinstance(tv, ttk.Treeview) and tv.winfo_exists():
        return tv
    stack = [parent]
    while stack:
        widget = stack.pop()
        if isinstance(widget, ttk.Treeview) and widget.winfo_exists():
            parent._mag_tree_ref = widget
            return widget
        try:
            stack.extend(list(widget.winfo_children()))
        except Exception:
            pass
    return None


CANDIDATE_SUBSTR = (
    "kreator",
    "zlecen",
    "zamów",
    "utwórz",
    "utworz",
    "dodaj",
    "orders",
    "order",
)


def _norm(text: str) -> str:
    return (text or "").strip().lower()


def _is_candidate_label(text: str) -> bool:
    normalized = _norm(text)
    return any(sub in normalized for sub in CANDIDATE_SUBSTR)


def _find_kreator_button(parent: tk.Misc) -> Optional[tk.Misc]:
    if parent is None:
        return None
    btn = getattr(parent, "_mag_btn_kreator_ref", None)
    if isinstance(btn, (tk.Button, ttk.Button, ttk.Menubutton)) and btn.winfo_exists():
        return btn

    stack = [parent]
    while stack:
        widget = stack.pop()
        try:
            if (
                isinstance(widget, (tk.Button, ttk.Button, ttk.Menubutton))
                and widget.winfo_exists()
            ):
                try:
                    label = str(widget.cget("text"))
                except Exception:
                    label = ""
                if _is_candidate_label(label):
                    parent._mag_btn_kreator_ref = widget
                    return widget
            stack.extend(list(widget.winfo_children()))
        except Exception:
            pass
    return None


def ensure_magazyn_kreator_binding(
    panel_root: tk.Misc,
    get_user_role: Optional[Callable[[], str]] = None,
    get_cfg: Optional[Callable[[], Any]] = None,
) -> None:
    """Zapewnij powiązanie przycisku kreatora z drzewem magazynu.

    Kolejność działań:
    1. Próba pobrania jawnie zarejestrowanych kontrolek.
    2. Fallback heurystyczny wyszukujący Treeview i przycisk w poddrzewie.
    3. Mechanizm ponawiania, aż UI się zbuduje lub wyczerpie limit prób.
    """

    if not panel_root or not panel_root.winfo_exists():
        return

    retries = getattr(panel_root, "_mag_autobind_retries", 0)

    tree, button = _get_registered(panel_root)

    if not tree:
        tree = _find_treeview(panel_root)
    if not button:
        button = _find_kreator_button(panel_root)

    if not tree or not button:
        if retries < _MAX_RETRIES:
            panel_root._mag_autobind_retries = retries + 1
            try:
                panel_root.after(
                    _RETRY_DELAY_MS,
                    lambda: ensure_magazyn_kreator_binding(
                        panel_root, get_user_role, get_cfg
                    ),
                )
            except Exception:
                pass
        else:
            print("[Magazyn-Autobind] Nie znaleziono kontrolki (btn/tree) po retry.")
        return

    panel_root._mag_autobind_retries = 0

    if getattr(button, "_mag_kreator_bound", False):
        return

    bind_kreator_button(button, tree, get_user_role=get_user_role, get_cfg=get_cfg)
    button._mag_kreator_bound = True
