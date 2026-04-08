# Mapa modułów WM

## Ustawienia
- **gui_settings.py** – panel konfiguracyjny z wyborem Folderu WM (`<root>`), migracją ścieżek oraz diagnostyką plików danych.【F:gui_settings.py†L252-L380】
- **config_manager.py** – centralny manager konfiguracji; odpowiada za mapowanie `resolve_rel`, migracje `<root>` i tworzenie backupów przed zapisem.【F:config_manager.py†L383-L456】【F:config_manager.py†L1477-L1496】
- **settings_schema.json** – definicje pól UI (tekst, opisy, walidacje) dla zakładek systemowych i domenowych.【F:settings_schema.json†L350-L460】
- **runtime_paths.py** – wykrywanie katalogu aplikacji w środowisku produkcyjnym/PyInstaller, fallback na ankrowy `C:\\wm`.【F:runtime_paths.py†L1-L76】

## Narzędzia (NN/SN)
- **gui_narzedzia.py** – główny widok narzędzi, obsługa migracji NN→SN, integracji z magazynem i kreatorem dyspozycji.【F:gui_narzedzia.py†L1-L120】
- **gui_tools.py** – helpery I/O zapisujące pliki narzędzi w `<root>/narzedzia` z tworzeniem katalogów.【F:gui_tools.py†L16-L58】
- **gui_tools_config.py / gui_tools_config_advanced.py** – konfiguracja typów/statusów i szablonów zadań; wykorzystują `tools_config_loader` do odczytu definicji.【F:tools_config_loader.py†L15-L135】
- **tools_history.py / narzedzia_history.py** – historia operacji na narzędziach, importowana w panelu do logowania zmian statusu.

## Maszyny
- **gui_maszyny.py / gui_maszyny_view.py** – widok hali, tryb edycji, podgląd statusów i szybkie akcje na maszynach (skala, siatka, wylogowanie).【F:gui_maszyny_view.py†L332-L391】
- **maszyny_logika.py / utils_maszyny.py** – ładowanie danych maszyn, agregacja serwisów, fallback na pliki `<root>/maszyny` dla Jarvisa.【F:core/jarvis_engine.py†L1045-L1070】
- **widok_hali/** – komponenty graficzne (SVG/tkinter) odpowiadające za layout hali.

## Zlecenia
- **gui_zlecenia.py** – lista zleceń z auto-odświeżaniem, integracją kreatora i obsługą zdarzeń `<<OrdersUpdated>>`.【F:gui_zlecenia.py†L268-L308】
- **gui_zlecenia_creator.py / gui_zlecenia_detail.py** – kreator i detale zleceń (statusy, zapisy).【F:gui_zlecenia_detail.py†L86-L120】
- **zlecenia_logika.py / zlecenia_utils.py** – logika biznesowa (terminy, liczenie zadań), wykorzystywana również przez Jarvisa przy budowie statystyk.【F:core/jarvis_engine.py†L1079-L1115】

## Profile i dostęp
- **gui_profile.py** – zarządzanie profilem użytkownika, przydziały zadań, rejestr aktywności.
- **profile_utils.py** – definicje ról, dostęp do Jarvisa (`can_access_jarvis`), funkcje bootstrap profili i wybór `<root>` przy pierwszym uruchomieniu.【F:profile_utils.py†L156-L218】
- **gui_uzytkownicy.py** – panel administracyjny użytkowników (lista, role, reset haseł).

## Magazyn & BOM
- **gui_magazyn.py** – panel listy materiałów, rezerwacje, szybkie zamówienia; zawiera wyłączony przycisk „Zamówienia” czekający na integrację.【F:gui_magazyn.py†L77-L142】
- **logika_magazyn.py / magazyn_io.py** – operacje na stanach magazynu, synchronizacja z BOM, obsługa rezerwacji.
- **logika_bom.py / ustawienia_produkty_bom.py** – zarządzanie strukturą BOM oraz powiązaniami półproduktów.

## Rdzeń / Config
- **core/bootstrap.py, core/** – inicjalizacja ścieżek, wczytywanie konfiguracji domenowych.
- **config_manager.py** – (jw.) serce konfiguracji i backupów; dostarcza `path_root`, `path_backup`, migracje z plików legacy.【F:config_manager.py†L1179-L1186】【F:config_manager.py†L1647-L1679】
- **logger.py / wm_log.py** – spójne logowanie (kanały `[JARVIS]`, `[CFG]`, etc.).

## Jarvis
- **core/jarvis_engine.py** – zbieranie statystyk, lokalna diagnostyka, harmonogram tła, fallback offline, alerty i powiadomienia.【F:core/jarvis_engine.py†L46-L112】【F:core/jarvis_engine.py†L1033-L1293】
- **core/jarvis_prompt_engine.py** – integracja z OpenAI, szacowanie kosztów, prompt builder i tryb offline.【F:core/jarvis_prompt_engine.py†L60-L195】
- **gui_jarvis_panel.py** – bogaty panel GUI (powiadomienia, historia, Q&A, auto-harmonogram).【F:gui_jarvis_panel.py†L22-L200】
- **gui_jarvis.py** – uproszczony panel tekstowy (legacy/demo) bazujący na `summarize_wm_data`.【F:gui_jarvis.py†L1-L78】
- **gui_panel.py** – integracja panelu Jarvisa w bocznym menu tylko dla ról z configu.【F:gui_panel.py†L776-L791】

## Powiadomienia i narzędzia wspólne
- **gui_notifications.py** – komponent toastów tkinter, obecnie niepodłączony do `notify()` Jarvisa.【F:gui_notifications.py†L1-L54】
- **wm_audit_runtime.py / rc1_*.py** – narzędzia audytowe i migracyjne wspierające konfigurację `<root>` i dane demonstracyjne.
- **tools/** – skrypty CLI (scan_missing_root, seed danych, migracje) wspomagające administrację.【F:tools/scan_missing_root.py†L1-L80】
