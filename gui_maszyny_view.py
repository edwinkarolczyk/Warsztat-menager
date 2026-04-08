# version: 1.0
"""Widok maszyn z obsługą siatki, skalowania, edycji i pulsowania awarii."""

import os
from typing import Callable, Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageTk  # type: ignore
except Exception:  # pragma: no cover - Pillow jest opcjonalny
    Image = None  # type: ignore[assignment]
    ImageTk = None  # type: ignore[assignment]

from core.settings_manager import Settings

DEFAULT_BG_COLOR = "#1e1e1e"
GRID_COLOR = "#2a2a2a"
SCALE_MODE_FIT = "fit"
SCALE_MODE_100 = "100"


class MachinesView:
    """Widok odpowiedzialny za prezentację maszyn na planie zakładu."""

    def __init__(
        self,
        parent,
        cfg: Settings,
        bg_path: Optional[str],
        logout_cb: Optional[Callable] = None,
        quit_cb: Optional[Callable] = None,
        reset_cb: Optional[Callable] = None,
        on_select: Optional[Callable[[str], None]] = None,
        on_move: Optional[Callable[[str, Dict[str, int]], None]] = None,
    ) -> None:
        import tkinter as tk
        from tkinter import ttk

        self.tk, self.ttk = tk, ttk
        self.parent, self.cfg = parent, cfg
        self.logout_cb, self.quit_cb = logout_cb, quit_cb
        self.reset_cb = reset_cb
        self.on_select_cb = on_select
        self.on_move_cb = on_move

        self._grid_visible = bool(cfg.get("gui.maszyny.show_grid", True))
        self._scale_mode = str(cfg.get("gui.maszyny.scale_mode", SCALE_MODE_FIT))
        self._scale = 1.0
        self._bg_anchor_xy = (0, 0)

        self.root = ttk.Frame(parent)
        self.root.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.root, bg=DEFAULT_BG_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self._build_footer(self.root)

        self._bg_img_pil = None
        self._bg_img_tk = None
        self._bg_w = 0
        self._bg_h = 0
        self._records: List[Dict[str, object]] = []

        self._edit_mode = False
        self._selected_mid: Optional[str] = None
        self._drag_last: Optional[Tuple[int, int]] = None
        self._id_to_screen_xy: Dict[str, Tuple[int, int]] = {}

        self._blink_on = False
        self._blink_job = None

        self._load_background(bg_path)

        self.canvas.bind("<Configure>", lambda _event: self.redraw())
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_drop)

        self.redraw()
        self._schedule_blink()

    def widget(self):
        return self.root

    def set_records(self, records: List[Dict[str, object]]) -> None:
        self._records = records or []
        if self._selected_mid and not any(
            str(record.get("id", "")) == self._selected_mid for record in self._records
        ):
            self._selected_mid = None
        self.redraw()

    def set_grid_visible(self, visible: bool) -> None:
        self._grid_visible = bool(visible)
        self.cfg.set("gui.maszyny.show_grid", self._grid_visible)
        self.cfg.save()
        self.redraw()

    def toggle_grid(self) -> None:
        self.set_grid_visible(not self._grid_visible)

    def set_scale_mode(self, mode: str) -> None:
        self._scale_mode = SCALE_MODE_FIT if mode == SCALE_MODE_FIT else SCALE_MODE_100
        self.cfg.set("gui.maszyny.scale_mode", self._scale_mode)
        self.cfg.save()
        self.redraw()

    def _load_background(self, bg_path: Optional[str]) -> None:
        if Image is None:
            self._bg_img_pil = None
            self._bg_w = 0
            self._bg_h = 0
            return

        if not bg_path or not os.path.exists(bg_path):
            self._bg_img_pil = None
            self._bg_w = 0
            self._bg_h = 0
            return
        try:
            image = Image.open(bg_path).convert("RGBA")
            self._bg_img_pil = image
            self._bg_w, self._bg_h = image.width, image.height
        except Exception:
            self._bg_img_pil = None
            self._bg_w = 0
            self._bg_h = 0

    def _compute_fit(self, width: int, height: int) -> Tuple[float, Tuple[int, int]]:
        if self._bg_w <= 0 or self._bg_h <= 0 or width <= 0 or height <= 0:
            return 1.0, (0, 0)
        scale = min(width / self._bg_w, height / self._bg_h)
        anchor_x = (width - int(self._bg_w * scale)) // 2
        anchor_y = (height - int(self._bg_h * scale)) // 2
        return scale, (anchor_x, anchor_y)

    def redraw(self) -> None:
        canvas = self.canvas
        canvas.delete("all")
        avail_w = max(1, self.root.winfo_width())
        avail_h = max(1, self.root.winfo_height() - self.footer.winfo_height())
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
            self._scale, self._bg_anchor_xy = self._compute_fit(avail_w, avail_h)
        else:
            anchor_x = max(0, (avail_w - self._bg_w) // 2)
            anchor_y = max(0, (avail_h - self._bg_h) // 2)
            self._scale = 1.0
            self._bg_anchor_xy = (anchor_x, anchor_y)

        if self._bg_img_pil is not None and ImageTk is not None:
            width = max(1, int(self._bg_w * self._scale))
            height = max(1, int(self._bg_h * self._scale))
            image = (
                self._bg_img_pil
                if self._scale == 1.0
                else self._bg_img_pil.resize((width, height), Image.NEAREST)
            )
            self._bg_img_tk = ImageTk.PhotoImage(image)
            anchor_x, anchor_y = self._bg_anchor_xy
            canvas.create_image(anchor_x, anchor_y, image=self._bg_img_tk, anchor="nw")
        elif self._bg_img_pil is not None:
            # Pillow bez ImageTk – rezygnujemy z tła zamiast zgłaszać wyjątek
            self._bg_img_tk = None

        if self._grid_visible and self._bg_w > 0 and self._bg_h > 0:
            self._draw_grid()

        self._id_to_screen_xy.clear()
        for record in self._records:
            self._draw_machine_point(record)

        if self._bg_w > 0 and self._bg_h > 0:
            anchor_x, anchor_y = self._bg_anchor_xy
            canvas.create_rectangle(
                anchor_x,
                anchor_y,
                anchor_x + int(self._bg_w * self._scale),
                anchor_y + int(self._bg_h * self._scale),
                outline="#3a3a3a",
            )

    def _draw_grid(self, step_bg_px: int = 25) -> None:
        canvas = self.canvas
        anchor_x, anchor_y = self._bg_anchor_xy
        bg_width = int(self._bg_w * self._scale)
        bg_height = int(self._bg_h * self._scale)
        if bg_width <= 0 or bg_height <= 0:
            return
        step = max(1, int(step_bg_px * self._scale))
        position_x = anchor_x
        while position_x <= anchor_x + bg_width:
            canvas.create_line(
                position_x,
                anchor_y,
                position_x,
                anchor_y + bg_height,
                fill=GRID_COLOR,
            )
            position_x += step
        position_y = anchor_y
        while position_y <= anchor_y + bg_height:
            canvas.create_line(
                anchor_x,
                position_y,
                anchor_x + bg_width,
                position_y,
                fill=GRID_COLOR,
            )
            position_y += step

    def _map_bg_to_canvas(self, x_bg: int, y_bg: int) -> Tuple[int, int]:
        anchor_x, anchor_y = self._bg_anchor_xy
        return anchor_x + int(x_bg * self._scale), anchor_y + int(y_bg * self._scale)

    def _map_canvas_to_bg(self, x: int, y: int) -> Tuple[int, int]:
        anchor_x, anchor_y = self._bg_anchor_xy
        return int((x - anchor_x) / self._scale), int((y - anchor_y) / self._scale)

    def _draw_machine_point(
        self, record: Dict[str, object], radius_bg_px: int = 6
    ) -> None:
        canvas = self.canvas
        machine_id = str(record.get("id", ""))
        try:
            x_bg = int(record.get("x", 0))
            y_bg = int(record.get("y", 0))
        except Exception:
            x_bg = 0
            y_bg = 0

        status = str(record.get("status", "")).lower()

        x_coord, y_coord = self._map_bg_to_canvas(x_bg, y_bg)
        radius = max(2, int(radius_bg_px * self._scale))

        fill = "#ffb400"
        if status == "awaria":
            fill = "#ef4444"
        outline = "#6a4900"

        canvas.create_oval(
            x_coord - radius,
            y_coord - radius,
            x_coord + radius,
            y_coord + radius,
            fill=fill,
            outline=outline,
            width=1,
            tags=(f"m-{machine_id}", "machine"),
        )

        if self._selected_mid == machine_id:
            canvas.create_oval(
                x_coord - radius - 3,
                y_coord - radius - 3,
                x_coord + radius + 3,
                y_coord + radius + 3,
                outline="#22d3ee",
                width=2,
                dash=(3, 2),
            )

        self._id_to_screen_xy[machine_id] = (x_coord, y_coord)

        if status == "awaria" and self._blink_on:
            canvas.create_oval(
                x_coord - radius - 6,
                y_coord - radius - 6,
                x_coord + radius + 6,
                y_coord + radius + 6,
                outline="#ef4444",
                width=2,
                dash=(2, 2),
            )

    def _machine_at(self, x: int, y: int) -> Optional[str]:
        best_id: Optional[str] = None
        best_distance = 12 * 12
        for machine_id, (mx, my) in self._id_to_screen_xy.items():
            distance = (mx - x) * (mx - x) + (my - y) * (my - y)
            if distance <= best_distance:
                best_id = machine_id
                best_distance = distance
        return best_id

    def _on_click(self, event) -> None:
        machine_id = self._machine_at(event.x, event.y)
        self._selected_mid = machine_id
        if machine_id and callable(self.on_select_cb):
            self.on_select_cb(machine_id)
        if self._edit_mode and machine_id:
            self._drag_last = (event.x, event.y)
        self.redraw()

    def _on_drag(self, event) -> None:
        if not self._edit_mode or not self._selected_mid or self._drag_last is None:
            return
        dx = event.x - self._drag_last[0]
        dy = event.y - self._drag_last[1]
        start_x, start_y = self._id_to_screen_xy.get(
            self._selected_mid, (event.x, event.y)
        )
        next_x, next_y = start_x + dx, start_y + dy
        bg_x, bg_y = self._map_canvas_to_bg(next_x, next_y)
        for record in self._records:
            if str(record.get("id", "")) == self._selected_mid:
                record["x"] = int(bg_x)
                record["y"] = int(bg_y)
                break
        self._drag_last = (event.x, event.y)
        self.redraw()

    def _on_drop(self, _event) -> None:
        if not self._edit_mode or not self._selected_mid:
            return
        for record in self._records:
            if str(record.get("id", "")) == self._selected_mid:
                if callable(self.on_move_cb):
                    payload = {"x": int(record["x"]), "y": int(record["y"])}
                    self.on_move_cb(self._selected_mid, payload)
                break
        self._drag_last = None

    def _schedule_blink(self) -> None:
        if self._blink_job:
            self.root.after_cancel(self._blink_job)

        def tick() -> None:
            self._blink_on = not self._blink_on
            self.redraw()
            self._blink_job = self.root.after(400, tick)

        self._blink_job = self.root.after(400, tick)

    def _build_footer(self, parent) -> None:
        from tkinter import ttk

        frame = ttk.Frame(parent)
        frame.grid(row=1, column=0, sticky="ew")
        parent.rowconfigure(1, weight=0)

        self.show_grid_var = self.tk.BooleanVar(value=self._grid_visible)
        ttk.Checkbutton(
            frame,
            text="Siatka",
            variable=self.show_grid_var,
            command=lambda: self.set_grid_visible(self.show_grid_var.get()),
        ).pack(side="left", padx=10, pady=6)

        self.edit_var = self.tk.BooleanVar(value=self._edit_mode)

        def _toggle_edit() -> None:
            self._edit_mode = bool(self.edit_var.get())
            self._drag_last = None
            self.redraw()

        ttk.Checkbutton(
            frame,
            text="Edycja",
            variable=self.edit_var,
            command=_toggle_edit,
        ).pack(side="left", padx=6, pady=6)

        ttk.Button(
            frame,
            text="Dopasuj do okna",
            command=lambda: self.set_scale_mode("fit"),
        ).pack(side="left", padx=6, pady=6)
        ttk.Button(
            frame,
            text="Skala 100%",
            command=lambda: self.set_scale_mode("100"),
        ).pack(side="left", padx=6, pady=6)

        ttk.Label(frame, text="").pack(side="left", expand=True, fill="x")
        if self.quit_cb:
            ttk.Button(
                frame,
                text="Zamknij program",
                command=self.quit_cb,
            ).pack(side="right", padx=6, pady=6)
        if self.logout_cb:
            ttk.Button(
                frame,
                text="Wyloguj",
                command=self.logout_cb,
            ).pack(side="right", padx=6, pady=6)
        if getattr(self, "reset_cb", None):
            ttk.Button(
                frame,
                text="Zresetuj licznik",
                command=self.reset_cb,
            ).pack(side="right", padx=6, pady=6)
        self.footer = frame
