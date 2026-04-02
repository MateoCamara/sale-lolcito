import subprocess
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def is_client_running():
    """Comprueba si el proceso LeagueClientUx.exe está corriendo."""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq LeagueClientUx.exe"],
            capture_output=True, text=True
        )
        return "LeagueClientUx.exe" in result.stdout
    except Exception:
        return False


def get_lockfile(path):
    """Parsea el lockfile de LoL y devuelve (port, password)."""
    with open(path, "r") as f:
        content = f.read().strip()
    # Formato: LeagueClient:pid:port:password:protocol
    parts = content.split(":")
    port = parts[2]
    password = parts[3]
    return port, password


def get_friends(port, password):
    """Obtiene la lista de amigos desde la LCU API."""
    url = f"https://127.0.0.1:{port}/lol-chat/v1/friends"
    resp = requests.get(url, auth=("riot", password), verify=False)
    resp.raise_for_status()
    return resp.json()


def get_last_match_result(port, password, puuid):
    """Consulta el historial y devuelve 'win', 'loss' o None."""
    try:
        url = f"https://127.0.0.1:{port}/lol-match-history/v1/products/lol/{puuid}/matches"
        resp = requests.get(
            url, auth=("riot", password), verify=False,
            params={"begIndex": 0, "endIndex": 1},
        )
        resp.raise_for_status()
        games = resp.json().get("games", {}).get("games", [])
        if not games:
            return None
        won = games[0].get("participants", [{}])[0].get("stats", {}).get("win")
        if won is None:
            return None
        return "win" if won else "loss"
    except Exception as e:
        print(f"  Error consultando historial: {e}")
        return None
