import os
from typing import Self
from injector import Injector, inject
from omnilife_framework_automations.event.modules import EventRepositoryModule
from omnilife_framework_automations.parameter.modules import ParameterRepositoryModule
from omnilife_framework_automations.infrastructure.services import ITaskService
from omnilife_framework_automations.task.modules import TaskRepositoryModule
from omnilife_framework_automations.logger.logger import setup_logger


def setup_injector():
    return Injector(
        [TaskRepositoryModule(), ParameterRepositoryModule(), EventRepositoryModule()]
    )


class Application:
    @inject
    def __init__(self, task_service: ITaskService):
        self.task_service = task_service

    def run(self: Self, task_database_id: str, agenda_id: str):
        self.task_service.plan_next_week(task_database_id, agenda_id)


def lambda_handler(event, context):
    logger = setup_logger(__name__)

    try:
        agenda_id = os.environ.get("GOOGLE_CALENDAR_AGENDA_ID")
        task_database_id = os.environ.get("NOTION_DATABASE_ID")

        injector = setup_injector()
        app = injector.get(Application)
        app.run(task_database_id, agenda_id)
    except Exception as e:
        logger.error(
            f"An error occurred: {e}",
            extra={
                "params": {
                    "agenda_id": agenda_id,
                }
            },
        )
        raise
