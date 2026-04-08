#!/usr/bin/env python
# version: 1.0
# -*- coding: utf-8 -*-
"""
Buduje indeks narzędzi na podstawie plików data/narzedzia/*.json

Tworzy dwa pliki:
  1) data/narzedzia/narzedzia.json         ← struktura: {"narzedzia":[ {...}, ... ]}
  2) data/tools_index.json                 ← prostszy indeks (lista skrócona)

To NIE nadpisuje pojedynczych plików narzędzi.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(".")
TOOLS_DIR = ROOT / "data" / "narzedzia"
OUT_NARZEDZIA = TOOLS_DIR / "narzedzia.json"
OUT_INDEX = ROOT / "data" / "tools_index.json"

def _safe_read(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    if not TOOLS_DIR.exists():
        print(f"[ERROR] Brak katalogu: {TOOLS_DIR}")
        return 2

    items = []
    short = []
    for f in sorted(TOOLS_DIR.glob("*.json")):
        if f.name.lower() == "narzedzia.json":
            continue
        obj = _safe_read(f)
        if not isinstance(obj, dict):
            print(f"[WARN] Pomijam niepoprawny: {f.name}")
            continue
        # Upewnij się, że numer zgadza się z nazwą pliku
        numer = str(obj.get("numer") or f.stem).strip()
        if numer != f.stem:
            obj["numer"] = f.stem
        items.append(obj)
        short.append({
            "numer": obj.get("numer", f.stem),
            "nazwa": obj.get("nazwa", f"Narzedzie {f.stem}"),
            "typ": obj.get("typ", ""),
            "status": obj.get("status", "")
        })

    # 1) pełny indeks (kompatybilny z obsługą listy/dict w WM)
    OUT_NARZEDZIA.parent.mkdir(parents=True, exist_ok=True)
    OUT_NARZEDZIA.write_text(
        json.dumps({"narzedzia": items}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[OK] Zapisano {OUT_NARZEDZIA} (pozycji: {len(items)})")

    # 2) indeks skrócony (jeśli gdzieś jest używany)
    OUT_INDEX.parent.mkdir(parents=True, exist_ok=True)
    OUT_INDEX.write_text(
        json.dumps(short, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[OK] Zapisano {OUT_INDEX} (pozycji: {len(short)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
