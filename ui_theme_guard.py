# version: 1.0
"""Idempotentny strażnik motywu.

Zapewnia, że "apply theme" wykona się tylko raz na sesję / dany motyw.
Dzięki temu unikamy powtarzających się logów THEME. Strażnik nie zależy
sztywno od konkretnego managera motywów – korzysta miękko z dostępnych
ścieżek.
"""
from typing import Any


def _get_current_theme_name(owner: Any) -> str:
    """Spróbuj wydobyć nazwę motywu z configu lub managera."""
    for path in (
        ("cfg_manager", "get_theme_name"),
        ("theme_manager", "current_name"),
        ("theme_manager", "get_current_name"),
    ):
        try:
            cur = owner
            for attr in path[:-1]:
                cur = getattr(cur, attr)
            fn = getattr(cur, path[-1])
            name = fn() if callable(fn) else str(fn)
            if name:
                return str(name)
        except Exception:
            continue
    # Fallback – przyjmij "default", jeśli brak informacji.
    return "default"


def ensure_theme_applied(owner: Any) -> None:
    """Zastosuj motyw tylko jeśli nie był jeszcze zastosowany."""
    try:
        theme_name = _get_current_theme_name(owner)
    except Exception:
        theme_name = "default"

    already = getattr(owner, "__wm_theme_applied__", None)
    if already == theme_name:
        # Już zastosowano – nic nie rób, unikamy spamowania logów.
        return

    # Spróbuj różnych ścieżek wywołania apply.
    for path in (
        ("theme_manager", "apply_current"),
        ("theme_manager", "apply"),
        ("apply_theme",),
    ):
        try:
            cur = owner
            for attr in path[:-1]:
                cur = getattr(cur, attr)
            fn = getattr(cur, path[-1])
            # Wywołaj bez parametrów – implementacja bazuje na configu.
            fn()
            # Zapamiętaj, że ten motyw został zastosowany.
            setattr(owner, "__wm_theme_applied__", theme_name)
            return
        except Exception:
            continue

    # Jeśli nie ma żadnej ścieżki – ustaw znacznik, by nie próbować w kółko.
    setattr(owner, "__wm_theme_applied__", theme_name)
