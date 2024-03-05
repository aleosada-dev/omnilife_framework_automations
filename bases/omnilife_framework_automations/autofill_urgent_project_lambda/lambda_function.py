import os
import pendulum
from omnilife_framework_automations.project.automations import urgent_project_automation
from omnilife_framework_automations.logger.logger import setup_logger


def lambda_handler(event, context):
    logger = setup_logger(__name__)

    try:
        database_id = os.environ.get("NOTION_DATABASE_ID")
        api_key = os.environ.get("NOTION_API_KEY")

        urgent_project_automation(database_id, api_key, pendulum.now())
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
