<h1 align="center">🤖 Telegram Userbot</h1>
<p align="center">
  Auto Message Sender | Heroku Deploy | Pyrogram-based Userbot
</p>

---

<p align="center">
  <a href="https://github.com/babaji067/userbot/fork">
    <img src="https://img.shields.io/github/forks/babaji067/userbot?style=social" alt="Forks">
  </a>
  <a href="https://github.com/babaji067/userbot/stargazers">
    <img src="https://img.shields.io/github/stars/babaji067/userbot?style=social" alt="Stars">
  </a>
  <a href="https://github.com/babaji067/userbot">
    <img src="https://img.shields.io/github/repo-size/babaji067/userbot?color=blue" alt="Repo Size">
  </a>
</p>

---

## ✨ Features

✅ Auto send any message repeatedly in any chat  
⚙️ Set time interval between each message  
✋ Start/Stop message loop with commands  
💡 Simple Telegram userbot using Pyrogram  
🚀 Deployable on Heroku in just 1 click  

---

## 💬 Telegram Commands

| Command            | Description                              |
|--------------------|------------------------------------------|
| `/setmessage`      | Set the auto message (or reply to one)   |
| `/setmute <secs>`  | Set time gap between messages            |
| `/autosend`        | Start auto message sending               |
| `/autostop`        | Stop sending messages                    |

---

## ☁️ Heroku Deployment

### 🛠 Requirements
- [x] Telegram API ID & HASH → [my.telegram.org](https://my.telegram.org)
- [x] Pyrogram Session String (see below 👇)

### 🚀 Deploy Steps

1. 🎯 Fork or clone this repo: `https://github.com/babaji067/userbot`
2. 🔧 Generate a session string (see below)
3. 🧩 Go to [Heroku](https://heroku.com) → Create new app
4. 🧪 Set config vars: `API_ID`, `API_HASH`, `SESSION_STRING`
5. 🟢 Enable the **Worker dyno**
6. 🎉 Done! Bot will start auto-sending!

---

## 🔐 Generate Session String (Required)

Paste this in Python (Replit, PC or Pydroid3):

```python
from pyrogram import Client

api_id = int(input("API ID: "))
api_hash = input("API HASH: ")

with Client(":session", api_id=api_id, api_hash=api_hash) as app:
    print("SESSION STRING:")
    print(app.export_session_string())
