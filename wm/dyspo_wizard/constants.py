# version: 1.0
"""Constants for the Dyspozycje wizard."""

from __future__ import annotations

from typing import Dict

from wm.gui.i18n import t


def _short(label: str) -> str:
    """Return a short label for buttons based on full type name."""

    prefix = "Dyspozycja "
    if label.startswith(prefix):
        candidate = label[len(prefix) :].strip()
    else:
        candidate = label

    overrides = {
        "naprawy maszyny": "Naprawa maszyny",
        "zamówienia": "Zamówienie",
        "wewnętrzna": "Wewnętrzna",
        "narzędzi": "Narzędzie",
    }
    lowered = candidate.lower()
    if lowered in overrides:
        return overrides[lowered]
    return candidate[:1].upper() + candidate[1:]


TYPES_REGISTRY: Dict[str, Dict[str, str]] = {}


def register_type(code: str, *, label: str, step: str, button: str | None = None) -> None:
    """Register Dyspozycja type metadata."""

    TYPES_REGISTRY[code] = {
        "label": label,
        "button": button or _short(label),
        "step": step,
    }


register_type(
    "DM",
    label=t("wizard.dyspo.type.DM"),
    step="wm.dyspo_wizard.steps_dm.StepDM",
)
register_type(
    "DZ",
    label=t("wizard.dyspo.type.DZ"),
    step="wm.dyspo_wizard.steps_dz.StepDZ",
)
register_type(
    "DW",
    label=t("wizard.dyspo.type.DW"),
    step="wm.dyspo_wizard.steps_dw.StepDW",
)
register_type(
    "DN",
    label=t("wizard.dyspo.type.DN"),
    step="wm.dyspo_wizard.steps_dn.StepDN",
)


__all__ = ["TYPES_REGISTRY", "register_type"]
