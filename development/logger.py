import pendulum
from omnilife_framework_automations.logger.logger import setup_logger
from omnilife_framework_automations.project.entities import (
    Project,
    ProjectSize,
    ProjectValue,
    ProjectStatus,
)

logger = setup_logger("logger_module")

p = Project(
    database_id="123",
    id="123",
    name="Project 1",
    status=ProjectStatus.NOT_STARTED,
    areas=["Area 1", "Area 2"],
    project_size=ProjectSize.EXTRA_SMALL,
    value=ProjectValue.LOW,
    days_before_urgent=5,
    deadline=pendulum.now(),
    urgent=False,
    goals=["Goal 1", "Goal 2"],
    start_date=pendulum.now(),
    end_date=pendulum.now(),
    created_at=pendulum.now(),
    last_edit_at=pendulum.now(),
)

# Log an info message
logger.info(
    "User login attempt",
    extra={
        "params": {
            "project": p.to_dict(),
        }
    },
)
