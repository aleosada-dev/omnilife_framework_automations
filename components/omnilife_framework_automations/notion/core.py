import requests

def query_pages(database_id: str, api_key: str):

    if database_id is None or database_id == "":
        raise ValueError("Database ID is empty or None")

    if api_key is None or api_key == "":
        raise ValueError("API key is empty or None") 

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
    #     "filter": {},
    #     "sorts": []
    }

    response = requests.post(f"https://api.notion.com/v1/databases/{database_id}/query", headers=headers, json=payload)
    data = response.json()

    # Process the data as per your requirements
    pages = data["results"]
    return pages