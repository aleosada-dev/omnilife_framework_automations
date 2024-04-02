import boto3
from omnilife_framework_automations.parameter.repositories import (
    AWSParameterStoreRepository,
)


def test_get_aws_parameter_by_key():
    session = boto3.Session()

    repository = AWSParameterStoreRepository(session, "sa-east-1", "")
    result = repository.get("/google/calendar/agenda_id")
    print(result)


test_get_aws_parameter_by_key()
