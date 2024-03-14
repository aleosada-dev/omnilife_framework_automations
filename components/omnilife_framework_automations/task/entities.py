from typing import Self
import pendulum
from omnilife_framework_automations.notion.core import (
    safe_check_notion_date,
    safe_check_notion_select,
)
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    FOLLOWUP = "Follow Up"
    DONE = "Done"


class TaskPriority(Enum):
    HIGHLIGHT = "Highlight"
    MUST_DO = "Must Do"
    SHOULD_DO = "Should Do"
    COULD_DO = "Could Do"
    WONT_DO = "Wont Do"
    NONE = None


@dataclass
class Task:
    database_id: str
    id: int
    name: str
    status: TaskStatus
    priority: TaskPriority
    areas: list
    projects: list
    planned_datetime_start: pendulum.DateTime
    planned_datetime_end: pendulum.DateTime
    real_start_datetime: pendulum.DateTime
    real_end_datetime: pendulum.DateTime
    deadline: pendulum.DateTime
    created_at: pendulum.DateTime
    last_edit_at: pendulum.DateTime

    def to_dict(self: Self) -> dict:
        return {
            "database_id": self.database_id,
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "priority": self.priority.value,
            "areas": self.areas,
            "projects": self.projects,
            "planned_datetime_start": self.planned_datetime_start.to_iso8601_string()
            if self.planned_datetime_start
            else None,
            "planned_datetime_end": self.planned_datetime_end.to_iso8601_string()
            if self.planned_datetime_end
            else None,
            "real_start_datetime": self.real_start_datetime.to_iso8601_string()
            if self.real_start_datetime
            else None,
            "real_end_datetime": self.real_end_datetime.to_iso8601_string()
            if self.real_end_datetime
            else None,
            "deadline": self.deadline.to_iso8601_string() if self.deadline else None,
            "created_at": self.created_at.to_iso8601_string()
            if self.created_at
            else None,
            "last_edit_at": self.last_edit_at.to_iso8601_string()
            if self.last_edit_at
            else None,
        }

    def map_to_notion_properties(self: Self) -> dict:
        props = {}
        props["Name"] = {"title": [{"text": {"content": self.name}}]}
        props["Status"] = {"status": {"name": self.status.value}}

        if self.priority:
            props["Priority"] = {"select": {"name": self.priority.value}}

        if self.planned_datetime_start:
            props["Planned DateTime"] = {
                "date": {"start": self.planned_datetime_start.to_iso8601_string()}
            }

        if self.planned_datetime_end:
            props["Planned DateTime"]["date"]["end"] = (
                self.planned_datetime_end.to_iso8601_string()
            )

        if self.real_start_datetime:
            props["Real Start DateTime"] = {
                "date": {"start": self.real_start_datetime.to_iso8601_string()}
            }

        if self.real_end_datetime:
            props["Real End DateTime"] = {
                "date": {"start": self.real_end_datetime.to_iso8601_string()}
            }

        if self.deadline:
            props["Deadline"] = {"date": {"start": self.deadline.to_iso8601_string()}}

        if self.areas:
            props["Areas"] = {"relation": [{"id": area} for area in self.areas]}

        if self.projects:
            props["Projects"] = {
                "relation": [{"id": project} for project in self.projects]
            }

        return props


def map_notion_task_to_entity(page: dict):
    planned_datetime_start = safe_check_notion_date(page, "Planned DateTime")
    planned_datetime_end = safe_check_notion_date(page, "Planned DateTime", True)
    real_start_datetime = safe_check_notion_date(page, "Real Start DateTime")
    real_end_datetime = safe_check_notion_date(page, "Real End DateTime")
    deadline = safe_check_notion_date(page, "Deadline")
    priority = safe_check_notion_select(page, "Priority")

    return Task(
        database_id=page["parent"]["database_id"],
        id=page["id"],
        name=page["properties"]["Name"]["title"][0]["text"]["content"],
        status=TaskStatus(page["properties"]["Status"]["select"]["name"]),
        priority=TaskPriority(priority),
        areas=[],
        projects=[],
        planned_datetime_start=planned_datetime_start,
        planned_datetime_end=planned_datetime_end,
        real_start_datetime=real_start_datetime,
        real_end_datetime=real_end_datetime,
        deadline=deadline,
        created_at=pendulum.parse(page["created_time"]),
        last_edit_at=pendulum.parse(page["last_edited_time"]),
    )
