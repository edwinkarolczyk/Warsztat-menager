# version: 1.0
from tools.importers import import_tools_from_excel as importer


def test_row_to_tool_assigns_defaults_when_missing_required_fields():
    row = {"Opis": "Opis testowy", "Inne": "wartość"}

    tool = importer._row_to_tool(row, lp=5)

    assert tool["numer"] == "auto_5"
    assert tool["nazwa"] == "bez nazwy"
    assert tool["opis"] == "Opis testowy"
    assert tool["niekompletny"] is True
    assert tool["meta"] == {"inne": "wartość"}


def test_row_to_tool_uses_provided_values_when_available():
    row = {"Numer": "A-123", "Nazwa": "Klucz", "Typ": "klucz"}

    tool = importer._row_to_tool(row, lp=1)

    assert tool["numer"] == "A-123"
    assert tool["nazwa"] == "Klucz"
    assert "niekompletny" not in tool
    assert tool["typ"] == "klucz"


def test_row_to_tool_marks_incomplete_when_name_missing():
    row = {"Numer": "B-77", "Nazwa": None}

    tool = importer._row_to_tool(row, lp=2)

    assert tool["numer"] == "B-77"
    assert tool["nazwa"] == "bez nazwy"
    assert tool["niekompletny"] is True
