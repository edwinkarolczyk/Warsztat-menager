# Struktura zapisu plików JSON

## Główny katalog danych

Domyślny katalog danych to folder `data` w katalogu głównym aplikacji (app_root).
Aktualny korzeń danych określa `paths.data_root` w `config.json`.
> **Uwaga (legacy):** `system.data_root` jest wspierane dla zgodności wstecznej, ale zalecamy używać wyłącznie `paths.data_root`.

## Mapowanie plików i katalogów

Ścieżki poniżej są **względem `paths.data_root`** (nie poprzedzamy ich `data/`):

| Klucz                              | Ścieżka względna                 | Zawartość |
|------------------------------------|----------------------------------|----------|
| `machines`                         | `layout/maszyny.json`            | Lista maszyn, pozycje, parametry |
| `warehouse` / `warehouse_stock`    | `magazyn/magazyn.json`           | Stany magazynowe i rejestry |
| `bom`                              | `produkty/bom.json`              | Struktury materiałowe produktów |
| `orders`                           | `zlecenia/zlecenia.json`         | Zlecenia produkcyjne |
| `tools`                            | `narzedzia/narzedzia.json`       | Indeks narzędzi |
| `tools.dir` / `tools_dir`          | `narzedzia/`                     | Katalog z plikami narzędzi |
| `tools.types`                      | `narzedzia/typy_narzedzi.json`   | Definicje typów narzędzi |
| `tools.statuses`                   | `narzedzia/statusy_narzedzi.json`| Statusy narzędzi |
| `tools.tasks_templates`            | `narzedzia/szablony_zadan.json`  | Szablony zadań dla narzędzi |
| `tools.tasks_defs`                 | `narzedzia/zadania_narzedzi.json`| Zadania/relacje z narzędziami |
| `profiles`                         | `profiles.json`                   | Profile użytkowników i uprawnienia |

Ścieżki katalogów **poza `data_root`** (domyślne; konfigurowalne):

| Klucz             | Domyślna lokalizacja        | Opis |
|-------------------|-----------------------------|------|
| `paths.logs_dir`  | `<app_root>/logs`           | Katalog na logi aplikacji |
| `paths.backup_dir`| `<data_root>/backup`        | Katalog kopii zapasowych (może wskazywać inny dysk) |
| *(legacy)* `system.backup_root` | zależnie od instalacji | Stare pole; jeśli ustawione, ma pierwszeństwo nad domyślnym `paths.backup_dir` |

## Logika ustalania ścieżek

1. `get_root()` zwraca `paths.data_root` (albo domyślnie `<app_root>/data`).
2. `resolve_rel()` składa ścieżki względem `data_root` z map aliasów (`PATH_MAP` / `RESOLVE_MAP`) – np. `tools`, `tools.dir`, `tools.types`.
3. `core.bootstrap`: przy `system.suppress_json_prompts=true` inicjuje brakujące wpisy w `config.json` na bazie `data_root` i domyślnych map.
4. `utils_paths`: dostarcza helpery do ścieżek narzędziowych (`tools_dir()`, `tools_file()`), magazynu, itp.

## Tworzenie brakujących plików i katalogów

- `ensure_json()` oraz `safe_read_json()` tworzą brakujące pliki z domyślną zawartością (dict/list) z kodowaniem UTF-8 i wcięciem **2 spacje**.
- `_ensure_parent()` gwarantuje istnienie katalogów nadrzędnych przed zapisem.
- `safe_write_json()` zapisuje dane i automatycznie tworzy katalog docelowy.

## Zalecenia dot. nazewnictwa kluczy (konfiguracja)

- Używaj przestrzeni `paths.*` dla wszystkich nowych ścieżek (np. `paths.data_root`, `paths.logs_dir`, `paths.backup_dir`).
- Pola `system.*` traktować jako **legacy**; nie dodawać nowych.
- Alias dla szablonów zadań: `tools.tasks_templates` (zamiast mieszanego `tools.tasks` / `tools_templates`).

## Przykład minimalnego `config.json`

```json
{
  "paths": {
    "data_root": "data",
    "logs_dir": "logs",
    "backup_dir": "data/backup"
  },
  "system": {
    "suppress_json_prompts": true
  }
}
```

## Uwagi zgodności wstecznej

- Jeżeli wykryta jest starsza konfiguracja (`system.data_root`, `system.backup_root`), migracja przenosi wartości do `paths.*`, zachowując stare pola do czasu pełnej aktualizacji.

---

Dzięki powyższemu aplikacja startuje poprawnie nawet przy pustym `data_root` — brakujące pliki są generowane przy pierwszym odczycie lub zapisie.
