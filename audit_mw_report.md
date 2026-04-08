# Audyt MW – raport

Katalog: /workspace/Warsztat-Menager

Plików .py: 256


## Sugestie

- Ujednolić nagłówki # Plik/# Wersja we wszystkich plikach (generator nagłówka w pre-commit).
- Rozbić cykliczne importy – wydzielić warstwę 'core' (modele, utils), 'gui' (widoki), 'app' (uruchomienie).
- Zapewnić pojedynczy mainloop, kontrolować .after() (cleanup przy zamknięciu), nie mieszać pack/grid w jednym kontenerze.
- Dodać pre-commit (ruff + black, isort). Włączyć flake nieużytych importów.
- Walidować config.json/maszyny.json/uzytkownicy.json z JSON Schema na starcie aplikacji.
- Moduł serwisowy jako oddzielny pakiet z event-busem (pub/sub) i kolejką zadań – izolacja od GUI.
- Potrójne potwierdzenie usuwania: dialog modalny z 3-krotnym 'OK' + timeout i klawisz ESC – antymisclick.
- Wydzielić ui_theme.py jako jedyne źródło kolorów/typografii; zakaz inline kolorów w GUI.

## Znalezione problemy

- **WARN** [HEADER] __version__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] __version__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] arch/start_full_1_4_3.py – Brak nagłówka # Plik: ...
- **INFO** [GUI] arch/start_full_1_4_3.py:32 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **WARN** [HEADER] audit_settings_schema.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] audit_settings_schema.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] audyt_mw.py:34 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] audyt_mw.py:72 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] backend/audit/wm_audit_runtime.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] backend/audit/wm_audit_runtime.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] backend/bootstrap_root.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] backend/bootstrap_root.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] backend/updater.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] backend/updater.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] backup.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] backup.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] bom.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] bom.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] config/paths.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] config/paths.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] config/paths.py:99 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] config/paths.py:113 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] config_manager.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] config_manager.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] config_manager.py:161 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] config_manager.py:202 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] config_manager.py:222 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] config_manager.py:229 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] config_manager.py:284 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] config_manager.py:1456 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] config_manager.py:1475 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] core/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/bootstrap.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/bootstrap.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] core/bootstrap.py:67 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] core/inventory_manager.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/inventory_manager.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/logging_config.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/logging_config.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/logika_zlecen.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/logika_zlecen.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/machines_loader.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/machines_loader.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/modules_manifest.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/modules_manifest.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/normalizers.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/normalizers.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/orders_storage.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/orders_storage.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] core/orders_storage.py:75 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] core/paths_compat.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/paths_compat.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/permissions.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/permissions.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/settings_manager.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/settings_manager.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] core/settings_manager.py:256 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] core/settings_manager.py:311 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] core/settings_manager.py:312 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] core/settings_manager.py:403 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] core/settings_manager.py:421 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] core/theme.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/theme.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] core/ui_notebook_autobind.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/ui_notebook_autobind.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] core/ui_notebook_autobind.py:65 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] core/window_manager.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/window_manager.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] core/window_manager.py:113 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] core/window_manager.py:37 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] core/zlecenia_loader.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] core/zlecenia_loader.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] dashboard_demo_fs.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] dashboard_demo_fs.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] dashboard_demo_fs.py:288 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] dashboard_demo_fs.py:77 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:79 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:95 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:156 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:160 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:209 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:211 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:213 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:215 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:219 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:220 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:224 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:234 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:235 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:236 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:237 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:241 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:250 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:251 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:259 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:263 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:265 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:268 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:269 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:271 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] dashboard_demo_fs.py:277 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] dirty_guard.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] dirty_guard.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] domain/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] domain/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] domain/bom/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] domain/bom/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] domain/bom/io.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] domain/bom/io.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] domain/magazyn.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] domain/magazyn.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] domain/orders.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] domain/orders.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] domain/tools/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] domain/tools/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] domain/tools/manager.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] domain/tools/manager.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] grafiki/__init__.py – Brak nagłówka # Wersja: ...
- **INFO** [HEADER] grafiki/__init__.py – Nagłówek # Plik wskazuje 'grafiki/__init__.py', ale plik to '__init__.py'
- **WARN** [HEADER] grafiki/shifts_schedule.py – Brak nagłówka # Wersja: ...
- **INFO** [HEADER] grafiki/shifts_schedule.py – Nagłówek # Plik wskazuje 'grafiki/shifts_schedule.py', ale plik to 'shifts_schedule.py'
- **WARN** [HEADER] gui/settings_action_handlers.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui/settings_action_handlers.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] gui/widgets_user_footer.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui/widgets_user_footer.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui/widgets_user_footer.py:45 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:52 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:55 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:168 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:175 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:179 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:184 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:191 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:193 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:199 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:206 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:210 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:215 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:222 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:230 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:231 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:232 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:235 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:265 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:269 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:270 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:281 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:283 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui/widgets_user_footer.py:314 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] gui_changelog.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_changelog.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_changelog.py:71 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] gui_changelog.py:67 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_changelog.py:69 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_logowanie.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_logowanie.py:502 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] gui_logowanie.py:162 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:171 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:177 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:191 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:194 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:196 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:200 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:203 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:217 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:219 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:223 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:225 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:226 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:234 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:238 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:241 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:244 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:249 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:252 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:274 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:286 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:290 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:294 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:302 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:305 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:362 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:365 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:367 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:370 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:398 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_logowanie.py:346 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_logowanie.py:357 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] gui_magazyn.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_magazyn.py:84 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:97 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:104 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:107 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:113 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:123 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:127 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:135 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:141 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:147 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:153 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:442 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:448 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:459 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:470 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:491 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:676 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:789 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn.py:238 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] gui_magazyn_add.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_magazyn_add.py:103 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:107 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:108 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:115 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:118 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:121 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:123 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:127 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:134 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:141 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:148 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:152 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:153 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:156 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:157 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:164 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:166 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_add.py:169 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_magazyn_autobind.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_magazyn_autobind.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] gui_magazyn_bom.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_magazyn_bom.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_magazyn_bom.py:621 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] gui_magazyn_bom.py:266 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:282 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:283 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:284 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:288 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:305 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:308 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:309 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:352 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:353 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:356 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:370 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:386 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:390 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:395 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:397 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:400 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:476 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:477 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:478 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:482 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:494 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:496 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:497 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:498 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:499 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:503 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:504 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:611 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:612 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_bom.py:620 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_magazyn_bridge.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_magazyn_bridge.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_magazyn_edit.py:61 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_edit.py:65 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_edit.py:71 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_edit.py:75 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_edit.py:86 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_edit.py:92 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_edit.py:93 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_edit.py:96 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_magazyn_kreator_bind.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_magazyn_kreator_bind.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] gui_magazyn_pz.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_magazyn_pz.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_magazyn_pz.py:118 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_pz.py:121 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_pz.py:123 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_pz.py:127 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_pz.py:131 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_pz.py:136 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_pz.py:137 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_pz.py:140 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_pz.py:160 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:21 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:60 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:62 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:66 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:68 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:71 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:77 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:79 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:81 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:107 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:108 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:121 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:123 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:127 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:129 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:131 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:133 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:162 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_magazyn_rezerwacje.py:163 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_maszyny.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_maszyny.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_maszyny.py:1296 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] gui_maszyny.py:221 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:229 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:231 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:233 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:240 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:260 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:262 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:264 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:266 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:274 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:277 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:278 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:279 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:330 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:367 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:372 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:373 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:519 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:617 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:743 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:983 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1002 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1008 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1010 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1014 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1110 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1113 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1117 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1126 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1132 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1146 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1147 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1152 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny.py:1294 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_maszyny_view.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_maszyny_view.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_maszyny_view.py:46 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:48 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:95 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:163 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:179 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:336 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:345 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:359 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:365 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:370 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:372 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:378 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:384 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:390 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_maszyny_view.py:328 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_maszyny_view.py:330 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] gui_narzedzia.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_narzedzia.py:447 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:459 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:461 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:1639 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:1640 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:1641 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:1642 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2007 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2437 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2438 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2441 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2466 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2474 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2485 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2487 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2493 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2502 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2512 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2522 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2533 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2765 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2766 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2768 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2769 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2771 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2777 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2778 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2835 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2842 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2843 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2846 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2852 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2866 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2911 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2912 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2944 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2954 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:2961 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3079 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3081 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3093 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3095 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3099 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3105 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3241 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3242 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3254 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3266 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3270 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3271 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3284 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3286 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3457 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3467 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3565 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3568 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3581 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3756 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3758 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3840 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3843 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3964 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia.py:3965 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_narzedzia_qr.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_narzedzia_qr.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_narzedzia_qr.py:129 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] gui_narzedzia_qr.py:112 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_narzedzia_qr.py:117 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_orders.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_orders.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_orders.py:30 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_orders.py:31 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_orders.py:35 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_orders.py:38 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_orders.py:40 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_orders.py:53 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_orders.py:57 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_orders.py:58 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_panel.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_panel.py:101 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:111 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:156 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:179 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:181 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:218 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:223 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:227 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:244 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:251 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:258 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:309 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:312 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:313 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:315 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:316 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:318 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:320 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:327 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:328 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:420 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:428 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:433 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:496 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:498 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:514 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:536 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:541 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:545 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:586 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:688 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:702 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:716 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:730 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:741 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:752 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:766 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:780 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:796 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:799 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:801 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_panel.py:430 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_panel.py:458 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] gui_products.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_products.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_products.py:60 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:69 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:71 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:72 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:75 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:78 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:81 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:88 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:93 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:103 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:105 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:106 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:109 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:112 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:115 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:135 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:137 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:138 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:141 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:144 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:147 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:355 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:358 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:360 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:362 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:366 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:378 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:380 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:387 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:390 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:403 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:404 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:405 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:445 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:510 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:512 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:516 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:518 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:522 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:530 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:532 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:543 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:545 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:552 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:555 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:568 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:569 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:570 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:617 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:665 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:667 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:671 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:678 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:680 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:682 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:686 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:688 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:692 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:699 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:701 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:703 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_products.py:752 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_profile.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_profile.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_profile.py:2272 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] gui_profile.py:412 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:413 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:416 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:417 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:419 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:424 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:426 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:428 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:435 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:436 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:438 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:466 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:470 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:477 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:478 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:479 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:480 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:481 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:482 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:483 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:486 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:492 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:592 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:593 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:596 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:604 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:607 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:615 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:642 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:649 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:652 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:655 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:661 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:671 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:675 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:678 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:686 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:687 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:697 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:712 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:713 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:714 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:717 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:750 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:751 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:752 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:753 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:754 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:792 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:800 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:894 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:967 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:972 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:977 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:991 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:996 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1001 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1004 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1012 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1019 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1027 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1032 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1037 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1041 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1045 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1047 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1050 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1055 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1290 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1295 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1301 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1308 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1312 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1321 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1330 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1338 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1343 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1354 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1363 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1372 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1382 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1389 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1393 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1398 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1406 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1441 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1448 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1465 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1480 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1490 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1491 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1506 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1519 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1526 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1539 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1544 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1548 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1551 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1552 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1557 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1563 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1569 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1572 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1574 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1576 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1582 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1587 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1644 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1648 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1653 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1662 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1671 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1675 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1681 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1702 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1709 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1729 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1735 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1739 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1742 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1744 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1748 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1751 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1753 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1759 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1767 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1780 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1781 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1784 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1792 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1816 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1867 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1875 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1876 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1883 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1890 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1894 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1903 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1934 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1935 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1938 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1979 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1982 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1992 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1994 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:1999 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2030 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2031 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2034 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2058 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2060 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2063 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2065 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2067 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2069 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2128 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2166 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2172 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2178 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2180 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2185 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2210 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2266 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_profile.py:2269 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_settings.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_settings.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_settings.py:3942 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] gui_settings.py:219 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:221 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:222 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:223 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:250 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:324 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:325 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:328 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:333 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:356 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:372 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:425 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:426 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:428 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:434 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:441 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:443 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:444 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:450 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:537 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:538 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:539 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:542 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:543 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:548 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:549 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:552 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:553 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:555 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:567 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:579 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:586 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:588 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:589 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:606 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:660 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:661 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:826 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:842 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:850 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:924 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:925 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1180 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1246 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1262 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1303 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1310 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1321 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1329 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1401 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1401 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1482 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1554 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1559 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1563 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1567 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1643 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1713 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1714 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1718 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:1808 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2057 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2067 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2089 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2090 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2136 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2155 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2174 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2193 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2204 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2211 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2222 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2246 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2288 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2293 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2327 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2330 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2344 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2348 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2360 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2361 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2366 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2372 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2377 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2382 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2814 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2821 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2831 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2846 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2869 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2879 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2888 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2900 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2915 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2929 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2932 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2936 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2937 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2938 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2941 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:2947 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3260 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3294 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3299 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3304 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3311 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3325 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3351 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3356 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3360 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3363 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3403 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3404 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3405 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3406 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3423 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3431 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3664 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3667 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3670 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3676 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3687 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3692 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3693 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_settings.py:3810 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3814 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3818 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3823 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3858 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3860 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3865 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3872 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3878 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3913 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3915 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3920 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] gui_settings.py:3928 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] gui_tool_editor.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_tool_editor.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_tool_editor.py:71 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:77 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:79 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:84 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:86 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:90 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:92 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:96 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:99 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:100 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tool_editor.py:103 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_tools.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_tools.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] gui_tools_config.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_tools_config.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_tools_config.py:63 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config.py:66 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config.py:67 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config.py:68 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_tools_config_advanced.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_tools_config_advanced.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_tools_config_advanced.py:118 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:119 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:127 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:130 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:132 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:136 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:139 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:140 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:142 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:146 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:147 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:148 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:153 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:154 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:156 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:158 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:162 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:168 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:174 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:176 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:177 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:180 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:185 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:186 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:188 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:190 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:193 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:199 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:205 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:207 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:208 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:211 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:216 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:217 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_tools_config_advanced.py:218 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_uzytkownicy.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_uzytkownicy.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_uzytkownicy.py:281 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:286 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:302 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:308 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:316 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:329 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:345 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:346 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:362 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:418 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:453 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:455 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:466 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:468 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:470 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:483 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:493 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:494 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:502 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:504 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:509 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:511 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:514 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:516 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:521 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:523 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:526 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:530 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:535 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:537 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:540 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:542 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:552 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:558 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:563 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:645 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:646 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:653 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:730 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:741 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:749 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:758 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:819 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:820 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:823 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:842 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_uzytkownicy.py:847 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_zlecenia.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_zlecenia.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_zlecenia.py:138 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia.py:165 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia.py:167 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia.py:229 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia.py:236 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia.py:244 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia.py:423 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_zlecenia_creator.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_zlecenia_creator.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_zlecenia_creator.py:40 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:43 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:46 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:48 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:50 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:62 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:83 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:95 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:97 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:108 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:111 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:113 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:121 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:134 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:136 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:139 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:141 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:149 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:172 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:179 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:182 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:184 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:187 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:195 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:206 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:211 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:230 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:233 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:235 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:238 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:241 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:244 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:246 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:249 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:251 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:254 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_creator.py:256 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] gui_zlecenia_detail.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] gui_zlecenia_detail.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] gui_zlecenia_detail.py:25 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:31 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:32 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:37 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:40 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:42 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:44 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:45 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:47 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:48 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:49 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:51 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:52 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:54 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:56 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:58 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:60 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:63 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:73 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:75 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:80 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] gui_zlecenia_detail.py:93 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] io_utils.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] io_utils.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] kreator_sprawdzenia.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] kreator_sprawdzenia.py – Brak nagłówka # Wersja: ...
- **INFO** [HEADER] kreator_sprawdzenia_plikow.py – Nagłówek # Plik wskazuje 'kreator_sprawdzenia.py', ale plik to 'kreator_sprawdzenia_plikow.py'
- **WARN** [HEADER] layout_prosty.py – Brak nagłówka # Plik: ...
- **INFO** [GUI] layout_prosty.py:9 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] layout_prosty.py:18 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] layout_prosty.py:22 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] layout_prosty.py:26 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] layout_prosty.py:30 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] layout_prosty.py:34 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] layout_prosty.py:38 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] layout_prosty.py:44 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] leaves.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] leaves.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] leaves.py:43 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] logger.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] logika_bom.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] logika_bom.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] logika_magazyn.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] logika_magazyn.py:103 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] logika_magazyn.py:265 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] logika_magazyn.py:367 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] logika_zadan.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] logika_zadan.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] logika_zakupy.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] logika_zakupy.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] magazyn_catalog.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] magazyn_catalog.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] magazyn_catalog.py:48 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] magazyn_catalog.py:48 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] magazyn_catalog.py:49 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] magazyn_io.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] magazyn_io.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] magazyn_io_pz.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] magazyn_io_pz.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] magazyn_slowniki.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] main.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] main.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] maszyny_logika.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] maszyny_logika.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] migrate_bom_to_polprodukty.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] migrate_bom_to_polprodukty.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] migrate_profiles_config.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] migrate_profiles_config.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] migrations.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] migrations.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] narzedzia_history.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] narzedzia_history.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] presence.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] presence.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] presence.py:64 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] presence_watcher.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] presence_watcher.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] presence_watcher.py:68 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] presence_watcher.py:154 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] presence_watcher.py:175 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] presence_watcher.py:175 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] presence_watcher.py:175 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] presence_watcher.py:201 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] profile_tasks.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] profile_tasks.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] profile_utils.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] profile_utils.py:109 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] profile_utils.py:404 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] rc1_audit_hook.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] rc1_audit_hook.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] rc1_audit_plus.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] rc1_audit_plus.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] rc1_data_bootstrap.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] rc1_data_bootstrap.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] rc1_data_bootstrap.py:353 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] rc1_data_bootstrap.py:354 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] rc1_hotfix_actions.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] rc1_hotfix_actions.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] rc1_magazyn_fix.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] rc1_magazyn_fix.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] rc1_profiles_bootstrap.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] rc1_profiles_bootstrap.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] rc1_theme_fix.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] rc1_theme_fix.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] runtime_paths.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] runtime_paths.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] scripts/check_json_format.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] scripts/check_json_format.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] scripts/gen_placeholder.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] scripts/gen_placeholder.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] scripts/wm_rc1_pack.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] scripts/wm_rc1_pack.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] services/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] services/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] services/activity_service.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] services/activity_service.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] services/activity_service.py:30 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] services/activity_service.py:93 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] services/activity_service.py:109 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] services/messages_service.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] services/messages_service.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] services/messages_service.py:35 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] services/messages_service.py:37 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] services/messages_service.py:67 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] services/messages_service.py:162 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] services/profile_service.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] services/profile_service.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] start.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] start.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] start.py:344 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] start.py:437 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] start.py:767 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] start.py:304 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] start.py:309 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] start.py:332 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] start.py:334 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] start.py:337 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] start.py:340 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] start.py:229 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] test_config_manager.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_config_manager.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_first_login_brygadzisty.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_first_login_brygadzisty.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_gui_logowanie.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_gui_logowanie.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_gui_logowanie.py:14 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_gui_logowanie.py:16 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_gui_narzedzia_config.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_gui_narzedzia_config.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_gui_narzedzia_config.py:73 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_gui_narzedzia_config.py:76 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_gui_narzedzia_enter.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_gui_narzedzia_enter.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_gui_narzedzia_enter.py:27 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_gui_narzedzia_enter.py:30 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_gui_narzedzia_files.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_gui_narzedzia_files.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_gui_narzedzia_files.py:49 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_gui_narzedzia_files.py:84 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_gui_narzedzia_qr.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_gui_narzedzia_qr.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_gui_narzedzia_tasks.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_gui_narzedzia_tasks.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_gui_narzedzia_tasks.py:44 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_gui_profile_roles.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_gui_profile_roles.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_gui_profile_smoke.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_gui_profile_smoke.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_gui_profile_smoke.py:50 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_kreator_gui.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_kreator_gui.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_kreator_gui.py:35 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_kreator_gui.py:43 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_kreator_wersji.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_logika_magazyn.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_logika_magazyn.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_logika_zlecenia_i_maszyny.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_logika_zlecenia_i_maszyny.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_narzedzia_history.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_narzedzia_history.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_presence_watcher.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_presence_watcher.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_priority_order.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_priority_order.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_profile_utils_regression.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_profile_utils_regression.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_shifts_schedule_weekend.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_shifts_schedule_weekend.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] test_start_user_activity.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_start_user_activity.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_start_user_activity.py:26 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] test_start_user_activity.py:39 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] test_start_user_activity.py:52 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] test_start_user_activity.py:25 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] test_start_user_activity.py:37 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] test_start_user_activity.py:38 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **INFO** [GUI] test_start_user_activity.py:51 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] test_startup_error.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_startup_error.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_startup_error.py:38 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] test_startup_error.py:47 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_startup_error.py:54 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_startup_error.py:67 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_startup_error.py:74 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_tool_media_io.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_tool_media_io.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] test_tool_media_io.py:69 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] test_tool_media_io.py:72 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] test_zlecenia_utils.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] test_zlecenia_utils.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/smoke_check.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/smoke_check.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/smoke_settings_window.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/smoke_settings_window.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tests/smoke_settings_window.py:37 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tests/test_audit_config.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_audit_config.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_backend_audit_runtime.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_backend_audit_runtime.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_bom_validation.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_bom_validation.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_config_helpers.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_config_helpers.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_config_manager.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_config_manager.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_dirty_guard.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_dirty_guard.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_domain_orders.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_domain_orders.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_dxf_preview.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_dxf_preview.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_magazyn_add.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_magazyn_add.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_magazyn_basic.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_magazyn_basic.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tests/test_gui_magazyn_basic.py:27 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tests/test_gui_magazyn_bom_ops.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_magazyn_bom_ops.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_magazyn_pz.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_magazyn_pz.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_narzedzia_missing_data.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_narzedzia_missing_data.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_narzedzia_numbering.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_narzedzia_numbering.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_narzedzia_task_order.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_narzedzia_task_order.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_narzedzia_tasks_mixed.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_narzedzia_tasks_mixed.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_panel_disabled_modules.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_panel_disabled_modules.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_gui_panel_logout_timer.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_panel_logout_timer.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tests/test_gui_panel_logout_timer.py:45 – Wywołanie mainloop() – upewnij się, że tylko jeden raz w całej aplikacji
- **INFO** [GUI] tests/test_gui_panel_logout_timer.py:44 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] tests/test_gui_panel_permissions.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_gui_panel_permissions.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_inventory_bridge.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_inventory_bridge.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_inventory_smoke.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_inventory_smoke.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_lines_from_text.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_lines_from_text.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_logika_zadan_api.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_logika_zadan_api.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_logika_zadan_tasks.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_logika_zadan_tasks.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_magazyn_catalog.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_magazyn_catalog.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_magazyn_io_comment_alias.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_magazyn_io_comment_alias.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_magazyn_io_core.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_magazyn_io_core.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_magazyn_io_pz.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_magazyn_io_pz.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_moduly_manifest.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_moduly_manifest.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_patcher.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_patcher.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_produkty_bom_io.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_produkty_bom_io.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_profile_disabled_modules_ui.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_profile_disabled_modules_ui.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_profile_utils_manifest.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_profile_utils_manifest.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_profiles_settings_gui.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_profiles_settings_gui.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_settings_gui.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_settings_gui.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_settings_manager.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_settings_manager.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_settings_root.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_settings_root.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_settings_tools_config_refresh.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_settings_tools_config_refresh.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tests/test_settings_tools_config_refresh.py:75 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] tests/test_settings_tools_config_refresh.py:88 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] tests/test_settings_tools_config_refresh.py:95 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tests/test_settings_window.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_settings_window.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tests/test_settings_window.py:55 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] tests/test_settings_window.py:91 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] tests/test_settings_window.py:170 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tests/test_shifts_schedule.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_shifts_schedule.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_shifts_schedule_anchor.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_shifts_schedule_anchor.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_shifts_schedule_default_override.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_shifts_schedule_default_override.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_tools_autocheck.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_tools_autocheck.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_tools_history.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_tools_history.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_tools_templates.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_tools_templates.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_tools_types_statuses.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_tools_types_statuses.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_tools_wrappers.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_tools_wrappers.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_ui_hover.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_ui_hover.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tests/test_ui_hover.py:22 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tests/test_update_logging.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_update_logging.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tests/test_updates_push_branch.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_updates_push_branch.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tests/test_updates_push_branch.py:38 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tests/test_widok_hali_machines_view.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tests/test_widok_hali_machines_view.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tests/test_widok_hali_machines_view.py:60 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tools/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/audit_machines_diff.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/audit_machines_diff.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/audit_settings_values.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/audit_settings_values.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/check_machines_file.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/check_machines_file.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/find_audit_limits.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/find_audit_limits.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tools/find_audit_limits.py:33 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tools/find_dialog_calls.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/find_dialog_calls.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tools/find_dialog_calls.py:35 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tools/find_hardcoded_paths.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/find_hardcoded_paths.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/fix_settings_schema_rooms.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/fix_settings_schema_rooms.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tools/fix_settings_schema_rooms.py:111 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tools/importers/build_tools_index.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/importers/build_tools_index.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/importers/tools_from_excel.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/importers/tools_from_excel.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tools/importers/tools_from_excel.py:40 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tools/inspect_machines.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/inspect_machines.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/list_branch_changes.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/list_branch_changes.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/merge_machines_json.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/merge_machines_json.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/patcher.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/patcher.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/repair_json.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/roadmap_apply_updates.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/roadmap_apply_updates.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/scan_legacy_paths.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/scan_legacy_paths.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/scan_missing_root.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/scan_missing_root.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tools/scan_missing_root.py:56 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] tools/scan_missing_root.py:76 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tools/scan_settings_duplicates.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/scan_settings_duplicates.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/seed_wm_data.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/seed_wm_data.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/seed_wm_maszyny_przeglady.py – Brak nagłówka # Plik: ...
- **INFO** [GUI] tools/seed_wm_maszyny_przeglady.py:43 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tools/update_roadmap_from_git.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/update_roadmap_from_git.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/validators/profiles_validator.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/validators/profiles_validator.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/validators/settings_paths_validator.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/validators/settings_paths_validator.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/validators/tools_schema_validator.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/validators/tools_schema_validator.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools/wm_sync.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools/wm_sync.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools_autocheck.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools_autocheck.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools_config_loader.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools_config_loader.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] tools_config_loader.py:64 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] tools_history.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools_history.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] tools_templates.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] tools_templates.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] ui_dialogs_safe.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] ui_dialogs_safe.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] ui_hover.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] ui_hover.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] ui_hover.py:102 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] ui_theme.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] ui_theme.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] ui_theme_guard.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] ui_theme_guard.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] ui_utils.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] ui_utils.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] updater.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] updater.py:260 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:305 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:308 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:313 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:317 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:324 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:330 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:334 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:336 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:340 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:345 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:351 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:352 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:353 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:362 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:366 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:601 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:610 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:613 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:624 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] updater.py:625 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] updates_utils.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] updates_utils.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] ustawienia_magazyn.py – Brak nagłówka # Plik: ...
- **INFO** [GUI] ustawienia_magazyn.py:95 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:121 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:122 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:123 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:133 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:139 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:142 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:147 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:148 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:155 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:157 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:162 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:164 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:165 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:166 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:169 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:171 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:176 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:178 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:179 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:180 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:223 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:230 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:231 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:233 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:234 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:236 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:238 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:239 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:249 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:250 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:251 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:260 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:261 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:263 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:269 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:277 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:279 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:280 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:281 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:284 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:286 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:287 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_magazyn.py:288 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] ustawienia_produkty_bom.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] ustawienia_produkty_bom.py:99 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:103 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:107 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:109 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:111 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:113 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:115 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:118 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:120 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:121 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:122 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:123 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:125 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:126 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:127 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:128 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:129 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:131 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:132 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:133 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:134 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:137 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:140 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:142 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:150 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:156 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:171 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:283 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:304 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:317 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:318 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:323 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:325 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:327 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:328 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:331 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:332 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:336 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:338 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:340 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_produkty_bom.py:386 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] ustawienia_systemu.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] ustawienia_systemu.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] ustawienia_uzytkownicy.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] ustawienia_uzytkownicy.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] ustawienia_uzytkownicy.py:68 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:69 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:72 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:75 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:87 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:215 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:217 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:219 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:221 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:228 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:230 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:234 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:236 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:243 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:246 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:247 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:248 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] ustawienia_uzytkownicy.py:279 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] utils/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils/dirty_guard.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils/dirty_guard.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils/error_dialogs.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils/error_dialogs.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] utils/error_dialogs.py:88 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] utils/error_dialogs.py:91 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] utils/error_dialogs.py:98 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] utils/error_dialogs.py:104 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] utils/error_dialogs.py:110 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] utils/error_dialogs.py:33 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] utils/gui_helpers.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils/gui_helpers.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils/json_io.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils/json_io.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils/moduly.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils/moduly.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils/path_utils.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils/path_utils.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils_json.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils_json.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils_maszyny.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils_maszyny.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils_orders.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils_orders.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils_paths.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils_paths.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] utils_tools.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] utils_tools.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] widok_hali/__init__.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/__init__.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] widok_hali/a_star.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/a_star.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] widok_hali/animator.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/animator.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] widok_hali/const.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/const.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] widok_hali/controller.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/controller.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] widok_hali/controller.py:102 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] widok_hali/machines_view.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/machines_view.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] widok_hali/machines_view.py:56 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/machines_view.py:63 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/machines_view.py:94 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/machines_view.py:216 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/machines_view.py:233 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/machines_view.py:301 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/machines_view.py:306 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/machines_view.py:313 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] widok_hali/models.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/models.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] widok_hali/renderer.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/renderer.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] widok_hali/renderer.py:95 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/renderer.py:325 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/renderer.py:500 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **INFO** [GUI] widok_hali/renderer.py:374 – Użycie .after(...) – sprawdź, czy nie gubi referencji i czy czyszczone przy zamykaniu
- **WARN** [HEADER] widok_hali/storage.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] widok_hali/storage.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] wm_access.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] wm_access.py – Brak nagłówka # Wersja: ...
- **INFO** [GUI] wm_access.py:116 – Mieszanie pack/grid/place w tym samym kontenerze może powodować błędy layoutu
- **WARN** [HEADER] wm_audit_runtime.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] wm_audit_runtime.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] wm_log.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] wm_log.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] wm_theme.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] wm_theme.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] wm_tools_helpers.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] wm_tools_helpers.py – Brak nagłówka # Wersja: ...
- **INFO** [HEADER] wymagane_pliki_version_check.py – Nagłówek # Plik wskazuje 'kreator_sprawdzenia.py', ale plik to 'wymagane_pliki_version_check.py'
- **WARN** [HEADER] zadania_assign_io.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] zadania_assign_io.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] zlecenia_logika.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] zlecenia_logika.py – Brak nagłówka # Wersja: ...
- **WARN** [HEADER] zlecenia_utils.py – Brak nagłówka # Plik: ...
- **WARN** [HEADER] zlecenia_utils.py – Brak nagłówka # Wersja: ...
- **WARN** [IMPORT] config_manager.py :: utils_json.py :: config_manager.py – Cykliczne importy (rozważ refaktor)
- **WARN** [IMPORT] start.py :: ustawienia_systemu.py :: gui_settings.py :: start.py – Cykliczne importy (rozważ refaktor)
- **WARN** [IMPORT] ustawienia_systemu.py :: gui_settings.py :: ustawienia_produkty_bom.py :: ustawienia_systemu.py – Cykliczne importy (rozważ refaktor)
- **WARN** [IMPORT] gui_logowanie.py :: gui_panel.py :: gui_narzedzia.py :: start.py :: gui_logowanie.py – Cykliczne importy (rozważ refaktor)
- **WARN** [IMPORT] gui_panel.py :: gui_narzedzia.py :: start.py :: gui_panel.py – Cykliczne importy (rozważ refaktor)
- **WARN** [IMPORT] gui_logowanie.py :: gui_panel.py :: gui_logowanie.py – Cykliczne importy (rozważ refaktor)
- **WARN** [IMPORT] gui_zlecenia.py :: gui_zlecenia_creator.py :: gui_zlecenia.py – Cykliczne importy (rozważ refaktor)
- **INFO** [STYLE] audyt_mw.py, /workspace/Warsztat-Menager/config_manager.py, /workspace/Warsztat-Menager/core/settings_manager.py, /workspace/Warsztat-Menager/core/window_manager.py, /workspace/Warsztat-Menager/dashboard_demo_fs.py, /workspace/Warsztat-Menager/dirty_guard.py, /workspace/Warsztat-Menager/gui/settings_action_handlers.py, /workspace/Warsztat-Menager/gui_magazyn.py, /workspace/Warsztat-Menager/gui_magazyn_add.py, /workspace/Warsztat-Menager/gui_magazyn_bom.py, /workspace/Warsztat-Menager/gui_magazyn_edit.py, /workspace/Warsztat-Menager/gui_magazyn_pz.py, /workspace/Warsztat-Menager/gui_maszyny.py, /workspace/Warsztat-Menager/gui_maszyny_view.py, /workspace/Warsztat-Menager/gui_narzedzia.py, /workspace/Warsztat-Menager/gui_narzedzia_qr.py, /workspace/Warsztat-Menager/gui_products.py, /workspace/Warsztat-Menager/gui_profile.py, /workspace/Warsztat-Menager/gui_settings.py, /workspace/Warsztat-Menager/gui_tool_editor.py, /workspace/Warsztat-Menager/gui_tools_config.py, /workspace/Warsztat-Menager/gui_tools_config_advanced.py, /workspace/Warsztat-Menager/gui_zlecenia.py, /workspace/Warsztat-Menager/layout_prosty.py, /workspace/Warsztat-Menager/rc1_audit_hook.py, /workspace/Warsztat-Menager/start.py, /workspace/Warsztat-Menager/test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_gui_profile_smoke.py, /workspace/Warsztat-Menager/test_presence_watcher.py, /workspace/Warsztat-Menager/test_startup_error.py, /workspace/Warsztat-Menager/test_tool_media_io.py, /workspace/Warsztat-Menager/tests/test_gui_magazyn_basic.py, /workspace/Warsztat-Menager/tests/test_gui_narzedzia_tasks_mixed.py, /workspace/Warsztat-Menager/tests/test_inventory_bridge.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py, /workspace/Warsztat-Menager/tests/test_widok_hali_machines_view.py, /workspace/Warsztat-Menager/tools/scan_missing_root.py, /workspace/Warsztat-Menager/ui_hover.py, /workspace/Warsztat-Menager/updater.py, /workspace/Warsztat-Menager/ustawienia_magazyn.py, /workspace/Warsztat-Menager/ustawienia_uzytkownicy.py, /workspace/Warsztat-Menager/utils/dirty_guard.py, /workspace/Warsztat-Menager/widok_hali/animator.py, /workspace/Warsztat-Menager/widok_hali/controller.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py, /workspace/Warsztat-Menager/widok_hali/renderer.py – Definicja '__init__' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] audyt_mw.py, /workspace/Warsztat-Menager/config/paths.py, /workspace/Warsztat-Menager/leaves.py – Definicja '_read' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] backend/audit/wm_audit_runtime.py, /workspace/Warsztat-Menager/gui_settings.py, /workspace/Warsztat-Menager/rc1_audit_plus.py – Definicja '_exists' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] backend/audit/wm_audit_runtime.py, /workspace/Warsztat-Menager/config_manager.py – Definicja '_normalized' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] backend/audit/wm_audit_runtime.py, /workspace/Warsztat-Menager/gui_narzedzia.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/tools/validators/settings_paths_validator.py – Definicja 'add' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] backend/audit/wm_audit_runtime.py, /workspace/Warsztat-Menager/rc1_audit_plus.py – Definicja 'run' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] backend/updater.py, /workspace/Warsztat-Menager/tools/patcher.py – Definicja '_run' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] backend/updater.py, /workspace/Warsztat-Menager/utils_maszyny.py – Definicja '_timestamp' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] bom.py, /workspace/Warsztat-Menager/logika_bom.py – Definicja 'compute_sr_for_pp' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config/paths.py, /workspace/Warsztat-Menager/rc1_audit_plus.py – Definicja '_data_root' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config/paths.py, /workspace/Warsztat-Menager/core/orders_storage.py – Definicja '_project_root' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config/paths.py, /workspace/Warsztat-Menager/runtime_paths.py – Definicja 'get_app_root' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config/paths.py, /workspace/Warsztat-Menager/config_manager.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja 'get_path' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/rc1_data_bootstrap.py – Definicja '_apply_root_defaults' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/gui_products.py, /workspace/Warsztat-Menager/logika_magazyn.py, /workspace/Warsztat-Menager/magazyn_catalog.py, /workspace/Warsztat-Menager/magazyn_io.py, /workspace/Warsztat-Menager/magazyn_io_pz.py, /workspace/Warsztat-Menager/updater.py, /workspace/Warsztat-Menager/ustawienia_produkty_bom.py, /workspace/Warsztat-Menager/utils/json_io.py, /workspace/Warsztat-Menager/wm_access.py, /workspace/Warsztat-Menager/zlecenia_logika.py – Definicja '_ensure_dirs' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/gui_magazyn_bom.py, /workspace/Warsztat-Menager/gui_profile.py, /workspace/Warsztat-Menager/logika_zakupy.py, /workspace/Warsztat-Menager/magazyn_catalog.py, /workspace/Warsztat-Menager/magazyn_io.py, /workspace/Warsztat-Menager/magazyn_io_pz.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja '_load_json' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/core/logging_config.py, /workspace/Warsztat-Menager/gui_magazyn_autobind.py, /workspace/Warsztat-Menager/profile_utils.py, /workspace/Warsztat-Menager/rc1_audit_plus.py, /workspace/Warsztat-Menager/rc1_data_bootstrap.py, /workspace/Warsztat-Menager/rc1_profiles_bootstrap.py, /workspace/Warsztat-Menager/tools/importers/tools_from_excel.py, /workspace/Warsztat-Menager/utils/moduly.py – Definicja '_norm' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/gui_magazyn_bom.py, /workspace/Warsztat-Menager/logika_zakupy.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja '_save_json' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/core/settings_manager.py, /workspace/Warsztat-Menager/gui_settings.py, /workspace/Warsztat-Menager/test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_startup_error.py, /workspace/Warsztat-Menager/test_tool_media_io.py, /workspace/Warsztat-Menager/tests/test_gui_magazyn_bom_ops.py, /workspace/Warsztat-Menager/tests/test_gui_panel_logout_timer.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py – Definicja 'get' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja 'get_machines_path' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/utils_json.py – Definicja 'get_root' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/magazyn_io.py, /workspace/Warsztat-Menager/magazyn_slowniki.py, /workspace/Warsztat-Menager/tests/test_gui_magazyn_basic.py, /workspace/Warsztat-Menager/tools/check_machines_file.py – Definicja 'load' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/core/paths_compat.py, /workspace/Warsztat-Menager/core/settings_manager.py – Definicja 'path_backup' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/core/paths_compat.py, /workspace/Warsztat-Menager/core/settings_manager.py – Definicja 'path_data' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/core/paths_compat.py – Definicja 'path_root' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/gui_magazyn.py, /workspace/Warsztat-Menager/widok_hali/controller.py – Definicja 'refresh' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/gui_maszyny.py, /workspace/Warsztat-Menager/utils_json.py – Definicja 'resolve_rel' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/core/settings_manager.py, /workspace/Warsztat-Menager/gui_narzedzia.py, /workspace/Warsztat-Menager/gui_products.py, /workspace/Warsztat-Menager/gui_settings.py, /workspace/Warsztat-Menager/magazyn_io.py, /workspace/Warsztat-Menager/magazyn_slowniki.py – Definicja 'save' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/gui_settings.py, /workspace/Warsztat-Menager/ustawienia_magazyn.py – Definicja 'save_all' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] config_manager.py, /workspace/Warsztat-Menager/core/settings_manager.py, /workspace/Warsztat-Menager/gui_settings.py, /workspace/Warsztat-Menager/test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py – Definicja 'set' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] core/orders_storage.py, /workspace/Warsztat-Menager/presence.py – Definicja '_atomic_write' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] core/orders_storage.py, /workspace/Warsztat-Menager/utils_json.py – Definicja '_ensure_parent' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] core/orders_storage.py, /workspace/Warsztat-Menager/domain/orders.py, /workspace/Warsztat-Menager/zlecenia_utils.py – Definicja 'load_orders' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] core/paths_compat.py, /workspace/Warsztat-Menager/core/settings_manager.py – Definicja 'path_assets' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] core/settings_manager.py, /workspace/Warsztat-Menager/widok_hali/renderer.py – Definicja 'reload' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] core/ui_notebook_autobind.py, /workspace/Warsztat-Menager/core/window_manager.py, /workspace/Warsztat-Menager/ustawienia_systemu.py – Definicja '_on_tab_changed' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] core/window_manager.py, /workspace/Warsztat-Menager/ustawienia_systemu.py – Definicja '_on_close' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] core/window_manager.py, /workspace/Warsztat-Menager/gui_maszyny.py – Definicja 'show' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dashboard_demo_fs.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja 'load_awarie' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dashboard_demo_fs.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja 'load_hale' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dashboard_demo_fs.py, /workspace/Warsztat-Menager/widok_hali/controller.py – Definicja 'on_click' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dashboard_demo_fs.py, /workspace/Warsztat-Menager/widok_hali/controller.py – Definicja 'on_drag' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dashboard_demo_fs.py, /workspace/Warsztat-Menager/gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/controller.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja 'redraw' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dashboard_demo_fs.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja 'save_hale' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dirty_guard.py, /workspace/Warsztat-Menager/utils/dirty_guard.py – Definicja 'DirtyGuard' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dirty_guard.py, /workspace/Warsztat-Menager/gui_narzedzia.py, /workspace/Warsztat-Menager/rc1_hotfix_actions.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja '_log' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] dirty_guard.py, /workspace/Warsztat-Menager/utils/dirty_guard.py – Definicja 'check_before' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] domain/orders.py, /workspace/Warsztat-Menager/zlecenia_utils.py – Definicja '_seq_path' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] domain/orders.py, /workspace/Warsztat-Menager/zlecenia_utils.py – Definicja 'save_order' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] grafiki/shifts_schedule.py, /workspace/Warsztat-Menager/profile_utils.py – Definicja '_default_users_file' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] grafiki/shifts_schedule.py, /workspace/Warsztat-Menager/ustawienia_uzytkownicy.py – Definicja '_load_users' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] grafiki/shifts_schedule.py, /workspace/Warsztat-Menager/presence_watcher.py, /workspace/Warsztat-Menager/rc1_audit_plus.py, /workspace/Warsztat-Menager/utils/json_io.py – Definicja '_read_json' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui/settings_action_handlers.py, /workspace/Warsztat-Menager/test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_tool_media_io.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'bind' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui/settings_action_handlers.py, /workspace/Warsztat-Menager/gui_settings.py – Definicja 'wm_dbg' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui/settings_action_handlers.py, /workspace/Warsztat-Menager/gui_settings.py – Definicja 'wm_err' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui/settings_action_handlers.py, /workspace/Warsztat-Menager/gui_settings.py – Definicja 'wm_info' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui/widgets_user_footer.py, /workspace/Warsztat-Menager/gui_profile.py – Definicja '_is_task_urgent' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui/widgets_user_footer.py, /workspace/Warsztat-Menager/gui_logowanie.py, /workspace/Warsztat-Menager/gui_profile.py, /workspace/Warsztat-Menager/gui_zlecenia.py – Definicja '_on_destroy' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui/widgets_user_footer.py, /workspace/Warsztat-Menager/gui_logowanie.py, /workspace/Warsztat-Menager/presence.py, /workspace/Warsztat-Menager/presence_watcher.py, /workspace/Warsztat-Menager/start.py – Definicja '_tick' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_logowanie.py, /workspace/Warsztat-Menager/rc1_profiles_bootstrap.py, /workspace/Warsztat-Menager/wm_access.py – Definicja '_profiles_path' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn.py, /workspace/Warsztat-Menager/gui_magazyn_bom.py, /workspace/Warsztat-Menager/gui_products.py, /workspace/Warsztat-Menager/gui_settings.py, /workspace/Warsztat-Menager/ustawienia_uzytkownicy.py – Definicja '_build_ui' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn.py, /workspace/Warsztat-Menager/gui_zlecenia.py – Definicja '_on_double_click' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn.py, /workspace/Warsztat-Menager/gui_magazyn_add.py – Definicja 'open_window' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_add.py, /workspace/Warsztat-Menager/gui_magazyn_edit.py, /workspace/Warsztat-Menager/gui_magazyn_pz.py, /workspace/Warsztat-Menager/tests/test_dirty_guard.py – Definicja 'on_save' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_autobind.py, /workspace/Warsztat-Menager/gui_magazyn_kreator_bind.py – Definicja '_find_treeview' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_bom.py, /workspace/Warsztat-Menager/zadania_assign_io.py – Definicja '_load_all' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_bom.py, /workspace/Warsztat-Menager/gui_products.py – Definicja 'delete_polprodukt' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_bom.py, /workspace/Warsztat-Menager/gui_products.py – Definicja 'delete_surowiec' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_edit.py, /workspace/Warsztat-Menager/gui_magazyn_pz.py, /workspace/Warsztat-Menager/logika_magazyn.py, /workspace/Warsztat-Menager/logika_zadan.py – Definicja '_safe_load' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_edit.py, /workspace/Warsztat-Menager/gui_magazyn_pz.py – Definicja '_safe_save' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_kreator_bind.py, /workspace/Warsztat-Menager/start.py – Definicja '_resolve_role' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_pz.py, /workspace/Warsztat-Menager/leaves.py, /workspace/Warsztat-Menager/presence_watcher.py – Definicja '_cfg' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_pz.py, /workspace/Warsztat-Menager/rc1_data_bootstrap.py – Definicja '_get' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_magazyn_pz.py, /workspace/Warsztat-Menager/gui_magazyn_rezerwacje.py – Definicja '_parse_qty' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_zlecenia.py – Definicja '_build_tree' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/widok_hali/renderer.py – Definicja '_draw_all' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja '_load_background' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja '_map_bg_to_canvas' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_maszyny_view.py – Definicja '_map_canvas_to_bg' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/logika_magazyn.py, /workspace/Warsztat-Menager/presence_watcher.py – Definicja '_now' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/updater.py, /workspace/Warsztat-Menager/ustawienia_produkty_bom.py, /workspace/Warsztat-Menager/ustawienia_uzytkownicy.py – Definicja '_ok' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_zlecenia.py – Definicja '_on_add' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/ui_hover.py – Definicja '_on_leave' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/ui_hover.py – Definicja '_on_motion' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_tool_editor.py – Definicja '_on_save' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_profile.py – Definicja '_refresh_view' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/maszyny_logika.py – Definicja '_save_machines' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_narzedzia.py, /workspace/Warsztat-Menager/gui_zlecenia.py – Definicja 'get_config' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny.py, /workspace/Warsztat-Menager/gui_panel.py – Definicja 'panel_maszyny' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja 'MachinesView' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja '_build_footer' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja '_draw_grid' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja '_draw_machine_point' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/controller.py – Definicja '_machine_at' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/renderer.py – Definicja '_on_click' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/renderer.py – Definicja '_on_drag' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/renderer.py – Definicja '_on_drop' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja 'set_grid_visible' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja 'set_records' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja 'set_scale_mode' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja 'toggle_grid' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_maszyny_view.py, /workspace/Warsztat-Menager/widok_hali/machines_view.py – Definicja 'widget' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_tools_config_advanced.py – Definicja '_add_task' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/start.py – Definicja '_dbg' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_narzedzia_qr.py, /workspace/Warsztat-Menager/rc1_data_bootstrap.py, /workspace/Warsztat-Menager/rc1_profiles_bootstrap.py – Definicja '_load_config' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_tool_editor.py – Definicja '_on_status_selected' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_narzedzia_qr.py – Definicja '_read_tool' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_tools_config_advanced.py – Definicja '_refresh_tasks' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_narzedzia_qr.py – Definicja '_resolve_tools_dir' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/rc1_data_bootstrap.py, /workspace/Warsztat-Menager/rc1_profiles_bootstrap.py – Definicja '_save_config' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_narzedzia_qr.py – Definicja '_save_tool' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/wm_tools_helpers.py – Definicja 'ensure_task_shape' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_profile.py, /workspace/Warsztat-Menager/gui_uzytkownicy.py, /workspace/Warsztat-Menager/start.py, /workspace/Warsztat-Menager/ui_theme.py, /workspace/Warsztat-Menager/ui_theme_guard.py – Definicja 'ensure_theme_applied' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/utils_json.py – Definicja 'normalize_tools_doc' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/utils_json.py – Definicja 'normalize_tools_index' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_panel.py – Definicja 'panel_narzedzia' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia.py, /workspace/Warsztat-Menager/gui_profile.py – Definicja 'row' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia_qr.py, /workspace/Warsztat-Menager/rc1_hotfix_actions.py, /workspace/Warsztat-Menager/start.py – Definicja '_error' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_narzedzia_qr.py, /workspace/Warsztat-Menager/rc1_hotfix_actions.py, /workspace/Warsztat-Menager/start.py – Definicja '_info' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_orders.py, /workspace/Warsztat-Menager/gui_tool_editor.py, /workspace/Warsztat-Menager/gui_zlecenia_creator.py, /workspace/Warsztat-Menager/gui_zlecenia_detail.py, /workspace/Warsztat-Menager/start.py, /workspace/Warsztat-Menager/ui_theme.py, /workspace/Warsztat-Menager/ustawienia_systemu.py, /workspace/Warsztat-Menager/wm_theme.py – Definicja 'apply_theme' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_panel.py, /workspace/Warsztat-Menager/gui_uzytkownicy.py – Definicja '_open_profile' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_panel.py, /workspace/Warsztat-Menager/gui_profile.py – Definicja '_submit' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_panel.py, /workspace/Warsztat-Menager/rc1_hotfix_actions.py, /workspace/Warsztat-Menager/rc1_profiles_bootstrap.py – Definicja '_warn' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_panel.py, /workspace/Warsztat-Menager/logger.py, /workspace/Warsztat-Menager/presence.py, /workspace/Warsztat-Menager/presence_watcher.py – Definicja 'log_akcja' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_panel.py, /workspace/Warsztat-Menager/gui_uzytkownicy.py – Definicja 'panel_uzytkownicy' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_panel.py, /workspace/Warsztat-Menager/gui_zlecenia.py – Definicja 'panel_zlecenia' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_panel.py, /workspace/Warsztat-Menager/gui_profile.py, /workspace/Warsztat-Menager/gui_uzytkownicy.py – Definicja 'uruchom_panel' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_products.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja '_read_json_list' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_profile.py, /workspace/Warsztat-Menager/services/activity_service.py – Definicja '_parse_timestamp' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_profile.py, /workspace/Warsztat-Menager/gui_zlecenia.py, /workspace/Warsztat-Menager/gui_zlecenia_creator.py, /workspace/Warsztat-Menager/ustawienia_produkty_bom.py – Definicja '_refresh' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_profile.py, /workspace/Warsztat-Menager/gui_settings.py, /workspace/Warsztat-Menager/gui_tools_config.py, /workspace/Warsztat-Menager/gui_tools_config_advanced.py, /workspace/Warsztat-Menager/gui_uzytkownicy.py, /workspace/Warsztat-Menager/tools/roadmap_apply_updates.py, /workspace/Warsztat-Menager/ustawienia_produkty_bom.py – Definicja '_save' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_profile.py, /workspace/Warsztat-Menager/ustawienia_produkty_bom.py, /workspace/Warsztat-Menager/ustawienia_uzytkownicy.py – Definicja 'make_tab' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_settings.py, /workspace/Warsztat-Menager/ustawienia_systemu.py, /workspace/Warsztat-Menager/utils/dirty_guard.py – Definicja '_mark_dirty' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_settings.py, /workspace/Warsztat-Menager/gui_uzytkownicy.py, /workspace/Warsztat-Menager/gui_zlecenia_creator.py – Definicja '_on_select' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_settings.py, /workspace/Warsztat-Menager/ustawienia_systemu.py – Definicja 'refresh_panel' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_tool_editor.py, /workspace/Warsztat-Menager/test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_startup_error.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'destroy' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_tools.py, /workspace/Warsztat-Menager/rc1_audit_plus.py – Definicja '_load_cfg' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_tools_config.py, /workspace/Warsztat-Menager/gui_tools_config_advanced.py – Definicja 'ToolsConfigDialog' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_tools_config_advanced.py, /workspace/Warsztat-Menager/ustawienia_uzytkownicy.py – Definicja '_save_now' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_uzytkownicy.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja 'get_all_users' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_uzytkownicy.py, /workspace/Warsztat-Menager/wm_access.py – Definicja 'get_disabled_modules_for' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_uzytkownicy.py, /workspace/Warsztat-Menager/profile_utils.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja 'get_user' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_uzytkownicy.py, /workspace/Warsztat-Menager/profile_utils.py, /workspace/Warsztat-Menager/wm_access.py – Definicja 'load_profiles' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_uzytkownicy.py, /workspace/Warsztat-Menager/profile_utils.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja 'save_user' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_uzytkownicy.py, /workspace/Warsztat-Menager/wm_access.py – Definicja 'set_modules_visibility_map' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_uzytkownicy.py, /workspace/Warsztat-Menager/utils/moduly.py – Definicja 'zaladuj_manifest' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] gui_zlecenia.py, /workspace/Warsztat-Menager/widok_hali/animator.py – Definicja 'cancel_all' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] kreator_sprawdzenia.py, /workspace/Warsztat-Menager/tools/list_branch_changes.py – Definicja 'parse_args' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] kreator_sprawdzenia_plikow.py, /workspace/Warsztat-Menager/wymagane_pliki_version_check.py – Definicja 'sprawdz' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] leaves.py, /workspace/Warsztat-Menager/presence_watcher.py, /workspace/Warsztat-Menager/services/messages_service.py – Definicja '_path' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] leaves.py, /workspace/Warsztat-Menager/tests/test_audit_config.py, /workspace/Warsztat-Menager/tests/test_logika_zadan_tasks.py – Definicja '_write' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] leaves.py, /workspace/Warsztat-Menager/presence.py, /workspace/Warsztat-Menager/presence_watcher.py – Definicja 'set_config' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] logika_bom.py, /workspace/Warsztat-Menager/zlecenia_logika.py – Definicja 'compute_material_needs' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] logika_magazyn.py, /workspace/Warsztat-Menager/magazyn_io.py – Definicja '_log_mag' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] logika_magazyn.py, /workspace/Warsztat-Menager/zlecenia_logika.py – Definicja 'rezerwuj_materialy' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] logika_zadan.py, /workspace/Warsztat-Menager/tools_autocheck.py – Definicja 'should_autocheck' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] logika_zakupy.py, /workspace/Warsztat-Menager/zlecenia_logika.py – Definicja '_next_id' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] magazyn_io.py, /workspace/Warsztat-Menager/magazyn_io_pz.py – Definicja 'ensure_in_katalog' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] magazyn_io.py, /workspace/Warsztat-Menager/magazyn_io_pz.py – Definicja 'generate_pz_id' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] magazyn_io.py, /workspace/Warsztat-Menager/magazyn_io_pz.py – Definicja 'save_pz' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] magazyn_io.py, /workspace/Warsztat-Menager/magazyn_io_pz.py – Definicja 'update_stany_after_pz' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] maszyny_logika.py, /workspace/Warsztat-Menager/utils_maszyny.py, /workspace/Warsztat-Menager/widok_hali/__init__.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja 'load_machines' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] migrate_bom_to_polprodukty.py, /workspace/Warsztat-Menager/migrations.py – Definicja 'migrate' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] narzedzia_history.py, /workspace/Warsztat-Menager/tools_history.py – Definicja 'append_tool_history' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] presence.py, /workspace/Warsztat-Menager/presence_watcher.py – Definicja 'TclError' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] presence.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja '_presence_path' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] presence.py, /workspace/Warsztat-Menager/services/messages_service.py – Definicja '_read_all' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] presence_watcher.py, /workspace/Warsztat-Menager/utils/json_io.py – Definicja '_write_json' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] profile_tasks.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja '_load_tasks_raw' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] profile_tasks.py, /workspace/Warsztat-Menager/profile_utils.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja 'get_tasks_for' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] profile_tasks.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja 'workload_for' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] profile_utils.py, /workspace/Warsztat-Menager/services/profile_service.py – Definicja 'write_users' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] rc1_audit_plus.py, /workspace/Warsztat-Menager/tools_config_loader.py – Definicja '_read_text' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] rc1_data_bootstrap.py, /workspace/Warsztat-Menager/rc1_hotfix_actions.py – Definicja '_ask_open_file' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] rc1_data_bootstrap.py, /workspace/Warsztat-Menager/rc1_hotfix_actions.py – Definicja '_ask_save_file' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] rc1_data_bootstrap.py, /workspace/Warsztat-Menager/rc1_profiles_bootstrap.py – Definicja '_ask_yesno' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] rc1_data_bootstrap.py, /workspace/Warsztat-Menager/ui_dialogs_safe.py – Definicja '_bootstrap_active' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] rc1_data_bootstrap.py, /workspace/Warsztat-Menager/rc1_profiles_bootstrap.py – Definicja '_ensure_dir_for' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] services/activity_service.py, /workspace/Warsztat-Menager/services/messages_service.py – Definicja '_append' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] services/activity_service.py, /workspace/Warsztat-Menager/services/messages_service.py – Definicja '_now_iso' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_first_login_brygadzisty.py, /workspace/Warsztat-Menager/test_start_user_activity.py, /workspace/Warsztat-Menager/tests/test_gui_magazyn_bom_ops.py, /workspace/Warsztat-Menager/tests/test_gui_narzedzia_missing_data.py, /workspace/Warsztat-Menager/tests/test_gui_panel_disabled_modules.py, /workspace/Warsztat-Menager/tests/test_gui_panel_logout_timer.py, /workspace/Warsztat-Menager/tests/test_gui_panel_permissions.py – Definicja 'root' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_profile_smoke.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'DummyLabel' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_presence_watcher.py – Definicja 'DummyRoot' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_tool_media_io.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'DummyWidget' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_presence_watcher.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'after' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'after_cancel' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_startup_error.py, /workspace/Warsztat-Menager/test_tool_media_io.py – Definicja 'config' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_tool_media_io.py, /workspace/Warsztat-Menager/tests/test_gui_narzedzia_tasks_mixed.py, /workspace/Warsztat-Menager/tests/test_inventory_bridge.py – Definicja 'delete' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/tests/test_settings_gui.py – Definicja 'fake_button' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_logika_zlecenia_i_maszyny.py – Definicja 'fake_get' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/tests/test_settings_gui.py – Definicja 'fake_label' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/tests/test_update_logging.py – Definicja 'fake_run' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_gui_profile_smoke.py, /workspace/Warsztat-Menager/test_startup_error.py, /workspace/Warsztat-Menager/test_tool_media_io.py, /workspace/Warsztat-Menager/tests/test_gui_magazyn_basic.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'pack' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_logowanie.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_startup_error.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py – Definicja 'title' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_tool_media_io.py – Definicja 'DummyVar' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_tool_media_io.py – Definicja 'column' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_tool_media_io.py, /workspace/Warsztat-Menager/tests/test_inventory_bridge.py – Definicja 'get_children' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_tool_media_io.py – Definicja 'grid' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_tool_media_io.py – Definicja 'heading' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/test_startup_error.py, /workspace/Warsztat-Menager/test_tool_media_io.py, /workspace/Warsztat-Menager/tests/test_gui_narzedzia_tasks_mixed.py, /workspace/Warsztat-Menager/tests/test_inventory_bridge.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py – Definicja 'insert' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_tool_media_io.py – Definicja 'tag_configure' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_config.py, /workspace/Warsztat-Menager/test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/test_tool_media_io.py – Definicja 'trace_add' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py – Definicja 'DummyButton' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_enter.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'DummyToplevel' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'DummyTree' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_files.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'identify_row' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_narzedzia_tasks.py, /workspace/Warsztat-Menager/tests/test_gui_narzedzia_tasks_mixed.py – Definicja 'DummyListbox' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_profile_smoke.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'DummyPhoto' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_profile_smoke.py, /workspace/Warsztat-Menager/tests/test_dirty_guard.py – Definicja 'dialog' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_gui_profile_smoke.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'fake_open' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_startup_error.py, /workspace/Warsztat-Menager/tests/test_gui_magazyn_bom_ops.py – Definicja 'DummyCfg' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] test_startup_error.py, /workspace/Warsztat-Menager/tests/test_ui_hover.py – Definicja 'withdraw' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tests/test_gui_magazyn_basic.py, /workspace/Warsztat-Menager/tests/test_settings_tools_config_refresh.py – Definicja 'DummyFrame' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tests/test_profile_disabled_modules_ui.py, /workspace/Warsztat-Menager/tests/test_profiles_settings_gui.py, /workspace/Warsztat-Menager/tests/test_settings_gui.py – Definicja '_make_root' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tests/test_profiles_settings_gui.py, /workspace/Warsztat-Menager/tests/test_settings_gui.py, /workspace/Warsztat-Menager/tests/test_shifts_schedule_anchor.py – Definicja 'cfg_env' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tests/test_settings_gui.py, /workspace/Warsztat-Menager/tests/test_settings_window.py – Definicja 'fake_askyesno' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tests/test_settings_gui.py, /workspace/Warsztat-Menager/tests/test_settings_window.py – Definicja 'test_save_creates_backup' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tests/test_ui_hover.py, /workspace/Warsztat-Menager/tests/test_widok_hali_machines_view.py – Definicja 'DummyCanvas' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tools/audit_machines_diff.py, /workspace/Warsztat-Menager/tools/merge_machines_json.py – Definicja '_key' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tools/audit_machines_diff.py, /workspace/Warsztat-Menager/tools/merge_machines_json.py, /workspace/Warsztat-Menager/tools/roadmap_apply_updates.py, /workspace/Warsztat-Menager/ustawienia_produkty_bom.py – Definicja '_load' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tools/audit_settings_values.py, /workspace/Warsztat-Menager/tools/validators/profiles_validator.py, /workspace/Warsztat-Menager/utils_json.py – Definicja 'load_json' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tools/find_dialog_calls.py, /workspace/Warsztat-Menager/updater.py – Definicja '_iter_python_files' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] tools/scan_legacy_paths.py, /workspace/Warsztat-Menager/tools/scan_settings_duplicates.py – Definicja 'iter_files' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] updater.py, /workspace/Warsztat-Menager/ustawienia_uzytkownicy.py – Definicja '_build' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] utils_maszyny.py, /workspace/Warsztat-Menager/utils_orders.py – Definicja '_fix_if_dir' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] utils_maszyny.py, /workspace/Warsztat-Menager/widok_hali/storage.py – Definicja 'save_machines' występuje w wielu plikach – rozważ prefiks albo wydzielenie wspólnego modułu
- **INFO** [STYLE] audyt_mw.py – Możliwy nieużyty import: Counter
- **INFO** [STYLE] audyt_mw.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] audyt_mw.py – Możliwy nieużyty import: deque
- **INFO** [STYLE] audyt_mw.py – Możliwy nieużyty import: traceback
- **INFO** [STYLE] backend/audit/wm_audit_runtime.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] backend/bootstrap_root.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] backend/updater.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] backup.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] config/paths.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] config_manager.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/bootstrap.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/inventory_manager.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/logging_config.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/logika_zlecen.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/machines_loader.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/modules_manifest.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/orders_storage.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/paths_compat.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/permissions.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/settings_manager.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/theme.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/ui_notebook_autobind.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/window_manager.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] core/zlecenia_loader.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] dirty_guard.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] domain/bom/io.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] domain/magazyn.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] domain/orders.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] domain/tools/__init__.py – Możliwy nieużyty import: save_tool
- **INFO** [STYLE] domain/tools/manager.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] grafiki/shifts_schedule.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] grafiki/shifts_schedule.py – Możliwy nieużyty import: os
- **INFO** [STYLE] gui/widgets_user_footer.py – Możliwy nieużyty import: Dict
- **INFO** [STYLE] gui/widgets_user_footer.py – Możliwy nieużyty import: Iterable
- **INFO** [STYLE] gui/widgets_user_footer.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui/widgets_user_footer.py – Możliwy nieużyty import: os
- **INFO** [STYLE] gui_changelog.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_logowanie.py – Możliwy nieużyty import: messagebox
- **INFO** [STYLE] gui_magazyn_autobind.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_magazyn_bom.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_magazyn_bom.py – Możliwy nieużyty import: os
- **INFO** [STYLE] gui_magazyn_bridge.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_magazyn_kreator_bind.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_maszyny.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_narzedzia.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_narzedzia.py – Możliwy nieużyty import: subprocess
- **INFO** [STYLE] gui_narzedzia.py – Możliwy nieużyty import: sys
- **INFO** [STYLE] gui_narzedzia_qr.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_panel.py – Możliwy nieużyty import: Path
- **INFO** [STYLE] gui_panel.py – Możliwy nieużyty import: _shift_bounds
- **INFO** [STYLE] gui_panel.py – Możliwy nieużyty import: _shift_progress
- **INFO** [STYLE] gui_panel.py – Możliwy nieużyty import: time
- **INFO** [STYLE] gui_products.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_settings.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_settings.py – Możliwy nieużyty import: data_path
- **INFO** [STYLE] gui_settings.py – Możliwy nieużyty import: resolve
- **INFO** [STYLE] gui_settings.py – Możliwy nieużyty import: ustawienia_produkty_bom
- **INFO** [STYLE] gui_tools.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_tools_config.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_tools_config_advanced.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_zlecenia.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_zlecenia_creator.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] gui_zlecenia_detail.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] io_utils.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] logika_bom.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] logika_zadan.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] magazyn_catalog.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] magazyn_io.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] magazyn_io_pz.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] maszyny_logika.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] migrations.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] narzedzia_history.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] profile_tasks.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] rc1_audit_hook.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] rc1_audit_plus.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] rc1_audit_plus.py – Możliwy nieużyty import: io
- **INFO** [STYLE] rc1_data_bootstrap.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] rc1_hotfix_actions.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] rc1_profiles_bootstrap.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] rc1_theme_fix.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] scripts/check_json_format.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] scripts/gen_placeholder.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] scripts/wm_rc1_pack.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] scripts/wm_rc1_pack.py – Możliwy nieużyty import: os
- **INFO** [STYLE] services/activity_service.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] services/messages_service.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] services/profile_service.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] services/profile_service.py – Możliwy nieużyty import: p_users
- **INFO** [STYLE] start.py – Możliwy nieużyty import: rc1_audit_hook
- **INFO** [STYLE] start.py – Możliwy nieużyty import: rc1_data_bootstrap
- **INFO** [STYLE] start.py – Możliwy nieużyty import: rc1_hotfix_actions
- **INFO** [STYLE] start.py – Możliwy nieużyty import: rc1_profiles_bootstrap
- **INFO** [STYLE] start.py – Możliwy nieużyty import: rc1_theme_fix
- **INFO** [STYLE] test_config_manager.py – Możliwy nieużyty import: make_manager
- **INFO** [STYLE] test_gui_narzedzia_files.py – Możliwy nieużyty import: os
- **INFO** [STYLE] tests/test_backend_audit_runtime.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tests/test_config_helpers.py – Możliwy nieużyty import: pytest
- **INFO** [STYLE] tests/test_domain_orders.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tests/test_logika_zadan_api.py – Możliwy nieużyty import: Path
- **INFO** [STYLE] tests/test_logika_zadan_tasks.py – Możliwy nieużyty import: pytest
- **INFO** [STYLE] tests/test_settings_tools_config_refresh.py – Możliwy nieużyty import: os
- **INFO** [STYLE] tests/test_shifts_schedule.py – Możliwy nieużyty import: importlib
- **INFO** [STYLE] tests/test_tools_wrappers.py – Możliwy nieużyty import: Path
- **INFO** [STYLE] tests/test_widok_hali_machines_view.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/audit_machines_diff.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/find_dialog_calls.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/find_hardcoded_paths.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/fix_settings_schema_rooms.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/importers/build_tools_index.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/importers/tools_from_excel.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/list_branch_changes.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/merge_machines_json.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/patcher.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/roadmap_apply_updates.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/scan_legacy_paths.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/scan_missing_root.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/scan_settings_duplicates.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/seed_wm_data.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/validators/profiles_validator.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/validators/settings_paths_validator.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/validators/tools_schema_validator.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools/wm_sync.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools_autocheck.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools_config_loader.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools_history.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] tools_templates.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] ui_dialogs_safe.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] ui_hover.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] ui_theme.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] ui_utils.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] updater.py – Możliwy nieużyty import: load_last_update_info
- **INFO** [STYLE] updates_utils.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] ustawienia_systemu.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] ustawienia_systemu.py – Możliwy nieużyty import: ttk
- **INFO** [STYLE] ustawienia_uzytkownicy.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] utils/__init__.py – Możliwy nieużyty import: clear_frame
- **INFO** [STYLE] utils/dirty_guard.py – Możliwy nieużyty import: tk
- **INFO** [STYLE] utils/error_dialogs.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] utils/moduly.py – Możliwy nieużyty import: ConfigManager
- **INFO** [STYLE] utils/moduly.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] utils/path_utils.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] utils_json.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] utils_json.py – Możliwy nieużyty import: resolve_rel
- **INFO** [STYLE] utils_maszyny.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] utils_maszyny.py – Możliwy nieużyty import: unicodedata
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: BG_GRID_COLOR
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: GRID_STEP
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: HALLS_FILE
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: HALL_OUTLINE
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: Hala
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: HalaController
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: LAYERS
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: MachinesView
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: RouteAnimator
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: SCALE_MODE_100
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: SCALE_MODE_FIT
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: TechnicianRoute
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: WallSegment
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: a_star
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: draw_background
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: draw_grid
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: draw_machine
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: draw_status_overlay
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: draw_walls
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: find_path
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: load_awarie
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: load_config_hala
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: load_hale
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: load_machines_raw
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: load_walls
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: save_awarie
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: save_hale
- **INFO** [STYLE] widok_hali/__init__.py – Możliwy nieużyty import: save_machines
- **INFO** [STYLE] widok_hali/a_star.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] widok_hali/animator.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] widok_hali/controller.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] widok_hali/machines_view.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] widok_hali/renderer.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] widok_hali/storage.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] wm_audit_runtime.py – Możliwy nieużyty import: run_audit
- **INFO** [STYLE] wm_log.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] wm_theme.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] wm_tools_helpers.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] wymagane_pliki_version_check.py – Możliwy nieużyty import: os
- **INFO** [STYLE] zadania_assign_io.py – Możliwy nieużyty import: annotations
- **INFO** [STYLE] zlecenia_utils.py – Możliwy nieużyty import: annotations
- **INFO** [TODO] audyt_mw.py:176 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] audyt_mw.py:176 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] audyt_mw.py:177 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] audyt_mw.py:177 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] audyt_mw.py:177 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] audyt_mw.py:179 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] audyt_mw.py:179 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] audyt_mw.py:179 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] audyt_mw.py:179 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] backend/audit/wm_audit_runtime.py:374 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] backend/audit/wm_audit_runtime.py:376 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] tools/roadmap_apply_updates.py:134 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] tools/roadmap_apply_updates.py:149 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] tools/roadmap_apply_updates.py:232 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **INFO** [TODO] tools/roadmap_apply_updates.py:240 – Znacznik TODO/FIXME/HACK – rozważ zaplanowanie zadania
- **WARN** [JSON] config.json – Brak kluczy ['theme', 'start_view', 'pin_required'] w obiekcie 

