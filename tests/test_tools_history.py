# version: 1.0
import json
from pathlib import Path

import pytest

import narzedzia_history
from narzedzia_history import append_tool_history


def test_append_tool_history_jsonl(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(narzedzia_history, "TOOL_HISTORY_DIR", tmp_path)
    entry1 = {"tool": "a", "action": "add"}
    entry2 = {"tool": "b", "action": "remove"}
    append_tool_history("test", "user", "create", payload=entry1)
    append_tool_history("test", "user", "create", payload=entry2)
    log_path = tmp_path / "test.jsonl"
    lines = log_path.read_text(encoding="utf-8").splitlines()
    data1 = json.loads(lines[-2])
    data2 = json.loads(lines[-1])
    assert data1["details"]["payload"]["tool"] == entry1["tool"]
    assert data2["details"]["payload"]["tool"] == entry2["tool"]


def test_append_tool_history_skips_duplicates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(narzedzia_history, "TOOL_HISTORY_DIR", tmp_path)
    append_tool_history("T005", "user", "edit", source="NN→SN")
    append_tool_history("T005", "user", "edit", source="NN→SN")

    log_path = tmp_path / "T005.jsonl"
    lines = [line for line in log_path.read_text(encoding="utf-8").splitlines() if line]

    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["action"] == "EDIT"
    assert payload["details"]["source"] == "NN→SN"
