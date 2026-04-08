# version: 1.0
"""Simplified settings window with Dyspozycje tab."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..settings.tabs import DyspoTab
from .i18n import t


class SettingsWindow(tk.Toplevel):
    """Lightweight settings window embedding Dyspo tab."""

    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.title(t("settings.tab.dyspo"))
        self.geometry("720x540")
        self.transient(master)
        self._build()

    def _build(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)
        notebook.add(DyspoTab(notebook), text=t("settings.tab.dyspo"))


__all__ = ["SettingsWindow"]
