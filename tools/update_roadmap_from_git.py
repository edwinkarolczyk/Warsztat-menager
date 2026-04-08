# version: 1.0
import subprocess
import os
import re
import pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
RM = ROOT / "ROADMAP.md"


def _git(args: list[str]) -> str:
    result = subprocess.run(
        ["git"] + args,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def collect_entries() -> list[tuple[str, str, str]]:
    """
    Zbiera linie z git log na gałęzi 'Rozwiniecie' i wyciąga:
    - R-xx (np. R-15)
    - PR #1234 (jeśli w tytule/treści)
    - datę commita
    """
    log = _git(["log", "Rozwiniecie", "--pretty=format:%h|%ad|%s", "--date=short"])
    entries = []
    rx_r = re.compile(r"\b(R-\d{1,3})\b", re.IGNORECASE)
    rx_pr = re.compile(r"\bPR\s*#(\d+)\b", re.IGNORECASE)
    for line in log.splitlines():
        try:
            _hash, adate, subject = line.split("|", 2)
        except ValueError:
            continue
        match_r = rx_r.search(subject)
        match_pr = rx_pr.search(subject)
        if match_r:
            rtag = match_r.group(1).upper()
            prn = f"PR #{match_pr.group(1)}" if match_pr else ""
            entries.append((rtag, prn, adate))
    # deduplikacja (ostatni wygrywa)
    uniq: dict[str, tuple[str, str, str]] = {}
    for rtag, prn, adate in entries[::-1]:
        uniq[rtag] = (rtag, prn, adate)
    return sorted(uniq.values(), key=lambda x: (int(x[0].split("-")[1])))


def render_section(items: list[tuple[str, str, str]]) -> str:
    out = [
        "# Roadmap (R-xx) — auto",
        f"_Updated: {datetime.now():%Y-%m-%d %H:%M}_",
        "",
    ]
    for rtag, prn, adate in items:
        out.append(f"- **{rtag}:** ( {prn} , merged {adate} )")
    out.append("")
    return "\n".join(out)


def main() -> None:
    items = collect_entries()
    text = render_section(items)
    RM.write_text(text, encoding="utf-8")
    print("[ROADMAP] zaktualizowano:", RM)


if __name__ == "__main__":
    if os.name == "nt":
        main()
    else:
        main()
