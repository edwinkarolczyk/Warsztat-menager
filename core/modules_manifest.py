# version: 1.0
"""Definicja listy modułów aplikacji wykorzystywana w testach i narzędziach."""

from __future__ import annotations

modules: list[str] = [
    "ustawienia",
    "profile",
    "panel_glowny",
    "narzedzia",
    "magazyn",
    "zlecenia",
    "maszyny",
    "jarvis",
]

__all__ = ["modules"]
