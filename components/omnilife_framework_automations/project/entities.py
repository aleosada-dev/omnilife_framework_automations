import pendulum
from dataclasses import dataclass
from enum import Enum


class ProjectStatus(Enum):
    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    DONE = "Done"


class ProjectSize(Enum):
    EXTRA_SMALL = "PP"
    SMALL = "P"
    MEDIUM = "M"
    LARGE = "G"
    EXTRA_LARGE = "GG"


class ProjectValue(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass(eq=True)
class Project:
    database_id: str
    id: str
    name: str
    status: ProjectStatus
    areas: list[str]
    project_size: ProjectSize
    value: ProjectValue
    days_before_urgent: int
    deadline: pendulum.DateTime
    urgent: bool
    goals: list[str]
    start_date: pendulum.DateTime
    end_date: pendulum.DateTime
    created_at: pendulum.DateTime
    last_edit_at: pendulum.DateTime


def safe_check_notion_date(page: dict, property_name: str) -> pendulum.DateTime | None:
    if page["properties"][property_name]["date"] != None:
        return pendulum.parse(page["properties"][property_name]["date"]["start"])
    return None


def project_page_to_class(page: dict) -> Project:
    deadline = safe_check_notion_date(page, "Deadline")
    start_date = safe_check_notion_date(page, "Start Date")
    end_date = safe_check_notion_date(page, "End Date")

    return Project(
        database_id=page["parent"]["database_id"],
        id=page["id"],
        name=page["properties"]["Name"]["title"][0]["text"]["content"],
        status=ProjectStatus(page["properties"]["Status"]["status"]["name"]),
        areas=[],
        project_size=ProjectSize(page["properties"]["Size"]["select"]["name"]),
        value=ProjectValue(page["properties"]["Value"]["select"]["name"]),
        days_before_urgent=page["properties"]["Days Before Urgent"]["number"],
        deadline=deadline,
        urgent=page["properties"]["Urgent"]["checkbox"],
        goals=[],
        start_date=start_date,
        end_date=end_date,
        created_at=pendulum.parse(page["created_time"]),
        last_edit_at=pendulum.parse(page["last_edited_time"]),
    )


def become_urgent(project: Project, now: pendulum.DateTime) -> Project:
    if (project.deadline - now).in_days() <= project.days_before_urgent:
        project.urgent = True

    return project
