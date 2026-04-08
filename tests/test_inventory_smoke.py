# version: 1.0
from core.settings_manager import Settings
from core.inventory_manager import (
    validate_inventory,
    save_inventory,
    load_inventory,
    add_or_update_item,
    can_access_inventory,
)


def test_inventory_validate_and_rbac(tmp_path):
    cfg = Settings(path=str(tmp_path / "config.json"), project_root=__file__)
    good = {
        "items": [
            {"id": "S-001", "name": "Śruba M8", "qty": 100, "unit": "szt", "location": "A1"},
            {"id": "F-010", "name": "Filtr", "qty": 2, "unit": "szt", "location": "B2"},
        ]
    }
    ok_items, ok_errors = validate_inventory(good)
    assert not ok_errors and len(ok_items) == 2

    assert can_access_inventory("brygadzista") is True

    save_path = save_inventory(cfg, good, user_role="brygadzista")
    assert save_path.endswith("magazyn.json")
    data2 = load_inventory(cfg)
    assert data2.get("items") and len(data2["items"]) == 2

    result = add_or_update_item(
        cfg,
        {"id": "S-001", "name": "Śruba M8", "qty": 120, "unit": "szt", "location": "A1"},
        user_role="brygadzista",
    )
    assert result["updated"] is True
    data3 = load_inventory(cfg)
    s1 = [x for x in data3["items"] if x["id"] == "S-001"][0]
    assert float(s1["qty"]) == 120.0
