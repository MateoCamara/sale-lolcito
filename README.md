# Sale Lolcito

**Harto de que tus colegas se echen un lolcito a escondidas y no avisen?** Esta es la solución.

Abre el cliente de LoL, activa el bot y te llegara un mensaje al Telegram cada vez que tus amigos se conecten, entren en partida o se desconecten. **No se escaparan de tus garras.**

## Que hace exactamente?

El bot se conecta a la API local del cliente de League of Legends (la LCU API) y monitoriza el estado de los amigos que le digas. Cuando detecta un cambio, te avisa:

- `🟢 Mejill0n se ha conectado!`
- `🔍 Mejill0n esta buscando partida (Ranked Solo/Duo)`
- `🧙 Mejill0n esta en seleccion de campeon (Ranked Solo/Duo)`
- `🎮 Mejill0n ha entrado en partida! (Milio - Ranked Solo/Duo)`
- `🏁 Mejill0n ha salido de partida`
- `🔴 Mejill0n se ha desconectado`

Si, te dice hasta el campeon y el tipo de cola. No hay escapatoria.

## Como lo monto?

### 1. Crea un bot de Telegram

1. Habla con [@BotFather](https://t.me/BotFather) en Telegram y crea un bot con `/newbot`
2. Guarda el token que te da
3. Anade el bot al grupo donde quieras recibir alertas
4. Envia un mensaje en el grupo y abre `https://api.telegram.org/bot<TU_TOKEN>/getUpdates` para sacar el `chat_id`

### 2. Configura el .env

Crea un archivo `.env` en la raiz del proyecto:

```
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
```

### 3. Instala dependencias

```bash
pip install -r requirements.txt
```

### 4. Edita config.py

Anade los nombres de invocador de tus amigos en la lista `FRIENDS`:

```python
FRIENDS = ["Chirla", "Volandeira", "Mejill0n", "Elfsmen", "XzQiyanaYuntalXz"]
```

### 5. Arranca el bot

Abre el cliente de LoL y ejecuta:

```bash
python -u monitor.py
```

Listo. Ahora sientate y espera. Cuando alguno de tus colegas se conecte, lo sabras.

## Modos de envio

El bot soporta 3 modos de mensajeria (se cambia en `config.py`):

| Modo | `MESSAGING_SERVICE` | Descripcion |
|------|-------------------|-------------|
| **Telegram** | `"telegram"` | Bot de Telegram oficial. Seguro y recomendado. |
| **Clipboard** | `"clipboard"` | Copia el mensaje y lo pega en la ventana activa (WhatsApp Web). Inarrastreable. |
| **WhatsApp** | `"whatsapp"` | Via whatsapp-web.js. Funciona pero riesgo de baneo. No recomendado. |

## Estructura

```
sale-lolcito/
├── monitor.py           # Bucle principal
├── config.py            # Configuracion (amigos, modo, etc.)
├── lcu.py               # Conexion a la LCU API del cliente de LoL
├── telegram_client.py   # Envio via Telegram
├── clipboard_client.py  # Envio via portapapeles (Ctrl+V + Enter)
├── whatsapp_client.py   # Envio via servicio Node.js
├── whatsapp-service/    # Servidor WhatsApp (opcional)
├── requirements.txt
└── .env                 # Credenciales (no se sube al repo)
```

## Por Demacia!