## Podsumowania plików

### __version__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: get_version

### arch/start_full_1_4_3.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: OK
- Deklarowana wersja: 1.4.3
- Składnia: OK
- Importy: gui_logowanie, json, os, tkinter
- Definicje: -

### audit_settings_schema.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, pathlib, typing
- Definicje: _extract_schema_fields, _flatten_dict, main, value_type

### audyt_mw.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: OK
- Deklarowana nazwa: audyt_mw.py
- Deklarowana wersja: 0.9.0
- Składnia: OK
- Importy: __future__, ast, collections, config_manager, dataclasses, json, os, re, sys, traceback, typing, utils.path_utils
- Definicje: AudytMW, FileIssue, FileSummary, __init__, _check_json_file, _collect_defs, _collect_imports, _find_cycles, _find_module_path, _issue, _parse_ast, _read, _read_headers, _render_md, build_suggestions, check_obj, dfs, discover, main, pass_deep, pass_fast, pass_risk, write_reports

### backend/audit/wm_audit_runtime.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, config_manager, json, os, pathlib, time, typing, wm_log
- Definicje: _audit_config_sections, _check_machines_sources, _exists, _fallback_from_paths, _flatten_extended_audit_rows, _format_detail, _load_extended_audit_data, _normalized, add, resolved, run, run_audit, wm_warn

