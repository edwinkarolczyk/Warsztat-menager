# version: 1.0
import os
from typing import Dict, Optional


# Domyślny katalog danych używany jako ostateczne zabezpieczenie.
DEFAULT_ROOT = "data"


def _fallback_root(cfg: Dict) -> str:
    """Return the configured root using :mod:`config_manager` when possible."""

    try:  # Lazy import to avoid circular dependencies during module import.
        from config_manager import get_root  # type: ignore

        resolved = get_root(cfg)
        if isinstance(resolved, str) and resolved.strip():
            return resolved
    except Exception:
        pass
    return DEFAULT_ROOT


def root_dir(cfg: Dict) -> str:
    """Return the root directory for data files.

    Falls back to the application-wide ``<root>`` directory and ultimately to
    ``data`` when configuration is missing or incomplete.
    """

    root = (cfg.get("paths", {}) or {}).get("data_root")
    if isinstance(root, str) and root.strip():
        return os.path.normpath(root.strip())
    return os.path.normpath(_fallback_root(cfg))


def rel_to_root(cfg: Dict, rel: str) -> str:
    """Return *rel* resolved against the configured root directory."""

    return os.path.normpath(os.path.join(root_dir(cfg), rel))


def tools_dir(cfg: Dict) -> str:
    """Return the absolute path to the tools directory under root."""

    return rel_to_root(cfg, r"narzedzia")


def tools_file(cfg: Dict, filename: str) -> str:
    """Return the absolute path for *filename* inside the tools directory.

    Ensures the directory exists and normalises ``.jslon`` extensions to
    ``.json`` as well as appending ``.json`` when missing.
    """

    base = tools_dir(cfg)
    os.makedirs(base, exist_ok=True)
    fn = (filename or "").strip()
    if fn.lower().endswith(".jslon"):
        fn = fn[:-6] + ".json"
    if not fn.lower().endswith(".json"):
        fn = f"{fn}.json"
    return os.path.join(base, fn)


def _anchor_root(cfg: Optional[Dict] = None) -> str:
    """Return the resolved anchor directory for placeholder paths."""

    cfg = cfg or {}
    try:  # Lazy import to avoid circular import at module load time
        from config_manager import get_root  # type: ignore

        root = get_root(cfg)
        if isinstance(root, str) and root.strip():
            return os.path.normpath(root.strip())
    except Exception:
        pass
    return os.path.normpath(os.getcwd())


def resolve_rel(value: os.PathLike[str] | str | None, *extra: str, cfg: Optional[Dict] = None) -> str:
    """Resolve ``value`` against the WM root directory.

    ``value`` may contain the ``<root>`` placeholder or be a relative
    fragment. ``extra`` path components are appended before resolving. When no
    value is provided the anchor root directory is returned.
    """

    cfg = cfg or {}
    anchor = _anchor_root(cfg)

    parts: list[str] = []
    if value:
        parts.append(os.fspath(value))
    parts.extend(extra)

    combined = os.path.join(*parts) if parts else ""
    if not combined:
        return anchor

    candidate = combined
    for placeholder in ("<root>", "<ROOT>"):
        if placeholder in candidate:
            candidate = candidate.replace(placeholder, anchor)

    candidate = candidate.strip()
    if not candidate:
        return anchor

    if not os.path.isabs(candidate) and not candidate.startswith("\\\\"):
        candidate = os.path.join(anchor, candidate)

    return os.path.normpath(candidate)


__all__ = [
    "DEFAULT_ROOT",
    "root_dir",
    "rel_to_root",
    "tools_dir",
    "tools_file",
    "resolve_rel",
]
