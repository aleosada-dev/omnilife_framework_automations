import os
import pendulum
from omnilife_framework_automations.project.automations import urgent_project_automation


def lambda_handler(event, context):
    database_id = os.environ.get("NOTION_DATABASE_ID")
    api_key = os.environ.get("NOTION_API_KEY")

    urgent_project_automation(database_id, api_key, pendulum.now())

    return {
        "statusCode": 200,
    }
