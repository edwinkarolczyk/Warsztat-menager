# version: 1.0
import json
import os
import zipfile
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List, Tuple

from utils_json import normalize_tools_index, safe_read_json as _r, safe_write_json as _w
from utils_paths import tools_dir, tools_file


def _tool_identifier(item: Dict, default: str) -> str:
    identifier = str(
        item.get("id")
        or item.get("nr")
        or item.get("numer")
        or default
    ).strip()
    item.setdefault("id", identifier)
    item.setdefault("nr", identifier)
    item.setdefault("numer", identifier)
    item.setdefault("lokalizacja", "")
    return identifier


def _coerce_relations(raw_value) -> list[str]:
    if raw_value is None:
        return []
    if isinstance(raw_value, (list, tuple, set)):
        return [str(item).strip() for item in raw_value if str(item).strip()]
    return [str(raw_value).strip()] if str(raw_value).strip() else []


def _ensure_bidirectional_relations(rows: List[Dict]) -> List[Dict]:
    """Ensure ``narzedzia_powiazane`` lists are symmetric between tools."""

    row_map: Dict[str, Dict] = {}
    relation_map: Dict[str, set[str]] = {}

    for row in rows:
        identifier = _tool_identifier(row, "")
        if not identifier:
            continue
        row_map[identifier] = row
        relation_map[identifier] = set(
            _coerce_relations(
                row.get("narzedzia_powiazane")
                or row.get("powiazane")
                or row.get("powiazane_narzedzia")
            )
        )

    for source, targets in list(relation_map.items()):
        for target in targets:
            if target not in row_map:
                continue
            relation_map.setdefault(target, set()).add(source)

    for identifier, related in relation_map.items():
        row = row_map.get(identifier)
        if row is None:
            continue
        row["narzedzia_powiazane"] = sorted(related)

    return rows


