# version: 1.0
"""Utilities for reading tool templates.

This module provides :func:`load_templates` which reads JSON files
representing tool templates. Each template must contain a unique ``id``
field. The loader enforces a maximum of 64 templates (8×8 limit) and will
skip missing files gracefully. If duplicate ``id`` values are encountered
or the limit is exceeded a :class:`ValueError` is raised.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from config.paths import p_tools_templates
from utils_paths import tools_file

MAX_TEMPLATES = 64  # 8x8 limit


def _normalize_payload(data: Any, default_id: str) -> List[Dict[str, Any]]:
    """Convert arbitrary JSON payload to a list of template dicts."""

    if isinstance(data, dict):
        if "id" in data:
            item = dict(data)
            item.setdefault("id", default_id)
            return [item]
        normalized: List[Dict[str, Any]] = []
        for key, value in data.items():
            entry: Dict[str, Any]
            if isinstance(value, dict):
                entry = dict(value)
            else:
                entry = {"template": value}
            entry.setdefault("id", str(key))
            normalized.append(entry)
        return normalized

    if isinstance(data, list):
        normalized = []
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                continue
            entry = dict(item)
            entry.setdefault("id", f"{default_id}-{idx}")
            normalized.append(entry)
        return normalized

    return []


def load_templates(paths: Iterable[Path]) -> List[Dict[str, Any]]:
    """Load templates from ``paths``.

    Parameters
    ----------
    paths:
        An iterable of file system paths pointing to JSON files. Missing
        files are ignored.

    Returns
    -------
    list of dict
        Parsed templates.

    Raises
    ------
    ValueError
        If more than :data:`MAX_TEMPLATES` templates are loaded or
        duplicate ``id`` values are encountered.
    """
    templates: Dict[str, Dict[str, Any]] = {}
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            # Gracefully ignore missing files.
            continue
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for entry in _normalize_payload(data, path.stem):
            template_id = entry.get("id")
            if template_id is None:
                raise ValueError("template missing 'id'")
            if template_id in templates:
                raise ValueError(f"duplicate template id: {template_id}")
            templates[template_id] = entry
            if len(templates) > MAX_TEMPLATES:
                raise ValueError("too many templates (limit 64)")
    return list(templates.values())


def load_default_templates(cfg: Any | None = None) -> List[Dict[str, Any]]:
    """Load tool templates using the canonical path resolution."""

    candidates: list[Path] = []
    try:
        candidates.append(Path(p_tools_templates(cfg)))
    except Exception:
        candidates.append(Path("narzedzia/szablony_zadan.json"))

    try:
        alt = Path(tools_file(cfg or {}, "szablony_zadan.json"))
        candidates.append(alt)
    except Exception:
        pass

    seen: set[str] = set()
    existing = []
    for candidate in candidates:
        norm = candidate.resolve()
        norm_key = norm.as_posix().lower()
        if norm_key in seen:
            continue
        seen.add(norm_key)
        if norm.exists():
            existing.append(norm)
    if not existing:
        return []
    return load_templates(existing)