### backend/bootstrap_root.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, logging, os, utils_json
- Definicje: _ensure_all, _migrate_legacy, ensure_root_min_files, ensure_root_ready

### backend/updater.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, os, shutil, subprocess, tempfile, time, typing, zipfile
- Definicje: _extract_zip_to_dir, _run, _should_include, _timestamp, backup_zip, git_pull, pull_branch, repo_git_dir, restore_from_zip

### backup.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, base64, config_manager, logging, os, urllib.error, urllib.parse, urllib.request
- Definicje: upload_backup

### bom.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, logging, packaging.version, pathlib
- Definicje: _get_unit, _produkt_candidates, _sort_key, compute_bom_for_prd, compute_sr_for_pp, compute_sr_for_prd, get_polprodukt, get_produkt

### config/paths.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, os, pathlib, sys, typing
- Definicje: _D, _anchor_root, _as_path, _call_accessor, _data_root, _default_paths, _expand_path, _is_abs, _project_root, _raw_anchor_value, _read, _read_base_dir, bind_settings, data_path, ensure_core_tree, get_app_root, get_backup_dir, get_base_dir, get_data_root, get_logs_dir, get_path, join_path, p_assign_orders, p_assign_tools, p_config, p_manifest_moduly, p_presence, p_profiles, p_settings_schema, p_tools_data, p_tools_defs, p_tools_statuses, p_tools_templates, p_tools_types, p_users, resolve, set_getter

