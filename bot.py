from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
OWNER_ID = int(os.getenv("OWNER_ID"))

auto_message = "Hello, this is auto-message!"
auto_interval = 2  # in minutes
auto_running = False

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, in_memory=True)


@app.on_message(filters.command("setmessage") & filters.user(OWNER_ID))
async def set_message(_, msg: Message):
    global auto_message
    if len(msg.command) < 2:
        await msg.reply("❌ Usage: `/setmessage Your message`", quote=True)
        return
    auto_message = msg.text.split(" ", 1)[1]
    await msg.reply(f"✅ Auto message set to:\n`{auto_message}`", quote=True)


@app.on_message(filters.command("setminute") & filters.user(OWNER_ID))
async def set_interval(_, msg: Message):
    global auto_interval
    if len(msg.command) < 2 or not msg.command[1].isdigit():
        await msg.reply("❌ Usage: `/setminute 5`", quote=True)
        return
    auto_interval = int(msg.command[1])
    await msg.reply(f"✅ Auto interval set to: `{auto_interval} minutes`", quote=True)


@app.on_message(filters.command("startauto") & filters.user(OWNER_ID))
async def start_auto(_, msg: Message):
    global auto_running
    if auto_running:
        await msg.reply("⚠️ Auto messaging already running!", quote=True)
        return
    auto_running = True
    await msg.reply("✅ Auto messaging started!", quote=True)

    while auto_running:
        try:
            async for dialog in app.get_dialogs():
                chat = dialog.chat
                if chat.type in ["supergroup", "group"]:
                    try:
                        await app.send_message(chat.id, auto_message)
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"[ERROR] {chat.id} - {e}")
            await asyncio.sleep(auto_interval * 60)
        except Exception as e:
            print(f"[MAIN LOOP ERROR] {e}")
            await asyncio.sleep(10)


@app.on_message(filters.command("stopauto") & filters.user(OWNER_ID))
async def stop_auto(_, msg: Message):
    global auto_running
    auto_running = False
    await msg.reply("🛑 Auto messaging stopped.", quote=True)


print("✅ Userbot deployed and running...")
app.run()
