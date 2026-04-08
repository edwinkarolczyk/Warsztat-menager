# version: 1.0
"""Simple hover tooltips with image carousel preview."""

from __future__ import annotations

import itertools
from typing import Iterable, List

try:  # Pillow is optional
    from PIL import Image, ImageTk  # type: ignore
    _PIL_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    Image = ImageTk = None  # type: ignore
    _PIL_AVAILABLE = False

import tkinter as tk


class ImageHoverTooltip:
    """Display a small image preview while hovering over a widget.

    When multiple image paths are provided, images rotate in a simple
    carousel at a fixed interval.  Pillow is used for loading images when
    available; otherwise a placeholder image is shown.
    """

    def __init__(
        self,
        widget: tk.Misc,
        image_paths: Iterable[str] | None,
        delay: int = 500,
        max_size: tuple[int, int] = (600, 800),
        *,
        bind_events: bool = True,
    ) -> None:
        self.widget = widget
        self.image_paths: List[str] = list(image_paths or [])
        self.delay = delay
        self.max_size = max_size
        self._images: List[tk.PhotoImage] = []
        self._image_cycle = itertools.cycle([])  # reset later
        self._index = 0
        self._after_id: int | None = None
        self._tooltip: tk.Toplevel | None = None
        self._label: tk.Label | None = None
        self._visible = False

        if bind_events:
            try:
                widget.bind("<Enter>", self.show_tooltip, add="+")
                widget.bind("<Leave>", self.hide_tooltip, add="+")
            except TypeError:  # fallback for simplified widgets (tests)
                widget.bind("<Enter>", self.show_tooltip)
                widget.bind("<Leave>", self.hide_tooltip)

        try:
            widget.bind("<Destroy>", self._on_widget_destroy, add="+")
        except TypeError:
            widget.bind("<Destroy>", self._on_widget_destroy)

    # ------------------------------------------------------------------
    # Image helpers
    def _placeholder_image(self) -> tk.PhotoImage:
        img = tk.PhotoImage(width=100, height=100)
        try:
            img.put("grey", to=(0, 0, 99, 99))
        except Exception:
            pass
        return img

    def _load_image(self, path: str) -> tk.PhotoImage:
        if _PIL_AVAILABLE and Image is not None:
            try:  # pragma: no cover - Pillow branch
                img = Image.open(path)
                img.thumbnail(self.max_size)
                return ImageTk.PhotoImage(img)
            except Exception:
                return self._placeholder_image()
        return self._placeholder_image()

    def _ensure_images(self) -> None:
        if not self._images:
            if self.image_paths:
                for p in self.image_paths:
                    self._images.append(self._load_image(p))
            else:  # always have at least one image
                self._images.append(self._placeholder_image())
            self._image_cycle = itertools.cycle(self._images)

    def update_image_paths(self, image_paths: Iterable[str] | None) -> None:
        """Replace the list of images and reset the internal cache."""

        self.image_paths = list(image_paths or [])
        self._images.clear()
        self._image_cycle = itertools.cycle([])

    # ------------------------------------------------------------------
    # Tooltip handling
    def _create_window(self) -> None:
        self._tooltip = tk.Toplevel(self.widget)
        self._tooltip.wm_overrideredirect(True)
        self._label = tk.Label(self._tooltip)
        self._label.pack()
        try:
            self._tooltip.withdraw()
        except Exception:
            pass

    def _cancel_animation(self) -> None:
        if self._after_id is not None:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def show_tooltip(self, _event: object | None = None) -> None:
        self._ensure_images()
        if self._tooltip is None or not getattr(self._tooltip, "winfo_exists", lambda: True)():
            self._create_window()
        assert self._tooltip is not None
        assert self._label is not None
        x = self.widget.winfo_rootx() + self.widget.winfo_width()
        y = self.widget.winfo_rooty()
        try:
            pointer_x = self.widget.winfo_pointerx()
            pointer_y = self.widget.winfo_pointery()
            x = pointer_x + 16
            y = pointer_y + 16
        except Exception:
            pass
        self._tooltip.geometry(f"+{x}+{y}")
        self._cancel_animation()
        self._image_cycle = itertools.cycle(self._images)
        self._visible = True
        self._tooltip.deiconify()
        try:
            self._tooltip.lift()
        except Exception:
            pass
        self._show_next_image()

    def _show_next_image(self) -> None:
        if not self._visible or self._label is None:
            self._cancel_animation()
            return

        try:
            img = next(self._image_cycle)
        except Exception:
            self._cancel_animation()
            return

        self._label.configure(image=img)
        self._label.image = img  # prevent GC

        if len(self._images) > 1 and self._visible:
            self._after_id = self.widget.after(self.delay, self._show_next_image)
        else:
            self._after_id = None

    def hide_tooltip(self, _event: object | None = None) -> None:
        self._visible = False
        self._cancel_animation()
        if self._tooltip is not None:
            try:
                self._tooltip.withdraw()
            except Exception:
                try:
                    self._tooltip.destroy()
                except Exception:
                    pass
                self._tooltip = None
                self._label = None
        if self._label is not None:
            try:
                self._label.configure(image="")
            except Exception:
                pass
            self._label.image = None  # type: ignore[attr-defined]
        self._image_cycle = itertools.cycle(self._images)

    def _on_widget_destroy(self, _event: object | None = None) -> None:
        self._visible = False
        self._cancel_animation()
        if self._tooltip is not None:
            try:
                self._tooltip.destroy()
            except Exception:
                pass
        self._tooltip = None
        self._label = None


# ----------------------------------------------------------------------
# Helper bindings

def bind_canvas_item_hover(
    canvas: tk.Canvas,
    item_id: int,
    image_paths,
    delay: int = 500,
    max_size: tuple[int, int] = (600, 800),
) -> ImageHoverTooltip:
    tooltip = ImageHoverTooltip(
        canvas, image_paths, delay=delay, max_size=max_size
    )
    try:
        canvas.tag_bind(item_id, "<Enter>", tooltip.show_tooltip, add="+")
        canvas.tag_bind(item_id, "<Leave>", tooltip.hide_tooltip, add="+")
    except TypeError:
        canvas.tag_bind(item_id, "<Enter>", tooltip.show_tooltip)
        canvas.tag_bind(item_id, "<Leave>", tooltip.hide_tooltip)
    return tooltip


def bind_treeview_row_hover(
    tree: tk.Treeview,
    row_id: str,
    image_paths,
    delay: int = 500,
    max_size: tuple[int, int] = (600, 800),
) -> ImageHoverTooltip:
    tooltip = ImageHoverTooltip(
        tree, image_paths, delay=delay, max_size=max_size
    )
    def _on_motion(event: tk.Event) -> None:
        if tree.identify_row(event.y) == row_id:
            tooltip.show_tooltip()
        else:
            tooltip.hide_tooltip()

    def _on_leave(_event: tk.Event | None = None) -> None:
        tooltip.hide_tooltip()

    try:
        tree.bind("<Motion>", _on_motion, add="+")
        tree.bind("<Leave>", _on_leave, add="+")
    except TypeError:
        tree.bind("<Motion>", _on_motion)
        tree.bind("<Leave>", _on_leave)
    return tooltip
