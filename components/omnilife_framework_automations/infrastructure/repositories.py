from omnilife_framework_automations.task.entities import Task


class IProjectRepository:
    def query_pages(
        self,
        database_id: str,
        api_key: str,
        filter_query: str = None,
        sort_query: str = None,
    ):
        raise NotImplementedError

    def update_notion_page(self, page_id: str, properties: dict, api_key: str):
        raise NotImplementedError


class IEventRespository:
    def get_events(calendar_id: str, start_min: str, start_max: str):
        raise NotImplementedError


class ITaskRepository:
    def add_task(self, task: Task):
        raise NotImplementedError


class IParameterRepository:
    def get(self, parameter: str):
        raise NotImplementedError
