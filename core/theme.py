# version: 1.0
"""Zarządzanie motywami interfejsu Warsztat Managera."""

from __future__ import annotations


_ACTIVE_THEME: str | None = None


class ThemeManager:
    """Pomocnicze narzędzia do bezpiecznego stosowania motywów."""

    @staticmethod
    def apply(name: str) -> None:
        """Bezpieczne zastosowanie motywu zanim powstanie główne okno.

        Funkcja jest idempotentna – wielokrotne wywołanie nic nie psuje.
        """
        from gui._theme import apply_theme  # late import (zachowujemy istniejącą architekturę)

        global _ACTIVE_THEME

        if _ACTIVE_THEME == name:
            return

        try:
            apply_theme(name)
            _ACTIVE_THEME = name
            print(f"[WM-DBG][THEME] Zastosowano motyw: {name}")
        except Exception as exc:  # pragma: no cover - diagnostyka awaryjna
            print(f"[WM-DBG][THEME] Błąd motywu '{name}': {exc}")
            fallback = "default"
            try:
                apply_theme(fallback)
                _ACTIVE_THEME = fallback
                print("[WM-DBG][THEME] Fallback → default")
            except Exception as fallback_exc:  # pragma: no cover - diagnostyka awaryjna
                print(f"[WM-DBG][THEME] Fallback '{fallback}' także nie działa: {fallback_exc}")
