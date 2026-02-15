const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const express = require("express");

const app = express();
app.use(express.json());

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  },
});

let isReady = false;

client.on("qr", (qr) => {
  console.log("Escanea este QR con WhatsApp:");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  isReady = true;
  console.log("WhatsApp conectado correctamente.");
});

client.on("disconnected", (reason) => {
  isReady = false;
  console.log("WhatsApp desconectado:", reason);
});

client.initialize();

app.post("/send", async (req, res) => {
  const { group, message } = req.body;

  if (!group || !message) {
    return res.status(400).json({ error: "Faltan campos 'group' y 'message'" });
  }

  if (!isReady) {
    return res.status(503).json({ error: "WhatsApp no está conectado todavía" });
  }

  try {
    const chats = await client.getChats();
    const chat = chats.find(
      (c) => c.isGroup && c.name.toLowerCase() === group.toLowerCase()
    );

    if (!chat) {
      return res.status(404).json({ error: `Grupo '${group}' no encontrado` });
    }

    await chat.sendMessage(message);
    console.log(`Mensaje enviado a '${group}': ${message}`);
    return res.json({ ok: true });
  } catch (err) {
    console.error("Error al enviar mensaje:", err);
    return res.status(500).json({ error: err.message });
  }
});

app.get("/health", (_req, res) => {
  res.json({ ready: isReady });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Servicio WhatsApp escuchando en http://localhost:${PORT}`);
});
