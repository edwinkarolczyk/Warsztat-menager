# version: 1.0
import start


def test_auto_login_success(monkeypatch):
    class DummyCfg:
        def get(self, key, default=None):
            mapping = {
                "auth.auto_login_enabled": True,
                "auth.auto_login_profile": "auto",
            }
            return mapping.get(key, default)

    monkeypatch.setattr(start, "ConfigManager", lambda: DummyCfg())
    monkeypatch.setattr(
        start.profile_service,
        "get_user",
        lambda login: {"login": login, "rola": "administrator", "active": True},
    )

    called = {}

    def fake_on_login(root, login, rola, extra=None):
        called["args"] = (root, login, rola, extra)

    monkeypatch.setattr(start, "_on_login", fake_on_login)
    start.SESSION_ID = "TEST"

    root = object()
    assert start._auto_login_if_enabled(root) is True
    assert called["args"][0] is root
    assert called["args"][1] == "auto"
    assert called["args"][2] == "administrator"
    assert called["args"][3]["auto_login"] is True


def test_auto_login_missing_profile(monkeypatch):
    class DummyCfg:
        def get(self, key, default=None):
            mapping = {
                "auth.auto_login_enabled": True,
                "auth.auto_login_profile": "ghost",
            }
            return mapping.get(key, default)

    monkeypatch.setattr(start, "ConfigManager", lambda: DummyCfg())
    monkeypatch.setattr(start.profile_service, "get_user", lambda login: None)

    called = {}

    def fake_on_login(root, login, rola, extra=None):
        called["called"] = True

    monkeypatch.setattr(start, "_on_login", fake_on_login)
    start.SESSION_ID = "TEST"

    assert start._auto_login_if_enabled(object()) is False
    assert called == {}
