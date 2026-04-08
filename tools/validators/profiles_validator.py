#!/usr/bin/env python
# version: 1.0
# -*- coding: utf-8 -*-
"""Walidator profili użytkowników: data/profiles.json + data/user/*.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

BASE = Path("data")
REPORT = Path("reports/profiles_report.md")


def load_json(path: Path) -> Dict:
    """Load JSON file and return dictionary, or wrapper with error."""

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep full error info
        return {"__error__": str(exc)}


def main() -> int:
    """Validate profiles consistency across files."""

    profiles_file = BASE / "profiles.json"
    users_dir = BASE / "user"
    result: List[Tuple[str, object]] = []
    seen_logins: Dict[str, Dict] = {}

    main_profiles = load_json(profiles_file)
    if not isinstance(main_profiles, list):
        print("[WARN] profiles.json nie jest listą")
        result.append(("__config__", "profiles.json nie jest listą"))
        main_profiles = []

    for profile in main_profiles:
        login = profile.get("login")
        if not login:
            result.append(("brak_login", profile))
            continue
        if login in seen_logins:
            result.append(("duplikat", login))
        seen_logins[login] = profile

    for user_file in users_dir.glob("*.json"):
        user_data = load_json(user_file)
        login = user_file.stem
        if "__error__" in user_data:
            result.append((login, f"Błąd JSON: {user_data['__error__']}"))
            continue
        if login not in seen_logins:
            result.append((login, "brak w profiles.json"))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Raport profili",
        "",
        "| Login | Problem |",
        "|--------|---------|",
    ]

    if not result:
        lines.append("| (brak) | wszystko OK |")
    else:
        for login, info in result:
            lines.append(f"| {login} | {info} |")

    lines.append("")
    lines.append(f"**Liczba profili:** {len(main_profiles)}")
    lines.append(f"**Problemy:** {len(result)}")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Raport zapisany → {REPORT}")
    print(f"Znaleziono {len(result)} problemów.")
    return 0 if not result else 1


if __name__ == "__main__":
    raise SystemExit(main())
