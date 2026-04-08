# version: 1.0
"""Utility helpers for interacting with the settings storage."""

from __future__ import annotations

import copy
import datetime as _dt
import json
import re
from pathlib import Path
from typing import Any, Dict

CONFIG_PATH = Path("config.json")
DEFAULTS_PATH = Path("config.defaults.json")


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def get_conf() -> Dict[str, Any]:
    """Return configuration merged with defaults."""

    defaults = _load_json(DEFAULTS_PATH)
    current = _load_json(CONFIG_PATH)
    merged = _deep_merge(defaults, current)
    merged.setdefault("dyspo", {})
    dyspo = merged["dyspo"]
    dyspo.setdefault("enabled_types", ["DM", "DZ", "DW", "DN"])
    dyspo.setdefault("numbering", {})
    for code in ("DM", "DZ", "DW", "DN"):
        dyspo["numbering"].setdefault(
            code,
            {"pattern": f"{code}-{{YYYY}}-{{####}}", "counter": 1},
        )
    dyspo.setdefault("flow", "simple")
    dyspo.setdefault(
        "required",
        {
            "machine_id": True,
            "tool_id": False,
            "at_least_one_item": True,
        },
    )
    dyspo.setdefault("shortcuts", {}).setdefault("ctrlD", True)
    return merged


def save_conf(conf: Dict[str, Any]) -> None:
    """Persist configuration to ``config.json`` with UTF-8 encoding."""

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as handle:
        json.dump(conf, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


def preview_number(pattern: str, code: str, counter: int) -> str:
    """Render a sample number based on ``pattern`` and ``counter``."""

    if not pattern:
        pattern = f"{code}-{{YYYY}}-{{####}}"
    now = _dt.datetime.now()
    mapping = {
        "YYYY": f"{now.year:04d}",
        "YY": f"{now.year % 100:02d}",
        "MM": f"{now.month:02d}",
        "DD": f"{now.day:02d}",
        "CODE": code,
        "code": code,
    }

    def _replace(match: re.Match[str]) -> str:
        token = match.group(1)
        if not token:
            return match.group(0)
        if set(token) == {"#"}:
            width = len(token)
            return str(max(counter, 0)).zfill(width)
        return mapping.get(token, match.group(0))

    return _PLACEHOLDER_RE.sub(_replace, pattern)
