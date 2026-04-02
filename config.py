import os
from dotenv import load_dotenv

load_dotenv()

FRIENDS = ["Chirla", "Volandeira", "Mejill0n", "Elfsmen", "XzQiyanaYuntalXz", "Alcreapy", "Carajill0"]

POLL_INTERVAL = 15  # segundos entre cada consulta

LOL_LOCKFILE_PATH = r"C:\Riot Games\League of Legends\lockfile"

# --- Servicio de mensajería: "telegram" o "whatsapp" ---
MESSAGING_SERVICE = "clipboard"

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# WhatsApp (solo si MESSAGING_SERVICE = "whatsapp")
WHATSAPP_GROUP = "Bbq + Velada"
WHATSAPP_SERVICE_URL = "http://localhost:3001"
