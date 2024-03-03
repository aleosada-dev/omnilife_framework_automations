import pytest
import pendulum
from omnilife_framework_automations.notion.core import (
    query_pages,
    safe_check_notion_date,
)


@pytest.fixture
def sample_page():
    return {
        "parent": {"database_id": "sample_database_id"},
        "id": "sample_id",
        "properties": {
            "Start Date": {"date": {"start": "2024-02-25T11:42:00.000-03:00"}},
            "End Date": {"date": None},
        },
        "created_time": "2022-01-01T00:00:00Z",
        "last_edited_time": "2022-01-01T00:00:00Z",
    }


def test_safe_check_notion_date_with_valid_datetime(sample_page):
    date = safe_check_notion_date(sample_page, "Start Date")
    assert isinstance(date, pendulum.DateTime)
    assert date.year == 2024
    assert date.month == 2
    assert date.day == 25
    assert date.hour == 11
    assert date.minute == 42
    assert date.timezone_name == "-03:00"


def test_safe_check_notion_date_with_invalid_date(sample_page):
    date = safe_check_notion_date(sample_page, "End Date")
    assert date is None


@pytest.mark.parametrize(
    "database_id, api_key, expected_error_msg",
    [
        (None, None, "Database ID is empty or None"),
        ("", "", "Database ID is empty or None"),
        (None, "", "Database ID is empty or None"),
        ("", None, "Database ID is empty or None"),
        ("", "api_key", "Database ID is empty or None"),
        (None, "api_key", "Database ID is empty or None"),
        ("database_id", "", "API key is empty or None"),
        ("database_id", None, "API key is empty or None"),
    ],
)
def test_empty_or_none_values(database_id, api_key, expected_error_msg):
    # test if a ValueRaise is raised for a expecifc parameter
    with pytest.raises(ValueError) as exec_info:
        query_pages(database_id, api_key)

    # Check if database_id or api_key is empty or None
    assert expected_error_msg in str(exec_info.value)
