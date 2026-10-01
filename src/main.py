import os
import yaml
import logging
from dotenv import load_dotenv

from src.scrapers import ALL_SCRAPERS
from src.matcher import filter_and_rank
from src.storage import save_new_jobs, export_json
from src.notifier import notify_telegram

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("job-bot")

SEARCH_TERMS = [
    # Inglés
    "technical support",
    "customer success",
    "zendesk",
    "gaming support",
    "player support",
    "helpdesk",
    "customer support",
    "support specialist",
    # Español
    "soporte técnico",
    "atención al cliente",
    "soporte al cliente",
]

def load_profile(path: str = "config/profile.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    load_dotenv()
    profile = load_profile()
    log.info("Perfil cargado para: %s", profile["candidate"]["name"])

    all_jobs: list[dict] = []
    seen_uids = set()

    for name, scraper in ALL_SCRAPERS:
        for term in SEARCH_TERMS:
            try:
                results = scraper(term)
                log.info("[%s] '%s' → %d resultados", name, term, len(results))
                for job in results:
                    uid = f"{job['source']}::{job['id']}"
                    if uid in seen_uids:
                        continue
                    seen_uids.add(uid)
                    all_jobs.append(job)
            except Exception as e:
                log.warning("[%s] fallo con '%s': %s", name, term, e)

    log.info("Total ofertas recogidas: %d", len(all_jobs))

    ranked = filter_and_rank(all_jobs, profile)
    log.info("Ofertas relevantes (score >= %s): %d", profile.get("min_score"), len(ranked))

    new_jobs = save_new_jobs(ranked)
    log.info("Ofertas NUEVAS guardadas: %d", len(new_jobs))

    export_json(ranked)
    notify_telegram(new_jobs)

    print("\n===== TOP OFERTAS NUEVAS =====")
    for j in new_jobs[:15]:
        print(f"  ★ {j['score']:>3}  {j['title']}  @ {j.get('company')}  [{j['source']}]")
        print(f"      {j['url']}")
    print("==============================\n")

if __name__ == "__main__":
    main()