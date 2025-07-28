import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
from datetime import datetime

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = os.getenv("SESSION_STRING")
control_group = int(os.getenv("CONTROL_GROUP_ID"))

client = TelegramClient(StringSession(session), api_id, api_hash)

# Variables
auto_message = "Hello everyone!"
interval_min = 10
auto_mode = False
sent_chats = set()


@client.on(events.NewMessage(chats=control_group, pattern=r"^/setmessage (.+)"))
async def set_message(event):
    global auto_message
    auto_message = event.pattern_match.group(1)
    await event.reply(f"✅ Auto message updated to:\n\n{auto_message}")


@client.on(events.NewMessage(chats=control_group, pattern=r"^/setminute (\d{1,2})"))
async def set_interval(event):
    global interval_min
    minutes = int(event.pattern_match.group(1))
    if 1 <= minutes <= 60:
        interval_min = minutes
        await event.reply(f"✅ Message interval set to {interval_min} minutes.")
    else:
        await event.reply("⚠️ Please enter a valid number between 1-60.")


@client.on(events.NewMessage(chats=control_group, pattern=r"^/startauto"))
async def start_auto(event):
    global auto_mode
    if auto_mode:
        return await event.reply("⚠️ Auto messaging is already running.")
    auto_mode = True
    await event.reply("✅ Auto messaging started.")
    asyncio.create_task(send_periodic_messages())


@client.on(events.NewMessage(chats=control_group, pattern=r"^/stopauto"))
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
                        print(f"❌ Failed to send to {entity.title}: {e}")
        except Exception as e:
            print("Error in message loop:", e)
        await asyncio.sleep(interval_min * 60)
        sent_chats.clear()


# Detect kicked/banned
@client.on(events.ChatAction())
async def chat_kick_handler(event):
    if event.user_id == (await client.get_me()).id:
        try:
            chat = await event.get_chat()
            text = f"⚠️ Removed from group:\n\nGroup: {chat.title}\nID: `{chat.id}`"
            await client.send_message(control_group, text)
        except Exception:
            pass


print("🔁 UserBot Starting...")
client.start()
client.run_until_disconnected()
