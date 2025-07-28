import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Get API credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Create Pyrogram client using session string
app = Client(name="userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Global variables
auto_send = False
auto_message = "Hello!"     # Default message
auto_interval = 30          # Default interval (seconds)
target_chat = None          # Target chat to send messages

# Command: /setmessage - to set the message
@app.on_message(filters.command("setmessage"))
async def set_message(_, msg: Message):
    global auto_message
    if msg.reply_to_message:
        auto_message = msg.reply_to_message.text
        await msg.reply("✅ Message set from reply.")
    elif len(msg.command) > 1:
        auto_message = msg.text.split(None, 1)[1]
        await msg.reply("✅ Auto message updated.")
    else:
        await msg.reply("⚠️ Use like: /setmessage Hello world!")

# Command: /setmute - to set interval between messages
@app.on_message(filters.command("setmute"))
async def set_mute(_, msg: Message):
    global auto_interval
    if len(msg.command) < 2:
        return await msg.reply("⚠️ Usage: /setmute 60")
    try:
        auto_interval = int(msg.command[1])
        await msg.reply(f"✅ Interval set to {auto_interval} seconds.")
    except:
        await msg.reply("❌ Invalid number.")

# Command: /autosend - start auto messaging
@app.on_message(filters.command("autosend"))
async def start_auto_send(_, msg: Message):
    global auto_send, target_chat
    if auto_send:
        return await msg.reply("⚠️ Already sending messages.")
    auto_send = True
    target_chat = msg.chat.id
    await msg.reply(f"🚀 Started auto messaging every {auto_interval} seconds.")
    
    while auto_send:
        try:
            await app.send_message(target_chat, auto_message)
        except Exception as e:
            print(f"❌ Error: {e}")
        await asyncio.sleep(auto_interval)

# Command: /autostop - stop auto messaging
@app.on_message(filters.command("autostop"))
async def stop_auto_send(_, msg: Message):
    global auto_send
    auto_send = False
    await msg.reply("🛑 Auto messaging stopped.")

# Start the userbot
app.run()
