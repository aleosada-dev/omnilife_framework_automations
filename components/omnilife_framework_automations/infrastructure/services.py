import pendulum


class IProjectService():
    def urgent_project_automation(self, database_id: str, api_key: str, now: pendulum.DateTime):
        raise NotImplementedError