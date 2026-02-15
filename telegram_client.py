import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(message):
    """Envía un mensaje al chat/grupo de Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("  Telegram no configurado: falta TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en config.py")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
        }, timeout=10)
        if resp.ok:
            print(f"  Telegram OK: {message}")
        else:
            print(f"  Telegram error ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"  Telegram error: {e}")
