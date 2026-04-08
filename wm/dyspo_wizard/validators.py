# version: 1.0
"""Validation helpers for Dyspozycje wizard."""

from __future__ import annotations

from typing import Dict, Iterable, List

from wm.gui.i18n import t
from wm.settings.util import get_conf


def validate_required(
    data: Dict[str, object],
    typ: str,
    conf: Dict[str, object] | None = None,
) -> List[str]:
    """Validate mandatory fields based on configuration."""

    cfg = conf or get_conf()
    required = ((cfg.get("dyspo") or {}).get("required") or {})
    errors: List[str] = []
    if required.get("machine_id") and not data.get("machine_id"):
        errors.append(t("wizard.dyspo.error.machine_id"))
    if required.get("tool_id") and not data.get("tool_id"):
        errors.append(t("wizard.dyspo.error.tool_id"))
    if required.get("at_least_one_item"):
        items = data.get("items")
        if not _has_items(items):
            errors.append(t("wizard.dyspo.error.items"))
    return errors


def _has_items(items: object) -> bool:
    if isinstance(items, dict):
        return bool(items)
    if isinstance(items, Iterable) and not isinstance(items, (str, bytes)):
        return any(bool(item) for item in items)
    return bool(items)


__all__ = ["validate_required"]