### config_manager.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, core.bootstrap, datetime, inspect, json, logging, os, pathlib, shutil, threading, time, typing, utils.path_utils, utils_json, utils_maszyny
- Definicje: ConfigError, ConfigManager, __init__, __new__, _abs_path, _absolute_with_root, _anchor, _apply_root_defaults, _apply_setting_aliases, _audit_change, _coerce_default_for_field, _dedupe_strings, _derive_root_dir, _ensure_defaults_from_schema, _ensure_dirs, _ensure_magazyn_defaults, _ensure_magazyn_slowniki, _ensure_paths_defaults, _ensure_root_directories, _expand, _expanded_path, _extract_strings, _flush_debounced_save, _init_config_storage, _is_absolute_path, _is_subpath, _is_windows_abs, _iter_schema_fields, _load_json, _load_json_or_raise, _looks_like_windows_path, _machines_rel_value, _merge_all, _migrate_legacy_keys, _migrate_legacy_paths, _migrate_profiles_config, _norm, _normalized, _path_from_cfg, _path_source, _perform_save_all, _prepare_loaded_config, _prune_rollbacks, _resolve_rel_legacy, _resolve_rroot_map, _rows, _safe_makedirs, _safe_write, _save_json, _schema_index, _set_machines_rel, _try_prepare, _validate_all, _validate_value, _walk, _write_backup, apply_import, config_path, deep_merge, default_for, delete_by_key, ensure_key, expanded, export_public, flatten, from_tabs, get, get_by_key, get_config_path, get_machines_path, get_path, get_root, import_with_dry_run, is_schema_default, load, load_tool_vocab, migrate_dotted_keys, migrate_legacy_machines_files, migrate_user_files, normalize_config, path_anchor, path_backup, path_data, path_logs, path_root, refresh, resolve_rel, resolve_under_root, save, save_all, set, set_by_key, set_path, try_migrate_if_missing, update_root_paths

