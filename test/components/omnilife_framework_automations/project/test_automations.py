import pendulum
from unittest.mock import patch
from omnilife_framework_automations.project.automations import urgent_project_automation


@patch("omnilife_framework_automations.project.automations.query_pages")
@patch("omnilife_framework_automations.project.automations.update_notion_page")
def test_urgent_project_automation(mock_update_notion_page, mock_query_pages):
    # Mock the query_pages function to return a list of sample project pages
    mock_query_pages.return_value = [
        {
            "parent": {"database_id": "sample_database_id"},
            "id": "sample_id_1",
            "properties": {
                "Name": {"title": [{"text": {"content": "Sample Project 1"}}]},
                "Status": {"status": {"name": "In progress"}},
                "Size": {"select": {"name": "M"}},
                "Value": {"select": {"name": "Medium"}},
                "Days Before Urgent": {"number": 4},
                "Deadline": {"date": {"start": "2022-12-31"}},
                "Urgent": {"checkbox": False},
                "Start Date": {"date": {"start": "2024-02-25T11:42:00.000-03:00"}},
                "End Date": {"date": None},
            },
            "created_time": "2022-01-01T00:00:00Z",
            "last_edited_time": "2022-01-01T00:00:00Z",
        },
        {
            "parent": {"database_id": "sample_database_id"},
            "id": "sample_id_2",
            "properties": {
                "Name": {"title": [{"text": {"content": "Sample Project 2"}}]},
                "Status": {"status": {"name": "In progress"}},
                "Size": {"select": {"name": "M"}},
                "Value": {"select": {"name": "Medium"}},
                "Days Before Urgent": {"number": 5},
                "Deadline": {"date": {"start": "2022-12-31"}},
                "Urgent": {"checkbox": False},
                "Start Date": {"date": {"start": "2024-02-25T11:42:00.000-03:00"}},
                "End Date": {"date": None},
            },
            "created_time": "2022-01-01T00:00:00Z",
            "last_edited_time": "2022-01-01T00:00:00Z",
        },
    ]
    now = pendulum.datetime(2022, 12, 26)

    # Call the function
    urgent_project_automation("sample_database_id", "sample_api_key", now)

    # Assert that the update_notion_page function is called with the correct arguments
    mock_update_notion_page.assert_called_with(
        "sample_id_2",
        properties={"Urgent": {"checkbox": True}},
        api_key="sample_api_key",
    )
