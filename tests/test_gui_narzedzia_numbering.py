# version: 1.0
import gui_narzedzia


def test_next_free_in_range_accepts_string_bounds(monkeypatch):
    monkeypatch.setattr(
        gui_narzedzia,
        "_existing_numbers",
        lambda: {"001", "002"},
    )

    assert gui_narzedzia._next_free_in_range("001", "003") == "003"


def test_next_free_in_range_invalid_or_reversed_bounds(monkeypatch):
    monkeypatch.setattr(gui_narzedzia, "_existing_numbers", lambda: set())

    assert gui_narzedzia._next_free_in_range(10, 5) is None
    assert gui_narzedzia._next_free_in_range("abc", "xyz") is None


def test_next_free_in_range_clamps_start(monkeypatch):
    monkeypatch.setattr(gui_narzedzia, "_existing_numbers", lambda: set())

    assert gui_narzedzia._next_free_in_range(-5, 2) == "001"
