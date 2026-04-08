# version: 1.0
"""Regression tests for Jarvis notifications refresh and persistence."""
import json
import os
from importlib import reload

import pytest
import tkinter as tk

import core.jarvis_engine as jarvis
import gui_jarvis_panel

if not os.environ.get("DISPLAY"):
    pytest.skip("Środowisko graficzne nie jest dostępne", allow_module_level=True)


class _DummyConfig:
    def __init__(self, refresh_ms: int) -> None:
        self._refresh_ms = refresh_ms

    def get(self, key: str, default=None):  # noqa: D401 - simple proxy for ConfigManager.get
        if key == "jarvis.notify.refresh_ms":
            return self._refresh_ms
        return default


def test_jarvis_notify_refresh_and_persistence(tmp_path, monkeypatch):
    target = tmp_path / "jarvis_notifications.json"
    monkeypatch.setenv("WM_JARVIS_NOTIFICATIONS", str(target))

    reload(jarvis)

    jarvis.notify("alert", "Test komunikat", level=4)

    assert target.exists()
    persisted = json.loads(target.read_text(encoding="utf-8"))
    assert isinstance(persisted, list)
    assert persisted[-1]["message"] == "Test komunikat"
    assert jarvis.get_notifications()[-1]["message"] == "Test komunikat"

    monkeypatch.setattr("config_manager.ConfigManager", lambda: _DummyConfig(1234))
    reload(gui_jarvis_panel)

    root = tk.Tk()
    root.withdraw()
    try:
        panel = gui_jarvis_panel.JarvisPanel(root)
        if panel._notifications_job is not None:
            panel.after_cancel(panel._notifications_job)
        calls: list[int] = []

        def fake_after(delay: int, callback):
            calls.append(delay)
            return "job-1"

        panel.after = fake_after  # type: ignore[assignment]
        panel.refresh_notifications()
        assert calls[-1] == 1234

        panel.notifications.configure(state="normal")
        content = panel.notifications.get("1.0", "end").strip()
        panel.notifications.configure(state="disabled")
        assert "Test komunikat" in content
    finally:
        root.destroy()


def test_jarvis_status_updates(tmp_path, monkeypatch):
    target = tmp_path / "jarvis_notifications.json"
    monkeypatch.setenv("WM_JARVIS_NOTIFICATIONS", str(target))

    reload(jarvis)

    jarvis.notify("status", "Analiza zakończona", level=1)

    status_path = target.with_name("jarvis_status.json")
    assert status_path.exists()
    persisted = json.loads(status_path.read_text(encoding="utf-8"))
    assert persisted.get("offline") is False

    jarvis.notify("fallback", "Przełączono na tryb offline (test)", level=3)

    snapshot = jarvis.get_status()
    assert snapshot.get("offline") is True
    reason = snapshot.get("offline_reason") or ""
    assert "offline" in reason.lower()
