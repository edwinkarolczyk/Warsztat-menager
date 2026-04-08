# version: 1.0
"""Panel Jarvisa z banerem trybu offline oraz integracją toastów."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Optional

try:  # pragma: no cover - import Tk w środowisku bez GUI
    import tkinter as tk
    from tkinter import ttk
except Exception:  # pragma: no cover - fallback dla testów headless
    tk = None  # type: ignore[assignment]
    ttk = None  # type: ignore[assignment]

_OFFLINE_TEXT = "⚠ Jarvis działa w trybie offline – dane lokalne"
_DEFAULT_BG = "#f7f9fc"
_DEFAULT_FG = "#212529"
_THEME_CACHE: dict[str, Any] = {}

try:  # pragma: no cover - moduł GUI może być niedostępny podczas testów
    from gui_jarvis_panel import JarvisPanel as _LegacyJarvisPanel
except Exception as exc:  # pragma: no cover - fallback bez panelu wewnętrznego
    _LegacyJarvisPanel = None  # type: ignore[assignment]
    _LEGACY_IMPORT_ERROR: Optional[Exception] = exc
else:  # pragma: no cover - brak specjalnego pokrycia
    _LEGACY_IMPORT_ERROR = None


class _BannerProxy:
    """Minimalna imitacja Labela wykorzystywana w trybie headless."""

    def __init__(self, *, bg: str, fg: str) -> None:
        self._state = {"text": "", "bg": bg, "fg": fg}
        self._visible = False

    def config(self, **kwargs: Any) -> None:  # noqa: D401 - API jak w Tkinterze
        self._state.update(kwargs)

    configure = config

    def cget(self, key: str) -> Any:  # noqa: D401 - API jak w Tkinterze
        return self._state.get(key)

    def pack(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        self._visible = True

    def pack_forget(self) -> None:  # noqa: D401
        self._visible = False

    def winfo_manager(self) -> str:
        return "pack" if self._visible else ""


def _load_theme_colors() -> tuple[str, str, str]:
    global _THEME_CACHE
    if _THEME_CACHE:
        return (
            str(_THEME_CACHE.get("offline_bg", _DEFAULT_BG)),
            str(_THEME_CACHE.get("offline_fg", _DEFAULT_FG)),
            str(_THEME_CACHE.get("online_bg", _DEFAULT_BG)),
        )

    path = Path("themes.json")
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        jarvis = data.get("jarvis", {}) if isinstance(data, dict) else {}
        banner = jarvis.get("banner", {}) if isinstance(jarvis, dict) else {}
        _THEME_CACHE = {
            "offline_bg": banner.get("offline_bg", "#ffc107"),
            "offline_fg": banner.get("offline_fg", _DEFAULT_FG),
            "online_bg": banner.get("online_bg", _DEFAULT_BG),
        }
    else:
        _THEME_CACHE = {
            "offline_bg": "#ffc107",
            "offline_fg": _DEFAULT_FG,
            "online_bg": _DEFAULT_BG,
        }

    return (
        str(_THEME_CACHE.get("offline_bg", "#ffc107")),
        str(_THEME_CACHE.get("offline_fg", _DEFAULT_FG)),
        str(_THEME_CACHE.get("online_bg", _DEFAULT_BG)),
    )


class JarvisPanel:
    """Lekki panel Jarvisa z obsługą banera offline."""

    def __init__(self, master: Optional["tk.Misc"] = None) -> None:
        offline_bg, offline_fg, online_bg = _load_theme_colors()
        self._offline_bg = offline_bg
        self._offline_fg = offline_fg
        self.bg_color = online_bg
        self.jarvis_online = True
        self._offline_reason: Optional[str] = None
        self._widget: Optional["ttk.Frame"] = None
        self._owned_master: Optional["tk.Tk"] = None
        self._status_job: Optional[str] = None
        self._status_interval_ms = 10000
        self._inner_panel: Optional[object] = None

        if tk is not None and ttk is not None:
            try:
                master = self._ensure_master(master)
                if master is not None:
                    self._widget = ttk.Frame(master)
                    try:
                        current_bg = self._widget.cget("background")
                    except tk.TclError:
                        current_bg = ""
                    if current_bg:
                        self.bg_color = str(current_bg)
                    self.banner = tk.Label(
                        self._widget,
                        text="",
                        anchor="center",
                        bg=self.bg_color,
                        fg=self._offline_fg,
                        font=("Segoe UI", 10, "bold"),
                    )
                    self._body = ttk.Frame(self._widget)
                    self._body.pack(fill="both", expand=True)
                    try:
                        from gui_notifications import register_notification_root
                    except Exception:
                        pass
                    else:
                        register_notification_root(self._widget.winfo_toplevel())
                else:
                    self.banner = _BannerProxy(bg=self.bg_color, fg=self._offline_fg)
            except Exception:
                self._teardown()
                self.banner = _BannerProxy(bg=self.bg_color, fg=self._offline_fg)
        else:
            self.banner = _BannerProxy(bg=self.bg_color, fg=self._offline_fg)

        if self._widget is not None:
            self.banner.pack(fill="x", padx=12, pady=(8, 0))
        self.update_banner_state()
        self._apply_status_snapshot(self._read_status_snapshot())
        self._start_status_poll()
        self._mount_legacy_panel()

    # ------------------------------------------------------------------
    def _ensure_master(self, master: Optional["tk.Misc"]) -> Optional["tk.Misc"]:
        if master is not None:
            return master
        if tk is None:
            return None
        try:
            root = tk.Tk()
            root.withdraw()
        except tk.TclError:
            return None
        self._owned_master = root
        return root

    # ------------------------------------------------------------------
    def _teardown(self) -> None:
        self._cancel_status_poll()
        inner = getattr(self, "_inner_panel", None)
        if inner is not None:
            try:
                inner.destroy()
            except Exception:
                pass
        self._inner_panel = None
        if self._widget is not None:
            try:
                self._widget.destroy()
            except Exception:
                pass
        self._widget = None
        if self._owned_master is not None:
            try:
                self._owned_master.destroy()
            except Exception:
                pass
        self._owned_master = None

    # ------------------------------------------------------------------
    def _read_status_snapshot(self) -> Mapping[str, Any]:
        try:
            from core import jarvis_engine as _jarvis_engine
        except Exception:
            return self._status_fallback()

        getter = getattr(_jarvis_engine, "get_status", None)
        if not callable(getter):
            return self._status_fallback()

        try:
            snapshot = getter()
        except Exception:
            return self._status_fallback()

        if isinstance(snapshot, Mapping):
            return snapshot
        return self._status_fallback()

    # >>> PATCH START: Jarvis – GUI notifications
    def _status_fallback(self) -> Mapping[str, Any]:
        """Fallback snapshot when backend status is unavailable."""

        try:
            from config_manager import ConfigManager
        except Exception:
            return {}

        try:
            cfg = ConfigManager()
        except Exception:
            return {}

        try:
            enabled = bool(cfg.get("jarvis.enabled", True))
        except Exception:
            enabled = True

        if not enabled:
            return {
                "offline": True,
                "offline_reason": "Jarvis wyłączony w ustawieniach.",
            }

        return {}

    # <<< PATCH END: Jarvis – GUI notifications

    # ------------------------------------------------------------------
    def _apply_status_snapshot(self, snapshot: Mapping[str, Any]) -> None:
        offline = bool(snapshot.get("offline")) if snapshot else False
        reason_raw = snapshot.get("offline_reason") if snapshot else None
        reason = None
        if reason_raw is not None:
            reason = str(reason_raw).strip()
            if not reason:
                reason = None
        # >>> PATCH START: Jarvis – GUI notifications
        self.set_online_state(not offline, reason)
        # <<< PATCH END: Jarvis – GUI notifications

    # >>> PATCH START: Jarvis – GUI notifications
    def set_online_state(self, online: bool, reason: Optional[str] = None) -> None:
        """Public setter allowing external callers to toggle offline banner."""

        reason_text = None
        if reason is not None:
            reason_candidate = str(reason).strip()
            if reason_candidate:
                reason_text = reason_candidate

        self.jarvis_online = bool(online)
        self._offline_reason = reason_text
        self.update_banner_state()

    # <<< PATCH END: Jarvis – GUI notifications

    # ------------------------------------------------------------------
    def _cancel_status_poll(self) -> None:
        job = self._status_job
        widget = self._widget
        if job is None or widget is None:
            self._status_job = None
            return
        try:
            widget.after_cancel(job)
        except Exception:
            pass
        self._status_job = None

    # ------------------------------------------------------------------
    def _start_status_poll(self) -> None:
        widget = self._widget
        if widget is None:
            return
        self._cancel_status_poll()
        try:
            self._status_job = widget.after(self._status_interval_ms, self._poll_status)
        except Exception:
            self._status_job = None

    # ------------------------------------------------------------------
    def _poll_status(self) -> None:
        self._status_job = None
        self._apply_status_snapshot(self._read_status_snapshot())
        widget = self._widget
        if widget is None:
            return
        try:
            self._status_job = widget.after(self._status_interval_ms, self._poll_status)
        except Exception:
            self._status_job = None

    # ------------------------------------------------------------------
    def _banner_visible(self) -> bool:
        try:
            manager = self.banner.winfo_manager()
        except Exception:
            manager = ""
        return bool(manager)

    # ------------------------------------------------------------------
    def update_banner_state(self) -> None:
        if getattr(self, "jarvis_online", True):
            self.banner.config(text="", bg=self.bg_color, fg=self._offline_fg)
            if self._banner_visible():
                try:
                    self.banner.pack_forget()
                except Exception:
                    pass
        else:
            reason = getattr(self, "_offline_reason", None) or ""
            reason_text = reason.strip()
            message = _OFFLINE_TEXT
            if reason_text:
                message = f"{_OFFLINE_TEXT}\n{reason_text}"
            self.banner.config(text=message, bg=self._offline_bg, fg=self._offline_fg)
            if not self._banner_visible():
                try:
                    self.banner.pack(fill="x", padx=12, pady=(8, 0))
                except Exception:
                    pass

    # ------------------------------------------------------------------
    def destroy(self) -> None:
        self._teardown()

    # -- API delegujące -------------------------------------------------
    def __getattr__(self, item: str) -> Any:
        widget = object.__getattribute__(self, "_widget")
        if widget is None:
            raise AttributeError(item)
        return getattr(widget, item)

    def pack(self, *args: Any, **kwargs: Any) -> Any:
        widget = self._widget
        if widget is None:
            return None
        return widget.pack(*args, **kwargs)

    def grid(self, *args: Any, **kwargs: Any) -> Any:
        widget = self._widget
        if widget is None:
            return None
        return widget.grid(*args, **kwargs)

    def place(self, *args: Any, **kwargs: Any) -> Any:
        widget = self._widget
        if widget is None:
            return None
        return widget.place(*args, **kwargs)

    def winfo_toplevel(self) -> Optional["tk.Misc"]:
        widget = self._widget
        if widget is None:
            return None
        return widget.winfo_toplevel()

    # ------------------------------------------------------------------
    def _mount_legacy_panel(self) -> None:
        if ttk is None:
            return
        container = getattr(self, "_body", None)
        if container is None:
            return
        if getattr(self, "_inner_panel", None) is not None:
            return
        if _LegacyJarvisPanel is None:
            self._show_placeholder(
                container,
                "Panel Jarvis jest niedostępny – błąd importu modułu GUI.",
                detail=str(_LEGACY_IMPORT_ERROR) if _LEGACY_IMPORT_ERROR else None,
            )
            return
        try:
            inner = _LegacyJarvisPanel(container)
        except Exception as exc:
            self._show_placeholder(
                container,
                "Nie udało się zainicjalizować panelu Jarvis.",
                detail=str(exc),
            )
            return
        self._inner_panel = inner
        try:
            inner.pack(fill="both", expand=True)
        except Exception:
            self._inner_panel = None

    # ------------------------------------------------------------------
    def _show_placeholder(
        self, container: "ttk.Frame", message: str, *, detail: Optional[str] = None
    ) -> None:
        try:
            for child in container.winfo_children():
                child.destroy()
        except Exception:
            pass
        text = message
        if detail:
            detail_text = str(detail).strip()
            if detail_text:
                text = f"{message}\nSzczegóły: {detail_text}"
        ttk.Label(
            container,
            text=text,
            foreground="#e53935",
            justify="left",
            anchor="w",
        ).pack(fill="both", expand=True, padx=16, pady=24)


__all__ = ["JarvisPanel"]