### core/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: -

### core/bootstrap.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, pathlib, typing
- Definicje: _ensure_or_default, _safe_get, _set_if_missing, bootstrap_paths

### core/inventory_manager.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, core.settings_manager, dataclasses, json, os, time, typing
- Definicje: InventoryItem, _inventory_path, _num, _req_str, _validate_item, add_or_update_item, can_access_inventory, load_inventory, save_inventory, validate_inventory

### core/logging_config.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, logging, os, typing
- Definicje: _cfg_lookup, _norm, init_logging, setup_logging

### core/logika_zlecen.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, core.orders_storage, core.settings_manager, re, time, typing
- Definicje: _next_number, _required_for_type, _settings, _statuses, create_order, validate_order

### core/machines_loader.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, typing
- Definicje: _ensure_list, _sanitize_int, _sanitize_str, load_machines_from_json

### core/modules_manifest.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__
- Definicje: -

### core/normalizers.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: typing
- Definicje: _as_list, normalize_doc_to_list

### core/orders_storage.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, os, pathlib, tempfile, time, typing
- Definicje: _atomic_write, _ensure_parent, _project_root, load_orders, orders_file_path, save_orders

### core/paths_compat.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, core.settings_manager, os, traceback
- Definicje: _check_legacy, _legacy_trace, path_assets, path_backup, path_data, path_root

### core/permissions.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, typing
- Definicje: ensure_minimal_modules_if_empty, resolve_modules_for_user

### core/settings_manager.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, copy, dataclasses, json, os, pathlib, threading, time, typing
- Definicje: KeySpec, SectionSpec, Settings, __init__, _build_defaults, _coerce_types_inplace, _delete_by_path, _get_by_path, _get_with_parent, _merge, _migrate_aliases_inplace, _migrate_one, _normalize_root_path, _resolve_under_root, _set_by_path, _to_bool, _to_int, _to_str, _update_project_root, _update_save_delay, add_observer, get, load_defaults, notify_observers, path_assets, path_backup, path_data, print_root_info, reload, remove_observer, reset_to_defaults, save, save_throttled, set, ui_groups, walk

### core/theme.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, gui._theme
- Definicje: ThemeManager, apply

### core/ui_notebook_autobind.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, core.settings_manager, gui_magazyn_kreator_bind, tkinter, typing
- Definicje: _default_role, _get_tab_frame, _on_tab_changed, attach_default_magazyn_autobind, attach_magazyn_autobind_to_notebook

### core/window_manager.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, core.settings_manager, core.ui_notebook_autobind, gui_magazyn_autobind, tkinter, typing
- Definicje: WindowManager, __init__, _fire_on_show, _on_close, _on_tab_changed, _restore_geometry, _store_geometry, ensure_tab, get_main_window, instance, show

### core/zlecenia_loader.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, importlib, inspect, typing
- Definicje: _import_optional, load_creator_from_settings, resolve_master, safe_open_creator, try_load_direct_creator

### dashboard_demo_fs.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: ctypes, json, logging, math, os, sys, tkinter, ui_theme
- Definicje: WMDashboard, WMMiniHala, WMSpark, WMTile, __init__, _enable_dpi_awareness, load_awarie, load_hale, on_click, on_drag, on_release, on_resize, redraw, sample_list_short, sample_orders, save_hale, toggle_edit_mode

### dirty_guard.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, typing
- Definicje: DirtyGuard, __init__, _log, check_before, dirty, mark_clean, mark_dirty

### domain/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: -

### domain/bom/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: -

### domain/bom/io.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, json, typing, wm_log
- Definicje: _bom_path, bom_load, bom_save

### domain/magazyn.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, json, os, wm_log
- Definicje: save_reservations

### domain/orders.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, json, os, typing
- Definicje: _normalise_filename, _orders_dir, _seq_path, delete_order, ensure_orders_dir, generate_order_id, list_order_files, load_order, load_orders, load_sequences, next_sequence, order_path, save_order, save_sequences

### domain/tools/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: manager
- Definicje: -

### domain/tools/manager.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, json, os, typing, wm_log
- Definicje: save_tool

### grafiki/__init__.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: grafiki/__init__.py
- Składnia: OK
- Importy: -
- Definicje: -

### grafiki/shifts_schedule.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: grafiki/shifts_schedule.py
- Składnia: OK
- Importy: __future__, config.paths, config_manager, datetime, json, os, pathlib, profile_utils, profiles, typing
- Definicje: _anchor_monday, _available_patterns, _default_users_file, _last_update_date, _load_modes, _load_users, _log_user_count, _parse_time, _read_json, _shift_times, _slot_for_mode, _user_mode, _week_idx, set_anchor_monday, set_user_mode, today_summary, week_matrix, who_is_on_now

### gui/settings_action_handlers.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: backend, backend.audit, os, tkinter, typing, wm_log
- Definicje: ActionHandlers, __init__, _ensure_tk_root, _initial_dir, _set_key, bind, dialog_open_dir, dialog_open_file, execute, os_open_path, wm_dbg, wm_err, wm_info

### gui/widgets_user_footer.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, datetime, json, logger, os, pathlib, profile_tasks, tkinter, typing
- Definicje: _alert_candidates, _build_tasks_tile, _current_shift_label, _draw, _format_alert_summary, _format_task_summary, _is_alert_active, _is_task_urgent, _load_alerts, _load_recent_tasks, _on_destroy, _parse_deadline_value, _shift_bounds, _shift_progress, _tick, create_user_footer

### gui_changelog.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, pathlib, re, tkinter, ui_theme
- Definicje: show_changelog

### gui_logowanie.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: gui_logowanie.py
- Składnia: OK
- Importy: PIL, config.paths, config_manager, datetime, grafiki.shifts_schedule, gui_panel, logging, os, pathlib, profile_utils, services.profile_service, subprocess, tkinter, ui_theme, updates_utils, utils, utils_json
- Definicje: _load_profiles, _login_pinless, _on_destroy, _profiles_path, _tick, _update_banner, _widget_ready, draw_login_shift, ekran_logowania, logowanie, zamknij

### gui_magazyn.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: gui_magazyn.py
- Składnia: OK
- Importy: config.paths, core.settings_manager, gui_magazyn_autobind, gui_magazyn_bridge, gui_magazyn_edit, gui_magazyn_kreator_bind, gui_magazyn_rezerwacje, gui_orders, json, logika_magazyn, logika_zakupy, magazyn_io, rc1_magazyn_fix, re, tkinter, ui_theme, wm_log
- Definicje: MagazynFrame, MagazynWindow, __init__, _add_orders_button, _apply_filters, _build_ui, _can, _clear_filters, _detect_panel_role, _format_row, _get_selected_item, _load_data, _mag_refresh_event, _on_double_click, _on_panel_mapped, _on_right_click, _open_orders_for_shortages, _quick_add_to_orders, _resolve_container, _resolve_order_author, _rez_do_polproduktu, _rez_release, _role, _role_rank, _selected_item_id, _setup_magazyn_autobind, _tag_low_stock, build_magazyn_toolbar, init_magazyn_panel, load_stock, open_panel_magazyn, open_window, refresh

### gui_magazyn_add.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: gui_magazyn_add.py
- Składnia: OK
- Importy: json, logika_magazyn, magazyn_io, services.profile_service, tkinter, ui_theme
- Definicje: MagazynAddDialog, __init__, _load_jednostki, _on_type_change, _refresh_suggest_id, on_cancel, on_save, open_window

### gui_magazyn_autobind.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, gui_magazyn_kreator_bind, tkinter, typing, weakref
- Definicje: _find_kreator_button, _find_treeview, _get_registered, _is_candidate_label, _norm, ensure_magazyn_kreator_binding, register_magazyn_widgets

### gui_magazyn_bom.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, config_manager, json, os, pathlib, tkinter, ui_theme, ui_utils, wm_log
- Definicje: MagazynBOM, WarehouseModel, __init__, _build_polprodukty, _build_produkty, _build_surowce, _build_ui, _coerce_qty, _delete_polprodukt, _delete_produkt, _delete_surowiec, _iter_records, _load_all, _load_bom_file, _load_dir, _load_json, _load_polprodukty, _load_produkty, _load_surowce, _normalise_bom_payload, _normalise_polprodukty, _on_pp_select, _on_pr_select, _on_sr_select, _parse_bom, _save_json, _save_ops, _save_polprodukt, _save_produkt, _save_surowiec, add_or_update_polprodukt, add_or_update_produkt, add_or_update_surowiec, delete_polprodukt, delete_produkt, delete_surowiec, load_bom, make_window

### gui_magazyn_bridge.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, core.inventory_manager, core.settings_manager, typing
- Definicje: _map_item_to_columns, _resolve_columns, apply_inventory_to_tree, refresh_inventory

### gui_magazyn_edit.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: OK
- Deklarowana nazwa: gui_magazyn_edit.py
- Deklarowana wersja: 1.0.1
- Składnia: OK
- Importy: logika_magazyn, magazyn_io, tkinter
- Definicje: MagazynEditDialog, __init__, _safe_load, _safe_save, on_save, open_edit_dialog

### gui_magazyn_kreator_bind.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, core.settings_manager, core.zlecenia_loader, tkinter, typing
- Definicje: _find_treeview, _handler, _prefill_from_selection, _resolve_cfg, _resolve_role, bind_kreator_button, invoke_creator_from_magazyn

### gui_magazyn_pz.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: logika_magazyn, magazyn_io, tkinter
- Definicje: PZDialog, __init__, _cfg, _enforce_int_for_szt, _get, _mb_precision, _parse_qty, _reauth, _require_reauth, _safe_load, _safe_save, on_save, open_pz_dialog

### gui_magazyn_rezerwacje.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: OK
- Deklarowana nazwa: gui_magazyn_rezerwacje.py
- Deklarowana wersja: 1.0.0
- Składnia: OK
- Importy: config_manager, logika_magazyn, magazyn_io, tkinter
- Definicje: _parse_qty, _validate_and_reserve, do_save, open_rezerwuj_dialog, open_zwolnij_rezerwacje_dialog

### gui_maszyny.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: PIL, __future__, config_manager, core.settings_manager, datetime, gui_maszyny_view, logging, os, tkinter, typing, ui_theme, utils_json, utils_maszyny
- Definicje: ImageTooltip, MachineEditDialog, MachineHallRenderer, MonthYearDialog, __init__, _add_inspection_date, _bind_drag, _bind_tree_tooltips, _build_edit_footer, _build_tree, _canvas_bounds, _clamp_to_canvas, _days_to_next_inspection, _days_to_next_inspection_safe, _detect_real_source, _drag_commit, _draw_all, _draw_background_and_grid, _ensure_tree_columns, _find_node_at, _handle_add, _handle_image, _iter_inspection_dates, _label_mode, _load_background, _load_bg_image_assets, _map_bg_to_canvas, _map_canvas_to_bg, _map_label_text, _move_group, _next_inspection_date, _next_inspection_date_safe, _node_center, _now, _ok, _on_add, _on_cancel, _on_canvas_motion, _on_del, _on_edit, _on_leave, _on_motion, _on_ok, _on_press, _on_release, _on_save, _on_tree_select, _open_machines_panel, _pair, _redraw_selection, _refresh_view, _reload_from, _render_days_label_on_canvas, _reset_background_state, _resolve_radius, _safe_clamp, _save_machines, _save_rows, _selected_id, _set_bg_geometry, _set_machine_image, _short_id, _status_color, _summary, _tree_insert_row, _trigger_changed, _value_for, commit, get_config, hide, init_maszyny_view, int_or_none, panel_maszyny, pick_machine_image, render, resolve_rel, row_entry, select, show, update_rows

### gui_maszyny_view.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: PIL, core.settings_manager, os, tkinter, typing
- Definicje: MachinesView, __init__, _build_footer, _compute_fit, _draw_grid, _draw_machine_point, _load_background, _machine_at, _map_bg_to_canvas, _map_canvas_to_bg, _on_click, _on_drag, _on_drop, _schedule_blink, _toggle_edit, redraw, set_grid_visible, set_records, set_scale_mode, tick, toggle_grid, widget

### gui_narzedzia.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: gui_narzedzia.py
- Składnia: OK
- Importy: PIL, __future__, config.paths, config_manager, contextlib, datetime, ezdxf, ezdxf.addons.drawing, importlib, importlib.util, json, logger, logging, logika_magazyn, logika_zadan, matplotlib.pyplot, os, pathlib, profile_utils, services.profile_service, shutil, start, subprocess, sys, tkinter, tools_config_loader, typing, ui_hover, ui_theme, utils, utils.gui_helpers, utils.path_utils, utils_json, utils_paths, utils_tools, wm_tools_helpers, zadania_assign_io
- Definicje: _TaskTemplateUI, __init__, _active_collection, _add_default_tasks_for_status, _add_from_template, _add_task, _append_from, _append_type_to_config, _apply_image_normalization, _apply_template_for_phase, _as_tool_dict, _asgn_assign, _assign_login_to_task, _assign_me, _assign_selected, _assign_to_user, _band_tag, _bar_text, _build_skip_note, _can_convert_nn_to_sn, _clean_list, _clear_assignment, _collect_preview_paths, _current_user, _dbg, _default_tools_tasks_file, _definitions_mtime, _definitions_path_for_collection, _del_sel, _delete_task_files, _ensure_folder, _existing_numbers, _filter_my, _format_images_label, _gen, _generate_dxf_preview, _get_collections, _get_statuses, _get_tasks, _get_types, _handle_status_reload, _handle_type_change, _has_title, _hide_preview, _init_tools_data, _invalidate_tools_definitions_cache, _is_allowed_file, _is_taken, _iter_folder_items, _iter_legacy_json_items, _legacy_parse_tasks, _load_all_tools, _load_config, _load_tools_definitions, _load_tools_list_from_file, _load_tools_rows, _load_tools_rows_from_json, _log, _lookup_id_by_name, _mark_all_done, _mark_done, _maybe_reload_definitions, _maybe_seed_config_templates, _media_dir, _next, _next_free_in_range, _norm_tasks, _normalize_image_list, _normalize_status, _normalize_tool_entry, _normalized_tool_images, _odswiez_zadania, _on_cfg_updated, _on_collection_selected, _on_focus_back, _on_status_change, _on_status_selected, _on_tool_select, _on_type_selected, _open_tools_panel, _owner_login, _pending_tasks_before, _phase_for_status, _profiles_usernames, _read_tool, _refresh_assignments_view, _refresh_images_label, _refresh_task_presets, _refresh_tasks, _reload_definitions_from_disk, _reload_from_lz, _reload_statuses_and_refresh, _reload_statuses_from_definitions, _remove_task, _render_collections_initial, _render_statuses, _render_tasks, _render_types, _resolve_definitions_path, _resolve_path_candidate, _resolve_tools_dir, _safe_read_json, _safe_tool_doc, _safe_write_json, _save_config, _save_tool, _save_tool_doc, _sel_idx, _selected_task, _selected_task_meta, _set_info, _set_tasks_context, _should_highlight, _show_task_menu, _stare_convert_templates_from_config, _status_names_for_type, _status_values_list, _statusy_for_mode, _suggest_after, _suspend_ui, _sync_conv_mode, _task_names_for_status, _task_templates_from_config, _task_title, _task_to_display, _tasks_for_type, _toggle_done, _tools_editor_user_choices, _type_names_for_collection, _types_from_config, _update_global_tasks, add, build_task_template, choose_mode_and_add, clear_images, ensure_task_shape, ensure_theme_applied, get_config, migrate_tools_folder_once, normalize_tools_doc, normalize_tools_index, on_double, open_tool_dialog, panel_narzedzia, preview_media, refresh_list, repaint_hist, repaint_tasks, row, save, select_dxf, select_img, toggle_hist

### gui_narzedzia_qr.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, narzedzia_history, os, sys, tkinter, ui_utils, utils.path_utils
- Definicje: QRWindow, __init__, _error, _info, _load_config, _on_enter, _read_tool, _resolve_tools_dir, _save_tool, handle_action, main

