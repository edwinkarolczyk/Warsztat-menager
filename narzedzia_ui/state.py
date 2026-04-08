# version: 1.0
"""Stan współdzielony panelu narzędzi WM."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

import tkinter as tk
from tkinter import ttk


@dataclass(slots=True)
class ToolsPanelState:
    """Agreguje rozproszone wcześniej zmienne globalne modułu narzędzi."""

    current_login: str | None = None
    current_role: str | None = None
    assign_tree: ttk.Treeview | None = None
    assign_row_data: dict[str, dict[str, Any]] = field(default_factory=dict)
    cmb_user_var: tk.StringVar | None = None
    var_filter_mine: tk.BooleanVar | None = None
    tasks_tree: ttk.Treeview | None = None
    tasks_owner: str | None = None
    tasks_selected_path: Path | None = None
    tasks_selected_nr: str | None = None
    tasks_rows_meta: dict[str, Dict[str, Any]] = field(default_factory=dict)
    tasks_docs_cache: dict[Path, Dict[str, Any]] = field(default_factory=dict)
    tools_docs_cache: dict[Path, Dict[str, Any]] = field(default_factory=dict)
    tasks_history_var: tk.BooleanVar | None = None
    tasks_archived_var: tk.BooleanVar | None = None
    tasks_tooltips: dict[str, str] = field(default_factory=dict)
    tasks_tooltip_helper: Any | None = None
    progress_after_id: Any | None = None
    progress_job_active: bool = False


STATE = ToolsPanelState()

__all__ = ["STATE", "ToolsPanelState"]
