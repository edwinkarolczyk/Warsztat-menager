# Audit Warsztat-Menager & Jarvis — podsumowanie

Data: 2025-10-27
Gałąź: work @ 4c9292cfa196c8c64ba7cc23aa14a597a720852c
Audytor: Codex

## Status modułów
| Moduł      | P0 | P1 | P2 | Uwagi kluczowe |
|------------|----|----|----|----------------|
| Ustawienia | ✅ | ✅ | ⛔ | `gui_settings.py` pokrywa ścieżki `<root>` i migracje, ale brak kompletnych testów/regresji dla kreatora root oraz brak cyklicznego health-checku backupów. |
| Narzędzia  | ✅ | ⛔ | ⛔ | Edycja NN/SN i migracje działają (`gui_narzedzia.py`, `tools_config_loader.py`), lecz brakuje automatycznego przenoszenia NOWE→SN i spójnego cache/history dashboardu. |
| Maszyny    | ✅ | ⛔ | ⛔ | Widoki i logika serwisów gotowe (`gui_maszyny_view.py`, `maszyny_logika.py`), jednak nie ma TTFM/metryk ładowania ani alertów do panelu głównego. |
| Zlecenia   | ✅ | ⛔ | ⛔ | Lista i kreator (`gui_zlecenia.py`, `gui_zlecenia_creator.py`) działają, ale brak kolumn zapotrzebowania/powrotów materiałów oraz integracji z harmonogramem zmian. |
| Profile    | ✅ | ⛔ | ⛔ | Zarządzanie użytkownikami dostępne (`gui_profile.py`, `profile_utils.py`), nadal brak filtra „moje zadania” i jednookiennej edycji profilu. |
| Magazyn    | ✅ | ⛔ | ⛔ | Panel rezerwacji i powiązań BOM działa (`gui_magazyn.py`, `logika_magazyn.py`), natomiast przycisk „Zamówienia” pozostaje wyłączony i nie ma alertów stanów krytycznych. |
| Rdzeń/Config | ✅ | ✅ | ⛔ | `config_manager.py` zapewnia migracje `<root>` i backupy, ale automatyczne testy dymne/config-backup watcher wciąż niewdrożone. |
| Jarvis     | ✅ | ✅ | ⛔ | Silnik zbiera realne dane i obsługuje fallback/harmonogram, lecz brak integracji z globalnymi toastami i playbookiem awaryjnym UI. |

## Jarvis — szybki werdykt
- Dane realne: ✅ `collect_wm_stats()` agreguje narzędzia/maszyny/zlecenia/profile z loaderów.【F:core/jarvis_engine.py†L1033-L1063】
- Panel tylko dla ról: ✅ przycisk widoczny wyłącznie po `can_access_jarvis()`.【F:gui_panel.py†L776-L791】【F:profile_utils.py†L156-L188】
- Harmonogram: ✅ `run_jarvis_background()` startuje timer wg `auto_interval_sec` z configu.【F:core/jarvis_engine.py†L1244-L1293】
- Anonimizacja + allow_ai: ✅ `anonymize_for_ai()` maskuje osoby/ścieżki, a panel respektuje flagę `allow_ai`.【F:core/jarvis_engine.py†L202-L287】【F:gui_jarvis_panel.py†L33-L71】
- Fallback offline: ✅ `_offline_summary()` i metadata `offline_reason` obsługują tryb bez OpenAI.【F:core/jarvis_prompt_engine.py†L91-L175】【F:core/jarvis_engine.py†L1085-L1115】
- Diagnostyka lokalna: ✅ `local_diagnostics()` wykrywa brak plików i wolne moduły oraz loguje alerty.【F:core/jarvis_engine.py†L960-L1010】
- Q&A: ✅ panel ma pole pytania + historia odpowiedzi.【F:gui_jarvis_panel.py†L164-L197】【F:gui_jarvis_panel.py†L216-L247】
- Modele 3.5/4 + fallback: ✅ combobox modeli i alert o fallbacku w metadata.【F:gui_jarvis_panel.py†L113-L125】【F:core/jarvis_engine.py†L1107-L1112】
- Powiadomienia: ♻️ Bufor `notify()` + logi [JARVIS], ale brak spięcia z `gui_notifications.show_notification`.【F:core/jarvis_engine.py†L46-L76】【F:gui_notifications.py†L1-L54】

## Najważniejsze braki (Top 5)
1) Brak aktywnego połączenia powiadomień Jarvisa z UI toastami i globalną sekcją alertów.
2) Moduły Narzędzia/Magazyn nie wystawiają spójnych statusów cache/historii oraz nie aktualizują panelu głównego w czasie rzeczywistym.
3) Zlecenia i Magazyn nie synchronizują zapotrzebowania materiałowego ani zwrotów przy cofnięciu zadań.
4) Brakuje automatycznych testów/regresji dla zmiany `<root>` i walidacji backupów configu.
5) Panel Profili nadal nie oferuje filtra „moje zadania” ani scentralizowanej edycji w jednym oknie.

## Rekomendacje następnych kroków
- Spiąć `core.jarvis_engine.notify()` z `gui_notifications.show_notification()` i centralnym panelem alertów.
- Dokończyć integrację Magazyn↔Zlecenia (zamówienia z braków, zwrot materiału) oraz dodać alerty stanów minimalnych.
- Wdrożyć test dymny ConfigManagera (backup/migracje `<root>`) odpalany przy starcie lub CI.
- Rozbudować panel profili o filtr „moje” i edycję inline, zgodnie z backlogiem.
- Zaimplementować monitor czasu ładowania modułów i eksponować TTFM/diagnostykę w GUI głównym.
