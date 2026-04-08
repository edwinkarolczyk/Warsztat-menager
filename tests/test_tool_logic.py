# version: 1.0
from tool_data_bridge import ToolDataBridge
from tools_config_loader import get_status_names_for_type


def _sample_config():
    return {
        "collections": {
            "NN": {
                "types": [
                    {
                        "id": "NN1",
                        "name": "Narzędzie NN",
                        "aliases": ["NN"],
                        "statuses": [
                            {"name": "Nowe"},
                            {"name": "W serwisie"},
                        ],
                    }
                ]
            }
        }
    }


def test_statuses_resolve_for_name_and_identifiers():
    cfg = _sample_config()

    assert get_status_names_for_type(cfg, "NN", "Narzędzie NN") == [
        "Nowe",
        "W serwisie",
    ]
    assert get_status_names_for_type(cfg, "NN", "NN1") == ["Nowe", "W serwisie"]
    assert get_status_names_for_type(cfg, "NN", "NN") == ["Nowe", "W serwisie"]


def test_tool_bridge_uses_config_statuses_for_short_type_ids():
    bridge = ToolDataBridge(cfg_manager=None)
    bridge._definitions = _sample_config()
    bridge._index_rows = []

    assert bridge.available_statuses("NN") == ["Nowe", "W serwisie"]
