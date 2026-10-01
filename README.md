# 🤖 Job Bot — Automated Remote Job Search

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B-5391FE?logo=powershell&logoColor=white)](https://learn.microsoft.com/powershell/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)](#-requirements)

A personal job-search bot that automatically queries multiple remote-job boards, filters offers by role and location, and stores new findings in a local database to avoid duplicates.

Built for **remote-only, Spain-based** opportunities in **Technical Support, Customer Success, and SaaS Support** — but easily configurable for any profile.

---

## ✨ Features

- 🔍 **Multi-source search** — queries RemoteOK, Remotive, and Arbeitnow public APIs
- 🧠 **Keyword-based scoring** — every offer is ranked using a weighted keyword profile
- 🇪🇸 **Location filtering** — restricts results to Spain / EU-remote / Worldwide roles
- 🚫 **Blacklist** — automatically discards roles outside your target (e.g. sales, full-stack dev)
- 💾 **SQLite storage** — deduplicates offers across runs
- 📲 **Telegram notifications** *(optional)* — get new offers pushed to your phone
- ⏰ **Daily automation** — runs itself every morning via Windows Task Scheduler
- 📄 **JSON export** — inspect results with a built-in viewer
- 🔒 **Secret-safe** — API keys stored in `.env`, never committed to Git

---

## 🗂️ Project Structure

```
job-bot/
├── config/
│   └── profile.yaml          # Your profile: keywords, blacklist, filters
├── src/
│   ├── main.py               # Orchestrator
│   ├── matcher.py            # Scoring + filtering logic
│   ├── storage.py            # SQLite + JSON persistence
│   ├── notifier.py           # Telegram notifications (optional)
│   └── scrapers/
│       ├── remoteok.py
│       ├── remotive.py
│       ├── arbeitnow.py
│       └── adzuna.py         # Optional, requires API key
├── scripts/
│   ├── setup.ps1             # One-time environment setup
│   ├── run_bot.ps1           # Manual execution
│   ├── schedule_task.ps1     # Register daily Windows task
│   └── ver_ofertas.py        # Pretty-print saved offers
├── data/                     # SQLite DB + JSON exports (gitignored)
├── logs/                     # Run logs (gitignored)
├── .env.example              # Template for secrets
├── requirements.txt
└── README.md
```

---

## 🧰 Requirements

| Tool | Version | Notes |
|---|---|---|
| **Python** | 3.10 or newer | Must be added to PATH |
| **Git** | Any recent version | For cloning and version control |
| **PowerShell** | 5.1 or newer | Ships with Windows 10/11 |
| **Windows** | 10 / 11 | Required for Task Scheduler automation |

---

## 🚀 Getting Started

### 1. Clone the repository

```powershell
git clone https://github.com/MIDNV/job-bot.git
cd job-bot
```

### 2. Run the setup script

Creates a virtual environment, installs dependencies, and copies `.env.example` → `.env`:

```powershell
.\scripts\setup.ps1
```

If PowerShell blocks the script, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 3. Configure your profile

Edit `config/profile.yaml` to match your target roles, languages, and country:

```yaml
candidate:
  name: "Your Name"
  location: "Your City, Country"
  languages: ["en", "es"]
  remote_only: true

location_required: true
location_keywords:
  - "spain"
  - "madrid"
  - "barcelona"
  - "remote spain"
  # ...

keywords:
  "zendesk": 10
  "customer success": 8
  "technical support": 8
  # ...

blacklist:
  - "account executive"
  - "full-stack"
  - "product manager"
  # ...

min_score: 10
```

**How scoring works:** every keyword found in an offer adds its weight to the offer's score. Offers below `min_score` are discarded. Any term in `blacklist` immediately disqualifies the offer.

### 4. Run your first search

```powershell
.\scripts\run_bot.ps1
```

### 5. View the results

```powershell
.\.venv\Scripts\python.exe scripts\ver_ofertas.py
```

Or open the JSON directly:

```powershell
Get-Content data\latest_jobs.json | ConvertFrom-Json
```

---

## ⚙️ Configuration Reference

### `config/profile.yaml`

| Key | Type | Description |
|---|---|---|
| `candidate.remote_only` | bool | Adds a bonus to remote-listed offers |
| `location_required` | bool | If `true`, offers must match a `location_keywords` entry |
| `location_keywords` | list | Regions/cities/countries you accept |
| `keywords` | map | `"term": weight` — the higher, the more it matters |
| `blacklist` | list | Terms that instantly discard an offer |
| `min_score` | int | Minimum score to keep an offer |

### `.env` (secrets — never committed)

```env
# Telegram notifications (optional)
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=

# Adzuna API (optional)
ADZUNA_APP_ID=
ADZUNA_APP_KEY=
```

---

## ⏰ Automating Daily Runs

Register a Windows Task Scheduler job that runs the bot every morning:

```powershell
.\scripts\schedule_task.ps1
```

By default, it runs at **09:00** and only while your user session is active.

### Managing the task

```powershell
Get-ScheduledTask -TaskName "JobBot"                     # View
Start-ScheduledTask -TaskName "JobBot"                   # Run now
Get-ScheduledTaskInfo -TaskName "JobBot"                 # Check last result
Disable-ScheduledTask -TaskName "JobBot"                 # Pause
Enable-ScheduledTask -TaskName "JobBot"                  # Resume
Unregister-ScheduledTask -TaskName "JobBot" -Confirm:$false   # Delete
```

To change the execution time, edit `$HoraEjecucion` inside `scripts/schedule_task.ps1` and re-run the script.

---

## 📲 Optional: Telegram Notifications

1. Open Telegram and message **@BotFather** → `/newbot` → copy the **token**
2. Message **@userinfobot** → copy your **chat ID**
3. Add both to `.env`:

   ```env
   TELEGRAM_TOKEN=123456789:ABCdef...
   TELEGRAM_CHAT_ID=987654321
   ```

4. Send any message to your own bot first (Telegram bots can't start chats)

The next time the bot finds **new** offers, they'll arrive as a Telegram message.

---

## 🧪 How It Works

```
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │  RemoteOK    │    │  Remotive    │    │  Arbeitnow   │
  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
         │                   │                   │
         └───────────────┬───┴───────────────────┘
                         ▼
                 ┌──────────────┐
                 │   matcher    │  ← scores + filters (profile.yaml)
                 └──────┬───────┘
                        ▼
                 ┌──────────────┐
                 │   storage    │  ← deduplicates with SQLite
                 └──────┬───────┘
                        ▼
        ┌───────────────┴──────────────┐
        ▼                              ▼
  ┌──────────────┐            ┌──────────────┐
  │  JSON export │            │  Telegram    │
  └──────────────┘            └──────────────┘
```

1. **Scrapers** pull offers from each API using the search terms defined in `src/main.py`
2. **Matcher** scores every offer using `profile.yaml` and drops the ones below `min_score`
3. **Storage** compares each offer's `source::id` against the SQLite DB and only keeps new ones
4. **Notifier** (optional) pushes new offers to Telegram
5. **Export** writes the full ranked list to `data/latest_jobs.json`

---

## 🛠️ Tech Stack

- **Python 3.10+** — core logic
- **requests** — HTTP client for API calls
- **PyYAML** — parses `profile.yaml`
- **python-dotenv** — loads `.env`
- **tenacity** — retries failed API calls with exponential backoff
- **SQLite** — zero-setup local database
- **PowerShell** — setup, execution, and automation on Windows
- **Windows Task Scheduler** — daily runs

---

## 🔒 Security Notes

- `.env` is **gitignored** — your API keys and Telegram tokens never leave your machine
- `.venv/`, `data/`, and `logs/` are also gitignored — no clutter in the repo
- Only `.env.example` (with empty values) is committed, so others know which variables to fill in

---

## 🧯 Troubleshooting

| Symptom | Fix |
|---|---|
| `Activate.ps1 cannot be loaded` | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `ModuleNotFoundError: No module named 'src'` | Run from project root: `cd D:\Documentos\job-bot` |
| `SSLError` / `ConnectionError` | Firewall or VPN blocking the API request |
| PowerShell prints red `NativeCommandError` | Harmless — PowerShell treats Python's stderr as errors. Ignore or check the log. |
| `KeyError: 'candidate'` in profile | YAML indentation issue — use spaces, not tabs |
| 0 relevant offers found | Lower `min_score` or add more `location_keywords` |

---

## 🗺️ Roadmap

- [ ] Additional scrapers (InfoJobs, Wellfound, WeWorkRemotely)
- [ ] Email digest via SMTP
- [ ] Static HTML dashboard (Jinja2)
- [ ] Semantic matching with sentence embeddings
- [ ] Docker image for cross-platform runs

---

## 📝 License

Released under the **MIT License** — feel free to fork, adapt, and reuse.

---

## 👤 Author

**Glen Owen Diaz Thornton**
- GitHub: [@MIDNV](https://github.com/MIDNV)
- LinkedIn: [linkedin.com/in/glenodt](https://linkedin.com/in/glenodt)
- Email: glen.owen.diaz.thornton@gmail.com

---

<p align="center">
  <sub>Built with 🐍 Python, ⚡ PowerShell, and a lot of ☕</sub>
</p>
