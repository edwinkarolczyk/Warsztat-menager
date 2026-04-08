# version: 1.0
import pytest

from utils_json import normalize_doc_list_or_dict


@pytest.mark.parametrize(
    "payload,expected",
    [
        ([{"id": 1}, {"id": 2}, "x", 3], [{"id": 1}, {"id": 2}]),
        ({"items": [{"id": "a"}, None, 5]}, [{"id": "a"}]),
        ({"items": "not-a-list"}, []),
    ],
)
def test_normalize_doc_list_or_dict_filters_dicts(payload, expected):
    assert normalize_doc_list_or_dict(payload, "items") == expected


def test_normalize_doc_list_or_dict_uses_fallback_keys():
    payload = {"machines": [{"id": "M1"}, "bad"], "items": [{"id": "ignored"}]}

    result = normalize_doc_list_or_dict(
        payload,
        "maszyny",
        fallback_keys=("machines",),
    )

    assert result == [{"id": "M1"}]


def test_normalize_doc_list_or_dict_missing_section_returns_empty():
    assert normalize_doc_list_or_dict({}, "items") == []
