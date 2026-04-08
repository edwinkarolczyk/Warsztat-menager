# Plan wdrożenia WM jako EXE portable

## Cele
Minimalne zmiany w kodzie, tak aby aplikacja działała:
- z katalogu lokalnego (onedir),
- bez instalacji Pythona,
- z zachowaniem struktury `data/`, `logs/`, `backup/`.

## Zakres modułów
**1. Narzędzia:** walidacja struktury plików JSON.  
**2. Profile:** kontrola spójności loginów i ról.  
**3. Ustawienia:** sprawdzenie kluczy `paths.*`, migracja z `system.*`.

## Minimalne modyfikacje
Dodaj funkcje w `config/paths.py`:

```python
import sys, os
from pathlib import Path

def get_app_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).parent
    return Path(__file__).resolve().parents[1]

def get_data_root(cfg: dict) -> Path:
    env = os.getenv("WM_DATA_ROOT")
    if env:
        return Path(env)
    p = (cfg.get("paths") or {}).get("data_root") or "data"
    return get_app_root() / p if not Path(p).is_absolute() else Path(p)

def get_logs_dir(cfg: dict) -> Path:
    p = (cfg.get("paths") or {}).get("logs_dir") or "logs"
    base = get_app_root() / p if not Path(p).is_absolute() else Path(p)
    return base

def get_backup_dir(cfg: dict) -> Path:
    p = (cfg.get("paths") or {}).get("backup_dir") or "data/backup"
    base = get_app_root() / p if not Path(p).is_absolute() else Path(p)
    return base
```

### Pliki dodatkowe
- `tools/validators/tools_schema_validator.py`
- `tools/validators/profiles_validator.py`
- `tools/validators/settings_paths_validator.py`
- `build/wm.spec`
- `build/build_exe.bat`

## Build
```
py -3 -m pip install pyinstaller
pyinstaller --clean --workpath build/_work --distpath build/dist build/wm.spec
```

## Test
1. Uruchom `build/dist/WM/WM.exe`  
2. Sprawdź automatyczne tworzenie plików w `data/`  
3. W razie potrzeby ustaw zmienną środowiskową `WM_DATA_ROOT`

## Raporty walidacji
Każdy walidator generuje raport w `reports/*.md`

- `tools_schema_report.md` – błędy w strukturze narzędzi  
- `profiles_report.md` – niespójne loginy / role  
- `settings_paths_report.md` – konfiguracja ścieżek

Po wykonaniu Codex ma zwrócić raporty z liczbą plików i błędów.
