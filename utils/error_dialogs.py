# version: 1.0
"""Utilities for showing standardized error dialogs."""

from __future__ import annotations

from tkinter import Button, Frame, Label, Tk, Toplevel, messagebox
from typing import Any, Literal, Optional

_DEFAULT_SUGGESTION = "Spróbuj ponownie lub skontaktuj się z administratorem."


def _resolve_parent(parent: Any | None = None) -> Any | None:
    """Return an existing parent window if available, otherwise ``None``."""

    try:
        import tkinter as tk

        if parent and getattr(parent, "winfo_exists", lambda: False)():
            return parent
        if getattr(tk, "_default_root", None) and tk._default_root.winfo_exists():
            return tk._default_root
    except Exception:
        pass
    return None


def _bring_on_top(window: Toplevel) -> None:
    """Raise dialog over other windows and ensure it temporarily stays on top."""

    try:
        window.lift()
        window.attributes("-topmost", True)
        window.focus_force()
        window.after(250, lambda: window.attributes("-topmost", False))
    except Exception:
        pass


def show_error_dialog(
    title: str,
    description: str,
    suggestion: Optional[str] = None,
    parent: Any | None = None,
) -> None:
    """Display an error dialog with description and optional suggestions."""

    if suggestion is None:
        suggestion = _DEFAULT_SUGGESTION
    message = f"{description}"
    if suggestion:
        message += f"\n\nSugerowane działania:\n{suggestion}"
    resolved_parent = _resolve_parent(parent)
    try:
        messagebox.showerror(title, message, parent=resolved_parent)
    except TypeError:
        messagebox.showerror(title, message)


def ask_unsaved_changes(
    title: str, msg: str, parent: Any | None = None
) -> Literal["save", "discard", "cancel"]:
    """Ask the user how to handle unsaved changes."""

    result: Literal["save", "discard", "cancel"] = "cancel"
    resolved_parent = _resolve_parent(parent)
    owned_root = None

    if resolved_parent is None:
        owned_root = Tk()
        owned_root.withdraw()
        resolved_parent = owned_root

    def close(value: Literal["save", "discard", "cancel"]) -> None:
        nonlocal result
        result = value
        try:
            dialog.destroy()
        except Exception:
            pass

    dialog = Toplevel(resolved_parent)
    dialog.title(title)
    dialog.resizable(False, False)
    dialog.transient(resolved_parent)
    dialog.grab_set()
    dialog.protocol("WM_DELETE_WINDOW", lambda: close("cancel"))
    dialog.bind("<Escape>", lambda e: close("cancel"))

    Label(dialog, text=msg, padx=20, pady=10).pack()

    btn_frame = Frame(dialog, pady=10)
    btn_frame.pack()

    Button(
        btn_frame,
        text="Zapisz",
        width=8,
        command=lambda: close("save"),
    ).pack(side="left", padx=5)
    Button(
        btn_frame,
        text="Odrzuć",
        width=8,
        command=lambda: close("discard"),
    ).pack(side="left", padx=5)
    Button(
        btn_frame,
        text="Anuluj",
        width=8,
        command=lambda: close("cancel"),
    ).pack(side="left", padx=5)

    _bring_on_top(dialog)
    try:
        resolved_parent.wait_window(dialog)
    except Exception:
        dialog.wait_window()

    if owned_root is not None:
        try:
            owned_root.destroy()
        except Exception:
            pass
    return result

