# version: 1.0
"""Helpers for binding global keyboard shortcuts."""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from wm.settings.util import get_conf

try:  # pragma: no cover - kreator opcjonalny w starych instalacjach
    from wm.dyspo_wizard import open_dyspo_wizard
except Exception:  # pragma: no cover - fallback bez kreatora
    open_dyspo_wizard = None  # type: ignore


def bind_ctrl_d(root: tk.Misc, *, context: Optional[dict] = None) -> None:
    """Bind Ctrl+D shortcut when enabled in the configuration."""

    conf = get_conf()
    enabled = (
        conf.get("dyspo", {})
        .get("shortcuts", {})
        .get("ctrlD", False)
    )
    if not enabled or open_dyspo_wizard is None:
        return

    def _handler(event: tk.Event | None = None) -> str:
        open_dyspo_wizard(root, context=context or {})
        return "break"

    if not hasattr(root, "bind"):
        return
    for seq in ("<Control-d>", "<Control-D>"):
        try:
            root.bind(seq, _handler, add="+")
        except Exception:  # pragma: no cover - środowiska testowe bez tk
            return


__all__ = ["bind_ctrl_d"]
