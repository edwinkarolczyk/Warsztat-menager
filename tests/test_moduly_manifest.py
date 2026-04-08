# version: 1.0
# tests/test_moduly_manifest.py
# Szybki smoke test manifestu (nie zmienia działania programu).
from utils.moduly import (
    module_active,
    zaladuj_manifest,
    lista_modulow,
    pobierz_modul,
    zaleznosci,
)


def test_manifest_smoke():
    man = zaladuj_manifest()
    mods = lista_modulow(man)
    assert "magazyn" in mods
    assert "zlecenia" in mods
    assert "jarvis" in mods
    z = pobierz_modul("zlecenia", man)
    assert z["id"] == "zlecenia"
    assert isinstance(z.get("depends", []), list)
    assert isinstance(zaleznosci("zlecenia", man), list)


def test_module_active_override():
    cfg = {"modules": {"active": {"magazyn": False}}}
    manifest = zaladuj_manifest()
    assert module_active("magazyn", manifest=manifest, cfg=cfg) is True


def test_narzedzia_active_by_default():
    cfg = {"modules": {"active": {}}}
    manifest = zaladuj_manifest()
    assert module_active("narzedzia", manifest=manifest, cfg=cfg) is True
