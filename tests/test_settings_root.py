# version: 1.0
import json
import os

from core.settings_manager import Settings


def test_settings_root(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_data = {"paths": {"root": str(tmp_path)}}
    cfg_file.write_text(json.dumps(cfg_data, indent=2), encoding="utf-8")

    settings_from_config = Settings(path=str(cfg_file))
    assert os.path.samefile(settings_from_config.project_root, tmp_path)

    manual_root = tmp_path / "manual_root"
    manual_root.mkdir()
    settings_manual = Settings(path=str(cfg_file), project_root=str(manual_root))
    assert os.path.samefile(settings_manual.project_root, manual_root)

    settings_from_config.print_root_info()
