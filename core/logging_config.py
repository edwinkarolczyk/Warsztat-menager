# version: 1.0
from __future__ import annotations

import logging
import os
from typing import Any

_LOGGING_INITIALIZED = False
_LOG_PATH: str | None = None


def _norm(path: str) -> str:
    return os.path.normcase(os.path.abspath(os.path.normpath(path)))


def _cfg_lookup(cfg: Any | None, dotted: str) -> Any | None:
    if cfg is None:
        return None
    getter = getattr(cfg, "get", None)
    if callable(getter):
        try:
            return getter(dotted)
        except Exception:
            pass
    if isinstance(cfg, dict):
        node: Any = cfg
        for part in dotted.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return None
        return node
    return None


def init_logging(cfg: Any | None = None) -> str:
    global _LOGGING_INITIALIZED, _LOG_PATH

    if _LOGGING_INITIALIZED and _LOG_PATH:
        return _LOG_PATH

    logs_dir = _cfg_lookup(cfg, "paths.logs_dir")
    if not logs_dir:
        root = _cfg_lookup(cfg, "paths.data_root")
        if root is None and hasattr(cfg, "path_root"):
            try:
                root = cfg.path_root()
            except Exception:
                root = None
        if not root:
            root = os.path.join(os.getcwd(), "data", "..")
        logs_dir = os.path.join(str(root), "logs")

    logs_dir = _norm(str(logs_dir))
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, "wm.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    _LOGGING_INITIALIZED = True
    _LOG_PATH = log_path
    print(f"[WM-DBG][LOGCFG] Logging initialized → {log_path}")
    return log_path


def setup_logging(log_dir: str | None = None, filename: str = "wm.log") -> None:
    cfg = None
    if log_dir:
        cfg = {"paths": {"logs_dir": log_dir}}
    path = init_logging(cfg)
    if filename != "wm.log" and path:
        logging.getLogger(__name__).warning(
            "[LOGCFG] Ignoring custom filename; using %s", path
        )
