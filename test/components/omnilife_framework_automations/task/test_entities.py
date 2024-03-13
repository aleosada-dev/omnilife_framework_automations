import pytest
import pendulum
from omnilife_framework_automations.task.entities import (
    Task,
    TaskStatus,
    TaskPriority,
    map_notion_task_to_entity,
)


@pytest.fixture
def sample_task_page():
    return {
        "parent": {"database_id": "sample_database_id"},
        "id": "sample_id",
        "properties": {
            "Name": {"title": [{"text": {"content": "Sample Task"}}]},
            "Status": {"select": {"name": "In progress"}},
            "Priority": {"select": {"name": "Must Do"}},
            "Planned DateTime": {
                "date": {
                    "start": "2022-12-31T10:00:00.000-03:00",
                    "end": "2022-12-31T11:00:00.000-03:00",
                }
            },
            "Real Start DateTime": {"date": {"start": "2022-12-31T11:00:00.000-03:00"}},
            "Real End DateTime": {"date": {"start": "2022-12-31T12:00:00.000-03:00"}},
            "Deadline": {"date": {"start": "2022-12-31T23:59:59.000-03:00"}},
        },
        "created_time": "2022-01-01T00:00:00Z",
        "last_edited_time": "2022-01-01T00:00:00Z",
    }


def test_map_notion_task_to_entity(sample_task_page):
    task = map_notion_task_to_entity(sample_task_page)
    assert isinstance(task, Task)
    assert task.database_id == "sample_database_id"
    assert task.id == "sample_id"
    assert task.name == "Sample Task"
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.priority == TaskPriority.MUST_DO
    assert task.areas == []
    assert task.projects == []
    assert task.planned_datetime_start == pendulum.datetime(
        2022, 12, 31, 10, 0, tz="America/Sao_Paulo"
    )
    assert task.planned_datetime_end == pendulum.datetime(
        2022, 12, 31, 11, 0, tz="America/Sao_Paulo"
    )
    assert task.real_start_datetime == pendulum.datetime(
        2022, 12, 31, 11, 0, tz="America/Sao_Paulo"
    )
    assert task.real_end_datetime == pendulum.datetime(
        2022, 12, 31, 12, 0, tz="America/Sao_Paulo"
    )
    assert task.deadline == pendulum.datetime(
        2022, 12, 31, 23, 59, 59, tz="America/Sao_Paulo"
    )
    assert task.created_at == pendulum.datetime(2022, 1, 1)
    assert task.last_edit_at == pendulum.datetime(2022, 1, 1)