### gui_orders.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, tkinter, ui_theme
- Definicje: apply_theme, open_orders_window

### gui_panel.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: gui_panel.py
- Składnia: OK
- Importy: __version__, datetime, gui.widgets_user_footer, gui_changelog, gui_logowanie, gui_magazyn, gui_maszyny, gui_narzedzia, gui_profile, gui_uzytkownicy, gui_zlecenia, json, logger, os, pathlib, presence, profile_utils, re, requests, services.profile_service, start, tkinter, tomllib, traceback, ui_theme, ustawienia_systemu, utils.gui_helpers, wm_access
- Definicje: _active_login, _build_sidebar, _center_container, _clear_markers, _close_changelog, _format_modules, _get_app_version, _has_unseen_changelog, _is_admin_role, _load_last_visit, _load_mag_alerts, _logout, _logout_tick, _maybe_mark_button, _on_logout_destroy, _open_feedback, _open_profile, _open_profile_entry, _reset_logout_timer, _save_last_visit, _submit, _toggle_changelog, _warn, log_akcja, otworz_panel, panel_magazyn, panel_maszyny, panel_narzedzia, panel_uzytkownicy, panel_zlecenia, uruchom_panel, wyczysc_content

### gui_products.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, logger, logika_magazyn, os, re, shutil, tkinter, typing, ui_theme, ui_utils
- Definicje: ProductsMaterialsTab, __init__, _backup, _build_ui, _ensure_dirs, _is_id_unique, _is_polprodukt_used, _is_surowiec_used, _is_symbol_unique, _load_products_from_dir, _polprodukt_form, _product_form, _read_json_list, _refresh_polprodukty, _refresh_products, _refresh_surowce, _surowiec_form, _write_json_list, add_czyn, add_polprodukt, add_product, add_surowiec, del_czyn, delete_polprodukt, delete_product, delete_surowiec, edit_polprodukt, edit_product, edit_surowiec, open_products_folder, preview_products, refresh_all, save

### gui_profile.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: PIL, config_manager, datetime, glob, grafiki.shifts_schedule, gui.widgets_user_footer, json, logger, logging, os, pathlib, profile_utils, re, services.messages_service, services.profile_service, tkinter, typing, ui_dialogs_safe, ui_theme, ui_theme_guard, utils.gui_helpers
- Definicje: ProfileView, UnidentifiedImageError, __init__, _activate_tab, _apply_theme_sync, _assigned_to_login, _avatar_placeholder, _build_about, _build_basic_tab, _build_columns, _build_cover_header, _build_description_tab, _build_header, _build_placeholder_tab, _build_preferences_tab, _build_pw_tab, _build_shortcuts, _build_simple_list_tab, _build_skills_tab, _build_stats_tab, _build_table, _build_tabs, _build_tasks_tab, _build_timeline, _convert_order_to_task, _convert_tool_task, _format_message_event, _format_task_event, _format_timestamp, _init_styles, _initials, _is_brygadzista, _is_overdue, _is_task_done, _is_task_overdue, _is_task_urgent, _load_assign_orders, _load_assign_tools, _load_avatar, _load_json, _load_selected_pin, _load_status_overrides, _load_users_list, _login_list, _make_avatar, _map_status_generic, _message_refs, _on_destroy, _on_least_tasks, _on_mark_read, _on_open_schedule, _on_open_settings, _on_pick_profile_dir, _on_pick_profile_json, _on_send_pw, _on_sim_event, _open_edit_profile, _open_manage_pins, _open_pw_modal, _order_visible_for, _parse_date, _parse_deadline, _parse_timestamp, _poll, _prepare_modal_owner, _read_tasks, _refresh, _refresh_modal_owner, _refresh_pw_tab, _refresh_view, _reload_profile_data, _render_tab, _save, _save_assign_order, _save_assign_tool, _save_pin, _save_status_override, _show_task_details, _stars, _submit, _task_deadline_text, _task_label_text, _task_refs, _task_status_value, _timeline_item, _tool_visible_for, _user_editable_fields, _valid_login, ensure_theme_applied, filtered, make_tab, on_dbl, reload_table, resetuj, row, tag_for, uruchom_panel, zapisz

### gui_settings.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: PIL, __future__, config.paths, config_manager, copy, core.logging_config, datetime, glob, gui.settings_action_handlers, gui_products, gui_tools_config, io, json, logger, logging, logika_zadan, os, pathlib, profile_utils, re, services, start, subprocess, sys, threading, tkinter, tools, tools_config_loader, typing, ui_theme, ui_utils, ustawienia_magazyn, ustawienia_produkty_bom, utils_json, wm_audit_runtime, wm_log, zlecenia_utils
- Definicje: CSVListVar, FloatDictVar, FloatListVar, NestedListVar, ScrollableFrame, SettingsPanel, SettingsWindow, StrDictVar, StrListVar, __init__, _add_field, _add_group, _add_machines_bg_group, _add_machines_map_group, _add_magazyn_tab, _add_patch_section, _add_readonly_info, _append_audit_out, _append_tests_out, _apply_orders_config, _apply_root_change, _apply_user_modules, _as_dict, _autosave_tick, _bind_copy_shortcut, _bind_defaults_shortcut, _bind_tooltip, _browse_bg, _build_orders_tab, _build_products_tab, _build_root_section, _build_root_status, _build_slowniki_tab, _build_tools_tab, _build_ui, _cleanup, _close_window, _coerce_default_for_var, _coerce_value_for_type, _create_button_field, _create_widget, _current_cfg_manager, _default_tools_definitions_path, _exists, _extract_tasks, _fallback_topmost, _get_schema, _get_tools_config_path, _handle_root_change, _hide, _init_audit_tab, _init_magazyn_tab, _init_root_resources, _install_pytest, _is_deprecated, _is_legacy_system_field, _iter_fields, _load_magazyn_dicts, _load_settings_state, _load_user_modules, _mag_dict_path, _make_system_tab, _mark_dirty, _mk_status, _normalize_field_definition, _on_button_field_clicked, _on_canvas_configure, _on_defaults_kbd, _on_inner_configure, _on_mousewheel, _on_select, _on_tab_change, _on_tools_config_saved, _on_toplevel_destroy, _on_var_write, _open_tools_config, _open_tools_definitions_editor, _pick, _pick_dir, _populate_audit_tree, _populate_tab, _refresh_paths_preview, _refresh_tools_def_preview, _register_option_var, _reload_tools_section, _reorder_tabs, _reset_legacy_file_overrides, _resolve_autosave_delay, _root_status_rows, _run_all_tests, _run_audit_now, _safe_pick_json, _safe_save_json, _save, _save_magazyn_dicts, _save_user_modules, _scroll, _show, _split, _start_autosave_loop, _status, _sync_display, _ts_value, _validate_and_save, _wm_copy_audit_report, _wm_copy_to_clipboard, _wm_read_latest_audit_from_disk, _wm_read_textwidget, _worker, add_item, audit, browse, del_item, ensure_type_entry, format_dict, format_list, format_nested, get, make_editor, move_down, move_up, on_close, on_setting_changed, pick_color, rebuild_status, refresh_panel, restore_defaults, rollback, run_patch, save, save_all, save_all_dicts, set, update_dict, update_fdict, update_list, update_nested, update_var, wm_bind_settings_getter, wm_dbg, wm_err, wm_info

### gui_tool_editor.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, datetime, json, logger, logika_zadan, tkinter, typing, ui_theme
- Definicje: ToolEditorDialog, __init__, _append_history_entry, _auto_check_all_tasks_if_exist, _ensure_single_instance, _get_tasks_for_current, _init_from_tool, _is_last_status, _keep_on_top, _load_tool_definitions_from_settings, _load_tool_file, _on_save, _on_status_selected, _ordered_statuses_for_type, _refresh_status_values, _refresh_tasks_list, _release_single_instance, _save_tool_file, apply_theme, destroy

### gui_tools.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, json, logging, os, typing, utils_json
- Definicje: _load_cfg, _tools_dir_abs, save_tool_entry

### gui_tools_config.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, gui_tools_config_advanced, json, logika_zadan, tkinter, tools_config_loader, ui_theme
- Definicje: ToolsConfigDialog, __init__, _can_use_advanced_dialog, _save

### gui_tools_config_advanced.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, glob, json, logika_zadan, os, re, time, tkinter, tools_config_loader
- Definicje: ToolsConfigDialog, __init__, _add_status, _add_task, _add_type, _del_status, _del_task, _del_type, _ensure_shared_types_integrity, _get_shared_types, _get_statuses_for_current, _load_or_init, _make_backup, _make_unique_id, _move_status, _move_task, _on_collection_change, _on_search, _on_status_edit, _on_status_select, _on_task_edit, _on_type_edit, _on_type_select, _refresh_statuses, _refresh_tasks, _refresh_types, _require_brygadzista_auth, _save, _save_now, _select_status_by_index, _select_type_by_index, _selected_status_index, _selected_type_index, _selected_type_true_index, _wm

### gui_uzytkownicy.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: collections.abc, datetime, gui_profile, json, os, profile_utils, re, services.profile_service, tkinter, ui_theme_guard, utils.moduly, wm_access
- Definicje: _current_user_login_safe, _current_user_role_safe, _edit_selected_user, _edit_user, _fill_form, _get_from, _iso_to_ym_display, _load_all_users, _load_manifest_modules_safe, _migrate_fill_missing_dates, _on_select, _open_profile, _open_profile_from_editor, _open_profile_in_main, _refresh_state, _reload_users, _save, _save_from_editor, _select_user, _validate_date_ym, ensure_theme_applied, get_all_users, get_disabled_modules_for, get_user, load_profiles, make_modules_access_button, open_modules_access_dialog, panel_uzytkownicy, save_user, set_modules_visibility_map, uruchom_panel, zaladuj_manifest

### gui_zlecenia.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, core.logika_zlecen, core.orders_storage, core.settings_manager, domain.orders, gui_zlecenia_creator, gui_zlecenia_detail, logging, start, tkinter, typing, ui_dialogs_safe, utils_orders
- Definicje: ZleceniaView, _AfterGuard, __init__, _bind_orders_event, _build_toolbar, _build_tree, _emit_orders_updated, _fill_orders_table, _load_orders_rows, _on_add, _on_destroy, _on_double_click, _on_refresh_timer, _open_orders_panel, _refresh, _reload_orders, _resolve_creator, _schedule_refresh, call_later, cancel_all, get_config, on_save_order, panel_zlecenia

### gui_zlecenia_creator.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, datetime, gui_zlecenia, json, os, tkinter, typing, ui_theme, utils.path_utils, zlecenia_utils
- Definicje: _clear, _finish, _go_back, _go_next, _on_select, _refresh, _step0, _step1, apply_theme, open_order_creator

### gui_zlecenia_detail.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, tkinter, typing, ui_theme, zlecenia_utils
- Definicje: _change_status, apply_theme, open_order_detail

### io_utils.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, logger, logging, os, traceback, typing
- Definicje: read_json, write_json

### kreator_sprawdzenia.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: argparse, config_manager, datetime, json, logika_magazyn, os, re
- Definicje: check_config_min_keys, check_file_version, check_required_paths, compare_versions, extract_version_from_text, load_expected_versions, main, parse_args, read_text_head, version_tuple, write_sample_versions

### kreator_sprawdzenia_plikow.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: OK
- Deklarowana nazwa: kreator_sprawdzenia.py
- Deklarowana wersja: 1.0
- Składnia: OK
- Importy: hashlib, logging, os
- Definicje: oblicz_sha256, sprawdz

### layout_prosty.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: OK
- Deklarowana wersja: 1.4.4
- Składnia: OK
- Importy: tkinter
- Definicje: LayoutProsty, __init__, filtruj_liste, ustaw_liste, ustaw_szczegoly

### leaves.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, json, os, time
- Definicje: _cfg, _path, _read, _read_users, _write, add_entry, entitlements_for, read_all, set_config, totals_for

### logger.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: logger.py
- Składnia: OK
- Importy: config.paths, datetime, json, logging, os
- Definicje: _ensure_app_handler, _ensure_logs_dir, log_akcja, log_magazyn

### logika_bom.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, typing
- Definicje: compute_material_needs, compute_sr_for_pp

### logika_magazyn.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: logika_magazyn.py
- Składnia: OK
- Importy: config_manager, datetime, fcntl, json, logger, logging, logika_zakupy, magazyn_io, msvcrt, os, portalocker, re, threading, tkinter
- Definicje: _append_history, _default_magazyn, _ensure_dirs, _history_path, _load_material_seq, _log_info, _log_mag, _magazyn_dir, _merge_list_into, _migrate_legacy_path, _normalize_item, _now, _safe_load, _save_material_seq, add_item_type, bump_material_seq_if_matches, delete_item, get_item, get_item_types, historia_item, lista_items, load_magazyn, lock_file, normalize_type, peek_next_material_id, performance_table, remove_item_type, rezerwuj, rezerwuj_materialy, save_magazyn, save_polprodukt, set_order, sprawdz_progi, unlock_file, upsert_item, zapisz_stan_magazynu, zuzyj, zwolnij_rezerwacje, zwrot

### logika_zadan.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, config_manager, json, os, pathlib, threading, tools_autocheck, typing
- Definicje: _default_collection, _ensure_cache, _resolve_tasks_path, _safe_load, get_collections, get_default_collection, get_statuses, get_tasks, get_tool_types, invalidate_cache, should_autocheck

### logika_zakupy.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, json, os, pathlib
- Definicje: _detect_min_field, _ensure_dir, _load_json, _next_id, _orders_raw, _save_json, add_item_to_orders, auto_order_missing, load_pending_orders, save_pending_orders, utworz_zlecenie_zakupow

### magazyn_catalog.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, os, typing, unicodedata
- Definicje: _ensure_dirs, _load_json, _normalize, build_code, load_catalog, save_catalog, suggest_names_for_category

### magazyn_io.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, logger, logging, os, pathlib, typing
- Definicje: _ensure_dirs, _load_json, _log_mag, append_history, ensure_in_katalog, generate_pz_id, load, save, save_pz, update_stany_after_pz

### magazyn_io_pz.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, os, typing
- Definicje: _ensure_dirs, _load_json, ensure_in_katalog, generate_pz_id, save_pz, update_stany_after_pz

### magazyn_slowniki.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: OK
- Deklarowana wersja: 1.0.0
- Składnia: OK
- Importy: json, os
- Definicje: _dedup_norm, get_jednostki, get_typy, load, save

### main.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, os, pathlib, runtime_paths, start
- Definicje: ensure_config_exists, main

### maszyny_logika.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, io_utils, logger, logging, pathlib, typing, utils.path_utils
- Definicje: _resolve_data_file, _save_machines, load_machines, machines_with_next_task, next_task

### migrate_bom_to_polprodukty.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: glob, json, os
- Definicje: migrate

### migrate_profiles_config.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, os, sys
- Definicje: -

### migrations.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, typing
- Definicje: migrate, needs_migration

### narzedzia_history.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, os, pathlib, typing
- Definicje: append_tool_history

### presence.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: atexit, datetime, json, logger, logging, os, platform, tempfile, time, tkinter, traceback
- Definicje: TclError, _atomic_write, _cfg_dir, _get_cfg, _now_utc_iso, _on_exit, _presence_path, _read_all, _tick, end_session, heartbeat, log_akcja, read_presence, set_config, start_heartbeat

### presence_watcher.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, json, logger, logging, os, presence, time, tkinter, traceback
- Definicje: TclError, _active_shift, _cfg, _ensure_alert, _now, _parse_hhmm, _path, _read_json, _shifts_from_cfg, _tick, _today_str, _users_meta, _write_json, log_akcja, run_check, schedule_watcher, set_config

### profile_tasks.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, os, typing, utils.path_utils
- Definicje: _load_tasks_raw, _normalize_login, _task_deadline, _task_owner, _task_status, get_tasks_for, workload_for

### profile_utils.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: profile_utils.py
- Składnia: OK
- Importy: collections.abc, config.paths, config_manager, datetime, io_utils, json, logging, os, pathlib, re, services.profile_service, sys, tkinter, typing, utils.moduly
- Definicje: _anchor_date_from_ym, _ask_root_directory_gui, _compute_sidebar_modules, _configured_users_path, _data_container, _default_admin_payload, _default_users_file, _ensure_default_users_file, _ensure_users_file_path, _load_manifest_modules, _norm, _prepare_root_structure, _prompt_for_users_root, ensure_profiles_file, ensure_user_fields, find_user_by_pin, get_tasks_for, get_user, list_user_ids, load_profiles, profiles_path, read_users, refresh_users_file, reset_admin_profile_if_needed, save_user, staz_days_for_login, staz_years_floor_for_login, write_users

### rc1_audit_hook.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, importlib, importlib.abc, importlib.machinery, sys, types, typing
- Definicje: _AuditPostImportHook, _LoaderWrapper, __getattr__, __init__, _install, _load_audit_plus, _patch_if_loaded_now, _wrap_audit_run, create_module, exec_module, find_spec, run_wrapper

### rc1_audit_plus.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, audit, datetime, dispatch, io, json, os, re, tempfile
- Definicje: _check_action_callable, _check_config_path_exists, _check_json_file_is_list, _check_json_file_readable, _check_json_min_length, _check_json_unique_field, _check_log_no_pattern, _check_profiles_no_default_admin, _data_root, _dget, _exists, _latest_file, _load_cfg, _logs_dir, _norm, _path_writable, _read_json, _read_text, _resolve_config_path, _tail, run

### rc1_data_bootstrap.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, os, sys, tkinter
- Definicje: _apply_root_defaults, _ask_directory, _ask_open_file, _ask_save_file, _ask_yesno, _autofill_optional_path, _bootstrap_active, _ensure_default_files, _ensure_dir_for, _ensure_root, _get, _load_config, _log_dialog_block, _migrate_layout_machines_path, _norm, _paths_from_settings, _pick_or_create_path, _resolve_initialdir, _save_config, _set, _set_aliases_for_bom, _write_if_missing, ensure_data_files

### rc1_hotfix_actions.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, audit, dispatch, json, os, rc1_audit_plus, shutil, tkinter, typing
- Definicje: _ask_open_file, _ask_save_file, _config_load, _config_save, _error, _info, _install_into_dispatch, _log, _warn, action_bom_export_current, action_bom_import_dialog, action_wm_audit_run, wrapped

### rc1_magazyn_fix.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: ensure_magazyn_toolbar_once, wrapper

