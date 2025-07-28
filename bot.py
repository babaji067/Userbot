from pyrogram import Client, filters
import asyncio
import os
from datetime import datetime

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
MASTER_CHAT_ID = int(os.getenv("MASTER_CHAT_ID", 123456789))  # Control group/chat

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# Files for storing
GROUPS_FILE = "groups.txt"
MESSAGE_FILE = "message.txt"
TIME_FILE = "time.txt"

auto_send_running = False


def get_groups():
    if not os.path.exists(GROUPS_FILE):
        return []
    with open(GROUPS_FILE, "r") as f:
        return [int(x.strip()) for x in f if x.strip().isdigit()]


def save_group(chat_id):
    groups = get_groups()
    if chat_id not in groups:
        with open(GROUPS_FILE, "a") as f:
            f.write(f"{chat_id}\n")


@app.on_message(filters.group)
async def group_tracker(_, message):
    save_group(message.chat.id)


@app.on_message(filters.command("setmessage") & filters.chat(MASTER_CHAT_ID))
async def set_message(_, message):
    text = message.text.split(" ", 1)
    if len(text) < 2:
        await message.reply("❌ Message text missing.")
        return
    msg = text[1]
    with open(MESSAGE_FILE, "w") as f:
        f.write(msg)
    await message.reply("✅ Message saved!")


@app.on_message(filters.command("setminute") & filters.chat(MASTER_CHAT_ID))
async def set_time(_, message):
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("❌ Usage: /setminute 2")
        return
    minutes = int(parts[1])
    with open(TIME_FILE, "w") as f:
        f.write(str(minutes))
    await message.reply(f"✅ Time set to {minutes} minute(s).")


@app.on_message(filters.command("autosend") & filters.chat(MASTER_CHAT_ID))
async def start_autosend(_, message):
    global auto_send_running
    if auto_send_running:
        await message.reply("⏳ Auto send already running.")
        return

    if not os.path.exists(MESSAGE_FILE) or not os.path.exists(TIME_FILE):
        await message.reply("⚠️ Use /setmessage and /setminute first.")
        return

    with open(MESSAGE_FILE) as f:
        msg = f.read()

    with open(TIME_FILE) as f:
        minutes = int(f.read())

    auto_send_running = True
    await message.reply(f"🚀 Auto sending started every {minutes} minutes.")

    while auto_send_running:
        groups = get_groups()
        for group_id in groups:
            try:
                await app.send_message(group_id, msg)
            except Exception as e:
                print(f"❌ Failed in {group_id}: {e}")
        await asyncio.sleep(minutes * 60)


@app.on_message(filters.command("autostop") & filters.chat(MASTER_CHAT_ID))
async def stop_autosend(_, message):
    global auto_send_running
    if auto_send_running:
        auto_send_running = False
        await message.reply("🛑 Auto sending stopped.")
    else:
        await message.reply("⏸ Auto sending was not running.")


@app.on_message(filters.command("status") & filters.chat(MASTER_CHAT_ID))
async def status(_, message):
    groups = get_groups()
    total = len(groups)
    msg = "📊 **Status:**\n"
    msg += f"👥 Groups: {total}\n"
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE) as f:
            msg += f"📝 Message: `{f.read()}`\n"
    if os.path.exists(TIME_FILE):
        with open(TIME_FILE) as f:
            msg += f"⏱ Interval: {f.read()} minute(s)\n"
    msg += f"🚦 Running: {'✅ Yes' if auto_send_running else '❌ No'}"
    await message.reply(msg)


@app.on_message(filters.command("ping"))
async def ping(_, message):
    start = datetime.now()
    m = await message.reply("🏓 Pinging...")
    end = datetime.now()
    latency = (end - start).microseconds // 1000
    await m.edit(f"✅ Pong! `{latency}ms`")


app.run()
