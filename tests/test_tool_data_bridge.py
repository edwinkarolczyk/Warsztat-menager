# version: 1.0
import json

import pytest

from tool_data_bridge import ToolDataBridge


# Testy warstwy pośredniej opartej o stabilny ToolDataBridge.
def test_transition_sequence_allows_any_defined_status_without_custom_mapping():
    bridge = ToolDataBridge(cfg_manager=None)
    bridge._definitions = {
        "collections": {
            "NN": {
                "types": [
                    {
                        "name": "FORM", 
                        "statuses": [
                            {"name": "status1"},
                            {"name": "status2"},
                            {"name": "status3"},
                        ],
                    }
                ]
            }
        }
    }

    assert bridge.is_transition_allowed("status1", "status2", "FORM")
    assert bridge.is_transition_allowed("status2", "status1", "FORM")
    assert bridge.is_transition_allowed("status1", "status3", "FORM")


def test_transition_custom_mapping_overrides_sequence():
    bridge = ToolDataBridge(cfg_manager=None)
    bridge._definitions = {"transitions": {"draft": ["archived"]}}

    assert bridge.is_transition_allowed("draft", "archived", None)
    assert not bridge.is_transition_allowed("draft", "active", None)


def test_detail_binding_validation(tmp_path):
    catalog_path = tmp_path / "katalog_detal.json"
    catalog_path.write_text(json.dumps([{"id": "DET-1"}, {"id": "DET-2"}]), encoding="utf-8")

    bridge = ToolDataBridge(cfg_manager=None)
    bridge._detail_catalog_path_override = str(catalog_path)
    bridge._detail_catalog = None

    bridge.validate_detail_binding("DET-1")

    with pytest.raises(ValueError):
        bridge.validate_detail_binding("UNKNOWN-DETAL")
