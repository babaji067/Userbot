import os
import asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
from datetime import datetime

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = os.getenv("SESSION_STRING")
control_group = int(os.getenv("CONTROL_GROUP_ID"))

client = TelegramClient(StringSession(session), api_id, api_hash)

auto_message = "👋 Hello, this is a default auto-message!"
interval_min = 10
auto_mode = False
sent_chats = set()

@client.on(events.NewMessage(chats=control_group, pattern=r"^/start$"))
async def start_cmd(event):
    await event.reply(
        "**👋 Welcome! Yeh Personal UserBot hai.**\n\n"
        "🛠 Available Commands:\n"
        "/setmessage <text> - Set message\n"
        "/setminute <1-60> - Set interval\n"
        "/startauto - Start auto messaging\n"
        "/stopauto - Stop auto messaging\n"
        "/help - Show commands"
    )

@client.on(events.NewMessage(chats=control_group, pattern=r"^/help$"))
async def help_cmd(event):
    await event.reply(
        "**📘 Help Menu**\n\n"
        "/start - Show welcome message\n"
        "/setmessage <text> - Custom auto message\n"
        "/setminute <1-60> - Set time in minutes\n"
        "/startauto - Begin auto-posting\n"
        "/stopauto - Stop auto-posting"
    )

@client.on(events.NewMessage(chats=control_group, pattern=r"^/setmessage (.+)"))
async def set_message(event):
    global auto_message
    auto_message = event.pattern_match.group(1)
    print(f"✅ /setmessage received: {auto_message}")
    await event.reply(f"✅ Auto-message updated:\n\n{auto_message}")

@client.on(events.NewMessage(chats=control_group, pattern=r"^/setminute (\d{1,2})"))
async def set_interval(event):
    global interval_min
    minutes = int(event.pattern_match.group(1))
    if 1 <= minutes <= 60:
        interval_min = minutes
        await event.reply(f"✅ Message interval set to {interval_min} minutes.")
    else:
        await event.reply("⚠️ Must be between 1 and 60.")

@client.on(events.NewMessage(chats=control_group, pattern=r"^/startauto$"))
async def start_auto(event):
    global auto_mode
    if auto_mode:
        return await event.reply("⚠️ Auto messaging already running.")
    auto_mode = True
    await event.reply("✅ Auto messaging started.")
    asyncio.create_task(send_periodic_messages())

@client.on(events.NewMessage(chats=control_group, pattern=r"^/stopauto$"))
async def stop_auto(event):
    global auto_mode
    auto_mode = False
    await event.reply("🛑 Auto messaging stopped.")

async def send_periodic_messages():
    global auto_mode
    while auto_mode:
        try:
            async for dialog in client.iter_dialogs():
                entity = dialog.entity
                if getattr(entity, "megagroup", False) and entity.id not in sent_chats:
                    try:
                        await client.send_message(entity.id, auto_message)
                        print(f"[{datetime.now()}] Sent to: {entity.title}")
                        sent_chats.add(entity.id)
                    except Exception as e:
                        print(f"❌ Failed to send in {entity.title}: {e}")
        except Exception as e:
            print("Loop Error:", e)
        await asyncio.sleep(interval_min * 60)
        sent_chats.clear()

@client.on(events.ChatAction())
async def kicked_from_group(event):
    if event.user_id == (await client.get_me()).id and event.left:
        chat = await event.get_chat()
        await client.send_message(
            control_group,
            f"🚫 Removed or banned from:\n**{chat.title}**\n🆔 ID: `{chat.id}`"
        )

print("🔁 UserBot Starting...")
client.start()
client.run_until_disconnected()
