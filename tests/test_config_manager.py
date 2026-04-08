# version: 1.0
import json
import os
import shutil
from pathlib import Path

import pytest

import config_manager as cm


@pytest.fixture
def make_manager(tmp_path, monkeypatch):
    def _make_manager(
        defaults=None,
        global_cfg=None,
        local_cfg=None,
        secrets=None,
        schema=None,
        rollback_keep=None,
    ):
        defaults = defaults or {}
        global_cfg = global_cfg or {}
        local_cfg = local_cfg or {}
        secrets = secrets or {}
        schema = schema or {"config_version": 1, "options": []}

        paths = {
            "schema": tmp_path / "settings_schema.json",
            "defaults": tmp_path / "config.defaults.json",
            "global": tmp_path / "config.json",
            "local": tmp_path / "config.local.json",
            "secrets": tmp_path / "secrets.json",
            "audit": tmp_path / "audit",
            "backup": tmp_path / "backup",
        }

        paths["audit"].mkdir()
        paths["backup"].mkdir()

        data_map = {
            paths["schema"]: schema,
            paths["defaults"]: defaults,
            paths["global"]: global_cfg,
            paths["local"]: local_cfg,
            paths["secrets"]: secrets,
        }
        for path, data in data_map.items():
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        default_root = cm._norm(str(tmp_path / "wm_root"))

        monkeypatch.setattr(cm, "SCHEMA_PATH", str(paths["schema"]))
        monkeypatch.setattr(cm, "DEFAULTS_PATH", str(paths["defaults"]))
        monkeypatch.setattr(cm, "GLOBAL_PATH", str(paths["global"]))
        monkeypatch.setattr(cm, "LOCAL_PATH", str(paths["local"]))
        monkeypatch.setattr(cm, "SECRETS_PATH", str(paths["secrets"]))
        monkeypatch.setattr(cm, "AUDIT_DIR", str(paths["audit"]))
        monkeypatch.setattr(cm, "BACKUP_DIR", str(paths["backup"]))
        monkeypatch.setattr(cm, "_DEFAULT_ROOT", default_root)
        monkeypatch.setitem(cm.DEFAULTS["paths"], "data_root", default_root)
        monkeypatch.setitem(cm.DEFAULTS["paths"], "anchor_root", default_root)
        monkeypatch.setitem(
            cm.DEFAULTS["paths"], "logs_dir", os.path.join(default_root, "logs")
        )
        monkeypatch.setitem(
            cm.DEFAULTS["paths"], "backup_dir", os.path.join(default_root, "backup")
        )
        monkeypatch.setitem(
            cm.DEFAULTS["paths"], "assets_dir", os.path.join(default_root, "assets")
        )
        monkeypatch.setitem(
            cm.DEFAULTS["paths"],
            "layout_dir",
            os.path.join(default_root, "data", "layout"),
        )
        if rollback_keep is not None:
            monkeypatch.setattr(cm, "ROLLBACK_KEEP", rollback_keep)

        return cm.ConfigManager.refresh(), paths

    return _make_manager


def test_load_and_merge_overrides(make_manager):
    schema = {
        "config_version": 1,
        "options": [
            {"key": "a", "type": "int"},
            {"key": "b.x", "type": "int"},
            {"key": "c", "type": "int"},
            {"key": "secret", "type": "string", "scope": "secret"},
        ],
    }
    defaults = {"a": 1, "b": {"x": 1}}
    global_cfg = {"b": {"x": 2}, "c": 3}
    local_cfg = {"c": 4}
    secrets = {"secret": "s"}

    mgr, _ = make_manager(
        defaults=defaults,
        global_cfg=global_cfg,
        local_cfg=local_cfg,
        secrets=secrets,
        schema=schema,
    )

    assert mgr.get("a") == 1
    assert mgr.get("b.x") == 2
    assert mgr.get("c") == 4
    assert mgr.get("secret") == "s"


