# version: 1.0
"""Smoke test for Dyspozycje schema section."""

import json
from pathlib import Path

import pytest

try:
    import jsonschema
except ImportError:  # pragma: no cover - dependency optional in legacy envs
    pytest.skip("jsonschema not available", allow_module_level=True)


def test_config_matches_schema() -> None:
    conf = json.loads(Path("config.defaults.json").read_text(encoding="utf-8"))
    schema = json.loads(Path("settings_schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(conf, schema)
