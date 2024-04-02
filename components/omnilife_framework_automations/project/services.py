from typing import Self
from injector import inject
from omnilife_framework_automations.infrastructure.repositories.project import (
    IProjectRepository,
)
from omnilife_framework_automations.infrastructure.services import IProjectService
import pendulum
from omnilife_framework_automations.project.entities import (
    become_urgent,
    project_page_to_class,
)


class ProjectService(IProjectService):
    @inject
    def __init__(self: Self, project_repository: IProjectRepository) -> None:
        self.project_repository = project_repository

    def urgent_project_automation(self: Self, database_id: str, now: pendulum.DateTime):
        pages = self.project_repository.query_pages(
            database_id=database_id,
        )

        for page in pages:
            project = project_page_to_class(page)
            if project.deadline:
                project = become_urgent(project, now)

                if project.urgent is True:
                    self.project_repository.update_notion_page(
                        project.id,
                        properties={"Urgent": {"checkbox": True}},
                    )
