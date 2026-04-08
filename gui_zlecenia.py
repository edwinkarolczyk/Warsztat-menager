# version: 1.0
"""Panel Dyspozycji – lista oparta o wspólny store Dyspozycji."""

from __future__ import annotations

import logging
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Callable

from config_manager import resolve_rel
from dyspozycje_store import load_dyspozycje

try:
    from config_manager import get_config  # type: ignore
except ImportError:  # pragma: no cover - fallback dla starszych wersji
    def get_config():
        try:
            from config_manager import ConfigManager  # type: ignore

            return ConfigManager().load()
        except Exception:
            return {}

try:
    from core.logika_zlecen import create_order  # type: ignore
except Exception as _orders_import_error:  # pragma: no cover - optional feature
    create_order = None  # type: ignore
    print("[ORDERS][ERROR] Brak create_order:", _orders_import_error)

from ui_dialogs_safe import error_box
from utils_orders import ensure_orders_sample_if_empty, load_orders_rows_with_fallback


def _emit_orders_updated(widget: tk.Misc) -> None:
    try:
        root = widget.winfo_toplevel()
        root.event_generate("<<OrdersUpdated>>", when="tail")
    except Exception:
        pass


def on_save_order(
    master: tk.Misc, order_type: str, form_values: dict[str, Any]
) -> None:
    if not callable(create_order):
        messagebox.showerror(
            "Dyspozycje",
            "Brak funkcji zapisu dyspozycji (create_order).",
            parent=master,
        )
        return

    try:
        ok, result = create_order(order_type, form_values)
    except Exception as exc:  # pragma: no cover - zabezpieczenie GUI
        messagebox.showerror(
            "Dyspozycje",
            f"Nie udało się zapisać dyspozycji:\n{exc}",
            parent=master,
        )
        return

    if ok:
        number = "(?)"
        if isinstance(result, dict):
            number = str(result.get("nr") or result.get("id") or "(?)")
        messagebox.showinfo(
            "Dyspozycje",
            f"Dyspozycja zapisana: {number}",
            parent=master,
        )
        _emit_orders_updated(master)
        try:
            master.destroy()
        except Exception:
            pass
    else:
        messagebox.showerror(
            "Dyspozycje",
            f"Nie zapisano dyspozycji:\n{result}",
            parent=master,
        )


logger = logging.getLogger(__name__)


def _resolve_creator() -> Callable[..., tk.Toplevel] | None:
    try:
        from gui_dyspozycje_creator import open_dyspozycje_creator  # type: ignore

        return open_dyspozycje_creator
    except Exception:
        return None


def _open_orders_panel():
    """
    Otwiera panel 'Dyspozycje' ZAWSZE.
    Gdy plik pusty/niepoprawny – pokazuje pustą listę i informację,
    bez crashy i bez file-dialogów.
    """

    try:
        from start import CONFIG_MANAGER  # type: ignore

        cfg = CONFIG_MANAGER.load() if hasattr(CONFIG_MANAGER, "load") else {}
    except Exception:
        cfg = {}

    if not cfg:
        try:
            cfg = get_config()
        except Exception:
            logger.exception("[Zlecenia] Nie udało się uzyskać konfiguracji przez get_config().")
            cfg = {}

    rows, primary_path = load_orders_rows_with_fallback(cfg, resolve_rel)
    had_rows = bool(rows)
    rows = ensure_orders_sample_if_empty(rows, primary_path)

    win = tk.Toplevel()
    win.title("Dyspozycje")
    win.geometry("960x560")

    info = tk.StringVar()
    if had_rows:
        info.set(f"Załadowano {len(rows)} pozycji.")
    else:
        info.set(
            "Brak Dyspozycji w konfiguracji – dodano przykładowe wpisy do zlecenia/zlecenia.json."
        )
    ttk.Label(win, textvariable=info).pack(fill="x", padx=8, pady=8)

    tv = ttk.Treeview(
        win,
        columns=("id", "klient", "status", "data"),
        show="headings",
        height=20,
    )
    for column_id, width in (
        ("id", 160),
        ("klient", 360),
        ("status", 160),
        ("data", 200),
    ):
        tv.heading(column_id, text=column_id.upper())
        tv.column(column_id, width=width, anchor="w")
    for row in rows:
        tv.insert(
            "",
            "end",
            values=(
                row.get("id", ""),
                row.get("klient", ""),
                row.get("status", ""),
                row.get("data", ""),
            ),
        )
    tv.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    ttk.Button(win, text="Zamknij", command=win.destroy).pack(side="right", padx=8, pady=8)
    logger.info("[Dyspozycje] Panel otwarty; rekordów: %d; plik=%s", len(rows), primary_path)
    return win


