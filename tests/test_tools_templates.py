# version: 1.0
import json
from pathlib import Path

import pytest

import tools_templates


@pytest.fixture
def template_factory(tmp_path: Path):
    def _create(name: str, ident: str, collection: str = "col") -> Path:
        col_dir = tmp_path / collection
        col_dir.mkdir(exist_ok=True)
        path = col_dir / name
        payload = {"id": ident, "name": f"Tool {ident}"}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    return _create


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures" / "tools_templates"


def test_limit_8x8(template_factory) -> None:
    paths = [
        template_factory(f"{i:03}.json", f"{i:03}")
        for i in range(tools_templates.MAX_TEMPLATES + 1)
    ]
    with pytest.raises(ValueError):
        tools_templates.load_templates(paths)


def test_duplicate_detection_within_collection(fixtures_dir) -> None:
    p1 = fixtures_dir / "dup" / "a.json"
    p2 = fixtures_dir / "dup" / "b.json"
    with pytest.raises(ValueError):
        tools_templates.load_templates([p1, p2])


def test_missing_file_is_ignored(tmp_path: Path) -> None:
    missing = tmp_path / "col" / "missing.json"
    result = tools_templates.load_templates([missing])
    assert result == []


def test_mapping_payload_is_normalized(tmp_path: Path) -> None:
    path = tmp_path / "col" / "map.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"A": {"steps": [1, 2]}, "B": ["x", "y"]}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = tools_templates.load_templates([path])
    ids = {tpl["id"] for tpl in result}
    assert ids == {"A", "B"}
