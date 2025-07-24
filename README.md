<h1 align="center">🚀 Telegram UserBot – Auto Message System</h1>

<p align="center">
  <img src="https://img.shields.io/github/repo-size/babaji067/Userbot?color=blue&style=flat-square">
  <img src="https://img.shields.io/github/stars/babaji067/Userbot?style=flat-square">
  <img src="https://img.shields.io/github/forks/babaji067/Userbot?style=flat-square">
</p>

<p align="center">
  Telegram UserBot that runs on your account and sends scheduled auto messages.<br>
  Control it via your own Telegram bot with simple commands.
</p>

<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/babaji067/Userbot">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku">
  </a>
</p>

---

## 📦 Features

- 🔐 **Secure login via session string**
- 💬 **Send auto messages** on interval
- ⏱️ **Custom time setting** via `/settime`
- 🛑 **Start/Stop** messaging anytime
- 👑 Only owner has control access
- ⚡ Built using **Pyrogram 2.x**

---

## 📘 Commands

| Command | Description |
|--------|-------------|
| `/login` | Login your Telegram account using session |
| `/setmessage your text` | Set the message that will auto-send |
| `/settime 10` | Set time interval in minutes |
| `/startauto` | Start sending message loop |
| `/stopauto` | Stop auto messaging |
| `/help` | Show help menu |

---

## 🔐 Environment Variables (Heroku Setup)

| Variable | Required | Description |
|----------|----------|-------------|
| `API_ID` | ✅ Yes | From https://my.telegram.org |
| `API_HASH` | ✅ Yes | From https://my.telegram.org |
| `BOT_TOKEN` | ✅ Yes | From @BotFather |
| `OWNER_ID` | ✅ Yes | Your Telegram User ID (not username) |

---

## 🧪 Generate Session String

> Run below script in your Python terminal (PC / Android / Replit):

```python
from pyrogram import Client
api_id = int(input("API_ID: "))
api_hash = input("API_HASH: ")
with Client("my", api_id, api_hash) as app:
    print(app.export_session_string())
