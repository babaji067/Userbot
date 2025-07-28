from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.session import StringSession
import asyncio
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
OWNER_ID = int(os.environ.get("OWNER_ID"))
STRING_SESSION = os.environ.get("STRING_SESSION")

auto_message = "Hello, this is auto-message!"
auto_interval = 2
auto_running = False

app = Client(session_name=StringSession(STRING_SESSION), api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.command("setmessage") & filters.user(OWNER_ID))
async def set_message(_, msg: Message):
    global auto_message
    if len(msg.command) < 2:
        return await msg.reply("❌ Usage: `/setmessage your message`")
    auto_message = msg.text.split(" ", 1)[1]
    await msg.reply(f"✅ Auto-message set:\n`{auto_message}`")


@app.on_message(filters.command("setminute") & filters.user(OWNER_ID))
async def set_interval(_, msg: Message):
    global auto_interval
    if len(msg.command) < 2 or not msg.command[1].isdigit():
        return await msg.reply("❌ Usage: `/setminute 5`")
    auto_interval = int(msg.command[1])
    await msg.reply(f"✅ Interval set to: `{auto_interval}` minute(s)")


@app.on_message(filters.command("startauto") & filters.user(OWNER_ID))
async def start_auto(_, msg: Message):
    global auto_running
    if auto_running:
        return await msg.reply("⚠️ Auto-messaging is already running!")
    auto_running = True
    await msg.reply("✅ Auto-messaging started.")

    while auto_running:
        try:
            async for dialog in app.get_dialogs():
                chat = dialog.chat
                if chat.type in ["supergroup", "group"]:
                    try:
                        await app.send_message(chat.id, auto_message)
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"[SEND ERROR] {chat.id} - {e}")
            await asyncio.sleep(auto_interval * 60)
        except Exception as e:
            print(f"[LOOP ERROR] {e}")
            await asyncio.sleep(10)


@app.on_message(filters.command("stopauto") & filters.user(OWNER_ID))
async def stop_auto(_, msg: Message):
    global auto_running
    auto_running = False
    await msg.reply("🛑 Auto-messaging stopped.")


@app.on_message(filters.command("status") & filters.user(OWNER_ID))
async def status(_, msg: Message):
    text = f"📊 **Auto Message Status**\n\n"
    text += f"Message: `{auto_message}`\n"
    text += f"Interval: `{auto_interval}` minute(s)\n"
    text += f"Running: {'✅ Yes' if auto_running else '❌ No'}"
    await msg.reply(text)


@app.on_message(filters.command("groups") & filters.user(OWNER_ID))
async def groups(_, msg: Message):
    text = "**📋 Joined Groups:**\n"
    count = 0
    async for dialog in app.get_dialogs():
        if dialog.chat.type in ["group", "supergroup"]:
            count += 1
            text += f"{count}. {dialog.chat.title} (`{dialog.chat.id}`)\n"
    if count == 0:
        await msg.reply("❌ No groups found.")
    else:
        await msg.reply(text)


@app.on_message(filters.command("ping") & filters.user(OWNER_ID))
async def ping(_, msg: Message):
    await msg.reply("🏓 Pong! I’m alive.")


print("✅ USERBOT RUNNING...")
app.run()
