# Konfiguracja `<root>` i ścieżki

## Aktualne źródła prawdy
- `config.json` nadal zawiera placeholdery `<root>\\…` dla katalogów danych, co wymaga zamiany przez ConfigManager przy każdym uruchomieniu.【F:config.json†L14-L24】
- `config.defaults.json` definiuje sekcję `jarvis` (modele, role) oraz ścieżki domyślne (anchor `C:\\wm`).【F:config.defaults.json†L61-L95】
- `settings_schema.json` dokumentuje w UI, że katalogi są wyliczane względem `<root>` (magazyn, BOM, zlecenia).【F:settings_schema.json†L350-L460】

## Mechanizmy migracji
- `ConfigManager.resolve_rel()` oraz `_apply_root_defaults()` przeliczają ścieżki względem aktualnego `paths.data_root` i uzupełniają brakujące wpisy (tools/orders/warehouse).【F:config_manager.py†L383-L456】
- `update_root_paths()` w panelu ustawień tworzy katalogi `backup/` i `logs/` po zmianie `<root>`.【F:gui_settings.py†L298-L319】
- `try_migrate_if_missing()` kopiuje pliki legacy do nowego `<root>` jeśli docelowe zasoby nie istnieją (narzędzia, magazyn itp.).【F:config_manager.py†L459-L566】
- `runtime_paths.get_app_root()` obsługuje PyInstaller, zmienną `WM_DATA_ROOT` i dialog wyboru katalogu – fallback na `C:\\wm`.【F:runtime_paths.py†L1-L76】
- Skrypt `tools/scan_missing_root.py` przeszukuje repo pod kątem twardych odwołań do `data/` bez `<root>`.【F:tools/scan_missing_root.py†L1-L80】

## Obszary ryzyka
1. **Literal `<root>` w config.json** – jeśli migracja nie zostanie uruchomiona (np. błąd ConfigManagera), ścieżki z backslashami mogą powodować `WinError 123`; rozważyć automatyczne podmienianie placeholderów przy bootstrapie CLI.【F:config.json†L14-L24】
2. **Brak testu dymnego** – repo nie zawiera testu sprawdzającego `ConfigManager().save_all()` po zmianie `paths.data_root`, przez co regresje backupów mogą ujść uwadze.
3. **Wyłączony moduł toastów** – brak powiązania `notify()` z informacją o zmianie `<root>` (np. brak toasta po migracji plików).
4. **Niejednoznaczność `anchor_root`** – domyślny `C:\\wm` może być nieosiągalny w środowiskach Linux; warto dodać logikę wyboru domyślnego z `Path.home()`.
5. **Stary panel `gui_jarvis.py`** nie korzysta z `ConfigManager`, może czytać pliki z bieżącego katalogu – ryzyko niespójnych danych przy zmianie `<root>`.【F:gui_jarvis.py†L1-L78】

## Rekomendacje
- Wymusić zapis realnych ścieżek do `config.json` (bez `<root>`) po pierwszym przejściu kreatora, aby uniknąć placeholderów w repo.
- Dodać automatyczny test (np. `pytest`) weryfikujący `ConfigManager().update_root_paths()` i powstawanie katalogów `logs/backup`.
- Rozszerzyć `tools/scan_missing_root.py` o automatyczną naprawę oraz raport JSON dla CI.
- Rozważyć przeniesienie starych plików `config_old.json` do archiwum, aby uniknąć przypadkowego użycia.
