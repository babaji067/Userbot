import os
from pyrogram import Client, filters
import asyncio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "userbot")
MASTER_GROUP_ID = int(os.getenv("MASTER_GROUP_ID"))

auto_message = "Default auto message"
delay_minutes = 1
auto_running = False

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

open("groups.txt", "a").close()

async def save_group(chat_id):
    with open("groups.txt", "r+") as f:
        groups = f.read().splitlines()
        if str(chat_id) not in groups:
            f.write(str(chat_id) + "\n")
            print(f"✅ Group saved: {chat_id}")

async def auto_send_loop():
    global auto_running
    while auto_running:
        with open("groups.txt", "r") as f:
            group_ids = f.read().splitlines()
        for group_id in group_ids:
            try:
                await app.send_message(int(group_id), auto_message)
            except Exception as e:
                print(f"❌ Failed in {group_id}: {e}")
        await asyncio.sleep(delay_minutes * 60)

@app.on_message(filters.command("setmessage") & filters.chat(MASTER_GROUP_ID))
async def set_message_handler(client, message):
    global auto_message
    try:
        auto_message = message.text.split(" ", 1)[1]
        await message.reply(f"✅ Message set:\n\n{auto_message}")
    except:
        await message.reply("❌ Usage: /setmessage Your text")

@app.on_message(filters.command("setminute") & filters.chat(MASTER_GROUP_ID))
async def set_minute_handler(client, message):
    global delay_minutes
    try:
        delay_minutes = int(message.text.split()[1])
        await message.reply(f"✅ Delay set to {delay_minutes} minute(s)")
    except:
        await message.reply("❌ Usage: /setminute 2")

@app.on_message(filters.command("autosend") & filters.chat(MASTER_GROUP_ID))
async def start_auto_send(client, message):
    global auto_running
    if not auto_running:
        auto_running = True
        await message.reply("▶️ Auto messaging started.")
        asyncio.create_task(auto_send_loop())
    else:
        await message.reply("⚠️ Already running.")

@app.on_message(filters.command("autostop") & filters.chat(MASTER_GROUP_ID))
async def stop_auto_send(client, message):
    global auto_running
    auto_running = False
    await message.reply("⏹ Auto messaging stopped.")

@app.on_message(filters.new_chat_members)
async def new_group_handler(client, message):
    await save_group(message.chat.id)

print("🚀 Userbot starting...")
app.run()
