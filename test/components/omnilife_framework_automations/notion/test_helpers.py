from omnilife_framework_automations.notion.helpers import (
    NotionFilterBuilder,
    NotionSortBuilder,
)


def test_start_or_group():
    builder = NotionFilterBuilder()
    builder.start_or_group()
    assert builder.current_group == builder.filter_group["and"][0]["or"]


def test_start_and_group():
    builder = NotionFilterBuilder()
    builder.start_and_group()
    assert builder.current_group == builder.filter_group["and"][0]["and"]


def test_end_group():
    builder = NotionFilterBuilder()
    builder.start_or_group()
    builder.end_group()
    assert builder.current_group == builder.filter_group["and"]


def test_text_filter():
    builder = NotionFilterBuilder()
    builder.text_filter("name", "equals", "John")
    assert builder.current_group[0] == {"property": "name", "text": {"equals": "John"}}


def test_richtext_filter():
    builder = NotionFilterBuilder()
    builder.richtext_filter("name", "equals", "John")
    assert builder.current_group[0] == {
        "property": "name",
        "rich_text": {"equals": "John"},
    }


def test_checkbox_filter():
    builder = NotionFilterBuilder()
    builder.checkbox_filter("urgent", "equals", True)
    assert builder.current_group[0] == {
        "property": "urgent",
        "checkbox": {"equals": True},
    }


def test_number_filter():
    builder = NotionFilterBuilder()
    builder.number_filter("age", "greater_than", 18)
    assert builder.current_group[0] == {
        "property": "age",
        "number": {"greater_than": 18},
    }


def test_datetime_filter():
    builder = NotionFilterBuilder()
    builder.datetime_filter("created_at", "before", "2022-01-01")
    assert builder.current_group[0] == {
        "property": "created_at",
        "date": {"before": "2022-01-01"},
    }


def test_select_filter():
    builder = NotionFilterBuilder()
    builder.select_filter("Status", "equals", "In Progress")
    assert builder.current_group[0] == {
        "property": "Status",
        "select": {"equals": "In Progress"},
    }


def test_status_filter():
    builder = NotionFilterBuilder()
    builder.status_filter("Status", "equals", "In Progress")
    assert builder.current_group[0] == {
        "property": "Status",
        "status": {"equals": "In Progress"},
    }


def test_filter_build():
    builder = NotionFilterBuilder()
    filter_obj = builder.text_filter("name", "equals", "John").build()
    assert filter_obj == {"filter": builder.filter_group}


def test_add_sort():
    builder = NotionSortBuilder()
    builder.add_sort("name", "ascending")
    assert builder.sorts == {"sorts": [{"property": "name", "direction": "ascending"}]}


def test_add_sort_invalid_direction():
    builder = NotionSortBuilder()
    try:
        builder.add_sort("name", "invalid_direction")
    except ValueError as e:
        assert str(e) == "Direction must be either 'ascending' or 'descending'"


def test_sort_build():
    builder = NotionSortBuilder()
    builder.add_sort("name", "ascending")
    builder.add_sort("age", "descending")
    sort_instructions = builder.build()
    assert sort_instructions == {
        "sorts": [
            {"property": "name", "direction": "ascending"},
            {"property": "age", "direction": "descending"},
        ]
    }
