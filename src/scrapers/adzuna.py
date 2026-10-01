import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_adzuna(keyword: str = "technical support") -> list[dict]:
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        return []

    jobs = []
    for country in ("es", "gb"):
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 50,
            "what": keyword,
            "content-type": "application/json",
        }
        try:
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json()
        except Exception:
            continue

        for item in data.get("results", []):
            jobs.append({
                "source": f"adzuna-{country}",
                "id": str(item.get("id")),
                "title": item.get("title"),
                "company": (item.get("company") or {}).get("display_name"),
                "location": (item.get("location") or {}).get("display_name"),
                "url": item.get("redirect_url"),
                "description": item.get("description", ""),
                "tags": [],
                "posted": item.get("created"),
            })
    return jobs