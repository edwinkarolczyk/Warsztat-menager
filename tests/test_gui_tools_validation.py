# version: 1.0
import json

from gui_tools import _validate_tool_payload


STATUSES = {"NN": ["Projekt", "Wykonanie", "Składanie"]}


def _write_statuses(base_dir):
    path = base_dir / "statusy_narzedzi.json"
    path.write_text(json.dumps(STATUSES, indent=2), encoding="utf-8")


def test_validate_tool_payload_blocks_non_adjacent_status_change(tmp_path):
    _write_statuses(tmp_path)

    data = {"id": "001", "nazwa": "Narzędzie", "typ": "NN", "status": "Składanie"}

    is_valid, reason = _validate_tool_payload(
        data, str(tmp_path), 1, previous_status="Projekt"
    )

    assert not is_valid
    assert "statusu" in reason.lower()
    assert "sąsiednie" in reason.lower()


def test_validate_tool_payload_allows_adjacent_status_change(tmp_path):
    _write_statuses(tmp_path)

    data = {"id": "001", "nazwa": "Narzędzie", "typ": "NN", "status": "Wykonanie"}

    is_valid, reason = _validate_tool_payload(
        data, str(tmp_path), 1, previous_status="Projekt"
    )

    assert is_valid, reason
