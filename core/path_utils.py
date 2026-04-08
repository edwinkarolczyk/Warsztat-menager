# version: 1.0
import os
import sys
from pathlib import Path
from typing import Union


def get_app_root() -> Path:
    """Return the application root directory handling PyInstaller bundles."""

    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]

PathLike = Union[os.PathLike[str], str, None]


def _normalized_base(base_root: Union[str, Path]) -> str:
    base = str(base_root) if base_root is not None else ""
    base = base.strip()
    if not base:
        base = os.getcwd()
    return os.path.normpath(base)


def resolve_root_path(base_root: Union[str, Path], raw_path: PathLike) -> str:
    """Resolve ``raw_path`` relative to ``base_root`` handling ``<root>`` tokens."""

    base_raw = str(base_root) if base_root is not None else ""
    base_raw = base_raw.strip()
    if not base_raw:
        base_raw = str(get_app_root())
    elif base_raw.lower().startswith("<root>") or base_raw.lower() == "<root>":
        anchor = str(get_app_root())
        base_raw = base_raw.replace("<root>", anchor).replace("<ROOT>", anchor)
    base = os.path.normpath(os.path.expanduser(base_raw))

    if raw_path is None:
        return base

    raw = str(os.fspath(raw_path)).strip()
    if not raw:
        return base

    if "<root>" in raw or "<ROOT>" in raw:
        raw = raw.replace("<root>", base).replace("<ROOT>", base)

    raw = raw.replace("\\", os.sep)

    expanded = os.path.expanduser(raw)
    if expanded.startswith("\\\\"):
        return os.path.normpath(expanded)

    drive, _ = os.path.splitdrive(expanded)
    if drive or (len(expanded) >= 2 and expanded[1] == ":"):
        return os.path.normpath(expanded)

    if os.path.isabs(expanded):
        return os.path.normpath(expanded)

    return os.path.normpath(os.path.join(base, expanded))


def resolve_path(base_root: Union[str, Path], raw_path: PathLike) -> str:
    """Zachowana dla kompatybilności nazwa starego helpera."""

    return resolve_root_path(base_root, raw_path)