def test_auto_heal_defaults(make_manager):
    mgr, paths = make_manager(global_cfg={})

    assert mgr.get("ui.theme") == "dark"
    assert mgr.get("ui.language") == "pl"
    assert mgr.get("backup.keep_last") == 10

    with open(mgr.config_path(), encoding="utf-8") as f:
        data = json.load(f)
    assert data["ui"]["theme"] == "dark"
    assert data["ui"]["language"] == "pl"
    assert data["backup"]["keep_last"] == 10

    audit_file = Path(paths["audit"]) / "config_changes.jsonl"
    with open(audit_file, encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]
    keys = {entry.get("key") for entry in lines}
    assert keys == {
        "ui.theme",
        "ui.language",
        "ui.start_on_dashboard",
        "ui.auto_check_updates",
        "ui.debug_enabled",
        "ui.log_level",
        "paths.anchor_root",
        "paths.data_root",
        "backup.keep_last",
        "updates.auto_pull",
    }
    recorded = {rec["key"]: rec["after"] for rec in lines}
    expected_anchor = mgr.get("paths.anchor_root")
    expected_root = mgr.get("paths.data_root")
    assert recorded["ui.theme"] == "dark"
    assert recorded["ui.language"] == "pl"
    assert recorded["ui.start_on_dashboard"] is True
    assert recorded["ui.auto_check_updates"] is True
    assert recorded["ui.debug_enabled"] is True
    assert recorded["ui.log_level"] == "debug"
    assert recorded["backup.keep_last"] == 10
    assert recorded["paths.anchor_root"] == expected_anchor
    assert recorded["paths.data_root"] == expected_root
    assert recorded["updates.auto_pull"] is True


def test_deprecated_fields_ignored(make_manager):
    schema = {
        "config_version": 1,
        "options": [
            {"key": "foo", "type": "int", "default": 1},
            {"key": "old", "type": "int", "default": 2, "deprecated": True},
        ],
    }
    mgr, paths = make_manager(schema=schema, global_cfg={})
    assert mgr.get("foo") == 1
    assert mgr.get("old") is None
    with open(mgr.config_path(), encoding="utf-8") as f:
        data = json.load(f)
    assert "old" not in data


def test_set_and_save_all_persistence(make_manager):
    schema = {
        "config_version": 1,
        "options": [{"key": "foo", "type": "int"}],
    }
    defaults = {"foo": 1}

    mgr, paths = make_manager(defaults=defaults, schema=schema)
    mgr.set("foo", 5, who="tester")
    assert mgr.get("foo") == 5

    mgr.save_all()

    with open(mgr.config_path(), encoding="utf-8") as f:
        assert json.load(f)["foo"] == 5

    reloaded = cm.ConfigManager.refresh()
    assert reloaded.get("foo") == 5


def test_root_path_persisted_after_save(make_manager, tmp_path):
    schema = {
        "config_version": 1,
        "options": [{"key": "paths.data_root", "type": "path"}],
    }

    mgr, _ = make_manager(schema=schema)

    new_root = tmp_path / "nowy_root"
    mgr.set("paths.data_root", str(new_root), who="test")
    mgr.save_all()

    expected_root = os.path.normpath(os.path.join(str(new_root), "data"))
    expected_anchor = os.path.normpath(str(new_root))
    with open(mgr.config_path(), encoding="utf-8") as handle:
        stored = json.load(handle)

    assert stored["paths"]["anchor_root"] == expected_anchor
    assert stored["paths"]["data_root"] == expected_root

    reloaded = cm.ConfigManager.refresh(
        config_path=str(new_root / "config.json"), schema_path=cm.SCHEMA_PATH
    )
    assert reloaded.get("paths.data_root") == expected_root


def test_update_root_paths_sets_relative_dirs(make_manager, tmp_path):
    mgr, _ = make_manager(schema={"config_version": 1, "options": []})

    new_root = tmp_path / "workspace_root"
    data_dir = new_root / "data"
    mgr.update_root_paths(str(data_dir))

    expected_root = os.path.normpath(str(new_root))
    expected_data = os.path.normpath(str(data_dir))
    expected_backup = os.path.normpath(str(new_root / "backup"))
    expected_logs = os.path.normpath(str(new_root / "logs"))
    expected_assets = os.path.normpath(str(new_root / "assets"))

    assert mgr.get("paths.anchor_root") == expected_root
    assert mgr.get("paths.data_root") == expected_data
    assert mgr.get("paths.backup_dir") == expected_backup
    assert mgr.get("paths.logs_dir") == expected_logs
    assert mgr.get("paths.assets_dir") == expected_assets

    assert mgr.path_data() == expected_data
    assert mgr.path_backup() == expected_backup
    assert mgr.path_logs() == expected_logs
    assert mgr.path_assets() == expected_assets

