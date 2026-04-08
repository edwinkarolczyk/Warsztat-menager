# version: 1.0
"""
Helpery do trybu narzędzi (NN/SN) i walidacji numerów.
Nie zmieniają istniejącej bazy – tylko pomagają w GUI.
"""
from __future__ import annotations

from typing import Optional, Tuple


def infer_mode_from_id(tool_id: str | int) -> str:
    """
    Ustala tryb na podstawie numeru, gdy brak pola 'mode'.
    Zasada: <500 → 'NN', >=500 → 'SN'
    """
    try:
        n = int(str(tool_id).lstrip("0") or "0")
    except Exception:
        n = 0
    return "NN" if 1 <= n <= 499 else "SN"


def get_tool_mode(tool: dict) -> str:
    """
    Zwraca tryb narzędzia, preferując pola jawne (mode/tryb) nad inferencją.
    """
    candidates = (
        tool.get("mode"),
        tool.get("tryb"),
        tool.get("class"),
        tool.get("kategoria"),
    )
    for raw in candidates:
        val = str(raw or "").strip().upper()
        if val in {"NN", "SN"}:
            return val
        if val in {"NOWE", "STARE"}:
            return "NN" if val == "NOWE" else "SN"
    return infer_mode_from_id(
        tool.get("id")
        or tool.get("nr")
        or tool.get("numer")
        or tool.get("number")
        or 0
    )


def validate_number(
    nr: int,
    mode: str,
    *,
    is_new: bool,
    keep_number: bool,
) -> Tuple[bool, Optional[str]]:
    """
    Walidacja numeru przy tworzeniu/edycji z obsługą zachowania numeru.
    Zasady:
      - przy NOWYM obiekcie trzymamy widełki NN:001–499, SN:500–1000;
      - przy EDISJI jeśli keep_number=True → akceptuj 001–1000 bez względu na tryb;
      - przy EDISJI gdy numer zmieniany (keep_number=False) → widełki jak wyżej.
    """
    mode = (mode or "").upper()
    if is_new:
        if mode == "NN" and not (1 <= nr <= 499):
            return False, "NN: dozwolone numery 001–499."
        if mode == "SN" and not (500 <= nr <= 1000):
            return False, "SN: dozwolone numery 500–1000."
        return True, None
    if keep_number:
        if not (1 <= nr <= 1000):
            return False, "Dozwolone numery 001–1000."
        return True, None
    # edycja + zmiana numeru
    if mode == "NN" and not (1 <= nr <= 499):
        return False, "NN: dozwolone numery 001–499."
    if mode == "SN" and not (500 <= nr <= 1000):
        return False, "SN: dozwolone numery 500–1000."
    return True, None
