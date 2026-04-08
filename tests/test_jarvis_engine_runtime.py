# version: 1.0
from __future__ import annotations

from core.jarvis_engine import anonymize_for_ai, local_diagnostics, run_analysis_report


def test_anonymize_for_ai_masks_sensitive_fields() -> None:
    payload = {
        "login": "Jan.Kowalski",
        "owner": "anna.nowak",
        "opis": "Operator Jan Kowalski obsługuje maszynę",
        "ścieżka": "C:/tajne/dane.txt",
        "adres": "10.1.2.3",
    }

    sanitized = anonymize_for_ai(payload)

    flat_values = [value for value in sanitized.values() if isinstance(value, str)]

    assert any(value.startswith("user_") for value in flat_values)
    assert any("path_" in value for value in flat_values)
    assert any(value.startswith("ip_") for value in flat_values)
    for value in flat_values:
        assert "Jan" not in value
        assert "Kowalski" not in value
        assert "tajne" not in value
        assert "10.1.2.3" not in value


def test_local_diagnostics_detects_missing_root(tmp_path) -> None:
    missing_root = tmp_path / "dane"
    stats = {"narzedzia": {}, "maszyny": {}, "zlecenia": {}, "operatorzy": {}}

    alerts = local_diagnostics(stats, cfg=None, root=missing_root)

    assert any("Katalog danych warsztatu nie istnieje" in alert.message for alert in alerts)


def test_local_diagnostics_reports_slow_module_and_empty_definitions(tmp_path) -> None:
    data_root = tmp_path / "root"
    data_root.mkdir()
    (data_root / "zadania_narzedzia.json").write_text("{}", encoding="utf-8")
    log_path = data_root / "logi_gui.txt"
    log_path.write_text(
        "[2024-01-01 10:00:00] Kliknięto: Narzędzia\n"
        "[2024-01-01 10:00:04] Otworzono: Narzędzia\n",
        encoding="utf-8",
    )

    stats = {
        "narzedzia": {"count": 0},
        "maszyny": {"count": 0},
        "zlecenia": {"count": 0},
        "operatorzy": {"count": 0},
    }

    alerts = local_diagnostics(stats, cfg=None, root=data_root)

    messages = "\n".join(f"{alert.level}:{alert.message}" for alert in alerts)
    assert "tools.definitions_path" in messages or "definic" in messages
    assert "Narzędzia" in messages
    assert "Brak plików narzędzi" in messages


def test_run_analysis_report_offline_when_ai_disabled(monkeypatch) -> None:
    report = run_analysis_report(allow_ai=False)

    assert report.summary
    assert report.offline is True
    assert report.metadata.get("offline_reason") == "disabled"
