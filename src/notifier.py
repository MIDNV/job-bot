import os
import requests

def notify_telegram(jobs: list[dict]) -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id or not jobs:
        return

    lines = ["🔔 *Nuevas ofertas para ti:*\n"]
    for j in jobs[:10]:
        lines.append(
            f"• *{j['title']}* @ {j.get('company','?')} — score {j['score']}\n"
            f"  {j.get('location','')}\n  {j['url']}\n"
        )
    text = "\n".join(lines)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }, timeout=15)
    except Exception as e:
        print(f"[notifier] Error enviando a Telegram: {e}")