import requests
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_arbeitnow(keyword: str = "support") -> list[dict]:
    url = "https://www.arbeitnow.com/api/job-board-api"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()

    jobs = []
    for item in data.get("data", []):
        title = (item.get("title") or "").lower()
        desc = (item.get("description") or "").lower()
        if keyword.lower() in title or keyword.lower() in desc:
            jobs.append({
                "source": "arbeitnow",
                "id": item.get("slug"),
                "title": item.get("title"),
                "company": item.get("company_name"),
                "location": item.get("location") or "Remote",
                "url": item.get("url"),
                "description": item.get("description", ""),
                "tags": item.get("tags", []),
                "posted": item.get("created_at"),
            })
    return jobs