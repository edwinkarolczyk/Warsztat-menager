# version: 1.0
"""Zgodność wsteczna: deleguje do backend.audytowego modułu runtime."""

from backend.audit.wm_audit_runtime import run_audit  # noqa: F401
