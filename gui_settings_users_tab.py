# version: 1.0
"""Helpers for injecting the legacy users panel into the settings window."""

from __future__ import annotations

from typing import Optional

import tkinter as tk
from tkinter import ttk

from ustawienia_uzytkownicy import SettingsProfilesTab


def _find_tab(notebook: ttk.Notebook, title: str) -> Optional[tk.Misc]:
    """Return the existing tab frame matching ``title`` if available."""

    for tab_id in notebook.tabs():
        try:
            if notebook.tab(tab_id, "text") == title:
                return notebook.nametowidget(tab_id)
        except Exception:
            continue
    return None


def create_users_tab(
    parent: tk.Misc, *, title: str = "Użytkownicy"
) -> ttk.Frame | None:
    """Build the legacy users panel inside Notebook tab or embedded Frame."""

    frame: ttk.Frame | None = None

    if isinstance(parent, ttk.Notebook):
        frame = _find_tab(parent, title)
        if frame is None:
            frame = ttk.Frame(parent)
            parent.add(frame, text=title)
    else:
        frame = ttk.Frame(parent)

    for child in list(frame.winfo_children()):
        try:
            child.destroy()
        except Exception:
            continue

    tab = SettingsProfilesTab(frame)
    tab.pack(fill="both", expand=True, padx=12, pady=12)
    return frame


__all__ = ["create_users_tab"]
