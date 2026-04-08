#!/usr/bin/env python
# version: 1.0
# -*- coding: utf-8 -*-
"""
Importer narzędzi z Excela → osobne JSON-y (data/narzedzia/*.json).

Zgodny z: docs/narzedzia_json_structure_example.md

WYMAGANIA:
  pip install pandas openpyxl
"""

from __future__ import annotations
import argparse
import copy
import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd


def _norm(s: str) -> str:
    if s is None:
        return ""
    s = str(s)
    repl = {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ó": "o",
        "ś": "s",
        "ź": "z",
        "ż": "z",
    }
    t = s.strip().lower()
    for key, value in repl.items():
        t = t.replace(key, value)
    t = re.sub(r"\s+", " ", t)
    return t


MAGIC_NUMER_HEADERS = ["nr", "numer", "nr narzedzia", "nr_narzedzia"]
MAGIC_NAZWA_HEADERS = ["nazwa", "opis", "kolumna3"]

DEFAULT_TASKS = [
    {
        "tytul": "ostrzenie stempla",
        "done": False,
        "by": "",
        "ts_done": "",
        "assigned_to": None,
        "source": "own"
    },
    {
        "tytul": "regeneracja matrycy",
        "done": False,
        "by": "",
        "ts_done": "",
        "assigned_to": None,
        "source": "own"
    }
]


def _guess_column(columns, candidates):
    cols_norm = {_norm(c): c for c in columns}
    for cand in candidates:
        if cand in cols_norm:
            return cols_norm[cand]
    return None


def _load_tasks(tasks_json_path: str | None):
    if not tasks_json_path:
        return DEFAULT_TASKS
    p = Path(tasks_json_path)
    if p.exists():
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        tasks = []
        if isinstance(data, list):
            for el in data:
                if isinstance(el, str):
                    tasks.append({
                        "tytul": el,
                        "done": False, "by": "", "ts_done": "",
                        "assigned_to": None, "source": "own"
                    })
                elif isinstance(el, dict):
                    t = {
                        "tytul": el.get("tytul") or el.get("title") or "",
                        "done": bool(el.get("done", False)),
                        "by": el.get("by", ""),
                        "ts_done": el.get("ts_done", ""),
                        "assigned_to": el.get("assigned_to"),
                        "source": el.get("source", "own"),
                    }
                    tasks.append(t)
        return tasks or DEFAULT_TASKS
    return DEFAULT_TASKS


def main():
    ap = argparse.ArgumentParser(
        description="Kreator narzędzi z Excela → JSONy",
    )
    ap.add_argument(
        "--input",
        required=True,
        help="Ścieżka do pliku .xlsx/.xlsm/.xls",
    )
    ap.add_argument(
        "--sheet",
        default=None,
        help="Nazwa arkusza (domyślnie pierwszy)",
    )
    ap.add_argument(
        "--data-root",
        default="data",
        help="Katalog danych (korzeń)",
    )
    ap.add_argument(
        "--out-subdir",
        default="narzedzia",
        help="Podkatalog na pliki narzędzi",
    )
    ap.add_argument(
        "--col-numer",
        default=None,
        help="Nazwa kolumny z numerem",
    )
    ap.add_argument(
        "--col-nazwa",
        default=None,
        help="Nazwa kolumny z nazwą/opisem",
    )
    ap.add_argument(
        "--pad",
        type=int,
        default=0,
        help="Zero-padding numeru (np. 3 → 001)",
    )
    ap.add_argument("--typ-default", default="Wykrawające")
    ap.add_argument("--status-default", default="sprawne")
    ap.add_argument("--pracownik-default", default="edwin")
    ap.add_argument("--tryb-default", default="STARE")
    ap.add_argument(
        "--tasks-json",
        default=None,
        help="Opcjonalnie: plik z listą zadań",
    )
    ap.add_argument(
        "--mode",
        choices=["skip", "overwrite"],
        default="skip",
        help="Zachowanie, jeśli plik istnieje",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Bez zapisu plików",
    )
    args = ap.parse_args()

    xls_path = Path(args.input)
    if not xls_path.exists():
        raise SystemExit(f"[ERROR] Brak pliku: {xls_path}")

    out_dir = Path(args.data_root) / args.out_subdir
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        df = pd.read_excel(xls_path, sheet_name=args.sheet)
    except Exception as e:
        raise SystemExit(f"[ERROR] Nie mogę wczytać Excela: {e}")

    if df.empty:
        raise SystemExit("[WARN] Pusty arkusz — brak danych do przetworzenia.")

    numer_col = args.col_numer or _guess_column(
        df.columns,
        MAGIC_NUMER_HEADERS,
    )
    nazwa_col = args.col_nazwa or _guess_column(
        df.columns,
        MAGIC_NAZWA_HEADERS,
    )

    if not numer_col:
        raise SystemExit(
            "[ERROR] Nie znaleziono kolumny z numerem (użyj --col-numer)."
        )
    if not nazwa_col:
        print(
            "[WARN] Nie znaleziono kolumny nazwy/opisu — użyję kolumny numeru."
        )
        nazwa_col = numer_col

    tasks_template = _load_tasks(args.tasks_json)
    created, skipped, overwritten = 0, 0, 0

    for _, row in df.iterrows():
        raw_nr = row.get(numer_col)
        raw_name = row.get(nazwa_col)
        if pd.isna(raw_nr):
            continue

        nr_str = str(raw_nr).strip()
        nr_str = re.sub(r"\.0+$", "", nr_str)  # np. 501.0 → 501

        if _norm(nr_str) in ("nr", "nr narzedzia", "numer"):
            continue

        if args.pad > 0 and nr_str.isdigit():
            nr_for_filename = nr_str.zfill(args.pad)
        else:
            nr_for_filename = nr_str

        nazwa = "" if pd.isna(raw_name) else str(raw_name).strip()
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M")

        tool = {
            "numer": nr_for_filename,
            "nazwa": nazwa or f"Narzędzie {nr_for_filename}",
            "typ": args.typ_default,
            "status": args.status_default,
            "opis": "",
            "pracownik": args.pracownik_default,
            "zadania": copy.deepcopy(tasks_template),
            "data_dodania": now_ts,
            "tryb": args.tryb_default,
            "interwencje": []
        }

        out_file = out_dir / f"{nr_for_filename}.json"
        if out_file.exists():
            if args.mode == "skip":
                skipped += 1
                print(f"[SKIP] {out_file.name} już istnieje")
                continue
            else:
                overwritten += 1

        if not args.dry_run:
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with out_file.open("w", encoding="utf-8") as f:
                json.dump(tool, f, ensure_ascii=False, indent=2)

        print(f"[OK]  {out_file}")
        created += 1

    print("\n=== PODSUMOWANIE ===")
    print(f"Utworzono : {created}")
    print(f"Pominięto : {skipped}")
    print(f"Nadpisano : {overwritten}")
    print(f"Wyjście   : {out_dir.resolve()}")


if __name__ == "__main__":
    main()
