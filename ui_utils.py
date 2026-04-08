# version: 1.0
"""Utility helpers for Tkinter popups."""

from __future__ import annotations

from typing import Any
import tkinter as tk
from tkinter import messagebox


class TopMost:
    """Context manager forcing ``widget`` to stay above other windows."""

    def __init__(
        self,
        widget: tk.Misc | None,
        parent: tk.Misc | None = None,
        *,
        grab: bool = True,
    ) -> None:
        self.widget = widget
        self.parent = parent
        self.grab = grab
        self._grabbed = False

    def __enter__(self) -> tk.Misc | None:
        if self.widget is None:
            return None
        try:
            _ensure_topmost(self.widget, self.parent)
        except Exception:
            return self.widget
        if self.grab:
            try:
                self.widget.grab_set()
                self._grabbed = True
            except Exception:
                self._grabbed = False
        return self.widget

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self._grabbed:
            try:
                self.widget.grab_release()
            except Exception:
                pass
        return False


def _ensure_topmost(widget: tk.Misc, parent: tk.Misc | None = None) -> None:
    """Ensure ``widget`` window stays above its parent (or master toplevel)."""

    def _window(obj: tk.Misc | None) -> tk.Misc | None:
        try:
            return obj.winfo_toplevel() if obj else None
        except Exception:
            return None

    def _drop_topmost(win: tk.Misc) -> None:
        try:
            win.attributes("-topmost", False)
        except Exception:
            pass

    try:
        window = _window(widget) or widget
        owner = _window(parent)
        if owner is None:
            owner = _window(getattr(window, "master", None))

        if owner and owner is not window:
            try:
                window.transient(owner)
            except Exception:
                pass
            try:
                owner.attributes("-topmost", True)
            except Exception:
                owner = None
            else:
                owner.after_idle(lambda: _drop_topmost(owner))

        try:
            window.lift(owner)
        except Exception:
            window.lift()
        window.focus_force()
        window.attributes("-topmost", True)
        window.after_idle(lambda: _drop_topmost(window))
    except Exception:
        pass


def _msg_info(parent: tk.Misc, title: str, message: str, **kwargs: Any) -> str:
    """Show an informational message box bound to ``parent``."""
    return messagebox.showinfo(title, message, parent=parent, **kwargs)


def _msg_warning(parent: tk.Misc, title: str, message: str, **kwargs: Any) -> str:
    """Show a warning message box bound to ``parent``."""
    return messagebox.showwarning(title, message, parent=parent, **kwargs)


def _msg_error(parent: tk.Misc, title: str, message: str, **kwargs: Any) -> str:
    """Show an error message box bound to ``parent``."""
    return messagebox.showerror(title, message, parent=parent, **kwargs)
