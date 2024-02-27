import requests

def query_pages(database_id: str, api_key: str):
    headers = {
        "Authorization": f"Bearer ${api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
    }

    payload = {
        "filter": {},
        "sorts": []
    }

    response = requests.post(f"https://api.notion.com/v1/databases/{database_id}/query", headers=headers, json=payload)
    data = response.json()

    # Process the data as per your requirements
    pages = data["results"]
    return pages