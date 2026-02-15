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
