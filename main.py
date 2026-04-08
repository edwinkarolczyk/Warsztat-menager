# version: 1.0
import json
import os
from pathlib import Path

from runtime_paths import get_app_root

APP_ROOT = get_app_root(default_anchor=r"C:\\wm", app_name="Warsztat-Menager")
CONFIG_FILE = Path(APP_ROOT) / "config.json"

os.environ.setdefault("WM_DATA_ROOT", str(APP_ROOT))
os.environ.setdefault("WM_CONFIG_FILE", str(CONFIG_FILE))


def ensure_config_exists() -> None:
    """Ensure config.json exists in the application root."""

    if CONFIG_FILE.exists():
        return

    default_config = {
        "paths": {
            "data_root": str(APP_ROOT),
            "logs_dir": "logs",
        },
        "tools": {
            "types_file": "narzedzia/typy_narzedzi.json",
            "statuses_file": "narzedzia/statusy_narzedzi.json",
        },
        "modules": {"active": {}},
    }

    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as file_handle:
        json.dump(default_config, file_handle, indent=2, ensure_ascii=False)


ensure_config_exists()


def main() -> None:
    """Entry point delegating to the legacy start module."""

    from start import main as start_main

    start_main()


if __name__ == "__main__":
    main()
