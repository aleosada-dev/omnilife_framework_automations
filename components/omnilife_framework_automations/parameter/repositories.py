import os


class EnviromentVariableParameterRepository:
    def __init__(self, env: str = None):
        self.env = env

    def get(self, key: str):
        return os.getenv(key, None)
