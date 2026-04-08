# version: 1.0
# -*- coding: utf-8 -*-
"""
Importer narzędzi z pliku Excel do formatu JSON WM: <root>/data/narzedzia/<nr>.json
Użycie z GUI Ustawienia→Narzędzia: run_via_gui(app_state)
Nie modyfikuje kodu WM poza zapisaniem plików JSON w <root>.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import pandas as pd  # type: ignore
except Exception:  # brak zależności – obsłużymy komunikatem w GUI
    pd = None  # type: ignore

def _sanitize_filename(s: str) -> str:
    s = str(s).strip()
    return re.sub(r'[\\/:*?"<>|]', "_", s)

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def _clean_cell(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    lowered = text.lower()
    if lowered in {"nan", "none", "null"}:
        return ""
    return text


def _row_to_tool(row: Dict[str, Any], lp: int) -> Dict[str, Any]:
    """
    Mapowanie domyślne (case-insensitive):
      Nr/Numer/Id -> numer (nazwa pliku)
      Nazwa       -> nazwa
      Opis        -> opis
      Zdjecie/„Zdjęcie” -> zdjecie (opcjonalnie)
    Pozostałe kolumny trafiają do meta.
    """
    lowered = {str(k).strip().lower(): v for k, v in row.items()}

    numer_value = _clean_cell(
        lowered.get("nr") or lowered.get("numer") or lowered.get("id")
    )
    missing_numer = not numer_value
    numer = numer_value
    if missing_numer:
        fallback_from_name = _clean_cell(lowered.get("nazwa"))
        if fallback_from_name:
            numer_candidate = _sanitize_filename(fallback_from_name)
            numer = numer_candidate or f"auto_{lp}"
        else:
            numer = f"auto_{lp}"

    nazwa_value = _clean_cell(lowered.get("nazwa"))
    missing_nazwa = not nazwa_value
    nazwa = nazwa_value or "bez nazwy"

    opis = _clean_cell(lowered.get("opis"))
    zdjecie = _clean_cell(lowered.get("zdjecie") or lowered.get("zdjęcie"))

    meta: Dict[str, Any] = {}
    for k, v in lowered.items():
        if k in ("nr", "numer", "id", "nazwa", "opis", "zdjecie", "zdjęcie"):
            continue
        if v is None or (
            hasattr(v, "__eq__") and str(v).lower() in ("nan", "none", "null")
        ):
            continue
        meta[k] = v

    out: Dict[str, Any] = {
        "numer": numer,
        "nazwa": nazwa,
        "opis": opis,
        "zdjecie": zdjecie,
    }
    # Zgodnie z instrukcją w GUI: kolumna „typ” trafia jako pole top-level
    if lowered.get("typ"):
        out["typ"] = str(lowered["typ"]).strip()
    if meta:
        out["meta"] = meta
    if missing_numer or missing_nazwa:
        out["niekompletny"] = True
    return out

def _collect_column_warnings(columns: Iterable[Any]) -> List[str]:
    normalized = {str(col).strip().lower() for col in columns}
    warnings: List[str] = []
    if not any(key in normalized for key in ("nr", "numer", "id")):
        warnings.append("⚠ Brak kolumny 'numer' – zostanie ustawiona wartość domyślna.")
    if "nazwa" not in normalized:
        warnings.append("⚠ Brak kolumny 'nazwa' – zostanie ustawiona wartość domyślna.")
    return warnings


def import_excel_to_json(excel_path: str, out_dir: str) -> Tuple[int, List[str]]:
    if pd is None:
        raise RuntimeError("Brak zależności: pandas/openpyxl. Uruchom: pip install pandas openpyxl")
    if not os.path.exists(excel_path):
        raise FileNotFoundError(excel_path)
    _ensure_dir(out_dir)
    df = pd.read_excel(excel_path, sheet_name=0, engine="openpyxl")  # type: ignore
    df = df.dropna(how="all")
    warnings = _collect_column_warnings(df.columns)
    count = 0
    for lp, (_, row) in enumerate(df.iterrows(), start=1):
        row_dict = {str(c): row[c] for c in df.columns}
        tool = _row_to_tool(row_dict, lp)
        numer = tool.get("numer", "").strip()
        fname = _sanitize_filename(numer) + ".json"
        fpath = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(tool, f, ensure_ascii=False, indent=2)
        count += 1
    return count, warnings

def run_via_gui(app_state) -> None:
    """
    Integracja z GUI Ustawień:
      - pyta o plik Excel
      - zapisuje do <root>/data/narzedzia
      - pokazuje komunikat o wyniku
    Wymagane: app_state.get_root_path() -> str
    """
    import tkinter as tk
    from tkinter import filedialog, messagebox

    try:
        root_dir: Optional[str] = app_state.get_root_path()
    except Exception:
        root_dir = None
    if not root_dir:
        messagebox.showerror("Import narzędzi", "Najpierw ustaw <root> w Ustawieniach.")
        return

    # wybór pliku
    tk_root = tk.Tk(); tk_root.withdraw()
    xlsx_path = filedialog.askopenfilename(
        title="Wybierz plik Excel ze spisem narzędzi",
        filetypes=[("Excel", "*.xlsx;*.xlsm;*.xls")],
    )
    tk_root.destroy()
    if not xlsx_path:
        return

    # ścieżka docelowa
    out_dir = os.path.join(root_dir, "data", "narzedzia")
    try:
        if pd is None:
            raise RuntimeError("Brak zależności: pandas/openpyxl.\nUruchom: pip install pandas openpyxl")
        n, warnings = import_excel_to_json(xlsx_path, out_dir)
        msg_lines = [f"Utworzono plików: {n}", f"Lokalizacja: {out_dir}"]
        if warnings:
            msg_lines.append("")
            msg_lines.extend(warnings)
        messagebox.showinfo("Import narzędzi", "\n".join(msg_lines))
    except Exception as e:
        messagebox.showerror("Import narzędzi", f"Błąd importu:\n{e}")
