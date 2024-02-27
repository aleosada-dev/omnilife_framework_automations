import json
from datetime import datetime
from omnilife_framework_automations.project.entities import Project


def lambda_handler(event, context):
    p = Project(
        id=1,
        name="Project 1",
        area="Area 1",
        status="Not started",
        start_date=datetime.now(),
        end_date=datetime.now(),
        created_at=datetime.now(),
        last_edit_at=datetime.now(),
    )
    return {
        'statusCode': 200,
        'body': json.dumps(p)
    }