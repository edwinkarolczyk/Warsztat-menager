"""Menadżer motywów z kontrolą logów i cache."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import ui_theme

CONFIG_FILE = Path("config.json")

# ogranicz spam w logach (wiele Topleveli)
_WM_THEME_LOG_ONCE: set[str] = set()


def _log(message: str) -> None:
    """Prosty wrapper na logowanie komunikatów debug."""

    try:
        print(message)
    except Exception:
        pass


def _get_theme_from_config() -> str | None:
    """Odczytaj motyw z config.json (sekcja ui.theme lub legacy theme)."""

    try:
        if CONFIG_FILE.is_file():
            data: dict[str, Any] = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            ui_section = data.get("ui")
            if isinstance(ui_section, dict):
                name = ui_section.get("theme")
                if isinstance(name, str):
                    return name
            legacy = data.get("theme")
            if isinstance(legacy, str):
                return legacy
    except Exception:
        return None
    return None


def _alias_theme(name: str) -> str:
    """Zmapuj alias motywu na właściwą nazwę, jeśli to możliwe."""

    try:
        resolved = ui_theme.resolve_theme_name(name)
        if resolved != name:
            msg = (
                f"[WM-DBG][THEME] Alias motywu '{name}' zamieniony na '{resolved}'"
            )
            if msg not in _WM_THEME_LOG_ONCE:
                _WM_THEME_LOG_ONCE.add(msg)
                print(msg)
        return resolved
    except Exception:
        return name


def apply_theme(widget, theme_name: str) -> None:
    """Bezpiecznie zastosuj motyw na podanym widgetcie."""

    try:
        ui_theme.apply_theme_safe(widget, scheme=theme_name)
    except Exception:
        try:
            ui_theme.apply_theme(widget, scheme=theme_name)  # type: ignore[arg-type]
        except Exception:
            pass


def apply_before_build(widget, theme_name: str | None = None, ctx: str = "") -> None:
    # Motyw jest GLOBALNY (ttk.Style) – wolno aplikować tylko na ROOT "tk".
    # Dla każdego Toplevel (!toplevel, !toplevel2, ...) nie robimy
    # ponownego apply ani logów, bo to tylko spam i koszt UI.
    if isinstance(ctx, str) and ("!toplevel" in ctx):
        return

    # UWAGA: ta funkcja jest wołana dla KAŻDEGO Toplevel.
    # Jeśli motyw już jest w cache, to nie spamujemy logów "apply before build".
    theme = theme_name or _get_theme_from_config() or "default"
    theme = _alias_theme(theme)

    # Jeśli mamy cache (motyw już ustawiony), pomijamy głośne logi i tylko
    # przypinamy motyw lekko (tło/kolory) – bez przebudowy stylu.
    if getattr(ui_theme, "_WM_THEME_APPLIED", False):
        try:
            ui_theme.attach_theme(widget)
        except Exception:
            pass
        return

    _log(f"[WM-DBG][THEME] Wybrany motyw z config: {theme}")
    _log(f"[WM-DBG][THEME] apply before build -> {theme} ({ctx})")
    apply_theme(widget, theme)
