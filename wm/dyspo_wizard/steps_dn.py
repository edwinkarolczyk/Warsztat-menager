# version: 1.0
"""Stub step for Dyspozycja DN."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from wm.gui.i18n import t


class StepDN(ttk.Frame):
    """Placeholder for DN flow."""

    def __init__(
        self,
        master: tk.Misc,
        context: dict | None = None,
        *,
        title: str | None = None,
    ) -> None:
        super().__init__(master)
        self.context = context or {}
        self._title = title or t("wizard.dyspo.type.DN")

    def render(self) -> None:
        ttk.Label(
            self,
            text=self._title,
            font=("TkDefaultFont", 12, "bold"),
        ).pack(pady=16)
        ttk.Label(
            self,
            text="(Wersja robocza – szczegóły w przygotowaniu)",
        ).pack(pady=8)

    def collect_data(self) -> dict:
        return self.context.get("data", {})

