# version: 1.0
import pytest
import tkinter as tk
from tkinter import ttk

import gui_panel


@pytest.fixture
def root():
    try:
        r = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter not available")
    r.withdraw()
    yield r
    r.destroy()


def test_disabled_modules_hide_buttons(root, monkeypatch):
    monkeypatch.setattr(
        gui_panel, "get_user", lambda login: {"login": login, "disabled_modules": ["narzedzia"]}
    )
    gui_panel.uruchom_panel(root, "demo", "user")
    side = root.winfo_children()[0]
    buttons = {
        w.cget("text"): w
        for w in side.winfo_children()
        if isinstance(w, ttk.Button)
    }
    assert "Narzędzia" in buttons
    assert buttons["Narzędzia"].instate(["disabled"])
    assert "Zlecenia" in buttons
    assert buttons["Zlecenia"].instate(["!disabled"])


def test_disabled_profile_module(root, monkeypatch):
    monkeypatch.setattr(
        gui_panel,
        "get_user",
        lambda login: {"login": login, "disabled_modules": ["profil"]},
    )
    gui_panel.uruchom_panel(root, "demo", "user")
    side = root.winfo_children()[0]
    buttons = {
        w.cget("text"): w
        for w in side.winfo_children()
        if isinstance(w, ttk.Button)
    }
    assert "Profil" in buttons
    assert buttons["Profil"].instate(["disabled"])
    assert "Zlecenia" in buttons
