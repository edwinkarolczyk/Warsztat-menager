# Import narzędzi z Excela → `data/narzedzia/*.json`

Ten importer tworzy **osobne pliki JSON** zgodne ze strukturą z  
`docs/narzedzia_json_structure_example.md`.

## Mapowanie kolumn (domyślne)
- **A** / nagłówek podobny do: `Nr`, `Numer`, `Nr narzędzia` → `numer`
- **C** / nagłówek podobny do: `Opis`, `Nazwa`, `Kolumna3` → `nazwa`

Można wymusić nazwy kolumn: `--col-numer`, `--col-nazwa`.

## Braki danych
- Brak kolumn `numer`/`nazwa` lub pustych wartości nie zatrzymuje importu.
- Numer zostanie nadany automatycznie (`auto_<lp>`), nazwa przyjmie wartość `"bez nazwy"`.
- Wygenerowany rekord otrzyma pole `"niekompletny": true`, aby łatwiej go odszukać.
- Importer wypisze ostrzeżenie, jeśli kolumny `numer`/`nazwa` nie zostały znalezione.

## Wymagania
```
py -3 -m pip install -U pandas openpyxl
```

## Przykład uruchomienia (Windows)
Użyj pliku: `tools/importers/run_tools_from_excel.bat` i ustaw:
- `XLS` – nazwa arkusza Excela,
- `SHEET` – nazwa arkusza (np. `Arkusz1`).

## Przykład uruchomienia (CLI)
```
python tools/importers/tools_from_excel.py ^
  --input "Spis narzędzi.xlsx" ^
  --sheet "Arkusz1" ^
  --data-root "data" ^
  --out-subdir "narzedzia" ^
  --col-numer "Nr" ^
  --col-nazwa "Opis" ^
  --pad 3 ^
  --typ-default "Wykrawające" ^
  --status-default "sprawne" ^
  --pracownik-default "edwin" ^
  --mode skip
```

## Parametry
- `--data-root` – korzeń danych (zgodnie z `paths.data_root`), default: `data`
- `--out-subdir` – katalog docelowy w `data_root`, default: `narzedzia`
- `--pad` – zero-padding numeru (np. 3 → `001.json`)
- `--mode` – `skip` (nie nadpisuj istniejących) / `overwrite`
- `--tasks-json` – opcjonalny plik z listą zadań (lista stringów lub obiektów)
- `--tryb-default` – domyślnie `STARE`
- `--dry-run` – tryb testowy, który nie zapisuje wygenerowanych plików

## Zgodność
Każdy wygenerowany plik ma pola:
`numer, nazwa, typ, status, opis, pracownik, zadania[], data_dodania, tryb, interwencje[]`
zgodnie z przykładem w `docs/narzedzia_json_structure_example.md`.
