# version: 1.0
"""Utilities for loading machine definitions from JSON-like structures."""
from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Sequence


def _ensure_list(data: object) -> Sequence[Mapping[str, object]]:
    """Normalize the incoming data to a sequence of machine mappings."""
    if isinstance(data, Mapping):
        machines = data.get("maszyny")
        if machines is None:
            raise ValueError("Dictionary input must contain the 'maszyny' key")
        data = machines

    if not isinstance(data, Iterable) or isinstance(data, (str, bytes)):
        raise TypeError("Machines data must be a list of mappings")

    machines_list: List[Mapping[str, object]] = list(data)
    return machines_list


def _sanitize_str(value: object, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _sanitize_int(value: object, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return default


def load_machines_from_json(data: object) -> List[Dict[str, object]]:
    """Return machines data with sanitized types.

    The function accepts either a list of mappings with machine data or a
    dictionary containing the ``"maszyny"`` key with such a list. For each
    machine the following conversions are applied:

    * ``id`` and ``nr_hali`` are converted to strings.
    * ``x`` and ``y`` are converted to integers with ``0`` as fallback.

    Parameters
    ----------
    data:
        JSON-like data structure holding machine definitions.

    Returns
    -------
    list[dict[str, object]]
        Sanitized machine definitions ready for downstream usage.
    """

    machines = _ensure_list(data)

    sanitized: List[Dict[str, object]] = []
    for machine in machines:
        if not isinstance(machine, Mapping):
            raise TypeError("Each machine entry must be a mapping")

        sanitized.append(
            {
                "id": _sanitize_str(machine.get("id")),
                "x": _sanitize_int(machine.get("x")),
                "y": _sanitize_int(machine.get("y")),
                "nr_hali": _sanitize_str(machine.get("nr_hali")),
            }
        )

    return sanitized


__all__ = ["load_machines_from_json"]
