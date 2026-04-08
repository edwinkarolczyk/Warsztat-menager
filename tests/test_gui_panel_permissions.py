# version: 1.0
import pytest
import tkinter as tk
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


def _extract_button_texts(container):
    return [
        w.cget("text")
        for w in container.winfo_children()
        if hasattr(w, "cget") and "text" in w.keys()
    ]


def test_brygadzista_side_panel_has_settings_button(root, monkeypatch):
    monkeypatch.setattr(gui_panel, "get_user", lambda _login: {"disabled_modules": []})
    gui_panel.uruchom_panel(root, "demo", "brygadzista")
    side = root.winfo_children()[0]
    texts = _extract_button_texts(side)
    assert "Ustawienia" in texts


def test_admin_has_profile_button_when_menu_hidden(root, monkeypatch):
    monkeypatch.setattr(gui_panel, "get_user", lambda _login: {"disabled_modules": []})
    gui_panel.uruchom_panel(root, "demo", "admin")
    side = root.winfo_children()[0]
    texts = _extract_button_texts(side)
    assert "Profil" in texts


def test_panel_has_no_menubar(root, monkeypatch):
    monkeypatch.setattr(gui_panel, "get_user", lambda _login: {"disabled_modules": []})
    gui_panel.uruchom_panel(root, "demo", "user")
    assert not root.cget("menu")
