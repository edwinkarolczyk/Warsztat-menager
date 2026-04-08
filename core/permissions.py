# version: 1.0
"""Helper utilities for resolving visible UI modules for a user profile."""

from __future__ import annotations

from typing import Any, Dict, List

DEFAULT_MODULES: List[str] = [
    "panel_glowny",
    "narzedzia",
    "zlecenia",
    "magazyn",
    "maszyny",
    "profile",
    "ustawienia",
]

MINIMAL_VISIBLE_MODULES: List[str] = ["profile", "narzedzia", "maszyny"]


def resolve_modules_for_user(
    user_doc: Dict[str, Any], settings: Dict[str, Any]
) -> List[str]:
    """Return modules visible for ``user_doc`` using ``settings`` as fallback."""

    mods = user_doc.get("modules") or settings.get("ui", {}).get("modules")
    if not mods:
        # Jeżeli nic nie zdefiniowano, pokaż rozsądne minimum zamiast wszystkiego.
        return MINIMAL_VISIBLE_MODULES
    return [m for m in mods if isinstance(m, str)]


def ensure_minimal_modules_if_empty(cfg) -> None:
    """Ensure a minimal module set when profile and settings omit explicit choices."""

    try:
        user = cfg.profile.active_user_doc()
        settings = cfg.raw()
        mods = (user or {}).get("modules") or settings.get("ui", {}).get("modules")
        if not mods and user is not None:
            user["modules"] = MINIMAL_VISIBLE_MODULES[:]
            print("[WM-DBG][PERMS] Fallback minimal modules →", user["modules"])
    except Exception as exc:  # pragma: no cover - defensive diagnostics only
        print("[WM-DBG][PERMS] ensure_minimal_modules_if_empty error:", exc)


__all__ = [
    "DEFAULT_MODULES",
    "MINIMAL_VISIBLE_MODULES",
    "ensure_minimal_modules_if_empty",
    "resolve_modules_for_user",
]
