# version: 1.0
import json
from pathlib import Path

from backend.audit import wm_audit_runtime as audit


def _write(path: Path, payload: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def test_audit_detects_duplicate_machine_sources(tmp_path):
    data_root = tmp_path / "data"
    legacy = data_root / "maszyny.json"
    primary = data_root / "maszyny" / "maszyny.json"

    _write(legacy, [{"nr_ewid": "1"}])
    _write(primary, [{"nr_ewid": "2"}])

    cfg = {"paths": {"data_root": str(data_root)}}
    ok, detail = audit._check_machines_sources(cfg)

    assert ok is False
    assert "primary=" in detail and "legacy=" in detail


def test_audit_accepts_single_machine_source(tmp_path):
    data_root = tmp_path / "data"
    primary = data_root / "maszyny" / "maszyny.json"
    _write(primary, [{"nr_ewid": "2"}])

    cfg = {"paths": {"data_root": str(data_root)}}
    ok, detail = audit._check_machines_sources(cfg)

    assert ok is True
    assert str(primary) in detail


def test_audit_config_sections_detects_missing(capsys):
    recorded: list[tuple[str, bool, str]] = []

    def capture(name: str, ok: bool, detail: str) -> None:
        recorded.append((name, ok, detail))

    audit._audit_config_sections({}, capture)

    missing = {name for name, ok, _ in recorded if not ok}

    assert "config.ui.theme" in missing
    assert "config.ui.start_on_dashboard" in missing
    assert "config.ui.auto_check_updates" in missing
    assert "config.ui.debug_enabled" in missing
    assert "config.ui.log_level" in missing
    assert "config.backup.keep_last" in missing
    assert "config.updates.auto_pull" in missing
    assert "config.tools.types" in missing

    output = capsys.readouterr().out
    assert "[WM-DBG][AUDIT]" in output


def test_audit_config_sections_accepts_complete_config(capsys):
    cfg = {
        "ui": {
            "theme": "dark",
            "language": "pl",
            "start_on_dashboard": True,
            "auto_check_updates": True,
            "debug_enabled": True,
            "log_level": "debug",
        },
        "paths": {
            "data_root": "data",
            "logs_dir": "logs",
            "backup_dir": "backup",
            "layout_dir": "data/layout",
        },
        "backup": {"keep_last": 5},
        "updates": {"auto_pull": True},
        "profiles": {
            "editable_fields": ["telefon"],
            "pin": {"change_allowed": True, "min_length": 4},
            "avatar": {"enabled": False},
        },
        "machines": {"rel_path": "maszyny/maszyny.json"},
        "tools": {
            "types": ["NN"],
            "statuses": ["OK"],
            "task_templates": ["Przegląd"],
        },
    }

    recorded: list[tuple[str, bool, str]] = []

    def capture(name: str, ok: bool, detail: str) -> None:
        recorded.append((name, ok, detail))

    audit._audit_config_sections(cfg, capture)

    assert all(ok for _, ok, _ in recorded)
    output = capsys.readouterr().out
    assert output.strip() == ""
