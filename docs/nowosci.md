# Nowości

## 2025-10-22 – Ulepszenia modułu „Narzędzia” i obsługi zadań

### Widok i dane zadań
- Dodano kolumnę **„Data”** w tabeli zadań (format DD-MM-YYYY) – pokazuje **datę dodania** zadania do narzędzia.
- Po zakończeniu zadania zapisywana jest również **data odznaczenia** i dopisywana do historii narzędzia.
- Zadania po odznaczeniu **nie są już usuwane** – trafiają do sekcji **Archiwalne**, zachowując pełne dane.

### Historia narzędzia
- W historii narzędzia rejestrowane są teraz trzy typy zdarzeń:
  - `task_added` – dodanie zadania (z datą),
  - `task_done` – zakończenie zadania (z datą),
  - `status_changed` – zmiana statusu narzędzia (z nazwą poprzedniego i nowego statusu).
- Historia nie jest czyszczona przy zmianie statusu — każdy cykl zostaje zapisany.

### Widok aktywnych i archiwalnych zadań
- Dodano przełącznik **„Pokaż historię zadań”**, który pozwala włączyć widok archiwalnych zadań.
- Archiwalne wiersze są **wyszarzone** i pokazują zarówno datę dodania, jak i datę zakończenia.
- Widok aktywny pokazuje tylko bieżące zadania dla aktualnego statusu narzędzia.

### Statusy i cykle życia
- Narzędzie może teraz przechodzić wielokrotnie przez różne statusy – każde przejście tworzy nowy cykl.
- Status pierwszy („Sprawne”) pozostaje końcowym – narzędzie podświetla się na **zielono (100 %)**, a aktywne zadania się zerują, bez kasowania historii.

---

🧭 **Efekt:**
Zachowana pełna historia pracy każdego narzędzia – wiadomo **kiedy dodano zadania, kiedy je zakończono i w jakich statusach**.
Widok jest czytelniejszy: „Aktywne” i „Archiwalne” da się teraz łatwo przełączać, bez utraty danych.
