# version: 1.0
"""Simple translation helper for the modern GUI modules."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict


@lru_cache(maxsize=1)
def _load_strings() -> Dict[str, str]:
    path = Path(__file__).with_name("strings_pl.json")
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def t(key: str) -> str:
    """Translate ``key`` into Polish text."""

    return _load_strings().get(key, key)


__all__ = ["t"]
