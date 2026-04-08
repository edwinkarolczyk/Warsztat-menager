# version: 1.0
# -*- coding: utf-8 -*-
"""Zakładka "Profile" w ustawieniach aplikacji."""

from __future__ import annotations

import calendar
import datetime as dt
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

import tkinter as tk
from tkinter import messagebox, ttk

from profiles_store import load_profiles_users, resolve_profiles_path, save_profiles_users
from profile_utils import PRIMARY_ADMIN_ROLE

logger = logging.getLogger(__name__)

USERS_PATH: str | None = None


class ProfilesLoadError(RuntimeError):
    """Raised when the profiles file cannot be loaded."""


def _profiles_path() -> Path:
    if USERS_PATH:
        return Path(USERS_PATH)
    return resolve_profiles_path(None)


def _load_users() -> list[dict[str, Any]]:
    """Return the list of users stored on disk."""

    path = _profiles_path()
    logger.debug("[WM-DBG][PROFILES] profiles_path = %s", path)
    try:
        return [dict(item) for item in load_profiles_users(path=path)]
    except FileNotFoundError as exc:
        logger.error("[WM-ERR][PROFILES] profiles file not found: %s", path)
        if USERS_PATH:
            return []
        raise ProfilesLoadError(f"Brak pliku profili: {path}") from exc
    except ValueError as exc:
        logger.error("[WM-ERR][PROFILES] invalid profiles structure: %s", path)
        raise ProfilesLoadError(str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("[WM-ERR][PROFILES] cannot load profiles: %s", exc)
        raise ProfilesLoadError(str(exc)) from exc


def _save_users(items: list[dict[str, Any]]) -> None:
    """Persist users to disk using UTF-8 JSON with two-space indent."""

    path = _profiles_path()
    logger.debug("[WM-DBG][PROFILES] saving profiles to %s", path)
    save_profiles_users(items, path=path)


class SettingsProfilesTab(ttk.Frame):
    """Simple manager for user profiles within the settings window."""

    COLUMNS: tuple[str, ...] = (
        "login",
        "pin",
        "rola",
        "zatrudniony_od",
        "status",
    )

    HEADERS: dict[str, str] = {
        "login": "LOGIN",
        "pin": "PIN",
        "rola": "ROLA",
        "zatrudniony_od": "ZATRUDNIONY_OD",
        "status": "STATUS",
    }

    def __init__(self, master: tk.Misc, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self.users: list[dict[str, Any]] = []
        self.tree = self._build_ui()
        self._load_from_storage()

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------
    def _build_ui(self) -> ttk.Treeview:
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=4)
        ttk.Button(toolbar, text="Dodaj profil", command=self._add_profile).pack(
            side="left"
        )
        ttk.Button(toolbar, text="Edytuj", command=self._edit_selected).pack(
            side="left", padx=6
        )
        ttk.Button(toolbar, text="Zapisz", command=self._save_now).pack(side="right")

        tree = ttk.Treeview(
            self,
            columns=self.COLUMNS,
            show="headings",
            height=12,
            selectmode="browse",
        )
        for column in self.COLUMNS:
            tree.heading(column, text=self.HEADERS[column])
            width = 80 if column == "pin" else 140
            tree.column(column, width=width)
        tree.pack(fill="both", expand=True, pady=(4, 0))
        tree.bind("<Double-1>", lambda _event: self._edit_selected())
        return tree

    def _load_from_storage(self) -> None:
        try:
            self.users = [dict(user) for user in _load_users()]
        except ProfilesLoadError as exc:
            messagebox.showerror("Profile", str(exc))
            self.users = []
        self._refresh_tree()

    def _refresh_tree(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for user in self.users:
            self.tree.insert(
                "",
                "end",
                values=(
                    user.get("login", ""),
                    user.get("pin", ""),
                    user.get("rola", "operator"),
                    user.get("zatrudniony_od", "—"),
                    user.get("status", "aktywny"),
                ),
            )

    def _select_login(self, login: str) -> None:
        for item in self.tree.get_children():
            values = self.tree.item(item).get("values", [])
            if values and values[0] == login:
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    # ------------------------------------------------------------------
    # Data helpers
    # ------------------------------------------------------------------
    def _get_selected_index(self) -> int | None:
        selected = self.tree.selection()
        if not selected:
            return None
        login = self.tree.item(selected[0]).get("values", [""])[0]
        for index, user in enumerate(self.users):
            if user.get("login") == login:
                return index
        return None

    def _login_exists(self, login: str, *, skip_index: int | None = None) -> bool:
        for index, user in enumerate(self.users):
            if skip_index is not None and index == skip_index:
                continue
            if user.get("login") == login:
                return True
        return False

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def _add_profile(self) -> None:
        ProfileEditDialog(self, on_ok=self._on_added)

    def _on_added(self, item: dict[str, Any]) -> bool:
        login = item.get("login", "")
        if self._login_exists(login):
            messagebox.showerror("Profil", "Login już istnieje.")
            return False
        self.users.append(item)
        self._refresh_tree()
        self._select_login(login)
        return True

    def _edit_selected(self) -> None:
        index = self._get_selected_index()
        if index is None:
            messagebox.showinfo("Profil", "Wybierz profil do edycji.")
            return
        ProfileEditDialog(
            self,
            seed=self.users[index],
            on_ok=lambda item: self._on_edited(index, item),
        )

    def _on_edited(self, index: int, item: dict[str, Any]) -> bool:
        login = item.get("login", "")
        if self._login_exists(login, skip_index=index):
            messagebox.showerror("Profil", "Login już istnieje.")
            return False
        self.users[index] = item
        self._refresh_tree()
        self._select_login(login)
        return True

    def _save_now(self) -> None:
        _save_users([dict(user) for user in self.users])
        messagebox.showinfo("Profile", "Zapisano zmiany.")


class ProfileEditDialog(tk.Toplevel):
    """Dialog window for creating or editing a single profile entry."""

    ROLES = [PRIMARY_ADMIN_ROLE, "admin", "operator", "serwisant", "brygadzista"]
    STATUSES = ["aktywny", "zablokowany"]
    SHIFT_MODES = [
        ("111", "Stała 1 zmiana (06–14)"),
        ("222", "Stała 2 zmiana (14–22)"),
        ("121", "Rotacja 1 → 2 → 1"),
        ("212", "Rotacja 2 → 1 → 2"),
    ]

    LEGACY_SHIFT_ALIASES = {
        "1111": "111",
        "2222": "222",
        "1212": "121",
        "2121": "212",
    }

    def __init__(
        self,
        master: tk.Misc,
        seed: dict[str, Any] | None = None,
        on_ok: Callable[[dict[str, Any]], bool | None] | None = None,
    ) -> None:
        super().__init__(master)
        self.title("Profil użytkownika")
        self.resizable(False, False)
        self.on_ok = on_ok

        defaults = {
            "login": "",
            "pin": "",
            "rola": "operator",
            "zatrudniony_od": "",
            "status": "aktywny",
            "disabled_modules": [],
        }
        self.seed: dict[str, Any] = dict(defaults)
        if seed:
            self.seed.update(seed)

        self._build()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build(self) -> None:
        self.geometry("420x300")
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Login:").grid(row=0, column=0, sticky="w")
        self.v_login = tk.StringVar(value=self.seed.get("login", ""))
        ttk.Entry(frame, textvariable=self.v_login).grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="PIN:").grid(row=1, column=0, sticky="w")
        self.v_pin = tk.StringVar(value=self.seed.get("pin", ""))
        ttk.Entry(frame, textvariable=self.v_pin).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Rola:").grid(row=2, column=0, sticky="w")
        self.v_role = tk.StringVar(value=self.seed.get("rola", "operator"))
        ttk.Combobox(
            frame,
            textvariable=self.v_role,
            values=self.ROLES,
            state="readonly",
        ).grid(row=2, column=1, sticky="ew")

        ttk.Label(frame, text="Zatrudniony od (YYYY-MM-DD):").grid(
            row=3, column=0, sticky="w"
        )
        self.v_date = tk.StringVar(value=self.seed.get("zatrudniony_od", ""))

        date_row = ttk.Frame(frame)
        date_row.grid(row=3, column=1, sticky="ew")
        date_row.columnconfigure(0, weight=1)

        self.entry_date = ttk.Entry(date_row, textvariable=self.v_date, state="readonly")
        self.entry_date.grid(row=0, column=0, sticky="ew")
        self.entry_date.bind("<Button-1>", lambda _e: self._open_date_picker())

        ttk.Button(
            date_row,
            text="📅",
            width=3,
            command=self._open_date_picker,
        ).grid(row=0, column=1, padx=(4, 0))

        ttk.Label(frame, text="Status:").grid(row=4, column=0, sticky="w")
        self.v_status = tk.StringVar(value=self.seed.get("status", "aktywny"))
        ttk.Combobox(
            frame,
            textvariable=self.v_status,
            values=self.STATUSES,
            state="readonly",
        ).grid(row=4, column=1, sticky="ew")

        ttk.Label(frame, text="Tryb zmian:").grid(row=5, column=0, sticky="w")
        self.v_shift_mode_label = tk.StringVar()
        cur_mode = (
            self.seed.get("tryb_zmian")
            or self.seed.get("zmiana_plan")
            or ""
        ).strip()
        cur_mode = self.LEGACY_SHIFT_ALIASES.get(cur_mode, cur_mode)
        labels_by_code = {code: label for code, label in self.SHIFT_MODES}
        self.v_shift_mode_label.set(labels_by_code.get(cur_mode, ""))
        ttk.Combobox(
            frame,
            textvariable=self.v_shift_mode_label,
            values=[label for _code, label in self.SHIFT_MODES],
            state="readonly",
        ).grid(row=5, column=1, sticky="ew")

        buttons = ttk.Frame(frame)
        buttons.grid(row=6, column=0, columnspan=2, sticky="e", pady=(8, 0))
        ttk.Button(buttons, text="OK", command=self._ok).pack(side="left", padx=4)
        ttk.Button(buttons, text="Anuluj", command=self.destroy).pack(
            side="left", padx=4
        )

        frame.columnconfigure(1, weight=1)

    def _ok(self) -> None:
        item = dict(self.seed)
        item.update(
            {
                "login": self.v_login.get().strip(),
                "pin": self.v_pin.get().strip(),
                "rola": self.v_role.get().strip() or "operator",
                "zatrudniony_od": self.v_date.get().strip(),
                "status": self.v_status.get().strip() or "aktywny",
            }
        )
        selected_label = self.v_shift_mode_label.get().strip()
        mode_code = ""
        for code, label in self.SHIFT_MODES:
            if label == selected_label:
                mode_code = code
                break
        if mode_code:
            item["tryb_zmian"] = mode_code
            item["zmiana_plan"] = mode_code

        if item["pin"] and not item["pin"].isdigit():
            messagebox.showwarning("Profil", "PIN może zawierać jedynie cyfry.")
            return
        item.setdefault("disabled_modules", [])

        if not item["login"]:
            messagebox.showwarning("Profil", "Login jest wymagany.")
            return

        if self.on_ok and self.on_ok(item) is False:
            return
        self.destroy()

    def _open_date_picker(self) -> None:
        current = str(self.v_date.get() or "").strip()
        try:
            base_date = dt.datetime.strptime(current, "%Y-%m-%d").date()
        except Exception:
            base_date = dt.date.today()

        top = tk.Toplevel(self)
        top.title("Data zatrudnienia")
        top.resizable(False, False)
        try:
            top.transient(self)
            top.grab_set()
            top.lift()
        except Exception:
            pass

        state = {"year": base_date.year, "month": base_date.month}
        month_var = tk.StringVar()
        year_var = tk.StringVar(value=str(base_date.year))

        outer = ttk.Frame(top, padding=8)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 6))

        grid_frame = ttk.Frame(outer)
        grid_frame.pack(fill="both", expand=True)

        footer = ttk.Frame(outer)
        footer.pack(fill="x", pady=(6, 0))

        def _month_title(year: int, month: int) -> str:
            names = [
                "",
                "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
                "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień",
            ]
            return f"{names[month]} {year}"

        def _set_date(day: int) -> None:
            picked = dt.date(state["year"], state["month"], day)
            self.v_date.set(picked.strftime("%Y-%m-%d"))
            top.destroy()

        def _prev_month() -> None:
            if state["month"] == 1:
                state["month"] = 12
                state["year"] -= 1
            else:
                state["month"] -= 1
            _render()

        def _next_month() -> None:
            if state["month"] == 12:
                state["month"] = 1
                state["year"] += 1
            else:
                state["month"] += 1
            _render()

        def _set_today() -> None:
            self.v_date.set(dt.date.today().strftime("%Y-%m-%d"))
            top.destroy()

        def _apply_year(*_args) -> None:
            raw = str(year_var.get() or "").strip()
            if not raw:
                return
            try:
                year = int(raw)
            except Exception:
                year_var.set(str(state["year"]))
                return
            if year < 1900:
                year = 1900
            if year > 2100:
                year = 2100
            state["year"] = year
            year_var.set(str(year))
            _render()

        def _render() -> None:
            for child in grid_frame.winfo_children():
                child.destroy()

            month_var.set(_month_title(state["year"], state["month"]))
            year_var.set(str(state["year"]))

            weekdays = ["Pn", "Wt", "Śr", "Cz", "Pt", "So", "Nd"]
            for col, label in enumerate(weekdays):
                ttk.Label(grid_frame, text=label, width=4, anchor="center").grid(
                    row=0, column=col, padx=1, pady=1
                )

            cal = calendar.Calendar(firstweekday=0)
            weeks = cal.monthdayscalendar(state["year"], state["month"])

            for row_idx, week in enumerate(weeks, start=1):
                for col_idx, day in enumerate(week):
                    if day == 0:
                        ttk.Label(grid_frame, text="", width=4).grid(
                            row=row_idx, column=col_idx, padx=1, pady=1
                        )
                    else:
                        ttk.Button(
                            grid_frame,
                            text=str(day),
                            width=4,
                            command=lambda d=day: _set_date(d),
                        ).grid(row=row_idx, column=col_idx, padx=1, pady=1)

        ttk.Button(header, text="◀", width=3, command=_prev_month).pack(side="left")
        ttk.Label(header, textvariable=month_var, anchor="center").pack(
            side="left", padx=(8, 6)
        )
        ttk.Label(header, text="Rok:").pack(side="left")
        year_entry = ttk.Entry(header, textvariable=year_var, width=6, justify="center")
        year_entry.pack(side="left", padx=(4, 8))
        year_entry.bind("<Return>", _apply_year)
        year_entry.bind("<FocusOut>", _apply_year)
        ttk.Button(header, text="Idź", width=4, command=_apply_year).pack(side="left")
        ttk.Frame(header).pack(side="left", fill="x", expand=True)
        ttk.Button(header, text="▶", width=3, command=_next_month).pack(side="right")

        ttk.Button(footer, text="Dziś", command=_set_today).pack(side="left")
        ttk.Button(footer, text="Anuluj", command=top.destroy).pack(side="right")

        _render()


def make_tab(parent: tk.Misc, _role: str | None = None) -> SettingsProfilesTab:
    """Compatibility helper used by starsze testy/UI."""

    tab = SettingsProfilesTab(parent)
    tab.pack(fill="both", expand=True)
    return tab


__all__ = [
    "SettingsProfilesTab",
    "ProfileEditDialog",
    "_load_users",
    "_save_users",
    "make_tab",
]
