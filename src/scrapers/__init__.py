from .remoteok import fetch_remoteok
from .remotive import fetch_remotive
from .arbeitnow import fetch_arbeitnow
from .adzuna import fetch_adzuna

ALL_SCRAPERS = [
    ("remoteok", fetch_remoteok),
    ("remotive", fetch_remotive),
    ("arbeitnow", fetch_arbeitnow),
    ("adzuna", fetch_adzuna),
]