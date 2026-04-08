# version: 1.0
"""Business logic for creating orders stored in a single JSON file."""

from __future__ import annotations

import re
import time
from typing import Any, Dict, List, Tuple

try:
    from core.settings_manager import Settings  # type: ignore
except Exception:  # pragma: no cover - konfiguracja opcjonalna
    Settings = None  # type: ignore

from core.orders_storage import load_orders, orders_file_path, save_orders

_DEFAULT_STATUSES = [
    "nowe",
    "w toku",
    "wstrzymane",
    "do odbioru",
    "zakończone",
    "anulowane",
]

_DEFAULT_REQUIRED_PER_TYPE: Dict[str, List[str]] = {
    "ZZ": ["typ", "opis", "termin", "klient"],
    "ZW": ["typ", "opis", "termin"],
    "ZM": ["typ", "opis", "termin"],
    "ZN": ["typ", "opis", "termin"],
}


def _settings() -> Any:
    if Settings is None:
        return {}
    try:
        return Settings(path="config.json", project_root=__file__)
    except Exception:
        return {}


def _statuses(cfg: Any) -> List[str]:
    try:
        statuses = cfg.get("orders.statuses")
        if isinstance(statuses, list) and statuses:
            return [str(item) for item in statuses if str(item).strip()]
    except Exception:
        pass
    return list(_DEFAULT_STATUSES)


def _required_for_type(cfg: Any, order_type: str) -> List[str]:
    order_kind = (order_type or "").upper().strip() or "ZW"
    try:
        per_type = cfg.get("orders.required_fields_per_type")
        if isinstance(per_type, dict):
            custom = per_type.get(order_kind)
            if isinstance(custom, list) and custom:
                return [str(item) for item in custom if str(item).strip()]
    except Exception:
        pass

    try:
        required = cfg.get("orders.required_fields")
        if isinstance(required, list) and required:
            return [str(item) for item in required if str(item).strip()]
    except Exception:
        pass

    return list(_DEFAULT_REQUIRED_PER_TYPE.get(order_kind, _DEFAULT_REQUIRED_PER_TYPE["ZW"]))


def _next_number(existing: List[Dict[str, Any]], prefix: str) -> str:
    """Return next sequential order number in format ``PREFIX-YYYYMM-XXX``."""

    year_month = time.strftime("%Y%m")
    pattern = re.compile(rf"^{re.escape(prefix)}-{year_month}-(\\d+)$")
    last = 0
    for item in existing:
        number = str(item.get("nr") or "")
        match = pattern.match(number)
        if not match:
            continue
        try:
            last = max(last, int(match.group(1)))
        except Exception:
            continue
    return f"{prefix}-{year_month}-{last + 1:03d}"


def validate_order(order_type: str, data: Dict[str, Any], cfg: Any | None = None) -> Tuple[bool, str]:
    required_fields = _required_for_type(cfg or {}, order_type)
    missing: List[str] = []
    for key in required_fields:
        value = data.get(key, "")
        if isinstance(value, str):
            value = value.strip()
        if value is None or value == "" or (isinstance(value, (list, dict)) and not value):
            missing.append(key)
    if missing:
        return False, "Brak wymaganych pól: " + ", ".join(missing)
    return True, ""


def create_order(order_type: str, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any] | str]:
    cfg = _settings()
    ok, message = validate_order(order_type, data, cfg)
    if not ok:
        print(f"[ORDERS][WARN] Walidacja nie przeszła: {message}")
        return False, message

    items_path = orders_file_path(cfg)
    items = load_orders(items_path)
    prefix = (order_type or "ZW").strip().upper()
    order_number = _next_number(items, prefix)
    statuses = _statuses(cfg)
    start_status = statuses[0] if statuses else "nowe"

    order = {
        "nr": order_number,
        "typ": prefix,
        "status": start_status,
        "utworzono": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    order.update(data)

    try:
        items.append(order)
        save_orders(items_path, items)
        print(f"[ORDERS][INFO] Zapisano zlecenie {order_number} → {items_path}")
        return True, order
    except Exception as exc:  # pragma: no cover - błąd zapisu jest logowany
        print(
            f"[ORDERS][ERROR] Nie udało się zapisać zlecenia: {exc} (plik={items_path})"
        )
        return False, f"Nie udało się zapisać zlecenia ({exc})"
