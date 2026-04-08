# version: 1.0
import json
import os
import zipfile
from pathlib import Path

from utils_tools import load_tools_rows_with_fallback


def _resolve_rel(cfg, rel: str) -> str:
    return os.path.join(cfg.get("paths", {}).get("data_root", ""), rel)


def test_load_tools_rows_applies_relation_symmetry(tmp_path: Path) -> None:
    cfg = {"paths": {"data_root": str(tmp_path)}}
    tools_dir = tmp_path / "narzedzia"
    tools_dir.mkdir()

    (tools_dir / "100.json").write_text(
        json.dumps({"id": "100", "narzedzia_powiazane": ["200"]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (tools_dir / "200.json").write_text(
        json.dumps({"id": "200", "narzedzia_powiazane": []}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    rows, _ = load_tools_rows_with_fallback(cfg, _resolve_rel)
    related = next(row for row in rows if row.get("id") == "200")
    assert "100" in related.get("narzedzia_powiazane", [])

    updated = json.loads((tools_dir / "200.json").read_text(encoding="utf-8"))
    assert "100" in updated.get("narzedzia_powiazane", [])


def test_load_tools_from_demo_zip(tmp_path: Path, monkeypatch) -> None:
    cfg = {"paths": {"data_root": str(tmp_path)}}
    zip_path = tmp_path / "wm_json_demo_20.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("narzedzia/300.json", json.dumps({"id": "300", "nazwa": "Demo"}, indent=2))

    monkeypatch.setenv("WM_DEMO_TOOLS_ZIP", str(zip_path))

    rows, _ = load_tools_rows_with_fallback(cfg, _resolve_rel)
    ids = {row.get("id") for row in rows}
    assert "300" in ids
