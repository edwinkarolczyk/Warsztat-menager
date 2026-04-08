# R-07 (root + maszyny) — Roadmapa napraw (bez rozwoju)

## Cel R-07
- Jedno źródło prawdy dla Ustawień (schema + migracje aliasów + koercja typów).
- Widok Maszyn stabilny: siatka ON/OFF, tryby skalowania (Fit/100%), stopka (Wyloguj/Zamknij), pamięć stanu.
- Jedno okno (brak duplikacji widoków), podstawowy smoke w CI.
- Zero rozwoju funkcji poza koniecznym „fixem”.

---

## Sekcja A — Zrobione i zamknięte (merged)
- **#1245** — Settings Manager + MachinesView (siatka/fit/100/stopka) + smoke test. ✅  
- **#1246** — Porządki pod R-07 (usunięcie duplikatów/aliasów w Ustawieniach). ✅  
- **#1247** — Poprawki integracyjne widoku Maszyn (pamięć trybu/siatki). ✅  
- **#1248** — Stabilizacja zachowania skalowania (Fit/100%) + drobne UI. ✅  
- **#1249** — Domknięcie R-07 (ostatni merge pakietu root+maszyny). ✅

> Status: **DONE**. Nie rozwijamy dalej w R-07.

---

## Sekcja B — Do domknięcia w R-07 (naprawy)
1) **CI Smoke – zawsze automatycznie**
   - [ ] Dodać workflow `.github/workflows/r07_smoke.yml` uruchamiający `pytest -q tests/test_settings_manager.py` (deps: `pillow`, `pytest`).
   - [ ] Ustawić zasadę: merge tylko przy **zielonym** CI.
2) **Jedno okno (bez duplikacji)**  
   - [ ] Wymusić start przez `WindowManager` (1 × Tk + Notebook).  
   - [ ] Sprawdzić, czy nigdzie nie tworzymy dodatkowego `Toplevel` dla Maszyn.
3) **Ustawienia — sanity check**  
   - [ ] Przegląd kluczy podwójnych (aliasy), czy wszystkie migrują do `gui.*`, `paths.*`, `maszyny.*`, `system.*`.  
   - [ ] Utrzymać koercję typów (bool/int/str) — brak wyjątków.

**Definicje gotowe (kod dodany wcześniej w R-07) — tylko upewnić się, że są użyte.**

---

## Sekcja C — PR-y #1200–#1244 (do klasyfikacji, bez rozwoju)
Założenie: **nie rozwijamy**, tylko **porządkujemy** i klasyfikujemy pod R-07 (fix/chore).  
Dla każdego PR w tym zakresie:

- [ ] **#1244** — Klasyfikacja: `fix`/`chore`/`feat` → jeśli `feat` → przenieść do R-08 (on-hold).  
- [ ] **#1243** — Klasyfikacja jw.  
- [ ] **#1242** — Klasyfikacja jw.  
- [ ] **#1241** — Klasyfikacja jw.  
- [ ] **#1240** — Klasyfikacja jw.  
- [ ] **#1239** — Klasyfikacja jw.  
- [ ] **#1238** — Klasyfikacja jw.  
- [ ] **#1237** — Klasyfikacja jw.  
- [ ] **#1236** — Klasyfikacja jw.  
- [ ] **#1235** — Klasyfikacja jw.  
- [ ] **#1234** — Klasyfikacja jw.  
- [ ] **#1233** — Klasyfikacja jw.  
- [ ] **#1232** — Klasyfikacja jw.  
- [ ] **#1231** — Klasyfikacja jw.  
- [ ] **#1230** — Klasyfikacja jw.  
- [ ] **#1229** — Klasyfikacja jw.  
- [ ] **#1228** — Klasyfikacja jw.  
- [ ] **#1227** — Klasyfikacja jw.  
- [ ] **#1226** — Klasyfikacja jw.  
- [ ] **#1225** — Klasyfikacja jw.  
- [ ] **#1224** — Klasyfikacja jw.  
- [ ] **#1223** — Klasyfikacja jw.  
- [ ] **#1222** — Klasyfikacja jw.  
- [ ] **#1221** — Klasyfikacja jw.  
- [ ] **#1220** — Klasyfikacja jw.  
- [ ] **#1219** — Klasyfikacja jw.  
- [ ] **#1218** — Klasyfikacja jw.  
- [ ] **#1217** — Klasyfikacja jw.  
- [ ] **#1216** — Klasyfikacja jw.  
- [ ] **#1215** — Klasyfikacja jw.  
- [ ] **#1214** — Klasyfikacja jw.  
- [ ] **#1213** — Klasyfikacja jw.  
- [ ] **#1212** — Klasyfikacja jw.  
- [ ] **#1211** — Klasyfikacja jw.  
- [ ] **#1210** — Klasyfikacja jw.  
- [ ] **#1209** — Klasyfikacja jw.  
- [ ] **#1208** — Klasyfikacja jw.  
- [ ] **#1207** — Klasyfikacja jw.  
- [ ] **#1206** — Klasyfikacja jw.  
- [ ] **#1205** — Klasyfikacja jw.  
- [ ] **#1204** — Klasyfikacja jw.  
- [ ] **#1203** — Klasyfikacja jw.  
- [ ] **#1202** — Klasyfikacja jw.  
- [ ] **#1201** — Klasyfikacja jw.  
- [ ] **#1200** — Klasyfikacja jw.

**Zasada klasyfikacji:**
- `fix` → wchodzi do R-07 (jeśli dotyczy ustawień/maszyn lub stabilności).  
- `chore` → porządki, refaktory nie-funkcjonalne (OK w R-07).  
- `feat` → **przenieść** do **R-08 (on-hold)**, bez wdrażania teraz.

---

## Sekcja D — R-08 (backlog rozwojowy, nie teraz)
**Nie wdrażać w R-07.**  
- Tryb edycji pozycji maszyn + trwały zapis.  
- Statusy z animacją (rozszerzona telemetria).  
- A*/RouteAnimator + walls/rooms.  
- Zaawansowane panele szczegółów maszyny.

---

## Checklista zamknięcia R-07
- [ ] Workflow `r07_smoke.yml` jest w repo i działa (zielone CI dla PR).  
- [ ] `MachinesView` osadzony w **jednym oknie** (WindowManager lub równoważna konstrukcja).  
- [ ] Brak pozostałych aliasów/dubli w Ustawieniach (przejście przez schemat).  
- [ ] Wszystkie PR-y #1200–#1244 mają etykietę `fix/chore/feat`; `feat` przeniesione na R-08.

