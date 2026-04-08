# version: 1.0
import logging

import profile_utils


def test_manifest_fallback_adds_core_modules(monkeypatch, caplog):
    monkeypatch.setattr(profile_utils, "_lista_modulow", lambda: ["ustawienia"])
    with caplog.at_level(logging.WARNING, logger=profile_utils._LOGGER.name):
        modules = profile_utils._compute_sidebar_modules()
    keys = [key for key, _ in modules]
    for expected in ("narzedzia", "maszyny", "zlecenia", "magazyn"):
        assert expected in keys
    warnings = [rec.message for rec in caplog.records if "Manifest modułów" in rec.message]
    assert warnings, "should log diagnostic warning when manifest misses core modules"
