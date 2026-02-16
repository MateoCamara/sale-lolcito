# Sale Lolcito

<p align="center">
  <img src="assets/lolcito.jpg" width="300">
</p>

**Harto de que tus colegas se echen un lolcito a escondidas y no avisen?** Esta es la solución.

Abre el cliente de LoL, activa el bot y te llegará un mensaje al Telegram cada vez que tus amigos se conecten, entren en partida o se desconecten. **No se escaparán de tus garras.**

## Qué hace exactamente?

El bot se conecta a la API local del cliente de League of Legends (la LCU API) y monitoriza el estado de los amigos que le digas. Cuando detecta un cambio, te avisa:

- `🟢 Mejill0n se ha conectado!`
- `🔍 Mejill0n está buscando partida (Ranked Solo/Duo)`
- `🧙 Mejill0n está en selección de campeón (Ranked Solo/Duo)`
- `🎮 Mejill0n ha entrado en partida! (Milio - Ranked Solo/Duo)`
- `🏁 Mejill0n ha salido de partida`
- `🔴 Mejill0n se ha desconectado`

Sí, te dice hasta el campeón y el tipo de cola. No hay escapatoria.

## Cómo lo monto?

### 1. Crea un bot de Telegram

1. Habla con [@BotFather](https://t.me/BotFather) en Telegram y crea un bot con `/newbot`
2. Guarda el token que te da
3. Añade el bot al grupo donde quieras recibir alertas
4. Envía un mensaje en el grupo y abre `https://api.telegram.org/bot<TU_TOKEN>/getUpdates` para sacar el `chat_id`

### 2. Configura el .env

Crea un archivo `.env` en la raíz del proyecto:

```
TELEGRAM_BOT_TOKEN=tu_token_aquí
TELEGRAM_CHAT_ID=tu_chat_id_aquí
```

### 3. Instala dependencias

```bash
pip install -r requirements.txt
```

### 4. Edita config.py

Añade los nombres de invocador de tus amigos en la lista `FRIENDS`:

```python
FRIENDS = ["Chirla", "Volandeira", "Mejill0n", "Elfsmen", "XzQiyanaYuntalXz"]
```

### 5. Arranca el bot

Abre el cliente de LoL y ejecuta:

```bash
python -u monitor.py
```

Listo. Ahora siéntate y espera. Cuando alguno de tus colegas se conecte, lo sabrás.

## Modos de envío

El bot soporta 3 modos de mensajería (se cambia en `config.py`):

| Modo | `MESSAGING_SERVICE` | Descripción |
|------|-------------------|-------------|
| **Telegram** | `"telegram"` | Bot de Telegram oficial. Seguro y recomendado. |
| **Clipboard** | `"clipboard"` | Copia el mensaje y lo pega en la ventana activa (WhatsApp Web). Irrastreable. |
| **WhatsApp** | `"whatsapp"` | Vía whatsapp-web.js. Funciona pero riesgo de baneo. No recomendado. |

## Estructura

```
sale-lolcito/
├── monitor.py           # Bucle principal
├── config.py            # Configuración (amigos, modo, etc.)
├── lcu.py               # Conexión a la LCU API del cliente de LoL
├── telegram_client.py   # Envío vía Telegram
├── clipboard_client.py  # Envío vía portapapeles (Ctrl+V + Enter)
├── whatsapp_client.py   # Envío vía servicio Node.js
├── whatsapp-service/    # Servidor WhatsApp (opcional)
├── requirements.txt
└── .env                 # Credenciales (no se sube al repo)
```

## Por Demacia!
