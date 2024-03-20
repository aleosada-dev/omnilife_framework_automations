from typing import Self
from injector import inject
from omnilife_framework_automations.event.entities import Event
from omnilife_framework_automations.infrastructure.repositories import (
    IEventRespository,
    ITaskRepository,
)
from omnilife_framework_automations.infrastructure.services import ITaskService
from omnilife_framework_automations.task.entities import Task, TaskPriority, TaskStatus


def map_event_to_task(event: Event):
    return Task(
        database_id="9044e0c3e3ac49b5bfddf61c9baf1032",
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

    def plan_next_week(self: Self, agenda_id: str):
        events = self.event_repository.get_events(
            agenda_id, "2024-03-17T00:00:00Z", "2024-03-24T00:00:00Z"
        )
        for event in events:
            task = map_event_to_task(event)
            self.task_repository.add_task(task)
