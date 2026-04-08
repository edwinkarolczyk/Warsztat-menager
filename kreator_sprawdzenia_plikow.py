# WM-VERSION: 0.1
# Plik: kreator_sprawdzenia.py
# version: 1.0
# Opis: Sprawdza obecność i zgodność plików programu Warsztat Menager

import os
import hashlib
import logging

DEBUG_MODE = bool(os.getenv("WM_DEBUG"))
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Lista wymaganych plików z sumami kontrolnymi SHA256 (mogą być uzupełniane)
wymagane_pliki = {
    "start.py": None,
    "gui_logowanie.py": None,
    "gui_panel.py": None,
    "layout_prosty.py": None,
    "ustawienia_systemu.py": None,
    "uzytkownicy.json": None,
    "config.json": None
}

def oblicz_sha256(nazwa):
    try:
        with open(nazwa, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None

def sprawdz():
    logging.info("🛠 Sprawdzanie plików Warsztat Menager...")
    brakujace = []
    for plik in wymagane_pliki:
        if not os.path.exists(plik):
            logging.error("Brakuje: %s", plik)
            brakujace.append(plik)
        else:
            logging.info("Jest: %s", plik)

    if not brakujace:
        logging.info("Wszystkie wymagane pliki są obecne.")
    else:
        logging.warning(
            "Uzupełnij brakujące pliki przed uruchomieniem programu.")

    logging.info(
        "(Jeśli chcesz dodać sprawdzanie sum kontrolnych, uzupełnij słownik 'wymagane_pliki')"
    )

if __name__ == "__main__":
    sprawdz()
