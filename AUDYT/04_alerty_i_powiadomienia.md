# Alerty i powiadomienia

## Jarvis
- `core.jarvis_engine.notify()` buforuje wpisy (czas, kategoria, poziom) i loguje na STDOUT oraz opcjonalnie korzysta z `plyer` dla alertów >=4.【F:core/jarvis_engine.py†L46-L76】
- `local_diagnostics()` dodaje alerty poziomu `warning/alert` do bufora i zapisuje `[JARVIS][ALERT]` w `wm.log`.【F:core/jarvis_engine.py†L960-L1010】
- Panel Jarvisa cyklicznie odświeża sekcję „Powiadomienia Jarvisa” z bufora `get_notifications()` i koloruje wpisy zależnie od poziomu.【F:gui_jarvis_panel.py†L126-L205】
- `start.py` uruchamia harmonogram tylko dla aktywnego użytkownika i zatrzymuje timer przy zamknięciu aplikacji (zapobiega wiszącym wątkom).【F:start.py†L757-L818】

## GUI i system
- `gui_notifications.py` dostarcza toast-like `NotificationPopup`, lecz nie jest obecnie wywoływany przez Jarvisa ani inne moduły – brak centralnej integracji.【F:gui_notifications.py†L1-L54】
- Panel główny (`gui_panel.py`) oznacza przyciski czerwonym markerem po zmianach, lecz nie konsumuje alertów Jarvisa ani stanów magazynu/maszyn.【F:gui_panel.py†L708-L813】
- `wm_log.py` pozwala filtrować poziom logów i integruje się z ustawieniami (`ui.log_level`, `ui.debug_enabled`), zapewniając konsolowe śledzenie `[JARVIS]`, `[CFG]` itd.【F:wm_log.py†L11-L110】

## Braki i rekomendacje
1. **Brak toastów Jarvisa** – należy podpiąć `notify()` do `gui_notifications.show_notification()` i/lub globalnej tablicy alertów w panelu głównym.【F:core/jarvis_engine.py†L46-L76】【F:gui_notifications.py†L1-L54】
2. **Alerty magazynowe** – przycisk „Zamówienia” w magazynie jest wyłączony (`if False`), więc brak sygnalizacji braków w UI mimo planowanych alertów stanów.【F:gui_magazyn.py†L77-L142】【F:WDROZENIA.md†L21-L22】
3. **Brak fallbacku UI** – tryb offline Jarvisa nie wyświetla dedykowanego baneru/ikon; informacja trafia tylko do status bara.【F:gui_jarvis_panel.py†L210-L235】
4. **Centralne powiadomienia** – brak modułu agregującego alerty (Jarvis, Magazyn, Maszyny) do jednego widoku; obecnie każdy moduł działa autonomicznie.
5. **Brak testów notyfikacji** – w katalogu `tests/` nie ma scenariuszy dla `notify()`/`gui_notifications`, co utrudnia regresję.
