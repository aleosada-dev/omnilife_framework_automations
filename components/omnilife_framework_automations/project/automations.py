import pendulum
from omnilife_framework_automations.notion.core import query_pages, update_notion_page
from omnilife_framework_automations.project.entities import (
    become_urgent,
    project_page_to_class,
)


def urgent_project_automation(database_id: str, api_key: str, now: pendulum.DateTime):
    pages = query_pages(
        database_id=database_id,
        api_key=api_key,
    )

    for page in pages:
        project = project_page_to_class(page)
        project = become_urgent(project, now)

        if project.urgent is True:
            update_notion_page(
                project.id,
                properties={"Urgent": {"checkbox": True}},
                api_key=api_key,
            )
