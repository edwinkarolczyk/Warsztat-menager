# version: 1.0
# migrate_profiles_config.py
# Minimalny migrator config.json -> dodaje profiles.* jeśli brak, bez ruszania reszty
import json, sys, os

PATH = sys.argv[1] if len(sys.argv)>1 else "config.json"
with open(PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

profiles = cfg.get("profiles") if isinstance(cfg.get("profiles"), dict) else {}

legacy_editable = profiles.pop("fields_editable_by_user", None)
legacy_pin = profiles.pop("allow_pin_change", None)
legacy_avatar = profiles.pop("avatar_dir", None)

defaults = {
    "tab_enabled": True,
    "show_name_in_header": True,
    "fields_visible": ["login","nazwa","rola","zmiana"],
    "editable_fields": [
        "imie",
        "nazwisko",
        "staz",
        "telefon",
        "email"
    ],
    "avatar": {"enabled": False, "directory": ""},
    "pin": {"change_allowed": False},
    "task_default_deadline_days": 7,
}
changed=False
for k,v in defaults.items():
    if profiles.get(k) is None:
        profiles[k]=v; changed=True

if legacy_editable is not None and not profiles.get("editable_fields"):
    profiles["editable_fields"] = legacy_editable
if legacy_pin is not None:
    profiles.setdefault("pin", {})["change_allowed"] = bool(legacy_pin)
if legacy_avatar is not None:
    profiles.setdefault("avatar", {})["directory"] = legacy_avatar

profiles.setdefault("pin", {}).setdefault("change_allowed", False)
profiles.setdefault("avatar", {}).setdefault("enabled", False)
profiles.setdefault("avatar", {}).setdefault("directory", "")
editable = profiles.get("editable_fields")
if not isinstance(editable, list):
    if isinstance(editable, str):
        profiles["editable_fields"] = [editable]
    elif isinstance(editable, (set, tuple)):
        profiles["editable_fields"] = list(editable)
    else:
        profiles["editable_fields"] = []
cfg["profiles"]=profiles

# płaskie klucze – dodaj tylko jeśli brak
flat = {
    "profiles.tab_enabled": profiles["tab_enabled"],
    "profiles.show_name_in_header": profiles["show_name_in_header"],
    "profiles.avatar.enabled": profiles["avatar"]["enabled"],
    "profiles.avatar.directory": profiles["avatar"]["directory"],
    "profiles.fields_visible": profiles["fields_visible"],
    "profiles.editable_fields": profiles["editable_fields"],
    "profiles.pin.change_allowed": profiles["pin"]["change_allowed"],
    "profiles.task_default_deadline_days": profiles["task_default_deadline_days"],
}
for k,v in flat.items():
    if k not in cfg:
        cfg[k]=v; changed=True

if changed:
    bak = PATH + ".bak"
    if not os.path.exists(bak):
        with open(bak,"w",encoding="utf-8") as f: json.dump(cfg, f, ensure_ascii=False, indent=2)
    with open(PATH,"w",encoding="utf-8") as f: json.dump(cfg, f, ensure_ascii=False, indent=2)
    print("[OK] Zaktualizowano", PATH, " (backup:", bak, ")")
else:
    print("[OK] Nic do zmiany – config jest aktualny")
