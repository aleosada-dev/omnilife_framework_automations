import os
from omnilife_framework_automations.infrastructure.repositories import (
    IParameterRepository,
)


class EnviromentVariableParameterRepository(IParameterRepository):
    def __init__(self, env: str = None):
        self.env = env

    def get(self, key: str):
        return os.getenv(key, None)
