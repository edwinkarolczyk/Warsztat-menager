# version: 1.0
"""Tkinter tab for configuring Dyspozycje."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List

from ..util import get_conf, preview_number, save_conf
from ...gui.i18n import t


class DyspoTab(ttk.Frame):
    """Tab responsible for Dyspozycje configuration."""

    CODES: List[str] = ["DM", "DZ", "DW", "DN"]

    def __init__(self, master: tk.Misc, *, conf: Dict | None = None) -> None:
        super().__init__(master)
        self._conf = conf or get_conf()
        self._dyspo = self._conf.get("dyspo", {})
        self._enabled_vars: Dict[str, tk.BooleanVar] = {}
        self._pattern_vars: Dict[str, tk.StringVar] = {}
        self._counter_vars: Dict[str, tk.IntVar] = {}
        self._preview_labels: Dict[str, ttk.Label] = {}
        self._build_ui()

    # region building
    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)

        self._build_enabled_section()
        self._build_numbering_section()
        self._build_flow_section()
        self._build_required_section()
        self._build_shortcuts_section()
        self._build_save_button()

    def _build_enabled_section(self) -> None:
        box = ttk.LabelFrame(self, text=t("settings.dyspo.enabled_types"))
        box.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        for idx, code in enumerate(self.CODES):
            var = tk.BooleanVar(
                value=code in (self._dyspo.get("enabled_types") or [])
            )
            self._enabled_vars[code] = var
            ttk.Checkbutton(
                box,
                text=t(f"settings.dyspo.type.{code}"),
                variable=var,
            ).grid(row=0, column=idx, padx=4, pady=4, sticky="w")

    def _build_numbering_section(self) -> None:
        frame = ttk.LabelFrame(self, text=t("settings.dyspo.numbering"))
        frame.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)
        frame.columnconfigure(3, weight=1)
        header = [
            (0, t("settings.dyspo.numbering.type")),
            (1, t("settings.dyspo.numbering.pattern")),
            (2, t("settings.dyspo.numbering.counter")),
            (3, t("settings.dyspo.numbering.preview")),
        ]
        for col, text in header:
            ttk.Label(frame, text=text, style="Caption.TLabel").grid(
                row=0, column=col, sticky="w", padx=4, pady=(0, 6)
            )

        numbering = self._dyspo.get("numbering") or {}
        for row, code in enumerate(self.CODES, start=1):
            ttk.Label(frame, text=code).grid(
                row=row, column=0, padx=4, pady=2, sticky="w"
            )
            defaults = numbering.get(
                code,
                {"pattern": f"{code}-{{YYYY}}-{{####}}", "counter": 1},
            )
            pattern_var = tk.StringVar(value=defaults.get("pattern", ""))
            counter_var = tk.IntVar(value=int(defaults.get("counter", 1)))
            self._pattern_vars[code] = pattern_var
            self._counter_vars[code] = counter_var

            entry = ttk.Entry(frame, textvariable=pattern_var)
            entry.grid(row=row, column=1, padx=4, pady=2, sticky="ew")

            spin = ttk.Spinbox(
                frame,
                from_=1,
                to=999999,
                textvariable=counter_var,
                width=8,
                increment=1,
            )
            spin.grid(row=row, column=2, padx=4, pady=2, sticky="w")

            preview = ttk.Label(frame, text="", width=24)
            preview.grid(row=row, column=3, padx=4, pady=2, sticky="w")
            self._preview_labels[code] = preview

            pattern_var.trace_add(
                "write", lambda *_a, c=code: self._update_preview(c)
            )
            counter_var.trace_add(
                "write", lambda *_a, c=code: self._update_preview(c)
            )
            self._update_preview(code)

    def _build_flow_section(self) -> None:
        frame = ttk.LabelFrame(self, text=t("settings.dyspo.flow"))
        frame.grid(row=2, column=0, sticky="ew", padx=12, pady=6)
        self._flow_var = tk.StringVar(value=self._dyspo.get("flow", "simple"))
        ttk.Radiobutton(
            frame,
            text=t("settings.dyspo.flow.simple"),
            variable=self._flow_var,
            value="simple",
        ).grid(row=0, column=0, padx=4, pady=2, sticky="w")
        ttk.Radiobutton(
            frame,
            text=t("settings.dyspo.flow.extended"),
            variable=self._flow_var,
            value="extended",
        ).grid(row=0, column=1, padx=4, pady=2, sticky="w")

    def _build_required_section(self) -> None:
        frame = ttk.LabelFrame(self, text=t("settings.dyspo.required"))
        frame.grid(row=3, column=0, sticky="ew", padx=12, pady=6)
        required = self._dyspo.get("required") or {}
        self._req_machine = tk.BooleanVar(
            value=bool(required.get("machine_id", True))
        )
        self._req_tool = tk.BooleanVar(value=bool(required.get("tool_id", False)))
        self._req_items = tk.BooleanVar(
            value=bool(required.get("at_least_one_item", True))
        )
        ttk.Checkbutton(
            frame,
            text=t("settings.dyspo.required.machine_id"),
            variable=self._req_machine,
        ).grid(row=0, column=0, padx=4, pady=2, sticky="w")
        ttk.Checkbutton(
            frame,
            text=t("settings.dyspo.required.tool_id"),
            variable=self._req_tool,
        ).grid(row=0, column=1, padx=4, pady=2, sticky="w")
        ttk.Checkbutton(
            frame,
            text=t("settings.dyspo.required.at_least_one_item"),
            variable=self._req_items,
        ).grid(row=0, column=2, padx=4, pady=2, sticky="w")

    def _build_shortcuts_section(self) -> None:
        frame = ttk.LabelFrame(self, text=t("settings.dyspo.shortcuts"))
        frame.grid(row=4, column=0, sticky="ew", padx=12, pady=6)
        shortcuts = self._dyspo.get("shortcuts") or {}
        self._shortcut_ctrl_d = tk.BooleanVar(
            value=bool(shortcuts.get("ctrlD", True))
        )
        ttk.Checkbutton(
            frame,
            text=t("settings.dyspo.shortcuts.ctrlD"),
            variable=self._shortcut_ctrl_d,
        ).grid(row=0, column=0, padx=4, pady=2, sticky="w")

    def _build_save_button(self) -> None:
        button = ttk.Button(self, text=t("settings.dyspo.save"), command=self._save)
        button.grid(row=5, column=0, padx=12, pady=12, sticky="e")

    # endregion

    def _update_preview(self, code: str) -> None:
        pattern = self._pattern_vars[code].get()
        counter = self._counter_vars[code].get()
        preview = preview_number(pattern, code, counter)
        self._preview_labels[code].configure(text=preview)

    def _save(self) -> None:
        dyspo = self._conf.setdefault("dyspo", {})
        dyspo["enabled_types"] = [
            code for code, var in self._enabled_vars.items() if var.get()
        ]
        numbering = {}
        for code in self.CODES:
            pattern = self._pattern_vars[code].get().strip()
            counter = max(1, int(self._counter_vars[code].get()))
            numbering[code] = {"pattern": pattern, "counter": counter}
        dyspo["numbering"] = numbering
        dyspo["flow"] = self._flow_var.get()
        dyspo["required"] = {
            "machine_id": self._req_machine.get(),
            "tool_id": self._req_tool.get(),
            "at_least_one_item": self._req_items.get(),
        }
        dyspo["shortcuts"] = {"ctrlD": self._shortcut_ctrl_d.get()}
        save_conf(self._conf)
        messagebox.showinfo(
            t("settings.dyspo.saved_title"),
            t("settings.dyspo.saved_message"),
        )
