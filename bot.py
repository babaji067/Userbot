import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.idle import idle

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
SESSION_FILE = "session.txt"

bot = Client("ManagerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_client = None
auto_task = None
auto_message = "Hello, this is an automated message."
auto_interval = 10  # minutes

async def auto_sender():
    while True:
        try:
            await user_client.send_message("me", auto_message)
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(auto_interval * 60)

async def start_userbot(session_string):
    global user_client
    user_client = Client(name="userbot", session_string=session_string, api_id=API_ID, api_hash=API_HASH)
    await user_client.start()
    print("✅ UserBot started.")

async def stop_userbot():
    global user_client
    if user_client:
        await user_client.stop()
        user_client = None
        print("🛑 UserBot stopped.")

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    await message.reply_text(
        "**🤖 Welcome to Telegram UserBot!**\n\n"
        "Use /login to send your session string.\n"
        "Only authorized owner can access commands."
    )

@bot.on_message(filters.command("login") & filters.user(OWNER_ID))
async def login_cmd(client, message: Message):
    await message.reply_text("🔐 Please send your **session string** as a reply to this message.")

@bot.on_message(filters.private & filters.reply & filters.user(OWNER_ID))
async def session_receiver(client, message: Message):
    if "session" not in message.reply_to_message.text.lower():
        return
    session = message.text.strip()
    with open(SESSION_FILE, "w") as f:
        f.write(session)
    await stop_userbot()
    await start_userbot(session)
    await message.reply_text("✅ Session loaded and userbot started!")

@bot.on_message(filters.command("setmessage") & filters.user(OWNER_ID))
async def set_message(client, message: Message):
    global auto_message
    parts = message.text.split(" ", 1)
    if len(parts) > 1:
        auto_message = parts[1]
        await message.reply_text("✅ Auto message set.")
    else:
        await message.reply_text("⚠ Usage: /setmessage Your message here")

@bot.on_message(filters.command("settime") & filters.user(OWNER_ID))
async def set_time(client, message: Message):
    global auto_interval
    parts = message.text.split(" ", 1)
    if len(parts) > 1 and parts[1].isdigit():
        auto_interval = int(parts[1])
        await message.reply_text(f"✅ Interval set to {auto_interval} minutes.")
    else:
        await message.reply_text("⚠ Usage: /settime 10")

@bot.on_message(filters.command("startauto") & filters.user(OWNER_ID))
async def start_auto(client, message: Message):
    global auto_task
    if not user_client:
        await message.reply_text("❌ Userbot not logged in.")
        return
    if auto_task is None or auto_task.done():
        auto_task = asyncio.create_task(auto_sender())
        await message.reply_text("✅ Auto messaging started.")
    else:
        await message.reply_text("⚠ Already running.")

@bot.on_message(filters.command("stopauto") & filters.user(OWNER_ID))
async def stop_auto(client, message: Message):
    global auto_task
    if auto_task and not auto_task.done():
        auto_task.cancel()
        await message.reply_text("🛑 Auto messaging stopped.")
    else:
        await message.reply_text("⚠ Auto messaging not active.")

@bot.on_message(filters.command("help") & filters.user(OWNER_ID))
async def help_command(client, message: Message):
    await message.reply_text(
        "📘 **UserBot Commands:**\n\n"
        "`/login` - Send session string\n"
        "`/setmessage your msg` - Set auto message\n"
        "`/settime 5` - Set interval (minutes)\n"
        "`/startauto` - Start auto messages\n"
        "`/stopauto` - Stop auto messages\n"
        "`/help` - Show help"
    )

async def main():
    await bot.start()
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            session = f.read().strip()
            try:
                await start_userbot(session)
            except Exception as e:
                print(f"❌ Failed to start userbot: {e}")
    print("✅ Bot is running.")
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