def test_audit_and_prune_rollbacks(make_manager):
    schema = {
        "config_version": 1,
        "options": [{"key": "foo", "type": "int"}],
    }
    defaults = {"foo": 1}

    mgr, paths = make_manager(defaults=defaults, schema=schema, rollback_keep=2)

    mgr.set("foo", 2, who="tester")

    audit_file = Path(paths["audit"]) / "config_changes.jsonl"
    with open(audit_file, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    rec = next(r for r in records if r["key"] == "foo")
    assert rec["before"] == 1
    assert rec["after"] == 2
    assert rec["user"] == "tester"

    backup_dir = Path(mgr.path_backup())
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name in [
        "config_20200101_000000.json",
        "config_20200102_000000.json",
        "config_20200103_000000.json",
    ]:
        (backup_dir / name).touch()

    mgr.save_all()

    files = sorted(f.name for f in backup_dir.iterdir() if f.is_file())
    assert len(files) == 2
    assert "config_20200101_000000.json" not in files
    assert "config_20200102_000000.json" not in files


def test_validate_dict_value_type(make_manager):
    schema = {
        "config_version": 1,
        "options": [
            {
                "key": "progi_alertow_surowce",
                "type": "dict",
                "value_type": "float",
            },
            {
                "key": "jednostki_miary",
                "type": "dict",
                "value_type": "string",
            },
        ],
    }
    defaults = {
        "progi_alertow_surowce": {"stal": 10.0},
        "jednostki_miary": {"szt": "sztuka"},
    }

    mgr, paths = make_manager(defaults=defaults, schema=schema)
    assert mgr.get("progi_alertow_surowce") == {"stal": 10.0}
    assert mgr.get("jednostki_miary") == {"szt": "sztuka"}

    for bad_defaults in [
        {"progi_alertow_surowce": 1},
        {"progi_alertow_surowce": {"stal": "dużo"}},
        {"jednostki_miary": {"szt": 1}},
    ]:
        shutil.rmtree(paths["audit"], ignore_errors=True)
        shutil.rmtree(paths["backup"], ignore_errors=True)
        with pytest.raises(cm.ConfigError):
            make_manager(defaults=bad_defaults, schema=schema)


def test_machines_relative_path_alias(make_manager):
    data_root = "C:/custom/data"
    relative = "maszyny/niestandardowe.json"
    mgr, paths = make_manager(
        global_cfg={
            "paths": {"data_root": data_root},
            "machines": {"relative_path": relative},
        }
    )

    expected = os.path.normpath(os.path.join(data_root, relative))
    assert cm.resolve_rel(mgr.merged, "machines") == expected

    with open(mgr.config_path(), encoding="utf-8") as f:
        stored = json.load(f)

    assert stored["machines"]["rel_path"] == relative
    assert "relative_path" not in stored["machines"]


def test_secret_admin_pin_masked(make_manager):
    schema = {
        "config_version": 1,
        "options": [{"key": "secrets.admin_pin", "type": "string"}],
    }
    defaults = {"secrets": {"admin_pin": ""}}

    mgr, paths = make_manager(defaults=defaults, schema=schema)
    mgr.set("secrets.admin_pin", "1234", who="tester")
    mgr.save_all()

    with open(mgr.config_path(), encoding="utf-8") as f:
        data = json.load(f)
    assert data["secrets"]["admin_pin"] == "1234"

    reloaded = cm.ConfigManager.refresh()
    assert reloaded.get("secrets.admin_pin") == "1234"

    audit_file = Path(paths["audit"]) / "config_changes.jsonl"
    with open(audit_file, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    rec = next(r for r in records if r["key"] == "secrets.admin_pin")
    assert rec["before"] == "***"
    assert rec["after"] == "***"


def test_refresh_with_custom_paths(tmp_path):
    schema = {"config_version": 1, "options": [{"key": "a", "type": "int"}]}
    cfg_data = {"a": 5}
    schema_path = tmp_path / "schema.json"
    cfg_path = tmp_path / "custom.json"
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg_data, f, ensure_ascii=False, indent=2)

    mgr = cm.ConfigManager.refresh(
        config_path=str(cfg_path), schema_path=str(schema_path)
    )
    try:
        assert mgr.get("a") == 5
    finally:
        cm.ConfigManager.refresh()


def test_backup_cloud_persistence(make_manager):
    schema = {
        "config_version": 1,
        "options": [
            {"key": "backup.cloud.url", "type": "string"},
            {"key": "backup.cloud.username", "type": "string"},
            {"key": "backup.cloud.password", "type": "string"},
            {"key": "backup.cloud.folder", "type": "string"},
        ],
    }
    defaults = {
        "backup": {
            "cloud": {
                "url": "",
                "username": "",
                "password": "",
                "folder": "",
            }
        }
    }

    mgr, paths = make_manager(defaults=defaults, schema=schema)
    assert mgr.get("backup.cloud.url") == ""
    assert mgr.get("backup.cloud.username") == ""
    assert mgr.get("backup.cloud.password") == ""
    assert mgr.get("backup.cloud.folder") == ""

    mgr.set("backup.cloud.url", "https://example.com")
    mgr.set("backup.cloud.username", "alice")
    mgr.set("backup.cloud.password", "secret")
    mgr.set("backup.cloud.folder", "/remote")
    mgr.save_all()

    with open(mgr.config_path(), encoding="utf-8") as f:
        data = json.load(f)
    assert data["backup"]["cloud"]["url"] == "https://example.com"
    assert data["backup"]["cloud"]["username"] == "alice"
    assert data["backup"]["cloud"]["password"] == "secret"
    assert data["backup"]["cloud"]["folder"] == "/remote"

    reloaded = cm.ConfigManager.refresh()
    assert reloaded.get("backup.cloud.url") == "https://example.com"
    assert reloaded.get("backup.cloud.username") == "alice"
    assert reloaded.get("backup.cloud.password") == "secret"
    assert reloaded.get("backup.cloud.folder") == "/remote"


def test_migrate_legacy_machines_files(tmp_path):
    data_root = tmp_path / "data"
    data_root.mkdir()

    legacy_path = data_root / "maszyny.json"
    legacy_payload = [
        {"nr_ewid": "100", "nazwa": "Legacy only"},
        {"nr_ewid": "42", "nazwa": "Legacy duplicate"},
    ]
    with open(legacy_path, "w", encoding="utf-8") as handle:
        json.dump(legacy_payload, handle, ensure_ascii=False, indent=2)

    primary_dir = data_root / "maszyny"
    primary_dir.mkdir()
    primary_path = primary_dir / "maszyny.json"
    primary_payload = [{"nr_ewid": "42", "nazwa": "Primary"}]
    with open(primary_path, "w", encoding="utf-8") as handle:
        json.dump(primary_payload, handle, ensure_ascii=False, indent=2)

    cfg = {"paths": {"data_root": str(data_root)}}
    migrated = cm.migrate_legacy_machines_files(cfg)

    assert migrated is True
    with open(primary_path, encoding="utf-8") as handle:
        merged = json.load(handle)

    assert {row["nr_ewid"] for row in merged} == {"42", "100"}
    primary_row = next(row for row in merged if row["nr_ewid"] == "42")
    assert primary_row["nazwa"] == "Primary"

    assert not legacy_path.exists()
    backups = list(data_root.glob("maszyny.json*.bak"))
    assert len(backups) == 1


def test_load_tool_vocab_merges_sources(tmp_path):
    data_root = tmp_path / "data"
    vocab_dir = data_root / "narzedzia"
    vocab_dir.mkdir(parents=True)

    types_file = vocab_dir / "typy_narzedzi.json"
    with types_file.open("w", encoding="utf-8") as handle:
        json.dump({"types": ["Plikowy"]}, handle, ensure_ascii=False, indent=2)

    statuses_file = vocab_dir / "statusy_narzedzi.json"
    with statuses_file.open("w", encoding="utf-8") as handle:
        json.dump({"NN": ["StatusZPliku"]}, handle, ensure_ascii=False, indent=2)

    tasks_file = vocab_dir / "szablony_zadan.json"
    with tasks_file.open("w", encoding="utf-8") as handle:
        json.dump({"NN": {"StatusZPliku": ["Zadanie z pliku"]}}, handle, ensure_ascii=False, indent=2)

    cfg = {
        "paths": {"data_root": str(data_root)},
        "tools": {
            "types": ["Nowe"],
            "statuses": ["Własny"],
            "task_templates": ["Checklist"],
        },
        "typy_narzedzi": ["Legacy"],
        "szablony_zadan_narzedzia": ["Stare"],
        "statusy_narzedzi": ["Historyczny"],
    }

    vocab = cm.load_tool_vocab(cfg)

    assert vocab["types"] == ["Nowe", "Legacy", "Plikowy"]
    assert vocab["statuses"] == ["Własny", "Historyczny", "StatusZPliku"]
    assert vocab["task_templates"] == ["Checklist", "Stare", "Zadanie z pliku"]

    assert "typy_narzedzi" not in cfg
    assert "szablony_zadan_narzedzia" not in cfg
    assert "statusy_narzedzi" not in cfg
    assert cfg["tools"]["types"] == vocab["types"]
    assert cfg["tools"]["statuses"] == vocab["statuses"]
    assert cfg["tools"]["task_templates"] == vocab["task_templates"]


def test_ui_theme_defaults_and_aliases(make_manager):
    schema = {
        "config_version": 1,
        "options": [
            {
                "key": "ui.theme",
                "type": "select",
                "default": "dark",
                "values": ["dark", "light"],
            },
            {
                "key": "ui.language",
                "type": "select",
                "default": "pl",
                "values": ["pl", "en"],
            },
            {
                "key": "ui.start_on_dashboard",
                "type": "boolean",
                "default": True,
            },
            {
                "key": "ui.auto_check_updates",
                "type": "boolean",
                "default": True,
            },
            {
                "key": "ui.debug_enabled",
                "type": "boolean",
                "default": True,
            },
            {
                "key": "ui.log_level",
                "type": "select",
                "default": "debug",
                "values": ["debug", "info", "error"],
            },
        ],
    }

    legacy = {
        "system": {
            "theme": "light",
            "language": "en",
            "start_on_dashboard": False,
            "auto_check_updates": False,
            "debug_enabled": False,
            "log_level": "info",
        }
    }
    mgr, paths = make_manager(schema=schema, global_cfg=legacy)

    assert mgr.get("ui.theme") == "light"
    assert mgr.get("ui.language") == "en"
    assert mgr.get("system.theme") == "light"
    assert mgr.get("system.language") == "en"
    assert mgr.get("ui.start_on_dashboard") is False
    assert mgr.get("system.start_on_dashboard") is False
    assert mgr.get("ui.auto_check_updates") is False
    assert mgr.get("system.auto_check_updates") is False
    assert mgr.get("ui.debug_enabled") is False
    assert mgr.get("system.debug_enabled") is False
    assert mgr.get("ui.log_level") == "info"
    assert mgr.get("system.log_level") == "info"

    with open(mgr.config_path(), encoding="utf-8") as handle:
        stored = json.load(handle)
    assert stored["ui"]["theme"] == "light"
    assert stored["ui"]["language"] == "en"
    assert stored["ui"]["start_on_dashboard"] is False
    assert stored["ui"]["auto_check_updates"] is False
    assert stored["ui"]["debug_enabled"] is False
    assert stored["ui"]["log_level"] == "info"
    assert "theme" not in stored.get("system", {})
    assert "language" not in stored.get("system", {})
    assert "start_on_dashboard" not in stored.get("system", {})
    assert "auto_check_updates" not in stored.get("system", {})
    assert "debug_enabled" not in stored.get("system", {})
    assert "log_level" not in stored.get("system", {})

    mgr.set("ui.theme", "dark", who="tester")
    mgr.set("ui.language", "pl", who="tester")
    mgr.save_all()

    with open(mgr.config_path(), encoding="utf-8") as handle:
        updated = json.load(handle)
    assert updated["ui"]["theme"] == "dark"
    assert updated["ui"]["language"] == "pl"
    assert "theme" not in updated.get("system", {})
    assert "language" not in updated.get("system", {})


def test_profiles_migration_creates_new_structure(make_manager):
    legacy_profiles = {
        "tab_enabled": True,
        "show_name_in_header": True,
        "avatar_dir": "avatars",
        "fields_editable_by_user": ["telefon"],
        "allow_pin_change": True,
        "task_default_deadline_days": 7,
    }

    mgr, paths = make_manager(global_cfg={"profiles": legacy_profiles})

    assert mgr.get("profiles.editable_fields") == ["telefon"]
    assert mgr.get("profiles.pin.change_allowed") is True
    assert mgr.get("profiles.pin.min_length") == 4
    assert mgr.get("profiles.avatar.directory") == "avatars"
    assert mgr.get("profiles.avatar.enabled") is False

    with open(mgr.config_path(), encoding="utf-8") as handle:
        stored = json.load(handle)
    stored_profiles = stored.get("profiles", {})
    assert "fields_editable_by_user" not in stored_profiles
    assert "allow_pin_change" not in stored_profiles
    assert "avatar_dir" not in stored_profiles
    assert stored_profiles["pin"]["change_allowed"] is True


def test_path_helpers_expand_relative_entries(make_manager, tmp_path):
    root = tmp_path / "wm_root"
    root.mkdir()
    (root / "data").mkdir()

    global_cfg = {
        "paths": {
            "data_root": str(root),
            "backup_dir": "backup",
            "logs_dir": "logs",
        }
    }

    mgr, _ = make_manager(global_cfg=global_cfg)

    expected_root = os.path.normpath(str(root))
    assert mgr.path_root() == expected_root
    assert mgr.path_data() == os.path.normpath(os.path.join(expected_root, "data"))
    assert mgr.path_backup() == os.path.normpath(os.path.join(expected_root, "backup"))
    assert mgr.path_logs() == os.path.normpath(os.path.join(expected_root, "logs"))


def test_config_manager_migrates_tool_vocab(make_manager, tmp_path):
    data_root = tmp_path / "data"
    data_root.mkdir()
    (data_root / "narzedzia").mkdir()

    schema = {
        "config_version": 1,
        "options": [
            {"key": "paths.data_root", "type": "path"},
            {"key": "tools.types", "type": "array"},
            {"key": "tools.statuses", "type": "array"},
            {"key": "tools.task_templates", "type": "array"},
        ],
    }

    defaults = {
        "paths": {"data_root": str(data_root)},
        "tools": {
            "types": ["Default"],
            "statuses": ["Domyślny"],
            "task_templates": ["Szablon"],
        },
    }

    global_cfg = {
        "paths": {"data_root": str(data_root)},
        "tools": {
            "types": ["Nowy"],
            "statuses": ["Własny"],
            "task_templates": ["Checklist"],
        },
        "typy_narzedzi": ["Legacy"],
        "szablony_zadan_narzedzia": ["Do migracji"],
    }

    mgr, paths = make_manager(
        defaults=defaults, global_cfg=global_cfg, schema=schema
    )

    assert mgr.get("tools.types") == ["Nowy", "Legacy"]
    assert mgr.get("tools.task_templates") == ["Checklist", "Do migracji"]
    assert mgr.get("tools.statuses") == ["Własny"]

    with open(mgr.config_path(), encoding="utf-8") as handle:
        stored = json.load(handle)

    assert "typy_narzedzi" not in stored
    assert "szablony_zadan_narzedzia" not in stored
    assert stored["tools"]["types"] == ["Nowy", "Legacy"]
    assert stored["tools"]["task_templates"] == ["Checklist", "Do migracji"]