### rc1_profiles_bootstrap.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, config_manager, json, os, tkinter
- Definicje: _ask_yesno, _ensure_dir_for, _ensure_profiles_file, _has_default_admin, _load_config, _norm, _paths_base, _profiles_path, _read_profiles, _save_config, _warn, _write_profiles, ensure_profiles_and_warn

### rc1_theme_fix.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, tkinter
- Definicje: apply_theme_fixes

### runtime_paths.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: os, pathlib, sys, tkinter
- Definicje: get_app_root, resource_path

### scripts/check_json_format.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, pathlib, subprocess, sys
- Definicje: check_json_file, main

### scripts/gen_placeholder.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: PIL, __future__, os
- Definicje: _measure_text, main

### scripts/wm_rc1_pack.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, os, pathlib, sys, tkinter, traceback, typing
- Definicje: detect_tk_version, main, p, quick_json_try, run_healthcheck, write_if_absent

### services/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: -

### services/activity_service.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, os, typing, uuid
- Definicje: _activity_path, _append, _load_activity, _matches_filters, _normalize_filter, _now_iso, _parse_timestamp, list_activity, list_activity_filtered, log_activity

### services/messages_service.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, os, typing, uuid
- Definicje: _append, _count_lines, _now_iso, _path, _read_all, _rotate_if_needed, last_inbox_ts, list_inbox, list_sent, mark_read, send_message

### services/profile_service.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, config_manager, contextlib, json, logger, os, pathlib, presence, profile_tasks, profile_utils, typing
- Definicje: _assign_orders_path, _assign_tools_path, _config_manager_or_none, _load_json, _load_tasks_raw, _overrides_dir, _presence_path, _save_json, _status_override_path, _use_users_file, authenticate, count_presence, ensure_brygadzista_account, find_first_brygadzista, get_all_users, get_tasks_for, get_user, is_logged_in, load_assign_orders, load_assign_tools, load_status_overrides, save_assign_order, save_assign_tool, save_status_override, save_user, sync_presence, tasks_data_status, workload_for, write_users

### start.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: backend.bootstrap_root, config.paths, config_manager, core.logging_config, dashboard_demo_fs, datetime, gui_changelog, gui_logowanie, gui_panel, gui_settings, json, logging, os, pathlib, profile_utils, rc1_audit_hook, rc1_data_bootstrap, rc1_hotfix_actions, rc1_profiles_bootstrap, rc1_theme_fix, shutil, subprocess, sys, tkinter, traceback, ui_theme, updater, ustawienia_systemu, utils, utils.moduly, utils_json
- Definicje: _InactivityMonitor, __init__, _dbg, _ensure_config_manager, _ensure_logging, _ensure_user_file, _error, _info, _log_path, _on_login, _open_main_panel, _post_config_bootstrap, _print_root_diagnostics, _reset, _resolve_login, _resolve_role, _show_tutorial_if_first_run, _tick, _update_paths_from_manager, _wm_git_check_on_start, apply_theme, auto_update_on_start, cancel, copy_log, ensure_theme_applied, logout, main, monitor_user_activity, open_settings_window, restart_user_activity_monitor, restore_backup, show_startup_error

### test_config_manager.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: tests.test_config_manager
- Definicje: -

### test_first_login_brygadzisty.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_panel, pytest, tkinter
- Definicje: root, test_first_login_frame_has_height

### test_gui_logowanie.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, gui_logowanie, json, pytest, services, subprocess, types
- Definicje: DummyElements, DummyLabel, DummyRoot, DummyWidget, __getitem__, __init__, after, after_cancel, attributes, bind, config, create_rectangle, delete, destroy, dummy_gui, failing_cb, fake_button, fake_cb, fake_check_output, fake_error, fake_get, fake_label, fake_run, keys, pack, place, test_label_color_current, test_label_color_outdated, test_load_last_update_info_fallback, test_load_last_update_info_git_show_fallback, test_load_last_update_info_json, test_load_last_update_info_missing_or_malformed, test_logowanie_callback_error, test_logowanie_case_insensitive, test_logowanie_invalid_pair, test_logowanie_success, test_pinless_button_present, title, winfo_children, winfo_exists, winfo_screenheight, winfo_screenwidth

### test_gui_narzedzia_config.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia, json, types
- Definicje: DummyVar, DummyWidget, __init__, bad_open, bind, column, config, delete, get, get_children, grid, heading, insert, pack, set, tag_configure, test_load_config_logs, test_panel_refreshes_after_config_change, test_save_config_logs, trace_add

### test_gui_narzedzia_enter.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia, types
- Definicje: DummyButton, DummyTk, DummyToplevel, DummyTtk, DummyVar, DummyWidget, __init__, add, bind, column, columnconfigure, config, current, delete, destroy, focus, get, get_children, grid, grid_remove, heading, insert, item, pack, rowconfigure, set, state, tag_configure, test_enter_triggers_actions, title, trace_add, yview

### test_gui_narzedzia_files.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia, json, os, types
- Definicje: DummyTree, DummyVar, DummyWidget, __init__, bind, column, config, delete, get, get_children, heading, identify_row, pack, set, tag_configure, test_is_allowed_file, test_panel_handles_return, test_remove_task_deletes_files, test_safe_tool_doc_extracts_nested_entry, trace_add

### test_gui_narzedzia_qr.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia_qr, json, narzedzia_history
- Definicje: test_handle_action_appends_history

### test_gui_narzedzia_tasks.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia, types
- Definicje: DummyListbox, DummyVar, DummyWidget, __init__, bind, config, delete, get, insert, pack, set, test_tasks_from_comboboxes

### test_gui_profile_roles.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, importlib, json
- Definicje: fake_load_json, test_foreman_role_case_insensitive, test_read_tasks_foreman_role_case_insensitive, test_read_tasks_invalid_json

### test_gui_profile_smoke.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: dirty_guard, importlib, os, pytest
- Definicje: DummyLabel, DummyPhoto, Img, __init__, dialog, fake_open, pack, test_avatar_fallback_without_pillow, test_default_avatar_used, test_dialog_invoked_on_unsaved_navigation, test_public_api

### test_kreator_gui.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: os, pyautogui, pytest, tkinter
- Definicje: on_login, test_login_window_event_simulation

### test_kreator_wersji.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: test_kreator_wersji.py
- Składnia: OK
- Importy: os, typing
- Definicje: sprawdz_wymagania, test_gui_logowanie_spelnia_wymagania

### test_logika_magazyn.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: builtins, importlib, json, logika_magazyn, multiprocessing, os, pytest, sys, time
- Definicje: DummyMB, _save_worker, askyesno, fake_import, lock_spy, slow_dump, test_alert_after_zuzycie_below_min, test_delete_item, test_load_magazyn_adds_progi_alertow, test_migrates_old_magazyn_path, test_module_loads_without_lock_lib, test_parallel_saves_are_serial, test_performance_table_aggregates, test_performance_table_limit, test_rezerwuj_materialy_braki_log, test_rezerwuj_materialy_updates_and_saves, test_rezerwuj_partial, test_save_magazyn_uses_lock_unix, test_save_magazyn_uses_lock_windows, test_set_order_persists, unlock_spy

### test_logika_zlecenia_i_maszyny.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: bom, config_manager, gui_zlecenia, json, maszyny_logika, pathlib, pytest, shutil, tkinter, zlecenia_logika
- Definicje: _setup_zlecenia_copy, fake_get, test_machines_with_next_task, test_role_without_permission_cannot_edit, test_surowce_check_and_reserve, test_wczytanie_wielu_zlecen_filtracja

### test_narzedzia_history.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, narzedzia_history
- Definicje: test_append_tool_history

### test_presence_watcher.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: presence, presence_watcher
- Definicje: DummyRoot, __init__, after, fail, test_schedule_watcher_failure_logs, test_schedule_watcher_success, test_start_heartbeat_failure_logs, test_start_heartbeat_replaces_handler, test_start_heartbeat_success

### test_priority_order.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_profile
- Definicje: test_deadline_sorting_and_default

### test_profile_utils_regression.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, profile_utils
- Definicje: test_old_style_users_upgraded

### test_shifts_schedule_weekend.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, grafiki.shifts_schedule
- Definicje: fake_times, test_week_matrix_weekend

### test_start_user_activity.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: pytest, start, tkinter
- Definicje: fake_logout, root, test_monitor_resets_on_activity, test_monitor_restart, test_monitor_triggers_logout

### test_startup_error.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: start, types
- Definicje: DummyCfg, FakeButton, FakeFrame, FakeLabel, FakeRoot, FakeText, __init__, clipboard_append, clipboard_clear, config, destroy, fake_pull, fake_restore, fake_showerror, get, insert, mainloop, pack, test_auto_update_on_start_conflict, test_show_startup_error_restores_and_copies_log, title, withdraw

### test_tool_media_io.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia, types
- Definicje: DummyVar, DummyWidget, __init__, bind, column, config, delete, fake_bind, get, get_children, grid, heading, insert, pack, tag_configure, test_refresh_list_prefers_dxf_png, test_save_and_read_media, trace_add

### test_zlecenia_utils.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, pytest, zlecenia_utils
- Definicje: test_przelicz_zapotrzebowanie_surowce, test_sprawdz_magazyn_alerts_and_warnings

### tests/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: -

### tests/smoke_check.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: bom, json, logika_magazyn, logika_zakupy, pathlib, pytest
- Definicje: test_smoke_check, test_zlecenie_zakupu_powstaje

### tests/smoke_settings_window.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: pytest, start, tkinter
- Definicje: test_open_settings_window_has_notebook_tabs, test_open_settings_window_uses_main_content_when_available

### tests/test_audit_config.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: backend.audit, json, pathlib
- Definicje: _write, capture, test_audit_accepts_single_machine_source, test_audit_config_sections_accepts_complete_config, test_audit_config_sections_detects_missing, test_audit_detects_duplicate_machine_sources

### tests/test_backend_audit_runtime.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, backend.audit, config, pathlib
- Definicje: _fake_getter, _fake_getter_factory, test_run_audit_returns_report_text

### tests/test_bom_validation.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: bom, json, pathlib, pytest
- Definicje: test_compute_bom_for_prd_ilosc_positive, test_compute_bom_for_prd_missing_czynnosci_logs_warning, test_compute_bom_for_prd_missing_ilosc_na_szt, test_compute_bom_for_prd_requires_surowiec_fields, test_compute_bom_for_prd_returns_extra_fields, test_compute_sr_for_pp_ilosc_positive, test_compute_sr_for_pp_missing_ilosc_na_szt, test_compute_sr_for_pp_missing_jednostka, test_compute_sr_for_pp_missing_surowce_file_uses_pp_unit, test_compute_sr_for_pp_missing_surowiec, test_get_produkt_prefers_numeric_version, test_get_produkt_warns_on_multiple_defaults, test_products_reference_existing_polprodukty_and_surowce

### tests/test_config_helpers.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, pytest
- Definicje: test_deep_merge_nested_and_preserves_original, test_deep_merge_overwrites_non_dict_values, test_flatten_nested_structure_and_prefix, test_get_by_key_retrieves_and_handles_missing, test_set_by_key_creates_path_and_overwrites

### tests/test_config_manager.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, json, os, pathlib, pytest, shutil
- Definicje: _make_manager, make_manager, test_audit_and_prune_rollbacks, test_auto_heal_defaults, test_backup_cloud_persistence, test_config_manager_migrates_tool_vocab, test_deprecated_fields_ignored, test_load_and_merge_overrides, test_load_tool_vocab_merges_sources, test_machines_relative_path_alias, test_migrate_legacy_machines_files, test_path_helpers_expand_relative_entries, test_profiles_migration_creates_new_structure, test_refresh_with_custom_paths, test_root_path_persisted_after_save, test_secret_admin_pin_masked, test_set_and_save_all_persistence, test_ui_theme_defaults_and_aliases, test_validate_dict_value_type

### tests/test_dirty_guard.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: dirty_guard, pytest
- Definicje: _run_check, dialog, on_discard, on_save, test_check_before_responses, test_mark_dirty_and_clean_reacts_and_logs

### tests/test_domain_orders.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config, contextlib, domain, json, os, pytest, typing
- Definicje: getter, override_orders_dir, test_delete_order, test_ensure_orders_dir_creates_directory, test_generate_order_id_respects_prefix_and_width, test_invalid_order_id_raises, test_load_orders_skips_invalid_and_hidden_files, test_save_and_load_order, test_sequence_generation

### tests/test_dxf_preview.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: PIL, ezdxf, gui_narzedzia, os, pytest
- Definicje: test_dxf_preview_resized

### tests/test_gui_magazyn_add.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_magazyn_add, json
- Definicje: test_load_jednostki_invalid_json_fallback, test_load_jednostki_missing_fallback, test_load_jednostki_valid

### tests/test_gui_magazyn_basic.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_magazyn, types
- Definicje: DummyFrame, DummyIO, __init__, load, pack, test_format_row_handles_optional_fields, test_load_data_prefers_io, test_open_panel_magazyn_passes_parent_config

### tests/test_gui_magazyn_bom_ops.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_magazyn_bom, json, pytest, tkinter
- Definicje: DummyCfg, _find_widget, get, root, test_loads_and_saves_operations

### tests/test_gui_magazyn_pz.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_magazyn_pz, pytest
- Definicje: _make_dialog, test_parse_qty_allows_fraction_when_disabled, test_parse_qty_enforces_int_for_szt_by_default, test_parse_qty_mb_precision_from_config, test_require_reauth_fallbacks

### tests/test_gui_narzedzia_missing_data.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia, pytest, tkinter
- Definicje: _setup, boom, root, test_on_collection_change_handles_missing_data, test_on_status_change_handles_missing_data, test_on_type_change_handles_missing_data

### tests/test_gui_narzedzia_numbering.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia
- Definicje: test_next_free_in_range_accepts_string_bounds, test_next_free_in_range_clamps_start, test_next_free_in_range_invalid_or_reversed_bounds

### tests/test_gui_narzedzia_task_order.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia
- Definicje: test_build_skip_note_handles_missing_title, test_build_skip_note_includes_comment_and_positions, test_pending_tasks_before_detects_unfinished_priorities

### tests/test_gui_narzedzia_tasks_mixed.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_narzedzia, types
- Definicje: DummyListbox, __init__, delete, insert, test_update_global_tasks_mixed

### tests/test_gui_panel_disabled_modules.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_panel, pytest, tkinter
- Definicje: root, test_disabled_modules_hide_buttons, test_disabled_profile_module

### tests/test_gui_panel_logout_timer.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_panel, pytest, re, tkinter
- Definicje: DummyCM, NewCM, _parse_seconds, get, root, test_logout_timer_restart_on_event, test_logout_timer_updates

### tests/test_gui_panel_permissions.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_panel, pytest, tkinter
- Definicje: _extract_button_texts, root, test_admin_has_profile_button_when_menu_hidden, test_brygadzista_side_panel_has_settings_button, test_panel_has_no_menubar

### tests/test_inventory_bridge.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: core.inventory_manager, core.settings_manager, gui_magazyn_bridge
- Definicje: _DummyTree, __init__, delete, get_children, insert, test_inventory_refresh

### tests/test_inventory_smoke.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: core.inventory_manager, core.settings_manager
- Definicje: test_inventory_validate_and_rbac

### tests/test_lines_from_text.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: pytest, tkinter, ustawienia_systemu
- Definicje: test_lines_from_text_destroyed_widget, test_lines_from_text_normal

### tests/test_logika_zadan_api.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, logika_zadan, pathlib
- Definicje: test_aliases_exposed, test_get_collections_and_default_collection, test_get_tool_types_statuses_and_tasks, test_should_autocheck_respects_global_status

### tests/test_logika_zadan_tasks.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, logika_zadan, os, pathlib, pytest, sys, threading
- Definicje: _write, test_cache_invalidation, test_concurrent_access, worker

### tests/test_magazyn_catalog.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, magazyn_catalog
- Definicje: test_build_code_variants, test_load_and_save_catalog, test_suggest_names_for_category

### tests/test_magazyn_io_comment_alias.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, magazyn_io
- Definicje: test_append_history_accepts_komentarz, test_append_history_allows_plain_filename

### tests/test_magazyn_io_core.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, json, logging, magazyn_io, re
- Definicje: test_ensure_in_katalog_unit_conflict, test_generate_pz_id_resets_each_year, test_load_bad_json, test_logging_messages

### tests/test_magazyn_io_pz.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, json, magazyn_io_pz, re
- Definicje: test_ensure_in_katalog_adds_new_position, test_generate_pz_id_format, test_save_pz_appends_entry, test_update_stany_after_pz_sums_quantities

### tests/test_moduly_manifest.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: utils.moduly
- Definicje: test_manifest_smoke

### tests/test_patcher.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, os, pathlib, subprocess, sys, tempfile, tools
- Definicje: _init_repo, test_apply_patch_and_rollback, test_get_commits

### tests/test_produkty_bom_io.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, os, pathlib, pytest, tkinter, ustawienia_produkty_bom
- Definicje: _find_widgets, test_only_one_default_version, test_save_and_load_polprodukty

### tests/test_profile_disabled_modules_ui.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: pytest, tkinter, typing, ustawienia_uzytkownicy
- Definicje: _make_root, _sample_user, on_ok, test_add_duplicate_login_shows_error, test_edit_profile_updates_tree, test_load_and_save_users_roundtrip, test_profile_edit_dialog_preserves_additional_fields, test_profile_edit_dialog_requires_login, test_profiles_tab_populates_tree, test_save_now_invokes_persistence

### tests/test_profile_utils_manifest.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: logging, profile_utils
- Definicje: test_manifest_fallback_adds_core_modules

### tests/test_profiles_settings_gui.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, gui_settings, json, pytest, test_config_manager, tkinter
- Definicje: _make_root, cfg_env, test_profile_tab_renders_and_saves

### tests/test_settings_gui.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, gui_logowanie, gui_settings, json, pytest, test_config_manager, test_gui_logowanie, tkinter, types
- Definicje: _make_root, _setup_dummy_login, cfg_env, fake_askyesno, fake_button, fake_label, test_change_and_close_warn, test_enable_pinless_login_from_settings, test_save_admin_pin, test_save_creates_backup, test_switch_tabs

### tests/test_settings_manager.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: core.settings_manager, json
- Definicje: test_settings_alias_and_types

### tests/test_settings_root.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: core.settings_manager, json, os
- Definicje: test_settings_root

### tests/test_settings_tools_config_refresh.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, gui_settings, importlib, logika_zadan, os, sys, types
- Definicje: DummyButton, DummyDialog, DummyFrame, DummyText, DummyToplevel, __init__, cb, destroy, get, insert, invalidate, pack, reload_section, resizable, test_dialog_save_invalidates_cache, test_open_tools_config_invalidates_cache, title

