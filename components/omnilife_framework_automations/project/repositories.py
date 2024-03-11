from omnilife_framework_automations.infrastructure.repositories import (
    IProjectRepository,
)
import omnilife_framework_automations.notion.core as notion
from omnilife_framework_automations.notion.helpers import NotionFilterBuilder


class ProjectNotionRepository(IProjectRepository):
    def query_pages(
        self,
        database_id: str,
        api_key: str,
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
        return notion.query_pages(database_id, api_key, filter_query, sort_query)

    def update_notion_page(self, page_id: str, properties: dict, api_key: str):
        notion.update_notion_page(page_id, properties, api_key)
