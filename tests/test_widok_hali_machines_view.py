# version: 1.0
"""Testy jednostkowe logiki pomocniczej widoku hali maszyn."""

from __future__ import annotations

from widok_hali.machines_view import MachinesView


class DummyCanvas:
    """Minimalny obiekt imitujący canvas Tk do testów bez GUI."""

    def __init__(self) -> None:
        self.lines: list[tuple[int, int, int, int, dict]] = []
        self.ovals: list[tuple[int, int, int, int, dict]] = []

    def create_line(self, x1: int, y1: int, x2: int, y2: int, **kwargs):
        self.lines.append((x1, y1, x2, y2, kwargs))
        return len(self.lines)

    def create_oval(self, x1: int, y1: int, x2: int, y2: int, **kwargs):
        self.ovals.append((x1, y1, x2, y2, kwargs))
        return len(self.ovals)


def _make_view_stub() -> MachinesView:
    view = MachinesView.__new__(MachinesView)  # type: ignore[call-arg]
    view.canvas = DummyCanvas()
    view._bg_anchor_xy = (0, 0)
    view._scale = 1.0
    view._bg_w = 0
    view._bg_h = 0
    return view


def test_compute_fit_scale_and_anchor_centering() -> None:
    view = _make_view_stub()
    view._bg_w = 100
    view._bg_h = 50

    scale, anchor = view._compute_fit_scale_and_anchor(300, 200)

    assert scale == 3.0
    assert anchor == (0, 25)


def test_map_bg_to_canvas_applies_anchor_and_scale() -> None:
    view = _make_view_stub()
    view._bg_anchor_xy = (5, 10)
    view._scale = 1.5

    assert view._map_bg_to_canvas(4, 6) == (11, 19)


def test_draw_grid_respects_scaled_dimensions() -> None:
    view = _make_view_stub()
    view._bg_anchor_xy = (2, 3)
    view._bg_w = 100
    view._bg_h = 80
    view._scale = 0.5

    view._draw_grid()

    canvas: DummyCanvas = view.canvas  # type: ignore[assignment]
    vertical = [line for line in canvas.lines if line[0] == line[2]]
    horizontal = [line for line in canvas.lines if line[1] == line[3]]

    assert [line[0] for line in vertical] == [2, 14, 26, 38, 50]
    assert [line[1] for line in horizontal] == [3, 15, 27, 39]


def test_draw_machine_point_scales_radius() -> None:
    view = _make_view_stub()
    view._bg_anchor_xy = (10, 20)
    view._scale = 2.0

    view._draw_machine_point({"x": 5, "y": 7})

    canvas: DummyCanvas = view.canvas  # type: ignore[assignment]
    assert canvas.ovals == [
        (8, 22, 32, 46, {"fill": "#ffb400", "outline": "#6a4900", "width": 1})
    ]
