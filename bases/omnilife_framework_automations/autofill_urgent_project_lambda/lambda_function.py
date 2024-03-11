import os
from typing import Self
from injector import Injector, inject
from omnilife_framework_automations.project.modules import ProjectServiceModule
from omnilife_framework_automations.infrastructure.services import IProjectService
from omnilife_framework_automations.project.repositories import ProjectNotionRepository
import pendulum
from omnilife_framework_automations.logger.logger import setup_logger


def setup_injector():
    return Injector([ProjectServiceModule(), ProjectNotionRepository()])

class Application:
    @inject
    def __init__(self, project_service: IProjectService):
        self.project_service = project_service
    
    def run(self: Self, database_id: str, api_key: str, now: pendulum.DateTime):
        self.project_service.urgent_project_automation(database_id, api_key, now)


def lambda_handler(event, context):
    logger = setup_logger(__name__)

    try:
        database_id = os.environ.get("NOTION_DATABASE_ID")
        api_key = os.environ.get("NOTION_API_KEY")

        injector = setup_injector() 
        app = injector.get(Application)
        app.run(database_id, api_key, pendulum.now())
    except Exception as e:
        logger.error(
            f"An error occurred: {e}",
            extra={
                "params": {
                    "database_id": database_id,
                }
            },
        )
        raise
