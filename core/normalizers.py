# version: 1.0
from typing import Any, Dict, List


def _as_list(value: Any) -> List[Dict]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in ("maszyny", "machines", "items", "narzedzia", "narzędzia"):
            items = value.get(key)
            if isinstance(items, list):
                return [row for row in items if isinstance(row, dict)]
        return [value]
    return []


def normalize_doc_to_list(data: Any) -> List[Dict]:
    """Akceptuje dict/list/None i zwraca listę słowników (bez None, bez śmieci)."""
    return _as_list(data)
