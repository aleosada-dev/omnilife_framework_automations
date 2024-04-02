from abc import abstractmethod


class IEventRepository:
    @abstractmethod
    def get_events(self, calendar_id: str, start_min: str, start_max: str):
        raise NotImplementedError