def _load_orders_rows() -> list[dict]:
    try:
        rows = load_dyspozycje()
    except Exception:
        rows = []
    return [row for row in rows if isinstance(row, dict)]


class _AfterGuard:
    """Helper zabezpieczający wywołania `after` przed zniszczeniem widgetu."""

    def __init__(self, widget: tk.Misc) -> None:
        self._widget = widget
        self._tokens: list[str] = []

    def call_later(self, ms: int, callback: Callable[[], None]) -> str | None:
        try:
            token = self._widget.after(ms, callback)
        except Exception:  # pragma: no cover - brak w testach GUI
            logger.exception("[ORD] after() failed")
            return None
        self._tokens.append(token)
        return token

    def cancel_all(self) -> None:
        for token in self._tokens:
            try:
                self._widget.after_cancel(token)
            except Exception:  # pragma: no cover - brak w testach GUI
                continue
        self._tokens.clear()


class ZleceniaView(ttk.Frame):
    """Widok listy Dyspozycji z automatycznym odświeżaniem."""

    _REFRESH_INTERVAL_MS = 5000

    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master, padding=8)
        self._after = _AfterGuard(self)
        self._refresh_error_shown = False
        self._order_rows: dict[str, dict] = {}
        self._order_ids: dict[str, str] = {}
        self._open_order_creator = _resolve_creator()
        self._build_toolbar()
        self._build_tree()
        self._bind_orders_event()
        self.bind("<Destroy>", self._on_destroy, add=True)
        self._refresh()
        self._schedule_refresh()

    # region UI helpers -------------------------------------------------
    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=(0, 6))

        btn_add = ttk.Button(toolbar, text="Dodaj Dyspozycję")
        if self._open_order_creator:
            btn_add.configure(command=self._on_add)
        else:
            btn_add.state(["disabled"])
        btn_add.pack(side="left")

    def _build_tree(self) -> None:
        columns = ("typ", "status", "tytul", "przypisane", "termin")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            self.tree.heading(column, text=column.capitalize())
            self.tree.column(column, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._on_double_click, add=True)

    # endregion ---------------------------------------------------------

    def _bind_orders_event(self) -> None:
        try:
            root = self.winfo_toplevel()
        except Exception:
            root = None
        if not root:
            return
        # nowy event dla Dyspozycji
        root.bind("<<DyspozycjeUpdated>>", lambda _event: self._reload_orders(), add=True)

    def _fill_orders_table(self, rows: list[dict]) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._order_rows = {}
        self._order_ids = {}
        for idx, order in enumerate(rows):
            if not isinstance(order, dict):
                continue
            rodzaj = str(order.get("typ_dyspozycji") or "")
            if rodzaj == "zlecenie_wykonania":
                rodzaj = "zlecenie wykonania"
            status_txt = str(order.get("status") or "")
            tytul = str(order.get("tytul") or "")
            przypisane = (
                "wszyscy"
                if order.get("dla_wszystkich") is True
                else str(order.get("przypisane_do") or "")
            )
            termin = str(order.get("termin") or "")
            order_id = (
                order.get("id")
                or order.get("nr")
                or order.get("kod")
                or order.get("numer")
            )
            order_key = str(order_id) if order_id is not None else ""
            iid = order_key if order_key else f"row-{idx}"
            try:
                self.tree.insert(
                    "",
                    "end",
                    values=(rodzaj, status_txt, tytul, przypisane, termin),
                    iid=iid,
                )
            except Exception as exc:  # pragma: no cover - wymagane GUI
                logger.exception("[DYSP] Błąd dodawania Dyspozycji do listy: %s", exc)
                continue
            self._order_rows[iid] = order
            if order_key:
                self._order_ids[iid] = order_key

    def _reload_orders(self) -> None:
        try:
            rows = load_dyspozycje()
        except Exception as exc:  # pragma: no cover - wymagane GUI
            logger.exception("[DYSP] Błąd wczytywania listy Dyspozycji: %s", exc)
            rows = []
        cleaned = [row for row in rows if isinstance(row, dict)]
        self._fill_orders_table(cleaned)

    # region Actions ----------------------------------------------------
    def _on_add(self) -> None:
        if not self._open_order_creator:
            return
        try:
            self._open_order_creator(
                self,
                autor="uzytkownik",
                context={"modul_zrodlowy": "dyspozycje"},
            )
        except Exception as exc:  # pragma: no cover - wymagane GUI
            logger.exception("[DYSP] Błąd otwierania kreatora: %s", exc)
            error_box(
                self,
                "Dyspozycje",
                f"Nie udało się otworzyć kreatora Dyspozycji.\n{exc}",
            )

    def _on_double_click(self, event: Any) -> None:
        del event
        selection = self.tree.selection()
        if not selection:
            return
        iid = selection[0]
        mapped = self._order_rows.get(iid, {})
        if not mapped:
            return
        body = (
            f"ID: {mapped.get('id', '')}\n"
            f"Typ: {mapped.get('typ_dyspozycji', '')}\n"
            f"Status: {mapped.get('status', '')}\n"
            f"Tytuł: {mapped.get('tytul', '')}\n"
            f"Opis: {mapped.get('opis', '')}\n"
            f"Priorytet: {mapped.get('priorytet', '')}\n"
            f"Termin: {mapped.get('termin', '')}\n"
            f"Przypisane do: {'wszyscy' if mapped.get('dla_wszystkich') else mapped.get('przypisane_do', '')}\n"
            f"Moduł źródłowy: {mapped.get('modul_zrodlowy', '')}\n"
            f"Obiekt ID: {mapped.get('obiekt_id', '')}\n"
            f"Autor: {mapped.get('autor', '')}"
        )
        messagebox.showinfo("Szczegóły Dyspozycji", body, parent=self)

    # endregion ---------------------------------------------------------

    # region Refresh ----------------------------------------------------
    def _refresh(self) -> None:
        try:
            rows = _load_orders_rows()
        except Exception as exc:  # pragma: no cover - wymagane GUI
            logger.exception("[DYSP] Błąd odświeżania listy Dyspozycji: %s", exc)
            if not self._refresh_error_shown:
                error_box(
                    self,
                    "Dyspozycje",
                    f"Nie udało się odświeżyć listy Dyspozycji.\n{exc}",
                )
            self._refresh_error_shown = True
            return

        self._refresh_error_shown = False
        self._fill_orders_table(rows)

    def _schedule_refresh(self) -> None:
        if not self.winfo_exists():  # pragma: no cover - brak w testach GUI
            return
        self._after.call_later(self._REFRESH_INTERVAL_MS, self._on_refresh_timer)

    def _on_refresh_timer(self) -> None:
        if not self.winfo_exists():  # pragma: no cover - brak w testach GUI
            self._after.cancel_all()
            return
        self._refresh()
        self._schedule_refresh()

    # endregion ---------------------------------------------------------

    def _on_destroy(self, _event: Any) -> None:
        self._after.cancel_all()


def panel_zlecenia(parent: tk.Widget) -> ttk.Frame:
    view = ZleceniaView(parent)
    view.pack(fill="both", expand=True)
    return view
