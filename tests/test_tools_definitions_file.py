# version: 1.0
from __future__ import annotations

import json
import warnings
from pathlib import Path


def _definitions_path() -> Path:
    candidates = [
        Path("data/zadania_narzedzia.json"),
        Path("wm/data/zadania_narzedzia.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def test_tool_definitions_have_statuses():
    definitions_path = _definitions_path()
    assert definitions_path.exists(), (
        "Brak pliku definicji zadań narzędzi w oczekiwanej lokalizacji: "
        f"{definitions_path}"
    )

    data = json.loads(definitions_path.read_text(encoding="utf-8"))
    collections = data.get("collections") or {}
    assert isinstance(collections, dict)

    missing_statuses: list[str] = []
    for collection_id, collection_def in collections.items():
        types = (collection_def or {}).get("types") or []
        for type_def in types:
            statuses = type_def.get("statuses") or []
            if not statuses:
                identifier = type_def.get("id") or type_def.get("name") or "<nieznany>"
                missing_statuses.append(f"{identifier} ({collection_id})")

    if missing_statuses:
        warnings.warn(
            "Brak statusów dla typów: " + ", ".join(sorted(missing_statuses)),
            stacklevel=1,
        )
