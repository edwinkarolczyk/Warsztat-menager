# version: 1.0
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from config_manager import ConfigManager  # [ROOT]
from services.profile_service import load_assign_tools, save_assign_tool

# [ROOT] Przypisania muszą iść do folderu ROOT ustawionego w Ustawieniach
try:
    _cfg = ConfigManager()
    DATA_PATH = Path(_cfg.path_data("zadania_przypisania.json"))
except Exception:
    # fallback awaryjny (gdy ConfigManager nie jest dostępny)
    DATA_PATH = Path("data") / "zadania_przypisania.json"

OVERRIDES_DIR = Path("data") / "profil_overrides"
ORDERS_PATH = OVERRIDES_DIR / "assign_orders.json"
TOOLS_CONTEXT = "narzedzia"


def _load_orders() -> Dict[str, List[str]]:
    if ORDERS_PATH.exists():
        try:
            with open(ORDERS_PATH, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except (OSError, json.JSONDecodeError):
            pass
    return {}


def _save_orders(data: Dict[str, List[str]]) -> None:
    OVERRIDES_DIR.mkdir(parents=True, exist_ok=True)
    with open(ORDERS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def assign(task_id: str, user: str, context: str) -> None:
    """Assign ``task_id`` in ``context`` to ``user``."""
    if context.strip().lower() == TOOLS_CONTEXT:
        save_assign_tool(task_id, user or None)
        return

    # orders → profil_overrides/assign_orders.json
    orders = _load_orders()
    if user:
        orders.setdefault(user, [])
        if task_id not in orders[user]:
            orders[user].append(task_id)
    _save_orders(orders)


def unassign(task_id: str, context: str) -> None:
    """Remove assignment for ``task_id`` in ``context``."""
    if context.strip().lower() == TOOLS_CONTEXT:
        save_assign_tool(task_id, None)
        return

    orders = _load_orders()
    for user, tasks in list(orders.items()):
        if task_id in tasks:
            tasks.remove(task_id)
        if not tasks:
            orders.pop(user, None)
    _save_orders(orders)


def list_for_user(user: str) -> List[Dict[str, Any]]:
    """Return assignments for ``user``."""
    records: List[Dict[str, Any]] = []

    # orders (override per user)
    orders = _load_orders()
    for task_id in orders.get(user, []):
        records.append({"task": task_id, "user": user, "context": "zlecenia"})

    # tools
    for task_id, assigned in load_assign_tools().items():
        if str(assigned) == user:
            records.append({"task": task_id, "user": assigned, "context": TOOLS_CONTEXT})
    return records


def list_in_context(context: str) -> List[Dict[str, Any]]:
    """Return assignments belonging to ``context``."""
    if context.strip().lower() == TOOLS_CONTEXT:
        return [
            {"task": task_id, "user": user, "context": TOOLS_CONTEXT}
            for task_id, user in load_assign_tools().items()
        ]
    if context.strip().lower() == "zlecenia":
        records: List[Dict[str, Any]] = []
        orders = _load_orders()
        for user, tasks in orders.items():
            for task_id in tasks:
                records.append({"task": task_id, "user": user, "context": "zlecenia"})
        return records
    return []


def list_all() -> List[Dict[str, Any]]:
    """Return all assignment records."""
    records: List[Dict[str, Any]] = []
    orders = _load_orders()
    for user, tasks in orders.items():
        for task_id in tasks:
            records.append({"task": task_id, "user": user, "context": "zlecenia"})
    records.extend(
        {"task": task_id, "user": user, "context": TOOLS_CONTEXT}
        for task_id, user in load_assign_tools().items()
    )
    return records


__all__ = [
    "assign",
    "unassign",
    "list_for_user",
    "list_in_context",
    "list_all",
]
