# version: 1.0
"""Helpers for synchronising inventory data with GUI widgets."""

from __future__ import annotations

from typing import Iterable, Optional

from core.inventory_manager import load_inventory
from core.settings_manager import Settings


def _resolve_columns(tree_widget) -> Iterable[str]:
    """Return configured columns for a ttk.Treeview-like widget."""

    columns = getattr(tree_widget, "columns", None)
    if columns:
        return columns
    try:
        return tree_widget["columns"]
    except Exception:  # pragma: no cover - defensive fallback
        return ()


def _map_item_to_columns(item: dict, columns: Iterable[str]) -> list[str]:
    """Map inventory item dict to Treeview column order."""

    iid = str(item.get("id", ""))
    unit = str(item.get("unit", ""))
    qty = item.get("qty", "")
    name = str(item.get("name", ""))
    location = str(item.get("location", ""))
    try:
        qty_txt = f"{float(qty):g}"
    except Exception:
        qty_txt = str(qty)
    state = f"{qty_txt} {unit}".strip()

    values: list[str] = []
    for col in columns:
        key = str(col).lower()
        if key == "id":
            values.append(iid)
        elif key in {"unit", "jm", "jednostka"}:
            values.append(unit)
        elif key in {"qty", "ilosc", "ilość", "quantity"}:
            values.append(qty_txt)
        elif key in {"name", "nazwa"}:
            values.append(name)
        elif key == "stan":
            values.append(state)
        elif key in {"location", "lokalizacja", "zadania"}:
            values.append(location)
        elif key in {"typ", "type"}:
            values.append(item.get("type", "") or unit)
        elif key in {"rozmiar", "size"}:
            values.append(item.get("size", ""))
        else:
            values.append(str(item.get(col, "")))
    return values


def apply_inventory_to_tree(tree_widget, items):
    """Populate a Treeview-like widget with inventory records."""

    if not tree_widget or not hasattr(tree_widget, "insert"):
        return

    for node in tree_widget.get_children():
        tree_widget.delete(node)

    columns = list(_resolve_columns(tree_widget))
    for item in items:
        values = _map_item_to_columns(item, columns)
        tree_widget.insert("", "end", values=values)


def refresh_inventory(tree_widget, cfg: Optional[Settings] = None) -> int:
    """Reload inventory data and apply it to a Treeview widget."""

    cfg = cfg or Settings(path="config.json", project_root=__file__)
    data = load_inventory(cfg)
    items = data.get("items", []) if isinstance(data, dict) else []
    apply_inventory_to_tree(tree_widget, items)
    return len(items)
