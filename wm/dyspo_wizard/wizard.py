# version: 1.0
"""Entry point for the Dyspozycje wizard."""

from __future__ import annotations

import importlib
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, Optional, Type

from wm.gui.i18n import t
from wm.settings.util import get_conf

from .constants import TYPES_REGISTRY
from .validators import validate_required


class _Wizard:
    def __init__(self, parent: tk.Misc | None, context: Optional[Dict] = None) -> None:
        self.root = tk.Toplevel(parent)
        self.root.title(t("wizard.dyspo.title"))
        self.root.geometry("540x420")
        self.root.transient(parent)
        self.root.grab_set()
        self.context = context or {}
        self._current_step: ttk.Frame | None = None
        self._current_code: str | None = None
        self._content = ttk.Frame(self.root)
        self._content.pack(fill="both", expand=True)
        self._controls = ttk.Frame(self.root)
        self._controls.pack(fill="x", pady=8)
        self._validate_btn = ttk.Button(
            self._controls,
            text=t("wizard.dyspo.validate"),
            state="disabled",
            command=self._validate,
        )
        self._validate_btn.pack(side=tk.RIGHT, padx=8)
        ttk.Button(
            self._controls,
            text=t("wizard.dyspo.close"),
            command=self.root.destroy,
        ).pack(side=tk.RIGHT, padx=8)
        self._show_selection()
        self.root.update_idletasks()
        self._center_on_parent(parent)

    def _center_on_parent(self, parent: tk.Misc | None) -> None:
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        if parent is not None:
            x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
            y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
        else:
            x = (self.root.winfo_screenwidth() - width) // 2
            y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _clear_content(self) -> None:
        for widget in self._content.winfo_children():
            widget.destroy()

    def _show_selection(self) -> None:
        self._clear_content()
        frame = ttk.Frame(self._content)
        frame.pack(fill="both", expand=True, padx=16, pady=16)
        ttk.Label(
            frame,
            text=t("wizard.dyspo.choose_type"),
            font=("TkDefaultFont", 12),
        ).pack(pady=(0, 12))
        for code, meta in TYPES_REGISTRY.items():
            ttk.Button(
                frame,
                text=meta["button"],
                command=lambda c=code: self._show_step(c),
            ).pack(fill="x", pady=4)
        self._validate_btn.configure(state="disabled")

    def _show_step(self, code: str) -> None:
        self._clear_content()
        meta = TYPES_REGISTRY.get(code)
        if meta is None:
            messagebox.showerror(t("wizard.dyspo.title"), f"Brak definicji kroku dla {code}.")
            return
        try:
            module_path, class_name = meta["step"].rsplit(".", 1)
            module = importlib.import_module(module_path)
            step_class: Type[ttk.Frame] = getattr(module, class_name)
        except Exception as exc:  # pragma: no cover - defensive
            messagebox.showerror(
                t("wizard.dyspo.title"),
                f"Nie udało się załadować kroku {code}: {exc}",
            )
            return
        step = step_class(self._content, context=self.context, title=meta["label"])
        step.pack(fill="both", expand=True, padx=12, pady=12)
        if hasattr(step, "render"):
            step.render()
        self._current_step = step
        self._current_code = code
        self._validate_btn.configure(state="normal")

    def _validate(self) -> None:
        if not self._current_step or not self._current_code:
            return
        data = {}
        if hasattr(self._current_step, "collect_data"):
            try:
                data = self._current_step.collect_data()
            except Exception:
                data = {}
        conf = get_conf()
        errors = validate_required(data or {}, self._current_code, conf)
        if errors:
            messagebox.showerror(t("wizard.dyspo.title"), "\n".join(errors))
        else:
            messagebox.showinfo(
                t("wizard.dyspo.title"),
                t("wizard.dyspo.valid"),
            )


def open_dyspo_wizard(parent: tk.Misc | None, context: Optional[Dict] = None) -> _Wizard:
    """Open Dyspozycje wizard and return controller instance."""

    return _Wizard(parent, context)


__all__ = ["open_dyspo_wizard"]