### tests/test_settings_window.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, gui_settings, pytest, test_config_manager, tkinter, ustawienia_systemu
- Definicje: _setup_schema, collect_defaults, fake_askyesno, test_deprecated_not_rendered, test_magazyn_tab_has_subtabs, test_open_and_switch_subtabs, test_open_and_switch_tabs, test_save_creates_backup, test_unsaved_changes_warning

### tests/test_shifts_schedule.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, grafiki.shifts_schedule, importlib, test_config_manager
- Definicje: _patch_loads, test_patterns_subset_defaults, test_set_anchor_monday, test_slot_for_mode_121, test_slot_for_mode_patterns, test_week_matrix_with_saturday

### tests/test_shifts_schedule_anchor.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, grafiki, pytest, test_config_manager
- Definicje: cfg_env, test_set_anchor_monday_far_future, test_set_anchor_monday_invalid_format, test_set_anchor_monday_past_date

### tests/test_shifts_schedule_default_override.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: grafiki, test_config_manager
- Definicje: test_set_user_mode_overrides_default

### tests/test_tools_autocheck.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: pathlib, pytest, tools_autocheck
- Definicje: sample_data_dir, test_entry_flag_takes_precedence, test_entry_flag_true_overrides_global, test_global_list_used_when_no_entry_flag, test_none_returns_false

### tests/test_tools_history.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, pathlib, tools_history
- Definicje: test_append_tool_history_jsonl

### tests/test_tools_templates.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, pathlib, pytest, tools_templates
- Definicje: _create, fixtures_dir, template_factory, test_duplicate_detection_within_collection, test_limit_8x8, test_missing_file_is_ignored

### tests/test_tools_types_statuses.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, json, pathlib
- Definicje: test_zadania_narzedzia_limits_and_structure

### tests/test_tools_wrappers.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, logika_zadan, pathlib
- Definicje: test_get_collections, test_get_tool_types_and_statuses_and_tasks, test_should_autocheck

### tests/test_ui_hover.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: types, ui_hover
- Definicje: DummyCanvas, DummyLabel, DummyPILImage, DummyPhoto, DummyPhotoImage, DummyToplevel, DummyTree, DummyWidget, __init__, after, after_cancel, bind, configure, deiconify, destroy, fake_open, geometry, identify_row, pack, put, setup_dummy, tag_bind, test_bind_helpers, test_hover_shows_and_hides, test_load_image_respects_max_size, thumbnail, trigger, trigger_leave, trigger_motion, winfo_height, winfo_rootx, winfo_rooty, winfo_width, withdraw, wm_overrideredirect

### tests/test_update_logging.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: pytest, subprocess, updater
- Definicje: fake_run, test_git_has_updates_logs_error, test_git_has_updates_missing_branch, test_run_git_pull_logs_error

### tests/test_updates_push_branch.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, pytest, test_config_manager, tkinter, ustawienia_systemu
- Definicje: test_push_branch_config_value, test_push_branch_ui_saves_value

### tests/test_widok_hali_machines_view.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, widok_hali.machines_view
- Definicje: DummyCanvas, __init__, _make_view_stub, create_line, create_oval, test_compute_fit_scale_and_anchor_centering, test_draw_grid_respects_scaled_dimensions, test_draw_machine_point_scales_radius, test_map_bg_to_canvas_applies_anchor_and_scale

### tools/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: -

### tools/audit_machines_diff.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, sys, typing
- Definicje: _key, _load, main

### tools/audit_settings_values.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, pathlib
- Definicje: check_value, extract_fields, get_value, load_json, main

### tools/check_machines_file.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: itertools, json, os, sys
- Definicje: load

### tools/find_audit_limits.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: os, re
- Definicje: scan

### tools/find_dialog_calls.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, os, re, sys
- Definicje: _iter_python_files, main

### tools/find_hardcoded_paths.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, os, re, sys
- Definicje: main

### tools/fix_settings_schema_rooms.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, os, re, sys, typing
- Definicje: _fix_missing_commas_in_array, ensure_maszyny_group, load_schema_resilient, main, read_text, strip_comments_and_fix_trailing_commas, write_text

### tools/importers/build_tools_index.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, pathlib
- Definicje: _safe_read, main

### tools/importers/tools_from_excel.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, argparse, copy, datetime, json, pandas, pathlib, re
- Definicje: _guess_column, _load_tasks, _norm, main

### tools/inspect_machines.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: os, sys, utils_maszyny
- Definicje: dump

### tools/list_branch_changes.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, argparse, datetime, subprocess, sys, typing
- Definicje: build_git_command, calculate_since, main, parse_args, run_git_log

### tools/merge_machines_json.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, argparse, copy, datetime, json, os, sys, typing
- Definicje: _add_all, _count_nonempty, _is_empty, _key, _load, _load_machines, _merge_record, _signature, _wrap, _write_report, main

### tools/patcher.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, logging, os, pathlib, subprocess, tempfile, typing, zipfile
- Definicje: _append_audit, _get_audit_file, _log_debug, _run, _run_apply, apply_patch, get_commits, rollback_to

### tools/repair_json.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: OK
- Deklarowana wersja: 1.0.0
- Składnia: OK
- Importy: io, json, os
- Definicje: main

### tools/roadmap_apply_updates.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, os, sys, typing
- Definicje: _apply_updates, _ensure_meta, _load, _match, _save, main

### tools/scan_legacy_paths.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, os, pathlib, re, sys
- Definicje: iter_files, main, scan_file

### tools/scan_missing_root.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, ast, dataclasses, datetime, os, pathlib, typing
- Definicje: Finding, RootUsageAnalyzer, __init__, _add_finding, _classify_cfg_path, _classify_os_join, _classify_path_call, _classify_path_div, _is_docstring, _line_source, _mark_constant, _prefix_match, _suspicious, analyze_file, collect_findings, dotted_name, iter_python_files, looks_like_repo_data, main, normalize_str, visit, visit_BinOp, visit_Call, visit_Constant, visit_JoinedStr, write_report

### tools/scan_settings_duplicates.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, os, pathlib, re, sys, typing
- Definicje: flatten_cfg, iter_files, load_schema_keys, main, scan_code_references

### tools/seed_wm_data.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, datetime, json, os
- Definicje: _dump, seed_all, seed_machines, seed_orders, seed_stock, seed_tools

### tools/seed_wm_maszyny_przeglady.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: OK
- Deklarowana wersja: 1.0.1 (pure-Python, bez pandas)
- Składnia: OK
- Importy: csv, datetime, json, os
- Definicje: Simple, build_machines_from_rows, fix_pl, main, read_csv_latin1_auto_delim

### tools/update_roadmap_from_git.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, os, pathlib, re, subprocess
- Definicje: _git, collect_entries, main, render_section

### tools/validators/profiles_validator.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, pathlib, typing
- Definicje: load_json, main

### tools/validators/settings_paths_validator.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, pathlib, typing
- Definicje: add, load_first, main

### tools/validators/tools_schema_validator.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, os, pathlib, typing
- Definicje: main, validate_one

### tools/wm_sync.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, base64, dotenv, json, os, pathlib, requests, sys, time, typing
- Definicje: _gh_headers, _is_text_path, _require_token, cmd_bundle, cmd_file, cmd_list, cmd_pull, get_branch_sha, get_content, get_tree_recursive, main, save_meta

### tools_autocheck.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, pathlib, typing
- Definicje: should_autocheck

### tools_config_loader.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, config_manager, glob, json, os, pathlib, re, shutil, time, typing
- Definicje: _add, _candidate_paths, _read_text, _restore_latest_backup, _sanitize_json, _try_load, _write_atomic, find_type, get_status_names_for_type, get_tasks_for_status, get_types, load_config

### tools_history.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, pathlib, typing
- Definicje: append_tool_history

### tools_templates.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, pathlib, typing
- Definicje: load_templates

### ui_dialogs_safe.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, logging, start, tkinter
- Definicje: _bootstrap_active, error_box, info_ok, safe_open_any, safe_open_dir, safe_open_json, safe_save_json, warning_box

### ui_hover.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: PIL, __future__, itertools, tkinter, typing
- Definicje: ImageHoverTooltip, __init__, _cancel_animation, _create_window, _ensure_images, _load_image, _on_leave, _on_motion, _on_widget_destroy, _placeholder_image, _show_next_image, bind_canvas_item_hover, bind_treeview_row_hover, hide_tooltip, show_tooltip, update_image_paths

### ui_theme.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, logging, pathlib, tkinter, typing
- Definicje: _apply_base_styles, _apply_widget_options, _build_palette, _configure_wm_styles, _get_apply_fn, _set_bg_recursive, _toplevel_init_patch, apply_theme, apply_theme_safe, apply_theme_tree, ensure_theme_applied, load_theme_name, resolve_theme_name

### ui_theme_guard.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: typing
- Definicje: _get_current_theme_name, ensure_theme_applied

### ui_utils.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, tkinter, typing
- Definicje: _drop_topmost, _ensure_topmost, _msg_error, _msg_info, _msg_warning, _window

### updater.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: updater.py
- Składnia: OK
- Importy: config_manager, datetime, os, pathlib, re, shutil, subprocess, sys, tkinter, traceback, typing, updates_utils, utils, zipfile
- Definicje: UpdatesUI, __init__, _append_out, _apply_local_theme, _backup_files, _build, _copy_versions, _do_restore, _ensure_dirs, _extract_zip_overwrite, _git_has_updates, _iter_python_files, _list_backups, _now_stamp, _ok, _on_git_pull, _on_git_push, _on_restore, _on_zip_update, _read_head, _refresh_versions, _restart_app, _restore_backup, _run_git_pull, _scan_versions, _style_exists, _theme_colors, _versions_to_text, _write_log, check_remote_status

### updates_utils.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, datetime, json, logging, pathlib, subprocess, typing
- Definicje: load_last_update_info, remote_branch_exists

### ustawienia_magazyn.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: OK
- Deklarowana wersja: 1.2.0
- Składnia: OK
- Importy: json, os, tkinter
- Definicje: MagazynSettingsFrame, __init__, _build_tab_alerty, _build_tab_ogolne, _build_tab_perms, _build_tab_pz, _build_tab_rezerwacje, _build_tab_slowniki, _dedup_str_list, _jm_add, _jm_del, _load_slowniki, _save_slowniki, _typy_add, _typy_del, reset_defaults, save_all

### ustawienia_produkty_bom.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: BRAK
- Deklarowana nazwa: ustawienia_produkty_bom.py
- Składnia: OK
- Importy: glob, logger, os, tkinter, ui_theme, ustawienia_systemu, utils.dirty_guard, utils.json_io
- Definicje: _add_row, _check_ok, _del_row, _delete, _ensure_dirs, _list_polprodukty, _list_produkty, _list_surowce, _load, _new, _ok, _on_pp_change, _refresh, _save, _select_idx, make_tab

### ustawienia_systemu.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, gui_settings, json, os, pathlib, tempfile, tkinter, utils.gui_helpers
- Definicje: _lines_from_text, _mark_dirty, _normalize_schema, _on_close, _on_tab_changed, apply_theme, panel_ustawien, refresh_panel

### ustawienia_uzytkownicy.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, collections.abc, json, os, profile_utils, tkinter, typing
- Definicje: ProfileEditDialog, SettingsProfilesTab, __init__, _add_profile, _build, _build_ui, _edit_selected, _get_selected_index, _load_from_storage, _load_users, _login_exists, _ok, _on_added, _on_edited, _refresh_tree, _save_now, _save_users, _select_login, make_tab

### utils/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: gui_helpers
- Definicje: -

### utils/dirty_guard.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: tkinter
- Definicje: DirtyGuard, __init__, _bind_widget, _mark_dirty, check_before, reset, set_dirty, watch

### utils/error_dialogs.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, tkinter, typing
- Definicje: _bring_on_top, _resolve_parent, ask_unsaved_changes, close, show_error_dialog

### utils/gui_helpers.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: tkinter
- Definicje: clear_frame, destroy_safe

### utils/json_io.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: json, logger, os, typing
- Definicje: _ensure_dirs, _read_json, _write_json

### utils/moduly.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, json, os, typing
- Definicje: ManifestBlad, _iter_modules, _module_id, _norm, _wczytaj_json, assert_zaleznosci_gotowe, lista_modulow, manifest_path, pobierz_modul, sprawdz_reguly, tag_logu, zaladuj_manifest, zaleznosci

### utils/path_utils.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, os
- Definicje: cfg_path

### utils_json.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config_manager, copy, json, logging, os, typing
- Definicje: _ensure_parent, ensure_dir_json, ensure_json, get_root, load_json, normalize_doc_list_or_dict, normalize_rows, normalize_tools_doc, normalize_tools_index, resolve_rel, safe_read_json, safe_write_json

### utils_maszyny.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, os, re, time, typing, unicodedata, utils_json
- Definicje: _coerce_rows, _explain_rows, _fix_if_dir, _ids_preview, _index_by_id, _load_json_file, _merge_unique, _normalize_machine_id, _pick_source, _save_json_file, _timestamp, apply_machine_updates, delete_machine, ensure_machines_sample_if_empty, index_by_id, load_json_file, load_machines, load_machines_from_path, load_machines_rows_with_fallback, merge_rows_union_by_id, merge_unique, now_iso, save_machines, save_machines_rows, sort_machines, upsert_machine

### utils_orders.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: datetime, os, utils_json
- Definicje: _fix_if_dir, ensure_orders_sample_if_empty, load_orders_rows_with_fallback

### utils_paths.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config_manager, os, typing
- Definicje: _fallback_root, rel_to_root, root_dir, tools_dir, tools_file

### utils_tools.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: os, typing, utils_json, utils_paths
- Definicje: ensure_tools_sample_if_empty, load_tools_rows_with_fallback, migrate_tools_scattered_to_root, save_tool_item, save_tools_rows

### widok_hali/__init__.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: a_star, animator, const, controller, machines_view, models, renderer, storage
- Definicje: load_machines

### widok_hali/a_star.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, heapq, typing
- Definicje: a_star, find_path, heuristic, neighbors

### widok_hali/animator.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, tkinter, typing
- Definicje: RouteAnimator, __init__, _step, cancel_all, start

### widok_hali/const.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: -
- Definicje: -

### widok_hali/controller.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, a_star, animator, models, renderer, storage, tkinter, typing
- Definicje: HalaController, __init__, _machine_at, _route_and_animate, check_for_awaria, delete_machine_with_triple_confirm, on_click, on_drag, on_drop, redraw, refresh, set_mode, show_details

### widok_hali/machines_view.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: PIL, __future__, os, tkinter, typing
- Definicje: MachinesView, __init__, _build_footer, _compute_fit_scale_and_anchor, _draw_grid, _draw_machine_point, _load_background, _map_bg_to_canvas, _on_resize, make_button, redraw, set_grid_visible, set_records, set_scale_mode, toggle_grid, widget

### widok_hali/models.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: dataclasses, typing
- Definicje: Hala, Machine, TechnicianRoute, WallSegment

### widok_hali/renderer.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, json, tkinter, wm_log
- Definicje: Renderer, __init__, _blink_tick, _canvas_size, _coerce_int, _configure_data_sources, _dot_radius, _draw_all, _draw_machine, _load_bg_image, _load_config_background, _load_machines_from_config, _machine_attr, _machine_position, _mid_from_event, _normalize_machines, _on_click, _on_drag, _on_drop, _on_hover_enter, _on_hover_leave, _oval_center, _start_blink, _update_paths_from_config, draw_background, draw_grid, draw_machine, draw_status_overlay, draw_walls, focus_machine, reload, set_edit_mode

### widok_hali/storage.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, config_manager, const, json, logger, models, os, typing, utils.path_utils
- Definicje: _log, _read_json_list, _resolve_machines_save_path, get_machines, get_machines_path, get_path, load_awarie, load_config_hala, load_hale, load_machines, load_machines_models, load_walls, resolve_machines_file, save_awarie, save_hale, save_machines

### wm_access.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: config.paths, config_manager, json, pathlib, profile_utils
- Definicje: _ensure_dirs, _profiles_path, add_disabled, get_disabled_modules_for, get_effective_allowed_modules, load_profiles, normalize_module_name, remove_disabled, save_profiles, set_modules_visibility, set_modules_visibility_map

### wm_audit_runtime.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: backend.audit.wm_audit_runtime
- Definicje: -

### wm_log.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, os, sys, time, traceback, typing
- Definicje: _emit, _enabled, _get_setting, _kv_pairs, _read_setting_with_legacy, _term_supports_color, bind_settings_getter, dbg, err, info

### wm_theme.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, tkinter
- Definicje: apply_theme

### wm_tools_helpers.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, config.paths, config_manager, json, pathlib, re, typing
- Definicje: _load_status_tasks, _task_definitions_path, _tools_data_dir, assign_task, assign_task_any, ensure_task_shape, is_pending_task, is_valid_tool_record, iter_tools_json, merge_tasks_with_status_templates, save_tool_json, status_tasks_for

### wymagane_pliki_version_check.py
- Nagłówek # Plik: OK
- Nagłówek # Wersja: OK
- Deklarowana nazwa: kreator_sprawdzenia.py
- Deklarowana wersja: 1.1
- Składnia: OK
- Importy: os, re
- Definicje: sprawdz, sprawdz_wersje

### zadania_assign_io.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, json, pathlib, typing
- Definicje: _load_all, _save_all, assign, list_all, list_for_user, list_in_context, unassign

### zlecenia_logika.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: bom, datetime, pathlib, utils.json_io
- Definicje: _ensure_dirs, _next_id, check_materials, compute_material_needs, create_zlecenie, delete_zlecenie, list_produkty, list_zlecenia, read_bom, read_magazyn, reserve_materials, rezerwuj_materialy, update_status, update_zlecenie

### zlecenia_utils.py
- Nagłówek # Plik: BRAK
- Nagłówek # Wersja: BRAK
- Składnia: OK
- Importy: __future__, bom, config.paths, config_manager, datetime, io_utils, json, os, typing
- Definicje: _add_oczekujace, _calc_bom, _config_types_snapshot, _ensure_int, _ensure_orders_dir, _ensure_str, _load_oczekujace, _load_seq, _orders_cfg, _orders_id_width, _orders_types, _save_oczekujace, _save_seq, _seq_path, _zamowienia_oczek_path, create_order_skeleton, load_orders, next_order_id, przelicz_zapotrzebowanie, save_order, sprawdz_magazyn, statuses_for
