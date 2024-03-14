from injector import Injector
from omnilife_framework_automations.event.modules import EventRepositoryModule
from omnilife_framework_automations.infrastructure.repositories import ITaskRepository
from omnilife_framework_automations.parameter.modules import ParameterRepositoryModule
from omnilife_framework_automations.task.modules import TaskRepositoryModule
from omnilife_framework_automations.task.services import TaskService
import pendulum
from omnilife_framework_automations.task.entities import Task, TaskPriority, TaskStatus


def setup_injector():
    return Injector(
        [TaskRepositoryModule(), ParameterRepositoryModule(), EventRepositoryModule()]
    )


def add_task():
    database_id = "9044e0c3e3ac49b5bfddf61c9baf1032"
    task = Task(
        database_id=database_id,
        id=None,
        name="Test Task",
        status=TaskStatus("Not started"),
        priority=TaskPriority("Highlight"),
        areas=["fba92d03bd514101a0fe00bad154b094", "8c6b3d33c7e5415ea97ef4e09416a66c"],
        projects=[],
        planned_datetime_start=pendulum.parse("2022-01-01T00:00:00Z"),
        planned_datetime_end=pendulum.parse("2022-01-01T00:40:00Z"),
        real_start_datetime=None,
        real_end_datetime=None,
        deadline=pendulum.parse("2022-01-01T00:00:00Z"),
        created_at=None,
        last_edit_at=None,
    )

    injector = setup_injector()
    task_repository = injector.get(ITaskRepository)

    task_repository.add_task(task)


def plan_week():
    injector = setup_injector()
    task_service = injector.get(TaskService)
    task_service.plan_next_week(
        "a73e7970246e334a1d8e4d80e7d96e87691eca29804c578dca7424104f685b24@group.calendar.google.com"
    )


# add_task()
plan_week()
