# version: 1.0
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from core.settings_manager import Settings

# Pełne uprawnienia RW mają: admin, magazynier, brygadzista
ALLOWED_RW_ROLES = {"admin", "administrator", "magazynier", "brygadzista"}


@dataclass
class InventoryItem:
    id: str
    name: str
    qty: float
    unit: str
    location: str = ""


def can_access_inventory(user_role: str) -> bool:
    return (user_role or "").lower() in ALLOWED_RW_ROLES


def _validate_item(raw: Dict[str, Any], idx: int) -> Tuple[Optional[InventoryItem], List[str]]:
    errs: List[str] = []

    def _req_str(key: str) -> str:
        value = str(raw.get(key, "")).strip()
        if not value:
            errs.append(f"[{idx}] '{key}' wymagane")
        return value

    def _num(key: str) -> float:
        try:
            return float(raw.get(key, 0))
        except Exception:
            errs.append(f"[{idx}] '{key}' nie jest liczbą")
            return 0.0

    item = InventoryItem(
        id=_req_str("id"),
        name=_req_str("name"),
        qty=_num("qty"),
        unit=_req_str("unit"),
        location=str(raw.get("location", "")).strip(),
    )
    if item.qty < 0:
        errs.append(f"[{idx}] 'qty' < 0")
    return (item if not errs else None), errs


def validate_inventory(data: Any) -> Tuple[List[InventoryItem], List[str]]:
    """Zwraca (lista_poprawnych, lista_błędów). Akceptuje listę słowników lub {'items': [...]}."""

    items: List[InventoryItem] = []
    errors: List[str] = []
    arr = data.get("items") if isinstance(data, dict) else data
    if not isinstance(arr, list):
        return [], ["format: oczekiwano listy lub klucza 'items' z listą"]

    for idx, raw in enumerate(arr):
        if not isinstance(raw, dict):
            errors.append(f"[{idx}] pozycja nie jest obiektem")
            continue
        item, item_errors = _validate_item(raw, idx)
        if item_errors:
            errors.extend(item_errors)
        if item:
            items.append(item)

    seen: set[str] = set()
    for item in items:
        if item.id in seen:
            errors.append(f"duplikat id: {item.id}")
        seen.add(item.id)
    return items, errors


def _inventory_path(cfg: Settings, filename: str = "magazyn.json") -> str:
    return cfg.path_data(filename)


def load_inventory(cfg: Settings) -> Dict[str, Any]:
    """Wczytuje magazyn z data/magazyn.json (lub tworzy pusty jeśli brak)."""

    path = _inventory_path(cfg)
    if not os.path.exists(path):
        return {"items": []}
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_inventory(cfg: Settings, data: Dict[str, Any], user_role: str) -> str:
    """Zapisuje magazyn po walidacji. Wymaga roli w ALLOWED_RW_ROLES. Tworzy backup."""

    if not can_access_inventory(user_role):
        raise PermissionError(
            "Brak uprawnień do zapisu magazynu (wymagany: administrator/admin/magazynier/brygadzista)."
        )
    items, errors = validate_inventory(data)
    if errors:
        raise ValueError("Błędy walidacji magazynu: " + "; ".join(errors))

    backup_dir = cfg.path_backup("magazyn")
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    inventory_path = _inventory_path(cfg)
    if os.path.exists(inventory_path):
        backup_path = os.path.join(backup_dir, f"magazyn-{timestamp}.json")
        with open(inventory_path, "r", encoding="utf-8") as src, open(
            backup_path, "w", encoding="utf-8"
        ) as dst:
            dst.write(src.read())

    os.makedirs(os.path.dirname(inventory_path) or ".", exist_ok=True)
    with open(inventory_path, "w", encoding="utf-8") as handle:
        json.dump({"items": [item.__dict__ for item in items]}, handle, ensure_ascii=False, indent=2)
    return inventory_path


def add_or_update_item(cfg: Settings, payload: Dict[str, Any], user_role: str) -> Dict[str, Any]:
    """Dodaje/aktualizuje 1 pozycję (po ID). Wymaga uprawnienia RW."""

    if not can_access_inventory(user_role):
        raise PermissionError(
            "Brak uprawnień do modyfikacji magazynu (wymagany: admin/magazynier/brygadzista)."
        )

    current = load_inventory(cfg)
    items, errors = validate_inventory(current)
    if errors:
        raise ValueError("Aktualny magazyn ma błędy: " + "; ".join(errors))

    new_item, new_errors = _validate_item(payload, idx=-1)
    if new_errors or not new_item:
        raise ValueError("Błędny payload: " + "; ".join(new_errors))

    updated = False
    out: List[Dict[str, Any]] = []
    for item in items:
        if item.id == new_item.id:
            out.append(new_item.__dict__)
            updated = True
        else:
            out.append(item.__dict__)
    if not updated:
        out.append(new_item.__dict__)

    save_inventory(cfg, {"items": out}, user_role=user_role)
    return {"updated": updated, "item": new_item.__dict__}
