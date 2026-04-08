#!/usr/bin/env python
# version: 1.0
# -*- coding: utf-8 -*-
"""Walidator konfiguracji ścieżek z config.json / config.defaults.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple

REPORT = Path("reports/settings_paths_report.md")


def load_first() -> Tuple[Dict, str | None]:
    """Return configuration data and file name (config.json preferred)."""

    for name in ("config.json", "config.defaults.json"):
        path = Path(name)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")), name
    return {}, None


def main() -> int:
    """Generate validation report for settings paths."""

    cfg, source = load_first()
    if not source:
        print("[ERROR] Brak pliku config.json / defaults.json")
        return 1

    paths = cfg.get("paths") or {}
    system = cfg.get("system") or {}

    lines = [
        f"# Raport ścieżek ({source})",
        "",
        "| Klucz | Wartość | Status |",
        "|--------|----------|---------|",
    ]

    def add(key: str, value: object, status: str = "OK") -> None:
        lines.append(f"| {key} | {value} | {status} |")

    for key in ("data_root", "logs_dir", "backup_dir"):
        value = paths.get(key)
        if value:
            add(f"paths.{key}", value)
        else:
            add(f"paths.{key}", "(domyślne)", "DEF")

    for key in ("data_root", "backup_root"):
        if key in system:
            add(f"system.{key}", system[key], "LEGACY")

    lines.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Raport zapisany → {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
