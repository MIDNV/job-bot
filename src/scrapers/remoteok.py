import requests
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_remoteok(keyword: str = "support") -> list[dict]:
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "job-bot/1.0 (contact: glen.owen.diaz.thornton@gmail.com)"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    data = r.json()

    jobs = []
    for item in data[1:]:
        title = (item.get("position") or "").lower()
        tags = " ".join(item.get("tags", [])).lower()
        if keyword.lower() in title or keyword.lower() in tags:
            jobs.append({
                "source": "remoteok",
                "id": str(item.get("id")),
                "title": item.get("position"),
                "company": item.get("company"),
                "location": item.get("location") or "Remote",
                "url": item.get("url"),
                "description": item.get("description", ""),
                "tags": item.get("tags", []),
                "posted": item.get("date"),
            })
    return jobs