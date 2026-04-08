#!/usr/bin/env python
# version: 1.0
# -*- coding: utf-8 -*-
"""Walidator struktury plików data/narzedzia/*.json."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List

DATA_DIR = Path("data/narzedzia")
REPORT = Path("reports/tools_schema_report.md")

REQUIRED_KEYS = [
    "numer",
    "nazwa",
    "typ",
    "status",
    "opis",
    "pracownik",
    "zadania",
    "data_dodania",
    "tryb",
    "interwencje",
]


def validate_one(path: Path) -> List[str]:
    """Validate single tool file and return list of errors."""

    errors: List[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - log exact error
        return [f"Niepoprawny JSON: {exc}"]

    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"Brak pola: {key}")

    if "numer" in data and data["numer"] != path.stem:
        errors.append(f"numer ≠ nazwa pliku ({data['numer']} != {path.stem})")

    if "zadania" in data and not isinstance(data["zadania"], list):
        errors.append("zadania nie jest listą")

    if "interwencje" in data and not isinstance(data["interwencje"], list):
        errors.append("interwencje nie jest listą")

    return errors


def main() -> int:
    """Generate report for all tools files."""

    paths = [p for p in DATA_DIR.glob("*.json") if p.is_file()]
    os.makedirs(REPORT.parent, exist_ok=True)
    total = 0
    ok = 0
    lines = [
        "# Raport walidacji narzędzi",
        "",
        "| Plik | Status | Błędy |",
        "|------|--------|--------|",
    ]

    for tool_path in sorted(paths):
        total += 1
        errors = validate_one(tool_path)
        if errors:
            lines.append(f"| {tool_path.name} | ❌ | {'; '.join(errors)} |")
        else:
            ok += 1
            lines.append(f"| {tool_path.name} | ✅ |  |")

    lines.append("")
    lines.append(f"**Podsumowanie:** {ok}/{total} poprawnych plików.")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Raport zapisany → {REPORT}")
    print(f"Plików: {total}, OK: {ok}, Błędnych: {total - ok}")
    return 0 if total == ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
