# version: 1.0
import types
from pathlib import Path

import gui_narzedzia
from narzedzia_ui import STATE


def test_tasks_from_comboboxes(monkeypatch):
    monkeypatch.setattr(
        gui_narzedzia,
        "LZ",
        types.SimpleNamespace(
            invalidate_cache=lambda: None,
            get_collections=lambda settings=None: [{"id": "C1", "name": "Coll1"}],
            get_default_collection=lambda settings=None: "C1",
            get_tool_types=lambda collection=None: (
                [{"id": "T1", "name": "Typ1"}] if collection == "C1" else []
            ),
            get_statuses=lambda tid, collection=None: (
                [{"id": "S1", "name": "St1"}] if tid == "T1" and collection == "C1" else []
            ),
            get_tasks=lambda tid, sid, collection=None: (
                ["A", "B"]
                if tid == "T1" and sid == "S1" and collection == "C1"
                else []
            ),
            should_autocheck=lambda sid, collection_id: True,
        ),
    )

    class DummyVar:
        def __init__(self, value=""):
            self.value = value

        def get(self):
            return self.value

        def set(self, val):
            self.value = val

    class DummyWidget:
        def __init__(self, *args, **kwargs):
            self.values = kwargs.get("values", [])
            self.textvariable = kwargs.get("textvariable")

        def pack(self, *args, **kwargs):
            pass

        def config(self, **kwargs):
            if "values" in kwargs:
                self.values = kwargs["values"]

        configure = config

        def bind(self, *args, **kwargs):
            pass

        def set(self, val):
            if self.textvariable:
                self.textvariable.set(val)

    class DummyListbox(DummyWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.items = []

        def delete(self, *args, **kwargs):
            self.items = []

        def insert(self, index, item):
            self.items.append(item)

    dummy_tk = types.SimpleNamespace(StringVar=DummyVar, Listbox=DummyListbox, END="end")
    dummy_ttk = types.SimpleNamespace(Combobox=DummyWidget)
    monkeypatch.setattr(gui_narzedzia, "tk", dummy_tk)
    monkeypatch.setattr(gui_narzedzia, "ttk", dummy_ttk)

    parent = DummyWidget()
    widgets = gui_narzedzia.build_task_template(parent)

    widgets["cb_collection"].set("Coll1")
    widgets["on_collection_change"]()
    widgets["cb_type"].set("Typ1")
    widgets["on_type_change"]()
    widgets["cb_status"].set("St1")
    widgets["on_status_change"]()

    assert widgets["listbox"].items == ["[x] A", "[x] B"]
    assert all(t["done"] for t in widgets["tasks_state"])


def test_refresh_tasks_archived_filter(monkeypatch):
    class DummyTree:
        def __init__(self):
            self.rows = []
            self.tags = {}
            self._children = []
            self._style = "Treeview"

        def delete(self, *items):
            self.rows.clear()
            self.tags.clear()
            self._children.clear()

        def insert(self, parent, index, values=(), tags=()):
            iid = f"row{len(self._children)}"
            self._children.append(iid)
            self.rows.append(values)
            self.tags[iid] = tags
            return iid

        def get_children(self):
            return tuple(self._children)

        def selection_set(self, *_):
            pass

        def focus(self, *_):
            pass

        def see(self, *_):
            pass

        def tag_configure(self, *_args, **_kwargs):
            pass

        def cget(self, _name):
            return self._style

        def winfo_toplevel(self):
            return self

        def update_idletasks(self):
            pass

        def bind(self, *_args, **_kwargs):
            pass

    class DummyVar:
        def __init__(self, value=False):
            self.value = value

        def get(self):
            return self.value

        def set(self, value):
            self.value = value

    class DummyStyle:
        def __init__(self, *_args, **_kwargs):
            pass

        def configure(self, *_args, **_kwargs):
            pass

        def map(self, *_args, **_kwargs):
            pass

    pending_task = {
        "tytul": "Naprawić uchwyt",
        "done": False,
        "status": "active",
        "date_added": "2024-05-01T08:00:00",
    }
    archived_task = {
        "tytul": "Wymiana modułu",
        "done": True,
        "status": "done",
        "date_added": "2024-04-01T09:00:00",
        "date_done": "2024-04-03T15:30:00",
        "archived_at": "2024-04-03T15:30:00",
    }
    fake_doc = {
        "nr": "001",
        "zadania": [pending_task, archived_task],
    }

    monkeypatch.setattr(
        gui_narzedzia,
        "iter_tools_json",
        lambda: [(Path("/tmp/001.json"), fake_doc)],
    )
    monkeypatch.setattr(gui_narzedzia, "_ensure_tasks_tooltip", lambda *_: None)
    monkeypatch.setattr(gui_narzedzia, "ensure_theme_applied", lambda *_: None)
    monkeypatch.setattr(gui_narzedzia.ttk, "Style", DummyStyle)

    STATE.tasks_history_var = DummyVar(False)
    STATE.tasks_archived_var = DummyVar(False)
    STATE.tasks_selected_nr = None
    STATE.tasks_selected_path = None
    STATE.tasks_docs_cache.clear()
    STATE.tasks_rows_meta.clear()
    STATE.tasks_tooltips.clear()

    tree = DummyTree()
    gui_narzedzia._refresh_tasks(tree)

    assert [row[1] for row in tree.rows] == ["Naprawić uchwyt"]

    STATE.tasks_archived_var.set(True)
    gui_narzedzia._refresh_tasks(tree)

    assert [row[1] for row in tree.rows] == ["Wymiana modułu"]
    assert any("arch" in tags for tags in tree.tags.values())
