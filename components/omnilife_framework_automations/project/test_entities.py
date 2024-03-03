import pytest
import pendulum
from omnilife_framework_automations.project.entities import (
    Project,
    ProjectStatus,
    ProjectSize,
    ProjectValue,
    safe_check_notion_date,
    project_page_to_class,
    become_urgent,
)


@pytest.fixture
def sample_project_page():
    return {
        "parent": {"database_id": "sample_database_id"},
        "id": "sample_id",
        "properties": {
            "Name": {"title": [{"text": {"content": "Sample Project"}}]},
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
    }


def test_safe_check_notion_date_with_valid_date(sample_project_page):
    date = safe_check_notion_date(sample_project_page, "Deadline")
    assert isinstance(date, pendulum.DateTime)
    assert date.year == 2022
    assert date.month == 12
    assert date.day == 31


def test_safe_check_notion_date_with_invalid_date(sample_project_page):
    date = safe_check_notion_date(sample_project_page, "End Date")
    assert date is None


def test_project_page_to_class(sample_project_page):
    project = project_page_to_class(sample_project_page)
    assert isinstance(project, Project)
    assert project.database_id == "sample_database_id"
    assert project.id == "sample_id"
    assert project.name == "Sample Project"
    assert project.status == ProjectStatus.IN_PROGRESS
    assert project.areas == []
    assert project.project_size == ProjectSize.MEDIUM
    assert project.value == ProjectValue.MEDIUM
    assert project.days_before_urgent == 5
    assert project.deadline == pendulum.datetime(2022, 12, 31)
    assert not project.urgent
    assert project.goals == []
    assert project.start_date == pendulum.datetime(
        2024, 2, 25, 11, 42, tz="America/Sao_Paulo"
    )
    assert project.end_date is None
    assert project.created_at == pendulum.datetime(2022, 1, 1)
    assert project.last_edit_at == pendulum.datetime(2022, 1, 1)


def test_become_urgent_with_past_deadline():
    project = Project(
        database_id="sample_database_id",
        id="sample_id",
        name="Sample Project",
        status=ProjectStatus.IN_PROGRESS,
        areas=[],
        project_size=ProjectSize.MEDIUM,
        value=ProjectValue.MEDIUM,
        days_before_urgent=5,
        deadline=pendulum.datetime(2022, 12, 31),
        urgent=False,
        goals=[],
        start_date=pendulum.datetime(2022, 1, 1),
        end_date=None,
        created_at=pendulum.datetime(2022, 1, 1),
        last_edit_at=pendulum.datetime(2022, 1, 1),
    )

    # Set the current time
    now = pendulum.datetime(2022, 12, 26)

    # Call the function
    updated_project = become_urgent(project, now)

    # Assert that the project is marked as urgent
    assert updated_project.urgent is True


def test_become_urgent_with_future_deadline():
    project = Project(
        database_id="sample_database_id",
        id="sample_id",
        name="Sample Project",
        status=ProjectStatus.IN_PROGRESS,
        areas=[],
        project_size=ProjectSize.MEDIUM,
        value=ProjectValue.MEDIUM,
        days_before_urgent=5,
        deadline=pendulum.datetime(2022, 12, 31),
        urgent=False,
        goals=[],
        start_date=pendulum.datetime(2022, 1, 1),
        end_date=None,
        created_at=pendulum.datetime(2022, 1, 1),
        last_edit_at=pendulum.datetime(2022, 1, 1),
    )

    # Set the current time
    now = pendulum.datetime(2022, 12, 25)

    # Call the function
    updated_project = become_urgent(project, now)

    # Assert that the project is marked as urgent
    assert updated_project.urgent is False
