# PLAN WDROŻENIA — status realizacji

Poniższe zestawienie podsumowuje, które punkty planu wdrożenia posiadają implementację w repozytorium, a które nadal wymagają prac.

## 🔧 Moduł Narzędzia
### P1 – krytyczne błędy
- ✅ Naprawiono filtrowanie zadań narzędzia po typie i statusie poprzez zestaw powiązanych comboboxów (kolekcja → typ → status), które ładują właściwe definicje zadań. 【F:gui_narzedzia.py†L1520-L1680】
- ⛔ Nie wykryto obsługi statusu „ZAKOŃCZONE” w zadaniach narzędzi (brak odniesień w module). 【1909b0†L1-L2】
- ✅ Zmiany statusu po oddaniu narzędzia (NN → ST → SN) są obsłużone – przełączenie na status „Odbiór zakończony” proponuje konwersję, a status końcowy automatycznie domyka zadania i loguje zdarzenie. 【F:gui_narzedzia.py†L3081-L3205】
- ✅ Numeracja plików narzędzi jest walidowana do formatu trzycyfrowego, co zapobiega błędom przy dodawaniu NN/SN. 【F:wm_tools_helpers.py†L1-L37】

### P2 – zmiany funkcjonalne
- ✅ Zadania narzędzi można przypisywać do konkretnego loginu oraz szybko przypisać sobie zadanie z menu kontekstowego. 【F:gui_narzedzia.py†L3489-L3568】
- ✅ Dostępny jest filtr „Moje” zawężający listę narzędzi do przypisanych operatorowi egzemplarzy i zadań. 【F:gui_narzedzia.py†L612-L640】【F:gui_narzedzia.py†L2476-L2516】
- ⛔ Nie znaleziono automatycznych przypomnień o przeglądach narzędzi w obecnym kodzie. 【61955d†L1-L2】

### P3 – ulepszenia / UI
- ✅ Tabela narzędzi ma poszerzone kolumny wraz z tooltipami prezentującymi pliki graficzne/dxf. 【F:gui_narzedzia.py†L2385-L2532】
- ✅ Kolorowe tagi odzwierciedlają status postępu (zielony/żółty/czerwony). 【F:gui_narzedzia.py†L2389-L2398】
- ⛔ Brak skrótu klawiszowego do szybkiego podglądu karty narzędzia (nie znaleziono powiązań z `<Control…>`). 【17c5d3†L1-L1】

## 🏭 Moduł Maszyny
### P1 – krytyczne błędy
- ✅ Wczytywanie `maszyny.json` uzupełnia `nr_hali` jako ciąg znaków dla każdej maszyny. 【F:core/machines_loader.py†L7-L74】
- ✅ Pozycje X/Y są zawężane do obszaru płótna dzięki funkcjom `_safe_clamp` oraz `_clamp_to_canvas`. 【F:gui_maszyny.py†L20-L36】【F:gui_maszyny.py†L656-L719】

### P2 – zmiany funkcjonalne
- ⛔ Automatyczne planowanie przeglądów z zewnętrznego harmonogramu nie jest obecne (z repozytorium wynika jedynie skrypt seedujący dane). 【042fd8†L1-L7】
- ✅ Kolor statusu maszyny zmienia się 30 dni przed terminem przeglądu, a etykieta pokazuje liczbę pozostałych dni. 【F:gui_maszyny.py†L150-L198】
- ⛔ Nie widać integracji przeglądów z kartami napraw z folderu „Karty przeglądów i napraw”. 【042fd8†L1-L7】

## 📦 Moduł Magazyn
### P1
- ✅ Rezerwacja narzędzia aktualizuje stan rezerwacji oraz zapisuje historię operacji. 【F:logika_magazyn.py†L638-L664】

### P2
- ⛔ Brak filtra po lokalizacji magazynowej w widoku GUI. 【b6de76†L1-L1】
- ⛔ Nie odnaleziono zapisu historii pobrań do `magazyn_log.json`. 【7e3fb9†L1-L1】

### P3
- ⛔ Nie zaimplementowano kolorów/ikon dla poziomów zapasów. 【b6de76†L1-L1】

## 🧰 Moduł Zlecenia
### P1
- ⛔ Błąd przypisywania zadań do użytkowników nie został zidentyfikowany jako naprawiony (brak modyfikacji obsługi ID). 【3453da†L1-L1】

### P2
- ⛔ W tabeli zleceń nie ma dodatkowych kolumn „czas realizacji” ani „brygadzista”. 【F:gui_zlecenia.py†L230-L279】
- ⛔ Nie zaobserwowano automatycznego zamykania zlecenia po wykonaniu. 【F:gui_zlecenia.py†L230-L315】

## ⚙️ Moduł Ustawienia / Config
### P2
- ⛔ Brak dowodu na przeniesienie `machines_file` do `layout/maszyny.json` w konfiguracji. 【825b27†L1-L1】
- ⛔ Nie wdrożono przełącznika motywu jasny/ciemny w GUI ustawień. 【8ce5f3†L1-L1】
- ⛔ Konfiguracja nie zawiera nowych pól ścieżek backupów i assets (brak wpisów `assets` w `config.json`). 【206390†L1-L1】

### P3
- ⛔ Nie znaleziono zakładki „Diagnostyka WM” w module ustawień. 【860807†L1-L1】

## 🧑‍💻 Moduł GUI / Panel główny
### P1
- ⛔ Stary pasek ustawień nadal widnieje (sekcja nagłówka pozostaje bez zmian). 【F:gui_panel.py†L574-L590】

### P2
- ⛔ Karty nie zostały ujednolicone do stylu „2xl rounded, shadow-md, padding p-2” – brak odniesień do stylu `shadow` w module. 【6cda62†L1-L1】
- ⛔ Brak automatycznego odświeżania danych po zapisie JSON w panelu (brak obsługi zdarzeń `<<Json…>>`). 【9130b8†L1-L1】

### P3
- ⛔ Layout panelu nadal opiera się na `pack`, bez konfiguracji siatki responsywnej. 【F:gui_panel.py†L574-L600】

## 🧱 System / Ogólne
### P1
- ⛔ Nie zaimplementowano automatycznej kopii zapasowej `config.json` i `data/*.json` przy starcie (backup dostępny wyłącznie z okna błędu). 【F:start.py†L219-L244】

### P2
- ✅ Moduły mają wpisy wersji w nagłówkach (np. `gui_narzedzia.py 1.5.31`). 【F:gui_narzedzia.py†L1-L9】
- ⛔ Brak dowodu na automatyczny zapis zmian wersji do `logi_wersji.json` (kod jedynie odczytuje ostatni wpis). 【F:updates_utils.py†L52-L108】

### P3
- ✅ Repozytorium zawiera aktualny plik `CHANGELOG.md` z podsumowaniem ostatnich zmian. 【F:CHANGELOG.md†L1-L28】

## 💡 Dodatkowe (Backlog)
- ⛔ Nie dodano roli „serwisant” w profilach użytkownika. 【34cb8f†L1-L1】
- ⛔ Wciąż należy sprawdzić błędy przy ładowaniu `narzedzia/*.json` (brak nowych walidacji w modułach GUI). 【1909b0†L1-L2】
- ⛔ Migracja starych konfiguracji `hall.machines_file` wymaga dalszego potwierdzenia (repo zawiera tylko skrypty migracyjne). 【1e2428†L1-L33】
- ⛔ Nie dodano wykresu aktywności użytkowników w panelu głównym. 【6cda62†L1-L1】

