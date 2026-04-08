# version: 1.0
from __future__ import annotations

from typing import Callable, Dict, Optional

import tkinter as tk
from tkinter import ttk

from core.settings_manager import Settings
from core.ui_notebook_autobind import attach_magazyn_autobind_to_notebook
from gui_magazyn_autobind import ensure_magazyn_kreator_binding


class WindowManager:
    """Singleton manager for the application's main window and notebook."""

    _instance: WindowManager | None = None

    @classmethod
    def instance(cls, cfg: Settings) -> WindowManager:
        if cls._instance is None:
            cls._instance = cls(cfg)
        return cls._instance

    def __init__(self, cfg: Settings) -> None:
        self.cfg = cfg
        self.root = tk.Tk()
        self.root.title("Warsztat Menager")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.nb = ttk.Notebook(self.root)
        attach_magazyn_autobind_to_notebook(
            self.nb,
            ensure_fn=ensure_magazyn_kreator_binding,
            get_user_role=lambda: "brygadzista",
            get_cfg=lambda: self.cfg,
        )
        self.nb.pack(fill="both", expand=True)

        self._tabs: Dict[str, tuple[ttk.Frame, Optional[Callable[[], None]]]] = {}

        self._restore_geometry()

        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _restore_geometry(self) -> None:
        if not self.cfg.get("gui.main.remember_geometry", True):
            return
        geom = self.cfg.get("gui.main.geometry", "")
        if geom:
            try:
                self.root.geometry(geom)
            except Exception:  # pragma: no cover - Tk behaviour depends on OS
                pass
        if self.cfg.get("gui.main.maximized", False):
            try:
                self.root.state("zoomed")
            except Exception:  # pragma: no cover
                try:
                    self.root.attributes("-zoomed", True)
                except Exception:  # pragma: no cover
                    pass

    def _store_geometry(self) -> None:
        if not self.cfg.get("gui.main.remember_geometry", True):
            return
        try:
            maximized = self.root.state() == "zoomed"
            self.cfg.set("gui.main.maximized", bool(maximized))
            if not maximized:
                self.cfg.set("gui.main.geometry", self.root.geometry())
            current = self.nb.select()
            if current:
                title = self.nb.tab(current, "text") or ""
                if title:
                    self.cfg.set("gui.main.active_tab", title)
            self.cfg.save()
        except Exception:  # pragma: no cover - Tk behaviour depends on OS
            pass

    def _on_close(self) -> None:
        self._store_geometry()
        self.root.destroy()

    def _on_tab_changed(self, _evt=None) -> None:
        try:
            current = self.nb.select()
            title = self.nb.tab(current, "text") or ""
            if title:
                self.cfg.set("gui.main.active_tab", title)
                self.cfg.save()
        except Exception:  # pragma: no cover - Tk behaviour depends on OS
            pass

    def ensure_tab(
        self, name: str, on_show: Optional[Callable[[], None]] = None
    ) -> ttk.Frame:
        if name in self._tabs:
            return self._tabs[name][0]

        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text=name)
        self._tabs[name] = (frame, on_show)
        return frame

    def show(self, tab_name: Optional[str] = None) -> None:
        want = tab_name or self.cfg.get("gui.main.active_tab", "Maszyny")
        if want in self._tabs:
            idx = list(self._tabs).index(want)
            self.nb.select(idx)
        self._fire_on_show()
        self.root.deiconify()
        self.root.lift()
        self.root.mainloop()

    def _fire_on_show(self) -> None:
        try:
            current = self.nb.select()
            for name, (frame, cb) in self._tabs.items():
                if str(frame) == current and cb:
                    cb()
                    break
        except Exception:  # pragma: no cover - Tk behaviour depends on OS
            pass


def get_main_window(cfg: Settings) -> WindowManager:
    return WindowManager.instance(cfg)
