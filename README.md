<h1 align="center">🤖 Telegram UserBot - Auto Message Sender</h1>

<p align="center">
  🔐 Session-based Telegram UserBot with auto messaging control via Bot commands.
</p>

<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/yourusername/userbot-heroku">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku">
  </a>
</p>

---

## 📦 Features

- 🔐 **Login your user account** with a secure Pyrogram session string
- ✏️ Set your custom auto-message with `/setmessage`
- ⏱️ Set time interval in minutes with `/settime`
- 🚀 Start/Stop message loop with `/startauto` and `/stopauto`
- 👮 Commands restricted to **OWNER only**

---

## ⚙️ Environment Variables (Heroku Config Vars)

| Variable     | Required | Description                          |
|--------------|----------|--------------------------------------|
| `API_ID`     | ✅       | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH`   | ✅       | Telegram API Hash                    |
| `BOT_TOKEN`  | ✅       | Telegram Bot Token from [@BotFather](https://t.me/BotFather) |
| `OWNER_ID`   | ✅       | Your personal Telegram user ID       |

---

## 📜 Commands (for OWNER only)

| Command             | Function                                    |
|---------------------|---------------------------------------------|
| `/login`            | Send session string to login user account   |
| `/setmessage text`  | Set custom auto-message                     |
| `/settime 5`        | Set interval in minutes                     |
| `/startauto`        | Begin automatic message sending             |
| `/stopauto`         | Stop auto message sending                   |
| `/help`             | Show all available commands                 |

---

## 🔐 Generate Your Pyrogram Session String

Run this code locally (not on Heroku):

```python
from pyrogram import Client

api_id = int(input("API ID: "))
api_hash = input("API HASH: ")

with Client(name="my_account", api_id=api_id, api_hash=api_hash) as app:
    print("Session String:\n", app.export_session_string())
