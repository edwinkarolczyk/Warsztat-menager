# version: 1.0
from __future__ import annotations

import sys
import os
import re
import pathlib
from datetime import datetime

REPO = pathlib.Path(os.getcwd())  # pokażemy to w konsoli i w raporcie
OUT = REPO / "legacy_paths_report.txt"

PATTERNS = [
    ("C:\\wm\\data\\backup", re.compile(r"C:\\wm\\data\\backup", re.IGNORECASE)),
    ("C:\\\\wm\\\\data\\\\backup", re.compile(r"C:\\\\wm\\\\data\\\\backup", re.IGNORECASE)),
    ("/wm/data/backup", re.compile(r"[\\/]+wm[\\/]+data[\\/]backup", re.IGNORECASE)),
    ("paths.backup", re.compile(r"\\bpaths\\.backup\\b", re.IGNORECASE)),
    ("backup.path", re.compile(r"\\bbackup\\.path\\b", re.IGNORECASE)),
    ("backup.dir", re.compile(r"\\bbackup\\.dir\\b", re.IGNORECASE)),
    ("BACKUP_DIR", re.compile(r"\\bBACKUP_DIR\\b")),
    ("WM_BACKUP", re.compile(r"\\bWM_BACKUP\\b")),
    ("wm\\data", re.compile(r"[\\/]+wm[\\/]data\\b", re.IGNORECASE)),
    ("C:\\wm\\", re.compile(r"C:\\wm\\", re.IGNORECASE)),
    ("backup_dir", re.compile(r"\\bbackup_dir\\b", re.IGNORECASE)),
    ("path_backup(", re.compile(r"\\bpath_backup\\s*\\(", re.IGNORECASE)),
]

EXTS = {".py", ".json", ".ini", ".txt", ".cfg", ".toml", ".yml", ".yaml", ".bat", ".ps1", ".md"}
EXCLUDE = re.compile(
    r"(?:[/\\]\.git|[/\\]\.venv|[/\\]venv|[/\\]node_modules|[/\\]dist|[/\\]build|[/\\]__pycache__)",
    re.IGNORECASE,
)


def iter_files(root: pathlib.Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS and not EXCLUDE.search(str(p.parent)):
            yield p


def scan_file(path: pathlib.Path):
    hits = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return hits
    for i, line in enumerate(lines, 1):
        for label, rx in PATTERNS:
            if rx.search(line):
                hits.append((label, i, line.strip()))
    return hits


def main():
    print(f"[SCAN] CWD: {REPO}")
    found = []
    for f in iter_files(REPO):
        for label, line_no, text in scan_file(f):
            found.append((f, label, line_no, text))

    # ZAWSZE zapisz plik
    OUT.write_text("", encoding="utf-8")
    with OUT.open("w", encoding="utf-8") as f:
        f.write(f"=== LEGACY PATHS SCAN === {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        f.write(f"CWD/Repo: {REPO}\n")
        f.write("Patterns: " + ", ".join(lbl for (lbl, _) in PATTERNS) + "\n\n")
        f.write("--- HITS (file:line: pattern: text) ---\n\n")
        if found:
            for file, label, line_no, text in sorted(found, key=lambda x: (str(x[0]).lower(), x[2], x[1])):
                f.write(f"{file}:{line_no}: [{label}] {text}\n")
        else:
            f.write("(brak trafień)\n")

        # podsumowania
        f.write("\n--- SUMMARY BY PATTERN ---\n")
        if found:
            by_pat = {}
            for _file, label, _ln, _tx in found:
                by_pat[label] = by_pat.get(label, 0) + 1
            for pat, cnt in sorted(by_pat.items(), key=lambda x: -x[1]):
                f.write(f"{cnt:4d} × {pat}\n")
        else:
            f.write("(pusto)\n")

        f.write("\n--- SUMMARY BY FILE ---\n")
        if found:
            by_file = {}
            for file, _label, _ln, _tx in found:
                s = str(file)
                by_file[s] = by_file.get(s, 0) + 1
            for s, cnt in sorted(by_file.items(), key=lambda x: -x[1]):
                f.write(f"{cnt:4d} × {s}\n")
        else:
            f.write("(pusto)\n")

    if found:
        print(f"[SCAN] ⚠️  Wykryto trafienia. Raport: {OUT}")
        return 1
    print(f"[SCAN] ✅  Czysto. Raport: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
