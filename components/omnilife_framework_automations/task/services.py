import pendulum
from typing import Self
from injector import inject
from omnilife_framework_automations.event.entities import Event
from omnilife_framework_automations.infrastructure.repositories import (
    IEventRespository,
    ITaskRepository,
)
from omnilife_framework_automations.infrastructure.services import ITaskService
from omnilife_framework_automations.task.entities import Task, TaskPriority, TaskStatus


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


class TaskService(ITaskService):
    @inject
    def __init__(
        self: Self,
        event_repository: IEventRespository,
        task_repository: ITaskRepository,
    ):
        self.task_repository = task_repository
        self.event_repository = event_repository

    def plan_next_week(self: Self, task_database_id: str, agenda_id: str):
        today = pendulum.now().start_of("day")
        start_min = today.to_iso8601_string()
        start_max = today.add(days=7).to_iso8601_string()

        events = self.event_repository.get_events(
            agenda_id, start_min, start_max 
        )
        for event in events:
            task = map_event_to_task(task_database_id, event)
            self.task_repository.add_task(task)
