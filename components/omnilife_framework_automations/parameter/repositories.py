import os
import boto3
from injector import inject
from omnilife_framework_automations.infrastructure.repositories.parameter import (
    IParameterRepository,
)


class EnviromentVariableParameterRepository(IParameterRepository):
    def get(self, key: str):
        key.upper()
        return os.getenv(key, None)


class AWSParameterStoreRepository(IParameterRepository):
    def __init__(self, session: boto3.Session):
        self.ssm_client = session.client("ssm")

    def get(self, key: str):
        try:
            key = key.replace("_", "/").lower()
            response = self.ssm_client.get_parameter(
                Name=f"/{key}", WithDecryption=True
            )
            return response["Parameter"]["Value"]
        except Exception as e:
            print(f"Error getting parameter {key}: {e}")
            return None
