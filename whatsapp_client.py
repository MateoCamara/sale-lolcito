import requests
from config import WHATSAPP_SERVICE_URL, WHATSAPP_GROUP


def send_whatsapp(message):
    """Envía un mensaje al grupo de WhatsApp a través del servicio Node.js."""
    try:
        resp = requests.post(
            f"{WHATSAPP_SERVICE_URL}/send",
            json={"group": WHATSAPP_GROUP, "message": message},
            timeout=10,
        )
        if resp.ok:
            print(f"  WhatsApp OK: {message}")
        else:
            print(f"  WhatsApp error ({resp.status_code}): {resp.text}")
    except requests.ConnectionError:
        print("  WhatsApp servicio no disponible (¿está corriendo el servidor Node.js?)")
    except Exception as e:
        print(f"  WhatsApp error: {e}")
