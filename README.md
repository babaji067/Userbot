# 🤖 Telegram UserBot – Heroku Deployable

This is a **Telegram UserBot** manager bot that allows you to:

- 🔐 Login using **session string**
- 📤 Send automated messages from your user account
- ⏱ Set message interval
- ⚙️ Fully controllable with Telegram bot commands

---

## 🧠 Features

- Secure **session-based login** via `/login`
- Set custom auto message: `/setmessage`
- Set interval in minutes: `/settime`
- Start/stop auto message loop: `/startauto`, `/stopauto`
- All actions only allowed by **OWNER ID**

---

## 🚀 Deploy to Heroku

### 🔧 Requirements

- [API_ID and API_HASH](https://my.telegram.org)
- [BOT_TOKEN from @BotFather](https://t.me/BotFather)
- [Session String](#-generate-session-string)

---

### 🌐 1. Fork/Clone this repository

Or download the ZIP and upload it to your GitHub.

---

### 🔁 2. Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

🔌 Set the following config vars:

| Variable     | Description                             |
|--------------|-----------------------------------------|
| `API_ID`     | Your Telegram API ID                    |
| `API_HASH`   | Your Telegram API Hash                  |
| `BOT_TOKEN`  | Bot Token from @BotFather               |
| `OWNER_ID`   | Your Telegram user ID (not bot ID)      |

---

## 🔐 Generate Session String

Run the following Python code **locally** to get your session string:

```python
from pyrogram import Client

api_id = int(input("API ID: "))
api_hash = input("API HASH: ")

with Client(name="my_account", api_id=api_id, api_hash=api_hash) as app:
    print("Session String:\n", app.export_session_string())
