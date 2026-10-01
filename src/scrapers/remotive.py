import requests
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_remotive(keyword: str = "support") -> list[dict]:
    url = "https://remotive.com/api/remote-jobs"
    params = {"search": keyword, "limit": 100}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    jobs = []
    for item in data.get("jobs", []):
        jobs.append({
            "source": "remotive",
            "id": str(item.get("id")),
            "title": item.get("title"),
            "company": item.get("company_name"),
            "location": item.get("candidate_required_location") or "Remote",
            "url": item.get("url"),
            "description": item.get("description", ""),
            "tags": item.get("tags", []),
            "posted": item.get("publication_date"),
        })
    return jobs