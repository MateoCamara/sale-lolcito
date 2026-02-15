import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from config import FRIENDS, POLL_INTERVAL, LOL_LOCKFILE_PATH, MESSAGING_SERVICE
from lcu import is_client_running, get_lockfile, get_friends

if MESSAGING_SERVICE == "telegram":
    from telegram_client import send_telegram as send_message
else:
    from whatsapp_client import send_whatsapp as send_message


QUEUE_NAMES = {
    "RANKED_SOLO_5x5": "Ranked Solo/Duo",
    "RANKED_FLEX_SR": "Ranked Flex",
    "NORMAL_BLIND": "Normal Ciega",
    "NORMAL_DRAFT": "Normal Draft",
    "ARAM_UNRANKED_5x5": "ARAM",
    "URF": "URF",
    "CHERRY": "Arena",
    "BOT": "vs IA",
    "ONEFORALL_5x5": "One for All",
}


def get_status(friend):
    """Extrae el estado resumido de un amigo de la LCU API."""
    lol = friend.get("lol", {})
    return {
        "availability": friend.get("availability", "offline"),
        "gameStatus": lol.get("gameStatus", ""),
        "champion": lol.get("skinname", ""),
        "queueType": lol.get("gameQueueType", ""),
        "gameMode": lol.get("gameMode", ""),
    }


def format_game_info(status):
    """Formatea la info de partida: campeón + tipo de cola."""
    parts = []
    if status["champion"]:
        parts.append(status["champion"])
    queue = QUEUE_NAMES.get(status["queueType"], "")
    if not queue and status["gameMode"]:
        queue = status["gameMode"]
    if queue:
        parts.append(queue)
    return " - ".join(parts) if parts else ""


def detect_changes(prev, curr):
    """Compara estados y devuelve lista de mensajes a enviar."""
    messages = []
    for name in FRIENDS:
        old = prev.get(name, {"availability": "offline", "gameStatus": ""})
        new = curr.get(name, {"availability": "offline", "gameStatus": ""})

        old_avail = old["availability"]
        new_avail = new["availability"]
        old_game = old["gameStatus"]
        new_game = new["gameStatus"]

        if old_avail == new_avail and old_game == new_game:
            continue

        was_offline = old_avail == "offline"
        is_offline = new_avail == "offline"
        is_in_game = new_game in ("inGame", "inTeamBuilder_Picking")
        was_in_game = old_game in ("inGame", "inTeamBuilder_Picking")
        is_in_champ_select = new_game == "championSelect"
        was_in_champ_select = old_game == "championSelect"
        is_in_queue = new_game == "inQueue"
        was_in_queue = old_game == "inQueue"

        if was_offline and not is_offline:
            messages.append(f"\U0001f7e2 {name} se ha conectado!")
        elif not was_offline and is_offline:
            messages.append(f"\U0001f534 {name} se ha desconectado")

        if is_in_queue and not was_in_queue:
            info = format_game_info(new)
            suffix = f" ({info})" if info else ""
            messages.append(f"\U0001f50d {name} est\u00e1 buscando partida{suffix}")
        elif is_in_champ_select and not was_in_champ_select:
            info = format_game_info(new)
            suffix = f" ({info})" if info else ""
            messages.append(f"\U0001f9d9 {name} est\u00e1 en selecci\u00f3n de campe\u00f3n{suffix}")
        elif is_in_game and not was_in_game:
            info = format_game_info(new)
            suffix = f" ({info})" if info else ""
            messages.append(f"\U0001f3ae {name} ha entrado en partida!{suffix}")
        elif not is_in_game and was_in_game and not is_offline:
            messages.append(f"\U0001f3c1 {name} ha salido de partida")

    return messages


def build_state(friends_list):
    """Construye dict {nombre: status} para los amigos objetivo."""
    state = {}
    for f in friends_list:
        name = (f.get("gameName") or f.get("name") or "").lower()
        if name in [n.lower() for n in FRIENDS]:
            original_name = next(n for n in FRIENDS if n.lower() == name)
            state[original_name] = get_status(f)
    return state


def main():
    print("Bot LoL - Monitor de amigos")
    print(f"Monitorizando: {', '.join(FRIENDS)}")
    print(f"Intervalo de sondeo: {POLL_INTERVAL}s")
    print("-" * 40)

    prev_state = {}

    while True:
        if not is_client_running():
            print("Cliente LoL no detectado. Esperando...")
            prev_state = {}
            time.sleep(POLL_INTERVAL)
            continue

        try:
            port, password = get_lockfile(LOL_LOCKFILE_PATH)
        except FileNotFoundError:
            print("Lockfile no encontrado. Esperando...")
            time.sleep(POLL_INTERVAL)
            continue
        except Exception as e:
            print(f"Error leyendo lockfile: {e}")
            time.sleep(POLL_INTERVAL)
            continue

        try:
            friends_list = get_friends(port, password)
        except Exception as e:
            print(f"Error consultando LCU API: {e}")
            time.sleep(POLL_INTERVAL)
            continue

        curr_state = build_state(friends_list)

        if prev_state:
            messages = detect_changes(prev_state, curr_state)
            for msg in messages:
                send_message(msg)
                print(f">> {msg}")
        else:
            print("Estado inicial capturado:")
            for name, status in curr_state.items():
                info = format_game_info(status)
                extra = f" | {info}" if info else ""
                print(f"  {name}: {status['availability']} / {status['gameStatus'] or '-'}{extra}")

        prev_state = curr_state
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
