# version: 1.0
"""Tests for the simple GUI inventory bridge."""

from core.inventory_manager import save_inventory
from core.settings_manager import Settings
from gui_magazyn_bridge import refresh_inventory


class _DummyTree:
    def __init__(self) -> None:
        self._rows: list[list[str]] = []

    def get_children(self):
        return list(range(len(self._rows)))

    def delete(self, _node):
        if self._rows:
            self._rows.pop()

    def insert(self, *_args, **kwargs):
        self._rows.append(list(kwargs.get("values", [])))


def test_inventory_refresh(tmp_path):
    cfg = Settings(path=str(tmp_path / "config.json"), project_root=__file__)
    data = {
        "items": [
            {
                "id": "S-001",
                "name": "Śruba M8",
                "qty": 100,
                "unit": "szt",
                "location": "A1",
            },
            {
                "id": "F-010",
                "name": "Filtr",
                "qty": 2,
                "unit": "szt",
                "location": "B2",
            },
        ]
    }
    save_inventory(cfg, data, user_role="brygadzista")
    tree = _DummyTree()
    count = refresh_inventory(tree, cfg)
    assert count == 2
