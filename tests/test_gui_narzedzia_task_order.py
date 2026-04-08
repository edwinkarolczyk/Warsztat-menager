# version: 1.0
import gui_narzedzia as gn


def test_pending_tasks_before_detects_unfinished_priorities():
    tasks = [
        {"tytul": "A", "done": True},
        {"tytul": "B", "done": False},
        {"tytul": "C", "done": False},
    ]

    result = gn._pending_tasks_before(tasks, 2)

    assert result == [(1, "B")]


def test_build_skip_note_includes_comment_and_positions():
    skipped = [(0, "A"), (2, "C")]

    note = gn._build_skip_note("Test", skipped, "brak części")

    assert "Test" in note
    assert "1. A" in note and "3. C" in note
    assert "brak części" in note


def test_build_skip_note_handles_missing_title():
    note = gn._build_skip_note("", [], "")

    assert "bez tytułu" in note
