import requests
import pendulum


def safe_check_notion_select(page: dict, property_name: str) -> str | None:
    if page["properties"].get(property_name) is None:
        return None

    if page["properties"][property_name]["select"] is not None:
        return page["properties"][property_name]["select"]["name"]

    return None


def safe_check_notion_date(page: dict, property_name: str) -> pendulum.DateTime | None:
    if page["properties"].get(property_name) is None:
        return None

    if page["properties"][property_name]["date"] is not None:
        return pendulum.parse(page["properties"][property_name]["date"]["start"])
    return None


def query_pages(
    database_id: str, api_key: str, filter_query: dict = None, sort_query: dict = None
):
    if database_id is None or database_id == "":
        raise ValueError("Database ID is empty or None")

    if api_key is None or api_key == "":
        raise ValueError("API key is empty or None")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    payload = {}
    if filter_query is not None:
        payload.update(filter_query)

    if sort_query is not None:
        payload.update(sort_query)

    response = requests.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        headers=headers,
        json=payload,
    )
    data = response.json()

    # Process the data as per your requirements
    pages = data["results"]
    return pages


def update_notion_page(page_id: str, properties: dict, api_key: str):
    if page_id is None or page_id == "":
        raise ValueError("Page ID is empty or None")

    if api_key is None or api_key == "":
        raise ValueError("API key is empty or None")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    payload = {"properties": properties}
    response = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=headers,
        json=payload,
    )
    if response.status_code != 200:
        raise ValueError("Failed to update Notion page")
