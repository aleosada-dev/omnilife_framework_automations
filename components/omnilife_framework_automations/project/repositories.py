from typing import Self
from injector import inject
from omnilife_framework_automations.infrastructure.repositories.project import (
    IProjectRepository,
)
from omnilife_framework_automations.infrastructure.repositories.parameter import (
    IParameterRepository,
)
import omnilife_framework_automations.notion.core as notion
from omnilife_framework_automations.notion.helpers import NotionFilterBuilder


class ProjectNotionRepository(IProjectRepository):
    @inject
    def __init__(self: Self, parameter_repository: IParameterRepository) -> None:
        self.api_key = parameter_repository.get("NOTION_APIKEY")

    def query_pages(
        self,
        database_id: str,
        filter_query: str = None,
        sort_query: str = None,
    ):
        filter_builder = NotionFilterBuilder()
        filter_query = (
            filter_builder.checkbox_filter("Urgent", "equals", False)
            .datetime_filter("Deadline", "is_not_empty", True)
            .start_or_group()
            .status_filter("Status", "equals", "In progress")
            .status_filter("Status", "equals", "Not started")
            .end_group()
            .build()
        )
        return notion.query_pages(database_id, self.api_key, filter_query, sort_query)

    def update_notion_page(self, page_id: str, properties: dict):
        notion.update_notion_page(page_id, properties, self.api_key)
