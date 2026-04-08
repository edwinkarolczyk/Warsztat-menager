#!/usr/bin/env python3
# version: 1.0
"""
WM: Localny czytnik gałęzi 'Rozwiniecie' (READ-ONLY).
Pobiera listę plików oraz zawartość (tylko tekst) z GitHuba przy użyciu tokena,
zapisuje je lokalnie do katalogu out/ i/lub buduje paczkę JSON do analizy.

Użycie:
  python tools/wm_sync.py pull             # pobierz drzewo i pliki tekstowe
  python tools/wm_sync.py list             # wypisz ścieżki plików (z cache)
  python tools/wm_sync.py file <path>      # pokaż zawartość pojedynczego pliku (z cache)
  python tools/wm_sync.py bundle           # zbuduj zbiorczy JSON (out/wm_bundle.json)

Wymagane:
  - Python 3.8+
  - pakiety: requests, python-dotenv
  - zmienne środowiska: GITHUB_TOKEN (fine-grained, read-only, 60 dni OK)
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - fallback when dotenv missing
    load_dotenv = lambda *args, **kwargs: None  # type: ignore

try:
    import requests
except Exception as exc:  # pragma: no cover - dependency missing
    print(
        "[wm_sync] Brak pakietu 'requests'. Zainstaluj: pip install requests "
        "python-dotenv",
        file=sys.stderr,
    )
    raise

# --- KONFIG ---
OWNER = os.environ.get("WM_GH_OWNER", "edwinkarolczyk")
REPO = os.environ.get("WM_GH_REPO", "Warsztat-Menager")
BRANCH = os.environ.get("WM_GH_BRANCH", "Rozwiniecie")
OUT_DIR = Path(os.environ.get("WM_SYNC_OUT", "out/WM_Rozwiniecie")).resolve()
META_PATH = OUT_DIR / "_meta.json"
BUNDLE_PATH = OUT_DIR.parent / "wm_bundle.json"

API = "https://api.github.com"

# Pliki binarne i duże – pomijamy (tylko czytamy listę)
BIN_EXT = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".ico",
    ".zip",
    ".rar",
    ".7z",
    ".pdf",
    ".xls",
    ".xlsx",
    ".xlsm",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".bin",
    ".ttf",
    ".otf",
    ".mp3",
    ".mp4",
}
MAX_TEXT_BYTES = 512_000  # 500 KB


def _is_text_path(path: str) -> bool:
    ext = Path(path).suffix.lower()
    return ext not in BIN_EXT


def _gh_headers(token: str) -> Dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "wm-sync-readonly",
    }


def _require_token() -> str:
    load_dotenv()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if not token:
        print("[wm_sync] Brak GITHUB_TOKEN. Ustaw w .env lub zmiennej środowiska.")
        sys.exit(2)
    return token


def get_branch_sha(token: str) -> str:
    url = f"{API}/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}"
    response = requests.get(url, headers=_gh_headers(token), timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["object"]["sha"]


def get_tree_recursive(token: str, tree_sha: str) -> List[Dict[str, str]]:
    url = f"{API}/repos/{OWNER}/{REPO}/git/trees/{tree_sha}?recursive=1"
    response = requests.get(url, headers=_gh_headers(token), timeout=60)
    response.raise_for_status()
    data = response.json()
    return data.get("tree", [])


def get_content(token: str, path: str, ref: str) -> Tuple[bytes, bool]:
    """Zwraca (bytes, encoded_base64_flag)."""
    url = f"{API}/repos/{OWNER}/{REPO}/contents/{path}"
    response = requests.get(
        url, headers=_gh_headers(token), params={"ref": ref}, timeout=60
    )
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list):
        msg = "Oczekiwano pliku, a zwrócono katalog."
        raise RuntimeError(msg)
    content = data.get("content", "")
    encoding = data.get("encoding", "")
    if encoding == "base64":
        return base64.b64decode(content), True
    return content.encode("utf-8", errors="replace"), False


def save_meta(commit_sha: str, files: List[str]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    meta_payload = {
        "owner": OWNER,
        "repo": REPO,
        "branch": BRANCH,
        "commit_sha": commit_sha,
        "files": files,
        "ts": int(time.time()),
    }
    META_PATH.write_text(
        json.dumps(meta_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def cmd_pull() -> None:
    token = _require_token()
    print(f"[wm_sync] Repo: {OWNER}/{REPO}  branch={BRANCH}")
    sha = get_branch_sha(token)
    print(f"[wm_sync] Commit SHA: {sha}")
    tree = get_tree_recursive(token, sha)
    files = [item["path"] for item in tree if item.get("type") == "blob"]
    print(f"[wm_sync] Plików w drzewie: {len(files)}")
    saved = 0
    skipped = 0
    for path in files:
        if not _is_text_path(path):
            skipped += 1
            continue
        try:
            data, _ = get_content(token, path, BRANCH)
            if len(data) > MAX_TEXT_BYTES:
                skipped += 1
                continue
            out_path = OUT_DIR / path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(data)
            saved += 1
        except Exception as exc:  # pragma: no cover - log and continue
            print(f"[wm_sync] WARN: pominięto {path}: {exc}")
            skipped += 1
    save_meta(sha, files)
    print(f"[wm_sync] Zapisano: {saved}  pominięto: {skipped}")
    print(f"[wm_sync] OUT: {OUT_DIR}")


def cmd_list() -> None:
    if not META_PATH.exists():
        print("[wm_sync] Brak cache. Uruchom: python tools/wm_sync.py pull")
        return
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    print(
        f"[wm_sync] {meta['owner']}/{meta['repo']}@{meta['branch']}  "
        f"sha={meta['commit_sha']}"
    )
    for path in sorted(OUT_DIR.rglob("*")):
        if path.is_file() and path.name != "_meta.json":
            rel = path.relative_to(OUT_DIR)
            print(rel.as_posix())


def cmd_file(path_arg: str) -> None:
    path = (OUT_DIR / path_arg).resolve()
    if not path.exists():
        print(f"[wm_sync] Nie znaleziono pliku w cache: {path}")
        return
    try:
        data = path.read_text(encoding="utf-8")
        print(data)
    except UnicodeDecodeError:
        print("[wm_sync] To nie jest plik tekstowy.")


def cmd_bundle() -> None:
    """Buduje paczkę JSON z cache."""
    if not META_PATH.exists():
        print("[wm_sync] Brak cache. Uruchom: python tools/wm_sync.py pull")
        return
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    files_out = []
    for path in sorted(OUT_DIR.rglob("*")):
        if path.is_file() and path.name != "_meta.json":
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            rel = path.relative_to(OUT_DIR).as_posix()
            files_out.append({"path": rel, "text": text})
    bundle = {"meta": meta, "files": files_out}
    BUNDLE_PATH.write_text(
        json.dumps(bundle, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[wm_sync] Zapisano paczkę: {BUNDLE_PATH}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Użycie: python tools/wm_sync.py [pull|list|file|bundle] [args]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "pull":
        cmd_pull()
    elif cmd == "list":
        cmd_list()
    elif cmd == "file":
        if len(sys.argv) < 3:
            print("Użycie: python tools/wm_sync.py file <sciezka/w/repo>")
            sys.exit(1)
        cmd_file(sys.argv[2])
    elif cmd == "bundle":
        cmd_bundle()
    else:
        print(f"Nieznana komenda: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
