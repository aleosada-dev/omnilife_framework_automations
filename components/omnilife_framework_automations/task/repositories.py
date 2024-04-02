from typing import Self
from injector import inject
from omnilife_framework_automations.infrastructure.repositories.task import (
    ITaskRepository,
)
from omnilife_framework_automations.infrastructure.repositories.parameter import (
    IParameterRepository,
)
from omnilife_framework_automations.notion.core import (
    add_database_page,
)
from omnilife_framework_automations.task.entities import Task


class TaskNotionRepository(ITaskRepository):
    @inject
    def __init__(self: Self, parameter_repository: IParameterRepository) -> None:
        self.api_key = parameter_repository.get("NOTION_APIKEY")

    def add_task(self: Self, task: Task):
        props = task.map_to_notion_properties()
        add_database_page(task.database_id, props, self.api_key)
