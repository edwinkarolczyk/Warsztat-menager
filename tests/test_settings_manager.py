# version: 1.0
"""Smoke tests for settings manager."""

import json
import os

from core.settings_manager import Settings


def test_settings_alias_and_types(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "theme": "light",
                "paths": {"datadir": "DATA"},
                "gui": {"maszyny": {"show_grid": "0", "scale_mode": "100"}},
            }
        ),
        encoding="utf-8",
    )
    cfg = Settings(path=str(config_path), project_root=__file__)
    assert cfg.get("gui.theme") == "light"
    assert cfg.get("paths.data_dir") in ("DATA", str(cfg.get("paths.data_dir")))
    assert cfg.get("gui.maszyny.show_grid") is False
    assert cfg.get("gui.maszyny.scale_mode") == "100"


def test_settings_root_placeholder(tmp_path):
    project_root = tmp_path / "workspace"
    project_root.mkdir()

    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "paths": {
                    "root": str(project_root),
                    "backup_dir": "<root>/backup",
                    "assets_dir": "<ROOT>\\assets",
                }
            }
        ),
        encoding="utf-8",
    )

    cfg = Settings(path=str(config_path))

    expected_backup = os.path.normpath(project_root / "backup")
    expected_assets = os.path.normpath(project_root / "assets")

    assert os.path.normpath(cfg.path_backup()) == expected_backup
    assert os.path.normpath(cfg.path_assets()) == expected_assets
