# version: 1.0
"""Testy interfejsu Jarvisa – baner offline i integracja powiadomień."""

from __future__ import annotations

import importlib


def test_jarvis_offline_banner():
    panel_module = importlib.import_module("panel_jarvis")
    panel = panel_module.JarvisPanel()
    try:
        panel.jarvis_online = False
        panel.update_banner_state()
        assert "offline" in str(panel.banner.cget("text")).lower()
    finally:
        destroy = getattr(panel, "destroy", None)
        if callable(destroy):
            destroy()
