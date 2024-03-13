import pendulum
from omnilife_framework_automations.parameter.repositories import (
    EnviromentVariableParameterRepository,
)
from omnilife_framework_automations.task.entities import Task, TaskPriority, TaskStatus
from omnilife_framework_automations.task.repositories import TaskNotionRepository


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

    parameter_repository = EnviromentVariableParameterRepository()
    task_repository = TaskNotionRepository(parameter_repository)
    task_repository.add_task(task)


add_task()
