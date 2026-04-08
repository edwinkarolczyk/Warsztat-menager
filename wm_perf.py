import time
from contextlib import contextmanager


def _now():
    return time.perf_counter()


def perf(msg: str):
    print(f"[WM-PERF] {msg}")


@contextmanager
def perf_span(name: str):
    t0 = _now()
    perf(f"{name} START")
    try:
        yield
    finally:
        dt_ms = (_now() - t0) * 1000.0
        perf(f"{name} END  {dt_ms:.2f} ms")


class PerfFlow:
    """
    Pomiar całego przepływu (klik -> gotowa lista / zakończenie inicjalizacji).
    """

    def __init__(self, name: str):
        self.name = name
        self.t0 = _now()
        self.last = self.t0
        perf(f"{self.name} FLOW START")

    def mark(self, label: str):
        t = _now()
        step_ms = (t - self.last) * 1000.0
        total_ms = (t - self.t0) * 1000.0
        perf(f"{self.name} MARK {label}  +{step_ms:.2f} ms  total={total_ms:.2f} ms")
        self.last = t

    def end(self):
        total_ms = (_now() - self.t0) * 1000.0
        perf(f"{self.name} FLOW END total={total_ms:.2f} ms")
