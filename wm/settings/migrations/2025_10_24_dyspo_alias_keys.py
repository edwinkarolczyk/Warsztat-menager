# version: 1.0
"""Migration copying legacy ZZ/ZM/ZW/ZN keys into dyspo section."""

from __future__ import annotations

from wm.settings.util import get_conf, save_conf

ALIAS_MAP = {"ZM": "DM", "ZZ": "DZ", "ZW": "DW", "ZN": "DN"}
LEGACY_PREFIXES = tuple(ALIAS_MAP.keys())


def migrate() -> None:
    conf = get_conf()
    dyspo = conf.setdefault("dyspo", {})
    enabled = set(dyspo.get("enabled_types") or [])
    numbering = dict(dyspo.get("numbering") or {})

    for legacy in LEGACY_PREFIXES:
        new_code = ALIAS_MAP[legacy]
        enable_key = f"enable_{legacy}"
        if conf.get(enable_key) is True:
            enabled.add(new_code)
        pattern_key = f"num_pattern_{legacy}"
        counter_key = f"num_counter_{legacy}"
        pattern = conf.get(pattern_key)
        counter = conf.get(counter_key)
        if pattern or counter is not None:
            entry = numbering.setdefault(new_code, {})
            if pattern:
                entry["pattern"] = pattern
            if counter is not None:
                try:
                    entry["counter"] = int(counter)
                except (TypeError, ValueError):
                    pass

    if enabled:
        dyspo["enabled_types"] = sorted(enabled)
    if numbering:
        dyspo["numbering"] = numbering

    save_conf(conf)


if __name__ == "__main__":
    migrate()
