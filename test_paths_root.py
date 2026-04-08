# version: 1.0
"""Smoke tests for root path resolution helpers."""

from utils_paths import resolve_rel


def test_resolve_rel_root_placeholder() -> None:
    resolved = resolve_rel("<root>")
    assert resolved, "resolve_rel should return a non-empty path"
    assert "<root>" not in resolved
    assert "C:" not in resolved
