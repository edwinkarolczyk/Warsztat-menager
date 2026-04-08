# version: 1.0
from __future__ import annotations

import os
import re
import sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAT = re.compile(
    r"([\"'])"
    r"(?:[A-Z]:\\\\|/)?"
    r"(?:wm[/\\\\]data|warsztat[-_ ]?menager|^data[/\\\\])"
    r"[^\"']*\1",
    re.IGNORECASE,
)


def main() -> int:
    offenders: list[str] = []
    for base, _, files in os.walk(ROOT):
        for filename in files:
            if not filename.endswith((".py", ".json", ".md", ".txt")):
                continue
            path = os.path.join(base, filename)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
            except OSError:
                continue
            if PAT.search(content):
                offenders.append(path)
    if not offenders:
        print("[SCAN] OK – brak podejrzanych twardych ścieżek.")
        return 0
    print("[SCAN] Potencjalne twarde ścieżki w plikach:")
    for path in offenders:
        print(" -", path)
    return 1


if __name__ == "__main__":
    sys.exit(main())