def _candidate_demo_zips(cfg: Dict) -> List[Path]:
    candidates: List[Path] = []
    for env_key in ("WM_DEMO_TOOLS_ZIP", "WM_JSON_DEMO_ZIP"):
        env_path = os.environ.get(env_key)
        if env_path:
            candidates.append(Path(env_path))

    root = Path(cfg.get("paths", {}).get("data_root") or "")
    candidates.extend(
        [
            Path("wm_json_demo_20.zip"),
            Path("/mnt/data/wm_json_demo_20.zip"),
            root / "wm_json_demo_20.zip",
            root / "import" / "wm_json_demo_20.zip",
            Path(tools_dir(cfg)) / "wm_json_demo_20.zip",
        ]
    )
    unique: List[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        normalized = os.path.normcase(os.path.abspath(str(candidate)))
        if normalized in seen:
            continue
        seen.add(normalized)
        if Path(candidate).is_file():
            unique.append(Path(candidate))
    return unique


def _load_rows_from_zip(zip_path: Path) -> List[Dict]:
    rows: List[Dict] = []
    try:
        with zipfile.ZipFile(zip_path) as archive:
            for name in archive.namelist():
                base = os.path.basename(name)
                if not base.lower().endswith(".json"):
                    continue
                if base.lower() in {
                    "narzedzia.json",
                    "statusy_narzedzi.json",
                    "typy_narzedzi.json",
                    "szablony_zadan.json",
                }:
                    continue
                with archive.open(name) as fh:
                    try:
                        payload = json.load(TextIOWrapper(fh, encoding="utf-8"))
                    except Exception:
                        continue
                if not isinstance(payload, dict):
                    continue
                identifier = _tool_identifier(payload, base[:-5])
                if identifier:
                    rows.append(payload)
    except Exception:
        return []
    return rows


def load_tools_rows_with_fallback(cfg: Dict, resolve_rel) -> Tuple[List[Dict], str]:
    """Load tools data preferring per-tool JSON documents."""

    # >>> PATCH START: narzędzia – model JSON per plik
    tools_path = tools_dir(cfg)
    os.makedirs(tools_path, exist_ok=True)
    aggregated_path = tools_file(cfg, "narzedzia.json")

    rows: List[Dict] = []
    try:
        entries = sorted(os.listdir(tools_path))
    except OSError:
        entries = []

    for name in entries:
        if not name.lower().endswith(".json"):
            continue
        if name.lower() == "narzedzia.json":
            continue
        path = os.path.join(tools_path, name)
        payload = _r(path, default={}, ensure=False)
        if not isinstance(payload, dict):
            continue
        item = dict(payload)
        identifier = _tool_identifier(item, name[:-5])
        if identifier:
            rows.append(item)

    if rows:
        # >>> PATCH START: narzędzia – model JSON per plik
        rows.sort(
            key=lambda item: str(item.get("nr") or item.get("numer") or item.get("id") or "")
        )
        # <<< PATCH END: narzędzia – model JSON per plik
        rows = _ensure_bidirectional_relations(rows)
        for row in rows:
            save_tool_item(cfg, row)
        save_tools_rows(aggregated_path, rows)
        return rows, aggregated_path
    # <<< PATCH END: narzędzia – model JSON per plik

    if not rows:
        for candidate in _candidate_demo_zips(cfg):
            rows = _load_rows_from_zip(candidate)
            if rows:
                break

    if rows:
        rows = _ensure_bidirectional_relations(rows)
        save_tools_rows(aggregated_path, rows)
        for row in rows:
            save_tool_item(cfg, row)
        return rows, aggregated_path

    data = normalize_tools_index(
        _r(aggregated_path, default={"items": [], "narzedzia": []})
    )
    rows = [row for row in data.get("items", []) if isinstance(row, dict)]
    rows = _ensure_bidirectional_relations(rows)
    if rows:
        save_tools_rows(aggregated_path, rows)

    if not rows:
        legacy = resolve_rel(cfg, r"narzedzia.json")
        data2 = normalize_tools_index(_r(legacy, default={"items": [], "narzedzia": []}))
        rows2 = [row for row in data2.get("items", []) if isinstance(row, dict)]
        if rows2:
            rows2 = _ensure_bidirectional_relations(rows2)
            save_tools_rows(aggregated_path, rows2)
            return rows2, aggregated_path
    return rows, aggregated_path


def ensure_tools_sample_if_empty(rows: List[Dict], primary_path: str) -> List[Dict]:
    """Ensure that the tools directory contains starter records."""

    # >>> PATCH START: narzędzia – model JSON per plik
    if rows:
        return rows

    sample = [
        {"id": "001", "nr": "001", "numer": "001", "nazwa": "Klucz dynamometryczny", "status": "OK", "typ": "NN", "lokalizacja": "Magazyn"},
        {"id": "002", "nr": "002", "numer": "002", "nazwa": "Suwmiarka 150 mm", "status": "OK", "typ": "NN", "lokalizacja": "Kontrola"},
        {"id": "003", "nr": "003", "numer": "003", "nazwa": "Wiertło Ø8 HSS", "status": "Zużyte", "typ": "NN", "lokalizacja": "Produkcja"},
    ]

    base_dir = os.path.dirname(primary_path) or tools_dir({})
    os.makedirs(base_dir, exist_ok=True)
    for item in sample:
        identifier = str(item.get("id") or item.get("nr") or item.get("numer") or "").strip()
        if not identifier:
            continue
        path = os.path.join(base_dir, f"{identifier}.json")
        _w(path, item)

    save_tools_rows(primary_path, sample)
    return sample
    # <<< PATCH END: narzędzia – model JSON per plik


def save_tools_rows(primary_path: str, rows: List[Dict]) -> bool:
    """Persist the full list of tools rows to *primary_path*."""

    payload = {"items": rows, "narzedzia": rows}
    return _w(primary_path, payload)


def save_tool_item(cfg: Dict, item: Dict) -> str | None:
    """Save a single tool item into a dedicated JSON file inside tools dir."""

    tid = str(item.get("id") or item.get("numer") or item.get("nr") or "").strip()
    if not tid:
        return None
    data = dict(item)
    data.setdefault("id", tid)
    path = tools_file(cfg, f"{tid}.json")
    _w(path, data)
    return path


def migrate_tools_scattered_to_root(cfg: Dict) -> int:
    """Migrate scattered tool files to the central tools directory.

    Returns the number of moved/copied files.
    """

    moved = 0
    root_tools = tools_dir(cfg)
    os.makedirs(root_tools, exist_ok=True)

    for base in ("narzedzia", "./narzedzia", ".\\narzedzia"):
        if not os.path.isdir(base):
            continue
        for name in os.listdir(base):
            if not name.lower().endswith((".json", ".jslon")):
                continue
            src = os.path.join(base, name)
            if not os.path.isfile(src):
                continue
            dst = tools_file(cfg, name)
            try:
                if os.path.abspath(src) != os.path.abspath(dst):
                    with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                        fdst.write(fsrc.read())
                    moved += 1
            except Exception:
                continue

    try:
        entries = os.listdir(root_tools)
    except OSError:
        entries = []
    for name in entries:
        if not name.lower().endswith(".jslon"):
            continue
        src = os.path.join(root_tools, name)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(root_tools, name[:-6] + ".json")
        try:
            with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                fdst.write(fsrc.read())
            moved += 1
        except Exception:
            continue

    return moved
