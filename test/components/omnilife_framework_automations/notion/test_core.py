import pytest
import pendulum
import requests_mock
from omnilife_framework_automations.notion.core import (
    query_pages,
    update_notion_page,
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
def test_query_pages_empty_or_none_values(database_id, api_key, expected_error_msg):
    # test if a ValueRaise is raised for a expecifc parameter
    with pytest.raises(ValueError) as exec_info:
        query_pages(database_id, api_key)

    # Check if database_id or api_key is empty or None
    assert expected_error_msg in str(exec_info.value)


def test_query_pages(sample_page):
    database_id = "sample_database_id"
    api_key = "sample_api_key"

    with requests_mock.Mocker() as mocker:
        mocker.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            status_code=200,
            json={"results": [sample_page]},
        )

        pages = query_pages(database_id, api_key)

        assert mocker.called
        assert mocker.call_count == 1
        assert mocker.last_request.method == "POST"
        assert (
            mocker.last_request.url
            == f"https://api.notion.com/v1/databases/{database_id}/query"
        )
        assert mocker.last_request.headers["Authorization"] == f"Bearer {api_key}"
        assert mocker.last_request.headers["Content-Type"] == "application/json"
        assert mocker.last_request.headers["Notion-Version"] == "2022-06-28"
        assert mocker.last_request.json() == {}

        assert len(pages) == 1
        assert pages[0] == sample_page


def test_update_notion_page_with_valid_inputs():
    page_id = "sample_page_id"
    properties = {"Title": "New Title", "Description": "New Description"}
    api_key = "sample_api_key"

    with requests_mock.Mocker() as mocker:
        mocker.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            status_code=200,
            json={},
        )

        update_notion_page(page_id, properties, api_key)

        assert mocker.called
        assert mocker.call_count == 1
        assert mocker.last_request.method == "PATCH"
        assert mocker.last_request.url == f"https://api.notion.com/v1/pages/{page_id}"
        assert mocker.last_request.headers["Authorization"] == f"Bearer {api_key}"
        assert mocker.last_request.headers["Content-Type"] == "application/json"
        assert mocker.last_request.headers["Notion-Version"] == "2022-06-28"
        assert mocker.last_request.json() == {"properties": properties}


def test_update_notion_page_with_empty_page_id():
    page_id = ""
    properties = {"Title": "New Title", "Description": "New Description"}
    api_key = "sample_api_key"

    with pytest.raises(ValueError) as exec_info:
        update_notion_page(page_id, properties, api_key)

    assert str(exec_info.value) == "Page ID is empty or None"


def test_update_notion_page_with_empty_api_key():
    page_id = "sample_page_id"
    properties = {"Title": "New Title", "Description": "New Description"}
    api_key = ""

    with pytest.raises(ValueError) as exec_info:
        update_notion_page(page_id, properties, api_key)

    assert str(exec_info.value) == "API key is empty or None"


def test_update_notion_page_with_failed_request():
    page_id = "sample_page_id"
    api_key = "sample_api_key"
    properties = {"Title": "New Title", "Description": "New Description"}

    with requests_mock.Mocker() as mocker:
        mocker.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            status_code=400,
            json={},
        )

        with pytest.raises(ValueError) as exec_info:
            update_notion_page(page_id, properties, api_key)

        assert str(exec_info.value) == "Failed to update Notion page"
