# version: 1.0
"""Helpery do wyświetlania powiadomień toast w aplikacji Tkinter."""

from __future__ import annotations

import tkinter as tk
from typing import Iterable, List, Optional, Tuple

__all__ = [
    "NotificationPopup",
    "register_notification_root",
    "show_notification",
]

_DEFAULT_DURATION = 5.0
_LEVEL_STYLES = {
    "info": {"bg": "#212529", "fg": "#f8f9fa"},
    "warning": {"bg": "#ffb300", "fg": "#212121"},
    "error": {"bg": "#d32f2f", "fg": "#fafafa"},
}
_LEVEL_DURATIONS = {"warning": 6.0, "error": 7.0}
_PENDING: List[Tuple[str, str, float]] = []
_DEFAULT_MASTER: Optional[tk.Misc] = None


class NotificationPopup(tk.Toplevel):
    """A small toast-like popup that disappears after a duration."""

    def __init__(
        self,
        master: tk.Misc,
        message: str,
        duration: float = _DEFAULT_DURATION,
        *,
        level: str = "info",
    ) -> None:
        super().__init__(master)
        self.duration = max(0.5, float(duration))
        self.message = message
        self.level = level if level in _LEVEL_STYLES else "info"
        self._build_ui()
        self.after(int(self.duration * 1000), self.destroy)

    def _build_ui(self) -> None:
        colors = _LEVEL_STYLES.get(self.level, _LEVEL_STYLES["info"])
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg=colors["bg"])

        label = tk.Label(
            self,
            text=self.message,
            bg=colors["bg"],
            fg=colors["fg"],
            font=("Segoe UI", 10),
            wraplength=320,
            justify="left",
            padx=12,
            pady=10,
        )
        label.pack(fill="both", expand=True)

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        x = screen_width - width - 20
        y = screen_height - height - 70
        self.geometry(f"{width}x{height}+{x}+{y}")


def _schedule_popup(master: tk.Misc, message: str, level: str, duration: float) -> None:
    def _show() -> None:
        NotificationPopup(master, message, duration, level=level)

    master.after(0, _show)


def _flush_pending(master: tk.Misc) -> None:
    if not _PENDING:
        return
    pending: Iterable[Tuple[str, str, float]] = tuple(_PENDING)
    _PENDING.clear()
    for message, level, duration in pending:
        _schedule_popup(master, message, level, duration)


def register_notification_root(master: tk.Misc) -> None:
    """Set the default Tk widget used for toast notifications."""

    global _DEFAULT_MASTER
    if master is None:
        return
    _DEFAULT_MASTER = master
    try:
        _flush_pending(master)
    except tk.TclError:
        # Jeśli master został zniszczony zanim opróżniono kolejkę, zostawiamy wpisy.
        pass


def show_notification(
    message: str,
    level: str = "info",
    *,
    master: Optional[tk.Misc] = None,
    duration: Optional[float] = None,
) -> bool:
    """Schedule a notification popup to appear on the Tkinter event loop.

    Zwraca ``True`` jeśli powiadomienie zostało zaplanowane, w przeciwnym razie
    (brak zainicjalizowanego GUI) komunikat trafia do kolejki i funkcja zwraca
    ``False``.
    """

    resolved_master = master or _DEFAULT_MASTER
    resolved_level = level if level in _LEVEL_STYLES else "info"
    resolved_duration = (
        max(0.5, float(duration))
        if duration is not None
        else _LEVEL_DURATIONS.get(resolved_level, _DEFAULT_DURATION)
    )

    if resolved_master is None:
        _PENDING.append((message, resolved_level, resolved_duration))
        return False

    try:
        _schedule_popup(resolved_master, message, resolved_level, resolved_duration)
    except tk.TclError:
        _PENDING.append((message, resolved_level, resolved_duration))
        return False

    return True


if __name__ == "__main__":  # pragma: no cover - manualne uruchomienie
    root = tk.Tk()
    root.withdraw()
    register_notification_root(root)
    show_notification("🔔 Jarvis: Wykryto długi przestój maszyny M-02.", level="warning")
    root.mainloop()
