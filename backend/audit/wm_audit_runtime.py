# version: 1.0
from __future__ import annotations
import os
import time
from typing import Any, Dict, List, Callable

from config.paths import get_path, join_path, ensure_core_tree
from config_manager import (
    ConfigManager,
    resolve_rel,
    get_root,
    get_machines_path,
    get_by_key,
)
from wm_log import dbg as wm_dbg, info as wm_info, err as wm_err

import json
from pathlib import Path


def wm_warn(where: str, msg: str, exc: BaseException | None = None, **kv: object) -> None:
    if exc is not None:
        kv = {**kv, "exc": repr(exc)}
    wm_info(where, msg, **kv)


_AUDIT_DATA_CANDIDATES = [
    Path("data") / "audyt.json",
    Path("config") / "audit_points.json",
]


def _load_extended_audit_data() -> dict | None:
    """Czyta rozszerzony audyt (Roadmapa) z pliku danych. Zwraca dict z 'groups' albo None."""
    for p in _AUDIT_DATA_CANDIDATES:
        try:
            if p.exists():
                with p.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict) and isinstance(data.get("groups"), list):
                    wm_info("audit.run", "extended_loaded", path=str(p))
                    return data
        except Exception as e:
            wm_warn("audit.run", "extended_read_failed", e, path=str(p))
    return None


def _flatten_extended_audit_rows(data: dict) -> list[tuple[str, str, str, bool, str]]:
    """Spłaszcza groups/items do wierszy: (group, id, label, done, notes)."""
    rows: list[tuple[str, str, str, bool, str]] = []
    try:
        for g in data.get("groups", []):
            gname = str(g.get("name", ""))
            for it in g.get("items", []):
                rid = str(it.get("id", ""))
                label = str(it.get("label", ""))
                done = bool(it.get("done", False))
                notes = str(it.get("notes", ""))
                rows.append((gname, rid, label, done, notes))
    except Exception as e:
        wm_warn("audit.run", "extended_flatten_failed", e)
    return rows

__all__ = ["run", "run_audit"]

_LEGACY_FALLBACKS: Dict[str, str] = {
    "machines": "hall.machines_file",
    "warehouse": "warehouse.stock_source",
    "bom": "bom.file",
    "tools.types": "tools.types_file",
    "tools.statuses": "tools.statuses_file",
    "tools.tasks": "tools.task_templates_file",
    "orders": "orders.file",
}


def _exists(path: str) -> bool:
    return bool(path) and os.path.exists(path)


def _check_machines_sources(cfg: Dict[str, Any]) -> tuple[bool, str]:
    """Return audit result for duplicated machine sources."""

    primary = get_machines_path(cfg)
    legacy = resolve_rel(cfg, r"maszyny.json")

    def _normalized(path: str | None) -> str:
        if not path:
            return ""
        try:
            return os.path.normcase(os.path.abspath(path))
        except Exception:
            return path or ""

    primary_exists = _exists(primary)
    legacy_exists = _exists(legacy)
    if primary_exists and legacy_exists and _normalized(primary) != _normalized(legacy):
        return False, f"primary={primary} legacy={legacy}"
    if primary_exists:
        return True, primary
    if legacy_exists:
        return False, legacy
    return False, "(brak pliku maszyn)"


_CONFIG_AUDIT_RULES: list[tuple[str, type, bool]] = [
    ("ui.theme", str, False),
    ("ui.language", str, False),
    ("ui.start_on_dashboard", bool, False),
    ("ui.auto_check_updates", bool, False),
    ("ui.debug_enabled", bool, False),
    ("ui.log_level", str, False),
    ("paths.data_root", str, False),
    ("paths.logs_dir", str, False),
    ("paths.backup_dir", str, False),
    ("paths.layout_dir", str, False),
    ("profiles.editable_fields", list, False),
    ("profiles.pin.change_allowed", bool, False),
    ("profiles.pin.min_length", int, False),
    ("profiles.avatar.enabled", bool, False),
    ("backup.keep_last", int, False),
    ("updates.auto_pull", bool, False),
    ("machines.rel_path", str, False),
    ("tools.types", list, False),
    ("tools.statuses", list, False),
    ("tools.task_templates", list, False),
]


def _format_detail(value: Any) -> str:
    if isinstance(value, list):
        return f"len={len(value)}"
    if isinstance(value, bool):
        return "True" if value else "False"
    if value is None:
        return "(brak)"
    return str(value)


def _audit_config_sections(
    cfg: Dict[str, Any], add: Callable[[str, bool, str], None]
) -> None:
    """Validate presence of critical configuration sections and emit audit entries."""

    for dotted, expected_type, allow_empty in _CONFIG_AUDIT_RULES:
        value = get_by_key(cfg, dotted, None)

        ok = isinstance(value, expected_type)
        if ok and expected_type is str:
            ok = bool(str(value).strip())
        elif ok and expected_type is list and not allow_empty:
            ok = len(value) > 0

        detail = _format_detail(value)

        if not ok:
            print(f"[WM-DBG][AUDIT] missing {dotted}: {detail}")
        add(f"config.{dotted}", ok, detail)


