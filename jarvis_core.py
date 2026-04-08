# version: 1.0
"""Jarvis core helpers integrujące powiadomienia z GUI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from jarvis_dispatch import dispatch

LoggerType = Optional[Callable[[str], None]]


@dataclass
class JarvisCore:
    """Prosta fasada odpowiedzialna za wysyłkę powiadomień Jarvisa."""

    logger: LoggerType = None
    origin: str = "Jarvis"

    def _log(self, message: str) -> None:
        if callable(self.logger):
            try:
                self.logger(message)
                return
            except Exception:
                pass
        print(message)

    def notify(self, message: str, level: str = "info") -> bool:
        """Wyślij powiadomienie do GUI i zaloguj sukces."""

        ok = dispatch(message, level=level, origin=self.origin)
        if ok:
            self._log("Jarvis → Toast OK")
        return ok


def notify(message: str, level: str = "info", *, origin: str = "Jarvis", logger: LoggerType = None) -> bool:
    """Shortcut do wysyłki powiadomień Jarvisa bez tworzenia instancji."""

    core = JarvisCore(logger=logger, origin=origin)
    return core.notify(message, level=level)


__all__ = ["JarvisCore", "notify"]
