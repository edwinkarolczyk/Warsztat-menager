# version: 1.0
"""Tests for helpers injecting the legacy users tab into the settings panel."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import pytest

from gui_settings_users_tab import create_users_tab
from ustawienia_uzytkownicy import SettingsProfilesTab


@pytest.fixture
def root():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter not available")
    root.withdraw()
    yield root
    root.destroy()


def test_create_users_tab_adds_profiles_frame(root):
    notebook = ttk.Notebook(root)
    notebook.pack()

    frame = create_users_tab(notebook)

    assert frame is not None
    root.update_idletasks()

    tab_ids = notebook.tabs()
    assert tab_ids
    assert notebook.tab(tab_ids[-1], "text") == "Użytkownicy"

    children = frame.winfo_children()
    assert len(children) == 1
    assert isinstance(children[0], SettingsProfilesTab)


def test_create_users_tab_reuses_existing_frame(root):
    notebook = ttk.Notebook(root)
    notebook.pack()

    frame1 = create_users_tab(notebook)
    frame2 = create_users_tab(notebook)

    assert frame1 is frame2
    assert len(frame1.winfo_children()) == 1
