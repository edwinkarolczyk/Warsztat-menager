# version: 1.0
from __future__ import annotations

import sys
import os
import re
import json
import pathlib
from datetime import datetime
from typing import Dict, List, Tuple, Set

ROOT = pathlib.Path(os.getcwd())
OUT = ROOT / "settings_duplicates_report.txt"

SCHEMA_PATH = ROOT / "settings_schema.json"
CONFIG_PATH = ROOT / "config.json"

PY_KEY_RX = re.compile(r'\b(?:get|set)\s*\(\s*["\']([^"\']+)["\']')
JSON_KEY_RX = re.compile(r'["\']key["\']\s*:\s*["\']([^"\']+)["\']')

EXCLUDE = re.compile(
    r"(?:[/\\]\.git|[/\\]\.venv|[/\\]venv|[/\\]node_modules|[/\\]dist|[/\\]build|[/\\]__pycache__)",
    re.IGNORECASE,
)
EXTS_SCAN = {".py", ".json"}


def iter_files(root: pathlib.Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS_SCAN and not EXCLUDE.search(str(p.parent)):
            yield p


def flatten_cfg(obj: Dict, prefix="") -> Dict[str, object]:
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                out.update(flatten_cfg(v, key))
            else:
                out[key] = v
    return out


def load_schema_keys() -> Tuple[Set[str], List[Tuple[str, str, str]]]:
    keys: Set[str] = set()
    defs: List[Tuple[str, str, str]] = []
    if not SCHEMA_PATH.exists():
        return keys, defs
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    tabs = data.get("tabs") or data
    for tab in tabs:
        tname = tab.get("tab") or tab.get("name") or ""
        for grp in (tab.get("groups") or []):
            gname = grp.get("label") or ""
            for fld in (grp.get("fields") or []):
                key = fld.get("key")
                if key:
                    defs.append((key, tname, gname))
                    keys.add(key)
    return keys, defs


def scan_code_references() -> Set[str]:
    refs: Set[str] = set()
    for f in iter_files(ROOT):
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in PY_KEY_RX.finditer(text):
            refs.add(m.group(1))
        for m in JSON_KEY_RX.finditer(text):
            refs.add(m.group(1))
    return refs


def main():
    print(f"[SCAN] CWD: {ROOT}")
    problems = 0
    schema_keys, schema_defs = load_schema_keys()

    # 1) Duplikaty w schema
    dup_map: Dict[str, List[Tuple[str, str]]] = {}
    for key, tab, grp in schema_defs:
        dup_map.setdefault(key, []).append((tab, grp))
    duplicates = {k: v for k, v in dup_map.items() if len(v) > 1}

    # 2) Odwołania w kodzie do nieistniejących kluczy
    code_refs = scan_code_references()
    missing_in_schema = sorted([k for k in code_refs if k not in schema_keys])

    # 3) Klucze w config.json nieobecne w schema
    cfg_unknown: List[str] = []
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            flat = flatten_cfg(cfg)
            for k in flat.keys():
                if k not in schema_keys:
                    cfg_unknown.append(k)
        except Exception:
            pass
    cfg_unknown = sorted(set(cfg_unknown))

    # ZAWSZE zapisz raport
    OUT.write_text("", encoding="utf-8")
    with OUT.open("w", encoding="utf-8") as f:
        f.write(f"=== SETTINGS SCAN === {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        f.write(f"CWD/Repo: {ROOT}\n\n")
        if duplicates:
            f.write("DUPLIKATY KLUCZY W settings_schema.json:\n")
            for k, items in duplicates.items():
                places = "; ".join([f"[{t}/{g}]" for t, g in items])
                f.write(f"- {k}: {places}\n")
            f.write("\n")
        else:
            f.write("DUPLIKATY KLUCZY W settings_schema.json: BRAK\n\n")

        if missing_in_schema:
            f.write("ODWOŁANIA W KODZIE DO KLUCZY SPOZA SCHEMATU:\n")
            for k in missing_in_schema:
                f.write(f"- {k}\n")
            f.write("\n")
        else:
            f.write("ODWOŁANIA W KODZIE DO KLUCZY SPOZA SCHEMATU: BRAK\n\n")

        if cfg_unknown:
            f.write("KLUCZE W config.json NIEOBECNE W SCHEMACIE (do weryfikacji):\n")
            for k in cfg_unknown:
                f.write(f"- {k}\n")
            f.write("\n")
        else:
            f.write("KLUCZE W config.json NIEOBECNE W SCHEMACIE: BRAK\n\n")

    if duplicates or missing_in_schema or cfg_unknown:
        print(f"[SCAN] ⚠️  Wykryto problemy. Raport: {OUT}")
        return 1
    print(f"[SCAN] ✅  Ustawienia OK. Raport: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
