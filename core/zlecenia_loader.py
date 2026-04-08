# version: 1.0
from __future__ import annotations

from typing import Any, Callable, Dict, Optional
import importlib
import inspect


def _import_optional(mod_name: str, func_name: str) -> Optional[Callable]:
    try:
        mod = importlib.import_module(mod_name)
        fn = getattr(mod, func_name, None)
        return fn if callable(fn) else None
    except Exception as e:  # pragma: no cover - diagnostyka importu
        print(f"[ZLC] Import fail: {mod_name}.{func_name} → {e}")
        return None


def load_creator_from_settings(settings) -> Optional[Callable]:
    """Wczytaj kreator wg config.json → orders.wizard_import / orders.wizard_func."""

    mod = (settings.get("orders.wizard_import") or "gui_zlecenia").strip()
    fn = (settings.get("orders.wizard_func") or "open_order_creator").strip()
    return _import_optional(mod, fn)


def try_load_direct_creator() -> Optional[Callable]:
    """Priorytet: prawdziwy kreator z GUI, klasyczny podpis (master, autor=...)."""

    direct_candidates = [
        ("gui_zlecenia_creator", "open_order_creator"),
        ("gui_zlecenia", "open_order_creator"),
    ]
    for mod_name, func_name in direct_candidates:
        fn = _import_optional(mod_name, func_name)
        if fn:
            return fn
    return None


def resolve_master(widget_or_none) -> Any:
    try:
        if widget_or_none and hasattr(widget_or_none, "winfo_toplevel"):
            return widget_or_none.winfo_toplevel()
    except Exception:
        pass
    return None


def safe_open_creator(
    open_creator: Callable,
    *,
    master,
    order_type: Optional[str],
    prefill: Dict[str, Any],
    user_role: str,
):
    """
    Obsługuje warianty:
      - open_creator(master, autor=...)            # klasyk
      - open_creator(master, **kwargs)             # hybryda
      - open_creator(**kwargs)                     # VAR_KEYWORD
      - open_creator(order_type=None, prefill=..., user_role=...)
      - open_creator(prefill)                      # legacy (tylko gdy nie ma master)
    Klucz: NIGDY nie przekazuj dict pozycyjnie, gdy 1. parametr to 'master'.
    """

    try:
        sig = inspect.signature(open_creator)
    except Exception:
        # Brak introspekcji — spróbuj najpierw master + autor, potem kwargs.
        try:
            return open_creator(master, autor=user_role or "brygadzista")
        except TypeError:
            return open_creator(
                order_type=order_type,
                prefill=prefill,
                user_role=user_role,
            )

    params = list(sig.parameters.values())
    names = [p.name for p in params]
    has_varkw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params)

    wants_master = (
        len(params) >= 1
        and params[0].kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        and params[0].name in ("master", "parent", "root")
    )

    if wants_master and ("autor" in names or has_varkw):
        return open_creator(master, autor=user_role or "brygadzista")

    kwargs = {"order_type": order_type, "prefill": prefill, "user_role": user_role}
    if has_varkw:
        if "master" in names and master is not None:
            kwargs["master"] = master
        return open_creator(**kwargs)

    filtered_kwargs = {k: v for k, v in kwargs.items() if k in names}
    if "master" in names and master is not None:
        filtered_kwargs["master"] = master
    if filtered_kwargs:
        return open_creator(**filtered_kwargs)

    if len(params) == 1 and params[0].name not in ("master", "parent", "root"):
        return open_creator(prefill)

    return open_creator(**{k: v for k, v in kwargs.items() if k in names})

