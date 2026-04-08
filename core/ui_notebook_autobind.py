# version: 1.0
from __future__ import annotations

from typing import Callable, Optional

import tkinter as tk
from tkinter import ttk

try:  # pragma: no cover - optional convenience helper
    from gui_magazyn_kreator_bind import ensure_magazyn_kreator_binding as _ensure
    from core.settings_manager import Settings as _Settings

    _CFG_GLOBAL = _Settings(path="config.json", project_root=__file__)

    def _default_role() -> str:
        return "brygadzista"

    def attach_default_magazyn_autobind(nb: ttk.Notebook) -> None:
        attach_magazyn_autobind_to_notebook(
            nb,
            ensure_fn=_ensure,
            get_user_role=_default_role,
            get_cfg=lambda: _CFG_GLOBAL,
        )

except Exception as _e:  # pragma: no cover - optional import guard
    _CFG_GLOBAL = None
    _ensure = None



def _get_tab_frame(nb: ttk.Notebook) -> Optional[tk.Misc]:
    try:
        cur = nb.select()
        if not cur:
            return None
        return nb.nametowidget(cur)
    except Exception:
        return None


def attach_magazyn_autobind_to_notebook(
    nb: ttk.Notebook,
    ensure_fn: Callable[..., None],
    get_user_role: Callable[[], str],
    get_cfg: Callable[[], object],
) -> None:
    """Attach notebook listener to trigger ``ensure_fn`` on tab change."""
    if not nb or not nb.winfo_exists():
        return

    def _on_tab_changed(_evt=None):
        frame = _get_tab_frame(nb)
        if frame and frame.winfo_exists():
            try:
                ensure_fn(frame, get_user_role=get_user_role, get_cfg=get_cfg)
            except Exception as e:
                print("[Notebook-Autobind] error:", e)

    try:
        nb.bind("<<NotebookTabChanged>>", _on_tab_changed, add="+")
    except Exception:
        pass

    try:
        nb.after(100, _on_tab_changed)
    except Exception:
        pass
