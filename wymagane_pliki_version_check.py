# version: 1.0
# WM-VERSION: 0.1
"""Sprawdza obecność plików i nagłówki wersji Warsztat Menagera."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

from __version__ import get_version

APP_VERSION = get_version()
WM_HEADER_RE = re.compile(r"#\s*WM-VERSION:\s*(\S+)")
FILE_HEADER_RE = re.compile(r"#\s*Wersja(?:\s+pliku)?:\s*(\S+)")
PYTHON_EXTENSIONS = {".py", ".pyw"}

REQUIRED_FILES = {
    "start.py": "1.5.1",
    "gui_logowanie.py": "1.4.12.1",
    "gui_panel.py": "1.6.17",
    "layout_prosty.py": "1.4.4",
    "ustawienia_systemu.py": "1.4.8",
    "uzytkownicy.json": None,
    "config.json": None,
}


@dataclass
class CheckResult:
    path: Path
    status: str  # "ok", "warn", "error"
    messages: List[str]
    suggestions: List[str]


def _severity(current: str, new: str) -> str:
    order = {"ok": 0, "warn": 1, "error": 2}
    return new if order[new] > order[current] else current


def _read_headers(path: Path) -> tuple[str | None, str | None]:
    wm_version: str | None = None
    file_version: str | None = None

    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if wm_version is None:
                    match = WM_HEADER_RE.match(line)
                    if match:
                        wm_version = match.group(1)
                        if file_version is not None:
                            break
                        continue
                if file_version is None:
                    match = FILE_HEADER_RE.match(line)
                    if match:
                        file_version = match.group(1)
                        if wm_version is not None:
                            break
    except OSError:
        return None, None

    return wm_version, file_version


def sprawdz_wersje(path_str: str, expected: str | None) -> CheckResult:
    path = Path(path_str)
    if not path.exists():
        if expected is None:
            return CheckResult(
                path=path,
                status="ok",
                messages=[f"ℹ️ Pominięto: {path_str} (plik opcjonalny, brak w repozytorium)"],
                suggestions=[],
            )

        status = "error"
        icon = "❌"
        suggestion = f"Utwórz lub przywróć plik `{path_str}`."
        return CheckResult(
            path=path,
            status=status,
            messages=[f"{icon} Brakuje: {path_str}"],
            suggestions=[suggestion],
        )

    extension = path.suffix.lower()
    check_headers = extension in PYTHON_EXTENSIONS
    wm_version: str | None = None
    file_version: str | None = None

    if check_headers:
        wm_version, file_version = _read_headers(path)

    status = "ok"
    messages: List[str] = []
    suggestions: List[str] = []

    if check_headers:
        if expected is not None and file_version == expected and wm_version == APP_VERSION:
            messages.append(
                f"✅ {path_str} – wersje OK (plik {file_version}, WM {wm_version})"
            )
        else:
            messages.append(
                f"ℹ️ {path_str} – wersja pliku: {file_version or 'brak'}, WM-VERSION: {wm_version or 'brak'}"
            )

            if expected is not None:
                if file_version is None:
                    status = _severity(status, "warn")
                    messages.append(f"⚠️ {path_str} – brak nagłówka wersji pliku")
                    suggestions.append(
                        f"Dodaj linię `# Wersja pliku: {expected}` w `{path_str}`."
                    )
                elif file_version != expected:
                    status = _severity(status, "warn")
                    messages.append(
                        f"⚠️ {path_str} – wersja pliku {file_version} ≠ oczekiwanej {expected}"
                    )
                    suggestions.append(
                        f"Zaktualizuj nagłówek `# Wersja pliku` w `{path_str}` do `{expected}`."
                    )

            if wm_version is None:
                status = _severity(status, "warn")
                messages.append(f"⚠️ {path_str} – brak nagłówka WM-VERSION")
                suggestions.append(
                    f"Dodaj linię `# WM-VERSION: {APP_VERSION}` na początku `{path_str}`."
                )
            elif wm_version != APP_VERSION:
                status = _severity(status, "warn")
                messages.append(
                    f"⚠️ {path_str} – WM-VERSION {wm_version} ≠ aktualnej {APP_VERSION}"
                )
                suggestions.append(
                    f"Ustaw nagłówek `# WM-VERSION` w `{path_str}` na `{APP_VERSION}`."
                )
    else:
        messages.append(f"✅ {path_str} – plik dostępny")

    suggestions = list(dict.fromkeys(suggestions))
    if status == "ok" and not messages:
        ok_note = (
            f"✅ {path_str} – wersje OK" if expected else f"✅ {path_str} – plik OK"
        )
        messages.append(ok_note)

    return CheckResult(path=path, status=status, messages=messages, suggestions=suggestions)


def sprawdz() -> int:
    print("\n🛠 Sprawdzanie plików i wersji Warsztat Menager...")
    results: List[CheckResult] = []
    for path_str, expected in REQUIRED_FILES.items():
        result = sprawdz_wersje(path_str, expected)
        results.append(result)
        for message in result.messages:
            print(message)

    warn_count = sum(1 for r in results if r.status == "warn")
    error_count = sum(1 for r in results if r.status == "error")
    ok_count = len(results) - warn_count - error_count
    print(
        f"\nPodsumowanie: OK {ok_count}, ostrzeżenia {warn_count}, błędy {error_count}."
    )

    suggestions = []
    for result in results:
        suggestions.extend(result.suggestions)

    print("\nSugestie naprawy:")
    if suggestions:
        for suggestion in dict.fromkeys(suggestions):
            print(f"- {suggestion}")
    else:
        print("- Brak – wszystko wygląda poprawnie.")

    return 0 if warn_count == 0 and error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(sprawdz())
