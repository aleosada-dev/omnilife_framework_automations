import pytest
from omnilife_framework_automations.notion.core import query_pages

def test_query_pages():
    # Arrange
    database_id = "72facfe731bd4c79a85c1ea132d59410"
    api_key = "secret_Gdu1D1v96dtAgIoiCKpFnGRCWjNYwuV9AJBJKnGzkc1"

    # Call the function
    pages = query_pages(database_id, api_key)

    # Assert the expected output
    assert isinstance(pages, list)
    assert all(isinstance(page, dict) for page in pages)


@pytest.mark.parametrize("database_id, api_key, expected_error_msg", [
    (None, None, "Database ID is empty or None"),
    ("", "", "Database ID is empty or None"),
    (None, "", "Database ID is empty or None"),
    ("", None, "Database ID is empty or None"),
    ("", "api_key", "Database ID is empty or None"), 
    (None, "api_key", "Database ID is empty or None"), 
    ("database_id", "", "API key is empty or None"), 
    ("database_id", None, "API key is empty or None"), 
])
def test_empty_or_none_values(database_id, api_key, expected_error_msg):
    # test if a ValueRaise is raised for a expecifc parameter
    with pytest.raises(ValueError) as exec_info:
        query_pages(database_id, api_key)
     
    # Check if database_id or api_key is empty or None
    assert expected_error_msg in str(exec_info.value)
