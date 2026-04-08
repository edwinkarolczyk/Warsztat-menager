# TODO / FIXME / HACK markers

Zestawienie aktualnych znaczników TODO/FIXME/HACK wykrytych w repozytorium
(pominięto katalogi audytu automatycznego).

## Kod

* `audyt_mw.py:176` – `# TODO/FIXME`
* `audyt_mw.py:177` – skanowanie wzorca `\b(TODO|FIXME|HACK)\b` w plikach audytu
* `audyt_mw.py:179` – raportowanie znaczników TODO/FIXME/HACK
* `backend/audit/wm_audit_runtime.py:374` – komentarz o formacie linii `[OK|TODO]`
* `backend/audit/wm_audit_runtime.py:376` – przypisanie statusu `OK`/`TODO`

## Konfiguracje i dane

* `data/audyt.json:30` – wpis statusu `"TODO"`
* `data/audyt.json:38` – wpis statusu `"TODO"`
* `data/audyt.json:87` – wpis statusu `"TODO"`
* `tools/roadmap_apply_updates.py:134` – `"status": "TODO"`
* `tools/roadmap_apply_updates.py:149` – `"status": "TODO"`
* `tools/roadmap_apply_updates.py:232` – `"status": "TODO"`
* `tools/roadmap_apply_updates.py:240` – `"status": "TODO"`

## Dokumentacja

* `ROADMAP.md:16` – sekcja „Drobne TODO/FIXME”
* `docs/code_review_checklist_c_answers.md:3` – nagłówek „TODO – szybka mapa kolejnych PR”
