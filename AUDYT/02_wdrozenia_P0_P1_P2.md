# Wdrożenia P0/P1/P2

## Ustawienia
- **P0 (wdrożone)**: wybór Folderu WM, zapis `<root>` i diagnostyka ścieżek w panelu ustawień.【F:gui_settings.py†L252-L377】
- **P1 (wdrożone)**: `ConfigManager` uzupełnia/migruje ścieżki relatywne i tworzy backupy przy zmianach.【F:config_manager.py†L383-L456】【F:config_manager.py†L1477-L1496】
- **P2 (braki)**: brak wdrożonego grupowania ustawień i skróconych opisów, nadal w sekcji „Planowane”.【F:WDROZENIA.md†L13-L26】

## Narzędzia
- **P0 (wdrożone)**: obsługa NN/SN z migracjami i integracją z magazynem (zwrot/zużycie materiałów).【F:gui_narzedzia.py†L1-L20】
- **P1 (częściowe)**: loader definicji potrafi leczyć JSON i korzysta z backupów, ale automatyczne przenoszenie NOWE→SN nadal w backlogu.【F:tools_config_loader.py†L98-L135】【F:WDROZENIA.md†L15-L25】
- **P2 (braki)**: brak batch-oznaczania zadań i historii operacji w UI (zapisane jako planowane).【F:WDROZENIA.md†L24-L25】

## Maszyny
- **P0 (wdrożone)**: widok hali z trybem edycji, skalą i kontrolą siatki.【F:gui_maszyny_view.py†L332-L391】
- **P1 (częściowe)**: Jarvis zbiera metryki serwisów, ale brak ekspozycji TTFM/alertów do głównego panelu (planowana wirtualizacja/filtry).【F:core/jarvis_engine.py†L1045-L1080】【F:WDROZENIA.md†L26-L26】
- **P2 (braki)**: brak TTFM + monitoringu w UI głównym – brak implementacji w kodzie panelu (`gui_panel.py`).

## Zlecenia
- **P0 (wdrożone)**: lista z auto-refresh i kreator zleceń z fallbackiem do kreatora dyspozycji.【F:gui_zlecenia.py†L268-L308】
- **P1 (braki)**: kolumny zapotrzebowania/rezerwacji oraz BOM explosion znajdują się w planie, nie w kodzie.【F:WDROZENIA.md†L19-L23】
- **P2 (braki)**: brak integracji ze zwrotem materiału i harmonogramem zmian (niewidoczne w `gui_zlecenia.py`).

## Profile
- **P0 (wdrożone)**: logika ról i dostęp do Jarvisa w `profile_utils`.【F:profile_utils.py†L156-L218】
- **P1 (braki)**: brak filtra „moje zadania” i stałych filtrów wyszukiwania (pozostają w planie).【F:WDROZENIA.md†L24-L26】
- **P2 (braki)**: edycja profilu w jednym oknie i zaawansowane workflowy niezaimplementowane w `gui_profile.py` (brak odpowiednich widżetów).

## Magazyn
- **P0 (wdrożone)**: panel rezerwacji, szybkie zamówienia oraz akcje rezerwuj/zwolnij.【F:gui_magazyn.py†L118-L147】
- **P1 (braki)**: brak alertów stanów minimalnych i listy „Do zamówienia” – wciąż planowane.【F:WDROZENIA.md†L21-L22】
- **P2 (braki)**: przycisk „Zamówienia” w toolbarze jest dezaktywowany (`if False`) i wymaga integracji z modułem zleceń.【F:gui_magazyn.py†L77-L92】

## Rdzeń / Config
- **P0 (wdrożone)**: `resolve_rel` i `_apply_root_defaults` gwarantują poprawne ścieżki względem `<root>`.【F:config_manager.py†L383-L456】
- **P1 (wdrożone)**: system backupów `config_manager` + `path_backup()` oraz sanitizacja konfiguracji przy zapisie.【F:config_manager.py†L1477-L1679】
- **P2 (braki)**: brak automatycznych testów dymnych i watcherów backupów (nie znaleziono w repo, brak integracji w `start.py`).

## Jarvis
- **P0 (wdrożone)**: bufor powiadomień, alerty lokalne, zebranie danych domenowych.【F:core/jarvis_engine.py†L46-L112】【F:core/jarvis_engine.py†L1033-L1115】
- **P1 (wdrożone)**: harmonogram wątku tła i panel GUI z Q&A, wyborem modeli, historią.【F:core/jarvis_engine.py†L1244-L1293】【F:gui_jarvis_panel.py†L22-L247】
- **P2 (braki)**: brak spięcia z toastami (`gui_notifications.py`) i brak scenariusza fallback UI mimo logów `[JARVIS][ALERT]`.【F:gui_notifications.py†L1-L54】
