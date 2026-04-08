# version: 1.0
"""Widok hali maszyn z dopasowywaną skalą i przełączaną siatką."""

from __future__ import annotations

import os
from typing import Callable, List, Optional, Tuple

try:  # pragma: no cover - PIL jest opcjonalne w środowisku testowym
    from PIL import Image, ImageTk  # type: ignore
except Exception:  # pragma: no cover - fallback gdy PIL brak
    Image = None  # type: ignore[assignment]
    ImageTk = None  # type: ignore[assignment]

DEFAULT_BG_COLOR = "#1e1e1e"
GRID_COLOR = "#2a2a2a"

SCALE_MODE_FIT = "fit"
SCALE_MODE_100 = "100"


class MachinesView:
    """Lekki widok z kanwą prezentującą maszyny na tle hali.

    Pozwala przełączać widoczność siatki, dopasować widok do rozmiaru
    kontenera lub wrócić do skali 1:1 oraz podłączać akcje stopki.
    """

    def __init__(
        self,
        parent,
        cfg,
        bg_path: Optional[str],
        logout_cb=None,
        quit_cb=None,
        reset_cb: Callable[[], None] | None = None,
    ) -> None:
        import tkinter as tk
        from tkinter import ttk

        self.tk = tk
        self.ttk = ttk
        self.parent = parent
        self.cfg = cfg
        self.logout_cb = logout_cb
        self.quit_cb = quit_cb
        self.reset_cb = reset_cb

        # Stan renderera
        self._grid_visible = True
        self._scale_mode = SCALE_MODE_FIT
        self._scale = 1.0
        self._bg_anchor_xy: Tuple[int, int] = (0, 0)

        # Layout root + kanwa
        self.root = self.ttk.Frame(parent)
        self.root.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self.root,
            bg=DEFAULT_BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Stopka z przyciskami sterującymi
        self._build_footer(self.root)

        # Zasoby tła
        self._bg_img_pil: Optional["Image.Image"] = None
        self._bg_img_tk: Optional["ImageTk.PhotoImage"] = None
        self._bg_w = 0
        self._bg_h = 0

        self._records: List[dict] = []
        self._img_cache: dict[str, object] = {}

        self._load_background(bg_path)

        # Reaguj na zmiany rozmiaru
        self.root.bind("<Configure>", self._on_resize)

        self.redraw()

    # ---------- API publiczne ----------
    def widget(self):
        return self.root

    def set_grid_visible(self, visible: bool) -> None:
        self._grid_visible = bool(visible)
        self.redraw()

    def toggle_grid(self) -> None:
        self.set_grid_visible(not self._grid_visible)

    def set_scale_mode(self, mode: str) -> None:
        self._scale_mode = (
            SCALE_MODE_FIT if mode == SCALE_MODE_FIT else SCALE_MODE_100
        )
        self.redraw()

    def set_records(self, records: List[dict]) -> None:
        self._records = records or []
        self.redraw()

    # ---------- Tło / rozmiar / skala ----------
    def _load_background(self, bg_path: Optional[str]) -> None:
        if not bg_path:
            self._bg_img_pil = None
            self._bg_img_tk = None
            self._bg_w = 0
            self._bg_h = 0
            return

        if not os.path.exists(bg_path):
            self._bg_img_pil = None
            self._bg_img_tk = None
            self._bg_w = 0
            self._bg_h = 0
            return

        if Image is None:
            # Bez PIL nie możemy odczytać wymiarów ani przeskalować grafiki.
            self._bg_img_pil = None
            self._bg_img_tk = None
            self._bg_w = 0
            self._bg_h = 0
            return

        try:
            img = Image.open(bg_path).convert("RGBA")
        except Exception:
            self._bg_img_pil = None
            self._bg_img_tk = None
            self._bg_w = 0
            self._bg_h = 0
            return

        self._bg_img_pil = img
        self._bg_w, self._bg_h = img.width, img.height

    def _compute_fit_scale_and_anchor(
        self, avail_w: int, avail_h: int
    ) -> Tuple[float, Tuple[int, int]]:
        if (
            self._bg_w <= 0
            or self._bg_h <= 0
            or avail_w <= 0
            or avail_h <= 0
        ):
            return 1.0, (0, 0)

        sx = avail_w / self._bg_w
        sy = avail_h / self._bg_h
        scale = min(sx, sy)
        new_w = int(self._bg_w * scale)
        new_h = int(self._bg_h * scale)
        anchor_x = (avail_w - new_w) // 2
        anchor_y = (avail_h - new_h) // 2
        return scale, (anchor_x, anchor_y)

    def _on_resize(self, _event) -> None:
        if self._scale_mode == SCALE_MODE_FIT:
            self.redraw()

    # ---------- Rysowanie ----------
    def redraw(self) -> None:
        canvas = self.canvas
        canvas.delete("all")

        avail_w = max(1, self.root.winfo_width())
        footer_h = max(0, self.footer.winfo_height())
        avail_h = max(1, self.root.winfo_height() - footer_h)

        canvas.config(width=avail_w, height=avail_h)
        canvas.create_rectangle(
            0,
            0,
            avail_w,
            avail_h,
            fill=DEFAULT_BG_COLOR,
            outline="",
        )

        if self._scale_mode == SCALE_MODE_FIT:
            self._scale, self._bg_anchor_xy = self._compute_fit_scale_and_anchor(
                avail_w,
                avail_h,
            )
        else:
            self._scale = 1.0
            anchor_x = max(0, (avail_w - self._bg_w) // 2)
            anchor_y = max(0, (avail_h - self._bg_h) // 2)
            self._bg_anchor_xy = (anchor_x, anchor_y)

        if self._bg_img_pil is not None and ImageTk is not None:
            if self._scale != 1.0:
                width = max(1, int(self._bg_w * self._scale))
                height = max(1, int(self._bg_h * self._scale))
                img = self._bg_img_pil.resize((width, height), Image.NEAREST)
            else:
                img = self._bg_img_pil
            self._bg_img_tk = ImageTk.PhotoImage(img)
            anchor_x, anchor_y = self._bg_anchor_xy
            canvas.create_image(
                anchor_x,
                anchor_y,
                image=self._bg_img_tk,
                anchor="nw",
            )
        else:
            self._bg_img_tk = None

        if self._grid_visible and self._bg_w > 0 and self._bg_h > 0:
            self._draw_grid()

        for record in self._records:
            self._draw_machine_point(record)

        if self._bg_w > 0 and self._bg_h > 0:
            anchor_x, anchor_y = self._bg_anchor_xy
            bottom_x = anchor_x + int(self._bg_w * self._scale)
            bottom_y = anchor_y + int(self._bg_h * self._scale)
            canvas.create_rectangle(
                anchor_x,
                anchor_y,
                bottom_x,
                bottom_y,
                outline="#3a3a3a",
            )

    def _draw_grid(self, step_bg_px: int = 25) -> None:
        canvas = self.canvas
        anchor_x, anchor_y = self._bg_anchor_xy
        scaled_w = int(self._bg_w * self._scale)
        scaled_h = int(self._bg_h * self._scale)
        if scaled_w <= 0 or scaled_h <= 0:
            return

        step = max(1, int(step_bg_px * self._scale))

        x = anchor_x
        while x <= anchor_x + scaled_w:
            canvas.create_line(
                x,
                anchor_y,
                x,
                anchor_y + scaled_h,
                fill=GRID_COLOR,
            )
            x += step

        y = anchor_y
        while y <= anchor_y + scaled_h:
            canvas.create_line(
                anchor_x,
                y,
                anchor_x + scaled_w,
                y,
                fill=GRID_COLOR,
            )
            y += step

    def _map_bg_to_canvas(self, x_bg: int, y_bg: int) -> Tuple[int, int]:
        anchor_x, anchor_y = self._bg_anchor_xy
        x_canvas = anchor_x + int(x_bg * self._scale)
        y_canvas = anchor_y + int(y_bg * self._scale)
        return x_canvas, y_canvas

    def _draw_machine_point(
        self,
        record: dict,
        radius_bg_px: int = 6,
        *,
        fill: str = "#ffb400",
        outline: str = "#6a4900",
    ) -> None:
        try:
            x_bg = int(record.get("x", 0))
            y_bg = int(record.get("y", 0))
        except Exception:
            x_bg = 0
            y_bg = 0

        x_canvas, y_canvas = self._map_bg_to_canvas(x_bg, y_bg)
        radius = max(2, int(radius_bg_px * self._scale))
        self.canvas.create_oval(
            x_canvas - radius,
            y_canvas - radius,
            x_canvas + radius,
            y_canvas + radius,
            fill=fill,
            outline=outline,
            width=1,
        )

    # ---------- Stopka ----------
    def _build_footer(self, parent) -> None:
        footer = self.ttk.Frame(parent)
        footer.grid(row=1, column=0, sticky="ew")
        parent.rowconfigure(1, weight=0)

        def make_button(text: str, command):
            btn = self.ttk.Button(footer, text=text, command=command)
            btn.pack(side="left", padx=6, pady=6)
            return btn

        make_button("Pokaż/Ukryj siatkę", self.toggle_grid)
        make_button("Dopasuj do okna", lambda: self.set_scale_mode(SCALE_MODE_FIT))
        make_button("Skala 100%", lambda: self.set_scale_mode(SCALE_MODE_100))

        self.ttk.Label(footer, text="").pack(
            side="left",
            padx=12,
            expand=True,
            fill="x",
        )

        if self.quit_cb is not None:
            make_button("Zamknij program", self.quit_cb)
        if self.logout_cb is not None:
            make_button("Wyloguj", self.logout_cb)
        if self.reset_cb is not None:
            make_button("Zresetuj licznik", self.reset_cb)

        self.footer = footer


__all__ = ["MachinesView", "SCALE_MODE_FIT", "SCALE_MODE_100"]

