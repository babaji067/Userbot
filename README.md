<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=6e48aa,9d50bb&height=200&section=header&text=Telegram%20Userbot&fontSize=40&fontColor=ffffff" />
</p>

<h2 align="center">🤖 Telegram Auto Message Userbot</h2>

<p align="center">
  Send messages automatically from your Telegram account using <b>Heroku</b> + <b>Pyrogram</b> 💥
</p>

<p align="center">
  <a href="https://github.com/babaji067/userbot/stargazers">
    <img src="https://img.shields.io/github/stars/babaji067/userbot?color=yellow&style=for-the-badge" />
  </a>
  <a href="https://github.com/babaji067/userbot/fork">
    <img src="https://img.shields.io/github/forks/babaji067/userbot?color=orange&style=for-the-badge" />
  </a>
  <a href="https://github.com/babaji067/userbot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/babaji067/userbot?color=blue&style=for-the-badge" />
  </a>
</p>

---

## 🧠 What is this?

This is a Telegram **userbot** that runs 24/7 on Heroku and automatically sends messages to your chosen chat at regular intervals.

✅ Uses your user session  
⏰ Sends messages at intervals  
🎯 Fully customizable  
🖥️ Works in groups, channels, or private chats  
🛡️ Privacy-respecting (no logging)

---

<details>
<summary><b>💡 Features List</b></summary>

| Command              | Description                                |
|----------------------|--------------------------------------------|
| `/setmessage`        | Set the custom message to send             |
| `/setmute <seconds>` | Set the interval between messages          |
| `/autosend`          | Start sending messages                     |
| `/autostop`          | Stop auto sending                          |
| ✅ Works via reply    | Can set message by replying to any text    |
| ⚡ Fast & Lightweight | Designed for smooth deployment             |

</details>

---

## ☁️ One-Click Heroku Deploy

> Easily deploy the bot on Heroku and start sending auto messages from your account.

### 🌐 Config Vars Required:
| Variable        | Required | Description                             |
|----------------|----------|-----------------------------------------|
| `API_ID`        | ✅ Yes    | Get from [my.telegram.org](https://my.telegram.org) |
| `API_HASH`      | ✅ Yes    | Same as above                          |
| `SESSION_STRING`| ✅ Yes    | Generated from your Telegram account   |

### 🛠 How to Deploy:
1. 🔗 Fork this repo → [babaji067/userbot](https://github.com/babaji067/userbot)
2. 🔐 Generate `SESSION_STRING` (see below)
3. ⚙️ Add API_ID, API_HASH & SESSION_STRING in Heroku config vars
4. 🚀 Activate `worker` dyno
5. 🎉 Done!

---

## 🔐 Generate Session String (Safe Method)

> Run this in Replit / Termux / Pydroid3:

```python
from pyrogram import Client
api_id = int(input("API ID: "))
api_hash = input("API HASH: ")
with Client(":session", api_id=api_id, api_hash=api_hash) as app:
    print("SESSION STRING:")
    print(app.export_session_string())