def run() -> dict:
    """
    Wykonuje prosty audyt środowiska WM:
      - sprawdza istnienie podstawowych katalogów/plików,
      - zapisuje raport do logs/audyt_wm-{timestamp}.txt,
      - zwraca {ok, msg, path}.
    """
    wm_dbg("audit.run", "enter")
    try:
        ensure_core_tree()

        data_override_pref = get_path("paths.data_root")
        logs_override_pref = get_path("paths.logs_dir")
        backup_override_pref = get_path("paths.backup_dir")

        try:
            manager = ConfigManager()
            cfg: Dict[str, Any] = (
                manager.merged if isinstance(manager.merged, dict) else {}
            )
        except Exception as exc:
            wm_warn("audit.run", "config_load_failed", exc)
            manager = None
            cfg = {}

        checks = []

        def add(name: str, ok: bool, detail: str = ""):
            checks.append({"name": name, "ok": ok, "detail": detail})

        paths_cfg = cfg.get("paths") if isinstance(cfg.get("paths"), dict) else {}

        overrides_lookup = {
            "data_root": data_override_pref,
            "logs_dir": logs_override_pref,
            "backup_dir": backup_override_pref,
        }

        if manager:
            data_dir = manager.path_data()
            root_dir = manager.path_root()
            logs_dir = manager.path_logs()
            backup_dir = manager.path_backup()
            if data_override_pref:
                override_path = Path(data_override_pref)
                if override_path.name.lower() == "data":
                    data_dir = str(override_path)
                    root_dir = str(override_path.parent)
                else:
                    root_dir = str(override_path)
                    data_dir = os.path.join(root_dir, "data")
            if logs_override_pref:
                logs_dir = str(logs_override_pref)
            if backup_override_pref:
                backup_dir = str(backup_override_pref)
        else:
            raw_root = (data_override_pref or "").strip() or (get_root(cfg) or "").strip()
            if raw_root:
                root_path = Path(raw_root)
                if root_path.name.lower() == "data":
                    root_dir = str(root_path.parent)
                    data_dir = str(root_path)
                else:
                    root_dir = str(root_path)
                    data_dir = os.path.join(root_dir, "data")
            else:
                root_dir = os.getcwd()
                data_dir = os.path.join(root_dir, "data")
            logs_dir = os.path.join(root_dir, "logs")
            backup_dir = os.path.join(root_dir, "backup")

        mach_path = get_machines_path(cfg)
        tools_path = os.path.join(data_dir, "zadania_narzedzia.json")
        profiles_path = os.path.join(data_dir, "profiles.json")
        print(
            f"[WM-DBG][AUDIT] using machines={mach_path} tools={tools_path} profiles={profiles_path}"
        )

        def _fallback_from_paths(key: str, default_rel: str = "") -> str:
            val = (paths_cfg.get(key) or overrides_lookup.get(key) or "").strip()
            if not val:
                val = (get_path(f"paths.{key}") or "").strip()
            if val:
                return val
            if default_rel:
                if key == "data_root":
                    return data_dir
                base_dir = root_dir if key in {"logs_dir", "backup_dir"} else data_dir
                return os.path.join(base_dir, default_rel)
            return ""

        data_override = _fallback_from_paths("data_root")
        if data_override:
            data_dir = data_override
            root_dir = os.path.dirname(data_dir)
            if os.path.basename(data_dir).lower() != "data":
                root_dir = data_dir
        logs_candidate = _fallback_from_paths("logs_dir", "logs")
        backups_candidate = _fallback_from_paths("backup_dir", "backup")
        logs_dir = logs_candidate or logs_dir
        backup_dir = backups_candidate or backup_dir

        data_dir = os.path.normpath(data_dir)
        logs_dir = os.path.normpath(logs_dir)
        backup_dir = os.path.normpath(backup_dir)

        add("data_root", _exists(data_dir), data_dir)
        add("logs_dir", _exists(logs_dir), logs_dir)
        add("backup_dir", _exists(backup_dir), backup_dir)

        def resolved(key: str) -> str:
            overrides = {
                "machines": mach_path,
                "tools.zadania": tools_path,
                "profiles": profiles_path,
            }
            if key in overrides:
                return overrides[key]
            path = resolve_rel(cfg, key)
            if path:
                return path
            legacy_key = _LEGACY_FALLBACKS.get(key)
            return get_path(legacy_key) if legacy_key else ""

        # Pliki i źródła
        for key in (
            "machines",
            "warehouse",
            "bom",
            "tools.types",
            "tools.statuses",
            "tools.tasks",
            "tools.zadania",
            "orders",
        ):
            path_val = resolved(key)
            add(key, _exists(path_val), path_val)

        ok_sources, sources_detail = _check_machines_sources(cfg)
        add("machines.sources", ok_sources, sources_detail)

        tools_dir = resolve_rel(cfg, "tools.dir")
        if not tools_dir:
            tools_dir = _fallback_from_paths("tools_dir", "narzedzia")
        add("tools.dir", _exists(tools_dir), tools_dir)

        machines_layout = get_path("hall.machines_file")
        add("hall.machines_file", _exists(machines_layout), machines_layout)

        machines_cfg = cfg.get("machines") if isinstance(cfg.get("machines"), dict) else {}
        machines_file_hint = (machines_cfg.get("file") or "").strip()
        if not machines_file_hint:
            add(
                "machines.file",
                False,
                "Wskaż plik maszyn w Ustawienia → Maszyny (machines.file)",
            )

        bg_img = get_path("hall.background_image", "")
        if bg_img:
            add("hall.background_image", _exists(bg_img), bg_img)
        else:
            add("hall.background_image", True, "(nie ustawiono — opcjonalne)")

        _audit_config_sections(cfg, add)

        # Podsumowanie
        failed = [c for c in checks if not c["ok"]]
        ok_all = len(failed) == 0
        summary = (
            f"OK: {len(checks) - len(failed)} / {len(checks)}; FAIL: {len(failed)}"
        )

        # Zapis raportu
        ts = time.strftime("%Y%m%d-%H%M%S")
        target_logs_dir = (
            overrides_lookup.get("logs_dir")
            or logs_dir
            or get_path("paths.logs_dir")
        )
        if target_logs_dir:
            out_path = os.path.join(target_logs_dir, f"audyt_wm-{ts}.txt")
        else:
            out_path = join_path("paths.logs_dir", f"audyt_wm-{ts}.txt")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        lines: List[str] = [
            f"Audyt WM — {ts}",
            "=" * 40,
            f"data_dir : {data_dir}",
            f"logs_dir : {logs_dir}",
            f"backup_dir: {backup_dir}",
            "-" * 40,
        ]
        for c in checks:
            lines.append(
                f"[{ 'OK' if c['ok'] else 'FAIL' }] {c['name']}: {c['detail']}"
            )
        lines.append("-" * 40)
        lines.append(summary)

        # --- BEGIN EXTENDED AUDIT APPEND ---
        try:
            _ext = _load_extended_audit_data()
            if _ext:
                _rows = _flatten_extended_audit_rows(_ext)
                if _rows:
                    lines.append("")  # odstęp
                    lines.append("---- ROADMAP AUDYT (data/audyt.json) ----")
                    total = len(_rows)
                    done = sum(1 for r in _rows if r[3] is True)
                    lines.append(f"Pozycje: {total} | Wykonane: {done} | Otwarte: {total-done}")
                    lines.append("")  # odstęp

                    # format jednej linii: [OK|TODO] Grupa :: ID – Opis  (notatka)
                    for (grp, rid, label, ok, notes) in _rows:
                        status = "OK" if ok else "TODO"
                        # skracanie bardzo długich notatek do czytelnego raportu
                        nshort = notes.strip()
                        if len(nshort) > 120:
                            nshort = nshort[:117] + "..."
                        line = f"[{status}] {grp} :: {rid} – {label}"
                        if nshort:
                            line += f"  ({nshort})"
                        lines.append(line)

                    lines.append("---- /ROADMAP AUDYT ----")
                    wm_info("audit.run", "extended_appended", count=total, done=done)
        except Exception as _e:
            wm_warn("audit.run", "extended_append_failed", _e)
        # --- END EXTENDED AUDIT APPEND ---

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        wm_info("audit.run", "written", path=out_path, summary=summary)
        return {"ok": ok_all, "msg": summary, "path": out_path}
    except Exception as e:  # pragma: no cover - logowanie błędów
        wm_err("audit.run", "exception", e)
        return {"ok": False, "msg": "Błąd audytu – szczegóły w logu."}


def run_audit() -> str:
    """Uruchamia audyt i zwraca treść raportu jako tekst."""
    result = run()
    report_path = result.get("path") if isinstance(result, dict) else None
    if report_path and os.path.exists(report_path):
        try:
            with open(report_path, "r", encoding="utf-8") as handle:
                report = handle.read()
        except Exception as exc:  # pragma: no cover - logowanie błędów
            wm_err("audit.run_audit", "read_failed", exc, path=report_path)
        else:
            wm_info("audit.run_audit", "report_ready", path=report_path)
            return report

    summary = ""
    if isinstance(result, dict):
        summary = result.get("msg") or ""
        try:
            serialized = json.dumps(result, ensure_ascii=False, indent=2)
        except Exception:
            serialized = summary or str(result)
    else:
        serialized = str(result)

    wm_info("audit.run_audit", "fallback", summary=summary)
    return serialized
