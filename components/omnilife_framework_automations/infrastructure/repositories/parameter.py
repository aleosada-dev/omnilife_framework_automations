from abc import abstractmethod


class IParameterRepository:
    @abstractmethod
    def get(self, key: str):
        raise NotImplementedError
