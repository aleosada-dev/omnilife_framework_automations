from typing import Self
import pendulum


class IProjectService:
    def urgent_project_automation(
        self, database_id: str, api_key: str, now: pendulum.DateTime
    ):
        raise NotImplementedError


class ITaskService:
    def plan_next_week(self: Self, agenda_id: str):
        raise NotImplementedError
