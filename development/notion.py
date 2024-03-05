import json
import pendulum
import os
from dotenv import load_dotenv
from omnilife_framework_automations.notion.helpers import (
    NotionFilterBuilder,
    NotionSortBuilder,
)
from omnilife_framework_automations.notion.core import (
    query_pages,
    safe_check_notion_select,
)
from omnilife_framework_automations.project.entities import project_page_to_class
from omnilife_framework_automations.project.automations import urgent_project_automation
from pprint import pprint


load_dotenv()


def test_query_pages():
    # Arrange
    database_id = os.getenv("NOTION_PROJECTS_DATABASE_ID")
    api_key = os.getenv("NOTION_API_KEY")
    filter_builder = NotionFilterBuilder()
    filter_query = filter_builder.richtext_filter(
        "Name", "contains", "Estabelecer"
    ).build()
    sort_builder = NotionSortBuilder()
    sort_builder.add_sort("Name", "ascending")
    sort_query = sort_builder.build()

    # Call the function
    pages = query_pages(database_id, api_key, filter_query, sort_query)

    projects = []
    for page in pages:
        projects.append(project_page_to_class(page))

    pprint(projects)


def test_urgent_project_automation():
    # Arrange
    database_id = os.getenv("NOTION_PROJECTS_DATABASE_ID")
    api_key = os.getenv("NOTION_API_KEY")

    # Call the function
    urgent_project_automation(database_id, api_key, pendulum.now())


def test_safe_check_notion_select_with_missing_property():
    sample_page = {}
    sample_page["properties"] = {}
    result = safe_check_notion_select(sample_page, "Missing Property")
    assert result is None


def test_notion_filter_builder():
    # Create a filter builder instance
    filter_builder = NotionFilterBuilder()

    filter_query = (
        filter_builder.checkbox_filter("Urgent", "equals", False)
        .datetime_filter("Deadline", "is_not_empty", True)
        .start_or_group()
        .status_filter("Status", "equals", "In progress")
        .status_filter("Status", "equals", "Not started")
        .end_group()
        .build()
    )

    # Build a complex filter with "or" condition and select specific columns
    # filter_query = filter_builder \
    #     .start_or_group() \
    #         .text_filter("Name", "contains", "Example") \
    #         .number_filter("Age", "greater_than", 20) \
    #     .end_group() \
    #     .datetime_filter("Birthday", "before", "2023-01-01T00:00:00Z") \
    #     .select_columns("Name", "Age", "Birthday") \
    #     .build()

    # filter_query = (
    #     filter_builder.richtext_filter("Name", "contains", "SYNC")
    #     .checkbox_filter("Urgent", "equals", True)
    #     .build()
    # )

    pprint(json.dumps(filter_query))


def test_notion_sort_builder():
    sort_builder = NotionSortBuilder()
    sort_builder.add_sort("Name", "ascending")
    sort_query = sort_builder.build()

    pprint(json.dumps(sort_query))


# test_query_pages()
# test_urgent_project_automation()
# test_safe_check_notion_select_with_missing_property()
test_notion_filter_builder()
# test_notion_sort_builder()
