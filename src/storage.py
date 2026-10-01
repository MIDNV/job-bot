import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/jobs.db")

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            uid TEXT PRIMARY KEY,
            source TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            url TEXT,
            score INTEGER,
            posted TEXT,
            first_seen TEXT
        )
    """)
    con.commit()
    con.close()

def save_new_jobs(jobs: list[dict]) -> list[dict]:
    init_db()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    new_jobs = []

    for job in jobs:
        uid = f"{job['source']}::{job['id']}"
        job["uid"] = uid
        cur.execute("SELECT 1 FROM jobs WHERE uid = ?", (uid,))
        if cur.fetchone():
            continue

        cur.execute("""
            INSERT INTO jobs (uid, source, title, company, location, url, score, posted, first_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            uid, job["source"], job.get("title"), job.get("company"),
            job.get("location"), job.get("url"), job.get("score", 0),
            job.get("posted"), datetime.utcnow().isoformat(),
        ))
        new_jobs.append(job)

    con.commit()
    con.close()
    return new_jobs

def export_json(jobs: list[dict], path: str = "data/latest_jobs.json"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(jobs, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )