# DEBUG PROFILES — co zobaczysz w konsoli

Po podmianie plików i uruchomieniu WM:
- Wejście w Panel → Użytkownicy wypisze:
  [PROFILES-DBG] panel_uzytkownicy: start ...
  [PROFILES-DBG] panel_uzytkownicy: cfg show_tab=... show_head=... fields=...
  [PROFILES-DBG] panel_uzytkownicy: Notebook created
  [PROFILES-DBG] panel_uzytkownicy: tabs added
  [PROFILES-DBG] panel_uzytkownicy: current_user=...
  [PROFILES-DBG] panel_uzytkownicy: render_profile OK

- Wejście w Ustawienia wypisze:
  [PROFILES-DBG] panel_ustawien: start
  [PROFILES-DBG] panel_ustawien: after-calls scheduled
  [PROFILES-DBG] ustawienia: helper start
  [PROFILES-DBG] ustawienia: scanning for Notebook...
  [PROFILES-DBG] ustawienia: Notebook NOT found yet   (jeśli za wcześnie)
  ...po chwili kolejne próby...
  [PROFILES-DBG] ustawienia: tab added

Jeśli zobaczysz ERROR-y, skopiuj je i podeślij — poprawię w punkt.

Aby wyłączyć logi — po testach można przywrócić poprzednie pliki lub usunąć printy.

## Szybkie testy profili
1. **Podstawowy odczyt** – w pliku `data/profiles.json` zostaw tylko konto `admin`, uruchom WM i sprawdź, że na ekranie logowania combobox zawiera `admin`.
2. **Dodawanie profilu** – dodaj nowy profil w zakładce Ustawienia → Lista profili, zapisz zmiany i uruchom ponownie WM. Na ekranie logowania powinny być widoczne oba loginy.
3. **Brak pliku** – tymczasowo usuń `data/profiles.json`, uruchom WM i zweryfikuj komunikat o brakującym pliku oraz log `[WM-ERR][LOGIN] profiles file not found`.
4. **Uszkodzony JSON** – celowo popsuj strukturę `profiles.json` (np. usuń nawias) i uruchom WM; powinien pojawić się komunikat o uszkodzonym pliku oraz log `[WM-ERR][LOGIN] invalid JSON in profiles file`.
5. **Ścieżka w logu** – sprawdź w konsoli wpisy `[WM-DBG][LOGIN] profiles_path = …` oraz `[WM-DBG][PROFILES] profiles_path = …` aby potwierdzić, że oba moduły pracują na tym samym pliku.
