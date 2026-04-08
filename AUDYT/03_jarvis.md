# Jarvis – szczegółowy audyt

## Checklist funkcjonalny
- ✅ **collect_wm_stats()** pobiera dane z loaderów narzędzi, maszyn, zleceń i profili wraz z fallbackiem do plików `<root>`.【F:core/jarvis_engine.py†L1033-L1063】
- ✅ **Sanity-checki**: `local_diagnostics()` zgłasza brak plików narzędzi/maszyn/zleceń oraz wolne moduły (log `[JARVIS][ALERT]`).【F:core/jarvis_engine.py†L960-L1010】
- ✅ **Panel wg ról**: przycisk Jarvisa widoczny tylko, gdy `can_access_jarvis()` zwróci True na podstawie `jarvis.role_access`.【F:gui_panel.py†L776-L791】【F:profile_utils.py†L156-L188】【F:config.defaults.json†L61-L70】
- ✅ **Akcje GUI**: `gui_jarvis_panel` udostępnia Analizuj/Zapisz/Historia/Otwórz raport oraz Q&A z polem pytania i historią wyników.【F:gui_jarvis_panel.py†L126-L197】【F:gui_jarvis_panel.py†L216-L247】
- ✅ **Harmonogram**: `run_jarvis_background()` uruchamia timer wg `jarvis.auto_interval_sec`, z obsługą zatrzymania i ponownych uruchomień.【F:core/jarvis_engine.py†L1244-L1293】
- ✅ **Anonimizacja + allow_ai**: `anonymize_for_ai()` maskuje osoby/IP/ścieżki, a panel odczytuje flagę `jarvis.allow_ai` i wyświetla status modelu.【F:core/jarvis_engine.py†L202-L287】【F:gui_jarvis_panel.py†L33-L71】
- ✅ **Fallback offline**: `_offline_summary()` tworzy raport tekstowy, a `run_analysis_report()` zapisuje `offline_reason` i alert o fallbacku modelu.【F:core/jarvis_prompt_engine.py†L91-L175】【F:core/jarvis_engine.py†L1085-L1112】
- ✅ **Diagnostyka lokalna**: wyniki `local_diagnostics()` trafiają do tabeli alertów i powiadomień `notify("diagnostyka", …)`.【F:core/jarvis_engine.py†L960-L1010】
- ✅ **Logowanie kosztów/modeli**: `core.jarvis_prompt_engine` zapisuje `[JARVIS][AI] model=… tokens … cost≈` do `wm.log`.【F:core/jarvis_prompt_engine.py†L60-L70】
- ✅ **Q&A pipeline**: `_send_question()` przekazuje pytanie do `run_analysis_report(question=…)`, wynik trafia do historii i autosave.【F:gui_jarvis_panel.py†L198-L247】【F:core/jarvis_engine.py†L1066-L1115】
- ✅ **Modele + fallback**: combobox udostępnia `gpt-3.5-turbo`/`gpt-4-turbo`, a metadane raportu wskazują użyty model/fallback.【F:gui_jarvis_panel.py†L113-L125】【F:core/jarvis_engine.py†L1107-L1112】
- ⚠️ **Powiadomienia GUI**: `notify()` utrzymuje bufor i opcjonalnie wyświetla systemowe toasty przez `plyer`, lecz brak podpięcia do `gui_notifications.show_notification()` (pozostaje do wdrożenia).【F:core/jarvis_engine.py†L46-L76】【F:gui_notifications.py†L1-L54】
- ⛔ **Fallback UI/Playbook**: brak dedykowanego komunikatu wizualnego w panelu przy przejściu w tryb offline; status trafia jedynie do paska tekstowego.【F:gui_jarvis_panel.py†L210-L235】

## Integracja danych i konfiguracji
- `collect_wm_stats()` dodaje alias `"zadania"` dla kompatybilności oraz dołącza aktywnego użytkownika z `ProfileService`.【F:core/jarvis_engine.py†L1051-L1061】
- Autosave raportów zapisuje pliki w `<root>/reports/auto/` i aktualizuje ścieżkę w metadanych, umożliwiając otwarcie z GUI.【F:core/jarvis_engine.py†L1013-L1106】【F:gui_jarvis_panel.py†L198-L247】
- Model domyślny i przełącznik zapisują się do configu (`ConfigManager().set('jarvis.model', …)`), z walidacją listy modeli.【F:gui_jarvis_panel.py†L89-L137】
- Harmonogram tła loguje stany (`wm_info`/`wm_err`) i respektuje wyłączenie `jarvis.enabled` lub `allow_ai`.【F:core/jarvis_engine.py†L1218-L1268】

## Ryzyka / luki
1. Brak wizualnej sygnalizacji alertów (toasty) mimo bufora `notify()` – wymaga spięcia z `gui_notifications`.【F:core/jarvis_engine.py†L46-L76】【F:gui_notifications.py†L1-L54】
2. Panel offline opiera się tylko na tekście w status barze; brak dedykowanego baneru/koloru przy `offline_reason`.【F:gui_jarvis_panel.py†L210-L235】
3. Nie ma globalnego rejestru kosztów/tokenów (tylko `wm.log`), co utrudnia raportowanie kosztowe.
4. Harmonogram bazuje na `threading.Timer` bez watchdogów – restart aplikacji wymagany po awarii wątku (brak auto-restartu w kodzie).
5. `gui_jarvis.py` (wersja legacy) nie respektuje roli ani ustawień `allow_ai`, co może prowadzić do niespójności przy jednoczesnym użyciu obu paneli.【F:gui_jarvis.py†L1-L78】
