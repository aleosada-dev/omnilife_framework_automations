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
