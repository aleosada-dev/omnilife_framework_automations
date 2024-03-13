import os
from dotenv import load_dotenv
from omnilife_framework_automations.infrastructure.repositories import (
    IParameterRepository,
)

load_dotenv()


class EnviromentVariableParameterRepository(IParameterRepository):
    def __init__(self, env: str = None):
        self.env = env

    def get(self, key: str):
        return os.getenv(key, None)
