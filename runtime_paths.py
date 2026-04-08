# version: 1.0
import os
import sys
from pathlib import Path
try:
    # Python 3.8+ type hints ok, ale bez problemu zadziała też starsze
    from tkinter import Tk, filedialog, messagebox
except Exception:
    Tk = None


def get_app_root(default_anchor=r"C:\\wm", app_name="Warsztat-Menager"):
    """
    Zwraca katalog danych aplikacji (<root>).
    Logika:
     - jeśli działa z PyInstaller: szuka config w %APPROOT% lub używa default_anchor
     - jeśli nie ma config, pyta użytkownika o folder (jeśli jest tkinter dostępny)
     - zwraca Path obiektu (tworzy foldery jeśli trzeba)
    """
    # preferowany kolejność:
    # 1) env var WM_DATA_ROOT
    # 2) config.json obok exe (w trybie dev)
    # 3) default anchor C:\wm (jeśli istnieje)
    # 4) pytanie użytkownika (jeśli brak i tkinter dostępny)
    env_root = os.environ.get("WM_DATA_ROOT")
    if env_root:
        root = Path(env_root)
        root.mkdir(parents=True, exist_ok=True)
        return root

    # jeśli spakowane przez PyInstaller, szukamy w program data albo fallback do default_anchor
    if getattr(sys, "frozen", False):
        # katalog, w którym uruchomiono exe (nie MEIPASS)
        exe_dir = Path(sys.executable).parent
    else:
        exe_dir = Path(__file__).parent

    # prefer config przy exe_dir/config.json
    candidate_config = exe_dir / "config.json"
    if candidate_config.exists():
        # staraj się użyć katalogu config->paths.data_root jeśli tam jest
        # ale tutaj tylko zwracamy exe_dir jako root do dalszego ładowania (app może czytać config)
        return exe_dir

    # jeśli istnieje domyślny anchor, użyj go
    anchor = Path(default_anchor)
    if anchor.exists():
        return anchor

    # jeśli tkinter dostępny — poproś o wybór katalogu; inaczej użyj domyślnego anchor (utwórz)
    if Tk is not None:
        root_tk = Tk()
        root_tk.withdraw()
        messagebox.showinfo(
            "Wybierz katalog aplikacji",
            (
                "Nie znaleziono katalogu danych. Domyślnie użyjemy: "
                f"{default_anchor}. Możesz wybrać inny katalog."
            ),
        )
        folder = filedialog.askdirectory(
            initialdir="C:\\",
            title="Wybierz katalog dla Warsztat-Menager",
        )
        root_tk.destroy()
        if folder:
            path = Path(folder)
            path.mkdir(parents=True, exist_ok=True)
            return path

    # fallback: utwórz i zwróć domyślny anchor
    anchor.mkdir(parents=True, exist_ok=True)
    return anchor


def resource_path(rel_path: str, app_root: Path = None):
    """
    Zwraca absolutną ścieżkę do pliku zasobu:
     - uwzględnia PyInstaller MEIPASS (wtedy zasoby dołączone przez --add-data będą dostępne)
     - lub jeśli używasz katalogu danych (<root>), łączy z app_root
    Użycie:
        icon = resource_path("assets/icon.ico", app_root)
    """
    if app_root is None:
        app_root = get_app_root()

    # jeśli spakowane: najpierw sprawdź w MEIPASS
    if getattr(sys, "frozen", False):
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        candidate = base / rel_path
        if candidate.exists():
            return str(candidate)
    # standardowo szukaj w app_root lub obok skryptu
    candidate = app_root / rel_path
    if candidate.exists():
        return str(candidate)
    # ostatecznie: względna ścieżka w katalogu skryptu
    fallback = Path(__file__).parent / rel_path
    return str(fallback)
