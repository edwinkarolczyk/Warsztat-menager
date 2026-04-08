# version: 1.0
"""[RC2][Jarvis] Middleware dispatchera komunikatów."""

from __future__ import annotations

try:  # pragma: no cover - import zależy od środowiska GUI
    from gui_notifications import show_notification
except Exception:  # pragma: no cover - środowisko headless
    show_notification = None  # type: ignore[assignment]

_ALLOWED_LEVELS = {"info", "warning", "error"}


def _normalize_level(level: str) -> str:
    text = (level or "info").strip().lower()
    if text not in _ALLOWED_LEVELS:
        return "info"
    return text


def dispatch(message: str, level: str = "info", origin: str = "Jarvis") -> bool:
    """Centralny dispatcher dla powiadomień i logów."""

    normalized_level = _normalize_level(level)
    payload = f"[{origin}] {message}"

    ok = False
    if show_notification is not None:
        try:
            ok = bool(show_notification(payload, level=normalized_level))
        except Exception as exc:  # pragma: no cover - diagnostyka środowiska
            print(f"[JARVIS-DISPATCH][ERR] {exc}")
            ok = False

    print(f"[JARVIS-DISPATCH] {normalized_level.upper()}: {message}")
    return ok
