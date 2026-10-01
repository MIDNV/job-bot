import re


def _clean(text: str) -> str:
    """Quita etiquetas HTML y pasa a minúsculas."""
    return re.sub(r"<[^>]+>", " ", text or "").lower()


def score_job(job: dict, profile: dict) -> int:
    """
    Devuelve la puntuación de una oferta.
    - -1 = descartada (blacklist o filtro geográfico)
    - 0+ = puntuación
    """
    haystack = " ".join([
        _clean(job.get("title", "")),
        _clean(job.get("description", "")),
        " ".join(job.get("tags") or []).lower(),
    ])
    location_text = _clean(job.get("location", ""))

    # ----- 1. Blacklist de roles -----
    for bad in profile.get("blacklist", []):
        if bad.lower() in haystack:
            return -1

    # ----- 2. Filtro geográfico -----
    if profile.get("location_required", False):
        loc_kws = [k.lower() for k in profile.get("location_keywords", [])]
        # Buscar en ubicación O en el resto del texto (a veces "Spain" sale en la descripción)
        if not any(kw in location_text or kw in haystack for kw in loc_kws):
            return -1

    # ----- 3. Puntuación por keywords -----
    score = 0
    for kw, weight in profile.get("keywords", {}).items():
        if kw.lower() in haystack:
            score += weight

    # ----- 4. Bonus por remoto -----
    if "remote" in location_text and profile.get("candidate", {}).get("remote_only"):
        score += 2

    # ----- 5. Bonus extra por España explícita -----
    spain_terms = ["spain", "españa", "espana", "madrid", "barcelona",
                   "valencia", "sevilla", "tenerife", "canarias"]
    if any(t in location_text for t in spain_terms):
        score += 5

    return score


def filter_and_rank(jobs: list[dict], profile: dict) -> list[dict]:
    """Filtra por min_score, añade campo 'score' y ordena descendente."""
    min_score = profile.get("min_score", 10)
    ranked = []
    for job in jobs:
        s = score_job(job, profile)
        if s >= min_score:
            job["score"] = s
            ranked.append(job)
    ranked.sort(key=lambda j: j["score"], reverse=True)
    return ranked