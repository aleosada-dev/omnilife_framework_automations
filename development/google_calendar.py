from pprint import pprint
from omnilife_framework_automations.event.entities import Event
from omnilife_framework_automations.task.repositories import TaskNotionRepository
from omnilife_framework_automations.google.repositories import (
    GoogleCalendarEventRepository,
)
from dotenv import load_dotenv
from omnilife_framework_automations.parameter.repositories import (
    EnviromentVariableParameterRepository,
)
from omnilife_framework_automations.task.entities import Task, TaskPriority, TaskStatus
import pendulum


load_dotenv()


def map_event_to_task(task_database_id: str, event: Event):
    return Task(
        database_id=task_database_id,
        id=None,
        name=event.name,
        status=TaskStatus("Not started"),
        priority=TaskPriority(event.priority),
        areas=[area for area in event.areas],
        projects=[project for project in event.projects],
        planned_datetime_start=event.start_date,
        planned_datetime_end=event.end_date,
        real_start_datetime=None,
        real_end_datetime=None,
        deadline=None,
        created_at=None,
        last_edit_at=None,
    )


def plan_next_week(task_database_id: str, agenda_id: str):
    today = pendulum.now().start_of("day")
    start_min = today.to_iso8601_string()
    start_max = today.add(days=7).to_iso8601_string()


    parameter_repository = EnviromentVariableParameterRepository()
    task_repository = TaskNotionRepository(parameter_repository)
    event_repository = GoogleCalendarEventRepository(parameter_repository)
    events = event_repository.get_events(agenda_id, start_min, start_max)

    for event in events:
        task = map_event_to_task(task_database_id, event)
        pprint(task)
        task_repository.add_task(task)


def test_get_events():
    today = pendulum.now().start_of("day")
    calendar_id = "5677e409133bbe8a6a12ccc0db9741a4d7589a0a1a3477778da3760feb2c4c56@group.calendar.google.com"
    start_min = today.to_iso8601_string()
    start_max = today.add(days=7).to_iso8601_string()

    parameter_repository = EnviromentVariableParameterRepository()
    event_repository = GoogleCalendarEventRepository(parameter_repository)
    events = event_repository.get_events(calendar_id, start_min, start_max)

    for event in events:
        pprint(event)


# test_get_events()
plan_next_week(
        "9044e0c3e3ac49b5bfddf61c9baf1032",
        "5677e409133bbe8a6a12ccc0db9741a4d7589a0a1a3477778da3760feb2c4c56@group.calendar.google.com"
)
